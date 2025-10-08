"""Project API endpoints."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.models.user import User
from app.schemas.project import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    ProjectReorderRequest,
)
from app.services.project_service import (
    ProjectService,
    ProjectNotFoundError,
)

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    project_data: ProjectCreate,
    profile_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Create a new project for a profile."""
    service = ProjectService(db)

    try:
        project = service.create_project(profile_id, current_user.id, project_data)
        return project.to_dict()
    except ProjectNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Get a project by ID."""
    service = ProjectService(db)

    project = service.get_project_by_id(project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    # Check if user can view this project through profile ownership
    from app.services.profile_service import ProfileService

    profile_service = ProfileService(db)
    profile = profile_service.get_profile_by_id(project.profile_id)

    if not profile or not profile.can_view(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to view this project"
        )

    return project.to_dict()


@router.patch("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: str,
    project_data: ProjectUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Update a project."""
    service = ProjectService(db)

    try:
        project = service.update_project(project_id, current_user.id, project_data)
        return project.to_dict()
    except ProjectNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Delete a project."""
    service = ProjectService(db)

    try:
        service.delete_project(project_id, current_user.id)
    except ProjectNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/profile/{profile_id}", response_model=List[ProjectResponse])
def get_profile_projects(
    profile_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Get all projects for a profile."""
    from app.services.profile_service import ProfileService

    profile_service = ProfileService(db)
    profile = profile_service.get_profile_by_id(profile_id)

    if not profile or not profile.can_view(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to view this profile"
        )

    service = ProjectService(db)
    projects = service.get_profile_projects(profile_id)

    return [project.to_dict() for project in projects]


@router.post("/profile/{profile_id}/reorder", response_model=List[ProjectResponse])
def reorder_projects(
    profile_id: str,
    reorder_data: ProjectReorderRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Reorder projects for a profile."""
    service = ProjectService(db)

    try:
        projects = service.reorder_projects(profile_id, current_user.id, reorder_data.project_ids)
        return [project.to_dict() for project in projects]
    except ProjectNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
