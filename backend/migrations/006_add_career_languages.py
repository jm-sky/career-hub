"""Migration: Create languages table (career module).

Usage:
    python migrations/006_add_career_languages.py upgrade
    python migrations/006_add_career_languages.py downgrade
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.database import engine
from app.modules.career.db_models import LanguageDB


async def upgrade() -> None:
    """Create languages table."""
    print("Creating languages table...")

    async with engine.begin() as conn:
        await conn.run_sync(lambda sync_conn: LanguageDB.__table__.create(sync_conn, checkfirst=True))

    print("✓ languages table created successfully")


async def downgrade() -> None:
    """Drop languages table."""
    print("Dropping languages table...")

    async with engine.begin() as conn:
        await conn.run_sync(lambda sync_conn: LanguageDB.__table__.drop(sync_conn, checkfirst=True))

    print("✓ languages table dropped successfully")


async def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Create languages table")
    parser.add_argument("action", choices=["upgrade", "downgrade"])
    args = parser.parse_args()

    if args.action == "upgrade":
        await upgrade()
    elif args.action == "downgrade":
        await downgrade()

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
