"""Migration: Create projects, project_experiences, project_technologies tables
(career module, Phase 3).

Usage:
    python migrations/003_add_career_projects.py upgrade
    python migrations/003_add_career_projects.py downgrade
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.database import engine
from app.modules.career.db_models import ProjectDB, ProjectExperienceDB, ProjectTechnologyDB


async def upgrade() -> None:
    """Create projects, project_experiences, project_technologies tables."""
    print("Creating projects, project_experiences, project_technologies tables...")

    async with engine.begin() as conn:
        await conn.run_sync(lambda sync_conn: ProjectDB.__table__.create(sync_conn, checkfirst=True))
        await conn.run_sync(lambda sync_conn: ProjectExperienceDB.__table__.create(sync_conn, checkfirst=True))
        await conn.run_sync(lambda sync_conn: ProjectTechnologyDB.__table__.create(sync_conn, checkfirst=True))

    print("✓ projects, project_experiences, project_technologies tables created successfully")


async def downgrade() -> None:
    """Drop project_technologies, project_experiences, projects tables (FK-safe order)."""
    print("Dropping project_technologies, project_experiences, projects tables...")

    async with engine.begin() as conn:
        await conn.run_sync(lambda sync_conn: ProjectTechnologyDB.__table__.drop(sync_conn, checkfirst=True))
        await conn.run_sync(lambda sync_conn: ProjectExperienceDB.__table__.drop(sync_conn, checkfirst=True))
        await conn.run_sync(lambda sync_conn: ProjectDB.__table__.drop(sync_conn, checkfirst=True))

    print("✓ tables dropped successfully")


async def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Create projects, project_experiences, project_technologies tables")
    parser.add_argument("action", choices=["upgrade", "downgrade"])
    args = parser.parse_args()

    if args.action == "upgrade":
        await upgrade()
    elif args.action == "downgrade":
        await downgrade()

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
