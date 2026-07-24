"""AI-backed career features (Phase 7): description optimization, responsibility
and skill suggestions, and profile-vs-role gap analysis.

Reuses the ``ai`` module's OpenRouter provider + token-accounting plumbing
(``OpenRouterProvider.chat``, ``HistoryRepository``) for a one-shot completion —
a different use case from that module's own chat/conversation endpoints, so this
is new service code rather than a call into ``ChatService``.
"""

import json
import re

from app.modules.ai.providers.openrouter import OpenRouterProvider
from app.modules.ai.repositories import HistoryRepository
from app.modules.ai.services.settings_service import SettingsService as AiSettingsService
from app.modules.ai.utils.models_config import calculate_cost

from .experience_repository import ExperienceRepository
from .project_repository import ProjectRepository
from .responsibilities_library_repository import ResponsibilitiesLibraryRepository
from .schemas import (
    AnalyzeProfileResponse,
    OptimizeDescriptionRequest,
    OptimizeDescriptionResponse,
    SuggestResponsibilitiesRequest,
    SuggestResponsibilitiesResponse,
)
from .skill_repository import SkillRepository

_LIBRARY_MATCH_THRESHOLD = 5


def _split_lines(message: str) -> list[str]:
    """AI responses are asked for one item per line — strip numbering/bullets."""
    lines = []
    for raw_line in message.splitlines():
        line = raw_line.strip().strip("-•*").strip()
        line = re.sub(r"^\d+[.)]\s*", "", line)
        if line:
            lines.append(line)
    return lines


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    deduped = []
    for item in items:
        key = item.lower()
        if key not in seen:
            seen.add(key)
            deduped.append(item)
    return deduped


def _parse_analysis(message: str) -> AnalyzeProfileResponse:
    match = re.search(r"\{.*\}", message, re.DOTALL)
    if not match:
        return AnalyzeProfileResponse(matchScore=0, strengths=[], gaps=[], recommendations=[])
    try:
        data = json.loads(match.group(0))
    except json.JSONDecodeError:
        return AnalyzeProfileResponse(matchScore=0, strengths=[], gaps=[], recommendations=[])
    return AnalyzeProfileResponse(
        matchScore=max(0, min(100, int(data.get("matchScore", 0)))),
        strengths=[str(item) for item in data.get("strengths", [])],
        gaps=[str(item) for item in data.get("gaps", [])],
        recommendations=[str(item) for item in data.get("recommendations", [])],
    )


