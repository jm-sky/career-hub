"""Career-module-local FastAPI dependencies."""

from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.modules.auth.auth_utils import verify_token
from app.modules.auth.repositories import get_user_repository
from app.modules.auth.types.repository import UserRepositoryInterface

from .repository import ProfileRepository
from .service import ProfileService

_optional_security = HTTPBearer(auto_error=False)


async def get_optional_user_id(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None, Depends(_optional_security)
    ],
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
