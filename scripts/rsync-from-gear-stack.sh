#!/usr/bin/env bash
# Sync boilerplate from gear-stack into CareerHub (mirrored monorepo layout).
#
# Adapted from AI-workspace's scripts/rsync-from-gear-stack.sh. Same pattern:
# rsync instead of git remote/pull, so gear-stack's own history and domain
# modules never enter career-hub's git log. Re-run (with --apply) any time you
# want to pull in upstream gear-stack fixes to shared core files.
#
# Usage:
#   ./scripts/rsync-from-gear-stack.sh              # dry-run (default)
#   ./scripts/rsync-from-gear-stack.sh --apply      # write changes
#   GEAR_STACK_SRC=/path/to/gear-stack ./scripts/rsync-from-gear-stack.sh --apply

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SOURCE="${GEAR_STACK_SRC:-${REPO_ROOT}/../gear-stack}"
DEST="${REPO_ROOT}"

DRY_RUN=1
if [[ "${1:-}" == "--apply" ]]; then
  DRY_RUN=0
elif [[ -n "${1:-}" ]]; then
  echo "Usage: $0 [--apply]" >&2
  exit 1
fi

if [[ ! -d "${SOURCE}" ]]; then
  echo "gear-stack source not found: ${SOURCE}" >&2
  echo "Set GEAR_STACK_SRC to override." >&2
  exit 1
fi

RSYNC_FLAGS=(
  -av
  --delete
  --exclude='.git/'
  --exclude='node_modules/'
  --exclude='dist/'
  --exclude='.env'
  --exclude='backups/'
  --exclude='.eslintcache'
  --exclude='__pycache__/'
  --exclude='.mypy_cache/'
  --exclude='.ruff_cache/'
  --exclude='.venv/'
  --exclude='test-results/'
  --exclude='playwright-report/'
  --exclude='.pytest_cache/'
  # gear-stack local runtime state (dev db, uploaded catalogue images)
  --exclude='backend/data/'
  --exclude='backend/images/'
  # CareerHub-owned (never overwrite from gear-stack)
  --exclude='docs/'
  --exclude='README.md'
  --exclude='LICENSE'
  --exclude='.cursorrules'
  --exclude='CLAUDE.md'
  --exclude='scripts/rsync-from-gear-stack.sh'
  # gear-stack narrative / meta (not part of boilerplate)
  --exclude='BUGS.md'
  --exclude='CHANGELOG.md'
  --exclude='DEPLOYMENT.md'
  --exclude='FEATURES.md'
  --exclude='MIGRATION_*.md'
  --exclude='V2_*.md'
  --exclude='screenshot.png'
  # gear domain (career-hub does not need the gear/inventory product)
  --exclude='src/modules/gear/'
  --exclude='src/modules/stats/'
  --exclude='src/pages/gear/'
  --exclude='backend/app/modules/gear/'
  --exclude='backend/app/modules/gear_settings/'
  --exclude='backend/app/modules/stats/'
  --exclude='backend/tests/integration/gear/'
  --exclude='tests/e2e/gear/'
  --exclude='tests/integration/gear/'
  --exclude='scripts/find-militaria-products.ts'
  --exclude='backend/migrations/010_add_gear_tables.py'
  --exclude='backend/migrations/010_add_gear_tables.sql'
  --exclude='backend/migrations/011_add_missing_gear_fields.py'
  --exclude='backend/migrations/026_add_currency_to_gear_items.py'
  --exclude='backend/migrations/030_add_catalogue_item_id_to_gear_items.py'
  --exclude='backend/migrations/039_add_gear_settings_table.py'
  --exclude='backend/migrations/044_add_shelf_life_to_gear_items.py'
  --exclude='backend/migrations/050_create_unified_gear_items.py'
)

if [[ "${DRY_RUN}" -eq 1 ]]; then
  RSYNC_FLAGS+=(--dry-run)
  echo "Dry-run: no files will be modified. Pass --apply to sync."
else
  echo "Applying rsync from ${SOURCE} -> ${DEST}"
fi

echo "Source: ${SOURCE}/"
echo "Dest:   ${DEST}/"
echo

rsync "${RSYNC_FLAGS[@]}" "${SOURCE}/" "${DEST}/"

if [[ "${DRY_RUN}" -eq 1 ]]; then
  echo
  echo "Review the list above, then run: $0 --apply"
fi
