# Career module Phase 2 (Experiences/Technologies/Skills) — completion log

Executed 2026-07-21 per `docs/plans/career-module-plan.md` Phase 2.

## Backend

New tables via `backend/migrations/002_add_career_experiences_technologies_skills.py`:
`technologies`, `experiences`, `experience_technologies` (M:N junction), `skills`. Models
in `backend/app/modules/career/db_models.py` (`TechnologyDB`, `ExperienceDB`,
`ExperienceTechnologyDB`, `SkillDB`).

**Module split:** Phase 1's single `router.py`/`repository.py`/`service.py` were getting
crowded, so Phase 2 split per-entity: `experience_repository.py` (+
`ExperienceTechnologyRepository` for the junction), `technology_repository.py`,
`skill_repository.py`; matching `*_service.py` files; matching `*_router.py` files. The
original `router.py` became `profile_router.py`, and a new `router.py` just aggregates
all four sub-routers (`include_router`) — same pattern `app/api/router.py` already uses
at the top level. `dependencies.py` gained a shared `CurrentProfile` dependency
(`get_current_profile`) so every Phase 2+ router gets the owning profile without
repeating the get-or-create call.

**Endpoints** (all under `/api/career`):
- `GET/POST /career/experiences`, `PUT/DELETE /career/experiences/{id}`,
  `PUT /career/experiences/reorder`.
- `GET /career/technologies?q=&limit=` — search/list the shared reference table.
- `GET/POST /career/skills`, `POST /career/skills/bulk`, `PUT/DELETE /career/skills/{id}`,
  `GET /career/skills/suggestions?role=` (stub, returns `[]` until Phase 7).

**Decisions made:**
- **Technologies are get-or-create by name, case-insensitively.** Both experiences
  (`technologies: string[]` names) and skills (`technologyName: string`) accept free-form
  names; `TechnologyService.resolve_by_name(s)` looks up case-insensitively
  (`func.lower(name) == name.lower()`) before creating, so "Python" and "python" resolve
  to the same row. Powers a tag-input UX without a separate "manage technologies" screen.
- **Experience `technologies` on update fully replaces the set** (not merged) when the
  field is provided at all; omitting it from the payload leaves technologies untouched.
  Matches how the frontend's tag input works (it always sends the complete current list).
- **`experience_technologies.experience_id` has `ON DELETE CASCADE`;
  `technology_id` does not.** Found via manual smoke-testing, not code review: deleting an
  experience 500'd with a `ForeignKeyViolationError` because the junction FK had no
  cascade. Technologies are shared reference data and must never be deleted as a side
  effect of unlinking one experience, so only the experience side cascades.
- **Skill uniqueness is per (profile, technology)** — `POST /skills` 409s if one already
  exists for that technology (use `PUT /skills/{id}` instead). `POST /skills/bulk` has no
  such restriction — it upserts by technology, since bulk import (future LinkedIn import,
  Phase 6) is expected to send overlapping data.
- **Reorder is all-or-nothing.** `PUT /experiences/reorder` requires `orderedIds` to be
  exactly the profile's existing experience ids (same set, same length) — a partial or
  stale list 400s rather than silently reordering a subset or dropping ids.
- **mypy + pydantic gotcha:** building `ExperienceResponse`/`SkillResponse` manually
  (not via `model_validate(orm_obj)`, since there's no SQLAlchemy `relationship()` for
  the M:N technologies) must use the schema's snake_case **aliases** as constructor
  kwargs, not the camelCase field names — mypy's pydantic plugin only recognizes the
  alias in the synthesized `__init__`, even with `populate_by_name=True` set. Runtime
  pydantic accepts either; mypy only accepts the alias form. See the comment in
  `experience_service.py`/`skill_service.py`'s `_build_response()`.
- **No dedicated tests added** — Phase 1 shipped without a `tests/modules/career/`
  suite either, so Phase 2 matches that (unintentional) precedent rather than
  introducing tests for only half the module. Flagging here since it should probably be
  addressed as its own task before the module gets much bigger.

## Frontend

