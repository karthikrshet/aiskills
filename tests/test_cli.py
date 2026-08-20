"""Tests for the CLI commands."""

from __future__ import annotations

from pathlib import Path

import pytest
from click.testing import CliRunner

from aiskills.main import cli


@pytest.fixture
def runner():
    return CliRunner()


class TestCLIVersion:
    def test_version_flag(self, runner):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "0.1.0" in result.output


class TestCLIInit:
    def test_init_creates_agents_md(self, runner, tmp_path):
        with runner.isolated_filesystem(temp_dir=tmp_path):
            result = runner.invoke(cli, ["init"])
            assert result.exit_code == 0
            assert Path("AGENTS.md").exists()

    def test_init_creates_context_md(self, runner, tmp_path):
        with runner.isolated_filesystem(temp_dir=tmp_path):
            result = runner.invoke(cli, ["init"])
            assert result.exit_code == 0
            assert Path("CONTEXT.md").exists()

    def test_init_does_not_overwrite_existing_agents_md(self, runner, tmp_path):
        with runner.isolated_filesystem(temp_dir=tmp_path):
            Path("AGENTS.md").write_text("# Existing AGENTS.md content")
            result = runner.invoke(cli, ["init"])
            assert result.exit_code == 0
            assert "AGENTS.md" in result.output
            # Content should not be overwritten
            assert Path("AGENTS.md").read_text() == "# Existing AGENTS.md content"

    def test_init_reports_created_files(self, runner, tmp_path):
        with runner.isolated_filesystem(temp_dir=tmp_path):
            result = runner.invoke(cli, ["init"])
            assert "AGENTS.md" in result.output
            assert "CONTEXT.md" in result.output


class TestCLIList:
    def test_list_with_empty_dir_shows_message(self, runner, tmp_path, monkeypatch):
        monkeypatch.setenv("AISKILLS_DIR", str(tmp_path))
        result = runner.invoke(cli, ["list"])
        assert result.exit_code == 0
        assert "No skills found" in result.output

    def test_list_with_skills_shows_table(self, runner, tmp_path, monkeypatch):
        """Create a minimal SKILL.md and verify it appears in list output."""
        monkeypatch.setenv("AISKILLS_DIR", str(tmp_path))
        skills_dir = tmp_path / "skills"
        skill_dir = skills_dir / "test-skill"
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text(
            """\
---
name: test-skill
description: |
  A test skill for CLI testing purposes. Used to verify list command.
version: "0.1.0"
category: discovery
tags: [testing]
risk: low
status: alpha
---

## Purpose
Test.
""",
            encoding="utf-8",
        )
        result = runner.invoke(cli, ["list"])
        assert result.exit_code == 0
        assert "test-skill" in result.output
        assert "discovery" in result.output


class TestCLISearch:
    def test_search_no_results(self, runner, tmp_path, monkeypatch):
        monkeypatch.setenv("AISKILLS_DIR", str(tmp_path))
        result = runner.invoke(cli, ["search", "zzz-no-match"])
        assert result.exit_code == 0
        assert "No skills found" in result.output


class TestCLIInfo:
    def test_info_missing_skill_exits_nonzero(self, runner, tmp_path, monkeypatch):
        monkeypatch.setenv("AISKILLS_DIR", str(tmp_path))
        result = runner.invoke(cli, ["info", "nonexistent-skill"])
        assert result.exit_code != 0
        assert "not found" in result.output.lower()


class TestCLIValidate:
    def test_validate_empty_directory_passes(self, runner, tmp_path, monkeypatch):
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()
        monkeypatch.setenv("AISKILLS_DIR", str(tmp_path))
        result = runner.invoke(cli, ["validate"])
        assert result.exit_code == 0

    def test_validate_invalid_skill_exits_nonzero(self, runner, tmp_path, monkeypatch):
        monkeypatch.setenv("AISKILLS_DIR", str(tmp_path))
        skills_dir = tmp_path / "skills"
        bad_skill_dir = skills_dir / "bad-skill"
        bad_skill_dir.mkdir(parents=True)
        (bad_skill_dir / "SKILL.md").write_text("# no frontmatter", encoding="utf-8")
        result = runner.invoke(cli, ["validate"])
        assert result.exit_code != 0

    def test_validate_with_skills_dir_option(self, runner, tmp_path):
        result = runner.invoke(cli, ["validate", "--skills-dir", str(tmp_path / "nonexistent")])
        assert result.exit_code != 0


class TestCLIDoctor:
    def test_doctor_with_both_files_present(self, runner, tmp_path, monkeypatch):
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()
        monkeypatch.setenv("AISKILLS_DIR", str(tmp_path))
        (tmp_path / "AGENTS.md").write_text("# Agent instructions")
        (tmp_path / "CONTEXT.md").write_text("# Project context - real content here", encoding="utf-8")
        result = runner.invoke(cli, ["doctor", "--project-dir", str(tmp_path)])
        assert result.exit_code == 0

    def test_doctor_warns_missing_agents_md(self, runner, tmp_path, monkeypatch):
        monkeypatch.setenv("AISKILLS_DIR", str(tmp_path))
        result = runner.invoke(cli, ["doctor", "--project-dir", str(tmp_path)])
        assert "AGENTS.md" in result.output
