"""Repository for career module CV version operations (career module, Phase 5)."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .db_models import CvVersionDB


class CvVersionRepository:
    """Repository for CV version database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_by_profile(self, profile_id: str) -> list[CvVersionDB]:
        result = await self.db.execute(select(CvVersionDB).where(CvVersionDB.profile_id == profile_id).order_by(CvVersionDB.created_at))
        return list(result.scalars().all())

    async def get_by_id_and_profile(self, id_: str, profile_id: str) -> CvVersionDB | None:
        result = await self.db.execute(select(CvVersionDB).where(CvVersionDB.id == id_, CvVersionDB.profile_id == profile_id))
        return result.scalar_one_or_none()

    async def create(self, cv_version: CvVersionDB) -> CvVersionDB:
        self.db.add(cv_version)
        await self.db.commit()
        await self.db.refresh(cv_version)
        return cv_version

    async def save(self, cv_version: CvVersionDB) -> CvVersionDB:
        await self.db.commit()
        await self.db.refresh(cv_version)
        return cv_version

    async def delete(self, cv_version: CvVersionDB) -> None:
        await self.db.delete(cv_version)
        await self.db.commit()

    async def clear_default(self, profile_id: str, except_id: str | None = None) -> None:
        """Unset ``is_default`` on every other CV version for the profile, enforcing
        at most one default per profile."""
        cv_versions = await self.list_by_profile(profile_id)
        changed = False
        for cv_version in cv_versions:
            if cv_version.id != except_id and cv_version.is_default:
                cv_version.is_default = False
                changed = True
        if changed:
            await self.db.commit()
