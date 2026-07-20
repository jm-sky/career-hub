# CareerHub Requirements Digest
Source: career-hub-old/docs/{REQUIREMENTS,ARCHITECTURE,DATABASE,API}.md + README.md + ROADMAP.md
Purpose: reference for rebuilding as a `career`/`profile` module on the gear-stack skeleton (Vue3 + FastAPI).

---

## 1. Core domain entities

All PKs are **ULID** (`TEXT PRIMARY KEY`). Timestamps `created_at`/`updated_at` via trigger.

- **users** — extends gear-stack's existing `users` (don't rebuild): `plan` (FREE/PRO/EXPERT), `plan_expires_at`. Otherwise standard auth fields already covered by gear-stack core (email, password_hash, is_active, is_verified, tokens).
- **profiles** — 1:1 with user. `slug` (unique, public URL), `headline`, `summary`, `location`, `visibility` (PRIVATE/FRIENDS/PUBLIC), `contact` JSONB (`{email, phone, linkedin, website}`), `draft_data` JSONB (wizard-in-progress storage), `profile_photo_url`, `completeness_score` (0–100, computed).
- **experiences** — belongs to profile. Rich company fields (name, website, size, industry, location), position, employment_type, start/end date + `is_current`, `description`, `responsibilities` JSONB array of strings, `technologies TEXT[]`, `display_order`. Check constraint: `end_date > start_date`.
- **projects** — belongs to profile. name, description, `role`, dates, `is_ongoing`, `is_anonymized` + `anonymized_company` (NDA-safe sharing), `status` (Active/Staging/Archived), `category` (Demo/Internal/Production), `achievements`/`challenges`/`clients` JSONB arrays, scale fields (team_size, duration_months, users_count, budget_range), links (demo/github/docs URLs), `visibility` (PUBLIC/ANONYMOUS), `technologies TEXT[]`.
- **project_experiences** — M:N junction (project ↔ experience linking, a named requirement: "document projects separately from roles, link cross-company").
- **technologies** — global reference table (name unique, category: Framework/Library/Platform/Service/System, layer: Backend/Database/DevOps/Frontend/Language/Tools). **Note**: gear-stack already has a "Global Item Catalog" pattern (promotion-by-voting) — reuse that pattern/table shape instead of reinventing.
- **skills** — profile's relationship to a technology: `level` (1–5), `years_of_experience`, `started_using_year`, `is_primary`. Unique per (profile, technology).
- **project_technologies**, **experience_technologies** — M:N junctions technology↔project/experience.
- **education** — institution, degree, field_of_study, dates, grade, description, display_order.
- **certifications** — name, issuing_organization, credential_id/url, issue/expiry date, `is_expired` (generated column).
- **achievements** — title, description, date, category (AWARD/PUBLICATION/SPEAKING/OTHER), url, display_order.
- **cv_versions** — name, template, `sections_config` JSONB (which experiences/projects/skills/education/certs to include by ID + custom_summary + include_photo/include_summary flags), `pdf_url`, `is_default`.
- **import_history** — source (LINKEDIN/GITHUB/...), status (PENDING/PROCESSING/COMPLETED/FAILED), items_imported, error_message, raw `import_data` JSONB.
- **responsibilities_library** — AI-suggestion seed data: role_category, responsibility text, seniority_level, usage_count.
- **audit_log** — user_id, action, entity_type/id, old/new values JSONB, ip/user_agent. **Note**: gear-stack doesn't appear to have a generic audit log module — worth checking before building one from scratch, or reuse `logs` module if suitable.

**Reconsider on rebuild:**
- `technologies TEXT[]` on experiences/projects duplicates the normalized `*_technologies` junction tables — old design kept both (denormalized array for display + relational for querying). Pick one on rebuild, don't carry both.
- Row-Level Security and table partitioning sections are speculative/future — not implemented, safe to drop from planning.
- pgcrypto field-level encryption for `contact` was proposed but never implemented — decide fresh if needed.

---

## 2. API surface

