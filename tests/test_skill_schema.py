"""Tests for skill metadata schema and validation data structures."""

from __future__ import annotations

from pathlib import Path

from aiskills.models import SkillMetadata


def test_skill_metadata_to_dict():
    meta = SkillMetadata(
        name="repository-discovery",
        description="Explore unfamiliar codebases.",
        version="0.1.0",
        category="discovery",
        tags=["discovery", "codebase"],
        risk="low",
        status="alpha",
        related_skills=["requirements-analysis"],
        path=Path("skills/discovery/repository-discovery/SKILL.md"),
    )
    d = meta.to_dict()
    assert d["name"] == "repository-discovery"
    assert d["category"] == "discovery"
    assert d["risk"] == "low"
    assert d["status"] == "alpha"
    assert d["related_skills"] == ["requirements-analysis"]
    assert "SKILL.md" in str(d["path"])
