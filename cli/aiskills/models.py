"""Data models for AISkills metadata and validation."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class SkillMetadata:
    """Parsed metadata for an individual AISkills skill."""

    name: str
    description: str
    version: str
    category: str
    tags: list[str]
    risk: str
    status: str
    related_skills: list[str] = field(default_factory=list)
    path: Path = field(default_factory=Path)

    def to_dict(self) -> dict[str, object]:
        """Convert metadata to dictionary format."""
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "category": self.category,
            "tags": self.tags,
            "risk": self.risk,
            "status": self.status,
            "related_skills": self.related_skills,
            "path": str(self.path),
        }
