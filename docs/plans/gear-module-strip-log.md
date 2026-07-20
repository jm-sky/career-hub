# Gear domain strip log

Executed 2026-07-20 as a follow-up to the rebranding pass, once it became clear that the
gear domain isn't isolated in `backend/app/modules/gear` / `src/modules/gear` the way
`gear-stack-keep-strip-checklist.md` assumed — those directories had **already been
deleted** (by the rsync bootstrap or an earlier pass) while dozens of other files across
the codebase still imported from them. The backend and frontend were both **non-building**
before this pass (dangling imports to a nonexistent module). This log records what was
found and fixed.

## Backend (`backend/`)

Removed all imports of the nonexistent `app.modules.gear`, `app.modules.gear_settings`,
`app.modules.stats`:

- `app/api/router.py` — dropped `gear_router`, `gear_router_v2`, `gear_settings_router`,
  `stats_router` registrations.
- `app/modules/admin/router.py` — removed the entire Containers/Items/Content-reports
  endpoint sections (they depended on `GearRepository`/`GearService`/gear schemas); admin
  now only manages users (billing/subscriptions endpoints live in the billing module,
  untouched).
- `app/modules/admin/repository.py` / `service.py` / `schemas.py` — removed
  `get_all_containers`/`get_container_by_id`/`update_container`/`delete_container`/
  `get_all_items`/`get_item_by_id`/`delete_item` and `AdminContainerResponse`/
  `AdminItemResponse`.
- `app/modules/auth/router.py` — removed the "delete all user gear images on account
  deletion" block (already defensively try/excepted, so this was silently failing before
  the fix, not crashing — but dead code referencing a nonexistent module).
- `app/modules/users/router.py` — `GET /users/me/storage/usage` used
  `ItemImageRepository` (gear) to compute usage; now hardcoded to `used_bytes = 0` with a
  `TODO` until a real storage consumer (profile photos, CV PDFs) exists.
- `backend/cli/commands/db.py` — removed the `seed`/`seed-remove` commands entirely
  (`_seed_catalogue`/`_remove_catalogue`, entirely about the global gear catalogue) and
  the dead `app.modules.gear[_settings].db_models` entries from `MODEL_MODULES`.
- Deleted `backend/app/seeders/` wholesale (39 KB of gear catalogue JSON + loader/types,
  only used by the now-removed CLI seed commands).
- `app/modules/ai/services/chat_service.py` — the chat system prompt described the app as
  a "gear management application" and told the LLM about `create_item`/`update_item`/
  `delete_item`/`create_container` structured-output actions. Replaced with a plain
  conversational prompt (see matching frontend change below) — **rewire this once the
  `career` module defines its own AI actions.**

**Left alone deliberately:** `backend/migrations/*.py` (000–055) — these define the
historical gear/container/item schema (containers, items, catalogue, content_reports,
etc.) going all the way back to migration 002. Deleting them was in scope per the
directive but judged too risky/large a call for this pass (would mean redesigning the
migration chain from scratch). Left in place; only the *code that reads/writes those
tables* was removed. `backend/migrations/051_migrate_data_to_unified_model.py` still
mentions `GearContainerDB`/`GearItemDB` in its docstring/comments only (no import) —
harmless, historical. **Follow-up decision needed:** whether to reset the migration
baseline before real users exist, or keep the history and let the `career` module's
migrations start from 056.

Verified with a throwaway `uv venv` + `uv pip install -r requirements.txt`: the full
`app.api.router` module and `cli.main`/`cli.commands.db`/`cli.commands.users` all import
cleanly (11 routes registered). `uv sync` itself fails on a pre-existing
`pyproject.toml` packaging issue (flat-layout multi-package discovery) unrelated to this
change — not touched, flagged here for whoever owns build tooling next.

## Frontend (`src/`)

Removed all imports of `@/modules/gear/*` and `@/modules/stats/*` (neither directory
exists on disk):

- **Router** (`src/router/routes.ts`, `src/App.vue`): dropped `gearRoutes` registration
  and the `DataMigrationDialog` (gear's offline-localStorage→API migration prompt, not
  applicable — career-hub has no localStorage domain data to migrate).
