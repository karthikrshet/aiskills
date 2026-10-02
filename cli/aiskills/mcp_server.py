"""Model Context Protocol (MCP) server for AISkills.

Exposes AISkills tools, resources, and prompt templates to MCP-compliant AI agents.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from aiskills import __version__
from aiskills.doctor import run_doctor
from aiskills.paths import find_project_root, find_skills_root
from aiskills.registry import SkillRegistry
from aiskills.validator import validate_all

try:
    from mcp.server.mcpserver import MCPServer
except ImportError:
    try:
        from mcp.server.fastmcp import FastMCP as MCPServer
    except ImportError:
        MCPServer = None


def is_mcp_available() -> bool:
    """Return True if the MCP SDK is installed and available."""
    return MCPServer is not None


# --- Core business logic helpers (independently testable) ---


def tool_list_skills(
    registry: SkillRegistry,
    category: str | None = None,
    risk: str | None = None,
) -> list[dict[str, object]]:
    """List skills discovered by the registry with optional filters."""
    skills = registry.all()
    if category:
        skills = [s for s in skills if s.category.lower() == category.lower()]
    if risk:
        skills = [s for s in skills if s.risk.lower() == risk.lower()]
    return [skill.to_dict() for skill in skills]


def tool_get_skill(registry: SkillRegistry, name: str) -> dict[str, object]:
    """Retrieve full skill metadata and raw markdown content."""
    skill = registry.get(name)
    if not skill:
        return {
            "found": False,
            "error": f"Skill '{name}' not found.",
            "available_skills": sorted(registry.names()),
        }

    raw_content = ""
    if skill.path and skill.path.exists():
        raw_content = skill.path.read_text(encoding="utf-8")

    return {
        "found": True,
        "metadata": skill.to_dict(),
        "content": raw_content,
    }


def tool_search_skills(registry: SkillRegistry, query: str) -> list[dict[str, object]]:
    """Search skills by keyword matching across names, tags, and descriptions."""
    matches = registry.search(query)
    return [skill.to_dict() for skill in matches]


def tool_validate_skills(skills_root: Path) -> dict[str, object]:
    """Validate all skills against the AISkills specification."""
    result = validate_all(skills_root)
    return {
        "is_valid": result.is_valid,
        "skill_count": result.skill_count,
        "pass_count": result.pass_count,
        "errors": [str(err) for err in result.errors],
        "warnings": [str(warn) for warn in result.warnings],
    }


def tool_run_doctor(project_root: Path, skills_root: Path) -> dict[str, object]:
    """Execute repository health checks."""
    report = run_doctor(project_root, skills_root)
    return {
        "ok_count": report.ok_count(),
        "warning_count": report.warning_count(),
        "error_count": report.error_count(),
        "has_errors": report.has_errors,
        "findings": [
            {"level": f.level, "check": f.check, "message": f.message} for f in report.findings
        ],
    }


def resource_skills_list(registry: SkillRegistry) -> str:
    """Return JSON string of available skills."""
    skills = [
        {
            "name": s.name,
            "category": s.category,
            "risk": s.risk,
            "status": s.status,
            "description": s.description.split("\n")[0].strip(),
        }
        for s in registry.all()
    ]
    return json.dumps(skills, indent=2)


def resource_skill(registry: SkillRegistry, name: str) -> str:
    """Return raw content of a skill's SKILL.md file."""
    skill = registry.get(name)
    if not skill or not skill.path or not skill.path.exists():
        return f"# Error\nSkill '{name}' not found."
    return skill.path.read_text(encoding="utf-8")


def resource_context(project_root: Path) -> str:
    """Return CONTEXT.md content for the project or guidance."""
    context_file = project_root / "CONTEXT.md"
    if context_file.exists():
        return context_file.read_text(encoding="utf-8")
    return (
        "# CONTEXT.md Missing\n\n"
        "No CONTEXT.md found at project root. Run `aiskills init` to generate one."
    )


def prompt_activate_skill(
    registry: SkillRegistry,
    skill_name: str,
    task_description: str = "",
) -> str:
    """Generate prompt instructions to activate and follow a specific skill."""
    skill = registry.get(skill_name)
    if not skill:
        return f"Skill '{skill_name}' was not found in the AISkills registry."

    content = ""
    if skill.path and skill.path.exists():
        content = skill.path.read_text(encoding="utf-8")

    task_block = f"**Target Task:**\n{task_description}\n\n" if task_description else ""

    return (
        f"# Activating AISkill: {skill.name} (v{skill.version})\n\n"
        f"**Category:** {skill.category}  |  **Risk:** {skill.risk}  |  **Status:** {skill.status}\n\n"
        f"{task_block}"
        f"## Skill Instructions\n\n"
        f"{content}\n\n"
        f"## Safety & Protocol\n"
        f"- Execute this skill phase by phase without skipping validation gates.\n"
        f"- If any action has high risk or requires human approval, pause and ask the user.\n"
    )


