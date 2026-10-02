# Model Context Protocol (MCP) Adapter

This guide explains how to connect AISkills to any AI client supporting the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) — such as Claude Desktop, Cursor, Zed, Windsurf, Claude Code, and Cline.

---

## Overview

The AISkills MCP server exposes engineering workflows, skill search, validation, and repository doctor diagnostics dynamically to AI agents via standard MCP:

- **Tools**: `list_skills`, `get_skill`, `search_skills`, `validate_skills`, `check_doctor`
- **Resources**: `skills://list`, `skill://{name}`, `context://current`
- **Prompts**: `activate(skill_name, task_description)`, `run_workflow(workflow_name)`

---

## Installation

Install AISkills with the `mcp` extra:

```bash
pip install "aiskills[mcp]"
```

Verify the installation:

```bash
aiskills mcp --help
```

---

## Client Configurations

### 1. Claude Desktop

Add AISkills to your Claude Desktop configuration file:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "aiskills": {
      "command": "aiskills",
      "args": ["mcp"]
    }
  }
}
```

If running within a specific project directory or virtual environment:

```json
{
  "mcpServers": {
    "aiskills": {
      "command": "/path/to/venv/bin/python",
      "args": [
        "-m", "aiskills", "mcp",
        "--project-dir", "/path/to/your/project"
      ]
    }
  }
}
```

---

### 2. Cursor

Add AISkills to `.cursor/mcp.json` in your workspace or in Cursor Settings > Features > MCP:

```json
{
  "mcpServers": {
    "aiskills": {
      "command": "aiskills",
      "args": ["mcp"]
    }
  }
}
```

---

### 3. Cline (VS Code Extension)

In Cline Settings > MCP Servers:

```json
{
  "mcpServers": {
    "aiskills": {
      "command": "aiskills",
      "args": ["mcp"],
      "disabled": false,
      "autoApprove": [
        "list_skills",
        "get_skill",
        "search_skills",
        "validate_skills",
        "check_doctor"
      ]
    }
  }
}
```

---

### 4. Zed

In `~/.config/zed/settings.json`:

```json
{
  "context_servers": {
    "aiskills": {
      "command": {
        "path": "aiskills",
        "args": ["mcp"]
      }
    }
  }
}
```

---

### 5. Running as SSE / Network Service

For distributed setups or containerized environments, run AISkills over Server-Sent Events (SSE):

```bash
aiskills mcp --transport sse --host 127.0.0.1 --port 8000
```

---

## What MCP Exposes to the Agent

### Tools

| Tool | Parameters | Description |
|------|------------|-------------|
| `list_skills` | `category` (optional), `risk` (optional) | Returns metadata for all discovered skills |
| `get_skill` | `name` (required) | Returns metadata and full Markdown instructions of `SKILL.md` |
| `search_skills` | `query` (required) | Searches skill library by keyword across name, tags, and description |
| `validate_skills` | `skills_dir` (optional) | Validates skills against the 13-section AISkills schema |
| `check_doctor` | `project_dir` (optional) | Runs repository health checks (`AGENTS.md`, `CONTEXT.md`, hygiene) |

### Resources

| Resource URI | Description |
|--------------|-------------|
| `skills://list` | JSON list of all available skill names, categories, and descriptions |
| `skill://{name}` | Full text of `SKILL.md` for direct context injection |
| `context://current` | Returns project `CONTEXT.md` content |

### Prompts

| Prompt | Parameters | Description |
|--------|------------|-------------|
| `activate` | `skill_name`, `task_description` | Structures a task according to the selected skill's phases and safety rules |
| `run_workflow` | `workflow_name` | Loads an end-to-end engineering pipeline (`feature-development`, `bug-fixing`, etc.) |

---

## Security & Human Approval Gates

- All skills marked with `risk: high` enforce explicit human review gates before destructive operations.
- The AISkills MCP server operates locally and does not transmit code or telemetry to external servers.
- Read permissions are confined to the repository and skills directory.

---

*AISkills v0.1.0 — Model Context Protocol Adapter Guide*
