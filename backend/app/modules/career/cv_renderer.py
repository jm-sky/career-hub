"""HTML/CSS CV rendering for the career module (Phase 5 — WeasyPrint pipeline).

``build_cv_html`` is a pure function (DB rows in, HTML string out) so templates
and watermarking are unit-testable without WeasyPrint or a database.
``render_pdf`` is the only place WeasyPrint is touched — it's imported lazily
because it drags in heavy native libraries (Pango/Cairo) that unit tests and
non-PDF code paths should never need.
"""

from dataclasses import dataclass, field
from datetime import date
from html import escape

from .db_models import (
    AchievementDB,
    CertificationDB,
    EducationDB,
    ExperienceDB,
    LanguageDB,
    ProfileDB,
    ProjectDB,
    SkillDB,
)
from .schemas import CvSectionsConfig

# Per-template accent styling. Templates share one layout; they differ in font
# stack and accent color, which keeps every template render path exercised by
# the same tests.
TEMPLATE_STYLES: dict[str, dict[str, str]] = {
    "default": {"font": "'Helvetica Neue', Arial, sans-serif", "accent": "#0f766e"},
    "modern": {"font": "'Segoe UI', 'DejaVu Sans', sans-serif", "accent": "#0369a1"},
    "classic": {"font": "Georgia, 'Times New Roman', serif", "accent": "#1f2937"},
    "minimal": {"font": "'DejaVu Sans', Arial, sans-serif", "accent": "#374151"},
}


@dataclass
class CvRenderData:
    """Everything the renderer needs, already selected/ordered by the service."""

    user_name: str
    profile: ProfileDB
    sections: CvSectionsConfig
    experiences: list[ExperienceDB] = field(default_factory=list)
    projects: list[ProjectDB] = field(default_factory=list)
    skills: list[tuple[SkillDB, str]] = field(default_factory=list)  # (skill, technology name)
    education: list[EducationDB] = field(default_factory=list)
    certifications: list[CertificationDB] = field(default_factory=list)
    achievements: list[AchievementDB] = field(default_factory=list)
    languages: list[LanguageDB] = field(default_factory=list)


def _format_date(value: date | None) -> str:
    return value.strftime("%m/%Y") if value else ""


def _date_range(start: date | None, end: date | None, ongoing: bool) -> str:
    start_str = _format_date(start)
    end_str = "present" if ongoing or (start and not end) else _format_date(end)
    return f"{start_str} – {end_str}" if start_str else end_str


def _section(title: str, body: str) -> str:
    return f"<section><h2>{escape(title)}</h2>{body}</section>"


def _experience_html(experiences: list[ExperienceDB]) -> str:
    items = []
    for exp in experiences:
        responsibilities = "".join(f"<li>{escape(str(r))}</li>" for r in exp.responsibilities or [])
        items.append(
            '<div class="entry">'
            f'<div class="entry-head"><strong>{escape(exp.position)}</strong>'
            f'<span class="dates">{_date_range(exp.start_date, exp.end_date, exp.is_current)}</span></div>'
            f'<div class="entry-sub">{escape(exp.company_name)}'
            + (f" · {escape(exp.employment_type)}" if exp.employment_type else "")
            + "</div>"
            + (f"<p>{escape(exp.description)}</p>" if exp.description else "")
            + (f"<ul>{responsibilities}</ul>" if responsibilities else "")
            + "</div>"
        )
    return "".join(items)


def _project_html(projects: list[ProjectDB]) -> str:
    items = []
    for project in projects:
        company = project.anonymized_company if project.is_anonymized else None
        items.append(
            '<div class="entry">'
            f'<div class="entry-head"><strong>{escape(project.name)}</strong>'
            f'<span class="dates">{_date_range(project.start_date, project.end_date, project.is_ongoing)}</span></div>'
            + (f'<div class="entry-sub">{escape(project.role or "")}' + (f" @ {escape(company)}" if company else "") + "</div>" if project.role or company else "")
            + (f"<p>{escape(project.description)}</p>" if project.description else "")
            + "</div>"
        )
    return "".join(items)


def _skills_html(skills: list[tuple[SkillDB, str]]) -> str:
    chips = []
    for skill, technology_name in skills:
        dots = "●" * skill.level + "○" * (5 - skill.level)
        chips.append(f'<span class="chip">{escape(technology_name)} <span class="dots">{dots}</span></span>')
    return f'<div class="chips">{"".join(chips)}</div>'


def _education_html(education: list[EducationDB]) -> str:
    items = []
    for entry in education:
        items.append(
            '<div class="entry">'
            f'<div class="entry-head"><strong>{escape(entry.degree)}</strong>'
            f'<span class="dates">{_date_range(entry.start_date, entry.end_date, False)}</span></div>'
            f'<div class="entry-sub">{escape(entry.institution)}' + (f" · {escape(entry.field_of_study)}" if entry.field_of_study else "") + "</div></div>"
        )
    return "".join(items)


