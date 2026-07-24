"""Business logic for skills (career module, Phase 2)."""

from app.common.id_utils import generate_id

from .db_models import SkillDB, TechnologyDB
from .schemas import (
    BulkSkillsRequest,
    CreateSkillRequest,
    SkillResponse,
    TechnologyResponse,
    UpdateSkillRequest,
)
from .skill_repository import SkillRepository
from .technology_service import TechnologyService


def _build_response(skill: SkillDB, technology: TechnologyDB) -> SkillResponse:
    # Keyword args use the schema's snake_case aliases, not the camelCase field
    # names — mypy's pydantic plugin only recognizes the alias in the synthesized
    # constructor signature, even with populate_by_name=True.
    return SkillResponse(
        id=skill.id,
        profile_id=skill.profile_id,
        technology=TechnologyResponse.model_validate(technology),
        level=skill.level,
        years_of_experience=skill.years_of_experience,
        started_using_year=skill.started_using_year,
        is_primary=skill.is_primary,
        created_at=skill.created_at,
        updated_at=skill.updated_at,
    )


class SkillService:
    """Business logic for skill CRUD, bulk upsert, and (stubbed) AI suggestions."""

    def __init__(self, repository: SkillRepository, technology_service: TechnologyService):
        self.repository = repository
        self.technology_service = technology_service

    async def list_for_profile(self, profile_id: str) -> list[SkillResponse]:
        rows = await self.repository.list_by_profile(profile_id)
        return [_build_response(skill, technology) for skill, technology in rows]

    async def get_entity_for_profile(self, id_: str, profile_id: str) -> tuple[SkillDB, TechnologyDB] | None:
        """Raw ORM lookup, scoped to the owning profile — for routers that need to
        pass the entity into ``update``/``delete`` rather than just render it."""
        return await self.repository.get_by_id_and_profile(id_, profile_id)

    async def get_for_profile(self, id_: str, profile_id: str) -> SkillResponse | None:
        row = await self.repository.get_by_id_and_profile(id_, profile_id)
        if row is None:
            return None
        return _build_response(*row)

    async def create(self, profile_id: str, payload: CreateSkillRequest) -> SkillResponse:
        technology = await self.technology_service.resolve_by_name(payload.technologyName)
        existing = await self.repository.get_by_profile_and_technology(profile_id, technology.id)
        if existing is not None:
            raise ValueError(f"A skill for '{technology.name}' already exists on this profile.")

        skill = await self.repository.create(
            SkillDB(
                id=generate_id(),
                profile_id=profile_id,
                technology_id=technology.id,
                level=payload.level,
                years_of_experience=payload.yearsOfExperience,
                started_using_year=payload.startedUsingYear,
                is_primary=payload.isPrimary,
            )
        )
        return _build_response(skill, technology)

    async def bulk_upsert(self, profile_id: str, payload: BulkSkillsRequest) -> list[SkillResponse]:
        """Add or update each entry, keyed by technology — no conflict errors, unlike
        the single-create endpoint, since bulk import is expected to overlap."""
        responses = []
        for item in payload.skills:
            technology = await self.technology_service.resolve_by_name(item.technologyName)
            existing = await self.repository.get_by_profile_and_technology(profile_id, technology.id)
            if existing is not None:
                existing.level = item.level
                existing.years_of_experience = item.yearsOfExperience
                existing.started_using_year = item.startedUsingYear
                existing.is_primary = item.isPrimary
                skill = await self.repository.save(existing)
            else:
                skill = await self.repository.create(
                    SkillDB(
                        id=generate_id(),
                        profile_id=profile_id,
                        technology_id=technology.id,
                        level=item.level,
                        years_of_experience=item.yearsOfExperience,
                        started_using_year=item.startedUsingYear,
                        is_primary=item.isPrimary,
                    )
                )
            responses.append(_build_response(skill, technology))
        return responses

    async def update(self, skill: SkillDB, technology: TechnologyDB, payload: UpdateSkillRequest) -> SkillResponse:
        if payload.level is not None:
            skill.level = payload.level
        if payload.yearsOfExperience is not None:
            skill.years_of_experience = payload.yearsOfExperience
        if payload.startedUsingYear is not None:
            skill.started_using_year = payload.startedUsingYear
        if payload.isPrimary is not None:
            skill.is_primary = payload.isPrimary

        skill = await self.repository.save(skill)
        return _build_response(skill, technology)

    async def delete(self, skill: SkillDB) -> None:
        await self.repository.delete(skill)
