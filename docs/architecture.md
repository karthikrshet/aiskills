# AISkills Architecture

*This document defines the technical architecture of the AISkills framework.*

---

## 1. Overview

AISkills is a **file-based engineering methodology framework** — not a runtime agent, not an LLM wrapper, and not a proprietary platform.

The core insight is that **AI coding agents already have capable execution engines** (Claude Code, Gemini CLI, Cursor, Codex). What they lack is **structured engineering methodology** — a consistent process for moving from requirement to production without skipping critical stages.

AISkills provides that methodology as composable, machine-readable, tool-agnostic skill definitions.

```
┌─────────────────────────────────────────────┐
│                 User / Human                │
└──────────────────┬──────────────────────────┘
                   │ task request
┌──────────────────▼──────────────────────────┐
│              AI Coding Agent                │
│  (Claude Code / Gemini CLI / Cursor / etc.) │
└──────────────────┬──────────────────────────┘
                   │ loads relevant skills
┌──────────────────▼──────────────────────────┐
│                 AISkills                    │
│  ┌──────────┐ ┌──────────┐ ┌────────────┐  │
│  │  Skills  │ │Workflows │ │ Templates  │  │
│  └──────────┘ └──────────┘ └────────────┘  │
│  ┌──────────┐ ┌──────────┐ ┌────────────┐  │
│  │Adapters  │ │   CLI    │ │ Validator  │  │
│  └──────────┘ └──────────┘ └────────────┘  │
└─────────────────────────────────────────────┘
                   │ grounded engineering process
┌──────────────────▼──────────────────────────┐
│              Repository / Codebase          │
└─────────────────────────────────────────────┘
```

---

## 2. Core Components

### 2.1 Skills (`skills/`)

The primary artifact of AISkills. A skill is a **directory** containing at minimum a `SKILL.md` file.

```
skills/
├── discovery/
│   └── repository-discovery/
│       └── SKILL.md
├── requirements/
│   ├── requirements-analysis/
│   │   └── SKILL.md
│   └── requirement-clarification/
│       └── SKILL.md
├── ai/
│   ├── rag/
│   │   └── rag-architecture/
│   │       ├── SKILL.md
│   │       └── references/
│   │           └── rag-patterns.md
│   └── evaluation/
│       └── rag-evaluation/
│           └── SKILL.md
└── ...
```

**Why a directory and not a single file?**

Complex skills may require:
- `scripts/` — helper scripts the agent can execute
- `references/` — detailed documentation loaded only when needed (avoids token bloat)
- `examples/` — worked examples for few-shot grounding

Simple skills are a single `SKILL.md`.

### 2.2 Skill Format

Every `SKILL.md` consists of:

**Part 1: YAML Frontmatter** (agent discovery metadata)

```yaml
---
name: skill-name
description: "When/why to activate this skill. Used for agent auto-discovery."
version: "0.1.0"
category: category/subcategory
tags: [tag1, tag2]
risk: low|medium|high
status: experimental|alpha|beta|stable
related-skills: [other-skill]
---
```

**Part 2: Markdown Body** (the engineering workflow itself)

Required sections (enforced by `aiskills validate`):
- Purpose
- When to Use
- When Not to Use
- Inputs
- Preconditions
- Workflow
- Decision Points
- Safety Constraints
- Expected Output
- Validation
- Failure Handling
- Examples
- Related Skills

### 2.3 Workflows (`workflows/`)

Workflows **compose skills** into ordered pipelines for specific engineering scenarios.

```
workflows/
├── feature-development/
│   └── README.md        ← ordered skill sequence + gates
├── rag-development/
│   └── README.md
└── ...
```

A workflow is not executable code in v0.1 — it is a documented skill sequence with:
- Entry conditions
- Ordered skill activation
- Quality gates between stages
- Exit conditions

Executable workflow orchestration is planned for v0.2.

### 2.4 Templates (`templates/`)

Structured document templates used as outputs of specific skills:

