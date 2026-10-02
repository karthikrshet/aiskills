"""Tests for the AISkills Model Context Protocol (MCP) server and CLI."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest
from aiskills.main import cli
from aiskills.mcp_server import (
    create_mcp_server,
    is_mcp_available,
    prompt_activate_skill,
    prompt_workflow,
    resource_context,
    resource_skill,
    resource_skills_list,
    tool_get_skill,
    tool_list_skills,
    tool_run_doctor,
    tool_search_skills,
    tool_validate_skills,
)
from aiskills.registry import SkillRegistry
from click.testing import CliRunner


@pytest.fixture
def sample_skills_root(tmp_path: Path) -> Path:
    """Create a temporary skills directory with sample skills."""
    skills_root = tmp_path / "skills"
    skills_root.mkdir()

    # Skill 1: low risk, discovery
    s1_dir = skills_root / "discovery" / "sample-discovery"
    s1_dir.mkdir(parents=True)
    (s1_dir / "SKILL.md").write_text(
        "---\n"
        "name: sample-discovery\n"
        "description: Explore codebase and architecture\n"
        'version: "0.1.0"\n'
        "category: discovery\n"
        "tags: [discovery, architecture]\n"
        "risk: low\n"
        "status: stable\n"
        "---\n\n"
        "# Sample Discovery\n\n"
        "## Purpose\nExplore code.\n\n"
        "## When to Use\nAt start of task.\n\n"
        "## When Not to Use\nWhen known.\n\n"
        "## Inputs\nNone.\n\n"
        "## Preconditions\nRepo cloned.\n\n"
        "## Workflow\nRun tree.\n\n"
        "## Decision Points\nScope.\n\n"
        "## Safety Constraints\nRead-only.\n\n"
        "## Expected Output\nSummary.\n\n"
        "## Validation\nCheck files.\n\n"
        "## Failure Handling\nReport missing.\n\n"
        "## Examples\nSee docs.\n\n"
        "## Related Skills\nNone.\n",
        encoding="utf-8",
    )

    # Skill 2: high risk, security
    s2_dir = skills_root / "security" / "sample-security"
    s2_dir.mkdir(parents=True)
    (s2_dir / "SKILL.md").write_text(
        "---\n"
        "name: sample-security\n"
        "description: Security audit checks\n"
        'version: "0.1.0"\n'
        "category: security\n"
        "tags: [security, audit]\n"
        "risk: high\n"
        "status: beta\n"
        "---\n\n"
        "# Sample Security\n\n"
        "Audit instructions.\n",
        encoding="utf-8",
    )

    return skills_root


@pytest.fixture
def sample_project_root(tmp_path: Path, sample_skills_root: Path) -> Path:
    """Create a sample project structure with CONTEXT.md and workflows."""
    project_root = tmp_path / "project"
    project_root.mkdir()

    # CONTEXT.md
    (project_root / "CONTEXT.md").write_text(
        "# Test Project Context\n\nProject details for testing.",
        encoding="utf-8",
    )

    # Workflows
    wf_dir = project_root / "workflows" / "feature-development"
    wf_dir.mkdir(parents=True)
    (wf_dir / "README.md").write_text(
        "# Feature Development Workflow\n\nStep 1: Discover\nStep 2: Plan",
        encoding="utf-8",
    )

    return project_root


class TestMCPBusinessLogic:
    def test_tool_list_skills(self, sample_skills_root: Path):
        registry = SkillRegistry(sample_skills_root)
        all_skills = tool_list_skills(registry)
        assert len(all_skills) == 2

        # Filter by category
        discovery_skills = tool_list_skills(registry, category="discovery")
        assert len(discovery_skills) == 1
        assert discovery_skills[0]["name"] == "sample-discovery"

        # Filter by risk
        high_risk_skills = tool_list_skills(registry, risk="high")
        assert len(high_risk_skills) == 1
        assert high_risk_skills[0]["name"] == "sample-security"

    def test_tool_get_skill(self, sample_skills_root: Path):
        registry = SkillRegistry(sample_skills_root)

        # Existing skill
        result = tool_get_skill(registry, "sample-discovery")
        assert result["found"] is True
        assert result["metadata"]["name"] == "sample-discovery"
        assert "# Sample Discovery" in result["content"]

        # Missing skill
        missing = tool_get_skill(registry, "non-existent")
        assert missing["found"] is False
        assert "sample-discovery" in missing["available_skills"]

    def test_tool_search_skills(self, sample_skills_root: Path):
        registry = SkillRegistry(sample_skills_root)
        matches = tool_search_skills(registry, "audit")
        assert len(matches) == 1
        assert matches[0]["name"] == "sample-security"

    def test_tool_validate_skills(self, sample_skills_root: Path):
        result = tool_validate_skills(sample_skills_root)
        assert "is_valid" in result
        assert result["skill_count"] == 2

    def test_tool_run_doctor(self, sample_project_root: Path, sample_skills_root: Path):
        result = tool_run_doctor(sample_project_root, sample_skills_root)
        assert "ok_count" in result
        assert "findings" in result
        assert isinstance(result["findings"], list)

    def test_resource_skills_list(self, sample_skills_root: Path):
        registry = SkillRegistry(sample_skills_root)
        catalog = json.loads(resource_skills_list(registry))
        assert len(catalog) == 2
        names = [item["name"] for item in catalog]
        assert "sample-discovery" in names

    def test_resource_skill(self, sample_skills_root: Path):
        registry = SkillRegistry(sample_skills_root)
        content = resource_skill(registry, "sample-discovery")
        assert "# Sample Discovery" in content

        missing = resource_skill(registry, "ghost-skill")
        assert "Error" in missing

    def test_resource_context(self, sample_project_root: Path, tmp_path: Path):
        content = resource_context(sample_project_root)
        assert "Test Project Context" in content

        # Missing CONTEXT.md
        empty_root = tmp_path / "empty_proj"
        empty_root.mkdir()
        missing_content = resource_context(empty_root)
        assert "CONTEXT.md Missing" in missing_content

    def test_prompt_activate_skill(self, sample_skills_root: Path):
        registry = SkillRegistry(sample_skills_root)
        prompt = prompt_activate_skill(
            registry,
            "sample-discovery",
            task_description="Explore auth service",
        )
        assert "Activating AISkill: sample-discovery" in prompt
        assert "Explore auth service" in prompt
        assert "Safety & Protocol" in prompt

        missing = prompt_activate_skill(registry, "does-not-exist")
        assert "was not found" in missing

    def test_prompt_workflow(self, sample_project_root: Path):
        prompt = prompt_workflow(sample_project_root, "feature-development")
        assert "AISkills Engineering Workflow: feature-development" in prompt
        assert "Step 1: Discover" in prompt

        missing = prompt_workflow(sample_project_root, "ghost-workflow")
        assert "Workflow 'ghost-workflow' not found" in missing


class TestMCPServerFactory:
    def test_is_mcp_available_returns_bool(self):
        assert isinstance(is_mcp_available(), bool)

    def test_create_mcp_server_with_mock(self, sample_skills_root: Path, sample_project_root: Path):
        from unittest.mock import MagicMock

        mock_server = MagicMock()
        mock_server.name = "aiskills"
        mock_cls = MagicMock(return_value=mock_server)
        with patch("aiskills.mcp_server.MCPServer", mock_cls):
            server = create_mcp_server(
                skills_root=sample_skills_root,
                project_root=sample_project_root,
            )
            assert server.name == "aiskills"
            mock_cls.assert_called_once()

    @pytest.mark.skipif(not is_mcp_available(), reason="mcp optional dependency not installed")
    def test_create_mcp_server(self, sample_skills_root: Path, sample_project_root: Path):
        server = create_mcp_server(
            skills_root=sample_skills_root,
            project_root=sample_project_root,
        )
        assert server.name == "aiskills"

    def test_create_mcp_server_raises_when_missing(self):
        with patch("aiskills.mcp_server.MCPServer", None):
            with pytest.raises(RuntimeError) as exc_info:
                create_mcp_server()
            assert "The 'mcp' package is required" in str(exc_info.value)


class TestMCPCLI:
    def test_mcp_help(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["mcp", "--help"])
        assert result.exit_code == 0
        assert "Run the AISkills Model Context Protocol (MCP) server" in result.output
        assert "--transport" in result.output

    def test_mcp_missing_dependency_exit(self):
        runner = CliRunner()
        with patch("aiskills.mcp_server.is_mcp_available", return_value=False):
            result = runner.invoke(cli, ["mcp"])
            assert result.exit_code == 1
            assert "MCP support is not installed" in result.output
            assert 'pip install "aiskills[mcp]"' in result.output