- **`src/pages/LandingPage.vue`, `src/pages/DashboardPage.vue`**: fully rewritten as
  generic CareerHub placeholders (hero + login/register CTA) — previously 100% gear
  container/item dashboards (readiness %, item counts, "Generate Example Gear", etc).
  Matching `en.ts`/`pl.ts` `landing.*` keys updated too (the old keys still existed in the
  locale files, so the new components' `t(key, fallback)` calls would otherwise have
  silently rendered the *old* "Gear Stack" text instead of the fallback — i18n only uses
  the fallback when the key is missing, not when it resolves to stale content. Caught and
  fixed).
- **`src/pages/NotFoundPage.vue`**: removed a dead "Go to Containers" (`/gear`) button.
- **`src/components/layout/`**: deleted `LocalContainersStats.vue`, `WelcomeQuickActions.vue`,
  `TotalsStats.vue`, `LandingPageContainerCard.vue`, `SidebarMenuContainerItem.vue`
  (all gear-only, only referenced from Landing/Dashboard/Sidebar). `AllItemsFilterBadges.vue`
  and `AllItemsFiltersMenu.vue` were already orphaned (zero importers) — deleted too.
  `AppSidebar.vue` was ~90% gear container nav/search — reduced to a minimal shell (just
  the About link); nav will need real content once the `career` module has pages to link
  to. `AppHeader.vue` and `BackButton.vue` had smaller gear nav-link/icon-helper
  dependencies — removed, kept the rest intact.
- **`src/modules/admin/`**: deleted `AdminContainersPage.vue`, `AdminItemsPage.vue`,
  `ContentReportsPage.vue` and their route entries/API-service methods/types (mirrors the
  backend endpoint removal above). `AdminDashboardPage.vue` quick-links trimmed to
  Users/Limits/Subscriptions.
- **`src/modules/ai/`**: `useAiActions.ts` and `useAiContext.ts` were entirely gear-item
  CRUD (create/update/delete gear items from AI structured output, building gear-item
  context for prompts). Neutered to no-ops with `TODO`s — the AI chat UI itself
  (`AiChatWindow.vue` and friends) needed no changes since its props were already
  gear-agnostic strings (`containerIds?: string[]`). `AiHistoryPage.vue` imported a
  generic-sounding `useSearchPaginationUrl` from the gear module — reimplemented as a
  small shared composable at `src/shared/composables/useSearchPaginationUrl.ts` (URL
  query param sync for search/page/pageSize), since the original implementation no longer
  existed anywhere to copy from.
- **`src/modules/billing/`**: `BillingSuccessPage.vue`/`BillingCancelPage.vue` redirected
  to `/gear` after checkout — now redirect to the dashboard. `BillingPage.vue` rendered a
  gear-only `AccountLimitsCard` (no props, only usage site) — removed; **a real
  feature-limits summary card should be added back once `feature_limits` has career-hub
  feature keys to show.** Plan copy in `types/index.ts` / `utils/planTranslations.ts` /
  `i18n/locales/{en,pl}.ts` said "Basic gear management" / "AI-powered gear
  recommendations" — reworded to "Basic profile management" / "AI-powered suggestions"
  (translation-key mappings updated to match). **Left untouched, flagged for a real
  decision:** the plan tiers are still named `free`/`pro`/`pro_plus` (not the
  `Free`/`Pro`/`Expert` from `requirements-digest.md`), and the numeric limits
  (`items`/`containers`/storage/aiTokens) are still gear-shaped, not
  `cvVersions`/watermark/custom-domain/API-access as the digest specifies. This is a
  business-model decision, not a mechanical strip — do it deliberately when building the
  `career` module's billing integration, not by find-replacing numbers.
- **`src/modules/settings/`**: deleted `BrandsSettingsCard.vue`, `CategoriesSettingsCard.vue`,
  `ContainerTypesSettingsCard.vue` — all three were already orphaned (not imported by
  `SettingsPage.vue` or anywhere else), so this is pure dead-code removal, not a behavior
  change.
