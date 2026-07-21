# Career module Phase 5 (CV versions — CRUD only) — completion log

Executed 2026-07-21 per `docs/plans/career-module-plan.md` Phase 5, scoped down to
CRUD + stubs by explicit agreement: PDF rendering and Free-tier watermark gating are
deliberately deferred as their own follow-up, not bundled in here. (Both were already
flagged as blocked on separate open decisions — the PDF engine choice, and the
billing-tier rename from `free`/`pro`/`pro_plus` to `Free`/`Pro`/`Expert`.)

## Backend

New `cv_versions` table via `backend/migrations/005_add_career_cv_versions.py`. Model
`CvVersionDB` in `db_models.py`. Same per-entity repository/service/router split as
prior phases (`cv_version_repository.py`, `cv_version_service.py`,
`cv_version_router.py`), wired into `router.py`/`dependencies.py`.

**Endpoints** (all under `/api/career`): `GET/POST /career/cv-versions`,
`PUT/DELETE /career/cv-versions/{id}`, `POST /career/cv-versions/{id}/generate`,
`GET /career/cv-versions/{id}/download`.

**Decisions made:**
- **`sections_config` is JSONB, not relational rows** — it's a snapshot of *which ids
  to select at render time* (experience/project/skill/education/certification/
  achievement ids + a custom summary override + include-photo/include-summary flags),
  not a copy of the underlying data. Matches the digest's framing of CV versions as
  curated *views* over the master profile, not separate documents.
- **Every id array in `sectionsConfig` is ownership-validated**, same rigor as
  Project's `experienceIds` in Phase 3 — added a `get_by_ids_and_profile()` bulk lookup
  to every remaining repository that didn't already have one (Project, Skill,
  Education, Certification, Achievement) specifically for this. Judged this in-scope
  for "CRUD" (not part of the deferred PDF/watermark work) since it's a real ownership
  boundary, not rendering logic — without it, one profile could reference another
  profile's private entity ids in `sectionsConfig`, which is a correctness/security
  concern regardless of whether a PDF is ever produced from it.
- **`CvVersionResponse` uses `model_validate(cv_version_db)` directly** — no manual
  `_build_response()` needed, unlike Experience/Project/Skill in earlier phases. Those
  needed manual construction only because of M:N-junction-derived fields
  (`technologies`, `experienceIds`) that don't exist as direct ORM attributes.
  `CvVersionDB` has no junctions of its own — `sections_config` is just a JSONB column
  that Pydantic validates into `CvSectionsConfig` automatically once the field's alias
  is set to `sections_config`.
- **Single-default enforcement**: `CvVersionRepository.clear_default()` unsets
  `is_default` on every other CV version for the profile whenever one is created or
  updated with `isDefault: true`. Verified both directions via curl (creating a second
  default un-defaults the first; updating the first back to default un-defaults the
  second).
- **`generate`/`download` are honest stubs, not fakes**: `generate` returns
  `202 Accepted` + a `jobId` (a bare ULID, not tracked anywhere — there is no job
  queue) so the frontend has a stable contract to build against later. `download`
  always 404s right now, since `pdf_url` is never set by any code path — it doesn't
  pretend a PDF exists. The frontend surfaces this as an explicit toast
  ("PDF generation is not implemented yet...") rather than silently failing.

## Frontend

`CvVersionsPage.vue` + `CvVersionFormDialog.vue`, following the established
list-plus-form-dialog pattern. New shared `SectionIdPicker.vue` — a clickable-row
checkbox list, reused six times in one dialog (experiences/projects/skills/education/
certifications/achievements) to avoid six copies of the same markup.

**Real bug found via browser smoke-test:** `SectionIdPicker`'s original markup put the
`Checkbox` and its label `<span>` as siblings with no shared click handler — clicking
the label text (the natural thing a user does, and what standard checkbox/label
semantics support) did nothing, only clicking the checkbox square itself worked. Fixed
by making each row a `<button>` that calls `toggle()`, with the `Checkbox` inside marked
`pointer-events-none` (purely visual) so the row's own click handler is the single
source of truth — avoids a double-toggle if both the row and the checkbox tried to
handle the same click.

## Concurrent-edit note (significant — read before touching cv_versions again)

Partway through this phase, a **separate, concurrent session added a full `languages`
entity** (table, migration 006, repository/service/router, frontend page/dialog/
composable) and — critically — **patched `CvSectionsConfig` in both `schemas.py` and
`cvVersion.type.ts` to add `languageIds`, and patched `CvVersionFormDialog.vue` to add
a seventh "Languages" section picker**, all while this phase's CV-versions work was
still in progress in the same working tree. This briefly produced a real 500 (the
service referenced `sections.languageIds` before the schema had the field) that
resolved itself once both sides landed. Read `career_hub_next_steps.md` memory for the
full timeline. Practical upshot: **`cv_version_service.py`'s `_validate_sections_config`
and `CvSectionsConfig` now have 7 id-array fields, not 6** — if adding an eighth
entity type later, follow the same pattern (repository `get_by_ids_and_profile` +
schema field + service validation tuple + frontend `SectionIdPicker`), and check
whether another session might be doing the same thing at the same time before
assuming a file's current shape.

## Verification

Backend: `black`/`mypy` clean (same pre-existing `no-any-return` baseline pattern,
now also present in the new `cv_version_repository.py` and one place in
`cv_version_service.py` — consistent, not a new class of issue). Full curl pass:
create with a valid experienceId, reject a bogus experienceId (400), single-default
enforcement in both directions, generate stub (202+jobId), download before generation
(404), update rejecting a bad id in `sectionsConfig` (400), delete-then-delete-again
(204→404). Frontend: `pnpm type-check`, `pnpm lint`, `pnpm test:run` (40/40, same
baseline). Full Playwright browser pass: create an experience, create a CV version
selecting it via the (fixed) section picker with a custom summary and `isDefault`
checked, confirm the saved card and "Default" badge, trigger `generate` and confirm the
honest stub toast.

## Follow-ups flagged, not resolved

- **PDF rendering engine** — still undecided (WeasyPrint vs ReportLab vs other).
  Blocks turning `generate`/`download` into something real.
- **Billing tier rename** (`free`/`pro`/`pro_plus` → `Free`/`Pro`/`Expert`) — still not
  done. Blocks Free-tier watermark gating specifically, independent of the PDF engine
  choice.
- No automated tests for the career module (Phases 1–5) — flagged every phase, still
  the single biggest gap.
- `template` is a free-text field with four cosmetic placeholder options
  (default/modern/classic/minimal) in the Select — none of them render differently
  yet, since there's no rendering pipeline. Revisit once the PDF engine is chosen.