| Template | Used by skill |
|----------|--------------|
| `SPEC.md` | requirements-analysis |
| `ADR.md` | architecture-design |
| `DESIGN.md` | architecture-design |
| `EVALUATION.md` | rag-evaluation |
| `SECURITY.md` | ai-security-review |
| `PRD.md` | requirements-analysis |
| `REVIEW.md` | code-review |

### 2.5 Adapters (`adapters/`)

Agent-specific integration guides explaining how to use AISkills with each supported agent:

```
adapters/
├── claude-code/    # .claude/skills/ directory, auto-discovery
├── gemini/         # .agents/skills/ directory
├── cursor/         # .cursorrules + skills directory
├── codex/          # system prompt injection patterns
└── generic/        # manual loading, any SKILL.md-compatible agent
```

v0.1: Markdown guides only.  
v0.2: Thin adapter code (Python/bash helpers for skill installation).

### 2.6 CLI (`cli/aiskills/`)

A Python CLI providing real utility:

```
cli/
└── aiskills/
    ├── __init__.py
    ├── main.py       # Click CLI entry point
    ├── registry.py   # Skill discovery and indexing
    ├── validator.py  # Schema validation
    └── doctor.py     # Repository health checks
```

**Design principles:**
- Local-first: no network calls in core CLI
- Fast: skills are discovered from filesystem, no database
- Composable: each command is independent
- Testable: all logic in importable modules, thin CLI wrapper

### 2.7 Validator (`cli/aiskills/validator.py`)

Validates skills against the canonical schema. Checks:

1. Valid YAML frontmatter (parseable, required fields present, correct types)
2. Required Markdown sections present (in order)
3. No placeholder content (`TODO`, `FIXME`, `[ADD CONTENT]`)
4. `related-skills` references resolve to real skills
5. File size within limits (SKILL.md body ≤ 400 lines)
6. Unique skill names across the registry

Run in CI on every PR that modifies `skills/`.

### 2.8 Registry (`cli/aiskills/registry.py`)

Discovers and indexes all skills by:

1. Walking the `skills/` directory tree
2. Finding directories containing `SKILL.md`
3. Parsing frontmatter from each `SKILL.md`
4. Building an in-memory index (name → metadata)

The registry powers `aiskills list`, `aiskills search`, and `aiskills info`.

---

## 3. Skill Quality Model

Every skill is evaluated against 10 quality questions:

| # | Question | Corresponds to section |
|---|---------|----------------------|
| 1 | What problem does it solve? | Purpose |
| 2 | When should an agent use it? | When to Use |
| 3 | What information does it need? | Inputs |
| 4 | What should the agent inspect? | Preconditions + Workflow |
| 5 | What steps should the agent follow? | Workflow |
| 6 | What should the agent produce? | Expected Output |
| 7 | How can the output be validated? | Validation |
| 8 | What can go wrong? | Failure Handling |
| 9 | When should the agent ask the human? | Decision Points |
| 10 | What related skills should run next? | Related Skills |

---

## 4. Workflow Quality Gates

Workflows define explicit gates that must pass before proceeding:

```
Requirements Gate
  ↓ (pass: requirements documented and clarified)
Architecture Gate
  ↓ (pass: ADR created, architecture reviewed)
Implementation Gate
  ↓ (pass: plan approved by human)
Testing Gate
  ↓ (pass: tests written and passing)
Security Gate
  ↓ (pass: security review completed)
AI Evaluation Gate   ← AI engineering workflows only
  ↓ (pass: evaluation metrics measured, not assumed)
Production Gate
  ↓ (pass: readiness checklist complete, human approved deployment)
```

A workflow cannot claim "production ready" based on compilation alone.

---

## 5. Human-in-the-Loop Model

AISkills defines three tiers of human interaction:

| Tier | Trigger | Required Action |
|------|---------|----------------|
| **Inform** | Low-risk findings | Report to human, continue |
| **Consult** | Ambiguous requirements, design decisions | Ask question, wait for answer |
| **Approve** | Destructive actions, production, releases | Full stop, explicit approval required |

