"""Repository for career module achievement operations (career module, Phase 4)."""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from .db_models import AchievementDB


class AchievementRepository:
    """Repository for achievement database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_by_profile(self, profile_id: str) -> list[AchievementDB]:
        result = await self.db.execute(select(AchievementDB).where(AchievementDB.profile_id == profile_id).order_by(AchievementDB.display_order))
        return list(result.scalars().all())

    async def get_by_id_and_profile(self, id_: str, profile_id: str) -> AchievementDB | None:
        result = await self.db.execute(select(AchievementDB).where(AchievementDB.id == id_, AchievementDB.profile_id == profile_id))
        return result.scalar_one_or_none()

    async def get_by_ids_and_profile(self, ids: list[str], profile_id: str) -> list[AchievementDB]:
        """Bulk ownership-scoped lookup — used to validate a batch of achievement ids
        (e.g. a CV version's ``sectionsConfig.achievementIds``) all belong to the profile."""
        if not ids:
            return []
        result = await self.db.execute(select(AchievementDB).where(AchievementDB.id.in_(ids), AchievementDB.profile_id == profile_id))
        return list(result.scalars().all())

    async def get_next_display_order(self, profile_id: str) -> int:
        result = await self.db.execute(select(func.max(AchievementDB.display_order)).where(AchievementDB.profile_id == profile_id))
        current_max = result.scalar_one_or_none()
        return (current_max + 1) if current_max is not None else 0

    async def create(self, achievement: AchievementDB) -> AchievementDB:
        self.db.add(achievement)
        await self.db.commit()
        await self.db.refresh(achievement)
        return achievement

    async def save(self, achievement: AchievementDB) -> AchievementDB:
        await self.db.commit()
        await self.db.refresh(achievement)
        return achievement

    async def delete(self, achievement: AchievementDB) -> None:
        await self.db.delete(achievement)
        await self.db.commit()

    async def reorder(self, entries: list[AchievementDB], ordered_ids: list[str]) -> None:
        """Assign ``display_order`` per position in ``ordered_ids``.

        Caller is responsible for validating that ``ordered_ids`` is exactly the set
        of ids in ``entries`` before calling this.
        """
        by_id = {entry.id: entry for entry in entries}
        for index, entry_id in enumerate(ordered_ids):
            by_id[entry_id].display_order = index
        await self.db.commit()
