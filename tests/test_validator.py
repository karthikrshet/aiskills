"""Tests for the skill validator."""

from __future__ import annotations

from pathlib import Path

import pytest

from aiskills.validator import validate_all, _validate_skill_file


MINIMAL_VALID_SKILL = """\
---
name: test-skill
description: |
  Use this skill when you need to test the validator. It is specifically
  designed for automated testing of the AISkills validation logic.
version: "0.1.0"
category: discovery
tags: [testing, validator]
risk: low
status: alpha
---

## Purpose

This is a test skill for the AISkills validator test suite.

## When to Use

- When writing tests for the validator
- When testing SKILL.md format compliance
- When validating frontmatter parsing

## When Not to Use

- In production skill libraries
- As a real engineering skill

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Test input | ✅ | Test input description |

## Preconditions

- [ ] Test environment is set up

## Workflow

### Step 1: Do the test thing

**Inspect:** Something to inspect.

**Produce:** Something to produce.

## Decision Points

| Condition | Tier | Action |
|-----------|------|--------|
| Condition A | Consult | Do something |
| Condition B | Approve | Do something else |

## Safety Constraints

- Never do unsafe things
- Always be safe
- Never skip this section

## Expected Output

- A test output

## Validation

- [ ] Validation check 1
- [ ] Validation check 2
- [ ] Validation check 3

## Failure Handling

| Failure | What to do |
|---------|------------|
| Failure A | Do this |
| Failure B | Do that |

## Examples

### Example 1

Input: test input. Agent actions: step 1, step 2. Output: test output.

## Related Skills

- repository-discovery — run before this skill
"""


def write_skill(tmp_path: Path, content: str, name: str = "test-skill") -> Path:
    """Write a SKILL.md to a temp directory."""
    skill_dir = tmp_path / name
    skill_dir.mkdir(parents=True, exist_ok=True)
    skill_file = skill_dir / "SKILL.md"
    skill_file.write_text(content, encoding="utf-8")
    return skill_file


