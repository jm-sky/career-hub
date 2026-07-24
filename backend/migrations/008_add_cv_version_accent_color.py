"""Migration: Add accent_color column to cv_versions (career module, Phase 5 follow-up).

Usage:
    python migrations/008_add_cv_version_accent_color.py upgrade
    python migrations/008_add_cv_version_accent_color.py downgrade
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text

from app.core.database import engine


async def upgrade() -> None:
    """Add the accent_color column to cv_versions."""
    print("Adding accent_color column to cv_versions...")

    async with engine.begin() as conn:
        await conn.execute(text("ALTER TABLE cv_versions ADD COLUMN IF NOT EXISTS accent_color VARCHAR(7)"))

    print("✓ accent_color column added successfully")


async def downgrade() -> None:
    """Drop the accent_color column from cv_versions."""
    print("Dropping accent_color column from cv_versions...")

    async with engine.begin() as conn:
        await conn.execute(text("ALTER TABLE cv_versions DROP COLUMN IF EXISTS accent_color"))

    print("✓ accent_color column dropped successfully")


async def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Add accent_color column to cv_versions")
    parser.add_argument("action", choices=["upgrade", "downgrade"])
    args = parser.parse_args()

    if args.action == "upgrade":
        await upgrade()
    elif args.action == "downgrade":
        await downgrade()

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
