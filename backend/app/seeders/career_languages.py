"""Spoken languages seed data for Jan Madeyski."""

from app.modules.career.schemas import CreateLanguageRequest, UpdateLanguageRequest

RAW_LANGUAGES: list[dict] = [
    {
        "name": "Polish",
        "level": "NATIVE",
        "description": "Native speaker.",
    },
    {
        "name": "English",
        "level": "B2",
        "description": "Fluent in speech and writing (B2).",
    },
    {
        "name": "Russian",
        "level": "B1",
        "description": "Approx. B1–B2.",
    },
    {
        "name": "Ukrainian",
        "level": "A2",
        "description": "Approx. A2.",
    },
    {
        "name": "French",
        "level": "A2",
        "description": "Approx. A2.",
    },
]


def build_create_language_request(raw: dict) -> CreateLanguageRequest:
    return CreateLanguageRequest(
        name=raw["name"],
        level=raw["level"],
        description=raw.get("description"),
    )


def build_update_language_request(raw: dict) -> UpdateLanguageRequest:
    return UpdateLanguageRequest(
        name=raw["name"],
        level=raw["level"],
        description=raw.get("description"),
    )