New `src/modules/career/`: `types/{technology,experience,skill}.type.ts`,
`services/{technology,experience,skill}ApiService.ts`,
`composables/{useTechnologies,useExperiences,useSkills}.ts` (TanStack Query, following
Phase 1's `useProfile.ts` pattern exactly — plain functions returning
query/mutation objects, no Pinia store), `validation/{experience,skill}.schema.ts`
(zod), new pages `ExperiencesPage.vue` / `SkillsPage.vue`, and shared components:
`TechnologyCombobox.vue` (single-select, creatable, backed by the shared `ui/combo-box`),
`TechnologyTagInput.vue` (multi-select wrapper around the combobox + removable
`Badge` chips), `ExperienceFormDialog.vue`, `SkillFormDialog.vue`,
`DeleteConfirmDialog.vue` (generic confirm dialog, title/description as props).
Routes (`/experiences`, `/skills`) added to `routes.ts` and wired into `AppSidebar.vue`
nav (previously only had the Profile link).

**Decisions made:**
- **`employmentType` is a free-text field, not an enum**, matching the backend column
  (`String(30)`, no fixed set of values in the requirements digest) — an earlier pass
  used a dedicated `EmploymentType` union type per the global TypeScript convention, but
  that was reverted since the UI is a plain text `Input`, not a `Select`; a union type
  there would have been a false type-safety signal not backed by real validation.
  Revisit if the product actually wants a fixed dropdown later.
- **Reordering uses up/down arrow buttons, not drag-and-drop.** Simpler to implement
  correctly and test; the backend's all-or-nothing reorder endpoint doesn't care how the
  new order was produced.
- **Responsibilities and technologies are plain local `ref` arrays inside
  `ExperienceFormDialog`, not vee-validate/zod-managed fields** — vee-validate doesn't
  have a natural array-field UI, so they're merged into the submit payload alongside the
  validated scalar fields rather than forcing them through the schema.
- **`common.add` / `common.remove` added to the shared i18n locale** (`src/shared/i18n/locales/{en,pl}.ts`),
  not module-local — generic enough (used by the responsibilities list add/remove
  buttons) to belong alongside the existing `common.save`/`common.cancel`/etc.

**Bug found via browser smoke-test (not caught by type-check/lint):**
`SkillFormDialog.vue` used `<FormLabel>`/`<FormControl>` for the technology combobox
field outside of a `<FormField>` wrapper (that field is bound manually via
`setFieldValue`, not a `componentField`). Both components call `useFormField()`
internally, which throws if there's no ancestor `<FormField>` providing context — this
doesn't surface in vue-tsc or ESLint, only at runtime, and specifically broke the *skill*
create dialog (the experience dialog's equivalent `isCurrent` checkbox field is correctly
inside a `<FormField>`, so it was unaffected). Fixed by using a plain
`<Label>` + `<div>` for that one manually-bound field instead. Verified via a full
Playwright-driven browser pass (login → create experience with dates/responsibilities/
technology tag → create skill) after the fix; screenshots not kept (dev-scratch only).

## Verification

Backend: `black`/`mypy` clean (mypy's remaining ~5 `no-any-return` findings in the new
repository files match the exact pre-existing pattern already present in Phase 1's
`repository.py` — not a new class of issue). Ran the full CRUD + edge-case surface via
curl against the dockerized app + Postgres: case-insensitive technology dedup, reorder
(valid + invalid-id-set), date validation (`endDate > startDate`), skill uniqueness
conflict (409), bulk upsert, cascade delete, 404s on second delete. Frontend:
`pnpm type-check`, `pnpm lint`, `pnpm test:run` (40/40 unit tests, same count as Phase 1
baseline — the one failing suite is a pre-existing Playwright/vitest config clash
unrelated to this work, confirmed by reproducing it on `develop` before any Phase 2
changes). Manually exercised both new pages in a real browser via Playwright.

## Follow-ups flagged, not resolved

- No automated tests for the career module at all yet (Phase 1 or 2) — worth doing as
  its own task rather than folding into Phase 3.
- Completeness score (`service.py`, Phase 1) still doesn't weigh experiences/skills —
  flagged again in Phase 1's log, still not extended.
- Technology search (`GET /career/technologies?q=`) is not live/reactive from the
  tag-input UI yet — `TechnologyCombobox` fetches a static batch once and relies on
  the `ui/combo-box` component's built-in client-side (cmdk) filtering, rather than
  hitting the API per keystroke. The composable (`useTechnologySearch`) already supports
  a reactive query ref for when/if that's wanted; wiring it up would need extending the
  shared `ui/combo-box` component to expose its internal search text (it doesn't
  currently), which felt like scope creep for a module-local component in this phase.