class CareerAiService:
    """One-shot AI completions for the career module, gated to Pro/Expert (or
    BYOK Free) at the router/dependency level — this service assumes access has
    already been granted."""

    def __init__(
        self,
        ai_settings_service: AiSettingsService,
        history_repo: HistoryRepository,
        responsibilities_repo: ResponsibilitiesLibraryRepository,
        experience_repo: ExperienceRepository,
        project_repo: ProjectRepository,
        skill_repo: SkillRepository,
    ):
        self.ai_settings_service = ai_settings_service
        self.history_repo = history_repo
        self.responsibilities_repo = responsibilities_repo
        self.experience_repo = experience_repo
        self.project_repo = project_repo
        self.skill_repo = skill_repo

    async def _complete(self, user_id: str, operation_type: str, messages: list[dict[str, str]], input_data: dict) -> str:
        user_settings = await self.ai_settings_service.get_settings(user_id)
        api_token = await self.ai_settings_service.get_api_token(user_id) if user_settings.use_own_token else None

        provider = OpenRouterProvider(api_key=api_token)
        response = await provider.chat(
            messages=messages,
            model=user_settings.selected_model,
            max_tokens=user_settings.max_tokens,
            temperature=user_settings.temperature,
        )

        cost = calculate_cost(response.model, response.prompt_tokens, response.completion_tokens)
        await self.history_repo.create(
            user_id=user_id,
            operation_type=operation_type,
            model=response.model,
            prompt_tokens=response.prompt_tokens,
            completion_tokens=response.completion_tokens,
            total_tokens=response.total_tokens,
            cost_usd=cost,
            input_data=input_data,
            output_data={"message": response.message},
            metadata={"module": "career", "used_own_token": user_settings.use_own_token},
        )
        return response.message

    async def optimize_description(self, user_id: str, payload: OptimizeDescriptionRequest) -> OptimizeDescriptionResponse:
        context_lines = []
        if payload.targetRole:
            context_lines.append(f"Target role: {payload.targetRole}")
        if payload.seniorityLevel:
            context_lines.append(f"Seniority level: {payload.seniorityLevel}")
        context = "\n".join(context_lines)

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a professional CV writer. Rewrite the given responsibility or "
                    "description to be concise, achievement-oriented, and use strong action verbs. "
                    "Keep it to 1-3 sentences. Reply with the rewritten text only — no preamble, no quotes."
                ),
            },
            {"role": "user", "content": f"{context}\n\nOriginal text:\n{payload.text}".strip()},
        ]
        message = await self._complete(
            user_id,
            "career_optimize_description",
            messages,
            {"text": payload.text, "targetRole": payload.targetRole, "seniorityLevel": payload.seniorityLevel},
        )
        return OptimizeDescriptionResponse(optimizedText=message.strip().strip('"'))

    async def suggest_responsibilities(self, user_id: str, payload: SuggestResponsibilitiesRequest) -> SuggestResponsibilitiesResponse:
        library_matches = await self.responsibilities_repo.find(payload.roleCategory, payload.seniorityLevel)
        if len(library_matches) >= _LIBRARY_MATCH_THRESHOLD:
            await self.responsibilities_repo.bump_usage([m.id for m in library_matches])
            return SuggestResponsibilitiesResponse(suggestions=[m.responsibility for m in library_matches], source="library")

        messages = [
            {
                "role": "system",
                "content": ("You are a career coach. List 6-8 concrete, distinct professional " "responsibilities typical for the given role and seniority level. " "Reply with one responsibility per line, no numbering, no bullet characters."),
            },
            {"role": "user", "content": f"Role: {payload.roleCategory}\nSeniority: {payload.seniorityLevel or 'any'}"},
        ]
        message = await self._complete(
            user_id,
            "career_suggest_responsibilities",
            messages,
            {"roleCategory": payload.roleCategory, "seniorityLevel": payload.seniorityLevel},
        )
        generated = _split_lines(message)
        if generated:
            await self.responsibilities_repo.create_many(payload.roleCategory, payload.seniorityLevel, generated)

        combined = _dedupe([m.responsibility for m in library_matches] + generated)
        return SuggestResponsibilitiesResponse(suggestions=combined, source="ai")

    async def suggest_skills(self, user_id: str, role: str, seniority_level: str | None = None) -> list[str]:
        messages = [
            {
                "role": "system",
                "content": ("You are a technical recruiter. List 8-12 specific technologies, tools, or " "skills commonly required for the given role. Reply with one skill per line, " "no numbering, no bullet characters, no descriptions."),
            },
            {"role": "user", "content": f"Role: {role}\nSeniority: {seniority_level or 'any'}"},
        ]
        message = await self._complete(
            user_id,
            "career_suggest_skills",
            messages,
            {"role": role, "seniorityLevel": seniority_level},
        )
        return _split_lines(message)

    async def analyze_profile(self, user_id: str, profile_id: str, target_role: str) -> AnalyzeProfileResponse:
        experiences = await self.experience_repo.list_by_profile(profile_id)
        projects = await self.project_repo.list_by_profile(profile_id)
        skill_rows = await self.skill_repo.list_by_profile(profile_id)

        experience_lines = [f"- {e.position} at {e.company_name} ({e.start_date} - {e.end_date or 'present'}): {e.description or ''}" for e in experiences]
        project_lines = [f"- {p.name}: {p.description or ''}" for p in projects]
        skill_lines = [f"- {technology.name} (level {skill.level}/5)" for skill, technology in skill_rows]

        profile_summary = "Experiences:\n" + ("\n".join(experience_lines) or "(none)") + "\n\n" "Projects:\n" + ("\n".join(project_lines) or "(none)") + "\n\n" "Skills:\n" + ("\n".join(skill_lines) or "(none)")

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a career advisor performing a gap analysis between a candidate's "
                    "profile and a target role. Reply with ONLY a JSON object, no markdown fences, "
                    'shaped exactly as {"matchScore": <integer 0-100>, "strengths": [<string>, ...], '
                    '"gaps": [<string>, ...], "recommendations": [<string>, ...]}. Keep each list to '
                    "3-6 concise items."
                ),
            },
            {"role": "user", "content": f"Target role: {target_role}\n\n{profile_summary}"},
        ]
        message = await self._complete(user_id, "career_analyze_profile", messages, {"targetRole": target_role})
        return _parse_analysis(message)
