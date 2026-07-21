# Career module implementation plan

Spec source: `requirements-digest.md`. This is the living plan for building the actual
CareerHub domain (profile → experiences/projects/skills → CV generation) on top of the
now-rebranded, gear-free gear-stack skeleton. Update this file as phases complete or
decisions change — it's the map for picking the work back up across sessions.

## Conventions (confirmed from existing kept modules, follow exactly)

- **IDs:** ULID via `app.common.id_utils.generate_id()`, stored as `String(36)` primary
  keys, generated explicitly in the repository's create method (not a DB column
  default) — this is the `logs`/`auth`/`two_factor`/`tenants` module pattern. (`billing`/`ai`
  use native Postgres `UUID`/`uuid4` instead — inconsistent legacy choice, do **not**
  copy that one for new `career` tables.)
- **Module layout, backend** (`backend/app/modules/career/`): `db_models.py`,
  `repositories.py` (or split per-entity if it gets large), `schemas.py`, `service.py`,
  `router.py`, `__init__.py`. Router registered in `app/api/router.py`.
- **Module layout, frontend** (`src/modules/career/`): `pages/`, `components/`,
  `services/`, `composables/`, `types/`, `routes.ts`, `i18n/locales/{en,pl}.ts`. Routes
  merged in `src/router/routes.ts`. State via TanStack Query (server state) — no Pinia
  store needed for career data itself (career-hub has no offline/localStorage domain
  data layer, see CLAUDE.md).
- **API convention:** camelCase in/out (Pydantic schemas use camelCase field names or
  alias generators — check how `billing`/`settings` schemas do it and match), standard
  envelope. Base path `/api/v1/career/...` — confirm actual prefix convention used by
  other modules (check `app/api/router.py`) before finalizing.
- **Migrations:** start fresh at `001` (the squash left only `000_create_schema_migrations.py`
  — see `migrations-and-assets-cleanup-log.md`). One migration per phase below is fine.

## Data model (per requirements-digest §1, with the "reconsider on rebuild" calls applied)

Decisions already made in the digest, restated here so they're not re-litigated per phase:
- Drop the denormalized `technologies TEXT[]` columns on experiences/projects — normalized
  `*_technologies` junction tables only.
- No RLS, no table partitioning, no pgcrypto field encryption — dropped as speculative.
- `technologies` table reuses gear-stack's existing "Global Item Catalog" promotion-by-voting
  *pattern* (not the actual gear catalogue table/code, which is deleted) — i.e. a shared,
  de-duplicated reference table, new promotion logic if wanted, not urgent for MVP.

Tables (all ULID PK unless noted, `created_at`/`updated_at` timestamps on all):
1. `profiles` — 1:1 with `users.id`. `slug` (unique), `headline`, `summary`, `location`,
   `visibility` (PRIVATE/FRIENDS/PUBLIC enum), `contact` JSONB, `draft_data` JSONB,
   `profile_photo_url`, `completeness_score` (int 0-100, computed on write).
2. `experiences` — FK `profile_id`. company fields, `position`, `employment_type`,
   `start_date`/`end_date`/`is_current`, `description`, `responsibilities` JSONB array,
   `display_order`. Check constraint `end_date > start_date` (nullable end_date for current).
3. `projects` — FK `profile_id`. `name`, `description`, `role`, dates, `is_ongoing`,
   `is_anonymized` + `anonymized_company`, `status`, `category`, `achievements`/
   `challenges`/`clients` JSONB arrays, scale fields, links, `visibility`.
4. `project_experiences` — M:N junction, `project_id`/`experience_id`.
5. `technologies` — global reference, `name` unique, `category`, `layer`.
6. `skills` — FK `profile_id` + `technology_id`, `level` (1-5), `years_of_experience`,
   `started_using_year`, `is_primary`. Unique per (profile_id, technology_id).
7. `project_technologies`, `experience_technologies` — M:N junctions to `technologies`.
8. `education` — FK `profile_id`. institution, degree, field_of_study, dates, grade,
   description, display_order.
9. `certifications` — FK `profile_id`. name, issuing_organization, credential_id/url,
   issue/expiry date, `is_expired` (computed, not a DB generated column — compute in
   service/response layer for portability, avoid DB-specific generated columns).
10. `achievements` — FK `profile_id`. title, description, date, category, url, display_order.
11. `cv_versions` — FK `profile_id`. name, template, `sections_config` JSONB (selected
    experience/project/skill/education/cert IDs + custom_summary + include flags),
    `pdf_url`, `is_default`.
12. `import_history` — FK `profile_id`. source, status, items_imported, error_message,
    `import_data` JSONB.
13. `responsibilities_library` — global seed/reference, not per-profile. role_category,
    responsibility text, seniority_level, usage_count. (AI-suggestion seed data — low
    priority, can stub/defer.)

## Phased build order

**Phase 1 — Profile (this is the anchor, build first):**
- Backend: `profiles` table + migration, repository, service (incl. completeness-score
  calculation), schemas (`ProfileResponse`, `UpdateProfileRequest`, `ProfileDraftRequest`),
  router (`GET/PUT /career/profile` own, `GET /career/profile/{slug}` public — filtered,
  `POST /career/profile/draft` step-scoped autosave per digest §2).
- Frontend: types, service (axios calls), composable (`useProfile`), `routes.ts`, i18n,
  a real `ProfileEditPage.vue` (can be a simple single-page form first, wizard/step-based
  UX is a refinement, not a blocker for the vertical slice).
- Wire `profiles` into `MODEL_MODULES` in `backend/cli/commands/db.py`.

