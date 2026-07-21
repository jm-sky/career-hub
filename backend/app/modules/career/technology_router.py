"""Global technology reference-data endpoints for the career module (Phase 2)."""

from fastapi import APIRouter, Depends

from app.modules.auth.dependencies import CurrentUser

from .dependencies import get_technology_service
from .schemas import TechnologyResponse
from .technology_service import TechnologyService

router = APIRouter(prefix="/career", tags=["Career", "Technologies"])


@router.get("/technologies", response_model=list[TechnologyResponse])
async def search_technologies(
    *,
    current_user: CurrentUser,
    q: str | None = None,
    limit: int = 20,
    service: TechnologyService = Depends(get_technology_service),
) -> list[TechnologyResponse]:
    """Search the shared technology reference table — powers autocomplete on the
    experience/skill tag inputs. Requires auth (not public) but is not scoped to any
    one profile, since technologies are a global reference, not owned data."""
    technologies = await service.search(q, min(limit, 100))
    return [TechnologyResponse.model_validate(t) for t in technologies]
