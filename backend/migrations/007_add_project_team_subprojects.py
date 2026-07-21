"""Migration: Add team and sub_projects columns to projects (issue 001).

Usage:
    python migrations/007_add_project_team_subprojects.py upgrade
    python migrations/007_add_project_team_subprojects.py downgrade
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text

from app.core.database import engine


async def upgrade() -> None:
    """Add team and sub_projects JSONB columns to projects."""
    print("Adding team and sub_projects columns to projects...")

    async with engine.begin() as conn:
        await conn.execute(text("ALTER TABLE projects ADD COLUMN IF NOT EXISTS team JSONB NOT NULL DEFAULT '[]'::jsonb"))
        await conn.execute(text("ALTER TABLE projects ADD COLUMN IF NOT EXISTS sub_projects JSONB NOT NULL DEFAULT '[]'::jsonb"))

    print("✓ team and sub_projects columns added successfully")


async def downgrade() -> None:
    """Drop team and sub_projects columns from projects."""
    print("Dropping team and sub_projects columns from projects...")

    async with engine.begin() as conn:
        await conn.execute(text("ALTER TABLE projects DROP COLUMN IF EXISTS team"))
        await conn.execute(text("ALTER TABLE projects DROP COLUMN IF EXISTS sub_projects"))

    print("✓ team and sub_projects columns dropped successfully")


async def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Add team and sub_projects columns to projects")
    parser.add_argument("action", choices=["upgrade", "downgrade"])
    args = parser.parse_args()

    if args.action == "upgrade":
        await upgrade()
    elif args.action == "downgrade":
        await downgrade()

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
