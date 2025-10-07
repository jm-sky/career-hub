"""Authentication service layer containing business logic."""

import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import (
    InvalidCredentialsError,
    InvalidTokenError,
    InvalidTokenTypeError,
    UserNotFoundError,
    InactiveUserError,
    InvalidResetTokenError,
    UserAlreadyExistsError,
)
from app.core.security import (
    create_access_token,
    create_refresh_token,
    create_password_reset_token,
    verify_token,
    token_blacklist,
)
from app.models.user import User
from app.schemas.auth import LoginResponse, TokenResponse, UserResponse


class AuthService:
    """
    Authentication service handling business logic for user authentication.

    Separates business logic from API endpoints for better testability
    and code organization.
    """

    @staticmethod
    def _create_login_response(user: User) -> LoginResponse:
        """
        Create login response with tokens for authenticated user.

        Args:
            user: Authenticated user object

        Returns:
            LoginResponse with user data and tokens
        """
        access_token = create_access_token({"sub": user.id})
        refresh_token = create_refresh_token({"sub": user.id})

        return LoginResponse(
            user=UserResponse.model_validate(user),
            accessToken=access_token,
            refreshToken=refresh_token,
            expiresIn=settings.security.access_token_expires_minutes * 60,
        )

    @staticmethod
    async def register_user(email: str, password: str, name: str, db: Session) -> LoginResponse:
        """
        Register new user and return authentication tokens.

        Args:
            email: User email address
            password: User password (will be hashed)
            name: User full name
            db: Database session

        Returns:
            LoginResponse with user data and tokens

        Raises:
            UserAlreadyExistsError: If email is already registered
        """
        # Normalize email to lowercase for case-insensitive storage
        normalized_email = email.lower().strip()

        # Check if user already exists
        existing_user = db.query(User).filter(User.email == normalized_email).first()
        if existing_user:
            raise UserAlreadyExistsError()

        # Create new user
        user = User(
            email=normalized_email,
            name=name,
        )
        user.set_password(password)

        db.add(user)
        db.commit()
        db.refresh(user)

        return AuthService._create_login_response(user)

    @staticmethod
    async def authenticate_user(email: str, password: str, db: Session) -> LoginResponse:
        """
        Authenticate user with email and password.

        Args:
            email: User email address
            password: User password
            db: Database session

        Returns:
            LoginResponse with user data and tokens

        Raises:
            InvalidCredentialsError: If credentials are invalid
            InactiveUserError: If user account is inactive
        """
        # Normalize email for case-insensitive lookup
        normalized_email = email.lower().strip()

        # Get user by email
        user = db.query(User).filter(User.email == normalized_email).first()
        if not user or not user.verify_password(password):
            raise InvalidCredentialsError()

        # Check if user is active
        if not user.is_active:
            raise InactiveUserError()

        return AuthService._create_login_response(user)

    @staticmethod
    async def refresh_tokens(refresh_token: str, db: Session) -> TokenResponse:
        """
        Refresh access token using refresh token.

        Args:
            refresh_token: Valid refresh token
            db: Database session

        Returns:
            TokenResponse with new access and refresh tokens

        Raises:
            InvalidTokenError: If token is invalid
            InvalidTokenTypeError: If token is not a refresh token
            UserNotFoundError: If user doesn't exist
            InactiveUserError: If user account is inactive
        """
        # Verify refresh token
        payload = verify_token(refresh_token)

        # Check if it's actually a refresh token
        if payload.get("type") != "refresh":
            raise InvalidTokenTypeError()

        # Get user ID (ULID as string)
        user_id = payload.get("sub")
        if not user_id:
            raise InvalidTokenError("Invalid token payload")

        # Basic validation that it looks like a ULID (26 characters)
        if not isinstance(user_id, str) or len(user_id) != 26:
            raise InvalidTokenError("Invalid user ID format in token")

        # Verify user exists and is active
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise UserNotFoundError()

        if not user.is_active:
            raise InactiveUserError()

        # Create new tokens
        new_access_token = create_access_token({"sub": user.id})
        new_refresh_token = create_refresh_token({"sub": user.id})

        return TokenResponse(
            accessToken=new_access_token,
            refreshToken=new_refresh_token,
            expiresIn=settings.security.access_token_expires_minutes * 60,
        )

    @staticmethod
    async def logout_user(access_token: str, user: User) -> None:
        """
        Logout user by blacklisting their access token.

        Args:
            access_token: User's access token to blacklist
            user: Current authenticated user
        """
        token_blacklist.add(access_token)

    @staticmethod
    async def get_user_profile(user: User) -> UserResponse:
        """
        Get user profile information.

        Args:
            user: Current authenticated user

        Returns:
            UserResponse with user data
        """
        return UserResponse.model_validate(user)

    @staticmethod
    async def request_password_reset(email: str, db: Session) -> Optional[str]:
        """
        Generate password reset token for user.

        Args:
            email: User email address
            db: Database session

        Returns:
            Reset token if user exists and is active, None otherwise
        """
        # Normalize email
        normalized_email = email.lower().strip()

        # Get user
        user = db.query(User).filter(User.email == normalized_email).first()
        if not user or not user.is_active:
            return None

        # Generate JWT reset token
        token = create_password_reset_token(data={"sub": user.id})

        # Store token in database
        user.set_reset_token(token, datetime.now(timezone.utc) + timedelta(hours=1))
        db.commit()

        return token

    @staticmethod
    async def reset_password(token: str, new_password: str, db: Session) -> bool:
        """
        Reset user password using reset token.

        Args:
            token: Password reset token
            new_password: New password to set
            db: Database session

        Returns:
            True if password was reset successfully

        Raises:
            InvalidResetTokenError: If token is invalid or expired
        """
        # Find user with valid reset token
        users = db.query(User).filter(User.reset_token.isnot(None)).all()

        for user in users:
            if user.is_reset_token_valid(token):
                user.set_password(new_password)
                user.clear_reset_token()
                db.commit()
                return True

        raise InvalidResetTokenError()

    @staticmethod
    async def change_password(user_id: str, current_password: str, new_password: str, db: Session) -> bool:
        """
        Change user password after verifying current password.

        Args:
            user_id: User ID
            current_password: Current password for verification
            new_password: New password to set
            db: Database session

        Returns:
            True if password was changed successfully

        Raises:
            InvalidCredentialsError: If current password is incorrect
            UserNotFoundError: If user doesn't exist
            InactiveUserError: If user is inactive
        """
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise UserNotFoundError()

        if not user.is_active:
            raise InactiveUserError()

        # Verify current password
        if not user.verify_password(current_password):
            raise InvalidCredentialsError("Current password is incorrect")

        # Update password
        user.set_password(new_password)
        db.commit()

        return True

    @staticmethod
    async def authenticate_with_google(email: str, name: str, google_id: str, db: Session) -> LoginResponse:
        """
        Authenticate user with Google OAuth.

        Creates new user if doesn't exist, or authenticates existing user.

        Args:
            email: User email from Google
            name: User name from Google
            google_id: Google user ID
            db: Database session

        Returns:
            LoginResponse with user data and tokens

        Raises:
            InactiveUserError: If user account is inactive
        """
        # Normalize email
        normalized_email = email.lower().strip()

        # Check if user exists
        user = db.query(User).filter(User.email == normalized_email).first()

        if not user:
            # Create new user with Google OAuth
            # Generate a random password since OAuth users don't need it
            random_password = secrets.token_urlsafe(32)

            user = User(
                email=normalized_email,
                name=name,
            )
            user.set_password(random_password)

            db.add(user)
            db.commit()
            db.refresh(user)

        # Check if user is active
        if not user.is_active:
            raise InactiveUserError()

        return AuthService._create_login_response(user)