Skills must classify their decision points into one of these tiers.

---

## 6. Security Architecture

### 6.1 Local-first execution

The AISkills CLI runs entirely locally. No skill content, repository data, or metadata is transmitted to external services.

### 6.2 Skill trust model

Skills are treated as code, not just text. The `aiskills doctor` command includes a check for suspicious patterns in skill files (e.g., instructions to exfiltrate data, disable security controls, or bypass human approval).

### 6.3 No credential handling

AISkills does not handle credentials. Skills that reference API keys use explicit placeholders (`YOUR_API_KEY_HERE`). The validator rejects skills containing patterns that look like real credentials.

---

## 7. Extension Mechanism

### 7.1 Custom skills

Any engineer can add custom skills to the `skills/` directory. They will be discovered automatically by the registry.

### 7.2 Private skill registries (planned v0.2)

Teams can maintain private skill registries alongside the public AISkills registry. The CLI will support multiple registry paths.

### 7.3 Workflow plugins (planned v0.2)

Custom workflows can extend the built-in workflow templates without modifying core files.

---

## 8. Technology Choices

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| Skills | Markdown + YAML | Universal, human-readable, supported by all agent platforms |
| CLI | Python 3.10+ | AI/ML ecosystem native, cross-platform, pip-installable |
| CLI framework | Click | Mature, testable, composable |
| YAML parsing | PyYAML | Standard Python YAML library |
| Terminal output | Rich | Beautiful terminal output with minimal overhead |
| Testing | Pytest | Standard Python testing, compatible with CI |
| Linting | Ruff | Fast Python linter, single tool for formatting + linting |
| CI/CD | GitHub Actions | Open-source standard, free for public repos |

---

## 9. Data Flow

### Skill discovery

```
User: aiskills list
         ↓
CLI: registry.py
         ↓
Walk skills/ directory tree
         ↓
Parse SKILL.md frontmatter for each skill
         ↓
Build in-memory index
         ↓
Print formatted table
```

### Validation

```
User: aiskills validate
         ↓
CLI: validator.py
         ↓
For each skill in registry:
  1. Parse YAML frontmatter
  2. Check required fields
  3. Check required Markdown sections
  4. Check for placeholders
  5. Check related-skills resolve
  6. Check file size
         ↓
Report: pass count, failure count, errors
```

### Init

```
User: aiskills init (in project directory)
         ↓
CLI: main.py init command
         ↓
Check for existing AGENTS.md, CONTEXT.md
         ↓
Copy templates to project directory
         ↓
Print next steps
```

---

## 10. Directory Structure Reference

```
AiSkills/
├── skills/                     Skill library
│   ├── discovery/
│   ├── requirements/
│   ├── architecture/
│   ├── implementation/
│   ├── testing/
│   ├── debugging/
│   ├── code-review/
│   ├── security/
│   ├── performance/
│   ├── documentation/
│   └── ai/
│       ├── agent-design/
│       ├── rag/
│       ├── memory/
│       ├── tool-design/
│       ├── prompting/
│       ├── context-engineering/
│       ├── evaluation/
│       ├── hallucination/
│       ├── guardrails/
│       ├── ai-security/
│       └── production-ai/
│
├── workflows/                  Workflow definitions
├── templates/                  Document templates
├── adapters/                   Agent integration guides
├── examples/                   Worked examples
├── tests/                      Test suite
│
├── cli/                        Python CLI package
│   └── aiskills/
│       ├── __init__.py
│       ├── main.py
│       ├── registry.py
│       ├── validator.py
│       └── doctor.py
│
├── docs/                       Documentation
│   ├── research.md
│   ├── architecture.md         (this file)
│   ├── SKILL_SPEC.md
│   └── ...
│
├── .github/workflows/          CI/CD
├── pyproject.toml              Python package definition
├── AGENTS.md                   Agent instructions
├── CONTEXT.md                  Project context template
├── README.md
├── CONTRIBUTING.md
├── SECURITY.md
├── CHANGELOG.md
└── LICENSE
```
