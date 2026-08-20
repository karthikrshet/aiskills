"""Skill discovery and registry for AISkills."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

VALID_RISK = {"low", "medium", "high"}
VALID_STATUS = {"experimental", "alpha", "beta", "stable"}
VALID_CATEGORIES = {
    "discovery",
    "requirements",
    "architecture",
    "implementation",
    "testing",
    "debugging",
    "code-review",
    "security",
    "performance",
    "documentation",
    "ai/agent-design",
    "ai/rag",
    "ai/memory",
    "ai/prompting",
    "ai/context-engineering",
    "ai/evaluation",
    "ai/hallucination",
    "ai/guardrails",
    "ai/ai-security",
    "ai/production-ai",
}

NAME_PATTERN = re.compile(r"^[a-z][a-z0-9-]{1,48}[a-z0-9]$")


@dataclass
class SkillMetadata:
    """Parsed metadata for a single AISkills skill."""

    name: str
    description: str
    version: str
    category: str
    tags: list[str]
    risk: str
    status: str
    related_skills: list[str] = field(default_factory=list)
    path: Path = field(default_factory=Path)


class SkillRegistry:
    """Discover and index all skills in the AISkills library."""

    def __init__(self, skills_root: Path) -> None:
        self.skills_root = skills_root
        self._skills: dict[str, SkillMetadata] = {}
        self._loaded = False

    def _load(self) -> None:
        """Walk the skills directory and parse all SKILL.md files."""
        if self._loaded:
            return

        if not self.skills_root.exists():
            self._loaded = True
            return

        for skill_md in self.skills_root.rglob("SKILL.md"):
            try:
                metadata = _parse_skill_md(skill_md)
                if metadata is not None:
                    self._skills[metadata.name] = metadata
            except Exception:
                # Silently skip unparseable skills during discovery;
                # the validator will report detailed errors.
                pass

        self._loaded = True

    def all(self) -> list[SkillMetadata]:
        """Return all discovered skills sorted by name."""
        self._load()
        return sorted(self._skills.values(), key=lambda s: s.name)

    def get(self, name: str) -> SkillMetadata | None:
        """Return a skill by name, or None if not found."""
        self._load()
        return self._skills.get(name)

    def search(self, query: str) -> list[SkillMetadata]:
        """Search skills by keyword — checks name, description, and tags."""
        self._load()
        query_lower = query.lower()
        results = []
        for skill in self._skills.values():
            if (
                query_lower in skill.name.lower()
                or query_lower in skill.description.lower()
                or any(query_lower in tag.lower() for tag in skill.tags)
                or query_lower in skill.category.lower()
            ):
                results.append(skill)
        return sorted(results, key=lambda s: s.name)

    def names(self) -> set[str]:
        """Return the set of all skill names."""
        self._load()
        return set(self._skills.keys())


def _parse_skill_md(path: Path) -> SkillMetadata | None:
    """Parse a SKILL.md file and return a SkillMetadata object, or None on failure."""
    content = path.read_text(encoding="utf-8")

    if not content.startswith("---"):
        return None

    # Extract YAML frontmatter between the first two --- delimiters
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None

    frontmatter_str = parts[1].strip()
    try:
        fm = yaml.safe_load(frontmatter_str)
    except yaml.YAMLError:
        return None

    if not isinstance(fm, dict):
        return None

    name = fm.get("name", "")
    description = fm.get("description", "")
    version = fm.get("version", "")
    category = fm.get("category", "")
    tags = fm.get("tags", [])
    risk = fm.get("risk", "")
    status = fm.get("status", "")
    related_skills = fm.get("related-skills", [])

    # Normalize description (strip YAML block scalar whitespace)
    if isinstance(description, str):
        description = description.strip()

    return SkillMetadata(
        name=str(name),
        description=str(description),
        version=str(version),
        category=str(category),
        tags=list(tags) if tags else [],
        risk=str(risk),
        status=str(status),
        related_skills=list(related_skills) if related_skills else [],
        path=path,
    )
