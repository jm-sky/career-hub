# Rebranding decisions (gear-stack → career-hub)

Decided 2026-07-20, applied while executing `gear-stack-keep-strip-checklist.md`. This
file is the source of truth for branding constants — if any of these need to change
later (e.g. real domain purchased differs), update here first, then re-grep the repo.

## Naming

| Constant | Value | Source / rationale |
|---|---|---|
| App name (display) | `CareerHub` | matches product name used throughout `career-hub-old` docs |
| App id (`VITE_APP_ID`) | `career-hub` | kebab-case convention gear-stack used for its own id |
| Domain (prod, placeholder) | `careerhub.com` | already used consistently in `career-hub-old/docs/{SETUP,API}.md` (`api.careerhub.com`, `storage.careerhub.com`, `noreply@careerhub.com`) — reusing avoids inventing a third name. Treat as provisional the same way `gear-stack.ovh` was — swap when a real domain is purchased. |
| API subdomain | `api.careerhub.com` | ditto |
| WebAuthn RP ID | `careerhub.com` | must match the domain passkeys are registered against |
| WebAuthn RP name | `CareerHub` | |
| Sender email default | `noreply@careerhub.com` | |
| Company/dev-org info (`VITE_COMPANY_NAME`, website, contact email) | **unchanged** (`DEV Made IT` / `dev-made.it`) | this is the real operating company across all of this account's projects (gear-stack, ops-monitor, AI-workspace), not gear-stack-specific — no need to rebrand |

## CSP (`backend/app/core/security_headers.py`)

`connect-src` domain changed from `gear-stack.ovh` → `careerhub.com` (+ `api.careerhub.com`).

## Docker Compose (`backend/docker-compose.yml`)

- Compose project `name:` → `career-hub`
- Container names: `career-hub-db`, `career-hub-redis`, `career-hub-app`
- Network: `career-hub-network`
- Volumes: `career_hub_postgres_data`, `career_hub_redis_data`, `career_hub_uploads` (external names `backend_career_hub_*`)
- Default ports changed to avoid clashing with sibling gear-stack forks running locally at once:

| Port | gear-stack/ops-monitor | AI-workspace | **career-hub** |
|---|---|---|---|
| `DB_FORWARD_PORT` | 5432 | 5435 | **5436** |
| `REDIS_FORWARD_PORT` | 6379 | 6382 | **6383** |
| `APP_PORT` | 8000 | 8003 | **8004** |
| `VITE_PORT` | 5176 | 5176 | 5176 (unchanged — frontends aren't normally run concurrently across these repos, matches sibling convention of not bothering to change this one) |

(ops-monitor and AI-workspace's actual chosen values checked directly from their `.env.example` files at rebrand time, 2026-07-20.)

## Scope notes

- `scripts/rsync-from-gear-stack.sh` intentionally keeps referring to gear-stack as the
  sync **source** — that's its whole job. Only checked it for accidental app-name leakage,
  not renamed wholesale.
- Top-level docs (`README.md`, `CLAUDE.md`, `FEATURES.md`, etc.) don't exist yet in this
  repo (the rsync script excludes them from copying) — these are being **written fresh**,
  not find/replaced. Tracked as a separate task, not part of the grep/rename pass.
