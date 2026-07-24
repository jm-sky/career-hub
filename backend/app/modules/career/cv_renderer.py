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

# Per-template defaults. ``layout`` picks the structural HTML/CSS a template
# renders with ("single" — one stacked column; "sidebar" — banner header plus
# a two-column body); "accent"/"font" are just the starting point a CV version
# can override independently via accent_color/font_family.
TEMPLATE_DEFAULTS: dict[str, dict[str, str]] = {
    "default": {"accent": "#0f766e", "font": "sans", "layout": "single"},
    "modern": {"accent": "#0369a1", "font": "modern-sans", "layout": "single"},
    "classic": {"accent": "#1f2937", "font": "serif", "layout": "single"},
    "minimal": {"accent": "#374151", "font": "minimal-sans", "layout": "single"},
    "sidebar": {"accent": "#0f766e", "font": "modern-sans", "layout": "sidebar"},
}

# Curated, print-safe font stacks — kept as a fixed set (rather than free text)
# since WeasyPrint only has the fonts installed in the app container image;
# arbitrary font names would silently fall back rather than error.
FONT_STACKS: dict[str, str] = {
    "sans": "'Helvetica Neue', Arial, sans-serif",
    "modern-sans": "'Segoe UI', 'DejaVu Sans', sans-serif",
    "serif": "Georgia, 'Times New Roman', serif",
    "minimal-sans": "'DejaVu Sans', Arial, sans-serif",
    "mono": "'Courier New', 'DejaVu Sans Mono', monospace",
}

