"""Project model."""

from datetime import datetime
from enum import Enum
from typing import List, Optional

from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Enum as SQLEnum, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from ulid import ULID

from app.core.database import Base


class ProjectStatus(str, Enum):
    """Project status enum."""
    ACTIVE = "ACTIVE"
    STAGING = "STAGING"
    ARCHIVED = "ARCHIVED"


class ProjectCategory(str, Enum):
    """Project category enum."""
    DEMO = "DEMO"
    INTERNAL = "INTERNAL"
    PRODUCTION = "PRODUCTION"


class ProjectScale(str, Enum):
    """Project scale enum."""
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"
    ENTERPRISE = "ENTERPRISE"


class Project(Base):
    """Project model."""

    __tablename__ = "projects"

    id = Column(String(26), primary_key=True, default=lambda: str(ULID()))
    profile_id = Column(String, ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Basic info
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(SQLEnum(ProjectStatus), default=ProjectStatus.ACTIVE, nullable=False)
    category = Column(SQLEnum(ProjectCategory), default=ProjectCategory.PRODUCTION, nullable=False)
    scale = Column(SQLEnum(ProjectScale), default=ProjectScale.MEDIUM, nullable=False)
    
    # Dates
    start_date = Column(String(7), nullable=True)  # YYYY-MM format
    end_date = Column(String(7), nullable=True)  # YYYY-MM format
    
    # Details
    client = Column(String(200), nullable=True)
    technologies = Column(ARRAY(String), default=list, nullable=False)
    achievements = Column(ARRAY(String), default=list, nullable=False)
    challenges = Column(ARRAY(String), default=list, nullable=False)
    
    # Metadata
    display_order = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    profile = relationship("Profile", back_populates="projects")

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "profileId": self.profile_id,
            "name": self.name,
            "description": self.description,
            "status": self.status.value if self.status else None,
            "category": self.category.value if self.category else None,
            "scale": self.scale.value if self.scale else None,
            "startDate": self.start_date,
            "endDate": self.end_date,
            "client": self.client,
            "technologies": self.technologies or [],
            "achievements": self.achievements or [],
            "challenges": self.challenges or [],
            "displayOrder": self.display_order,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
            "updatedAt": self.updated_at.isoformat() if self.updated_at else None,
        }
