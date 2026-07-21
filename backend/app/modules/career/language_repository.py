"""Repository for career module language operations."""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from .db_models import LanguageDB


class LanguageRepository:
    """Repository for language database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_by_profile(self, profile_id: str) -> list[LanguageDB]:
        result = await self.db.execute(select(LanguageDB).where(LanguageDB.profile_id == profile_id).order_by(LanguageDB.display_order))
        return list(result.scalars().all())

    async def get_by_id_and_profile(self, id_: str, profile_id: str) -> LanguageDB | None:
        result = await self.db.execute(select(LanguageDB).where(LanguageDB.id == id_, LanguageDB.profile_id == profile_id))
        return result.scalar_one_or_none()

    async def get_by_ids_and_profile(self, ids: list[str], profile_id: str) -> list[LanguageDB]:
        if not ids:
            return []
        result = await self.db.execute(select(LanguageDB).where(LanguageDB.id.in_(ids), LanguageDB.profile_id == profile_id))
        return list(result.scalars().all())

    async def get_by_profile_and_name(self, profile_id: str, name: str) -> LanguageDB | None:
        result = await self.db.execute(select(LanguageDB).where(LanguageDB.profile_id == profile_id, LanguageDB.name == name))
        return result.scalar_one_or_none()

    async def get_next_display_order(self, profile_id: str) -> int:
        result = await self.db.execute(select(func.max(LanguageDB.display_order)).where(LanguageDB.profile_id == profile_id))
        current_max = result.scalar_one_or_none()
        return (current_max + 1) if current_max is not None else 0

    async def create(self, language: LanguageDB) -> LanguageDB:
        self.db.add(language)
        await self.db.commit()
        await self.db.refresh(language)
        return language

    async def save(self, language: LanguageDB) -> LanguageDB:
        await self.db.commit()
        await self.db.refresh(language)
        return language

    async def delete(self, language: LanguageDB) -> None:
        await self.db.delete(language)
        await self.db.commit()

    async def reorder(self, entries: list[LanguageDB], ordered_ids: list[str]) -> None:
        by_id = {entry.id: entry for entry in entries}
        for index, entry_id in enumerate(ordered_ids):
            by_id[entry_id].display_order = index
        await self.db.commit()
