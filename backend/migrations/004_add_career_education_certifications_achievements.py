"""Migration: Create education, certifications, achievements tables (career module,
Phase 4).

Usage:
    python migrations/004_add_career_education_certifications_achievements.py upgrade
    python migrations/004_add_career_education_certifications_achievements.py downgrade
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.database import engine
from app.modules.career.db_models import AchievementDB, CertificationDB, EducationDB


async def upgrade() -> None:
    """Create education, certifications, achievements tables."""
    print("Creating education, certifications, achievements tables...")

    async with engine.begin() as conn:
        await conn.run_sync(lambda sync_conn: EducationDB.__table__.create(sync_conn, checkfirst=True))
        await conn.run_sync(lambda sync_conn: CertificationDB.__table__.create(sync_conn, checkfirst=True))
        await conn.run_sync(lambda sync_conn: AchievementDB.__table__.create(sync_conn, checkfirst=True))

    print("✓ education, certifications, achievements tables created successfully")


async def downgrade() -> None:
    """Drop achievements, certifications, education tables."""
    print("Dropping achievements, certifications, education tables...")

    async with engine.begin() as conn:
        await conn.run_sync(lambda sync_conn: AchievementDB.__table__.drop(sync_conn, checkfirst=True))
        await conn.run_sync(lambda sync_conn: CertificationDB.__table__.drop(sync_conn, checkfirst=True))
        await conn.run_sync(lambda sync_conn: EducationDB.__table__.drop(sync_conn, checkfirst=True))

    print("✓ tables dropped successfully")


async def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Create education, certifications, achievements tables")
    parser.add_argument("action", choices=["upgrade", "downgrade"])
    args = parser.parse_args()

    if args.action == "upgrade":
        await upgrade()
    elif args.action == "downgrade":
        await downgrade()

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
