"""FastAPI dependencies for authentication and authorization."""

from typing import Annotated, Optional

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import InvalidTokenError, UserNotFoundError, InactiveUserError
from app.core.security import verify_token
from app.models.user import User

# Security scheme for Bearer token
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)
) -> User:
    """
    Get current authenticated user from JWT token.

    Validates the Bearer token, extracts user ID, and fetches user from database.
    Checks that user exists and is active.

    Args:
        credentials: HTTP Bearer token credentials
        db: Database session

    Returns:
        User: Authenticated user object

    Raises:
        InvalidTokenError: If token is invalid, expired, or malformed
        UserNotFoundError: If user doesn't exist in database
        InactiveUserError: If user account is not active
    """
    # Validate Bearer scheme
    if credentials.scheme.lower() != "bearer":
        raise InvalidTokenError("Invalid authentication scheme")

    # Verify token (checks blacklist and JWT validity)
    payload = verify_token(credentials.credentials)

    # Get user ID from token (ULID as string)
    user_id: Optional[str] = payload.get("sub")
    if not user_id:
        raise InvalidTokenError("Invalid token payload")

    # Basic validation that it looks like a ULID (26 characters, alphanumeric)
    if not isinstance(user_id, str) or len(user_id) != 26:
        raise InvalidTokenError("Invalid user ID format in token")

    # Get user from database
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise UserNotFoundError()

    if not user.is_active:
        raise InactiveUserError()

    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Get current active user (alias for clarity).

    This is functionally the same as get_current_user but provides
    a clearer semantic meaning in endpoints that specifically require
    an active user.

    Args:
        current_user: User from get_current_user dependency

    Returns:
        User: Active user object
    """
    return current_user


# ============================================================================
# Type Aliases for Cleaner Endpoint Signatures
# ============================================================================

CurrentUser = Annotated[User, Depends(get_current_user)]
"""Type alias for current authenticated user dependency."""

CurrentActiveUser = Annotated[User, Depends(get_current_active_user)]
"""Type alias for current active user dependency."""

BearerCredentials = Annotated[HTTPAuthorizationCredentials, Depends(security)]
"""Type alias for HTTP Bearer token credentials."""

DBSession = Annotated[Session, Depends(get_db)]
"""Type alias for database session dependency."""


# ============================================================================
# Dependency Registry (Optional - for advanced use cases)
# ============================================================================


class Dependencies:
    """
    Central dependency registry for common dependencies.

    Provides static methods that return dependency functions for use in endpoints.

    Usage:
        from app.core.dependencies import CurrentActiveUser

        @router.get("/me")
        async def get_me(user: CurrentActiveUser) -> UserResponse:
            return UserResponse.model_validate(user)
    """

    @staticmethod
    def current_user() -> User:
        """Get current authenticated user."""
        return Depends(get_current_user)

    @staticmethod
    def active_user() -> User:
        """Get current active user."""
        return Depends(get_current_active_user)

    @staticmethod
    def bearer_credentials() -> HTTPAuthorizationCredentials:
        """Get Bearer token credentials."""
        return Depends(security)

    @staticmethod
    def db_session() -> Session:
        """Get database session."""
        return Depends(get_db)
