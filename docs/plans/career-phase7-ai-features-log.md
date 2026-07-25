# Career module Phase 7 (AI features — Pro/Expert) — completion log

Executed 2026-07-25 as part of concurrent Phase 5 (CV versions CRUD) delivery.
Three domain-specific AI endpoints, distinct from the general `ai` module's chat/conversation interface.

## Backend

New `ai_router.py` and `ai_service.py` in `backend/app/modules/career/`.

**Endpoints** (all under `/api/career/ai`):
1. `POST /career/ai/optimize-description` — Rewrite a responsibility/description into achievement-oriented language.
2. `POST /career/ai/suggest-responsibilities` — Suggest responsibilities for a role/seniority (from library or AI).
3. `POST /career/ai/analyze-profile` — Gap analysis (match score + strengths/gaps) vs. target role.

**Schemas** (`schemas.py`):
- `OptimizeDescriptionRequest/Response` — input: `text`, output: `optimized`
- `SuggestResponsibilitiesRequest/Response` — input: `role`, `seniority`, output: `suggestions[]`
- `AnalyzeProfileRequest/Response` — input: `targetRole`, output: `matchScore`, `strengths[]`, `gaps[]`, `recommendations[]`

**Access Control:**
- Gate via `CareerAiUser` dependency (reuses `ai` module's `AiAccessUser` pattern).
- Checks: Pro/Expert tier via `BillingService.get_subscription_limits()` OR user has configured OpenRouter token (BYOK Free tier).
- Error: 403 if tier/token check fails; 503 if AI is disabled globally.

**Provider Integration:**
- Reuses existing `ai` module's OpenRouter plumbing (provider config, token accounting, cache).
- Three separate prompts (not a unified chat): optimizations are stateless, one-shot completions.
- Responsibilities library (`responsibilities_library` table, seeded) feeds `suggest-responsibilities` as examples/context.

## Frontend

No new UI in Phase 7 — endpoints are contract-only in this phase. Frontend integration (UI forms, response rendering) deferred to after this validation. Accessible via curl/API clients for testing.

## Verification

Backend: `black`/`mypy` clean. API contract verified via curl:
- `POST /career/ai/optimize-description` with sample text → `optimized` response (non-empty string)
- `POST /career/ai/suggest-responsibilities` with role + seniority → `suggestions` array (>0 items)
- `POST /career/ai/analyze-profile` with target role → `matchScore` (0–100), `strengths/gaps/recommendations` arrays
- Access control: 403 when tier/token check fails (tested: Free tier no BYOK → 403)
- Billing gate: Pro tier → 200; Expert tier → 200; Free (no token) → 403

No regression: existing `/career/*` (profile, experiences, projects, skills, education, certifications, achievements, cv-versions) all still 200.

## Follow-ups flagged, not resolved

- **Frontend UI** — no forms/components yet to call these endpoints. Candidates: 
  - Modal/drawer in experience/project/skill edit (context-aware optimize + suggest).
  - Standalone "Analyze my profile" page (role picker → analysis card).
  - Deferred pending design feedback (responsiveness on mobile, modal complexity, etc.).
- **Responsibilities library seeding** — currently empty or minimal. Populate with domain-appropriate role categories + sample text before making `suggest-responsibilities` useful in production.
- **API token accounting** — inherits from `ai` module's cost tracking (Anthropic/OpenRouter tokens). Verify cost is correctly attributed per user/subscription tier in billing reports before launch.

## Notes

- Phase 7 arrived as a consequence of Phase 5 (CV CRUD) landing in the same session. Both are logically independent, but were implemented concurrently.
- Three endpoints are stateless, fire-and-forget — no job queue, no async tracking needed (unlike PDF generation in Phase 5, which is async 202 + jobId).
- Distinct from `ai` module's `/ai/chat` (conversation history + streaming SSE); no integration with chat context here, each API call is standalone.
