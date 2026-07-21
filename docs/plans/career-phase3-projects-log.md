# Career module Phase 3 (Projects) — completion log

Executed 2026-07-21 per `docs/plans/career-module-plan.md` Phase 3.

## Backend

New tables via `backend/migrations/003_add_career_projects.py`: `projects`,
`project_experiences` (M:N to experiences), `project_technologies` (M:N to
technologies, reusing Phase 2's shared reference table). Models in `db_models.py`
(`ProjectDB`, `ProjectExperienceDB`, `ProjectTechnologyDB`). Followed Phase 2's
per-entity split: `project_repository.py` (+ `ProjectExperienceRepository` /
`ProjectTechnologyRepository`), `project_service.py`, `project_router.py`, wired into
the `router.py` aggregator and `dependencies.py` (`get_project_service`).

**Endpoints** (all under `/api/career`): `GET/POST /career/projects`,
`PUT/DELETE /career/projects/{id}`, `PUT /career/projects/reorder`.

**Decisions made:**
- **Deviated from the requirements digest's "explicit link endpoints" note.** The
  digest (and the original Phase 3 plan bullet) called for
  `POST /projects/{id}/link-experience` / `link-skill` as separate calls. Implemented
  instead as `technologies: string[]` and `experienceIds: string[]` fields directly on
  `CreateProjectRequest`/`UpdateProjectRequest` — full-replace semantics on update, same
  as Phase 2's experience `technologies` field. Reasoning: consistency with the
  already-shipped Phase 2 pattern beats matching the old codebase's API shape, and the
  digest's own framing note says old-codebase details are dropped, kept, or superseded
  case-by-case, not copied by default. There is no `project_skills` junction table
  either — the digest's "link-skill" wording doesn't match its own data model (only
  `project_technologies` is defined), so technologies (which skills rate) are the actual
  link target.
- **`experienceIds` are ownership-validated, not just existence-checked.**
  `ExperienceRepository.get_by_ids_and_profile()` (new method) fetches only experiences
  belonging to the requesting profile; if the count doesn't match the requested id set,
  the whole request 400s. Prevents linking someone else's experience by guessing an id.
- **Cascade delete applied correctly from the start this time.** Both
  `project_experiences.project_id` AND `.experience_id` have `ON DELETE CASCADE` (unlike
  `*_technologies` junctions, where only the profile-owned side cascades — technologies
  stay put). This was the exact class of bug found and fixed in Phase 2; getting it
  right up front here was a direct result of that lesson, and verified via the same
  curl delete-then-delete-again (204 → 404) check with no 500.
- **`visibility` reuses `ProfileVisibility` (PRIVATE/FRIENDS/PUBLIC), separate from
  `is_anonymized`/`anonymized_company`.** The digest lists project visibility as
  "PUBLIC/ANONYMOUS", which looked at first like it might conflate two concerns. Read
  in context of the digest's own emphasis that anonymization is "a first-class field,
  not just a visibility toggle," the two are orthogonal: `visibility` controls whether a
  project appears on the public profile at all (matching Profile's own three-level
  model, for consistency); `is_anonymized` is an independent redaction toggle for
  NDA-restricted work, applicable regardless of visibility level.
- **`status`/`category` are Postgres `String` columns validated by a Pydantic
  `Literal`, not a DB enum type** — same pattern as `Profile.visibility`, chosen for
  consistency and to avoid a DB migration if the value set changes later.

## Frontend

New `types/project.type.ts` (dedicated `ProjectStatus`/`ProjectCategory` union types —
these genuinely map to fixed backend `Literal`s, unlike `Experience.employmentType`
which stayed free-text), `services/projectApiService.ts`,
`composables/useProjects.ts`, `validation/project.schema.ts`, `pages/ProjectsPage.vue`,
`components/ProjectFormDialog.vue`. Route `/projects` + sidebar nav entry added.

New shared component: `components/StringListInput.vue` — extracted because
`ProjectFormDialog` needed the same "list of strings with add/remove" UI three times
(achievements/challenges/clients); inlining it thrice like `ExperienceFormDialog` did
for responsibilities would have tripled the same ~15 lines. Not retrofitted into
`ExperienceFormDialog`'s responsibilities field — out of scope for this phase, left as
future cleanup if touched again.

**Real bug found and fixed via browser smoke-testing (not caught by type-check, lint,
or curl):** every `Checkbox` bound via `<Checkbox v-bind="componentField" />` inside a
vee-validate `<FormField>` silently failed to toggle on click. Root cause: vee-validate's
`componentField` helper auto-detects a native `<input type="checkbox">` element
rendered *inside* the bound component (our shadcn `Checkbox` renders exactly one, hidden,
for native-form compatibility) and switches its binding strategy to `checked`/`change`
semantics — but our `Checkbox` component only understands `modelValue`/
`update:modelValue` (per the project's own Reka-ui convention, documented in
`CLAUDE.md`). The mismatch meant clicks never updated the bound value, while a
per-field validation error still got attached (visible as `aria-invalid="true"`, a red
label, but permanently `data-state="unchecked"`) — cosmetically only \"wrong-colored,\"
easy to miss without actually clicking it in a real browser. **This affected three
already-shipped Phase 2 checkboxes too** (`ExperienceFormDialog`'s `isCurrent`,
`SkillFormDialog`'s `isPrimary`), never caught earlier because the Phase 2 browser
smoke-test worked around `isCurrent` by filling dates directly instead of clicking the
checkbox. Fixed everywhere (all 4 checkboxes across 3 dialogs) by binding explicitly:
`:model-value="componentField.modelValue"` /
`@update:model-value="componentField['onUpdate:modelValue']"`, bypassing the
auto-detection heuristic. Verified via direct DOM attribute inspection
(`data-state`/`aria-checked` before/after click) in addition to the visual screenshot,
since the visual symptom alone (red label) is easy to misread as "just needs the right
value filled in" rather than "never toggles at all."

## Verification

Backend: `black`/`mypy` clean (same ~5 pre-existing `no-any-return` findings as Phase 2,
no new ones — and no call-arg alias mistakes this time, got the mypy/pydantic
alias-vs-field-name convention right on the first pass). Full curl pass against the
dockerized app: create with technologies + linked experience, reject foreign
`experienceIds` (400), reject bad dates (400), update replacing links, reorder, cascade
delete (204 → 404, no 500). Frontend: `pnpm type-check`, `pnpm lint`, `pnpm test:run`
(40/40, same pre-existing Playwright/vitest config clash as Phase 2, confirmed
unrelated). Full Playwright browser pass: login → open project dialog → fill every
field group (dates, both checkboxes, anonymization, achievements list, technology tag) →
submit → verify the saved card renders all of it, including the "Linked experiences"
checkbox list against real experience data.

## Follow-ups flagged, not resolved

- No automated tests for the career module (Phase 1, 2, or 3) — flagged again, still not
  addressed. Growing more overdue with each phase.
- `StringListInput.vue` duplicates `ExperienceFormDialog`'s inline responsibilities
  list logic — low priority, only worth doing if that file is touched again.
- Completeness score (Phase 1) still doesn't weigh experiences/skills/projects.
