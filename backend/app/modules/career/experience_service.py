"""Business logic for work experiences (career module, Phase 2)."""

from datetime import date

from app.common.id_utils import generate_id

from .db_models import ExperienceDB, TechnologyDB
from .experience_repository import ExperienceRepository, ExperienceTechnologyRepository
from .schemas import CreateExperienceRequest, ExperienceResponse, TechnologyResponse, UpdateExperienceRequest
from .technology_repository import TechnologyRepository
from .technology_service import TechnologyService


def _build_response(experience: ExperienceDB, technologies: list[TechnologyDB]) -> ExperienceResponse:
    # Keyword args use the schema's snake_case aliases, not the camelCase field
    # names — mypy's pydantic plugin only recognizes the alias in the synthesized
    # constructor signature, even with populate_by_name=True.
    return ExperienceResponse(
        id=experience.id,
        profile_id=experience.profile_id,
        company_name=experience.company_name,
        position=experience.position,
        employment_type=experience.employment_type,
        start_date=experience.start_date,
        end_date=experience.end_date,
        is_current=experience.is_current,
        description=experience.description,
        responsibilities=list(experience.responsibilities or []),
        display_order=experience.display_order,
        technologies=[TechnologyResponse.model_validate(t) for t in technologies],
        created_at=experience.created_at,
        updated_at=experience.updated_at,
    )


class ExperienceService:
    """Business logic for work-experience CRUD, technology linking, and reordering."""

    def __init__(
        self,
        repository: ExperienceRepository,
        junction_repository: ExperienceTechnologyRepository,
        technology_repository: TechnologyRepository,
        technology_service: TechnologyService,
    ):
        self.repository = repository
        self.junction_repository = junction_repository
        self.technology_repository = technology_repository
        self.technology_service = technology_service

    def _validate_dates(self, start_date: date, end_date: date | None) -> None:
        if end_date is not None and end_date <= start_date:
            raise ValueError("End date must be after start date.")

    async def _technologies_for(self, experience_ids: list[str]) -> dict[str, list[TechnologyDB]]:
        by_experience_ids = await self.junction_repository.get_technology_ids_by_experience_ids(experience_ids)
        all_technology_ids = {tid for ids in by_experience_ids.values() for tid in ids}
        technologies = await self.technology_repository.get_by_ids(list(all_technology_ids))
        technologies_by_id = {t.id: t for t in technologies}
        return {experience_id: [technologies_by_id[tid] for tid in tech_ids if tid in technologies_by_id] for experience_id, tech_ids in by_experience_ids.items()}

    async def list_for_profile(self, profile_id: str) -> list[ExperienceResponse]:
        experiences = await self.repository.list_by_profile(profile_id)
        technologies_by_experience = await self._technologies_for([e.id for e in experiences])
        return [_build_response(experience, technologies_by_experience.get(experience.id, [])) for experience in experiences]

    async def get_entity_for_profile(self, id_: str, profile_id: str) -> ExperienceDB | None:
        """Raw ORM lookup, scoped to the owning profile — for routers that need to
        pass the entity into ``update``/``delete`` rather than just render it."""
        return await self.repository.get_by_id_and_profile(id_, profile_id)

    async def get_for_profile(self, id_: str, profile_id: str) -> ExperienceResponse | None:
        experience = await self.repository.get_by_id_and_profile(id_, profile_id)
        if experience is None:
            return None
        technologies_by_experience = await self._technologies_for([experience.id])
        return _build_response(experience, technologies_by_experience.get(experience.id, []))

    async def create(self, profile_id: str, payload: CreateExperienceRequest) -> ExperienceResponse:
        self._validate_dates(payload.startDate, payload.endDate)
        display_order = await self.repository.get_next_display_order(profile_id)
        experience = ExperienceDB(
            id=generate_id(),
            profile_id=profile_id,
            company_name=payload.companyName,
            position=payload.position,
            employment_type=payload.employmentType,
            start_date=payload.startDate,
            end_date=payload.endDate,
            is_current=payload.isCurrent,
            description=payload.description,
            responsibilities=list(payload.responsibilities),
            display_order=display_order,
        )
        experience = await self.repository.create(experience)

        technologies = await self.technology_service.resolve_by_names(payload.technologies)
        await self.junction_repository.replace_technologies(experience.id, [t.id for t in technologies])
        return _build_response(experience, technologies)

    async def update(self, experience: ExperienceDB, payload: UpdateExperienceRequest) -> ExperienceResponse:
        if payload.companyName is not None:
            experience.company_name = payload.companyName
        if payload.position is not None:
            experience.position = payload.position
        if payload.employmentType is not None:
            experience.employment_type = payload.employmentType
        if payload.startDate is not None:
            experience.start_date = payload.startDate
        if payload.endDate is not None:
            experience.end_date = payload.endDate
        if payload.isCurrent is not None:
            experience.is_current = payload.isCurrent
        if payload.description is not None:
            experience.description = payload.description
        if payload.responsibilities is not None:
            experience.responsibilities = list(payload.responsibilities)

        self._validate_dates(experience.start_date, experience.end_date)
        experience = await self.repository.save(experience)

        if payload.technologies is not None:
            technologies = await self.technology_service.resolve_by_names(payload.technologies)
            await self.junction_repository.replace_technologies(experience.id, [t.id for t in technologies])
        else:
            technologies_by_experience = await self._technologies_for([experience.id])
            technologies = technologies_by_experience.get(experience.id, [])

        return _build_response(experience, technologies)

    async def delete(self, experience: ExperienceDB) -> None:
        await self.repository.delete(experience)

    async def reorder(self, profile_id: str, ordered_ids: list[str]) -> list[ExperienceResponse]:
        experiences = await self.repository.list_by_profile(profile_id)
        if {e.id for e in experiences} != set(ordered_ids) or len(ordered_ids) != len(experiences):
            raise ValueError("orderedIds must contain exactly the profile's existing experience ids.")

        await self.repository.reorder(experiences, ordered_ids)
        return await self.list_for_profile(profile_id)
