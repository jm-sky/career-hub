"""Pydantic schemas for Profile model."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, validator


class ProfileBase(BaseModel):
    """Base profile schema with common fields."""
    
    headline: Optional[str] = Field(None, max_length=200, description="Professional headline")
    summary: Optional[str] = Field(None, description="Professional summary")
    location: Optional[str] = Field(None, max_length=100, description="Location")
    visibility: str = Field("PRIVATE", description="Profile visibility")
    contact: Dict[str, Any] = Field(default_factory=dict, description="Contact information")
    profile_photo_url: Optional[str] = Field(None, alias="profilePhotoUrl", description="Profile photo URL")

    @validator("visibility")
    def validate_visibility(cls, v):
        """Validate visibility value."""
        allowed = ["PRIVATE", "FRIENDS", "PUBLIC"]
        if v not in allowed:
            raise ValueError(f"Visibility must be one of: {allowed}")
        return v

    class Config:
        """Pydantic config."""
        populate_by_name = True
        alias_generator = lambda field_name: ''.join(
            word.capitalize() if i > 0 else word 
            for i, word in enumerate(field_name.split('_'))
        )


class ProfileCreate(ProfileBase):
    """Schema for creating a profile."""
    
    slug: Optional[str] = Field(None, max_length=100, description="URL slug")
    draft_data: Optional[Dict[str, Any]] = Field(None, alias="draftData", description="Draft wizard data")

    @validator("slug")
    def validate_slug(cls, v):
        """Validate slug format."""
        if v is None:
            return v
        
        import re
        if not re.match(r'^[a-z0-9-]+$', v):
            raise ValueError("Slug must contain only lowercase letters, numbers, and hyphens")
        
        if len(v) < 3:
            raise ValueError("Slug must be at least 3 characters long")
            
        return v


class ProfileUpdate(BaseModel):
    """Schema for updating a profile."""
    
    headline: Optional[str] = Field(None, max_length=200)
    summary: Optional[str] = None
    location: Optional[str] = Field(None, max_length=100)
    visibility: Optional[str] = None
    contact: Optional[Dict[str, Any]] = None
    profile_photo_url: Optional[str] = Field(None, alias="profilePhotoUrl")
    draft_data: Optional[Dict[str, Any]] = Field(None, alias="draftData")

    @validator("visibility")
    def validate_visibility(cls, v):
        """Validate visibility value."""
        if v is None:
            return v
        allowed = ["PRIVATE", "FRIENDS", "PUBLIC"]
        if v not in allowed:
            raise ValueError(f"Visibility must be one of: {allowed}")
        return v

    class Config:
        """Pydantic config."""
        populate_by_name = True
        alias_generator = lambda field_name: ''.join(
            word.capitalize() if i > 0 else word 
            for i, word in enumerate(field_name.split('_'))
        )


class ProfileResponse(ProfileBase):
    """Schema for profile responses."""
    
    id: str = Field(description="Profile ID")
    user_id: str = Field(alias="userId", description="User ID")
    slug: Optional[str] = Field(description="URL slug")
    completeness_score: int = Field(alias="completenessScore", description="Profile completeness (0-100)")
    created_at: datetime = Field(alias="createdAt", description="Creation timestamp")
    updated_at: Optional[datetime] = Field(alias="updatedAt", description="Last update timestamp")

    class Config:
        """Pydantic config."""
        from_attributes = True
        populate_by_name = True
        alias_generator = lambda field_name: ''.join(
            word.capitalize() if i > 0 else word 
            for i, word in enumerate(field_name.split('_'))
        )


class ProfilePublicResponse(BaseModel):
    """Schema for public profile responses (limited fields)."""
    
    id: str = Field(description="Profile ID")
    slug: Optional[str] = Field(description="URL slug")
    headline: Optional[str] = Field(description="Professional headline")
    summary: Optional[str] = Field(description="Professional summary")
    location: Optional[str] = Field(description="Location")
    profile_photo_url: Optional[str] = Field(alias="profilePhotoUrl", description="Profile photo URL")
    created_at: datetime = Field(alias="createdAt", description="Creation timestamp")

    class Config:
        """Pydantic config."""
        from_attributes = True
        populate_by_name = True
        alias_generator = lambda field_name: ''.join(
            word.capitalize() if i > 0 else word 
            for i, word in enumerate(field_name.split('_'))
        )


class ProfileSummaryResponse(BaseModel):
    """Schema for profile summary (for lists)."""
    
    id: str = Field(description="Profile ID")
    headline: Optional[str] = Field(description="Professional headline")
    location: Optional[str] = Field(description="Location")
    completeness_score: int = Field(alias="completenessScore", description="Profile completeness (0-100)")
    visibility: str = Field(description="Profile visibility")

    class Config:
        """Pydantic config."""
        from_attributes = True
        populate_by_name = True