Base: `/api/v1`, camelCase in/out, standard envelope (`{data, message?}` / `{error:{code,message,details?}}` / paginated `{data,pagination}`).

- **Auth**: register, login, refresh, logout, `GET /auth/me` (returns plan + profileId). *(Superseded by gear-stack's existing, more complete auth module — 2FA, OAuth, WebAuthn already there.)*
- **Profile**: `GET/PUT /profile` (own), `GET /profile/{slug}` (public, filtered to visible fields only), `POST /profile/draft` (partial wizard-step save: `{step, data}` — used for auto-save, not a full submit).
- **Experiences**: standard list/create/update/delete + `PUT /experiences/reorder` (body: ordered array of IDs — gear-stack already has an "item ordering with batch save" pattern to reuse).
- **Projects**: standard CRUD + `POST /projects/{id}/link-experience`, `POST /projects/{id}/link-skill` (explicit link endpoints, not nested payload on create).
- **Skills**: list, `POST /skills/bulk` (bulk-add, returns created/skipped counts), `GET /skills/suggestions?role=` (AI-backed).
- **CV versions**: list, create (with `sectionsConfig`), `POST /cv-versions/{id}/generate` (202 Accepted, async job → `jobId`), `GET /cv-versions/{id}/download` (binary PDF).
- **Import/Export**: `POST /import/linkedin` (multipart file upload, async 202), `POST /import/parse-text` (sync copy-paste fallback parser), `GET /export/json` (full data dump).
- **Subscription**: `GET /subscription` (plan + features + usage counters), `POST /subscription/upgrade` (Stripe payment method), `DELETE /subscription` (cancel, access continues until expiry). *(Superseded by gear-stack's Stripe billing module — reuse, don't rebuild.)*
- **Audit log**: `GET /audit-log`, paginated, per-field old/new diff.
- **AI** (Pro/Expert only): `POST /ai/optimize-description`, `POST /ai/suggest-responsibilities`, `POST /ai/analyze-profile` (match score + strengths/gaps/recommendations vs. a target role). *(gear-stack's `ai` module is chat/context-based, not text-optimization — this is a different AI use case, will need new endpoints even if reusing the provider/token-accounting plumbing.)*
- **Health**: `GET /health`.

Non-obvious business rules:
- Draft-saving is step-scoped, not whole-form (`POST /profile/draft {step, data}`), separate from the final `PUT /profile`.
- PDF generation is async (job pattern), not synchronous in the request.
- Rate limits differ by plan tier per endpoint category (auth/read/write/AI/PDF/import — see API.md table), not a single global limit.
- Free tier gets watermarked PDFs — a rendering-time flag, not a separate endpoint.

---

## 3. Key user flows / requirements

- **Profile wizard**: multi-step creation with per-step draft autosave (debounced). Manual entry OR bootstrap via LinkedIn import (HTML/data parsing) OR copy-paste text fallback parser. Completeness score shown to nudge users to fill more sections.
- **Experience**: rich per-role data incl. free-text responsibilities list (JSONB) and technology tags; user-orderable.
- **Projects**: documented independently of experiences, then explicitly linked to one or more experiences and skills — supports cross-company/portfolio projects. Anonymization: hide real company name, show a placeholder ("Fortune 500 Bank") for NDA-restricted work — this is a first-class field, not just a visibility toggle.
- **Skills**: categorized (Technical/Tools/Soft), 1–5 level, years of experience, linkable to projects; AI can suggest skills for a role (Pro/Expert).
- **CV generation**: multiple named CV versions per profile, each an explicit *selection* of which experiences/projects/skills/education/certs to include (by ID) plus optional custom summary override and template choice — i.e. CVs are curated views over the master profile, not separate documents. PDF export, watermarked on Free.
- **Public profile**: shareable at `/{slug}`, three-level visibility (Private/Friends/Public) with per-section granularity implied (only "public data" returned for experiences/projects/skills). SEO-optimized, shareable via link/QR.
- **AI features (Pro/Expert)**: optimize responsibility/description text, suggest missing responsibilities for a role+seniority, gap analysis against a target role.
- **Subscription**: Free/Pro/Expert with feature gates (CV version limits, watermark, AI access, custom domain, API access) — needs mapping onto gear-stack's existing `feature_limits` module (already handles per-role AI/storage limits — same shape, different feature keys).

Out of scope for MVP (explicitly, from old REQUIREMENTS.md — still likely true): mobile apps, team collaboration, white-label, multi-language (though gear-stack already has i18n infra, so this constraint may no longer apply/could be trivially lifted), video intros, interview prep, salary negotiation tools.

---

## 4. Architectural decisions: carry forward vs. drop

**Carry forward (product/data decisions, framework-agnostic):**
- ULID for all IDs — gear-stack already does this, no change needed.
- JSONB for flexible/evolving fields (responsibilities, achievements, sections_config) — consistent with gear-stack's own JSONB usage patterns.
- camelCase API convention — gear-stack already does this.
- Async job pattern for PDF generation (202 + jobId) — consistent with "long operation → background job" pattern.
- Plan-tiered rate limiting per endpoint category.
- Draft/step-scoped autosave for multi-step forms.
- Project anonymization as explicit product feature (not just RBAC/visibility).

**Drop entirely (React/Next.js-specific, dead on Vue rebuild):**
- React Hook Form + FormProvider + `useFieldArray` + `triggerMode: onChange` — all of career-hub-old's CLAUDE.md "critical" form guidance is void. gear-stack's form stack is **vee-validate + Zod**; follow that instead.
- Zustand (client state) — gear-stack uses Pinia.
- Next.js App Router — gear-stack uses Vue Router with module-based `routes.ts`.
- `react-beautiful-dnd` (was planned, never implemented) — if drag-and-drop reordering is wanted, check what gear-stack already uses/plans (its own FEATURES.md lists drag & drop as still "planned", so no ready-made component to borrow there).

**Re-evaluate given gear-stack now provides it:**
- Auth service (register/login/refresh/2FA/OAuth/reCAPTCHA/token blacklist) — gear-stack's is a superset of what career-hub-old built. Don't rebuild; adapt.
- Billing/Stripe — gear-stack has a working `billing` module; map Free/Pro/Expert onto its plan model instead of building `/subscription/*` from scratch.
- Feature limits — gear-stack's `feature_limits` module (per-role AI $ and storage limits) covers the same shape career-hub needs for plan-gated features.
- Storage adapter (S3/local) — gear-stack's `storage` core covers profile photos / PDFs, no need to redecide MinIO vs. S3 from scratch.
- i18n — gear-stack ships PL/EN i18n infra; career-hub-old's "multi-language out of scope for MVP" constraint can likely be dropped since it's nearly free now.

---

## 5. Open gaps (undecided, from old ROADMAP.md "Open Questions")

- **AI provider**: OpenAI vs. Anthropic was never decided. gear-stack uses OpenRouter (BYOK on Free tier) — likely the path of least resistance to reuse its `ai` module's provider plumbing, but career-hub's AI use case (text optimization/gap analysis) is structurally different from gear-stack's chat interface, so only the provider/billing plumbing carries over, not the UI/interaction pattern.
- **Payment processor**: was "Stripe likely" — now decided by inheritance, since gear-stack's billing module is already Stripe-based.
- **Deployment platform**: was undecided (Vercel+Railway floated) — moot once frontend is Vue (no more Vercel-for-Next.js rationale); should follow gear-stack's existing Docker/Nginx deployment pattern instead.
- **Monitoring**: Sentry+DataDog floated, undecided — gear-stack already wires Sentry; reuse that, DataDog was never adopted anywhere in this account's other projects (ops-monitor, gear-stack) so likely dead.
- **LinkedIn import** (Sprint 5), **CV generation/PDF** (Sprint 6), **Public profile** (Sprint 7): all marked NOT STARTED in old roadmap — these are still fully greenfield regardless of stack choice, no salvageable implementation, only the requirements above.
