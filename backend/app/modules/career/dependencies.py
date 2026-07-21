"""Career-module-local FastAPI dependencies."""

from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.modules.auth.auth_utils import verify_token
from app.modules.auth.dependencies import CurrentUser
from app.modules.auth.repositories import get_user_repository
from app.modules.auth.types.repository import UserRepositoryInterface

from .achievement_repository import AchievementRepository
from .achievement_service import AchievementService
from .certification_repository import CertificationRepository
from .certification_service import CertificationService
from .db_models import ProfileDB
from .education_repository import EducationRepository
from .education_service import EducationService
from .experience_repository import ExperienceRepository, ExperienceTechnologyRepository
from .experience_service import ExperienceService
from .project_repository import (
    ProjectExperienceRepository,
    ProjectRepository,
    ProjectTechnologyRepository,
)
from .project_service import ProjectService
from .repository import ProfileRepository
from .service import ProfileService
from .skill_repository import SkillRepository
from .skill_service import SkillService
from .technology_repository import TechnologyRepository
from .technology_service import TechnologyService

_optional_security = HTTPBearer(auto_error=False)


async def get_optional_user_id(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_optional_security)],
    user_repository: Annotated[UserRepositoryInterface, Depends(get_user_repository)],
) -> str | None:
    """Best-effort viewer identification for public endpoints.

    Unlike ``get_current_user``, this never raises: a missing, expired, or invalid
    token simply means "anonymous viewer" rather than a 401. Used only to decide
    whether the requester happens to be the profile owner on the public slug
    endpoint — not a substitute for real auth on any endpoint that requires it.
    """
    if credentials is None:
        return None
    try:
        payload = verify_token(credentials.credentials, expected_type="access")
    except Exception:
        return None

    user_id = payload.get("sub")
    if not user_id:
        return None

    user = await user_repository.get_user_by_id(user_id)
    if user is None or not user.isActive:
        return None
    return user_id


OptionalUserId = Annotated[str | None, Depends(get_optional_user_id)]


def get_profile_service(db: AsyncSession = Depends(get_db)) -> ProfileService:
    return ProfileService(ProfileRepository(db))


async def get_current_profile(
    current_user: CurrentUser,
    profile_service: ProfileService = Depends(get_profile_service),
) -> ProfileDB:
    """The authenticated user's profile, auto-creating an empty one if needed.

    Shared by every Phase 2+ router (experiences/technologies/skills/...) so each
    doesn't have to repeat the get-or-create call itself.
    """
    return await profile_service.get_or_create_for_user(current_user.id, current_user.name)


CurrentProfile = Annotated[ProfileDB, Depends(get_current_profile)]


def get_technology_service(db: AsyncSession = Depends(get_db)) -> TechnologyService:
    return TechnologyService(TechnologyRepository(db))


def get_experience_service(db: AsyncSession = Depends(get_db)) -> ExperienceService:
    return ExperienceService(
        ExperienceRepository(db),
        ExperienceTechnologyRepository(db),
        TechnologyRepository(db),
        TechnologyService(TechnologyRepository(db)),
    )


def get_skill_service(db: AsyncSession = Depends(get_db)) -> SkillService:
    return SkillService(SkillRepository(db), TechnologyService(TechnologyRepository(db)))


def get_project_service(db: AsyncSession = Depends(get_db)) -> ProjectService:
    return ProjectService(
        ProjectRepository(db),
        ProjectTechnologyRepository(db),
        ProjectExperienceRepository(db),
        TechnologyRepository(db),
        TechnologyService(TechnologyRepository(db)),
        ExperienceRepository(db),
    )


def get_education_service(db: AsyncSession = Depends(get_db)) -> EducationService:
    return EducationService(EducationRepository(db))


def get_certification_service(db: AsyncSession = Depends(get_db)) -> CertificationService:
    return CertificationService(CertificationRepository(db))


def get_achievement_service(db: AsyncSession = Depends(get_db)) -> AchievementService:
    return AchievementService(AchievementRepository(db))