- **`src/modules/user/pages/PublicUserProfilePage.vue`**: was a public-container gallery
  keyed on `authorId`. This is functionally the predecessor of the `career` module's
  future public-profile feature (`requirements-digest.md` §2/§3) — kept the generic
  user-identity header (avatar/name/role badge) and replaced the container grid with a
  "coming soon" placeholder, rather than deleting the page/route outright.
- **`src/components/ui/shelf-life-input/`, `src/components/ui/weight-input/`**: deleted —
  both were gear-typed (`TShelfLifeUnit`, `TGearWeightUnit`) and had zero importers.
- **`src/shared/utils/appInit.ts`**: `initializeStores()` only ever touched the gear
  store; now a documented no-op, kept as a hook point for a future `career` store.
- **`src/shared/config/config.ts`**: removed three dead gear-only localStorage key
  exports (`GEAR_SETTINGS_STORAGE_KEY`, `ITEMS_TABLE_COLUMN_VISIBILITY_KEY`,
  `ITEMS_TABLE_EDIT_MODE_KEY`) — all had zero importers.
- **`src/i18n/index.ts`**: dropped the `gearEn`/`gearPl` message-merge import (the module
  no longer exists).

**Not touched — flagged, not fixed (low-risk, cosmetic, or genuinely out of scope):**
- A long tail of `t('gear.settings.ai.*')`/`t('gear.catalogue.*')`/`t('gear.filters.*')`
  i18n *key names* across `src/modules/ai/components/**` (AiTokenManager, AiUsageDisplay,
  AiModelSelector, AiSettingsCard, AiContextConfig, RemoveTokenConfirmDialog,
  AiHistoryFilters). These keys don't exist in the locale files (the `gear` i18n module is
  gone), so every one of these calls falls back to its hardcoded default string — visibly
  correct, just poorly namespaced. Renaming ~20 keys across 7 components was judged lower
  value than the functional fixes above; do it as a batch when someone's next in this
  file.
- `src/modules/ai/utils/historyNavigation.spec.ts` — a self-contained test (the function
  under test is defined inline in the spec, not imported) still asserts on `/gear`-shaped
  paths. Doesn't break anything (no import to a missing module), but the logic it tests
  isn't wired into `AiHistoryPage.vue` — looks like dead/pre-existing test debt, not
  something this pass introduced.
- `src/shared/composables/usePageTitle.ts` — a JSDoc example comment mentions
  `'gear.page.title'`. Documentation only.
- Backend comments only (no behavior): `billing/service.py` rate-limit comments
  ("gear lists"/"gear collections"), migration docstrings in `002_create_users_table.py`
  and `017_add_item_images_table.py`.

## Verification performed

- Backend: throwaway `uv venv` + `pip install -r requirements.txt`, then imported
  `app.api.router` (11 routes) and all three touched `cli.commands.*` modules — clean.
- Frontend: `pnpm install` (cached, fast), then:
  - `pnpm vue-tsc --noEmit` — 0 errors.
  - `pnpm build` — succeeds, produces a normal dist bundle + PWA precache manifest.
  - `pnpm lint` (`eslint --fix`) — clean.
  - `pnpm vitest run` — 40/40 unit tests pass; the only failed suite
    (`tests/e2e/auth/login.spec.ts`) is a pre-existing Playwright-vs-Vitest config
    mismatch (vitest picking up an e2e spec it shouldn't), unrelated to this change and
    out of scope for this pass.
- All verification venvs/node_modules/dist artifacts created during checking were removed
  afterward — nothing left behind that isn't a real source change.

## Summary for whoever builds the `career` module next

The scaffolding is now gear-free and builds clean, but several places are intentionally
thin placeholders waiting on real domain data: `DashboardPage.vue`, `LandingPage.vue`,
`AppSidebar.vue` (empty nav), `PublicUserProfilePage.vue`, `useAiContext.ts`/
`useAiActions.ts` (AI context/actions are no-ops), and the billing plan model (still
gear-shaped limits, wrong tier names). None of these need "fixing" in isolation — they
should each get real content as the `career` module's data model and pages land.
