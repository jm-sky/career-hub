# backend/app/models/__init__.py

from app.models.user import User
from app.models.profile import Profile
from app.models.experience import Experience
from app.models.project import Project, ProjectExperience, ProjectSkill
from app.models.skill import Skill
from app.models.education import Education
from app.models.certification import Certification
from app.models.achievement import Achievement
from app.models.cv import CVVersion

__all__ = [
    "User",
    "Profile", 
    "Experience",
    "Project",
    "ProjectExperience",
    "ProjectSkill",
    "Skill",
    "Education",
    "Certification",
    "Achievement",
    "CVVersion"
]


# backend/app/models/user.py

from sqlalchemy import Column, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.core.database import Base
from app.core.security import generate_ulid


class UserPlan(str, enum.Enum):
    FREE = "FREE"
    PRO = "PRO"
    EXPERT = "EXPERT"


class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=generate_ulid)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String, nullable=True)
    reset_token = Column(String, nullable=True)
    reset_token_expires = Column(DateTime, nullable=True)
    plan = Column(Enum(UserPlan), default=UserPlan.FREE)
    plan_expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login_at = Column(DateTime, nullable=True)
    
    # Relationships
    profile = relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan")


# backend/app/models/profile.py

from sqlalchemy import Column, String, Integer, Text, JSON, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.core.database import Base
from app.core.security import generate_ulid


class ProfileVisibility(str, enum.Enum):
    PRIVATE = "PRIVATE"
    FRIENDS = "FRIENDS"
    PUBLIC = "PUBLIC"


class Profile(Base):
    __tablename__ = "profiles"
    
    id = Column(String, primary_key=True, default=generate_ulid)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    slug = Column(String(100), unique=True, nullable=True, index=True)
    headline = Column(String(200), nullable=True)
    summary = Column(Text, nullable=True)
    location = Column(String(100), nullable=True)
    visibility = Column(Enum(ProfileVisibility), default=ProfileVisibility.PRIVATE)
    contact = Column(JSON, default=dict)  # {email, phone, linkedin, website}
    draft_data = Column(JSON, nullable=True)  # Wizard progress
    profile_photo_url = Column(String, nullable=True)
    completeness_score = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="profile")
    experiences = relationship("Experience", back_populates="profile", cascade="all, delete-orphan", order_by="Experience.display_order")
    projects = relationship("Project", back_populates="profile", cascade="all, delete-orphan")
    skills = relationship("Skill", back_populates="profile", cascade="all, delete-orphan")
    education = relationship("Education", back_populates="profile", cascade="all, delete-orphan")
    certifications = relationship("Certification", back_populates="profile", cascade="all, delete-orphan")
    achievements = relationship("Achievement", back_populates="profile", cascade="all, delete-orphan")
    cv_versions = relationship("CVVersion", back_populates="profile", cascade="all, delete-orphan")


# backend/app/models/experience.py

from sqlalchemy import Column, String, Integer, Text, JSON, ForeignKey, Date, Boolean, ARRAY
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base
from app.core.security import generate_ulid


class Experience(Base):
    __tablename__ = "experiences"
    
    id = Column(String, primary_key=True, default=generate_ulid)
    profile_id = Column(String, ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    company_name = Column(String(200), nullable=False)
    company_website = Column(String(500), nullable=True)
    company_size = Column(String(50), nullable=True)  # "1-10", "11-50", etc.
    industry = Column(String(100), nullable=True)
    company_location = Column(String(100), nullable=True)
    position = Column(String(200), nullable=False)
    employment_type = Column(String(50), nullable=True)  # FULL_TIME, PART_TIME, CONTRACT
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    is_current = Column(Boolean, default=False)
    description = Column(Text, nullable=True)
    responsibilities = Column(JSON, default=list)  # Array of strings
    technologies = Column(ARRAY(String), default=list)  # PostgreSQL array
    display_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    profile = relationship("Profile", back_populates="experiences")
    project_links = relationship("ProjectExperience", back_populates="experience", cascade="all, delete-orphan")


# backend/app/models/project.py

from sqlalchemy import Column, String, Text, ForeignKey, Date, Boolean, ARRAY, Enum, Table
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.core.database import Base
from app.core.security import generate_ulid


class ProjectVisibility(str, enum.Enum):
    PUBLIC = "PUBLIC"
    ANONYMOUS = "ANONYMOUS"


# Junction table for Project-Experience many-to-many
class ProjectExperience(Base):
    __tablename__ = "project_experiences"
    
    project_id = Column(String, ForeignKey("projects.id", ondelete="CASCADE"), primary_key=True)
    experience_id = Column(String, ForeignKey("experiences.id", ondelete="CASCADE"), primary_key=True)
    
    # Relationships
    project = relationship("Project", back_populates="experience_links")
    experience = relationship("Experience", back_populates="project_links")


# Junction table for Project-Skill many-to-many
class ProjectSkill(Base):
    __tablename__ = "project_skills"
    
    project_id = Column(String, ForeignKey("projects.id", ondelete="CASCADE"), primary_key=True)
    skill_id = Column(String, ForeignKey("skills.id", ondelete="CASCADE"), primary_key=True)
    
    # Relationships
    project = relationship("Project", back_populates="skill_links")
    skill = relationship("Skill", back_populates="project_links")


class Project(Base):
    __tablename__ = "projects"
    
    id = Column(String, primary_key=True, default=generate_ulid)
    profile_id = Column(String, ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    role = Column(String(100), nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    is_ongoing = Column(Boolean, default=False)
    is_anonymized = Column(Boolean, default=False)
    anonymized_company = Column(String(200), nullable=True)
    project_url = Column(String(500), nullable=True)
    visibility = Column(Enum(ProjectVisibility), default=ProjectVisibility.PUBLIC)
    technologies = Column(ARRAY(String), default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    profile = relationship("Profile", back_populates="projects")
    experience_links = relationship("ProjectExperience", back_populates="project", cascade="all, delete-orphan")
    skill_links = relationship("ProjectSkill", back_populates="project", cascade="all, delete-orphan")


# backend/app/models/skill.py

from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.core.database import Base
from app.core.security import generate_ulid


class SkillCategory(str, enum.Enum):
    TECHNICAL = "TECHNICAL"
    TOOLS = "TOOLS"
    SOFT = "SOFT"


class Skill(Base):
    __tablename__ = "skills"
    
    id = Column(String, primary_key=True, default=generate_ulid)
    profile_id = Column(String, ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    category = Column(Enum(SkillCategory), default=SkillCategory.TECHNICAL)
    level = Column(Integer, nullable=True)  # 1-5
    years_of_experience = Column(Integer, nullable=True)
    is_primary = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    profile = relationship("Profile", back_populates="skills")
    project_links = relationship("ProjectSkill", back_populates="skill", cascade="all, delete-orphan")
    
    # Unique constraint
    __table_args__ = (
        UniqueConstraint('profile_id', 'name', name='unique_profile_skill'),
    )