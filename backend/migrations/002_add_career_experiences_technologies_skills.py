"""Migration: Create technologies, experiences, experience_technologies, skills
tables (career module, Phase 2).

Usage:
    python migrations/002_add_career_experiences_technologies_skills.py upgrade
    python migrations/002_add_career_experiences_technologies_skills.py downgrade
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.database import engine
from app.modules.career.db_models import (
    ExperienceDB,
    ExperienceTechnologyDB,
    SkillDB,
    TechnologyDB,
)


async def upgrade() -> None:
    """Create technologies, experiences, experience_technologies, skills tables."""
    print("Creating technologies, experiences, experience_technologies, skills tables...")

    async with engine.begin() as conn:
        await conn.run_sync(lambda sync_conn: TechnologyDB.__table__.create(sync_conn, checkfirst=True))
        await conn.run_sync(lambda sync_conn: ExperienceDB.__table__.create(sync_conn, checkfirst=True))
        await conn.run_sync(lambda sync_conn: ExperienceTechnologyDB.__table__.create(sync_conn, checkfirst=True))
        await conn.run_sync(lambda sync_conn: SkillDB.__table__.create(sync_conn, checkfirst=True))

    print("✓ technologies, experiences, experience_technologies, skills tables created successfully")


async def downgrade() -> None:
    """Drop skills, experience_technologies, experiences, technologies tables (FK-safe order)."""
    print("Dropping skills, experience_technologies, experiences, technologies tables...")

    async with engine.begin() as conn:
        await conn.run_sync(lambda sync_conn: SkillDB.__table__.drop(sync_conn, checkfirst=True))
        await conn.run_sync(lambda sync_conn: ExperienceTechnologyDB.__table__.drop(sync_conn, checkfirst=True))
        await conn.run_sync(lambda sync_conn: ExperienceDB.__table__.drop(sync_conn, checkfirst=True))
        await conn.run_sync(lambda sync_conn: TechnologyDB.__table__.drop(sync_conn, checkfirst=True))

    print("✓ tables dropped successfully")


async def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Create technologies, experiences, experience_technologies, skills tables")
    parser.add_argument("action", choices=["upgrade", "downgrade"])
    args = parser.parse_args()

    if args.action == "upgrade":
        await upgrade()
    elif args.action == "downgrade":
        await downgrade()

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
