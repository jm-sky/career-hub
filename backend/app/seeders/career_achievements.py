"""Profile-level achievements seed data for Jan Madeyski.

Separate from per-project ``achievements`` strings on ProjectDB.
"""

from datetime import date

from app.modules.career.schemas import CreateAchievementRequest

# Titles from older seed revisions — deleted on seed so renames don't leave duplicates.
OBSOLETE_ACHIEVEMENT_TITLES = {
    "Founded DEV Made IT",
}

RAW_ACHIEVEMENTS: list[dict] = [
    {
        "title": "Head of the Programming Team",
        "description": (
            "Promoted to lead the programming team at Skłodowscy Sp. z o.o., owning delivery "
            "of portals, ERP/MES integrations, and internal AI tooling."
        ),
        "date": "2021-11-01",
        "category": "OTHER",
        "url": None,
    },
    {
        "title": "DEV Made IT personal brand",
        "description": (
            "Started shipping SaaS products, client websites, and full-stack tools under the "
            "DEV Made IT personal brand (Gear Stack, Company Hub, SaasBase, CareerHub, and more)."
        ),
        "date": "2025-04-01",
        "category": "OTHER",
        "url": "https://dev-made.it",
    },
    {
        "title": "Portal Klienta — long-running production system",
        "description": (
            "Led architecture and delivery of a client portal used by hundreds of users, "
            "integrating ERP data, documents, and later KSeF e-invoicing."
        ),
        "date": "2018-01-01",
        "category": "OTHER",
        "url": "https://portal-klienta.sklodowscy.pl",
    },
    {
        "title": "LiteMES — original MES for production floor",
        "description": (
            "Designed and led development of a custom manufacturing execution system with "
            "RFID/barcode workflows, service tracking, and time & attendance."
        ),
        "date": "2016-02-01",
        "category": "OTHER",
        "url": None,
    },
]


def build_create_achievement_request(raw: dict) -> CreateAchievementRequest:
    d = raw.get("date")
    return CreateAchievementRequest(
        title=raw["title"],
        description=raw.get("description"),
        date=date.fromisoformat(d) if d else None,
        category=raw.get("category"),
        url=raw.get("url"),
    )
