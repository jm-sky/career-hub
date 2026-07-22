"""Education / courses seed data for Jan Madeyski."""

from datetime import date

from app.modules.career.schemas import CreateEducationRequest

RAW_EDUCATION: list[dict] = [
    {
        "institution": "University of Warsaw",
        "degree": "Psychology studies (without Master's Degree)",
        "fieldOfStudy": "Psychology",
        "startDate": "2005-10-01",
        "endDate": "2011-06-01",
        "grade": None,
        "description": ("Psychology at Uniwersytet Warszawski (2005–2011), completed without a Master's Degree. " "Activities: SKN Psychologii Uzależnień (Student Scientific Circle for Addiction Psychology)."),
    },
]


def education_key(raw: dict) -> tuple[str, str, str]:
    return (raw["institution"], raw["degree"], raw["startDate"])


def build_create_education_request(raw: dict) -> CreateEducationRequest:
    end = raw.get("endDate")
    return CreateEducationRequest(
        institution=raw["institution"],
        degree=raw["degree"],
        fieldOfStudy=raw.get("fieldOfStudy"),
        startDate=date.fromisoformat(raw["startDate"]),
        endDate=date.fromisoformat(end) if end else None,
        grade=raw.get("grade"),
        description=raw.get("description"),
    )
