"""Migration: Create profiles table (career module, Phase 1).

Usage:
    python migrations/001_add_career_profiles.py upgrade
    python migrations/001_add_career_profiles.py downgrade
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.database import engine
from app.modules.career.db_models import ProfileDB


async def upgrade() -> None:
    """Create the profiles table."""
    print("Creating profiles table...")

    async with engine.begin() as conn:
        await conn.run_sync(lambda sync_conn: ProfileDB.__table__.create(sync_conn, checkfirst=True))

    print("✓ profiles table created successfully")


async def downgrade() -> None:
    """Drop the profiles table."""
    print("Dropping profiles table...")

    async with engine.begin() as conn:
        await conn.run_sync(lambda sync_conn: ProfileDB.__table__.drop(sync_conn, checkfirst=True))

    print("✓ profiles table dropped successfully")


async def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Create profiles table")
    parser.add_argument("action", choices=["upgrade", "downgrade"])
    args = parser.parse_args()

    if args.action == "upgrade":
        await upgrade()
    elif args.action == "downgrade":
        await downgrade()

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