# Spacing/size presets — the "how much fits on a page" knob, independent of
# font and color.
DENSITY_PRESETS: dict[str, dict[str, str]] = {
    "compact": {"font_size": "9.5pt", "line_height": "1.35", "section_gap": "4mm", "entry_gap": "2.5mm"},
    "standard": {"font_size": "10.5pt", "line_height": "1.45", "section_gap": "5mm", "entry_gap": "3.5mm"},
    "spacious": {"font_size": "11.5pt", "line_height": "1.6", "section_gap": "6.5mm", "entry_gap": "4.5mm"},
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


def _shared_css(font_stack: str, accent: str, dens: dict[str, str]) -> str:
    """CSS rules common to every layout — typography, entries, chips."""
    return f"""
  * {{ box-sizing: border-box; }}
  body {{ font-family: {font_stack}; color: #1f2430; font-size: {dens['font_size']}; line-height: {dens['line_height']}; margin: 0; }}
  h1 {{ font-size: 20pt; margin: 0 0 1mm; }}
  .headline {{ font-size: 12pt; margin: 0 0 2mm; }}
  .contact {{ font-size: 9pt; }}
  h2 {{ font-size: 11pt; text-transform: uppercase; letter-spacing: 0.08em; color: {accent};
       border-bottom: 1px solid #e5e7eb; padding-bottom: 1mm; margin: {dens['section_gap']} 0 2.5mm; }}
  section:first-child h2 {{ margin-top: 0; }}
  section {{ page-break-inside: auto; }}
  .entry {{ margin-bottom: {dens['entry_gap']}; page-break-inside: avoid; }}
  .entry.compact {{ margin-bottom: 1.5mm; }}
  .entry-head {{ display: flex; justify-content: space-between; align-items: baseline; }}
  .entry-sub {{ color: #4b5563; font-size: 9.5pt; }}
  .dates {{ color: #6b7280; font-size: 9pt; margin-left: 3mm; white-space: nowrap; }}
  p {{ margin: 1mm 0; }}
  ul {{ margin: 1mm 0 0; padding-left: 5mm; }}
  li {{ margin-bottom: 0.5mm; }}
  .chips {{ display: flex; flex-wrap: wrap; gap: 1.5mm; }}
  .chip {{ background: #f3f4f6; border-radius: 2mm; padding: 0.8mm 2.5mm; font-size: 9pt; }}
  .dots {{ color: {accent}; letter-spacing: 0.1em; }}
  .watermark {{ position: fixed; bottom: 4mm; right: 0; font-size: 8pt; color: #9ca3af; }}
"""


def _header_html(data: CvRenderData, contact_line: str, banner: bool) -> str:
    profile = data.profile
    return f"""<header class="{'banner' if banner else ''}">
    <h1>{escape(data.user_name)}</h1>
    {f'<p class="headline">{escape(profile.headline)}</p>' if profile.headline else ''}
    {f'<p class="contact">{contact_line}</p>' if contact_line else ''}
  </header>"""


def _render_single(data: CvRenderData, contact_line: str, summary: str | None, accent: str, font_stack: str, dens: dict[str, str]) -> tuple[str, str]:
    """Returns (css, body_html) for the single-column layout."""
    sections = data.sections
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

    css = _shared_css(font_stack, accent, dens) + f"""
  header {{ border-bottom: 2px solid {accent}; padding-bottom: 4mm; margin-bottom: 6mm; }}
  h1 {{ color: {accent}; }}
  .headline {{ color: #374151; }}
  .contact {{ color: #6b7280; }}
"""
    body_html = f"""{_header_html(data, contact_line, banner=False)}
  {''.join(body_sections)}"""
    return css, body_html


def _render_sidebar(data: CvRenderData, contact_line: str, summary: str | None, accent: str, font_stack: str, dens: dict[str, str]) -> tuple[str, str]:
    """Returns (css, body_html) for the two-column sidebar layout."""
    sections = data.sections
    main_sections = []
    if sections.includeSummary and summary:
        main_sections.append(_section("Summary", f"<p>{escape(summary)}</p>"))
    if data.experiences:
        main_sections.append(_section("Experience", _experience_html(data.experiences)))
    if data.projects:
        main_sections.append(_section("Projects", _project_html(data.projects)))
    if data.achievements:
        main_sections.append(_section("Achievements", _achievements_html(data.achievements)))

    side_sections = []
    if data.skills:
        side_sections.append(_section("Skills", _skills_html(data.skills)))
    if data.languages:
        side_sections.append(_section("Languages", _languages_html(data.languages)))
    if data.education:
        side_sections.append(_section("Education", _education_html(data.education)))
    if data.certifications:
        side_sections.append(_section("Certifications", _certifications_html(data.certifications)))

    css = _shared_css(font_stack, accent, dens) + f"""
  header.banner {{ background: {accent}; color: #fff; border-radius: 2mm; padding: 6mm 8mm; margin-bottom: {dens['section_gap']}; }}
  header.banner h1, header.banner .headline {{ color: #fff; }}
  header.banner .contact {{ color: rgba(255, 255, 255, 0.82); }}
  .layout {{ display: flex; gap: 8mm; align-items: flex-start; }}
  .sidebar {{ flex: 0 0 33%; background: #f8fafc; border-radius: 2mm; padding: 5mm; }}
  .sidebar h2 {{ font-size: 9.5pt; border-bottom: none; margin-top: 0; }}
  .main {{ flex: 1 1 auto; min-width: 0; }}
"""
    body_html = f"""{_header_html(data, contact_line, banner=True)}
  <div class="layout">
    <div class="main">{''.join(main_sections)}</div>
    <div class="sidebar">{''.join(side_sections)}</div>
  </div>"""
    return css, body_html


def build_cv_html(
    data: CvRenderData,
    template: str,
    watermark: bool,
    accent_color: str | None = None,
    font_family: str | None = None,
    density: str | None = None,
) -> str:
    """Render the full, self-contained CV document (inline CSS only — WeasyPrint
    gets no network access and must not need any).

    ``accent_color``/``font_family``/``density`` override the template's
    defaults when set. ``accent_color`` is trusted to already be a validated
    ``#rrggbb`` string (enforced by the create/update request schemas) since
    it is interpolated directly into inline CSS here; ``font_family`` and
    ``density`` are validated by the schemas against ``FONT_STACKS``/
    ``DENSITY_PRESETS`` keys, with a safe fallback here regardless.
    """
    defaults = TEMPLATE_DEFAULTS.get(template, TEMPLATE_DEFAULTS["default"])
    accent = accent_color or defaults["accent"]
    font_stack = FONT_STACKS.get(font_family or defaults["font"], FONT_STACKS["sans"])
    dens = DENSITY_PRESETS.get(density or "standard", DENSITY_PRESETS["standard"])

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
    watermark_html = '<div class="watermark">Created with CareerHub — Free plan</div>' if watermark else ""

    render = _render_sidebar if defaults["layout"] == "sidebar" else _render_single
    layout_css, body_html = render(data, contact_line, summary, accent, font_stack, dens)

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @page {{ size: A4; margin: 18mm 16mm; }}
{layout_css}
</style>
</head>
<body>
  {watermark_html}
  {body_html}
</body>
</html>"""


def render_pdf(html: str) -> bytes:
    """HTML → PDF bytes. Lazy import: WeasyPrint needs native Pango/Cairo libs
    that only exist in the app container image."""
    from weasyprint import HTML

    pdf: bytes = HTML(string=html).write_pdf()
    return pdf
