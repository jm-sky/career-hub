# Career module Phase 4 (Education, Certifications, Achievements) — completion log

Executed 2026-07-21 per `docs/plans/career-module-plan.md` Phase 4.

## Backend

New tables via `backend/migrations/004_add_career_education_certifications_achievements.py`:
`education`, `certifications`, `achievements`. Models in `db_models.py`
(`EducationDB`, `CertificationDB`, `AchievementDB`). Simpler than Phases 2/3 — no
technology linking, no junction tables, per the plan doc's "straightforward CRUD, no
special business rules beyond the digest." Same per-entity repository/service/router
split as before, wired into `router.py` and `dependencies.py`.

**Endpoints** (all under `/api/career`): `GET/POST /career/education`,
`PUT/DELETE /career/education/{id}`, `PUT /career/education/reorder`; same shape for
`/certifications` and `/achievements`.

**Decisions made:**
- **No `is_current`/`is_ongoing` flag on education** — unlike experiences/projects, the
  digest doesn't list one for education. A nullable `end_date` means "still studying,"
  reusing the same "null = ongoing" convention without adding a field the digest didn't
  ask for.
- **`is_expired` on certifications is computed at the service/response layer, never
  stored** — `_is_expired(expiry_date) = expiry_date is not None and expiry_date < date.today()`,
  recomputed on every read. This was already the explicit plan-doc decision (overriding
  the digest's "generated column" suggestion) carried over from the original data-model
  notes; Phase 4 just implements it.
- **`AchievementCategory` is a genuine dedicated union type**
  (`AWARD`/`PUBLICATION`/`SPEAKING`/`OTHER`) — unlike `Experience.employmentType` (free
  text) or `Project.status`/`category`, this one has a fixed, digest-specified set of
  values on both backend (`Literal`) and frontend (dedicated TS union), matching the
  project's general "dedicated union types over inline ones" convention where the value
  set is actually fixed.
- **Client-side date-order validation added to `education.schema.ts` and
  `certification.schema.ts`** (`.refine()`, matching the pattern already used in
  `experience.schema.ts`/`project.schema.ts`) — these were initially missed since Phase
  4's entities don't have an "is ongoing" checkbox forcing the same date logic into view;
  added during self-review before the live smoke test, not found by a tool.

## A real, reproducible bug found via the backend smoke test (not by black/mypy)

`AchievementResponse`, `CreateAchievementRequest`, and `UpdateAchievementRequest` all
declare a field literally named `date` typed as `date | None` (matching the digest's
field name and the DB column). This crashes the entire app at import time with
`TypeError: unsupported operand type(s) for |: 'FieldInfo' and 'NoneType'`.

**Root cause**: for a class-body statement `name: annotation = value`, CPython binds
`value` to `name` in the class namespace *before* evaluating `annotation`. When `name`
and a bare type used in `annotation` are the same identifier (`date: date | None = ...`),
the annotation's `date` resolves to the just-bound `FieldInfo` instance instead of the
imported `datetime.date` type — a self-shadowing footgun, not a pydantic-specific bug.
`AchievementDB.date: Mapped[date | None]` in `db_models.py` has the exact same shape and
is subject to the same mechanism, but doesn't crash: `MappedColumn` happens to implement
`__or__` (for SQL OR-expressions), so `MappedColumn_instance | None` silently produces an
unused expression object instead of raising — meaning this exact pattern was already
latent in `db_models.py` and would have crashed the moment anyone added an equivalent
Pydantic field. mypy did not flag either occurrence (it resolves annotations statically
from source, not by replicating CPython's runtime name-binding order).

**Fix**: added `from datetime import date as _Date` and used `_Date` (not `date`) in the
annotation for all four occurrences (3 in `schemas.py`, 1 in `db_models.py`), keeping the
field/column name as `date`. General lesson for this codebase: never name a Pydantic or
SQLAlchemy field identically to a bare type name used in its own annotation — alias the
type import instead of renaming the field.

## Frontend

`EducationPage.vue`/`CertificationsPage.vue`/`AchievementsPage.vue` +
`EducationFormDialog.vue`/`CertificationFormDialog.vue`/`AchievementFormDialog.vue`,
following the Experience/Project page pattern (list + reorder arrows + edit/delete +
form dialog). New types/services/composables per entity. Routes (`/education`,
`/certifications`, `/achievements`) + sidebar nav entries added. No checkboxes in any of
these three dialogs — the Phase 2/3 `componentField`-on-`Checkbox` gotcha (documented in
memory) simply didn't come up this phase.

## Verification

Backend: `black`/`mypy` clean (same ~9 pre-existing `no-any-return` findings, one per
repository file including the three new ones — consistent, not a new class of issue).
Full curl pass against the dockerized app for all three entities: create, `isExpired`
true/false on certifications with future/past expiry, invalid category (422), bad dates
(400) for both education and certifications, reorder, delete-then-delete-again
(204 → 404). Frontend: `pnpm type-check`, `pnpm lint`, `pnpm test:run` (40/40, same
baseline). Full Playwright browser pass creating one entry of each of the three types,
confirming saved-card rendering including the certification "Expired" badge and the
achievement category badge.

**Session note**: the dockerized Postgres/Redis containers and their named volumes were
removed and recreated mid-session (not by this agent — the user paused to reclaim
resources, "back in ~15 minutes"). Work continued on static verification
(type-check/lint, a self-review pass that caught the two missing `.refine()` date
checks above) while waiting, then migrations 001–004 and the test user were recreated
from scratch once containers came back, and the full live smoke test ran clean against
the fresh database.

## Follow-ups flagged, not resolved

- No automated tests for the career module (Phases 1–4) — flagged every phase, still
  the single biggest gap as the module grows.
- Completeness score (Phase 1) still doesn't weigh experiences/skills/projects/
  education/certifications/achievements.
- `StringListInput.vue` (Phase 3) still duplicates `ExperienceFormDialog`'s inline
  responsibilities list logic — unchanged this phase, not touched.
