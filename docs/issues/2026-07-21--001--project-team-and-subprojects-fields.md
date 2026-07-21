# 001 — Projects have no `team` or `subProjects` fields

**Status:** Fields implemented 2026-07-21 (schema, API, frontend). Seeding the
actual historical values from `madeyski.org/src/data/projects.ts` is still
open — that source file isn't available in this checkout.
**Found:** 2026-07-21, while writing `cli db seed career-projects` to load real
project history from `madeyski.org/src/data/projects.ts` into the `projects` table.

## Problem

The source data (and the site it's transcribed from) records two things per
project that `ProjectDB` / `CreateProjectRequest` / the frontend
`project.type.ts` have no field for at all:

- **`team`** — a list of colleague names who worked on the project alongside
  the owner (e.g. `["Tomasz Smykowski", "Kamil Żelechowski", "Jan Madeyski"]`).
- **`subProjects`** — a list of `{ name, url }`, used when one project is
  actually a template/platform instantiated for multiple clients (e.g. "DEV
  Made IT Template" → DEV Made IT, WIARBUD, SAVA GROUP, Kraina Snów sites).

Neither field appears anywhere in `docs/plans/*.md` as planned work. The seed
script drops both rather than force-fitting them into an existing column
(`clients`, `description`, etc.).

## Resolution (2026-07-21)

Implemented in full:

- `team` (JSONB list of strings) and `sub_projects` (JSONB list of
  `{name, url}`) columns added to `projects` via migration `007`.
- `ProjectResponse` / `CreateProjectRequest` / `UpdateProjectRequest`
  (`backend/app/modules/career/schemas.py`) extended with `team` / `subProjects`
  (new `SubProject` schema).
- `ProjectService` (`project_service.py`) reads/writes both fields on
  create/update.
- Frontend `src/modules/career/types/project.type.ts` gained `team: string[]`
  and `subProjects: SubProject[]`; `ProjectFormDialog.vue` exposes both
  (`StringListInput` for team, new `SubProjectListInput.vue` for sub-projects);
  `ProjectsPage.vue` displays both on the project card, with sub-project URLs
  rendered as links.
- i18n keys added for `en`/`pl`.
- Verified end-to-end against the live API (create → list → field values
  round-trip correctly, including non-ASCII names).

## Remaining follow-up

Seeding the *actual* historical `team`/`subProjects` values (e.g. "DEV Made IT
Template" → WIARBUD/SAVA GROUP/Kraina Snów) from
`madeyski.org/src/data/projects.ts` into `app/seeders/career_projects.py` is
still open — that source file is not present in this checkout. Once available,
extend the seeder's project dicts with `team`/`sub_projects` keys and pass them
through in `career_projects.py`.
