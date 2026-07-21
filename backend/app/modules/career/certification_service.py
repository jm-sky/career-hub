"""Business logic for certifications (career module, Phase 4)."""

from datetime import date

from app.common.id_utils import generate_id

from .certification_repository import CertificationRepository
from .db_models import CertificationDB
from .schemas import CertificationResponse, CreateCertificationRequest, UpdateCertificationRequest


def _is_expired(expiry_date: date | None) -> bool:
    return expiry_date is not None and expiry_date < date.today()


def _build_response(certification: CertificationDB) -> CertificationResponse:
    return CertificationResponse(
        id=certification.id,
        profile_id=certification.profile_id,
        name=certification.name,
        issuing_organization=certification.issuing_organization,
        credential_id=certification.credential_id,
        credential_url=certification.credential_url,
        issue_date=certification.issue_date,
        expiry_date=certification.expiry_date,
        isExpired=_is_expired(certification.expiry_date),
        display_order=certification.display_order,
        created_at=certification.created_at,
        updated_at=certification.updated_at,
    )


class CertificationService:
    """Business logic for certification CRUD and reordering."""

    def __init__(self, repository: CertificationRepository):
        self.repository = repository

    def _validate_dates(self, issue_date: date, expiry_date: date | None) -> None:
        if expiry_date is not None and expiry_date <= issue_date:
            raise ValueError("Expiry date must be after issue date.")

    async def list_for_profile(self, profile_id: str) -> list[CertificationResponse]:
        entries = await self.repository.list_by_profile(profile_id)
        return [_build_response(entry) for entry in entries]

    async def get_entity_for_profile(self, id_: str, profile_id: str) -> CertificationDB | None:
        return await self.repository.get_by_id_and_profile(id_, profile_id)

    async def create(self, profile_id: str, payload: CreateCertificationRequest) -> CertificationResponse:
        self._validate_dates(payload.issueDate, payload.expiryDate)
        display_order = await self.repository.get_next_display_order(profile_id)
        certification = CertificationDB(
            id=generate_id(),
            profile_id=profile_id,
            name=payload.name,
            issuing_organization=payload.issuingOrganization,
            credential_id=payload.credentialId,
            credential_url=payload.credentialUrl,
            issue_date=payload.issueDate,
            expiry_date=payload.expiryDate,
            display_order=display_order,
        )
        certification = await self.repository.create(certification)
        return _build_response(certification)

    async def update(self, certification: CertificationDB, payload: UpdateCertificationRequest) -> CertificationResponse:
        if payload.name is not None:
            certification.name = payload.name
        if payload.issuingOrganization is not None:
            certification.issuing_organization = payload.issuingOrganization
        if payload.credentialId is not None:
            certification.credential_id = payload.credentialId
        if payload.credentialUrl is not None:
            certification.credential_url = payload.credentialUrl
        if payload.issueDate is not None:
            certification.issue_date = payload.issueDate
        if payload.expiryDate is not None:
            certification.expiry_date = payload.expiryDate

        self._validate_dates(certification.issue_date, certification.expiry_date)
        certification = await self.repository.save(certification)
        return _build_response(certification)

    async def delete(self, certification: CertificationDB) -> None:
        await self.repository.delete(certification)

    async def reorder(self, profile_id: str, ordered_ids: list[str]) -> list[CertificationResponse]:
        entries = await self.repository.list_by_profile(profile_id)
        if {e.id for e in entries} != set(ordered_ids) or len(ordered_ids) != len(entries):
            raise ValueError("orderedIds must contain exactly the profile's existing certification ids.")

        await self.repository.reorder(entries, ordered_ids)
        return await self.list_for_profile(profile_id)
