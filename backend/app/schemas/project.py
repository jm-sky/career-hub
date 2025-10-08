"""Project schemas."""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

from app.models.project import ProjectStatus, ProjectCategory, ProjectScale


class ProjectBase(BaseModel):
    """Base project schema."""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    status: ProjectStatus = ProjectStatus.ACTIVE
    category: ProjectCategory = ProjectCategory.PRODUCTION
    scale: ProjectScale = ProjectScale.MEDIUM
    start_date: Optional[str] = Field(None, pattern=r'^\d{4}-\d{2}$')
    end_date: Optional[str] = Field(None, pattern=r'^\d{4}-\d{2}$')
    client: Optional[str] = Field(None, max_length=200)
    technologies: List[str] = Field(default_factory=list)
    achievements: List[str] = Field(default_factory=list)
    challenges: List[str] = Field(default_factory=list)


class ProjectCreate(ProjectBase):
    """Schema for creating a project."""
    pass


class ProjectUpdate(BaseModel):
    """Schema for updating a project."""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    status: Optional[ProjectStatus] = None
    category: Optional[ProjectCategory] = None
    scale: Optional[ProjectScale] = None
    start_date: Optional[str] = Field(None, pattern=r'^\d{4}-\d{2}$')
    end_date: Optional[str] = Field(None, pattern=r'^\d{4}-\d{2}$')
    client: Optional[str] = Field(None, max_length=200)
    technologies: Optional[List[str]] = None
    achievements: Optional[List[str]] = None
    challenges: Optional[List[str]] = None


class ProjectResponse(BaseModel):
    """Schema for project response."""
    id: str
    profileId: str
    name: str
    description: Optional[str] = None
    status: str
    category: str
    scale: str
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    client: Optional[str] = None
    technologies: List[str] = Field(default_factory=list)
    achievements: List[str] = Field(default_factory=list)
    challenges: List[str] = Field(default_factory=list)
    displayOrder: int
    createdAt: datetime
    updatedAt: Optional[datetime] = None

    class Config:
        from_attributes = True
        populate_by_name = True


class ProjectReorderRequest(BaseModel):
    """Schema for reordering projects."""
    project_ids: List[str] = Field(..., min_length=1)
