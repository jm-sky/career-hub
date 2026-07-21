"""Profile seed data for Jan Madeyski."""

from app.modules.career.schemas import ContactInfo, UpdateProfileRequest

SEED_PROFILE: dict = {
    "headline": "Head of Programming · Full Stack Developer · DEV Made IT",
    "summary": (
        "Full-stack engineer and team lead with 15+ years building ERP/MES integrations, "
        "client portals, and modern SaaS products. Currently Head of the Programming Team at "
        "Skłodowscy; side projects and client work ship under the DEV Made IT personal brand — "
        "Vue/Python systems, AI-assisted back-office tools, and multi-tenant platforms."
    ),
    "location": "Warsaw, Poland",
    "visibility": "PRIVATE",
    "slug": "jan-madeyski",
    "contact": {
        "email": "jan.madeyski@gmail.com",
        "linkedin": "https://www.linkedin.com/in/jan-madeyski/",
        "website": "https://madeyski.org",
    },
}


def build_update_profile_request(raw: dict | None = None) -> UpdateProfileRequest:
    data = raw or SEED_PROFILE
    contact = data.get("contact") or {}
    return UpdateProfileRequest(
        headline=data.get("headline"),
        summary=data.get("summary"),
        location=data.get("location"),
        visibility=data.get("visibility"),
        slug=data.get("slug"),
        contact=ContactInfo(
            email=contact.get("email"),
            phone=contact.get("phone"),
            linkedin=contact.get("linkedin"),
            website=contact.get("website"),
        ),
    )
