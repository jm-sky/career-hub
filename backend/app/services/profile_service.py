"""Profile service for managing user profiles."""

from typing import List, Optional

from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError

from app.core.exceptions import AuthenticationError
from app.models.profile import Profile
from app.models.user import User
from app.schemas.profile import ProfileCreate, ProfileUpdate


class ProfileNotFoundError(Exception):
    """Raised when profile is not found."""

    pass


class ProfileAlreadyExistsError(Exception):
    """Raised when user already has a profile."""

    pass


class SlugAlreadyExistsError(Exception):
    """Raised when slug is already taken."""

    pass


class ProfileService:
    """Service for managing user profiles."""

    def __init__(self, db: Session):
        """Initialize profile service."""
        self.db = db

    def create_profile(self, user_id: str, profile_data: ProfileCreate) -> Profile:
        """
        Create a new profile for a user.

        Args:
            user_id: User ID
            profile_data: Profile creation data

        Returns:
            Created profile

        Raises:
            ProfileAlreadyExistsError: If user already has a profile
            SlugAlreadyExistsError: If slug is already taken
            AuthenticationError: If user not found
        """
        # Check if user exists
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise AuthenticationError("User not found")

        # Check if user already has a profile
        existing_profile = self.db.query(Profile).filter(Profile.user_id == user_id).first()
        if existing_profile:
            raise ProfileAlreadyExistsError("User already has a profile")

        # Check if slug is already taken
        if profile_data.slug:
            existing_slug = self.db.query(Profile).filter(Profile.slug == profile_data.slug).first()
            if existing_slug:
                raise SlugAlreadyExistsError("Slug is already taken")

        # Create profile
        profile = Profile(
            user_id=user_id,
            headline=profile_data.headline,
            summary=profile_data.summary,
            location=profile_data.location,
            visibility=profile_data.visibility,
            contact=profile_data.contact,
            profile_photo_url=profile_data.profile_photo_url,
            draft_data=profile_data.draft_data,
        )

        # Generate slug if not provided
        if not profile_data.slug:
            profile.slug = profile.generate_slug()
        else:
            profile.slug = profile_data.slug

        # Ensure slug uniqueness
        original_slug = profile.slug
        counter = 1
        while self.db.query(Profile).filter(Profile.slug == profile.slug).first():
            profile.slug = f"{original_slug}-{counter}"
            counter += 1

        try:
            self.db.add(profile)
            self.db.commit()
            self.db.refresh(profile)

            # Update completeness score
            profile.update_completeness()
            self.db.commit()

            return profile
        except IntegrityError:
            self.db.rollback()
            raise ProfileAlreadyExistsError("Profile creation failed due to constraint violation")

    def get_profile_by_id(self, profile_id: str, include_relations: bool = False) -> Optional[Profile]:
        """
        Get profile by ID.

        Args:
            profile_id: Profile ID
            include_relations: Whether to include related data

        Returns:
            Profile or None if not found
        """
        query = self.db.query(Profile)

        if include_relations:
            query = query.options(
                joinedload(Profile.experiences),
                # TODO: Add when models are implemented:
                # joinedload(Profile.projects),
                # joinedload(Profile.skills),
                # joinedload(Profile.education),
                # joinedload(Profile.certifications),
                # joinedload(Profile.achievements),
            )

        return query.filter(Profile.id == profile_id).first()

    def get_profile_by_user_id(self, user_id: str, include_relations: bool = False) -> Optional[Profile]:
        """
        Get profile by user ID.

        Args:
            user_id: User ID
            include_relations: Whether to include related data

        Returns:
            Profile or None if not found
        """
        query = self.db.query(Profile)

        if include_relations:
            query = query.options(
                joinedload(Profile.experiences),
                # TODO: Add when models are implemented:
                # joinedload(Profile.projects),
                # joinedload(Profile.skills),
                # joinedload(Profile.education),
                # joinedload(Profile.certifications),
                # joinedload(Profile.achievements),
            )

        return query.filter(Profile.user_id == user_id).first()

    def get_profile_by_slug(self, slug: str, include_relations: bool = False) -> Optional[Profile]:
        """
        Get profile by slug.

        Args:
            slug: Profile slug
            include_relations: Whether to include related data

        Returns:
            Profile or None if not found
        """
        query = self.db.query(Profile)

        if include_relations:
            query = query.options(
                joinedload(Profile.experiences),
                # TODO: Add when models are implemented:
                # joinedload(Profile.projects),
                # joinedload(Profile.skills),
                # joinedload(Profile.education),
                # joinedload(Profile.certifications),
                # joinedload(Profile.achievements),
            )

        return query.filter(Profile.slug == slug).first()

    def update_profile(self, profile_id: str, user_id: str, profile_data: ProfileUpdate) -> Profile:
        """
        Update a profile.

        Args:
            profile_id: Profile ID
            user_id: User ID (for authorization)
            profile_data: Profile update data

        Returns:
            Updated profile

        Raises:
            ProfileNotFoundError: If profile not found
            AuthenticationError: If user doesn't own the profile
            SlugAlreadyExistsError: If slug is already taken
        """
        profile = self.db.query(Profile).filter(Profile.id == profile_id).first()
        if not profile:
            raise ProfileNotFoundError("Profile not found")

        # Check ownership
        if profile.user_id != user_id:
            raise AuthenticationError("You don't have permission to update this profile")

        # Update fields
        update_data = profile_data.dict(exclude_unset=True)

        for field, value in update_data.items():
            if hasattr(profile, field):
                setattr(profile, field, value)

        try:
            self.db.commit()
            self.db.refresh(profile)

            # Update completeness score
            profile.update_completeness()
            self.db.commit()

            return profile
        except IntegrityError:
            self.db.rollback()
            raise SlugAlreadyExistsError("Slug is already taken")

    def delete_profile(self, profile_id: str, user_id: str) -> bool:
        """
        Delete a profile.

        Args:
            profile_id: Profile ID
            user_id: User ID (for authorization)

        Returns:
            True if deleted, False if not found

        Raises:
            AuthenticationError: If user doesn't own the profile
        """
        profile = self.db.query(Profile).filter(Profile.id == profile_id).first()
        if not profile:
            return False

        # Check ownership
        if profile.user_id != user_id:
            raise AuthenticationError("You don't have permission to delete this profile")

        self.db.delete(profile)
        self.db.commit()
        return True

    def get_public_profiles(self, limit: int = 20, offset: int = 0) -> List[Profile]:
        """
        Get public profiles.

        Args:
            limit: Maximum number of profiles to return
            offset: Number of profiles to skip

        Returns:
            List of public profiles
        """
        return (
            self.db.query(Profile)
            .filter(Profile.visibility == "PUBLIC")
            .order_by(Profile.completeness_score.desc(), Profile.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

    def search_profiles(self, query: str, limit: int = 20, offset: int = 0) -> List[Profile]:
        """
        Search public profiles by headline, summary, or location.

        Args:
            query: Search query
            limit: Maximum number of profiles to return
            offset: Number of profiles to skip

        Returns:
            List of matching profiles
        """
        search_term = f"%{query.lower()}%"

        return (
            self.db.query(Profile)
            .filter(
                Profile.visibility == "PUBLIC",
                (
                    Profile.headline.ilike(search_term)
                    | Profile.summary.ilike(search_term)
                    | Profile.location.ilike(search_term)
                ),
            )
            .order_by(Profile.completeness_score.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

    def update_completeness_score(self, profile_id: str) -> int:
        """
        Update and return profile completeness score.

        Args:
            profile_id: Profile ID

        Returns:
            Updated completeness score

        Raises:
            ProfileNotFoundError: If profile not found
        """
        profile = self.get_profile_by_id(profile_id, include_relations=True)
        if not profile:
            raise ProfileNotFoundError("Profile not found")

        profile.update_completeness()
        self.db.commit()

        return profile.completeness_score

    def is_slug_available(self, slug: str, exclude_profile_id: Optional[str] = None) -> bool:
        """
        Check if slug is available.

        Args:
            slug: Slug to check
            exclude_profile_id: Profile ID to exclude from check (for updates)

        Returns:
            True if slug is available
        """
        query = self.db.query(Profile).filter(Profile.slug == slug)

        if exclude_profile_id:
            query = query.filter(Profile.id != exclude_profile_id)

        return query.first() is None

    def generate_unique_slug(self, base_slug: str) -> str:
        """
        Generate a unique slug based on base slug.

        Args:
            base_slug: Base slug to start with

        Returns:
            Unique slug
        """
        if self.is_slug_available(base_slug):
            return base_slug

        counter = 1
        while True:
            candidate_slug = f"{base_slug}-{counter}"
            if self.is_slug_available(candidate_slug):
                return candidate_slug
            counter += 1
