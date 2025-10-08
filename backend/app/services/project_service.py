"""Project service for business logic."""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.project import Project
from app.models.profile import Profile
from app.schemas.project import ProjectCreate, ProjectUpdate


class ProjectNotFoundError(Exception):
    """Raised when project is not found."""
    pass


class ProjectService:
    """Service for managing projects."""

    def __init__(self, db: Session):
        self.db = db

    def create_project(
        self, profile_id: str, user_id: str, project_data: ProjectCreate
    ) -> Project:
        """Create a new project."""
        # Verify profile ownership
        profile = self.db.query(Profile).filter(Profile.id == profile_id).first()
        if not profile or profile.user_id != user_id:
            raise ProjectNotFoundError("Profile not found or access denied")

        # Get max display_order for this profile
        max_order = (
            self.db.query(Project)
            .filter(Project.profile_id == profile_id)
            .count()
        )

        project = Project(
            profile_id=profile_id,
            name=project_data.name,
            description=project_data.description,
            status=project_data.status,
            category=project_data.category,
            scale=project_data.scale,
            start_date=project_data.start_date,
            end_date=project_data.end_date,
            client=project_data.client,
            technologies=project_data.technologies,
            achievements=project_data.achievements,
            challenges=project_data.challenges,
            display_order=max_order,
        )

        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)

        return project

    def get_project_by_id(self, project_id: str) -> Optional[Project]:
        """Get a project by ID."""
        return self.db.query(Project).filter(Project.id == project_id).first()

    def get_profile_projects(self, profile_id: str) -> List[Project]:
        """Get all projects for a profile."""
        return (
            self.db.query(Project)
            .filter(Project.profile_id == profile_id)
            .order_by(Project.display_order.asc(), Project.created_at.desc())
            .all()
        )

    def update_project(
        self, project_id: str, user_id: str, project_data: ProjectUpdate
    ) -> Project:
        """Update a project."""
        project = self.get_project_by_id(project_id)
        if not project:
            raise ProjectNotFoundError("Project not found")

        # Verify ownership through profile
        profile = self.db.query(Profile).filter(Profile.id == project.profile_id).first()
        if not profile or profile.user_id != user_id:
            raise ProjectNotFoundError("Project not found or access denied")

        # Update fields
        update_data = project_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(project, field, value)

        self.db.commit()
        self.db.refresh(project)

        return project

    def delete_project(self, project_id: str, user_id: str) -> None:
        """Delete a project."""
        project = self.get_project_by_id(project_id)
        if not project:
            raise ProjectNotFoundError("Project not found")

        # Verify ownership through profile
        profile = self.db.query(Profile).filter(Profile.id == project.profile_id).first()
        if not profile or profile.user_id != user_id:
            raise ProjectNotFoundError("Project not found or access denied")

        self.db.delete(project)
        self.db.commit()

    def reorder_projects(
        self, profile_id: str, user_id: str, project_ids: List[str]
    ) -> List[Project]:
        """Reorder projects for a profile."""
        # Verify profile ownership
        profile = self.db.query(Profile).filter(Profile.id == profile_id).first()
        if not profile or profile.user_id != user_id:
            raise ProjectNotFoundError("Profile not found or access denied")

        # Update display_order for each project
        for index, project_id in enumerate(project_ids):
            project = self.get_project_by_id(project_id)
            if project and project.profile_id == profile_id:
                project.display_order = index

        self.db.commit()

        return self.get_profile_projects(profile_id)