def prompt_workflow(project_root: Path, workflow_name: str) -> str:
    """Generate workflow instructions from the workflows/ directory."""
    workflows_dir = project_root / "workflows"
    workflow_md = workflows_dir / workflow_name / "README.md"

    if workflow_md.exists():
        content = workflow_md.read_text(encoding="utf-8")
        return (
            f"# AISkills Engineering Workflow: {workflow_name}\n\n"
            f"{content}\n\n"
            f"Follow all human review gates and verify testing gates before completing the task."
        )

    available = []
    if workflows_dir.exists():
        available = [d.name for d in workflows_dir.iterdir() if d.is_dir()]

    return (
        f"Workflow '{workflow_name}' not found. Available workflows: {', '.join(sorted(available))}"
    )


# --- MCP Server Factory ---


def create_mcp_server(
    skills_root: Path | None = None,
    project_root: Path | None = None,
) -> Any:
    """Create and configure an MCPServer instance for AISkills.

    Raises RuntimeError if the 'mcp' dependency is not installed.
    """
    if MCPServer is None:
        raise RuntimeError(
            "The 'mcp' package is required to run the MCP server. "
            "Install it with: pip install 'aiskills[mcp]'"
        )

    resolved_skills_root = find_skills_root(skills_root)
    resolved_project_root = find_project_root(project_root)
    registry = SkillRegistry(resolved_skills_root)

    server = MCPServer(
        name="aiskills",
        instructions=(
            "AISkills MCP Server: Reusable engineering workflows, skills, "
            "and health checks for AI coding agents."
        ),
        version=__version__,
    )

    # Register Tools
    @server.tool()
    def list_skills(
        category: str | None = None,
        risk: str | None = None,
    ) -> list[dict[str, object]]:
        """List available AISkills with metadata, optionally filtered by category or risk level."""
        return tool_list_skills(registry, category=category, risk=risk)

    @server.tool()
    def get_skill(name: str) -> dict[str, object]:
        """Retrieve full details, metadata, and markdown workflow content for a skill by name."""
        return tool_get_skill(registry, name)

    @server.tool()
    def search_skills(query: str) -> list[dict[str, object]]:
        """Search skills by keyword matching across names, tags, categories, and descriptions."""
        return tool_search_skills(registry, query)

    @server.tool()
    def validate_skills(skills_dir: str | None = None) -> dict[str, object]:
        """Validate all skills in the library or target directory against the AISkills specification."""
        target_root = Path(skills_dir) if skills_dir else resolved_skills_root
        return tool_validate_skills(target_root)

    @server.tool()
    def check_doctor(project_dir: str | None = None) -> dict[str, object]:
        """Run repository health checks for AGENTS.md, CONTEXT.md, and skills hygiene."""
        target_project = Path(project_dir) if project_dir else resolved_project_root
        return tool_run_doctor(target_project, resolved_skills_root)

    # Register Resources
    @server.resource("skills://list")
    def get_skills_catalog() -> str:
        """Catalog of all discovered skills with categories and descriptions."""
        return resource_skills_list(registry)

    @server.resource("skill://{name}")
    def get_skill_by_uri(name: str) -> str:
        """Full Markdown instructions for a specific skill."""
        return resource_skill(registry, name)

    @server.resource("context://current")
    def get_current_context() -> str:
        """Current project context from CONTEXT.md."""
        return resource_context(resolved_project_root)

    # Register Prompts
    @server.prompt()
    def activate(skill_name: str, task_description: str = "") -> str:
        """Activate a skill to guide an AI agent step-by-step through a specific engineering task."""
        return prompt_activate_skill(registry, skill_name, task_description)

    @server.prompt()
    def run_workflow(workflow_name: str) -> str:
        """Load an engineering workflow pipeline (e.g. feature-development, bug-fixing, rag-development)."""
        return prompt_workflow(resolved_project_root, workflow_name)

    return server


def run_mcp_server(
    transport: str = "stdio",
    skills_root: Path | None = None,
    project_root: Path | None = None,
    **kwargs: Any,
) -> None:
    """Create and start the AISkills MCP server."""
    server = create_mcp_server(skills_root=skills_root, project_root=project_root)
    server.run(transport=transport, **kwargs)
