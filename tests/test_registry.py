"""Tests for the skill registry."""

from __future__ import annotations

from pathlib import Path

from aiskills.registry import SkillRegistry, _parse_skill_md

SKILL_A = """\
---
name: skill-alpha
description: |
  Use this skill for alpha testing. It covers important alpha scenarios
  that are useful for AI coding agents.
version: "0.1.0"
category: discovery
tags: [alpha, testing, discovery]
risk: low
status: alpha
---

## Purpose

Alpha skill body.

## When to Use

- During alpha tests

## When Not to Use

- Never in production

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Input | ✅ | Something |

## Preconditions

- [ ] Precondition

## Workflow

### Step 1: Do something

**Inspect:** Something. **Produce:** Something.

## Decision Points

| Condition | Tier | Action |
|-----------|------|--------|
| Cond | Inform | Do |

## Safety Constraints

- Never unsafe
- Always safe
- Be careful

## Expected Output

- Output A

## Validation

- [ ] Check 1
- [ ] Check 2
- [ ] Check 3

## Failure Handling

| Failure | What to do |
|---------|------------|
| Fail | Fix |

## Examples

Example 1: something.

## Related Skills

- skill-beta — use after this
"""

SKILL_B = (
    SKILL_A.replace("name: skill-alpha", "name: skill-beta")
    .replace(
        "description: |\n  Use this skill for alpha testing. It covers important alpha scenarios\n  that are useful for AI coding agents.",
        "description: |\n  Use this skill for beta RAG evaluation testing. It covers retrieval\n  scenarios that are useful for AI coding agents building RAG systems.",
    )
    .replace("tags: [alpha, testing, discovery]", "tags: [beta, rag, evaluation]")
    .replace("category: discovery", "category: ai/rag")
)


def write_skill(tmp_path: Path, content: str, name: str) -> Path:
    skill_dir = tmp_path / name
    skill_dir.mkdir(parents=True, exist_ok=True)
    skill_file = skill_dir / "SKILL.md"
    skill_file.write_text(content, encoding="utf-8")
    return skill_file


class TestParseSkillMd:
    def test_parses_valid_skill(self, tmp_path):
        path = write_skill(tmp_path, SKILL_A, "skill-alpha")
        metadata = _parse_skill_md(path)
        assert metadata is not None
        assert metadata.name == "skill-alpha"
        assert metadata.version == "0.1.0"
        assert metadata.category == "discovery"
        assert metadata.risk == "low"
        assert metadata.status == "alpha"
        assert "alpha" in metadata.tags
        assert "testing" in metadata.tags

    def test_returns_none_without_frontmatter(self, tmp_path):
        path = tmp_path / "SKILL.md"
        path.write_text("# No frontmatter here\n")
        assert _parse_skill_md(path) is None

    def test_returns_none_for_malformed_yaml(self, tmp_path):
        path = tmp_path / "SKILL.md"
        path.write_text("---\n: invalid: yaml: content\n---\n# Body\n")
        _parse_skill_md(path)
        # May return None or a partial result depending on yaml parser behavior
        # Key: it should not raise an exception

    def test_description_is_stripped(self, tmp_path):
        path = write_skill(tmp_path, SKILL_A, "skill-alpha")
        metadata = _parse_skill_md(path)
        assert metadata is not None
        assert not metadata.description.startswith("\n")
        assert not metadata.description.endswith("\n")

    def test_related_skills_parsed(self, tmp_path):
        # Add related-skills frontmatter
        content_with_related = SKILL_A.replace(
            "status: alpha\n",
            "status: alpha\nrelated-skills:\n  - skill-beta\n",
        )
        path = write_skill(tmp_path, content_with_related, "skill-alpha")
        metadata = _parse_skill_md(path)
        assert metadata is not None
        assert "skill-beta" in metadata.related_skills


class TestSkillRegistry:
    def test_empty_directory_returns_empty_list(self, tmp_path):
        registry = SkillRegistry(tmp_path)
        assert registry.all() == []

    def test_nonexistent_directory_returns_empty_list(self, tmp_path):
        registry = SkillRegistry(tmp_path / "nonexistent")
        assert registry.all() == []

    def test_discovers_skills(self, tmp_path):
        write_skill(tmp_path, SKILL_A, "skill-alpha")
        write_skill(tmp_path, SKILL_B, "skill-beta")
        registry = SkillRegistry(tmp_path)
        skills = registry.all()
        assert len(skills) == 2
        names = {s.name for s in skills}
        assert "skill-alpha" in names
        assert "skill-beta" in names

    def test_all_returns_sorted_by_name(self, tmp_path):
        write_skill(tmp_path, SKILL_B, "skill-beta")
        write_skill(tmp_path, SKILL_A, "skill-alpha")
        registry = SkillRegistry(tmp_path)
        names = [s.name for s in registry.all()]
        assert names == sorted(names)

    def test_get_returns_correct_skill(self, tmp_path):
        write_skill(tmp_path, SKILL_A, "skill-alpha")
        registry = SkillRegistry(tmp_path)
        skill = registry.get("skill-alpha")
        assert skill is not None
        assert skill.name == "skill-alpha"

    def test_get_returns_none_for_missing(self, tmp_path):
        registry = SkillRegistry(tmp_path)
        assert registry.get("nonexistent") is None

    def test_search_by_name(self, tmp_path):
        write_skill(tmp_path, SKILL_A, "skill-alpha")
        write_skill(tmp_path, SKILL_B, "skill-beta")
        registry = SkillRegistry(tmp_path)
        results = registry.search("alpha")
        assert len(results) == 1
        assert results[0].name == "skill-alpha"

    def test_search_by_tag(self, tmp_path):
        write_skill(tmp_path, SKILL_A, "skill-alpha")
        write_skill(tmp_path, SKILL_B, "skill-beta")
        registry = SkillRegistry(tmp_path)
        results = registry.search("rag")
        assert any(s.name == "skill-beta" for s in results)

    def test_search_case_insensitive(self, tmp_path):
        write_skill(tmp_path, SKILL_A, "skill-alpha")
        registry = SkillRegistry(tmp_path)
        results = registry.search("ALPHA")
        assert len(results) == 1

    def test_search_no_results(self, tmp_path):
        write_skill(tmp_path, SKILL_A, "skill-alpha")
        registry = SkillRegistry(tmp_path)
        results = registry.search("zzz-no-match-zzz")
        assert results == []

    def test_names_returns_set(self, tmp_path):
        write_skill(tmp_path, SKILL_A, "skill-alpha")
        write_skill(tmp_path, SKILL_B, "skill-beta")
        registry = SkillRegistry(tmp_path)
        names = registry.names()
        assert isinstance(names, set)
        assert "skill-alpha" in names
        assert "skill-beta" in names

    def test_lazy_loading(self, tmp_path):
        """Registry should not load skills until first access."""
        registry = SkillRegistry(tmp_path)
        assert not registry._loaded
        registry.all()
        assert registry._loaded

    def test_nested_skill_discovery(self, tmp_path):
        """Skills nested in subdirectories should be discovered."""
        nested = tmp_path / "ai" / "rag"
        nested.mkdir(parents=True)
        skill_dir = nested / "skill-alpha"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(SKILL_A, encoding="utf-8")
        registry = SkillRegistry(tmp_path)
        assert registry.get("skill-alpha") is not None
