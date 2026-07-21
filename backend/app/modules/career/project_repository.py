"""Repository for career module project + project-junction operations
(career module, Phase 3)."""

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from .db_models import ProjectDB, ProjectExperienceDB, ProjectTechnologyDB


class ProjectRepository:
    """Repository for project database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_by_profile(self, profile_id: str) -> list[ProjectDB]:
        result = await self.db.execute(select(ProjectDB).where(ProjectDB.profile_id == profile_id).order_by(ProjectDB.display_order))
        return list(result.scalars().all())

    async def get_by_id_and_profile(self, id_: str, profile_id: str) -> ProjectDB | None:
        result = await self.db.execute(select(ProjectDB).where(ProjectDB.id == id_, ProjectDB.profile_id == profile_id))
        return result.scalar_one_or_none()

    async def get_next_display_order(self, profile_id: str) -> int:
        result = await self.db.execute(select(func.max(ProjectDB.display_order)).where(ProjectDB.profile_id == profile_id))
        current_max = result.scalar_one_or_none()
        return (current_max + 1) if current_max is not None else 0

    async def create(self, project: ProjectDB) -> ProjectDB:
        self.db.add(project)
        await self.db.commit()
        await self.db.refresh(project)
        return project

    async def save(self, project: ProjectDB) -> ProjectDB:
        await self.db.commit()
        await self.db.refresh(project)
        return project

    async def delete(self, project: ProjectDB) -> None:
        await self.db.delete(project)
        await self.db.commit()

    async def reorder(self, projects: list[ProjectDB], ordered_ids: list[str]) -> None:
        """Assign ``display_order`` per position in ``ordered_ids``.

        Caller is responsible for validating that ``ordered_ids`` is exactly the set
        of ids in ``projects`` before calling this.
        """
        by_id = {project.id: project for project in projects}
        for index, project_id in enumerate(ordered_ids):
            by_id[project_id].display_order = index
        await self.db.commit()


class ProjectTechnologyRepository:
    """Repository for the project<->technology M:N junction table."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_technology_ids_by_project_ids(self, project_ids: list[str]) -> dict[str, list[str]]:
        if not project_ids:
            return {}
        result = await self.db.execute(select(ProjectTechnologyDB.project_id, ProjectTechnologyDB.technology_id).where(ProjectTechnologyDB.project_id.in_(project_ids)))
        by_project: dict[str, list[str]] = {}
        for project_id, technology_id in result.all():
            by_project.setdefault(project_id, []).append(technology_id)
        return by_project

    async def replace_technologies(self, project_id: str, technology_ids: list[str]) -> None:
        """Fully replace the technology set linked to a project."""
        await self.db.execute(delete(ProjectTechnologyDB).where(ProjectTechnologyDB.project_id == project_id))
        for technology_id in technology_ids:
            self.db.add(ProjectTechnologyDB(project_id=project_id, technology_id=technology_id))
        await self.db.commit()


class ProjectExperienceRepository:
    """Repository for the project<->experience M:N junction table."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_experience_ids_by_project_ids(self, project_ids: list[str]) -> dict[str, list[str]]:
        if not project_ids:
            return {}
        result = await self.db.execute(select(ProjectExperienceDB.project_id, ProjectExperienceDB.experience_id).where(ProjectExperienceDB.project_id.in_(project_ids)))
        by_project: dict[str, list[str]] = {}
        for project_id, experience_id in result.all():
            by_project.setdefault(project_id, []).append(experience_id)
        return by_project

    async def replace_experiences(self, project_id: str, experience_ids: list[str]) -> None:
        """Fully replace the experience links for a project."""
        await self.db.execute(delete(ProjectExperienceDB).where(ProjectExperienceDB.project_id == project_id))
        for experience_id in experience_ids:
            self.db.add(ProjectExperienceDB(project_id=project_id, experience_id=experience_id))
        await self.db.commit()
