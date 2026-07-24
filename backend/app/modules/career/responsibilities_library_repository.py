"""Repository for the responsibilities_library reference table (career module, Phase 7)."""

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.id_utils import generate_id

from .db_models import ResponsibilitiesLibraryDB


class ResponsibilitiesLibraryRepository:
    """Repository for responsibilities_library database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def find(self, role_category: str, seniority_level: str | None, limit: int = 8) -> list[ResponsibilitiesLibraryDB]:
        """Most-used entries for a role, optionally narrowed to a seniority level.

        Rows with no seniority_level are generic and match any seniority filter.
        """
        query = select(ResponsibilitiesLibraryDB).where(func.lower(ResponsibilitiesLibraryDB.role_category) == role_category.strip().lower())
        if seniority_level:
            query = query.where((ResponsibilitiesLibraryDB.seniority_level == seniority_level) | (ResponsibilitiesLibraryDB.seniority_level.is_(None)))
        query = query.order_by(ResponsibilitiesLibraryDB.usage_count.desc()).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def bump_usage(self, ids: list[str]) -> None:
        if not ids:
            return
        await self.db.execute(update(ResponsibilitiesLibraryDB).where(ResponsibilitiesLibraryDB.id.in_(ids)).values(usage_count=ResponsibilitiesLibraryDB.usage_count + 1))
        await self.db.commit()

    async def create_many(self, role_category: str, seniority_level: str | None, responsibilities: list[str]) -> None:
        """Persist newly AI-generated responsibilities so future lookups for this
        role/seniority hit the fast library path instead of calling the AI again."""
        for text_ in responsibilities:
            self.db.add(
                ResponsibilitiesLibraryDB(
                    id=generate_id(),
                    role_category=role_category.strip(),
                    responsibility=text_,
                    seniority_level=seniority_level,
                    usage_count=1,
                )
            )
        await self.db.commit()
