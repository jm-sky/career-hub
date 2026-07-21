"""Business logic for education entries (career module, Phase 4)."""

from datetime import date

from app.common.id_utils import generate_id

from .db_models import EducationDB
from .education_repository import EducationRepository
from .schemas import CreateEducationRequest, EducationResponse, UpdateEducationRequest


def _build_response(education: EducationDB) -> EducationResponse:
    return EducationResponse(
        id=education.id,
        profile_id=education.profile_id,
        institution=education.institution,
        degree=education.degree,
        field_of_study=education.field_of_study,
        start_date=education.start_date,
        end_date=education.end_date,
        grade=education.grade,
        description=education.description,
        display_order=education.display_order,
        created_at=education.created_at,
        updated_at=education.updated_at,
    )


class EducationService:
    """Business logic for education CRUD and reordering."""

    def __init__(self, repository: EducationRepository):
        self.repository = repository

    def _validate_dates(self, start_date: date, end_date: date | None) -> None:
        if end_date is not None and end_date <= start_date:
            raise ValueError("End date must be after start date.")

    async def list_for_profile(self, profile_id: str) -> list[EducationResponse]:
        entries = await self.repository.list_by_profile(profile_id)
        return [_build_response(entry) for entry in entries]

    async def get_entity_for_profile(self, id_: str, profile_id: str) -> EducationDB | None:
        return await self.repository.get_by_id_and_profile(id_, profile_id)

    async def create(self, profile_id: str, payload: CreateEducationRequest) -> EducationResponse:
        self._validate_dates(payload.startDate, payload.endDate)
        display_order = await self.repository.get_next_display_order(profile_id)
        education = EducationDB(
            id=generate_id(),
            profile_id=profile_id,
            institution=payload.institution,
            degree=payload.degree,
            field_of_study=payload.fieldOfStudy,
            start_date=payload.startDate,
            end_date=payload.endDate,
            grade=payload.grade,
            description=payload.description,
            display_order=display_order,
        )
        education = await self.repository.create(education)
        return _build_response(education)

    async def update(self, education: EducationDB, payload: UpdateEducationRequest) -> EducationResponse:
        if payload.institution is not None:
            education.institution = payload.institution
        if payload.degree is not None:
            education.degree = payload.degree
        if payload.fieldOfStudy is not None:
            education.field_of_study = payload.fieldOfStudy
        if payload.startDate is not None:
            education.start_date = payload.startDate
        if payload.endDate is not None:
            education.end_date = payload.endDate
        if payload.grade is not None:
            education.grade = payload.grade
        if payload.description is not None:
            education.description = payload.description

        self._validate_dates(education.start_date, education.end_date)
        education = await self.repository.save(education)
        return _build_response(education)

    async def delete(self, education: EducationDB) -> None:
        await self.repository.delete(education)

    async def reorder(self, profile_id: str, ordered_ids: list[str]) -> list[EducationResponse]:
        entries = await self.repository.list_by_profile(profile_id)
        if {e.id for e in entries} != set(ordered_ids) or len(ordered_ids) != len(entries):
            raise ValueError("orderedIds must contain exactly the profile's existing education ids.")

        await self.repository.reorder(entries, ordered_ids)
        return await self.list_for_profile(profile_id)
