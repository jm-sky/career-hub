"""Experience service for managing work experiences."""

from typing import List, Optional

from sqlalchemy.orm import Session

from app.core.exceptions import AuthenticationError
from app.models.experience import Experience
from app.models.profile import Profile
from app.schemas.experience import ExperienceCreate, ExperienceUpdate


class ExperienceNotFoundError(Exception):
    """Raised when experience is not found."""
    pass


class ExperienceService:
    """Service for managing work experiences."""

    def __init__(self, db: Session):
        """Initialize experience service."""
        self.db = db

    def create_experience(self, profile_id: str, user_id: str, experience_data: ExperienceCreate) -> Experience:
        """
        Create a new experience for a profile.
        
        Args:
            profile_id: Profile ID
            user_id: User ID (for authorization)
            experience_data: Experience creation data
            
        Returns:
            Created experience
            
        Raises:
            AuthenticationError: If user doesn't own the profile
        """
        # Check if profile exists and user owns it
        profile = self.db.query(Profile).filter(Profile.id == profile_id).first()
        if not profile:
            raise AuthenticationError("Profile not found")
        
        if profile.user_id != user_id:
            raise AuthenticationError("You don't have permission to add experiences to this profile")

        # Set display order (highest + 1)
        max_order = (
            self.db.query(Experience.display_order)
            .filter(Experience.profile_id == profile_id)
            .order_by(Experience.display_order.desc())
            .first()
        )
        display_order = (max_order[0] + 1) if max_order else 0

        # Create experience
        experience = Experience(
            profile_id=profile_id,
            company_name=experience_data.company_name,
            company_website=experience_data.company_website,
            company_size=experience_data.company_size,
            industry=experience_data.industry,
            company_location=experience_data.company_location,
            position=experience_data.position,
            employment_type=experience_data.employment_type,
            start_date=experience_data.start_date,
            end_date=experience_data.end_date,
            is_current=experience_data.is_current,
            description=experience_data.description,
            responsibilities=experience_data.responsibilities,
            technologies=experience_data.technologies,
            display_order=experience_data.display_order or display_order,
        )

        self.db.add(experience)
        self.db.commit()
        self.db.refresh(experience)

        # Update profile completeness
        profile.update_completeness()
        self.db.commit()

        return experience

    def get_experience_by_id(self, experience_id: str) -> Optional[Experience]:
        """
        Get experience by ID.
        
        Args:
            experience_id: Experience ID
            
        Returns:
            Experience or None if not found
        """
        return self.db.query(Experience).filter(Experience.id == experience_id).first()

    def get_experiences_by_profile(self, profile_id: str, user_id: Optional[str] = None) -> List[Experience]:
        """
        Get all experiences for a profile.
        
        Args:
            profile_id: Profile ID
            user_id: User ID (for authorization check)
            
        Returns:
            List of experiences ordered by display_order
            
        Raises:
            AuthenticationError: If profile is private and user doesn't own it
        """
        # Check if profile exists and is accessible
        profile = self.db.query(Profile).filter(Profile.id == profile_id).first()
        if not profile:
            return []

        # Check access permissions
        if not profile.can_view(user_id):
            raise AuthenticationError("You don't have permission to view this profile")

        return (
            self.db.query(Experience)
            .filter(Experience.profile_id == profile_id)
            .order_by(Experience.display_order.desc(), Experience.start_date.desc())
            .all()
        )

    def update_experience(self, experience_id: str, user_id: str, experience_data: ExperienceUpdate) -> Experience:
        """
        Update an experience.
        
        Args:
            experience_id: Experience ID
            user_id: User ID (for authorization)
            experience_data: Experience update data
            
        Returns:
            Updated experience
            
        Raises:
            ExperienceNotFoundError: If experience not found
            AuthenticationError: If user doesn't own the experience
        """
        experience = self.db.query(Experience).filter(Experience.id == experience_id).first()
        if not experience:
            raise ExperienceNotFoundError("Experience not found")

        # Check ownership through profile
        profile = self.db.query(Profile).filter(Profile.id == experience.profile_id).first()
        if not profile or profile.user_id != user_id:
            raise AuthenticationError("You don't have permission to update this experience")

        # Update fields
        update_data = experience_data.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            if hasattr(experience, field):
                setattr(experience, field, value)

        self.db.commit()
        self.db.refresh(experience)

        # Update profile completeness
        profile.update_completeness()
        self.db.commit()

        return experience

    def delete_experience(self, experience_id: str, user_id: str) -> bool:
        """
        Delete an experience.
        
        Args:
            experience_id: Experience ID
            user_id: User ID (for authorization)
            
        Returns:
            True if deleted, False if not found
            
        Raises:
            AuthenticationError: If user doesn't own the experience
        """
        experience = self.db.query(Experience).filter(Experience.id == experience_id).first()
        if not experience:
            return False

        # Check ownership through profile
        profile = self.db.query(Profile).filter(Profile.id == experience.profile_id).first()
        if not profile or profile.user_id != user_id:
            raise AuthenticationError("You don't have permission to delete this experience")

        self.db.delete(experience)
        self.db.commit()

        # Update profile completeness
        profile.update_completeness()
        self.db.commit()

        return True

    def reorder_experiences(self, profile_id: str, user_id: str, experience_ids: List[str]) -> List[Experience]:
        """
        Reorder experiences for a profile.
        
        Args:
            profile_id: Profile ID
            user_id: User ID (for authorization)
            experience_ids: List of experience IDs in desired order
            
        Returns:
            List of reordered experiences
            
        Raises:
            AuthenticationError: If user doesn't own the profile
        """
        # Check ownership
        profile = self.db.query(Profile).filter(Profile.id == profile_id).first()
        if not profile or profile.user_id != user_id:
            raise AuthenticationError("You don't have permission to reorder experiences for this profile")

        # Get all experiences for the profile
        experiences = (
            self.db.query(Experience)
            .filter(Experience.profile_id == profile_id)
            .all()
        )

        # Create a mapping of experience ID to experience object
        experience_map = {exp.id: exp for exp in experiences}

        # Update display order based on the provided order
        for index, experience_id in enumerate(experience_ids):
            if experience_id in experience_map:
                experience_map[experience_id].display_order = len(experience_ids) - index

        self.db.commit()

        # Return experiences in new order
        return (
            self.db.query(Experience)
            .filter(Experience.profile_id == profile_id)
            .order_by(Experience.display_order.desc())
            .all()
        )

    def add_responsibility(self, experience_id: str, user_id: str, responsibility: str) -> Experience:
        """
        Add a responsibility to an experience.
        
        Args:
            experience_id: Experience ID
            user_id: User ID (for authorization)
            responsibility: Responsibility text
            
        Returns:
            Updated experience
            
        Raises:
            ExperienceNotFoundError: If experience not found
            AuthenticationError: If user doesn't own the experience
        """
        experience = self.db.query(Experience).filter(Experience.id == experience_id).first()
        if not experience:
            raise ExperienceNotFoundError("Experience not found")

        # Check ownership through profile
        profile = self.db.query(Profile).filter(Profile.id == experience.profile_id).first()
        if not profile or profile.user_id != user_id:
            raise AuthenticationError("You don't have permission to update this experience")

        experience.add_responsibility(responsibility)
        self.db.commit()
        self.db.refresh(experience)

        return experience

    def remove_responsibility(self, experience_id: str, user_id: str, responsibility: str) -> Experience:
        """
        Remove a responsibility from an experience.
        
        Args:
            experience_id: Experience ID
            user_id: User ID (for authorization)
            responsibility: Responsibility text to remove
            
        Returns:
            Updated experience
            
        Raises:
            ExperienceNotFoundError: If experience not found
            AuthenticationError: If user doesn't own the experience
        """
        experience = self.db.query(Experience).filter(Experience.id == experience_id).first()
        if not experience:
            raise ExperienceNotFoundError("Experience not found")

        # Check ownership through profile
        profile = self.db.query(Profile).filter(Profile.id == experience.profile_id).first()
        if not profile or profile.user_id != user_id:
            raise AuthenticationError("You don't have permission to update this experience")

        experience.remove_responsibility(responsibility)
        self.db.commit()
        self.db.refresh(experience)

        return experience

    def add_technology(self, experience_id: str, user_id: str, technology: str) -> Experience:
        """
        Add a technology to an experience.
        
        Args:
            experience_id: Experience ID
            user_id: User ID (for authorization)
            technology: Technology name
            
        Returns:
            Updated experience
            
        Raises:
            ExperienceNotFoundError: If experience not found
            AuthenticationError: If user doesn't own the experience
        """
        experience = self.db.query(Experience).filter(Experience.id == experience_id).first()
        if not experience:
            raise ExperienceNotFoundError("Experience not found")

        # Check ownership through profile
        profile = self.db.query(Profile).filter(Profile.id == experience.profile_id).first()
        if not profile or profile.user_id != user_id:
            raise AuthenticationError("You don't have permission to update this experience")

        experience.add_technology(technology)
        self.db.commit()
        self.db.refresh(experience)

        return experience

    def remove_technology(self, experience_id: str, user_id: str, technology: str) -> Experience:
        """
        Remove a technology from an experience.
        
        Args:
            experience_id: Experience ID
            user_id: User ID (for authorization)
            technology: Technology name to remove
            
        Returns:
            Updated experience
            
        Raises:
            ExperienceNotFoundError: If experience not found
            AuthenticationError: If user doesn't own the experience
        """
        experience = self.db.query(Experience).filter(Experience.id == experience_id).first()
        if not experience:
            raise ExperienceNotFoundError("Experience not found")

        # Check ownership through profile
        profile = self.db.query(Profile).filter(Profile.id == experience.profile_id).first()
        if not profile or profile.user_id != user_id:
            raise AuthenticationError("You don't have permission to update this experience")

        experience.remove_technology(technology)
        self.db.commit()
        self.db.refresh(experience)

        return experience

