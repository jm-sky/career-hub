"""Experience model for work history."""

from datetime import date
from typing import Any, Dict, Optional, TYPE_CHECKING

from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import relationship
from ulid import ULID

from app.core.database import Base

if TYPE_CHECKING:
    pass


class Experience(Base):
    """Experience model for work history entries."""

    __tablename__ = "experiences"

    # Primary fields
    id = Column(String(26), primary_key=True, default=lambda: str(ULID()))
    profile_id = Column(String(26), ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)

    # Company information
    company_name = Column(String(200), nullable=False)
    company_website = Column(String(500), nullable=True)
    company_size = Column(String(50), nullable=True)  # "1-10", "11-50", "51-200", etc.
    industry = Column(String(100), nullable=True)
    company_location = Column(String(100), nullable=True)

    # Position information
    position = Column(String(200), nullable=False)
    employment_type = Column(String(50), nullable=True)  # "FULL_TIME", "PART_TIME", "CONTRACT", etc.

    # Dates
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    is_current = Column(Boolean, default=False, nullable=False)

    # Job description and responsibilities
    description = Column(Text, nullable=True)
    # Array of responsibility strings
    responsibilities = Column(JSONB, default=[], nullable=False, server_default="[]")

    # Technologies used (will be replaced with relationships later)
    technologies: list[str] = Column(ARRAY(Text), default=[], nullable=False, server_default="{}") # type: ignore

    # Display order for sorting
    display_order = Column(Integer, default=0, nullable=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    profile = relationship("Profile", back_populates="experiences")
    # project_experiences = relationship("ProjectExperience", back_populates="experience")

    @property
    def duration_months(self) -> Optional[int]:
        """Calculate duration in months."""
        if not self.start_date:
            return None

        end = self.end_date or date.today()

        # Calculate months between dates
        months = (end.year - self.start_date.year) * 12 + (end.month - self.start_date.month)

        # Add 1 to include the current month
        return max(months + 1, 1)

    @property
    def duration_text(self) -> str:
        """Get human-readable duration text."""
        months = self.duration_months
        if not months:
            return "Unknown duration"

        if months < 12:
            return f"{months} {'month' if months == 1 else 'months'}"

        years = months // 12
        remaining_months = months % 12

        if remaining_months == 0:
            return f"{years} {'year' if years == 1 else 'years'}"

        return f"{years} {'year' if years == 1 else 'years'} {remaining_months} {'month' if remaining_months == 1 else 'months'}"

    def add_responsibility(self, responsibility: str) -> None:
        """Add a responsibility to the list."""
        if not self.responsibilities:
            self.responsibilities = []  # type: ignore

        if responsibility.strip() and responsibility not in self.responsibilities:
            self.responsibilities = self.responsibilities + [responsibility.strip()]  # type: ignore

    def remove_responsibility(self, responsibility: str) -> None:
        """Remove a responsibility from the list."""
        if self.responsibilities and responsibility in self.responsibilities:
            self.responsibilities = [r for r in self.responsibilities if r != responsibility]  # type: ignore

    def add_technology(self, technology: str) -> None:
        """Add a technology to the list."""
        if not self.technologies:
            self.technologies = []  # type: ignore

        if technology.strip() and technology not in self.technologies:
            self.technologies = self.technologies + [technology.strip()]  # type: ignore

    def remove_technology(self, technology: str) -> None:
        """Remove a technology from the list."""
        if self.technologies and technology in self.technologies:
            self.technologies = [t for t in self.technologies if t != technology]  # type: ignore

    def is_date_valid(self) -> bool:
        """Validate that end_date is after start_date."""
        if not self.end_date:
            return True
        return self.end_date > self.start_date  # type: ignore[return-value]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to camelCase dict for API responses."""
        return {
            "id": self.id,
            "profileId": self.profile_id,
            "companyName": self.company_name,
            "companyWebsite": self.company_website,
            "companySize": self.company_size,
            "industry": self.industry,
            "companyLocation": self.company_location,
            "position": self.position,
            "employmentType": self.employment_type,
            "startDate": self.start_date.isoformat() if self.start_date else None,
            "endDate": self.end_date.isoformat() if self.end_date else None,
            "isCurrent": self.is_current,
            "description": self.description,
            "responsibilities": self.responsibilities or [],
            "technologies": self.technologies or [],
            "displayOrder": self.display_order,
            "durationMonths": self.duration_months,
            "durationText": self.duration_text,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
        }

    def to_summary_dict(self) -> Dict[str, Any]:
        """Convert to summary dict for lists (less detailed)."""
        return {
            "id": self.id,
            "companyName": self.company_name,
            "position": self.position,
            "startDate": self.start_date.isoformat() if self.start_date else None,
            "endDate": self.end_date.isoformat() if self.end_date else None,
            "isCurrent": self.is_current,
            "durationText": self.duration_text,
            "technologies": self.technologies or [],
        }

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"<Experience(id={self.id}, company={self.company_name}, position={self.position})>"