class TestValidateSkillFile:
    def test_valid_skill_passes(self, tmp_path):
        skill_file = write_skill(tmp_path, MINIMAL_VALID_SKILL)
        seen_names = {}
        errors, warnings = _validate_skill_file(skill_file, seen_names)
        assert errors == [], f"Unexpected errors: {errors}"

    def test_missing_frontmatter_fails(self, tmp_path):
        content = "# Just a markdown file without frontmatter\n"
        skill_file = write_skill(tmp_path, content)
        seen_names = {}
        errors, warnings = _validate_skill_file(skill_file, seen_names)
        assert any("frontmatter" in e.message.lower() for e in errors)

    def test_missing_name_fails(self, tmp_path):
        content = MINIMAL_VALID_SKILL.replace("name: test-skill\n", "")
        skill_file = write_skill(tmp_path, content)
        seen_names = {}
        errors, warnings = _validate_skill_file(skill_file, seen_names)
        assert any("name" in e.message.lower() for e in errors)

    def test_invalid_name_format_fails(self, tmp_path):
        # Name starts with a number — invalid
        content = MINIMAL_VALID_SKILL.replace("name: test-skill", "name: 1badname")
        skill_file = write_skill(tmp_path, content)
        seen_names = {}
        errors, warnings = _validate_skill_file(skill_file, seen_names)
        assert any("name" in e.message.lower() for e in errors)

    def test_invalid_name_uppercase_fails(self, tmp_path):
        content = MINIMAL_VALID_SKILL.replace("name: test-skill", "name: TestSkill")
        skill_file = write_skill(tmp_path, content)
        seen_names = {}
        errors, warnings = _validate_skill_file(skill_file, seen_names)
        assert any("name" in e.message.lower() for e in errors)

    def test_missing_description_fails(self, tmp_path):
        content = MINIMAL_VALID_SKILL.replace(
            "description: |\n  Use this skill when you need to test the validator. It is specifically\n  designed for automated testing of the AISkills validation logic.\n",
            "",
        )
        skill_file = write_skill(tmp_path, content)
        seen_names = {}
        errors, warnings = _validate_skill_file(skill_file, seen_names)
        assert any("description" in e.message.lower() for e in errors)

    def test_invalid_version_fails(self, tmp_path):
        content = MINIMAL_VALID_SKILL.replace('version: "0.1.0"', 'version: "v0.1"')
        skill_file = write_skill(tmp_path, content)
        seen_names = {}
        errors, warnings = _validate_skill_file(skill_file, seen_names)
        assert any("version" in e.message.lower() for e in errors)

    def test_invalid_category_fails(self, tmp_path):
        content = MINIMAL_VALID_SKILL.replace("category: discovery", "category: invalid-category")
        skill_file = write_skill(tmp_path, content)
        seen_names = {}
        errors, warnings = _validate_skill_file(skill_file, seen_names)
        assert any("category" in e.message.lower() for e in errors)

    def test_valid_ai_category_passes(self, tmp_path):
        content = MINIMAL_VALID_SKILL.replace("category: discovery", "category: ai/rag")
        skill_file = write_skill(tmp_path, content)
        seen_names = {}
        errors, warnings = _validate_skill_file(skill_file, seen_names)
        assert not any("category" in e.message.lower() for e in errors)

    def test_empty_tags_fails(self, tmp_path):
        content = MINIMAL_VALID_SKILL.replace("tags: [testing, validator]", "tags: []")
        skill_file = write_skill(tmp_path, content)
        seen_names = {}
        errors, warnings = _validate_skill_file(skill_file, seen_names)
        assert any("tag" in e.message.lower() for e in errors)

    def test_invalid_risk_fails(self, tmp_path):
        content = MINIMAL_VALID_SKILL.replace("risk: low", "risk: critical")
        skill_file = write_skill(tmp_path, content)
        seen_names = {}
        errors, warnings = _validate_skill_file(skill_file, seen_names)
        assert any("risk" in e.message.lower() for e in errors)

    def test_invalid_status_fails(self, tmp_path):
        content = MINIMAL_VALID_SKILL.replace("status: alpha", "status: draft")
        skill_file = write_skill(tmp_path, content)
        seen_names = {}
        errors, warnings = _validate_skill_file(skill_file, seen_names)
        assert any("status" in e.message.lower() for e in errors)

    def test_missing_required_section_fails(self, tmp_path):
        content = MINIMAL_VALID_SKILL.replace("## Purpose\n", "")
        skill_file = write_skill(tmp_path, content)
        seen_names = {}
        errors, warnings = _validate_skill_file(skill_file, seen_names)
        assert any("Purpose" in e.message for e in errors)

    def test_all_required_sections_missing_fails(self, tmp_path):
        # Only frontmatter, no body sections
        content = """\
---
name: test-skill
description: |
  Test description for the validator — long enough to pass the length check.
version: "0.1.0"
category: discovery
tags: [testing]
risk: low
status: alpha
---

Some content without required sections.
"""
        skill_file = write_skill(tmp_path, content)
        seen_names = {}
        errors, warnings = _validate_skill_file(skill_file, seen_names)
        # Should fail for all 13 missing sections
        section_errors = [e for e in errors if "Missing required Markdown section" in e.message]
        assert len(section_errors) == 13

    def test_placeholder_content_warns(self, tmp_path):
        content = MINIMAL_VALID_SKILL + "\nTODO: add more content here\n"
        skill_file = write_skill(tmp_path, content)
        seen_names = {}
        errors, warnings = _validate_skill_file(skill_file, seen_names)
        assert any("placeholder" in w.message.lower() for w in warnings)

    def test_duplicate_name_fails(self, tmp_path):
        skill_file = write_skill(tmp_path, MINIMAL_VALID_SKILL, "test-skill-1")
        seen_names = {"test-skill": tmp_path / "other" / "SKILL.md"}
        errors, warnings = _validate_skill_file(skill_file, seen_names)
        assert any("duplicate" in e.message.lower() for e in errors)


class TestValidateAll:
    def test_valid_skills_pass(self, tmp_path):
        write_skill(tmp_path, MINIMAL_VALID_SKILL, "skill-one")

        # Second valid skill with different name
        skill2 = MINIMAL_VALID_SKILL.replace("name: test-skill", "name: skill-two")
        write_skill(tmp_path, skill2, "skill-two")

        result = validate_all(tmp_path)
        assert result.is_valid
        assert result.skill_count == 2
        assert result.pass_count == 2

    def test_empty_directory_returns_zero(self, tmp_path):
        result = validate_all(tmp_path)
        assert result.skill_count == 0
        assert result.is_valid

    def test_nonexistent_directory_returns_error(self, tmp_path):
        result = validate_all(tmp_path / "nonexistent")
        assert not result.is_valid

    def test_invalid_skill_counted(self, tmp_path):
        write_skill(tmp_path, "# no frontmatter", "bad-skill")
        result = validate_all(tmp_path)
        assert result.failed_count == 1
        assert not result.is_valid
