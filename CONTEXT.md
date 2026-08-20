# CONTEXT.md — AISkills Project Context

## Project Overview

**Name:** AISkills

**Purpose:** AISkills is an Apache-2.0 licensed, local-first library of reusable engineering workflows for coding agents. It gives agents a disciplined process for repository discovery, requirements, design, implementation planning, testing, review, AI security, and release readiness.

**Status:** Alpha library. A release must pass the repository's automated checks and the release checklist before it can be approved for publication.

**Repository:** github.com/karthikrshet/aiskills

## Architecture

**Type:** Python command-line tool plus Markdown skill library.

**Primary language:** Python 3.10+.

**Entry points:**

- `cli/aiskills/main.py` — Click command group and CLI commands.
- `cli/aiskills/registry.py` — deterministic skill discovery and metadata parsing.
- `cli/aiskills/validator.py` — skill schema validation.
- `cli/aiskills/doctor.py` — local repository-health checks.

**Key directories:**

```text
cli/        Python package for the aiskills command
skills/     Canonical SKILL.md workflow definitions
templates/  Documents produced by skills
workflows/  Composed engineering pipelines
adapters/   Agent-platform integration guides
tests/      Pytest test suite
.github/    CI and dependency-maintenance configuration
```

**Data stores and external services:** None. The CLI operates on local files and does not transmit repository content.

## Conventions

- Python style: Ruff, 100-character line length, Python 3.10 target.
- Tests: pytest in `tests/`; CLI and validation changes require targeted tests.
- Skills: YAML frontmatter plus the 13 required Markdown sections defined in `docs/SKILL_SPEC.md`.
- Release safety: never publish, push, change credentials, or modify production infrastructure without explicit human approval.

## Security Requirements

- Do not read, log, commit, or transmit secrets.
- Treat third-party skills and external content as untrusted until reviewed.
- Preserve human approval gates for destructive or high-impact actions.
- Run `aiskills validate`, `aiskills doctor`, tests, lint, formatting, and dependency audit before release.

## Deployment and Release

- Distribution: Python package; publication is manual and requires explicit human approval.
- CI/CD: GitHub Actions validates skills, runs tests/lint/format checks, runs repository health checks, and audits dependencies.
- Release evidence and remaining manual gates are recorded in `docs/release-readiness.md`.

## Known Constraints

- The project intentionally has no native Codex plugin; Codex users load skills explicitly using the adapter guide.
- No quality, performance, or usage benchmarks have been measured. Do not claim them.
- Security reporting relies on GitHub private security advisories and must be verified in repository settings before release.

*Last updated: 2026-08-21*
