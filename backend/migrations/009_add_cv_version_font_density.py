"""Migration: Add font_family and density columns to cv_versions (career module,
Phase 5 follow-up — CV customization beyond accent color).

Usage:
    python migrations/009_add_cv_version_font_density.py upgrade
    python migrations/009_add_cv_version_font_density.py downgrade
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text

from app.core.database import engine


async def upgrade() -> None:
    """Add the font_family and density columns to cv_versions."""
    print("Adding font_family and density columns to cv_versions...")

    async with engine.begin() as conn:
        await conn.execute(text("ALTER TABLE cv_versions ADD COLUMN IF NOT EXISTS font_family VARCHAR(20)"))
        await conn.execute(text("ALTER TABLE cv_versions ADD COLUMN IF NOT EXISTS density VARCHAR(20)"))

    print("✓ font_family and density columns added successfully")


async def downgrade() -> None:
    """Drop the font_family and density columns from cv_versions."""
    print("Dropping font_family and density columns from cv_versions...")

    async with engine.begin() as conn:
        await conn.execute(text("ALTER TABLE cv_versions DROP COLUMN IF EXISTS font_family"))
        await conn.execute(text("ALTER TABLE cv_versions DROP COLUMN IF EXISTS density"))

    print("✓ font_family and density columns dropped successfully")


async def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Add font_family and density columns to cv_versions")
    parser.add_argument("action", choices=["upgrade", "downgrade"])
    args = parser.parse_args()

    if args.action == "upgrade":
        await upgrade()
    elif args.action == "downgrade":
        await downgrade()

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