def _certifications_html(certifications: list[CertificationDB]) -> str:
    items = []
    for cert in certifications:
        items.append('<div class="entry compact">' f"<strong>{escape(cert.name)}</strong> — {escape(cert.issuing_organization)}" f'<span class="dates">{_format_date(cert.issue_date)}</span></div>')
    return "".join(items)


def _achievements_html(achievements: list[AchievementDB]) -> str:
    items = []
    for achievement in achievements:
        items.append('<div class="entry compact">' f"<strong>{escape(achievement.title)}</strong>" + (f" — {escape(achievement.description)}" if achievement.description else "") + f'<span class="dates">{_format_date(achievement.date)}</span></div>')
    return "".join(items)


def _languages_html(languages: list[LanguageDB]) -> str:
    chips = "".join(f'<span class="chip">{escape(language.name)} <span class="dots">{escape(language.level)}</span></span>' for language in languages)
    return f'<div class="chips">{chips}</div>'


def build_cv_html(data: CvRenderData, template: str, watermark: bool) -> str:
    """Render the full, self-contained CV document (inline CSS only — WeasyPrint
    gets no network access and must not need any)."""
    style = TEMPLATE_STYLES.get(template, TEMPLATE_STYLES["default"])
    profile = data.profile
    sections = data.sections

    contact_bits = []
    contact = profile.contact or {}
    for key in ("email", "phone", "linkedin", "website"):
        if contact.get(key):
            contact_bits.append(escape(str(contact[key])))
    if profile.location:
        contact_bits.append(escape(profile.location))
    contact_line = " · ".join(contact_bits)

    summary = sections.customSummary or profile.summary
    body_sections = []
    if sections.includeSummary and summary:
        body_sections.append(_section("Summary", f"<p>{escape(summary)}</p>"))
    if data.experiences:
        body_sections.append(_section("Experience", _experience_html(data.experiences)))
    if data.projects:
        body_sections.append(_section("Projects", _project_html(data.projects)))
    if data.skills:
        body_sections.append(_section("Skills", _skills_html(data.skills)))
    if data.education:
        body_sections.append(_section("Education", _education_html(data.education)))
    if data.certifications:
        body_sections.append(_section("Certifications", _certifications_html(data.certifications)))
    if data.achievements:
        body_sections.append(_section("Achievements", _achievements_html(data.achievements)))
    if data.languages:
        body_sections.append(_section("Languages", _languages_html(data.languages)))

    watermark_html = '<div class="watermark">Created with CareerHub — Free plan</div>' if watermark else ""

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @page {{ size: A4; margin: 18mm 16mm; }}
  * {{ box-sizing: border-box; }}
  body {{ font-family: {style['font']}; color: #1f2430; font-size: 10.5pt; line-height: 1.45; margin: 0; }}
  header {{ border-bottom: 2px solid {style['accent']}; padding-bottom: 4mm; margin-bottom: 6mm; }}
  h1 {{ font-size: 20pt; margin: 0 0 1mm; color: {style['accent']}; }}
  .headline {{ font-size: 12pt; margin: 0 0 2mm; color: #374151; }}
  .contact {{ font-size: 9pt; color: #6b7280; }}
  h2 {{ font-size: 11pt; text-transform: uppercase; letter-spacing: 0.08em; color: {style['accent']};
       border-bottom: 1px solid #e5e7eb; padding-bottom: 1mm; margin: 5mm 0 2.5mm; }}
  section {{ page-break-inside: auto; }}
  .entry {{ margin-bottom: 3.5mm; page-break-inside: avoid; }}
  .entry.compact {{ margin-bottom: 1.5mm; }}
  .entry-head {{ display: flex; justify-content: space-between; align-items: baseline; }}
  .entry-sub {{ color: #4b5563; font-size: 9.5pt; }}
  .dates {{ color: #6b7280; font-size: 9pt; margin-left: 3mm; white-space: nowrap; }}
  p {{ margin: 1mm 0; }}
  ul {{ margin: 1mm 0 0; padding-left: 5mm; }}
  li {{ margin-bottom: 0.5mm; }}
  .chips {{ display: flex; flex-wrap: wrap; gap: 1.5mm; }}
  .chip {{ background: #f3f4f6; border-radius: 2mm; padding: 0.8mm 2.5mm; font-size: 9pt; }}
  .dots {{ color: {style['accent']}; letter-spacing: 0.1em; }}
  .watermark {{ position: fixed; bottom: 4mm; right: 0; font-size: 8pt; color: #9ca3af; }}
</style>
</head>
<body>
  {watermark_html}
  <header>
    <h1>{escape(data.user_name)}</h1>
    {f'<p class="headline">{escape(profile.headline)}</p>' if profile.headline else ''}
    {f'<p class="contact">{contact_line}</p>' if contact_line else ''}
  </header>
  {''.join(body_sections)}
</body>
</html>"""


def render_pdf(html: str) -> bytes:
    """HTML → PDF bytes. Lazy import: WeasyPrint needs native Pango/Cairo libs
    that only exist in the app container image."""
    from weasyprint import HTML

    pdf: bytes = HTML(string=html).write_pdf()
    return pdf
