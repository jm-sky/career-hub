"""Business logic for languages (career module)."""

from app.common.id_utils import generate_id

from .db_models import LanguageDB
from .language_repository import LanguageRepository
from .schemas import CreateLanguageRequest, LanguageResponse, UpdateLanguageRequest


def _build_response(language: LanguageDB) -> LanguageResponse:
    return LanguageResponse(
        id=language.id,
        profile_id=language.profile_id,
        name=language.name,
        level=language.level,  # type: ignore[arg-type]
        description=language.description,
        display_order=language.display_order,
        created_at=language.created_at,
        updated_at=language.updated_at,
    )


class LanguageService:
    """Business logic for language CRUD and reordering."""

    def __init__(self, repository: LanguageRepository):
        self.repository = repository

    async def list_for_profile(self, profile_id: str) -> list[LanguageResponse]:
        entries = await self.repository.list_by_profile(profile_id)
        return [_build_response(entry) for entry in entries]

    async def get_entity_for_profile(self, id_: str, profile_id: str) -> LanguageDB | None:
        return await self.repository.get_by_id_and_profile(id_, profile_id)

    async def create(self, profile_id: str, payload: CreateLanguageRequest) -> LanguageResponse:
        existing = await self.repository.get_by_profile_and_name(profile_id, payload.name)
        if existing is not None:
            raise ValueError(f"A language entry for '{payload.name}' already exists on this profile.")

        display_order = await self.repository.get_next_display_order(profile_id)
        language = LanguageDB(
            id=generate_id(),
            profile_id=profile_id,
            name=payload.name,
            level=payload.level,
            description=payload.description,
            display_order=display_order,
        )
        language = await self.repository.create(language)
        return _build_response(language)

    async def update(self, language: LanguageDB, payload: UpdateLanguageRequest) -> LanguageResponse:
        if payload.name is not None and payload.name != language.name:
            conflict = await self.repository.get_by_profile_and_name(language.profile_id, payload.name)
            if conflict is not None:
                raise ValueError(f"A language entry for '{payload.name}' already exists on this profile.")
            language.name = payload.name
        if payload.level is not None:
            language.level = payload.level
        if payload.description is not None:
            language.description = payload.description

        language = await self.repository.save(language)
        return _build_response(language)

    async def delete(self, language: LanguageDB) -> None:
        await self.repository.delete(language)

    async def reorder(self, profile_id: str, ordered_ids: list[str]) -> list[LanguageResponse]:
        entries = await self.repository.list_by_profile(profile_id)
        if {e.id for e in entries} != set(ordered_ids) or len(ordered_ids) != len(entries):
            raise ValueError("orderedIds must contain exactly the profile's existing language ids.")

        await self.repository.reorder(entries, ordered_ids)
        return await self.list_for_profile(profile_id)
