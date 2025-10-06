"""Security utilities for authentication, password hashing, and JWT tokens."""

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

import jwt
import redis
from passlib.context import CryptContext

from app.core.config import settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.security.access_token_expires_minutes)

    to_encode.update({
        "exp": expire,
        "type": "access",
        "iat": datetime.now(timezone.utc)
    })
    encoded_jwt = jwt.encode(to_encode, settings.security.secret_key, algorithm=settings.security.jwt_algorithm)
    return encoded_jwt


def create_refresh_token(data: Dict[str, Any]) -> str:
    """Create a JWT refresh token with longer expiration."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=settings.security.refresh_token_expires_days)
    to_encode.update({
        "exp": expire,
        "type": "refresh",
        "iat": datetime.now(timezone.utc)
    })
    encoded_jwt = jwt.encode(to_encode, settings.security.secret_key, algorithm=settings.security.jwt_algorithm)
    return encoded_jwt


def create_password_reset_token(data: Dict[str, Any]) -> str:
    """Create a JWT password reset token with 1-hour expiration."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(hours=1)
    to_encode.update({
        "exp": expire,
        "type": "password_reset",
        "iat": datetime.now(timezone.utc)
    })
    encoded_jwt = jwt.encode(to_encode, settings.security.secret_key, algorithm=settings.security.jwt_algorithm)
    return encoded_jwt


def verify_token(token: str) -> Dict[str, Any]:
    """Verify and decode a JWT token."""
    from app.core.exceptions import InvalidTokenError, ExpiredTokenError

    # Check if token is blacklisted first
    if token_blacklist.is_blacklisted(token):
        raise InvalidTokenError("Token has been revoked")

    try:
        payload = jwt.decode(token, settings.security.secret_key, algorithms=[settings.security.jwt_algorithm])
        return payload
    except jwt.ExpiredSignatureError:
        raise ExpiredTokenError()
    except jwt.InvalidTokenError:
        raise InvalidTokenError()


# ============================================================================
# Redis Token Blacklist
# ============================================================================

class RedisTokenBlacklist:
    """Redis-based token blacklist with automatic expiration."""

    def __init__(self) -> None:
        self._redis: Optional[redis.Redis] = None

    def _get_redis(self) -> redis.Redis:
        """Get or create Redis connection."""
        if self._redis is None:
            self._redis = redis.from_url(
                settings.redis.url,
                decode_responses=True,
                socket_connect_timeout=5
            )
        return self._redis

    def add(self, token: str) -> None:
        """Add a token to the blacklist with automatic expiration."""
        try:
            r = self._get_redis()

            # Decode token to get expiration time (without verification)
            try:
                payload = jwt.decode(
                    token,
                    settings.security.secret_key,
                    algorithms=[settings.security.jwt_algorithm],
                    options={"verify_signature": False, "verify_exp": False}
                )
                exp_timestamp = payload.get("exp", 0)
                current_timestamp = datetime.now(timezone.utc).timestamp()

                # Calculate TTL (time until token expires)
                ttl = int(exp_timestamp - current_timestamp)

                # Only blacklist if token hasn't expired yet
                if ttl > 0:
                    r.setex(f"blacklist:{token}", ttl, "1")

            except Exception:
                # If we can't decode the token, blacklist it for 24 hours
                r.setex(f"blacklist:{token}", 86400, "1")

        except redis.RedisError:
            # If Redis is down, log error but don't crash
            # In production, you'd want proper logging here
            pass

    def is_blacklisted(self, token: str) -> bool:
        """Check if a token is blacklisted."""
        try:
            r = self._get_redis()
            return r.exists(f"blacklist:{token}") > 0
        except redis.RedisError:
            # If Redis is down, assume token is not blacklisted (fail open)
            # In production, you might want to fail closed for security
            return False

    def remove(self, token: str) -> None:
        """Remove a token from the blacklist (for testing/admin)."""
        try:
            r = self._get_redis()
            r.delete(f"blacklist:{token}")
        except redis.RedisError:
            pass

    def clear(self) -> None:
        """Clear all blacklisted tokens (for testing)."""
        try:
            r = self._get_redis()
            # Delete all keys matching blacklist:*
            keys = r.keys("blacklist:*")
            if keys:
                r.delete(*keys)
        except redis.RedisError:
            pass


# Global blacklist instance
token_blacklist = RedisTokenBlacklist()
