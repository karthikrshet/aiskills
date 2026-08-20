---
name: repository-discovery
description: |
  Use this skill to systematically explore an unfamiliar codebase before making
  any changes. Activates when starting work in an unknown repository, adding a
  new feature, debugging without prior context, or when no CONTEXT.md exists.
  Produces a grounded understanding of architecture, conventions, and constraints.
version: "0.1.0"
category: discovery
tags: [discovery, codebase, exploration, context, architecture, onboarding]
risk: low
status: alpha
related-skills:
  - requirements-analysis
  - implementation-planning
  - architecture-design
---

# Repository Discovery

## Purpose

AI coding agents frequently invent architecture by assumption. They generate code that contradicts existing patterns, imports libraries that aren't installed, or proposes designs incompatible with the actual codebase.

This skill provides a systematic methodology for exploring a repository and building accurate grounding context before any implementation work begins. It ensures the agent's mental model of the codebase matches reality.

## When to Use

- Starting work in a repository the agent has not seen before
- Before adding a feature to an existing codebase
- Before debugging a problem without prior context
- When `CONTEXT.md` does not exist or is incomplete
- Before proposing an architectural change
- When the agent's assumptions about the codebase need verification

## When Not to Use

- The agent has already completed discovery in the same session and the codebase is unchanged
- A complete and current `CONTEXT.md` exists and has been read
- The task is purely conceptual (no code changes required)

Use `requirements-analysis` after this skill to structure the task.

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Repository root path | ✅ | The directory to explore |
| Task description | optional | What the human wants to accomplish (helps focus discovery) |

## Preconditions

- [ ] Agent has file system read access to the repository
- [ ] Agent has not already made code modifications to the repository

## Workflow

### Step 1: Map the Top-Level Structure

**Inspect:**
- List all top-level directories and their apparent purpose
- Note the presence of key files: `README.md`, `CONTEXT.md`, `AGENTS.md`, `pyproject.toml`, `package.json`, `Cargo.toml`, `go.mod`, `Makefile`, `Dockerfile`, `docker-compose.yml`, `.github/`

**Produce:**
- A directory map: `directory/ — [inferred purpose]`
- Identification of primary language and build system

### Step 2: Read Grounding Files

**Inspect (in priority order):**
1. `CONTEXT.md` — project-level context (if present)
2. `AGENTS.md` — agent instructions (if present)
3. `README.md` — project overview
4. `.claude/settings.json`, `.cursorrules`, or equivalent — agent-specific config

**Produce:**
- Key facts extracted: purpose, architecture type, important conventions, known constraints

### Step 3: Analyze Project Configuration

**Inspect:**
- Dependency file (`pyproject.toml`, `package.json`, `requirements.txt`, `Cargo.toml`, `go.sum`)
- CI/CD configuration (`.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`)
- Linting/formatting config (`.ruff.toml`, `.eslintrc`, `.prettierrc`, `mypy.ini`)
- Environment template (`.env.example` — DO NOT read `.env`)

**Produce:**
- List of key dependencies with versions
- CI/CD pipeline summary
- Code quality standards in use

### Step 4: Explore Source Structure

**Inspect:**
- Primary source directory (`src/`, `lib/`, `app/`, or equivalent)
- Entry points: `main.py`, `index.ts`, `cmd/`, `app.py`
- Core modules/packages (one level deep)
- Test directory structure (`tests/`, `__tests__/`, `spec/`)

**Produce:**
- Source map: key modules and their responsibilities
- Test strategy: what is tested, how tests are organized

### Step 5: Sample Key Patterns

**Inspect (sample 2–3 files from different modules):**
- Coding style: naming conventions, type hints, docstrings
- Error handling patterns
- Logging patterns
- Configuration loading patterns
- Import structure

**Produce:**
- 3–5 key conventions the agent must follow when writing code for this project

### Step 6: Identify Constraints and Risks

**Inspect:**
- Any `TODO`, `FIXME`, `HACK`, or `DEPRECATED` comments in key files
- `SECURITY.md` or security-related configuration
- Any `legacy/`, `deprecated/`, or `do-not-touch/` directories

**Produce:**
- List of areas to avoid or handle with care
- Any files or modules marked as out of scope

## Decision Points

| Condition | Tier | Action |
|-----------|------|--------|
| `CONTEXT.md` exists but appears stale | Inform | Note the discrepancy; do not silently use stale context |
| `.env` file found with apparent real credentials | Approve | Report to human immediately; do not read or log the contents |
| Repository is extremely large (>500 files) | Consult | Ask human which subdirectories are relevant to the task |
| Contradictory information across files | Consult | Ask: "I found conflicting information about [topic]. Can you clarify?" |

## Safety Constraints

- Never read `.env`, `.env.local`, or files likely to contain credentials
- Never run executable files during discovery
- Never modify any file during this skill — this is read-only
- Do not access directories outside the repository root
- Treat `.gitignore`-d paths as potentially sensitive — inspect with care

## Expected Output

- A summary of key findings in the following structure:
  ```
  ## Repository Discovery Summary

  **Language/Framework:** [e.g., Python 3.11 / FastAPI]
  **Architecture:** [e.g., Layered monolith]
  **Entry points:** [list]
  **Key dependencies:** [list]
  **Test framework:** [e.g., pytest]
  **CI/CD:** [e.g., GitHub Actions — runs on PR]
  **Key conventions:** [list of 3–5 conventions]
  **Constraints/Risks:** [list]
  **Suggested next skill:** [skill name]
  ```
- Updated or created `CONTEXT.md` (ask human before overwriting an existing one)

## Validation

- [ ] All top-level directories are accounted for
- [ ] Primary language and framework identified with evidence
- [ ] At least 3 coding conventions documented
- [ ] CI/CD configuration status known
- [ ] No `.env` or credential files were read
- [ ] At least one constraint or risk identified (or explicitly confirmed none found)

## Failure Handling

| Failure | What to do |
|---------|------------|
| Repository root does not exist | Stop; ask human for correct path |
| No README, no CONTEXT.md, no package files | Proceed with deeper source inspection; note that grounding context is sparse |
| Source structure is opaque (generated files, minified code) | Report to human; ask for architecture description |
| Circular imports or broken build artifacts found | Note in output; do not attempt to fix during discovery |

## Examples

### Example 1: New feature in a Python/FastAPI project

**Input:** Python monorepo, task = "add email notification when a user's report is complete"

**Agent actions:**
1. Maps top-level: `src/`, `tests/`, `docs/`, `.github/`, `pyproject.toml`
2. Reads `CONTEXT.md` → learns it uses FastAPI + PostgreSQL + Celery for async tasks
3. Reads `pyproject.toml` → sees `celery`, `sendgrid` already in dependencies
4. Explores `src/notifications/` → finds existing `NotificationService` class
5. Samples `src/reports/service.py` → sees pattern: services are injected via FastAPI dependency injection
6. Notes: `legacy/` directory marked DEPRECATED; `src/billing/` handled by separate team

**Output:**
- Summary noting existing SendGrid integration, Celery setup, notification service
- Convention: use dependency injection, not direct class instantiation
- Constraint: do not modify `src/billing/`
- Recommended next skill: `requirements-analysis`

## Related Skills

- `requirements-analysis` — analyze and structure requirements after discovery
- `implementation-planning` — create an implementation plan grounded in discovery findings
- `architecture-design` — design architecture informed by what exists
- `context-engineering` — manage the context budget when the codebase is large
