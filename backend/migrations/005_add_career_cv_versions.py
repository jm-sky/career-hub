"""Migration: Create cv_versions table (career module, Phase 5).

Usage:
    python migrations/005_add_career_cv_versions.py upgrade
    python migrations/005_add_career_cv_versions.py downgrade
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.database import engine
from app.modules.career.db_models import CvVersionDB


async def upgrade() -> None:
    """Create the cv_versions table."""
    print("Creating cv_versions table...")

    async with engine.begin() as conn:
        await conn.run_sync(lambda sync_conn: CvVersionDB.__table__.create(sync_conn, checkfirst=True))

    print("✓ cv_versions table created successfully")


async def downgrade() -> None:
    """Drop the cv_versions table."""
    print("Dropping cv_versions table...")

    async with engine.begin() as conn:
        await conn.run_sync(lambda sync_conn: CvVersionDB.__table__.drop(sync_conn, checkfirst=True))

    print("✓ cv_versions table dropped successfully")


async def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Create cv_versions table")
    parser.add_argument("action", choices=["upgrade", "downgrade"])
    args = parser.parse_args()

    if args.action == "upgrade":
        await upgrade()
    elif args.action == "downgrade":
        await downgrade()

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
