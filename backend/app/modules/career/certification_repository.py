"""Repository for career module certification operations (career module, Phase 4)."""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from .db_models import CertificationDB


class CertificationRepository:
    """Repository for certification database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_by_profile(self, profile_id: str) -> list[CertificationDB]:
        result = await self.db.execute(select(CertificationDB).where(CertificationDB.profile_id == profile_id).order_by(CertificationDB.display_order))
        return list(result.scalars().all())

    async def get_by_id_and_profile(self, id_: str, profile_id: str) -> CertificationDB | None:
        result = await self.db.execute(select(CertificationDB).where(CertificationDB.id == id_, CertificationDB.profile_id == profile_id))
        return result.scalar_one_or_none()

    async def get_next_display_order(self, profile_id: str) -> int:
        result = await self.db.execute(select(func.max(CertificationDB.display_order)).where(CertificationDB.profile_id == profile_id))
        current_max = result.scalar_one_or_none()
        return (current_max + 1) if current_max is not None else 0

    async def create(self, certification: CertificationDB) -> CertificationDB:
        self.db.add(certification)
        await self.db.commit()
        await self.db.refresh(certification)
        return certification

    async def save(self, certification: CertificationDB) -> CertificationDB:
        await self.db.commit()
        await self.db.refresh(certification)
        return certification

    async def delete(self, certification: CertificationDB) -> None:
        await self.db.delete(certification)
        await self.db.commit()

    async def reorder(self, entries: list[CertificationDB], ordered_ids: list[str]) -> None:
        """Assign ``display_order`` per position in ``ordered_ids``.

        Caller is responsible for validating that ``ordered_ids`` is exactly the set
        of ids in ``entries`` before calling this.
        """
        by_id = {entry.id: entry for entry in entries}
        for index, entry_id in enumerate(ordered_ids):
            by_id[entry_id].display_order = index
        await self.db.commit()
