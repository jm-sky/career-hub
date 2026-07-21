# Deployment

Not yet deployed anywhere. This file documents the intended shape, mirroring the sibling `gear-stack`/`ops-monitor` projects' setup — update it once a real environment exists.

## Scenarios

| Environment | How |
|-------------|-----|
| **Local (WSL)** | `pnpm dev` + `docker compose up -d` (repo root) |
| **Production VPS (manual)** | `bash scripts/deploy.sh` (once a production host is provisioned) |

## Planned production paths (placeholder — confirm before first real deploy)

- **Repository:** `/home/madeyskij/projects/career-hub`
- **Frontend (Caddy/Nginx):** `/var/www/career-hub`
- **Backend:** root `compose.yaml` / `docker-compose.dev.yml` (volume mounts for hot reload)
- **Domain:** `careerhub.com` / `api.careerhub.com` (provisional — see `docs/plans/rebranding-decisions.md`)

## Quick manual deploy (once configured)

```bash
cd /home/madeyskij/projects/career-hub
bash scripts/deploy.sh
```

## More

- [CLAUDE.md](CLAUDE.md) — development commands
- `docs/plans/rebranding-decisions.md` — domain/port/naming decisions
