# 001 — Projects have no `team` or `subProjects` fields

**Status:** Open
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

## Proposed follow-up

If this data is wanted in the UI later:

- Add `team` (JSONB list of strings) and `sub_projects` (JSONB list of
  `{name, url}`) columns to `projects`, with a migration.
- Extend `ProjectResponse` / `CreateProjectRequest` / `UpdateProjectRequest`
  (`backend/app/modules/career/schemas.py`) with `team` / `subProjects`.
- Extend the frontend `src/modules/career/types/project.type.ts` and the
  project form/detail components to expose them.

Not urgent — no current UI need beyond preserving the historical seed data
faithfully.
