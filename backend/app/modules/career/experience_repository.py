"""Repository for career module experience + experience-technology operations
(career module, Phase 2)."""

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from .db_models import ExperienceDB, ExperienceTechnologyDB


class ExperienceRepository:
    """Repository for work-experience database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_by_profile(self, profile_id: str) -> list[ExperienceDB]:
        result = await self.db.execute(select(ExperienceDB).where(ExperienceDB.profile_id == profile_id).order_by(ExperienceDB.display_order))
        return list(result.scalars().all())

    async def get_by_id_and_profile(self, id_: str, profile_id: str) -> ExperienceDB | None:
        result = await self.db.execute(select(ExperienceDB).where(ExperienceDB.id == id_, ExperienceDB.profile_id == profile_id))
        return result.scalar_one_or_none()

    async def get_next_display_order(self, profile_id: str) -> int:
        result = await self.db.execute(select(func.max(ExperienceDB.display_order)).where(ExperienceDB.profile_id == profile_id))
        current_max = result.scalar_one_or_none()
        return (current_max + 1) if current_max is not None else 0

    async def create(self, experience: ExperienceDB) -> ExperienceDB:
        self.db.add(experience)
        await self.db.commit()
        await self.db.refresh(experience)
        return experience

    async def save(self, experience: ExperienceDB) -> ExperienceDB:
        await self.db.commit()
        await self.db.refresh(experience)
        return experience

    async def delete(self, experience: ExperienceDB) -> None:
        await self.db.delete(experience)
        await self.db.commit()

    async def reorder(self, experiences: list[ExperienceDB], ordered_ids: list[str]) -> None:
        """Assign ``display_order`` per position in ``ordered_ids``.

        Caller is responsible for validating that ``ordered_ids`` is exactly the set
        of ids in ``experiences`` before calling this.
        """
        by_id = {experience.id: experience for experience in experiences}
        for index, experience_id in enumerate(ordered_ids):
            by_id[experience_id].display_order = index
        await self.db.commit()


class ExperienceTechnologyRepository:
    """Repository for the experience<->technology M:N junction table."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_technology_ids_by_experience_ids(self, experience_ids: list[str]) -> dict[str, list[str]]:
        if not experience_ids:
            return {}
        result = await self.db.execute(select(ExperienceTechnologyDB.experience_id, ExperienceTechnologyDB.technology_id).where(ExperienceTechnologyDB.experience_id.in_(experience_ids)))
        by_experience: dict[str, list[str]] = {}
        for experience_id, technology_id in result.all():
            by_experience.setdefault(experience_id, []).append(technology_id)
        return by_experience

    async def replace_technologies(self, experience_id: str, technology_ids: list[str]) -> None:
        """Fully replace the technology set linked to an experience."""
        await self.db.execute(delete(ExperienceTechnologyDB).where(ExperienceTechnologyDB.experience_id == experience_id))
        for technology_id in technology_ids:
            self.db.add(ExperienceTechnologyDB(experience_id=experience_id, technology_id=technology_id))
        await self.db.commit()
