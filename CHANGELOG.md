# Changelog

All notable changes to AISkills are documented here.

This project adheres to [Semantic Versioning](https://semver.org/).

---

## [Unreleased]

---

## [0.1.0] — 2026-08-21

**Status:** Alpha

### Added

#### Core
- Canonical skill specification (`docs/SKILL_SPEC.md`) defining the YAML frontmatter schema and required Markdown sections
- Architecture documentation (`docs/architecture.md`)
- Research and design rationale (`docs/research.md`)
- `AGENTS.md` — instructions for AI coding agents on using AISkills
- `CONTEXT.md` — template for repositories to define project context

#### Skills (14 initial)
- `repository-discovery` — systematic codebase exploration before changes
- `requirements-analysis` — structured analysis of ambiguous requirements
- `requirement-clarification` — detect and resolve requirement ambiguities
- `architecture-design` — system architecture with documented trade-offs
- `implementation-planning` — safe, reviewable implementation plans
- `tdd` — test-driven development workflow for AI agents
- `bug-diagnosis` — systematic bug diagnosis and root cause analysis
- `code-review` — structured code review (correctness, security, performance)
- `agent-design` — single and multi-agent system design
- `rag-architecture` — end-to-end RAG system design
- `rag-evaluation` — RAG evaluation using faithfulness, relevancy, context metrics
- `context-engineering` — context discovery, selection, compression, budgeting
- `ai-security-review` — AI security audit grounded in OWASP GenAI LLM Top 10
- `production-readiness` — pre-production checklist for AI systems

#### Workflows (6)
- `feature-development` — discovery through production
- `bug-fixing` — diagnosis, fix, regression test
- `agent-development` — goal through production
- `rag-development` — ingestion through production monitoring
- `production-readiness` — pre-production gate
- `security-review` — AI security review

#### Templates (7)
- `SPEC.md`, `ADR.md`, `DESIGN.md`, `EVALUATION.md`, `SECURITY.md`, `PRD.md`, `REVIEW.md`

#### CLI (`aiskills`)
- `aiskills init` — initialize AISkills in a repository
- `aiskills list` — list all available skills
- `aiskills search <query>` — search skills by keyword
- `aiskills info <skill>` — display skill metadata
- `aiskills validate` — validate all skills against the schema
- `aiskills doctor` — repository health checks

#### Adapters (v0.1 integration guides)
- Claude Code, Gemini CLI, OpenAI Codex, Cursor, Generic

#### Infrastructure
- GitHub Actions CI (tests, lint, skill validation)
- Pytest test suite (schema validation, CLI, validator)
- `pyproject.toml` for `pip install aiskills`

---

## Versioning Notes

| Label | Meaning |
|-------|---------|
| `experimental` | Concept only, subject to complete redesign |
| `alpha` | Working but API/format may change |
| `beta` | Stable API, undergoing community testing |
| `stable` | Validated by community use |

Current status of all v0.1.0 skills: **alpha**

[Unreleased]: https://github.com/karthikrshet/aiskills/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/karthikrshet/aiskills/releases/tag/v0.1.0
