"""Business logic for the global technologies reference table (career module,
Phase 2)."""

from app.common.id_utils import generate_id

from .db_models import TechnologyDB
from .technology_repository import TechnologyRepository


class TechnologyService:
    """Get-or-create resolution and search for the shared technology reference data."""

    def __init__(self, repository: TechnologyRepository):
        self.repository = repository

    async def resolve_by_names(self, names: list[str]) -> list[TechnologyDB]:
        """Get-or-create a technology per name, de-duplicated case-insensitively,
        preserving first-seen order. Powers the free-form tag-input UX on
        experiences and skills — unknown names become new reference rows."""
        resolved: dict[str, TechnologyDB] = {}
        for raw_name in names:
            name = raw_name.strip()
            if not name or name.lower() in resolved:
                continue
            technology = await self.repository.get_by_name(name)
            if technology is None:
                technology = await self.repository.create(TechnologyDB(id=generate_id(), name=name))
            resolved[name.lower()] = technology
        return list(resolved.values())

    async def resolve_by_name(self, name: str) -> TechnologyDB:
        """Get-or-create a single technology by name."""
        technology = await self.repository.get_by_name(name)
        if technology is None:
            technology = await self.repository.create(TechnologyDB(id=generate_id(), name=name))
        return technology

    async def search(self, query: str | None, limit: int = 20) -> list[TechnologyDB]:
        return await self.repository.search(query, limit)
