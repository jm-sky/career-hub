"""Business logic for projects (career module, Phase 3)."""

from datetime import date

from app.common.id_utils import generate_id

from .db_models import ProjectDB, TechnologyDB
from .experience_repository import ExperienceRepository
from .project_repository import ProjectExperienceRepository, ProjectRepository, ProjectTechnologyRepository
from .schemas import (
    CreateProjectRequest,
    ProjectLinks,
    ProjectResponse,
    TechnologyResponse,
    UpdateProjectRequest,
)
from .technology_repository import TechnologyRepository
from .technology_service import TechnologyService


def _build_response(project: ProjectDB, technologies: list[TechnologyDB], experience_ids: list[str]) -> ProjectResponse:
    # Keyword args use the schema's snake_case aliases where one is set, or the
    # literal field name otherwise — see the mypy/pydantic note in experience_service.py.
    return ProjectResponse(
        id=project.id,
        profile_id=project.profile_id,
        name=project.name,
        description=project.description,
        role=project.role,
        start_date=project.start_date,
        end_date=project.end_date,
        is_ongoing=project.is_ongoing,
        is_anonymized=project.is_anonymized,
        anonymized_company=project.anonymized_company,
        status=project.status,
        category=project.category,
        achievements=list(project.achievements or []),
        challenges=list(project.challenges or []),
        clients=list(project.clients or []),
        team_size=project.team_size,
        duration_months=project.duration_months,
        users_count=project.users_count,
        budget_range=project.budget_range,
        links=ProjectLinks(**(project.links or {})),
        visibility=project.visibility,
        display_order=project.display_order,
        technologies=[TechnologyResponse.model_validate(t) for t in technologies],
        experienceIds=experience_ids,
        created_at=project.created_at,
        updated_at=project.updated_at,
    )


