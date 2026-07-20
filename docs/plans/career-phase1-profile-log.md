# Career module Phase 1 (Profile) — completion log

Executed 2026-07-20 per `docs/plans/career-module-plan.md` Phase 1.

## Backend

New module `backend/app/modules/career/`: `db_models.py`, `repository.py`, `service.py`,
`schemas.py`, `router.py`, `dependencies.py`, `__init__.py`. New migration
`backend/migrations/001_add_career_profiles.py`. Registered in
`backend/cli/commands/db.py` (`MODEL_MODULES`) and `backend/app/api/router.py`.

**Endpoints** (all under `/api/career`, confirmed base path has no `/v1` — it's just `/api`,
set in `app/core/app_factory.py`):
- `GET /career/profile` — own profile, auto-creates an empty one on first access.
- `PUT /career/profile` — partial update, recomputes `completenessScore`.
- `POST /career/profile/draft` — step-scoped autosave, merges into `draftData[step]`.
- `GET /career/profile/{slug}` — public view (`PublicProfileResponse`, no contact/draft
  data ever), 404s instead of leaking existence for anything not visible.

**Decisions made:**
- **Slug strategy:** slugify the user's display name (lowercase, hyphenated) on first
  profile creation; on collision, append a random 6-hex-char suffix and retry. User can
  change it later via `PUT /profile` (`slug` field), re-validated for uniqueness
  (slugified again, so arbitrary input is still normalized).
- **Visibility/privacy defaults:** `PRIVATE` by default for new profiles. On the public
  slug endpoint, `PUBLIC` is visible to anyone, `PRIVATE`/`FRIENDS` are owner-only.
  **`FRIENDS` has no real semantics yet** — no friends/connections system exists, so it's
  currently identical to `PRIVATE`. Needs revisiting once (if) a connections feature is
  built. `contact` and `draftData` are **never** returned by the public endpoint,
  regardless of visibility — a deliberate privacy default, not just an oversight to flag.
- **Optional auth for the public endpoint:** added a module-local
  `get_optional_user_id` dependency (`career/dependencies.py`) rather than touching the
  shared `auth` module — parses a Bearer token if present, returns `None` on anything
  missing/invalid/expired instead of raising 401. Used only to decide "is the viewer the
  owner", nothing else relies on it.
- **Completeness score:** `service.compute_completeness_score()` only weighs
  profile-level fields (headline/summary/location/contact/photo, 20/25/15/20/20 out of
  100) since experience/project/skill/education tables don't exist yet. Docstring flags
  this needs extending once Phase 2+ ships — don't forget, or profiles will look
  "complete" at 100 while missing an entire empty career history.
- **IDs:** followed the `logs`/`auth` ULID convention (`generate_id()`, `String(36)`),
  not billing/ai's native-UUID pattern, per the plan doc.

## Frontend

New module `src/modules/career/`: `types/profile.type.ts`, `services/profileApiService.ts`,
`composables/useProfile.ts`, `utils/queryUtils.ts`, `validation/profile.schema.ts`,
`routes.ts`, `i18n/{index.ts,locales/en.ts,locales/pl.ts}`, `pages/ProfileEditPage.vue`,
`pages/PublicProfilePage.vue`. Wired into `src/router/routes.ts`, `src/i18n/index.ts`,
and `src/components/layout/AppSidebar.vue` (added a real "My Profile" nav link — the
sidebar was down to just an "About" link after the gear-module strip).

- `ProfileEditPage.vue` (`/profile`, authenticated layout): single-page form (headline,
  summary, location, visibility, contact fields), vee-validate + zod, TanStack Query via
  `useProfile()`. Not a multi-step wizard — that's an explicit later refinement per the
  plan, not a blocker for this vertical slice.
- `PublicProfilePage.vue` (`/p/:slug`, public layout): read-only public view.
- **Did NOT wire this into `src/modules/user/pages/PublicUserProfilePage.vue`** (the
  "coming soon" placeholder from the gear-module-strip pass) despite the directive
  suggesting checking it first — that page is keyed on `route.params.userId` and fetches
  a generic `IUser` shape (name/avatar/email/role badges) via the `user` module's API, a
  different concept from a slug-keyed career profile. Conflating the two would mean two
  different URL schemes pointing at overlapping-but-different data. Left
  `PublicUserProfilePage.vue` untouched. **Flag for a human decision:** should these two
  "public profile" pages eventually be merged into one, or do they serve genuinely
  different purposes (e.g. one is a lightweight user directory entry, the other the real
  CV-source public page)? Not resolved here.

## Verification performed

- **Backend:** throwaway venv + `pip install -r requirements.txt`. Confirmed
  `app.api.router` imports cleanly with the career router registered (12 top-level
  routes, up from 11; the 4 `/career/profile*` endpoints individually confirmed via
  `career_router.routes`). Then spun up a throwaway `postgres:17-alpine` Docker
  container, ran `python -m cli db init` against it, confirmed via `psql \dt` that
  `profiles` was created alongside the other 17 tables (18 total) with the exact
  expected column types (`\d profiles`). Then exercised the full service layer directly
  in a Python shell against that real database: created two fake users, verified
  `get_or_create_for_user` (slug generation), `update_profile` (completeness score went
  to 80/100 after filling headline/summary/location/contact), `save_draft` (step-scoped
  merge), `get_public_profile` under all three visibility states (public→visible to
  anon, private→blocked for anon but visible to owner), and slug collision handling
  (second user with the same name got `jan-testowy-ff5d36` instead of colliding). All
  camelCase schema serialization via `.model_validate(orm_object)` confirmed correct
  (aliases resolve against ORM attribute names as expected). Docker container and venv
  removed afterward.
- **Frontend:** `pnpm run type-check` (0 errors), `pnpm build` (clean), `pnpm lint`
  (clean, only auto-fixed import ordering), `pnpm test:run` (40/40 unit tests pass; the
  one failing suite, `tests/e2e/auth/login.spec.ts`, is the same pre-existing
  Playwright-vs-Vitest config mismatch already flagged in
  `gear-module-strip-log.md` — unrelated to this change). `dist/` removed afterward.

## Left as TODO / punted to later phases

- Multi-step wizard UX for profile creation (digest mentions this) — deferred, current
  page is a single-page form.
- Profile photo upload — `profilePhotoUrl` field exists and is editable as a raw URL in
  the schema/API, but there's no upload UI/storage wiring yet in the frontend.
- Completeness score does not yet account for experiences/projects/skills/education
  (Phase 2+ — see docstring in `service.py`).
- `FRIENDS` visibility is a no-op (same as `PRIVATE`) until a connections system exists.
- The `user`-module vs `career`-module "public profile" page duplication noted above.
