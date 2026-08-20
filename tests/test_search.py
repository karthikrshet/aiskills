"""Tests for the ranked skill search engine."""

from __future__ import annotations

from pathlib import Path

from aiskills.models import SkillMetadata
from aiskills.search import search_skills


def make_skill(name: str, description: str, tags: list[str], category: str) -> SkillMetadata:
    return SkillMetadata(
        name=name,
        description=description,
        version="0.1.0",
        category=category,
        tags=tags,
        risk="low",
        status="alpha",
        related_skills=[],
        path=Path(f"skills/{name}/SKILL.md"),
    )


def test_empty_query_returns_empty_list():
    skills = [make_skill("rag-architecture", "RAG system design", ["rag", "ai"], "ai/rag")]
    assert search_skills(skills, "") == []
    assert search_skills(skills, "   ") == []


def test_exact_name_match_ranks_highest():
    s1 = make_skill("rag-architecture", "Design RAG systems", ["rag", "ai"], "ai/rag")
    s2 = make_skill(
        "rag-evaluation", "Evaluate rag systems", ["rag-architecture", "eval"], "ai/evaluation"
    )
    s3 = make_skill(
        "agent-design", "Mentions rag-architecture in text", ["agent"], "ai/agent-design"
    )

    results = search_skills([s2, s3, s1], "rag-architecture")
    assert len(results) == 3
    assert results[0].name == "rag-architecture"


def test_tag_match_ranking():
    s1 = make_skill("tdd", "Test driven development", ["testing", "tdd"], "testing")
    s2 = make_skill("other-skill", "Mentions testing in description", ["code"], "discovery")

    results = search_skills([s2, s1], "testing")
    assert len(results) == 2
    assert results[0].name == "tdd"  # Tag match scores higher than description match


def test_no_matches_returns_empty():
    s1 = make_skill("tdd", "Test driven development", ["testing"], "testing")
    assert search_skills([s1], "completely-unrelated-query") == []
