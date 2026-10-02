"""Filesystem path helpers for locating skills and project roots."""

from __future__ import annotations

import os
from pathlib import Path


def find_skills_root(custom_dir: Path | str | None = None) -> Path:
    """Locate the AISkills skills/ directory.

    Search order:
    1. Explicit custom_dir argument if provided
    2. AISKILLS_DIR environment variable
    3. The package's own skills/ directory (for development / installed package)
    4. Current working directory skills/
    """
    if custom_dir:
        return Path(custom_dir)

    env_dir = os.environ.get("AISKILLS_DIR")
    if env_dir:
        return Path(env_dir) / "skills"

    # When installed as a package, skills/ lives alongside pyproject.toml
    # Walk up from this file to find the project root containing skills
    this_file = Path(__file__).resolve()
    for parent in this_file.parents:
        candidate = parent / "skills"
        if candidate.is_dir() and any(candidate.rglob("SKILL.md")):
            return candidate

    # Fallback: cwd
    return Path.cwd() / "skills"


def find_project_root(custom_dir: Path | str | None = None) -> Path:
    """Walk up from cwd to find a git root or pyproject.toml."""
    if custom_dir:
        return Path(custom_dir)

    cwd = Path.cwd()
    for parent in [cwd, *cwd.parents]:
        if (parent / ".git").exists() or (parent / "pyproject.toml").exists():
            return parent
    return cwd