**Phase 2 — Experiences + Technologies + Skills:**
- `experiences`, `technologies`, `skills`, `experience_technologies` tables/migration.
- Standard list/create/update/delete + `PUT /experiences/reorder` (batch reorder — check
  if gear-stack's item-ordering pattern left any reusable pieces before writing fresh,
  per digest §2 "gear-stack already has an item ordering with batch save pattern to reuse"
  — verify this actually survived the module strip; if not, write fresh, it's simple).
- Skills: list, `POST /skills/bulk`, `GET /skills/suggestions?role=` (AI-backed — stub
  returning empty/static list until the `ai` integration phase).

**Phase 3 — Projects + junctions:**
- `projects`, `project_experiences`, `project_technologies` tables/migration.
- CRUD + `POST /projects/{id}/link-experience`, `POST /projects/{id}/link-skill`.

**Phase 4 — Education, Certifications, Achievements:**
- Straightforward CRUD tables/migration, no special business rules beyond what's in
  the digest.

**Phase 5 — CV versions:**
- `cv_versions` table/migration. List/create with `sectionsConfig`.
- `POST /cv-versions/{id}/generate` — 202 + jobId, async PDF job (digest §2). PDF
  rendering engine choice not yet decided — flag as an open question, don't block the
  rest of the module on it; the endpoint can accept the request and stub/queue before
  the actual renderer is wired up.
- `GET /cv-versions/{id}/download` — binary PDF, watermark on Free tier (feature_limits
  gate — see the open billing-tier-rename item in `gear-module-strip-log.md`, this
  endpoint's gating logic depends on that being resolved first).

**DONE 2026-07-21 (CRUD only, deliberately split from the above):** table/migration,
full CRUD, single-default enforcement, `sectionsConfig` ownership validation. `generate`
returns 202+jobId but never renders a PDF; `download` 404s honestly. See
`career-phase5-cv-versions-log.md`.

**Billing-tier rename + watermark gating — DONE 2026-07-21** (separate follow-up task,
not bundled into the CRUD work above): `pro_plus` → `expert` renamed everywhere, limits
redesigned to CareerHub dimensions, `generate` now resolves and returns a `watermark:
bool` flag from the caller's subscription tier via `BillingService.get_subscription_limits`
(defaults to `true`/watermarked if no subscription row exists yet). Still open: the
PDF engine (WeasyPrint, decided but not implemented) — `generate`/`download` remain
stubs until that's wired up, at which point the renderer should just read this flag
rather than re-deriving it.

**Phase 6 — Import/Export:**
- `import_history` table/migration. `POST /import/linkedin` (multipart, async 202),
  `POST /import/parse-text` (sync fallback parser), `GET /export/json`.

**Phase 7 — AI features (Pro/Expert):**
- `POST /ai/optimize-description`, `POST /ai/suggest-responsibilities`,
  `POST /ai/analyze-profile`. Reuse the existing `ai` module's provider/token-accounting
  plumbing (OpenRouter) — this is a *different* use case from that module's chat
  interface (digest §5), so new endpoints, not new UI chat pattern.
- `responsibilities_library` seed data feeds `suggest-responsibilities`.

**Phase 8 — Public profile polish:**
- `GET /profile/{slug}` already exists from Phase 1; this phase is about the *public*
  frontend page rendering (SEO meta tags, QR/share link, per-section visibility
  filtering already enforced server-side).

## Open questions (flag before the relevant phase, don't block earlier phases on these)

- PDF rendering engine — **DECIDED: WeasyPrint.** Not yet implemented; `generate`/
  `download` are still stubs. This is the next open item for Phase 5.
- ~~Feature-limits tier rename~~ — **DONE 2026-07-21.** `free`/`pro`/`pro_plus` →
  `free`/`pro`/`expert` end-to-end (backend + frontend + Stripe env vars), and the
  limits redesigned to `cvVersionsLimit`/`pdfWatermark`/`customDomain`/`apiAccess`
  per the Free/Pro/Expert table below. Watermark gating is wired into the
  `generate` stub (see Status section). See `gear-module-strip-log.md` for full detail.

  | | Free | Pro | Expert |
  |---|---|---|---|
  | CV versions | 1 | 10 | Unlimited |
  | Watermarked PDF | Yes | No | No |
  | AI features | No | Yes | Yes |
  | Custom domain | No | No | Yes |
  | API access | No | No | Yes |
- LinkedIn import parsing approach (official API vs. HTML scrape vs. user-exported data
  archive) — Phase 6, genuinely undecided per the old ROADMAP.
- Sensitive numeric fields (`usersCount`, `teamSize`) on shared/public profiles may need
  a descriptive-display mode: store the real number, but let the owner flag it per-field
  (e.g. `usersCountDisplayMode` / `teamSizeDisplayMode`: `EXACT|DESCRIPTIVE`) so the API
  returns a bucketed label ("dozens", "hundreds", "thousands", ...) instead of the
  precise value on public output. Raised while seeding real project data where several
  source values were only ever qualitative words to begin with. Touches Phase 3
  (`projects` schema) and Phase 8 (public profile rendering).

## Status

- [x] Phase 1 — Profile (see `career-phase1-profile-log.md`)
- [x] Phase 2 — Experiences/Technologies/Skills (see `career-phase2-experiences-log.md`)
- [x] Phase 3 — Projects (see `career-phase3-projects-log.md`)
- [x] Phase 4 — Education/Certifications/Achievements (see `career-phase4-education-log.md`)
- [x] Phase 5 — CV versions, CRUD only (see `career-phase5-cv-versions-log.md`; PDF generation/watermark gating deliberately deferred)
- [ ] Phase 6 — Import/Export
- [ ] Phase 7 — AI features
- [ ] Phase 8 — Public profile polish
