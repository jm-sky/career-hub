"""Repository for career module education operations (career module, Phase 4)."""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from .db_models import EducationDB


class EducationRepository:
    """Repository for education database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_by_profile(self, profile_id: str) -> list[EducationDB]:
        result = await self.db.execute(select(EducationDB).where(EducationDB.profile_id == profile_id).order_by(EducationDB.display_order))
        return list(result.scalars().all())

    async def get_by_id_and_profile(self, id_: str, profile_id: str) -> EducationDB | None:
        result = await self.db.execute(select(EducationDB).where(EducationDB.id == id_, EducationDB.profile_id == profile_id))
        return result.scalar_one_or_none()

    async def get_next_display_order(self, profile_id: str) -> int:
        result = await self.db.execute(select(func.max(EducationDB.display_order)).where(EducationDB.profile_id == profile_id))
        current_max = result.scalar_one_or_none()
        return (current_max + 1) if current_max is not None else 0

    async def create(self, education: EducationDB) -> EducationDB:
        self.db.add(education)
        await self.db.commit()
        await self.db.refresh(education)
        return education

    async def save(self, education: EducationDB) -> EducationDB:
        await self.db.commit()
        await self.db.refresh(education)
        return education

    async def delete(self, education: EducationDB) -> None:
        await self.db.delete(education)
        await self.db.commit()

    async def reorder(self, entries: list[EducationDB], ordered_ids: list[str]) -> None:
        """Assign ``display_order`` per position in ``ordered_ids``.

        Caller is responsible for validating that ``ordered_ids`` is exactly the set
        of ids in ``entries`` before calling this.
        """
        by_id = {entry.id: entry for entry in entries}
        for index, entry_id in enumerate(ordered_ids):
            by_id[entry_id].display_order = index
        await self.db.commit()
