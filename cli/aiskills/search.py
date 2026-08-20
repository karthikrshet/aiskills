"""Search engine for the AISkills skill catalog."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aiskills.models import SkillMetadata


def search_skills(skills: list[SkillMetadata], query: str) -> list[SkillMetadata]:
    """Search and rank skills against a query.

    Ranking Priority:
    1. Exact name match (Score: 100)
    2. Name substring match (Score: 75)
    3. Exact tag match (Score: 50)
    4. Tag substring match (Score: 35)
    5. Category match (Score: 20)
    6. Description match (Score: 10)
    """
    if not query or not query.strip():
        return []

    q = query.strip().lower()
    scored_results: list[tuple[int, str, SkillMetadata]] = []

    for skill in skills:
        name_lower = skill.name.lower()
        score = 0

        if name_lower == q:
            score += 100
        elif q in name_lower:
            score += 75

        for tag in skill.tags:
            tag_lower = tag.lower()
            if tag_lower == q:
                score += 50
            elif q in tag_lower:
                score += 35

        if q in skill.category.lower():
            score += 20

        if q in skill.description.lower():
            score += 10

        if score > 0:
            # Sort by (-score, skill.name) to ensure deterministic descending order
            scored_results.append((score, skill.name, skill))

    scored_results.sort(key=lambda item: (-item[0], item[1]))
    return [item[2] for item in scored_results]
