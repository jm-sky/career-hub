"""Authentication endpoints for user registration, login, and password management."""

import logging

from authlib.integrations.starlette_client import OAuthError  # type: ignore[import-untyped]
from fastapi import APIRouter, Request, status

from app.core.config import settings
from app.core.decorators import rate_limit, recaptcha_protected
from app.core.dependencies import BearerCredentials, CurrentActiveUser, DBSession
from app.core.exceptions import InvalidCredentialsError
from app.core.oauth import oauth
from app.schemas.auth import (
    LoginResponse,
    MessageResponse,
    TokenRefresh,
    TokenResponse,
    UserLogin,
    UserRegister,
    UserResponse,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    ChangePasswordRequest,
)
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["authentication"])
logger = logging.getLogger(__name__)


@router.post("/register", response_model=LoginResponse, status_code=status.HTTP_201_CREATED)
@rate_limit(settings.rate_limit.auth_register)
@recaptcha_protected("register")
async def register(
    request: Request,
    user_data: UserRegister,
    db: DBSession
) -> LoginResponse:
    """
    Register a new user.

    Creates a new user account with email and password, then returns
    authentication tokens for immediate login.

    Rate limit: 5 requests per minute per IP
    Requires: reCAPTCHA token (if enabled)
    """
    return await AuthService.register_user(
        email=user_data.email,
        password=user_data.password,
        name=user_data.name,
        db=db
    )


@router.post("/login", response_model=LoginResponse)
@rate_limit(settings.rate_limit.auth_login)
@recaptcha_protected("login")
async def login(
    request: Request,
    user_credentials: UserLogin,
    db: DBSession
) -> LoginResponse:
    """
    Authenticate user and return tokens.

    Validates email/password credentials and returns JWT access and refresh tokens.

    Rate limit: 10 requests per minute per IP
    Requires: reCAPTCHA token (if enabled)
    """
    return await AuthService.authenticate_user(
        email=user_credentials.email,
        password=user_credentials.password,
        db=db
    )


@router.post("/refresh", response_model=TokenResponse)
@rate_limit(settings.rate_limit.auth_refresh)
async def refresh_token(
    request: Request,
    token_data: TokenRefresh,
    db: DBSession
) -> TokenResponse:
    """
    Refresh access token using refresh token.

    Validates the refresh token and issues a new pair of access and refresh tokens.
    This implements token rotation for enhanced security.

    Rate limit: 20 requests per minute per IP
    """
    return await AuthService.refresh_tokens(token_data.refreshToken, db)


@router.post("/logout", response_model=MessageResponse)
async def logout(
    credentials: BearerCredentials,
    current_user: CurrentActiveUser
) -> MessageResponse:
    """
    Logout user and blacklist their access token.

    Adds the current access token to the blacklist, preventing further use.
    The user will need to log in again to get new tokens.
    """
    await AuthService.logout_user(credentials.credentials, current_user)
    return MessageResponse(message="Successfully logged out")


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: CurrentActiveUser) -> UserResponse:
    """
    Get current user information.

    Returns the profile information for the authenticated user.

    Requires: Valid access token in Authorization header
    """
    return await AuthService.get_user_profile(current_user)


@router.post("/forgot-password", response_model=MessageResponse)
@rate_limit(settings.rate_limit.auth_register)
@recaptcha_protected("forgot_password")
async def forgot_password(
    request: Request,
    forgot_request: ForgotPasswordRequest,
    db: DBSession
) -> MessageResponse:
    """
    Request password reset token.

    Generates a password reset token and stores it in the database.
    In production, this would also send an email with the reset link.

    For security, always returns success even if the email doesn't exist.

    Rate limit: 5 requests per minute per IP
    Requires: reCAPTCHA token (if enabled)
    """
    # Generate reset token (always return success for security - don't reveal if email exists)
    token = await AuthService.request_password_reset(forgot_request.email, db)

    if token:
        # In production, send email with reset link containing the token
        # TODO: Send email with reset link
        # await send_password_reset_email(forgot_request.email, token)

        # For development only - log the reset link
        if settings.app.environment == "development":
            reset_link = f"{settings.frontend_url}/reset-password/{token}"
            logger.info(f"Password reset link for {forgot_request.email}: {reset_link}")

    # Always return success message for security (don't reveal if email exists)
    return MessageResponse(message="If the email exists, a password reset link has been sent")


@router.post("/reset-password", response_model=MessageResponse)
@rate_limit(settings.rate_limit.auth_register)
async def reset_password(
    request: Request,
    reset_request: ResetPasswordRequest,
    db: DBSession
) -> MessageResponse:
    """
    Reset password using token.

    Validates the password reset token and updates the user's password.
    The reset token is valid for 1 hour and can only be used once.

    Rate limit: 5 requests per minute per IP
    """
    await AuthService.reset_password(reset_request.token, reset_request.newPassword, db)
    return MessageResponse(message="Password has been successfully reset")


@router.post("/change-password", response_model=MessageResponse)
@rate_limit(settings.rate_limit.auth_password_change)
async def change_password(
    request: Request,
    change_request: ChangePasswordRequest,
    current_user: CurrentActiveUser,
    db: DBSession
) -> MessageResponse:
    """
    Change password for authenticated user.

    Verifies the current password and updates it to the new password.
    Requires the user to be authenticated with a valid access token.

    Rate limit: 3 requests per minute per IP
    Requires: Valid access token in Authorization header
    """
    await AuthService.change_password(
        user_id=str(current_user.id),
        current_password=change_request.currentPassword,
        new_password=change_request.newPassword,
        db=db
    )

    # TODO: Invalidate all user tokens after password change
    # This requires implementing a token blacklist system:
    # 1. Create a token blacklist store (Redis or database)
    # 2. Add all current user tokens to blacklist
    # 3. Update get_current_user dependency to check blacklist
    # For now, users should log out and log back in after password change

    return MessageResponse(message="Password has been successfully changed")


# ============================================================================
# OAuth Google Authentication
# ============================================================================


@router.get("/google/login")
async def google_login(request: Request):
    """
    Initiate Google OAuth login flow.

    Redirects the user to Google's OAuth consent screen.
    After authentication, Google will redirect back to the callback endpoint.
    """
    # Build redirect URI dynamically from request
    redirect_uri = str(request.url_for('google_callback'))
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/google/callback")
async def google_callback(request: Request, db: DBSession) -> LoginResponse:
    """
    Handle Google OAuth callback and authenticate user.

    This endpoint receives the OAuth callback from Google after the user
    authenticates. It exchanges the authorization code for user information
    and creates or authenticates the user in our system.

    If the user doesn't exist, a new account is created automatically.
    """
    try:
        # Exchange authorization code for access token
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        # OAuth failed - redirect to login with error
        raise InvalidCredentialsError(f"Google authentication failed: {error.error}")

    # Extract user info from token
    user_info = token.get('userinfo')
    if not user_info:
        raise InvalidCredentialsError("Failed to get user information from Google")

    email = user_info.get('email')
    name = user_info.get('name', '')
    google_id = user_info.get('sub')  # Google user ID

    if not email or not google_id:
        raise InvalidCredentialsError("Incomplete user information from Google")

    return await AuthService.authenticate_with_google(email, name, google_id, db)
