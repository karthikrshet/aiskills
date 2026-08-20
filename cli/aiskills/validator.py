"""Skill schema validator for AISkills."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from aiskills.registry import (
    NAME_PATTERN,
    VALID_CATEGORIES,
    VALID_RISK,
    VALID_STATUS,
)

REQUIRED_SECTIONS = [
    "## Purpose",
    "## When to Use",
    "## When Not to Use",
    "## Inputs",
    "## Preconditions",
    "## Workflow",
    "## Decision Points",
    "## Safety Constraints",
    "## Expected Output",
    "## Validation",
    "## Failure Handling",
    "## Examples",
    "## Related Skills",
]

PLACEHOLDER_PATTERNS = [
    re.compile(r"\bTODO\b"),
    re.compile(r"\bFIXME\b"),
    re.compile(r"\[ADD CONTENT\]"),
    re.compile(r"\[YOUR .+?\]"),
    re.compile(r"Lorem ipsum"),
]

SEMVER_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")

MAX_BODY_LINES = 400


@dataclass
class ValidationError:
    """A single validation error or warning."""

    level: str  # "ERROR" or "WARNING"
    skill_path: Path
    message: str

    def __str__(self) -> str:
        relative = self.skill_path
        return f"[{self.level}] {relative}: {self.message}"


@dataclass
class ValidationResult:
    """Result of validating the full skills library."""

    errors: list[ValidationError] = field(default_factory=list)
    warnings: list[ValidationError] = field(default_factory=list)
    skill_count: int = 0
    pass_count: int = 0

    @property
    def failed_count(self) -> int:
        return self.skill_count - self.pass_count

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0


def validate_all(skills_root: Path) -> ValidationResult:
    """Validate all skills in the skills directory."""
    result = ValidationResult()

    if not skills_root.exists():
        result.errors.append(
            ValidationError("ERROR", skills_root, "Skills directory does not exist")
        )
        return result

    skill_files = list(skills_root.rglob("SKILL.md"))
    result.skill_count = len(skill_files)

    seen_names: dict[str, Path] = {}

    for skill_path in sorted(skill_files):
        skill_errors, skill_warnings = _validate_skill_file(skill_path, seen_names)

        result.errors.extend(skill_errors)
        result.warnings.extend(skill_warnings)

        if not skill_errors:
            result.pass_count += 1

    return result


def _validate_skill_file(
    path: Path, seen_names: dict[str, Path]
) -> tuple[list[ValidationError], list[ValidationError]]:
    """Validate a single SKILL.md file. Returns (errors, warnings)."""
    errors: list[ValidationError] = []
    warnings: list[ValidationError] = []

    def err(msg: str) -> None:
        errors.append(ValidationError("ERROR", path, msg))

    def warn(msg: str) -> None:
        warnings.append(ValidationError("WARNING", path, msg))

    # Read file
    try:
        content = path.read_text(encoding="utf-8")
    except OSError as e:
        err(f"Cannot read file: {e}")
        return errors, warnings

    # ── Frontmatter extraction ──────────────────────────────────────────────
    if not content.startswith("---"):
        err("File does not start with YAML frontmatter (---)")
        return errors, warnings

    parts = content.split("---", 2)
    if len(parts) < 3:
        err("Malformed frontmatter: missing closing ---")
        return errors, warnings

    frontmatter_str = parts[1].strip()
    body = parts[2]

    try:
        fm = yaml.safe_load(frontmatter_str)
    except yaml.YAMLError as e:
        err(f"Invalid YAML frontmatter: {e}")
        return errors, warnings

    if not isinstance(fm, dict):
        err("Frontmatter must be a YAML mapping")
        return errors, warnings

    # ── Required field validation ───────────────────────────────────────────

    # name
    name = fm.get("name")
    if not name:
        err("Missing required field: 'name'")
    elif not isinstance(name, str):
        err("Field 'name' must be a string")
    elif not NAME_PATTERN.match(name):
        err(f"Field 'name' has invalid format '{name}' — must be lowercase-hyphenated, 3–50 chars")
    else:
        if name in seen_names:
            err(f"Duplicate skill name '{name}' — also used by {seen_names[name]}")
        else:
            seen_names[name] = path

    # description
    description = fm.get("description")
    if not description:
        err("Missing required field: 'description'")
    elif not isinstance(description, str):
        err("Field 'description' must be a string")
    elif len(description.strip()) < 10:
        err("Field 'description' is too short (minimum 10 characters)")
    elif len(description.strip()) > 500:
        warn("Field 'description' exceeds 500 characters — agents may truncate it")

    # version
    version = fm.get("version")
    if not version:
        err("Missing required field: 'version'")
    elif not isinstance(version, str):
        err("Field 'version' must be a string (quoted in YAML, e.g., \"0.1.0\")")
    elif not SEMVER_PATTERN.match(str(version)):
        err(f"Field 'version' must be semantic version format (e.g., '0.1.0'), got '{version}'")

    # category
    category = fm.get("category")
    if not category:
        err("Missing required field: 'category'")
    elif str(category) not in VALID_CATEGORIES:
        err(
            f"Field 'category' has invalid value '{category}'. "
            f"Valid values: {sorted(VALID_CATEGORIES)}"
        )

    # tags
    tags = fm.get("tags")
    if tags is None:
        err("Missing required field: 'tags'")
    elif not isinstance(tags, list):
        err("Field 'tags' must be a YAML list")
    elif len(tags) == 0:
        err("Field 'tags' must have at least 1 tag")
    elif len(tags) > 10:
        warn(f"Field 'tags' has {len(tags)} tags — recommended maximum is 10")

    # risk
    risk = fm.get("risk")
    if not risk:
        err("Missing required field: 'risk'")
    elif str(risk) not in VALID_RISK:
        err(f"Field 'risk' must be one of {VALID_RISK}, got '{risk}'")

    # status
    status = fm.get("status")
    if not status:
        err("Missing required field: 'status'")
    elif str(status) not in VALID_STATUS:
        err(f"Field 'status' must be one of {VALID_STATUS}, got '{status}'")

    # ── Markdown body validation ────────────────────────────────────────────

    # Required sections
    for section in REQUIRED_SECTIONS:
        if section not in body:
            err(f"Missing required Markdown section: '{section}'")

    # Placeholder content
    for pattern in PLACEHOLDER_PATTERNS:
        if pattern.search(body):
            warn(f"Body contains placeholder content matching '{pattern.pattern}'")

    # Body length
    body_lines = body.count("\n")
    if body_lines > MAX_BODY_LINES:
        warn(
            f"Skill body is {body_lines} lines — exceeds recommended maximum of {MAX_BODY_LINES}. "
            "Consider moving detailed content to references/ subdirectory."
        )

    return errors, warnings
