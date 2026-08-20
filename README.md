# AISkills

> **Reusable AI Engineering Skills for Coding Agents**

[![CI](https://github.com/karthikrshet/aiskills/actions/workflows/ci.yml/badge.svg)](https://github.com/karthikrshet/aiskills/actions/workflows/ci.yml)
[![Validate Skills](https://github.com/karthikrshet/aiskills/actions/workflows/validate-skills.yml/badge.svg)](https://github.com/karthikrshet/aiskills/actions/workflows/validate-skills.yml)
[![Tests](https://img.shields.io/badge/tests-68-brightgreen.svg)](tests/)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](pyproject.toml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.1.0--alpha-orange.svg)](CHANGELOG.md)

---

## Table of Contents

1. [What is AISkills?](#what-is-aiskills)
2. [The Core Concept](#the-core-concept)
3. [The AISkills Difference](#the-aiskills-difference)
4. [Canonical Skills Catalog (14 Skills)](#canonical-skills-catalog)
   - [Software Engineering Skills](#software-engineering-skills)
   - [AI Engineering Skills](#ai-engineering-skills)
5. [Engineering Document Templates (7 Templates)](#engineering-document-templates)
6. [Engineering Workflows (6 Pipelines)](#engineering-workflows)
7. [Agent Platform Integration Guides](#agent-platform-integration-guides)
   - [Claude Code](#1-claude-code)
   - [Gemini CLI / Antigravity](#2-gemini-cli--antigravity)
   - [Cursor](#3-cursor)
   - [OpenAI Codex](#4-openai-codex)
   - [Generic / Any Coding Agent](#5-generic--any-coding-agent)
8. [CLI Installation and Usage](#cli-installation-and-usage)
9. [Human-in-the-Loop Approval Model](#human-in-the-loop-approval-model)
10. [AI Security by Design (OWASP GenAI Top 10)](#ai-security-by-design)
11. [Evaluation Honesty Standard](#evaluation-honesty-standard)
12. [Skill Authoring Guide](#skill-authoring-guide)
13. [Testing and CI/CD](#testing-and-cicd)
14. [Roadmap](#roadmap)
15. [Contributing and License](#contributing-and-license)

---

## What is AISkills?

AI coding agents are capable executors, but they are inconsistent engineers:

- They **jump straight to code generation** without understanding requirements or constraints.
- They **invent architecture** without inspecting existing repository conventions.
- They **skip testing, security audits, and evaluation**.
- They have **no structured process** for AI-native challenges (RAG architectures, agent tool permissions, token budgets, hallucination rates, indirect prompt injection).

**AISkills** solves this by providing a standardized, tool-agnostic **engineering playbook** for AI coding agents. It encodes disciplined engineering workflows into the machine-readable open `SKILL.md` format.

---

## The Core Concept

```text
LLM          = Brain (Reasoning, Language Understanding, Code Generation)
Coding Agent = Worker (File I/O, Command Execution, IDE Tooling)
AISkills     = Engineering Playbook (Requirements -> Architecture -> TDD -> Evaluation -> Security -> Production)
```

An analogy: a licensed civil engineer does not begin pouring concrete the moment a building is requested. They survey the terrain, verify soil mechanics, draft blueprints, calculate load limits, document trade-offs, and obtain permits before construction. AISkills brings this exact engineering discipline to AI coding agents.

---

## The AISkills Difference

```text
User: "Build a document Q&A RAG application for our internal docs."

Without AISkills:
└── Agent immediately writes arbitrary boilerplate using unverified libraries.

With AISkills:
└── 1. Requirements Analysis   -> [SPEC.md] (Extract functional requirements, latency SLOs, cost budget)
    2. Repository Discovery    -> Inspect existing stack (PostgreSQL + pgvector, FastAPI)
    3. RAG Architecture Design -> [DESIGN.md + ADR.md] (Chunking strategy, embedding model, hybrid search)
    4. Implementation Planning -> Ordered, reviewable steps with human approval gates
    5. TDD Implementation      -> Write failing tests first for chunking, parser, and search
    6. RAG Evaluation          -> [EVALUATION.md] (Measure faithfulness, answer relevancy, context precision)
    7. AI Security Audit       -> [SECURITY.md] (OWASP GenAI LLM Top 10 defense against prompt injection)
    8. Production Readiness    -> 11-point pre-deploy verification (fallbacks, observability, rate limits)
```

---

## Why These Skills Exist: Fixing the 3 Classic Agent Failure Modes

AISkills is built to resolve the three most common failure modes developers encounter with Claude Code, Cursor, Codex, and coding agents:

### 1. Misalignment: "The Agent Didn't Build What I Wanted"
> *"No-one knows exactly what they want."* - David Thomas & Andrew Hunt, The Pragmatic Programmer

- **The Problem:** The user provides a brief prompt ("add OAuth login"). The agent begins coding with unspoken assumptions, leading to massive rework when the result doesn't match the user's intent.
- **The Fix:** An interactive grilling session ([`grill-with-docs`](skills/requirements/grill-with-docs/SKILL.md) / [`grill-me`](skills/requirements/grill-me/SKILL.md)). The agent interrogates the human on edge cases, domain models, permissions, and failure modes before touching code.

### 2. Verbosity: "The Agent Is Too Wordy and Hallucinates Jargon"
> *"With a ubiquitous language, conversations among developers and expressions of the code are all derived from the same domain model."* - Eric Evans, Domain-Driven Design

- **The Problem:** Agents dropped into a repository use 20 vague words where 1 precise domain term will do.
- **The Fix:** A shared **Ubiquitous Language** documented in [`CONTEXT.md`](CONTEXT.md). For example:
  - *Before:* "There's an issue when a lesson inside a course section is given a spot on the file system."
  - *After (Ubiquitous Language):* "There's a problem with the materialization cascade."
  - Using [`grill-with-docs`](skills/requirements/grill-with-docs/SKILL.md), the agent extracts domain jargon and captures hard architectural trade-offs in ADRs (`templates/ADR.md`).

### 3. Lack of Engineering Guardrails: "Vibe Coding without Verification"
- **The Problem:** Agents delete files, skip tests, force-push branches, and declare features "done" without measuring quality.
- **The Fix:** Hard safety rules ([`git-guardrails`](skills/security/git-guardrails/SKILL.md)), test-first discipline ([`tdd`](skills/testing/tdd/SKILL.md)), ticket slicing ([`task-decomposition`](skills/implementation/task-decomposition/SKILL.md)), and formal evaluation ([`rag-evaluation`](skills/ai/evaluation/rag-evaluation/SKILL.md)).

---

## Canonical Skills Catalog (22 Skills)

All skills follow the [canonical SKILL.md specification](docs/SKILL_SPEC.md) (YAML frontmatter + 13 mandatory sections).

### Software Engineering Skills (15)

| Skill | Category | Risk | Purpose | File Link |
|---|---|---|---|---|
| `repository-discovery` | `discovery` | Low | Ground agent context in existing codebase patterns before touching code | [`SKILL.md`](skills/discovery/repository-discovery/SKILL.md) |
| `requirements-analysis` | `requirements` | Low | Transform ambiguous requests into structured, testable specifications | [`SKILL.md`](skills/requirements/requirements-analysis/SKILL.md) |
| `requirement-clarification` | `requirements` | Low | Formulate targeted questions to resolve blocking ambiguities | [`SKILL.md`](skills/requirements/requirement-clarification/SKILL.md) |
| `grill-me` | `requirements` | Low | Interactive requirements interview to uncover hidden edge cases | [`SKILL.md`](skills/requirements/grill-me/SKILL.md) |
| `grill-with-docs` | `requirements` | Low | Build ubiquitous domain language, update `CONTEXT.md`, and draft ADRs | [`SKILL.md`](skills/requirements/grill-with-docs/SKILL.md) |
| `triage` | `requirements` | Low | Systematically categorize, prioritize, and label issues and bug reports | [`SKILL.md`](skills/requirements/triage/SKILL.md) |
| `architecture-design` | `architecture` | Medium | System design with explicit trade-offs and Architecture Decision Records (ADRs) | [`SKILL.md`](skills/architecture/architecture-design/SKILL.md) |
| `rapid-prototyping` | `architecture` | Low | Time-boxed disposable spikes and exploratory feasibility prototypes | [`SKILL.md`](skills/architecture/rapid-prototyping/SKILL.md) |
| `implementation-planning` | `implementation` | Medium | Ordered, step-by-step implementation plans with risk mitigation | [`SKILL.md`](skills/implementation/implementation-planning/SKILL.md) |
| `task-decomposition` | `implementation` | Low | Slice features and PRDs into atomic, independently verifiable tickets | [`SKILL.md`](skills/implementation/task-decomposition/SKILL.md) |
| `tdd` | `testing` | Low | Test-driven development workflow (write failing tests first) | [`SKILL.md`](skills/testing/tdd/SKILL.md) |
| `bug-diagnosis` | `debugging` | Low | Systematic root-cause isolation before attempting code fixes | [`SKILL.md`](skills/debugging/bug-diagnosis/SKILL.md) |
| `code-review` | `code-review` | Low | Multi-dimensional review (correctness, security, performance, maintainability) | [`SKILL.md`](skills/code-review/code-review/SKILL.md) |
| `session-handoff` | `documentation` | Low | Compress session state into structured handoff notes for continuity | [`SKILL.md`](skills/documentation/session-handoff/SKILL.md) |
| `git-guardrails` | `security` | High | Enforce safety boundaries on git commands and prevent secret leaks | [`SKILL.md`](skills/security/git-guardrails/SKILL.md) |

### AI Engineering Skills (7)

| Skill | Category | Risk | Purpose | File Link |
|---|---|---|---|---|
| `agent-design` | `ai/agent-design` | Medium | Design single/multi-agent boundaries, tool permissions, memory, and guardrails | [`SKILL.md`](skills/ai/agent-design/agent-design/SKILL.md) |
| `rag-architecture` | `ai/rag` | Medium | End-to-end RAG architecture (chunking, embeddings, hybrid search, context assembly) | [`SKILL.md`](skills/ai/rag/rag-architecture/SKILL.md) |
| `rag-evaluation` | `ai/evaluation` | Low | Measure faithfulness, relevancy, context precision/recall, and hallucination | [`SKILL.md`](skills/ai/evaluation/rag-evaluation/SKILL.md) |
| `context-engineering` | `ai/context-engineering` | Low | Token budgeting, context compression, prioritization, and injection detection | [`SKILL.md`](skills/ai/context-engineering/context-engineering/SKILL.md) |
| `concise-mode` | `ai/context-engineering` | Low | Zero-filler, high-density communication to conserve token budget | [`SKILL.md`](skills/ai/context-engineering/concise-mode/SKILL.md) |
| `ai-security-review` | `ai/ai-security` | Low | Security audit grounded in **OWASP GenAI LLM Top 10 (2026)** | [`SKILL.md`](skills/ai/ai-security/ai-security-review/SKILL.md) |
| `production-readiness` | `ai/production-ai` | High | Pre-deploy gating for model abstraction, cost SLOs, latency, and rollbacks | [`SKILL.md`](skills/ai/production-ai/production-readiness/SKILL.md) |

---

## Engineering Document Templates

Standardized markdown templates produced by skills during execution:

- [`templates/SPEC.md`](templates/SPEC.md) - Feature specification and acceptance criteria.
- [`templates/ADR.md`](templates/ADR.md) - Architecture Decision Records with alternatives and trade-offs.
- [`templates/DESIGN.md`](templates/DESIGN.md) - System design with dedicated AI/LLM architecture section.
- [`templates/EVALUATION.md`](templates/EVALUATION.md) - AI evaluation report with RAG, agent, and operational metrics.
- [`templates/SECURITY.md`](templates/SECURITY.md) - Security review report mapping OWASP LLM01-LLM10.
- [`templates/PRD.md`](templates/PRD.md) - Product requirements document.
- [`templates/REVIEW.md`](templates/REVIEW.md) - Code review report with categorized findings.

---

## Engineering Workflows

Composed pipelines that coordinate multiple skills across project milestones:

- [`workflows/feature-development`](workflows/feature-development/README.md) - Discovery through production release.
- [`workflows/rag-development`](workflows/rag-development/README.md) - Use case analysis through production monitoring.
- [`workflows/agent-development`](workflows/agent-development/README.md) - Agent boundaries, tools, and guardrails.
- [`workflows/bug-fixing`](workflows/bug-fixing/README.md) - Reproduction, root cause analysis, regression test, and fix.
- [`workflows/security-review`](workflows/security-review/README.md) - AI security audit pipeline.
- [`workflows/production-readiness`](workflows/production-readiness/README.md) - Mandatory pre-deploy checklist.

---

## Agent Platform Integration Guides

AISkills is tool-agnostic and functions with any AI coding agent.

### 1. Claude Code

Claude Code auto-discovers skills placed in `.claude/skills/`.

```bash
# Copy skills into your repository
mkdir -p .claude/skills
cp -r /path/to/aiskills/skills/* .claude/skills/
```

Claude Code will automatically select and activate skills based on user prompt context. See [adapters/claude-code/README.md](adapters/claude-code/README.md).

### 2. Gemini CLI / Antigravity

Gemini CLI auto-discovers skills from `.agents/skills/` in the workspace root.

```bash
mkdir -p .agents/skills
cp -r /path/to/aiskills/skills/* .agents/skills/
```

Initialize your workspace with `aiskills init` to produce `AGENTS.md` and `CONTEXT.md`. See [adapters/gemini/README.md](adapters/gemini/README.md).

### 3. Cursor

Add skill instructions to `.cursorrules`:

```text
Before starting any task:
1. Read AGENTS.md and CONTEXT.md.
2. Inspect available skills in .aiskills/skills/.
3. Follow the relevant SKILL.md workflow.
4. Stop for human approval on all destructive actions.
```

See [adapters/cursor/README.md](adapters/cursor/README.md).

### 4. OpenAI Codex

Inject the skill specification directly into the system prompt:

```python
with open("skills/discovery/repository-discovery/SKILL.md") as f:
    skill_content = f.read()

system_prompt = f"Follow this engineering workflow:\n{skill_content}"
```

See [adapters/codex/README.md](adapters/codex/README.md).

### 5. Generic / Any Coding Agent

For any custom or LLM-based coding agent:
1. Run `aiskills init` in the project root.
2. Instruct the agent: *"Read AGENTS.md and CONTEXT.md before beginning work, and execute the relevant skill from skills/."*
3. See [adapters/generic/README.md](adapters/generic/README.md).

---

## CLI Installation and Usage

### Installation

```bash
# Clone repository
git clone https://github.com/karthikrshet/aiskills.git
cd aiskills

# Install package with development dependencies
pip install -e ".[dev]"
```

Verify installation:

```bash
aiskills --version
# aiskills 0.1.0
```

### CLI Commands Reference

| Command | Description | Example |
|---|---|---|
| `aiskills init` | Initialize `AGENTS.md` and `CONTEXT.md` in current project | `aiskills init` |
| `aiskills list` | List all 22 canonical skills with categories and risk levels | `aiskills list` |
| `aiskills search <query>` | Deterministic ranked search across names, tags, categories, descriptions | `aiskills search "RAG evaluation"` |
| `aiskills info <skill>` | Display detailed skill metadata, description, tags, and related skills | `aiskills info rag-evaluation` |
| `aiskills validate` | Validate all skills against schema, section, and placeholder rules | `aiskills validate --skills-dir skills/` |
| `aiskills doctor` | Verify repository health, grounding context, and scan for suspicious patterns | `aiskills doctor --project-dir .` |

---

## Human-in-the-Loop Approval Model

AISkills enforces a strict three-tier human interaction model across all workflows:

| Tier | When Used | Required Agent Action |
|---|---|---|
| **Inform** | Low-risk findings, non-blocking observations | Report findings to human; continue workflow |
| **Consult** | Ambiguous requirements, architectural alternatives | Formulate targeted questions; pause for response |
| **Approve** | Destructive actions, production deployments, secrets | **Full stop**. Explicit written human approval required |

### Mandatory Approval Actions
An AI coding agent must **never** execute the following without explicit human consent:
- Deleting files or directories
- Modifying production configuration files
- Changing credentials, API keys, or environment secrets
- Pushing commits or publishing releases
- Executing destructive database migrations or schema alterations

---

## AI Security by Design

The `ai-security-review` skill provides a defensive audit grounded in the **OWASP GenAI LLM Top 10 (2026)**:

1. **LLM01 - Prompt Injection**: Direct prompt hijacking and indirect injection via retrieved documents.
2. **LLM02 - Sensitive Information Disclosure**: System prompt leakage, training data extraction, PII exposure.
3. **LLM03 - Supply Chain Vulnerabilities**: Unverified third-party models, plugins, and fine-tuning datasets.
4. **LLM04 - Data and Model Poisoning**: Manipulation of knowledge base content and embeddings.
5. **LLM05 - Improper Output Handling**: Passing unsanitized LLM output to SQL engines, shell interpreters, or HTML DOM.
6. **LLM06 - Excessive Agency**: Over-permissioned agents taking autonomous high-impact actions.
7. **LLM07 - System Prompt Leakage**: Adversarial extraction of confidential business logic.
8. **LLM08 - Vector and Embedding Weaknesses**: Semantic poisoning and adversarial query crafting.
9. **LLM09 - Misinformation & Hallucination**: Fabricated outputs presented without source grounding.
10. **LLM10 - Unbounded Consumption**: Resource exhaustion and unmonitored API billing spikes.

---

## Evaluation Honesty Standard

AISkills strictly forbids fabricated benchmarks or assumed quality:

```text
Evaluation Honesty Rule:
If a metric has not been measured on an actual evaluation dataset:
-> Report: NOT MEASURED
-> Do NOT estimate or invent scores.
-> Quality must be verified before declaring production readiness.
```

When evaluating RAG systems or Agents using [`templates/EVALUATION.md`](templates/EVALUATION.md):
- **Faithfulness**: Does the answer contain only information from retrieved context?
- **Answer Relevancy**: Does the answer address the question?
- **Context Precision**: What fraction of retrieved chunks are relevant?
- **Context Recall**: Was all necessary context retrieved?
- **Hallucination Rate**: Fraction of answers containing ungrounded claims.

---

## Skill Authoring Guide

To add a new skill to AISkills:

1. Create a directory: `skills/<category>/<skill-name>/`
2. Create `SKILL.md` with YAML frontmatter:
   ```yaml
   ---
   name: your-skill-name
   description: |
     Clear description of when and why an agent should activate this skill.
   version: "0.1.0"
   category: discovery
   tags: [tag1, tag2]
   risk: low
   status: alpha
   related-skills: [repository-discovery]
   ---
   ```
3. Include all 13 required Markdown sections:
   - `## Purpose`
   - `## When to Use`
   - `## When Not to Use`
   - `## Inputs`
   - `## Preconditions`
   - `## Workflow`
   - `## Decision Points`
   - `## Safety Constraints`
   - `## Expected Output`
   - `## Validation`
   - `## Failure Handling`
   - `## Examples`
   - `## Related Skills`
4. Run validation:
   ```bash
   aiskills validate
   ```

See [`docs/skill-authoring.md`](docs/skill-authoring.md) for the complete authoring specification.

---

## Testing and CI/CD

```bash
# Run the test suite (68 automated tests)
pytest tests/ -v

# Run linting and code formatting checks
ruff check cli/ tests/
ruff format --check cli/ tests/
```

GitHub Actions automatically executes:
- Multi-version matrix test across **Python 3.10, 3.11, and 3.12**
- Ruff linting and formatting compliance
- Automatic skill schema validation on pull requests

---

## Roadmap

- **v0.1.0-alpha (Current)**: 22 canonical skills, 7 templates, 6 workflows, 5 adapters, Python CLI with ranked search and validation, 68 automated tests.
- **v0.2**: Memory design skills, tool-use evaluation benchmarks, automated skill chaining engine.
- **v0.3**: Native RAGAS / DeepEval evaluation runners, expanded IDE sidecar plugins.
- **v1.0**: Stable release following community feedback and production validation.

---

## Contributing and License

Contributions are welcome! Please read [`CONTRIBUTING.md`](CONTRIBUTING.md) and [`SECURITY.md`](SECURITY.md) before submitting pull requests.

### License
Distributed under the **Apache License 2.0**. See [`LICENSE`](LICENSE) for terms.  
Copyright (c) 2026 Karthik Rajesh Shet.
