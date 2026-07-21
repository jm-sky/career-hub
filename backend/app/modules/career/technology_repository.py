"""Repository for the global technologies reference table (career module, Phase 2)."""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from .db_models import TechnologyDB


class TechnologyRepository:
    """Repository for technology reference-data operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_name(self, name: str) -> TechnologyDB | None:
        """Case-insensitive lookup — avoids creating near-duplicate technologies
        that only differ by case (e.g. "Python" vs "python")."""
        result = await self.db.execute(select(TechnologyDB).where(func.lower(TechnologyDB.name) == name.lower()))
        return result.scalar_one_or_none()

    async def get_by_ids(self, ids: list[str]) -> list[TechnologyDB]:
        if not ids:
            return []
        result = await self.db.execute(select(TechnologyDB).where(TechnologyDB.id.in_(ids)))
        return list(result.scalars().all())

    async def search(self, query: str | None, limit: int) -> list[TechnologyDB]:
        stmt = select(TechnologyDB).order_by(TechnologyDB.name).limit(limit)
        if query:
            stmt = stmt.where(TechnologyDB.name.ilike(f"%{query}%"))
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, technology: TechnologyDB) -> TechnologyDB:
        self.db.add(technology)
        await self.db.commit()
        await self.db.refresh(technology)
        return technology
