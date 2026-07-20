# gear-stack → career-hub: keep/strip + rebrand checklist

Prepared while gear-stack was still being edited — based on a read-only survey of its
current module layout. Re-verify module list at clone time in case new modules were
added in the meantime.

## Modules

### Backend (`backend/app/modules/`)
| Module | Action | Notes |
|---|---|---|
| `auth` | **keep** | JWT, OAuth, WebAuthn, password reset |
| `two_factor` | **keep** | TOTP + WebAuthn 2FA |
| `users` | **keep** | user model/CRUD |
| `settings` | **keep** | user settings (units etc. are gear-specific — audit fields, drop gear-only ones) |
| `admin` | **keep** | admin dashboard (users/containers/items → will need career-domain admin views later, but user/role management ports as-is) |
| `billing` | **keep** | Stripe subscriptions — career-hub already has Free/Pro/Expert tiers, this is a direct fit |
| `feature_limits` | **keep** | per-role AI/storage limits — same pattern career-hub will want for tier gating |
| `ai` | **keep** | chat/context/history infra — career-hub roadmap wants "AI-powered description optimization" later, infra is reusable even if prompts are new |
| `logs` | **keep** | audit/logging module |
| `tenants` | **evaluate** | lightweight multi-tenant/workspace module (name/description/role membership). Not in career-hub's current requirements (single-user profiles) — keep on ice, drop if unused after 1 sprint |
| `gear` | **drop** | core gear/container/item domain — fully gear-specific |
| `gear_settings` | **drop** | gear-specific settings (weight units etc.) |
| `stats` | **drop** | gear weight/category analytics — career-hub will want its own stats module later (profile views, CV downloads) but not this one |

### Frontend (`src/modules/`)
| Module | Action | Notes |
|---|---|---|
| `auth` | **keep** | |
| `user` | **keep** | |
| `settings` | **keep** | strip gear-specific settings (weight unit prefs) once ported |
| `admin` | **keep** | strip container/item admin pages, keep user admin |
| `billing` | **keep** | |
| `ai` | **keep** | |
| `gear` | **drop** | |
| `stats` | **drop** | |

New module to build: `career` (or `profile`) — profile/experience/project/skills/CV, per requirements digest.

## Branding / config touchpoints to rename (found via `grep -rniE "gear-stack|gearstack" .`, excluding node_modules and gear-stack's own internal docs/plans/research which won't be copied)

Code/config files that actually need edits (not just gear-stack's own historical docs):
- `package.json` — name field
- `pwa.config.ts` — app name/short_name/description in manifest
- `src/shared/config/config.ts` — app-level constants
- `src/shared/i18n/locales/en.ts`, `pl.ts` — any hardcoded "Gear Stack" strings in shared i18n keys
- `backend/app/core/config.py` — APP name, WebAuthn RP name/id (**must** match new domain or passkeys break), default sender email, etc.
- `backend/app/core/security_headers.py` — CSP `connect-src` domain (currently `gear-stack.ovh`)
- `backend/app/core/storage/local_adapter.py` — check for hardcoded path/bucket naming
- `backend/docker-compose.yml` — service/container names, project name, ports (must not collide with gear-stack's own containers if both run locally at once)
- `backend/cli/commands/db.py`, `users.py`, `cli/main.py` — check for hardcoded app name in CLI banner/help text
- `README.md`, `CLAUDE.md`, `FEATURES.md`, `CHANGELOG.md`, `DEPLOYMENT.md`, `V2_MIGRATION_STATUS.md`, `backend/README.md` — rewrite wholesale for career-hub, not a find/replace job (these describe gear-stack's own product); pull relevant *structural* sections (commands, module pattern) into new CLAUDE.md, don't try to reuse gear-domain content
- `docs/` (ROADMAP*.md, archive, deployment, examples, features, issues, plans, prompts, research, reviews, testing) — **gear-stack's own project history, do not copy**. Only the module-pattern/tooling knowledge should transfer, written fresh for career-hub.
- `tests/e2e/*` — fixtures/global-setup reference gear-stack; port structure, not content
- `.claude/settings.local.json` — check for gear-stack-specific permission entries before copying

## Not yet decided (flag for discussion before/at rebrand time)
- Keep gear-stack's WebAuthn RP ID scheme or start fresh (affects domain/passkey config)
- Local dev ports for docker-compose (avoid clash if running both repos simultaneously)
- Whether `tenants` module is worth keeping now vs. dropping until actually needed
