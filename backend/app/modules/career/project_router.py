"""Project endpoints for the career module (Phase 3)."""

from fastapi import APIRouter, Depends, HTTPException, status

from .dependencies import CurrentProfile, get_project_service
from .project_service import ProjectService
from .schemas import (
    CreateProjectRequest,
    ProjectResponse,
    ReorderRequest,
    UpdateProjectRequest,
)

router = APIRouter(prefix="/career", tags=["Career", "Projects"])


@router.get("/projects", response_model=list[ProjectResponse])
async def list_projects(
    *,
    profile: CurrentProfile,
    service: ProjectService = Depends(get_project_service),
) -> list[ProjectResponse]:
    """List the authenticated user's projects, ordered by display_order."""
    return await service.list_for_profile(profile.id)


@router.post("/projects", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    *,
    payload: CreateProjectRequest,
    profile: CurrentProfile,
    service: ProjectService = Depends(get_project_service),
) -> ProjectResponse:
    """Create a project, appended to the end of the display order."""
    try:
        return await service.create(profile.id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.put("/projects/reorder", response_model=list[ProjectResponse])
async def reorder_projects(
    *,
    payload: ReorderRequest,
    profile: CurrentProfile,
    service: ProjectService = Depends(get_project_service),
) -> list[ProjectResponse]:
    """Batch-reorder all of the authenticated user's projects.

    ``orderedIds`` must be exactly the full set of the profile's existing project
    ids — partial reorders are rejected rather than silently dropped.
    """
    try:
        return await service.reorder(profile.id, payload.orderedIds)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.put("/projects/{id}", response_model=ProjectResponse)
async def update_project(
    *,
    id: str,
    payload: UpdateProjectRequest,
    profile: CurrentProfile,
    service: ProjectService = Depends(get_project_service),
) -> ProjectResponse:
    """Partially update a project owned by the authenticated user."""
    project = await service.get_entity_for_profile(id, profile.id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    try:
        return await service.update(project, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.delete("/projects/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    *,
    id: str,
    profile: CurrentProfile,
    service: ProjectService = Depends(get_project_service),
) -> None:
    """Delete a project owned by the authenticated user."""
    project = await service.get_entity_for_profile(id, profile.id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    await service.delete(project)
