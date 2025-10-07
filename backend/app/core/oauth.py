"""OAuth configuration for third-party authentication providers."""

from authlib.integrations.starlette_client import OAuth  # type: ignore[import-untyped]

from app.core.config import settings

# Create OAuth registry
oauth = OAuth()

# Register Google OAuth provider
oauth.register(
    name="google",
    client_id=settings.google_oauth.client_id,
    client_secret=settings.google_oauth.client_secret,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)