class ProjectService:
    """Business logic for project CRUD, technology/experience linking, and reordering."""

    def __init__(
        self,
        repository: ProjectRepository,
        technology_junction_repository: ProjectTechnologyRepository,
        experience_junction_repository: ProjectExperienceRepository,
        technology_repository: TechnologyRepository,
        technology_service: TechnologyService,
        experience_repository: ExperienceRepository,
    ):
        self.repository = repository
        self.technology_junction_repository = technology_junction_repository
        self.experience_junction_repository = experience_junction_repository
        self.technology_repository = technology_repository
        self.technology_service = technology_service
        self.experience_repository = experience_repository

    def _validate_dates(self, start_date: date, end_date: date | None) -> None:
        if end_date is not None and end_date <= start_date:
            raise ValueError("End date must be after start date.")

    async def _validate_experience_ids(self, profile_id: str, experience_ids: list[str]) -> None:
        if not experience_ids:
            return
        owned = await self.experience_repository.get_by_ids_and_profile(experience_ids, profile_id)
        if len(owned) != len(set(experience_ids)):
            raise ValueError("One or more experienceIds do not belong to this profile.")

    async def _technologies_for(self, project_ids: list[str]) -> dict[str, list[TechnologyDB]]:
        by_project_ids = await self.technology_junction_repository.get_technology_ids_by_project_ids(project_ids)
        all_technology_ids = {tid for ids in by_project_ids.values() for tid in ids}
        technologies = await self.technology_repository.get_by_ids(list(all_technology_ids))
        technologies_by_id = {t.id: t for t in technologies}
        return {project_id: [technologies_by_id[tid] for tid in tech_ids if tid in technologies_by_id] for project_id, tech_ids in by_project_ids.items()}

    async def list_for_profile(self, profile_id: str) -> list[ProjectResponse]:
        projects = await self.repository.list_by_profile(profile_id)
        project_ids = [p.id for p in projects]
        technologies_by_project = await self._technologies_for(project_ids)
        experience_ids_by_project = await self.experience_junction_repository.get_experience_ids_by_project_ids(project_ids)
        return [
            _build_response(
                project,
                technologies_by_project.get(project.id, []),
                experience_ids_by_project.get(project.id, []),
            )
            for project in projects
        ]

    async def get_entity_for_profile(self, id_: str, profile_id: str) -> ProjectDB | None:
        """Raw ORM lookup, scoped to the owning profile — for routers that need to
        pass the entity into ``update``/``delete`` rather than just render it."""
        return await self.repository.get_by_id_and_profile(id_, profile_id)

    async def _response_for(self, project: ProjectDB) -> ProjectResponse:
        technologies_by_project = await self._technologies_for([project.id])
        experience_ids_by_project = await self.experience_junction_repository.get_experience_ids_by_project_ids([project.id])
        return _build_response(
            project,
            technologies_by_project.get(project.id, []),
            experience_ids_by_project.get(project.id, []),
        )

    async def create(self, profile_id: str, payload: CreateProjectRequest) -> ProjectResponse:
        self._validate_dates(payload.startDate, payload.endDate)
        await self._validate_experience_ids(profile_id, payload.experienceIds)

        display_order = await self.repository.get_next_display_order(profile_id)
        project = ProjectDB(
            id=generate_id(),
            profile_id=profile_id,
            name=payload.name,
            description=payload.description,
            role=payload.role,
            start_date=payload.startDate,
            end_date=payload.endDate,
            is_ongoing=payload.isOngoing,
            is_anonymized=payload.isAnonymized,
            anonymized_company=payload.anonymizedCompany,
            status=payload.status,
            category=payload.category,
            achievements=list(payload.achievements),
            challenges=list(payload.challenges),
            clients=list(payload.clients),
            team_size=payload.teamSize,
            duration_months=payload.durationMonths,
            users_count=payload.usersCount,
            budget_range=payload.budgetRange,
            links=payload.links.model_dump(exclude_none=True),
            visibility=payload.visibility,
            display_order=display_order,
        )
        project = await self.repository.create(project)

        technologies = await self.technology_service.resolve_by_names(payload.technologies)
        await self.technology_junction_repository.replace_technologies(project.id, [t.id for t in technologies])
        await self.experience_junction_repository.replace_experiences(project.id, payload.experienceIds)

        return _build_response(project, technologies, payload.experienceIds)

    async def update(self, project: ProjectDB, payload: UpdateProjectRequest) -> ProjectResponse:
        if payload.experienceIds is not None:
            await self._validate_experience_ids(project.profile_id, payload.experienceIds)

        if payload.name is not None:
            project.name = payload.name
        if payload.description is not None:
            project.description = payload.description
        if payload.role is not None:
            project.role = payload.role
        if payload.startDate is not None:
            project.start_date = payload.startDate
        if payload.endDate is not None:
            project.end_date = payload.endDate
        if payload.isOngoing is not None:
            project.is_ongoing = payload.isOngoing
        if payload.isAnonymized is not None:
            project.is_anonymized = payload.isAnonymized
        if payload.anonymizedCompany is not None:
            project.anonymized_company = payload.anonymizedCompany
        if payload.status is not None:
            project.status = payload.status
        if payload.category is not None:
            project.category = payload.category
        if payload.achievements is not None:
            project.achievements = list(payload.achievements)
        if payload.challenges is not None:
            project.challenges = list(payload.challenges)
        if payload.clients is not None:
            project.clients = list(payload.clients)
        if payload.teamSize is not None:
            project.team_size = payload.teamSize
        if payload.durationMonths is not None:
            project.duration_months = payload.durationMonths
        if payload.usersCount is not None:
            project.users_count = payload.usersCount
        if payload.budgetRange is not None:
            project.budget_range = payload.budgetRange
        if payload.links is not None:
            project.links = payload.links.model_dump(exclude_none=True)
        if payload.visibility is not None:
            project.visibility = payload.visibility

        self._validate_dates(project.start_date, project.end_date)
        project = await self.repository.save(project)

        if payload.technologies is not None:
            technologies = await self.technology_service.resolve_by_names(payload.technologies)
            await self.technology_junction_repository.replace_technologies(project.id, [t.id for t in technologies])
        if payload.experienceIds is not None:
            await self.experience_junction_repository.replace_experiences(project.id, payload.experienceIds)

        return await self._response_for(project)

    async def delete(self, project: ProjectDB) -> None:
        await self.repository.delete(project)

    async def reorder(self, profile_id: str, ordered_ids: list[str]) -> list[ProjectResponse]:
        projects = await self.repository.list_by_profile(profile_id)
        if {p.id for p in projects} != set(ordered_ids) or len(ordered_ids) != len(projects):
            raise ValueError("orderedIds must contain exactly the profile's existing project ids.")

        await self.repository.reorder(projects, ordered_ids)
        return await self.list_for_profile(profile_id)
