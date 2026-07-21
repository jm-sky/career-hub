"""Repository for career module skill operations (career module, Phase 2)."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .db_models import SkillDB, TechnologyDB


class SkillRepository:
    """Repository for skill database operations. Every read joins in the linked
    technology, since a skill is never meaningfully rendered without it."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_by_profile(self, profile_id: str) -> list[tuple[SkillDB, TechnologyDB]]:
        result = await self.db.execute(select(SkillDB, TechnologyDB).join(TechnologyDB, SkillDB.technology_id == TechnologyDB.id).where(SkillDB.profile_id == profile_id).order_by(TechnologyDB.name))
        return [(skill, technology) for skill, technology in result.all()]

    async def get_by_id_and_profile(self, id_: str, profile_id: str) -> tuple[SkillDB, TechnologyDB] | None:
        result = await self.db.execute(select(SkillDB, TechnologyDB).join(TechnologyDB, SkillDB.technology_id == TechnologyDB.id).where(SkillDB.id == id_, SkillDB.profile_id == profile_id))
        row = result.first()
        return (row[0], row[1]) if row else None

    async def get_by_profile_and_technology(self, profile_id: str, technology_id: str) -> SkillDB | None:
        result = await self.db.execute(select(SkillDB).where(SkillDB.profile_id == profile_id, SkillDB.technology_id == technology_id))
        return result.scalar_one_or_none()

    async def get_by_ids_and_profile(self, ids: list[str], profile_id: str) -> list[SkillDB]:
        """Bulk ownership-scoped lookup — used to validate a batch of skill ids
        (e.g. a CV version's ``sectionsConfig.skillIds``) all belong to the profile."""
        if not ids:
            return []
        result = await self.db.execute(select(SkillDB).where(SkillDB.id.in_(ids), SkillDB.profile_id == profile_id))
        return list(result.scalars().all())

    async def create(self, skill: SkillDB) -> SkillDB:
        self.db.add(skill)
        await self.db.commit()
        await self.db.refresh(skill)
        return skill

    async def save(self, skill: SkillDB) -> SkillDB:
        await self.db.commit()
        await self.db.refresh(skill)
        return skill

    async def delete(self, skill: SkillDB) -> None:
        await self.db.delete(skill)
        await self.db.commit()
