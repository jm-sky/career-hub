# Migrations squash + visual assets cleanup log

Executed 2026-07-20 as a follow-up to `gear-module-strip-log.md`, per explicit user request.

## Job 1: Migrations squashed (44 files → 1)

`backend/migrations/` went from `000`–`055` (44 files) down to just `000_create_schema_migrations.py`.

**Reasoning verified before deleting (not just assumed):** career-hub has never been deployed
(no real database anywhere). `db init` calls `Base.metadata.create_all()` against whatever
`db_models.py` currently defines for the modules listed in `MODEL_MODULES`
(`backend/cli/commands/db.py`) — since SQLAlchemy ORM models are the live source of truth and
already reflect every historical incremental change (spot-checked: `AIUserSettingsDB` already
has `max_tokens`/`temperature` from migration 037, `AIHistoryDB` already has `container_ids` from
041, `auth` already has `token_version` from 055, `oauth_provider`/`oauth_connections` from
012/028) — a fresh `create_all()` produces the exact same end-state schema the full migration
chain would have produced, for every *schema* change. Migrations 001–055 were entirely either
(a) schema changes already baked into current models, or (b) pure gear-domain schema
(containers/items/catalogue/ratings/share-tokens/content-reports) with no corresponding code
left after the module strip.

**Bug found and fixed along the way:** `MODEL_MODULES` in `cli/commands/db.py` was missing
`billing`, `feature_limits`, and `ai` — meaning `db init` alone was *not* actually creating those
tables; they only existed in a real deployment because migrations `021`/`033`/`047` created them
directly via raw SQL/DDL, bypassing the ORM metadata path. Deleting the migrations without fixing
this would have silently produced a broken fresh install (11 tables instead of 17). Added the
three missing modules to `MODEL_MODULES`.

**One piece of seed *data* found, deliberately NOT ported forward:** migration `033` seeded
default `feature_limits` rows for roles `user`/`premium` (AI $ limit + storage byte limit), and
migration `047` added a `business` role row. This is real data, not just schema — a completely
empty `feature_limits` table after a fresh `db init` is a behavior difference from the old
migration chain. I did not recreate this seed data because the previous fork's log already flags
that the entire billing/feature-limits tier model is gear-shaped and slated for replacement
(`free`/`pro`/`pro_plus` → `Free`/`Pro`/`Expert`, items/storage/aiTokens limits →
cvVersions/watermark/custom-domain/API-access). Seeding old tier names into a fresh install would
just recreate data due for deletion anyway. **Action needed:** whoever wires up the `career`
module's billing integration must seed `feature_limits` with real Free/Pro/Expert rows — the table
exists (schema is correct) but is empty on a fresh `db init`.

**Verified end-to-end**, not just "should work": spun up a throwaway `postgres:17-alpine` Docker
container, ran `python -m cli db init` against it with the new `MODEL_MODULES`, and confirmed via
`psql \dt` that all 17 expected tables were created (`ai_cache`, `ai_history`,
`ai_user_settings`, `email_audit_log`, `feature_limits`, `logs`, `oauth_connections`, `passkeys`,
`schema_migrations`, `stripe_webhook_events`, `subscription_history`, `subscriptions`,
`tenant_memberships`, `tenants`, `totp_configs`, `user_settings`, `users`). Also ran
`db migrate` and `db migrate-status` — both work cleanly against the now-tiny migrations
directory (1 migration, applied). Throwaway container and venv removed afterward.

Future schema work (the `career` module and anything else) should add new migrations starting
from `001` again, with real content only for what's actually being added.

## Job 2: Gear-branded visual assets replaced

- Deleted orphaned dead files: `public/backpack-icon.svg`, `public/backpack-icon-color.svg`,
  `public/backpack.png` (zero code references, confirmed via grep before deleting).
- `public/favicon.svg` and `public/app-icon.svg` were literally Lucide's `Backpack` icon in an
  orange circle badge. Replaced with Lucide's `file-user` icon (a document with a person —
  reads naturally as "profile/CV"), same circle-badge style and colors (`#EE610F` /
  `rgba(238, 97, 15, ...)` on `#FFF4ED` background / `rgba(238, 97, 15, 0.1)`). Path data pulled
  directly from the installed `node_modules/lucide-vue-next/dist/esm/icons/file-user.js` (not
  reconstructed from memory) to guarantee it's pixel-accurate to the real icon.
- Regenerated all 15 `public/icons/icon-*.png` sizes (16 through 1024) from the new
  `app-icon.svg` using `sharp` (via a throwaway script, `npx`-cached, deleted after use) — no
  filename changes, so `manifest.webmanifest`/`pwa.config.ts` needed no edits, just new pixel
  content. Spot-checked the 192×192 output visually — clean file-user icon, no backpack artifacts.
- `favicon.ico` (was also a 32×32 backpack) was regenerated too: rasterized the new SVG to a
  32×32 PNG via sharp, then hand-wrapped it in a minimal ICO container (sharp itself doesn't
  write `.ico`; a single-image PNG-in-ICO container is a well-defined, simple binary format —
  6-byte ICONDIR + 16-byte ICONDIRENTRY + raw PNG bytes). `file` confirms it's recognized as a
  valid "MS Windows icon resource, 32x32, PNG image data".

## Job 3: Final rebrand sweep

Repo-wide grep for `gear-stack|gearstack|gear stack` (case-insensitive) turned up only the
already-reviewed intentional mentions: `CLAUDE.md`, `DEPLOYMENT.md`, `CHANGELOG.md` (referring to
the sibling `gear-stack` project by name) and `scripts/rsync-from-gear-stack.sh` (its own name,
by design). `.github/` and `components.json` are clean (nothing found).

Three unrelated, pre-existing, low-risk "backpack" mentions remain — not gear-stack *branding*,
just borrowed example vocabulary in test/doc code that has nothing to do with whether the gear
module exists:
- `src/shared/composables/usePageTitle.ts` — a JSDoc `@example` comment (`setTitle('gear.pages...', { name: 'Backpack' })`). Doc-only, already flagged by the previous fork.
- `backend/tests/test_convert_empty_strings_middleware.py` — uses `"name": "Backpack"` as an
  arbitrary example string testing a generic empty-string-conversion middleware; unrelated to
  gear domain logic.
- `tests/integration/fixtures/test-data.ts` — a fixture default `containerType: 'backpack'`;
  the fixture itself is generic test scaffolding, not gear-module-dependent.

Left alone — cosmetic, zero functional impact, not worth the churn of touching test files that
aren't testing gear functionality in the first place.

## Verification performed

- Backend: fresh throwaway venv, `pip install -r requirements.txt`, then
  `SECRET_KEY=<dummy> ENVIRONMENT=local python -c "import app.api.router"` (11 routes) and
  `cli.main`/`cli.commands.db`/`cli.commands.users` — all import cleanly. Plus the full
  `db init` → real Postgres → `\dt` end-to-end check described in Job 1.
- Frontend: `pnpm install` (already cached), `pnpm run type-check` (0 errors), `pnpm build`
  (succeeds, produces PWA precache manifest), `pnpm lint` (clean).
- All throwaway venvs, Docker containers, node scripts, and `dist/` build output were removed
  afterward. Nothing left behind except real source changes.
- Nothing committed — all changes are unstaged, as instructed.
