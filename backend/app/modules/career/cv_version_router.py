"""CV version endpoints for the career module (Phase 5).

Generate/download are stubs — no PDF rendering engine has been chosen yet (see
the open question in `docs/plans/career-module-plan.md` Phase 5). They exist so
the frontend has a stable contract to build against; the download endpoint 404s
honestly rather than pretending a PDF exists.
"""

from fastapi import APIRouter, Depends, HTTPException, status

from .cv_version_service import CvVersionService
from .dependencies import CurrentProfile, get_cv_version_service
from .schemas import (
    CreateCvVersionRequest,
    CvVersionResponse,
    GenerateCvVersionResponse,
    UpdateCvVersionRequest,
)

router = APIRouter(prefix="/career", tags=["Career", "CV Versions"])


@router.get("/cv-versions", response_model=list[CvVersionResponse])
async def list_cv_versions(
    *,
    profile: CurrentProfile,
    service: CvVersionService = Depends(get_cv_version_service),
) -> list[CvVersionResponse]:
    """List the authenticated user's CV versions."""
    return await service.list_for_profile(profile.id)


@router.post("/cv-versions", response_model=CvVersionResponse, status_code=status.HTTP_201_CREATED)
async def create_cv_version(
    *,
    payload: CreateCvVersionRequest,
    profile: CurrentProfile,
    service: CvVersionService = Depends(get_cv_version_service),
) -> CvVersionResponse:
    """Create a CV version — a named, curated selection of profile sections."""
    try:
        return await service.create(profile.id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.put("/cv-versions/{id}", response_model=CvVersionResponse)
async def update_cv_version(
    *,
    id: str,
    payload: UpdateCvVersionRequest,
    profile: CurrentProfile,
    service: CvVersionService = Depends(get_cv_version_service),
) -> CvVersionResponse:
    """Partially update a CV version owned by the authenticated user."""
    cv_version = await service.get_entity_for_profile(id, profile.id)
    if cv_version is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CV version not found")
    try:
        return await service.update(cv_version, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.delete("/cv-versions/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cv_version(
    *,
    id: str,
    profile: CurrentProfile,
    service: CvVersionService = Depends(get_cv_version_service),
) -> None:
    """Delete a CV version owned by the authenticated user."""
    cv_version = await service.get_entity_for_profile(id, profile.id)
    if cv_version is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CV version not found")
    await service.delete(cv_version)


@router.post(
    "/cv-versions/{id}/generate",
    response_model=GenerateCvVersionResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def generate_cv_version(
    *,
    id: str,
    profile: CurrentProfile,
    service: CvVersionService = Depends(get_cv_version_service),
) -> GenerateCvVersionResponse:
    """Queue PDF generation for a CV version. Stub: accepts the request and hands
    back a job id, but no PDF is actually rendered yet."""
    cv_version = await service.get_entity_for_profile(id, profile.id)
    if cv_version is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CV version not found")
    return await service.generate(cv_version)


@router.get("/cv-versions/{id}/download")
async def download_cv_version(
    *,
    id: str,
    profile: CurrentProfile,
    service: CvVersionService = Depends(get_cv_version_service),
) -> dict[str, str]:
    """Return the generated PDF's URL. 404s if generation hasn't produced one yet
    (always true for now — no render pipeline exists)."""
    cv_version = await service.get_entity_for_profile(id, profile.id)
    if cv_version is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CV version not found")
    try:
        pdf_url = await service.get_pdf_url(cv_version)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return {"pdfUrl": pdf_url}
