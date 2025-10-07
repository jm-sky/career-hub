"""Pydantic schemas for Experience model."""

from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, Field, validator


def to_camel(string: str) -> str:
    return "".join(word.capitalize() if i > 0 else word for i, word in enumerate(string.split("_")))


class ExperienceBase(BaseModel):
    """Base experience schema with common fields."""

    company_name: str = Field(alias="companyName", max_length=200, description="Company name")
    company_website: Optional[str] = Field(None, alias="companyWebsite", max_length=500, description="Company website")
    company_size: Optional[str] = Field(None, alias="companySize", max_length=50, description="Company size")
    industry: Optional[str] = Field(None, max_length=100, description="Industry")
    company_location: Optional[str] = Field(
        None, alias="companyLocation", max_length=100, description="Company location"
    )
    position: str = Field(max_length=200, description="Job position")
    employment_type: Optional[str] = Field(None, alias="employmentType", max_length=50, description="Employment type")
    start_date: date = Field(alias="startDate", description="Start date")
    end_date: Optional[date] = Field(None, alias="endDate", description="End date")
    is_current: bool = Field(False, alias="isCurrent", description="Is current position")
    description: Optional[str] = Field(None, description="Job description")
    responsibilities: List[str] = Field(default_factory=list, description="List of responsibilities")
    technologies: List[str] = Field(default_factory=list, description="Technologies used")
    display_order: int = Field(0, alias="displayOrder", description="Display order")

    @validator("employment_type")
    def validate_employment_type(cls, v):
        """Validate employment type."""
        if v is None:
            return v
        allowed = ["FULL_TIME", "PART_TIME", "CONTRACT", "FREELANCE", "INTERNSHIP", "TEMPORARY"]
        if v not in allowed:
            raise ValueError(f"Employment type must be one of: {allowed}")
        return v

    @validator("company_size")
    def validate_company_size(cls, v):
        """Validate company size."""
        if v is None:
            return v
        allowed = ["1-10", "11-50", "51-200", "201-500", "501-1000", "1001-5000", "5000+"]
        if v not in allowed:
            raise ValueError(f"Company size must be one of: {allowed}")
        return v

    @validator("end_date")
    def validate_end_date(cls, v, values):
        """Validate that end_date is after start_date."""
        if v is None:
            return v

        start_date = values.get("start_date")
        if start_date and v <= start_date:
            raise ValueError("End date must be after start date")

        return v

    @validator("is_current")
    def validate_current_position(cls, v, values):
        """Validate current position logic."""
        if v and values.get("end_date"):
            raise ValueError("Current position cannot have an end date")
        return v

    class Config:
        """Pydantic config."""

        populate_by_name = True
        alias_generator = to_camel


class ExperienceCreate(ExperienceBase):
    """Schema for creating an experience."""

    pass


class ExperienceUpdate(BaseModel):
    """Schema for updating an experience."""

    company_name: Optional[str] = Field(None, alias="companyName", max_length=200)
    company_website: Optional[str] = Field(None, alias="companyWebsite", max_length=500)
    company_size: Optional[str] = Field(None, alias="companySize", max_length=50)
    industry: Optional[str] = Field(None, max_length=100)
    company_location: Optional[str] = Field(None, alias="companyLocation", max_length=100)
    position: Optional[str] = Field(None, max_length=200)
    employment_type: Optional[str] = Field(None, alias="employmentType", max_length=50)
    start_date: Optional[date] = Field(None, alias="startDate")
    end_date: Optional[date] = Field(None, alias="endDate")
    is_current: Optional[bool] = Field(None, alias="isCurrent")
    description: Optional[str] = None
    responsibilities: Optional[List[str]] = None
    technologies: Optional[List[str]] = None
    display_order: Optional[int] = Field(None, alias="displayOrder")

    @validator("employment_type")
    def validate_employment_type(cls, v):
        """Validate employment type."""
        if v is None:
            return v
        allowed = ["FULL_TIME", "PART_TIME", "CONTRACT", "FREELANCE", "INTERNSHIP", "TEMPORARY"]
        if v not in allowed:
            raise ValueError(f"Employment type must be one of: {allowed}")
        return v

    @validator("company_size")
    def validate_company_size(cls, v):
        """Validate company size."""
        if v is None:
            return v
        allowed = ["1-10", "11-50", "51-200", "201-500", "501-1000", "1001-5000", "5000+"]
        if v not in allowed:
            raise ValueError(f"Company size must be one of: {allowed}")
        return v

    class Config:
        """Pydantic config."""

        populate_by_name = True
        alias_generator = to_camel


class ExperienceResponse(ExperienceBase):
    """Schema for experience responses."""

    id: str = Field(description="Experience ID")
    profile_id: str = Field(alias="profileId", description="Profile ID")
    duration_months: Optional[int] = Field(alias="durationMonths", description="Duration in months")
    duration_text: str = Field(alias="durationText", description="Human-readable duration")
    created_at: datetime = Field(alias="createdAt", description="Creation timestamp")
    updated_at: Optional[datetime] = Field(alias="updatedAt", description="Last update timestamp")

    class Config:
        """Pydantic config."""

        from_attributes = True
        populate_by_name = True
        alias_generator = to_camel


class ExperienceSummaryResponse(BaseModel):
    """Schema for experience summary (for lists)."""

    id: str = Field(description="Experience ID")
    company_name: str = Field(alias="companyName", description="Company name")
    position: str = Field(description="Job position")
    start_date: date = Field(alias="startDate", description="Start date")
    end_date: Optional[date] = Field(alias="endDate", description="End date")
    is_current: bool = Field(alias="isCurrent", description="Is current position")
    duration_text: str = Field(alias="durationText", description="Human-readable duration")
    technologies: List[str] = Field(description="Technologies used")

    class Config:
        """Pydantic config."""

        from_attributes = True
        populate_by_name = True
        alias_generator = to_camel


class ExperienceReorderRequest(BaseModel):
    """Schema for reordering experiences."""

    experience_ids: List[str] = Field(alias="experienceIds", description="Ordered list of experience IDs")

    class Config:
        """Pydantic config."""

        populate_by_name = True
