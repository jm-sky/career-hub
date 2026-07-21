"""Certifications seed data for Jan Madeyski (from LinkedIn)."""

from datetime import date

from app.modules.career.schemas import CreateCertificationRequest

RAW_CERTIFICATIONS: list[dict] = [
    {
        "name": "Front End Libraries",
        "issuingOrganization": "freeCodeCamp",
        "credentialId": None,
        "credentialUrl": "https://www.freecodecamp.org/certification/jan_madeyski/front-end-development-libraries",
        "issueDate": "2021-03-01",
        "expiryDate": None,
    },
    {
        "name": "Data Visualization",
        "issuingOrganization": "freeCodeCamp",
        "credentialId": None,
        "credentialUrl": "https://www.freecodecamp.org/certification/jan_madeyski/data-visualization",
        "issueDate": "2020-09-01",
        "expiryDate": None,
    },
    {
        "name": "APIs and Microservices",
        "issuingOrganization": "freeCodeCamp",
        "credentialId": None,
        "credentialUrl": "https://www.freecodecamp.org/certification/jan_madeyski/back-end-development-and-apis",
        "issueDate": "2020-08-01",
        "expiryDate": None,
    },
    {
        "name": "JavaScript Algorithms and Data Structures",
        "issuingOrganization": "freeCodeCamp",
        "credentialId": None,
        "credentialUrl": "https://www.freecodecamp.org/certification/jan_madeyski/javascript-algorithms-and-data-structures",
        "issueDate": "2020-08-01",
        "expiryDate": None,
    },
    {
        "name": "Performance Tuning and Optimizing SQL Databases",
        "issuingOrganization": "Microsoft",
        "credentialId": "MS-10987",
        "credentialUrl": None,
        "issueDate": "2019-12-01",
        "expiryDate": None,
    },
    {
        "name": "PRINCE2 Foundation Certificate in Project Management",
        "issuingOrganization": "AXELOS Global Best Practice",
        "credentialId": "GR633127941JM",
        "credentialUrl": None,
        "issueDate": "2019-12-01",
        "expiryDate": None,
    },
    {
        "name": "Atakowanie i Ochrona Webaplikacji",
        "issuingOrganization": "Niebezpiecznik.pl",
        "credentialId": None,
        "credentialUrl": None,
        "issueDate": "2018-07-01",
        "expiryDate": None,
    },
    {
        "name": "MTA: Database Fundamentals",
        "issuingOrganization": "Microsoft",
        "credentialId": "F163-2712",
        "credentialUrl": "https://www.credly.com/badges/5f0ea681-49a3-427e-b9f3-bf26b9eec642/linked_in_profile",
        "issueDate": "2015-01-01",
        "expiryDate": None,
    },
    {
        "name": "Certyfikat Biegłości — Angielski, poziom B2",
        "issuingOrganization": "Uniwersytet Warszawski",
        "credentialId": "1186/18",
        "credentialUrl": None,
        "issueDate": "2007-01-01",
        "expiryDate": None,
    },
]


def certification_key(raw: dict) -> tuple[str, str]:
    return (raw["name"], raw["issuingOrganization"])


def build_create_certification_request(raw: dict) -> CreateCertificationRequest:
    expiry = raw.get("expiryDate")
    return CreateCertificationRequest(
        name=raw["name"],
        issuingOrganization=raw["issuingOrganization"],
        credentialId=raw.get("credentialId"),
        credentialUrl=raw.get("credentialUrl"),
        issueDate=date.fromisoformat(raw["issueDate"]),
        expiryDate=date.fromisoformat(expiry) if expiry else None,
    )
