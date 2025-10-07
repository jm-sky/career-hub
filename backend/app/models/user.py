"""User model for authentication and profile management."""

import secrets
from datetime import datetime
from typing import Any, Dict, TYPE_CHECKING

from sqlalchemy import Boolean, Column, DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from ulid import ULID

from app.core.database import Base
from app.core.security import verify_password, get_password_hash, verify_token

if TYPE_CHECKING:
    pass


class User(Base):
    """User model with authentication and profile fields."""

    __tablename__ = "users"

    # Primary fields
    id = Column(String(26), primary_key=True, default=lambda: str(ULID()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False, index=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Password reset fields
    reset_token = Column(Text, nullable=True)
    reset_token_expiry = Column(DateTime(timezone=True), nullable=True)

    # Business model: CareerHub tiers
    tier = Column(String(20), default="free", nullable=False)  # free, pro, expert

    # User settings (JSONB for flexibility)
    settings = Column(JSONB, default={}, nullable=False, server_default="{}")

    def verify_password(self, password: str) -> bool:
        """Verify password against stored hash."""
        return verify_password(password, str(self.hashed_password))

    def set_password(self, password: str) -> None:
        """Set new password hash."""
        self.hashed_password = get_password_hash(password)  # type: ignore[assignment]

    def set_reset_token(self, token: str, expiry: datetime) -> None:
        """Set password reset token and expiry."""
        self.reset_token = token  # type: ignore[assignment]
        self.reset_token_expiry = expiry  # type: ignore[assignment]

    def clear_reset_token(self) -> None:
        """Clear password reset token."""
        self.reset_token = None  # type: ignore[assignment]
        self.reset_token_expiry = None  # type: ignore[assignment]

    def is_reset_token_valid(self, token: str) -> bool:
        """Check if reset token is valid and not expired using secure comparison."""
        if not self.reset_token:
            return False

        try:
            # Verify JWT token
            payload = verify_token(token)

            # Check token type
            if payload.get("type") != "password_reset":
                return False

            # Check if it matches stored token using secure comparison
            if not secrets.compare_digest(str(self.reset_token), token):
                return False

            # Check user ID matches
            if payload.get("sub") != str(self.id):
                return False

            return True
        except Exception:
            return False

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to camelCase dict for API responses.

        Returns a sanitized dictionary suitable for public API responses.
        Excludes sensitive fields like hashed_password and reset tokens.
        """
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "isActive": self.is_active,
            "createdAt": self.created_at,
            "tier": self.tier,
        }

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"<User(id={self.id}, email={self.email}, tier={self.tier})>"
