# AISkills

> **Reusable AI Engineering Skills for Coding Agents**

[![CI](https://github.com/karthikrshet/aiskills/actions/workflows/ci.yml/badge.svg)](https://github.com/karthikrshet/aiskills/actions/workflows/ci.yml)
[![Skill Validation](https://github.com/karthikrshet/aiskills/actions/workflows/validate-skills.yml/badge.svg)](https://github.com/karthikrshet/aiskills/actions/workflows/validate-skills.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.1.0--alpha-orange.svg)](CHANGELOG.md)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](pyproject.toml)

---

## What is AISkills?

AI coding agents are powerful, but they frequently fail in predictable ways:

- They **start coding before understanding requirements**
- They **invent architecture** without inspecting the codebase
- They **skip testing, security review, and evaluation**
- They **produce inconsistent outputs** across different runs
- They have **no structured process** for AI-specific work like RAG or agent design

**AISkills** solves this by giving coding agents a reusable **engineering playbook** — a library of composable skills and workflows that guide agents through the full software and AI engineering lifecycle.

```
LLM = brain
Coding agent = worker
AISkills = engineering playbook that tells the worker how to work properly
```

---

## The Problem, Illustrated

**Without AISkills:**
```
User: "Build a RAG application for our company docs."
Agent: [starts writing LangChain boilerplate immediately]
```

**With AISkills:**
```
User: "Build a RAG application for our company docs."

AISkills guides the agent through:
  1. Requirements Analysis     ← What problem? What data? What constraints?
  2. Repository Discovery      ← What already exists?
  3. RAG Architecture Design   ← Chunking? Embedding? Retrieval strategy?
  4. Evaluation Planning       ← How will we measure faithfulness/relevancy?
  5. Security Review           ← Prompt injection? Data leakage?
  6. Implementation Planning   ← Ordered, reviewable steps
  7. Implementation            ← Small, testable changes
  8. Testing                   ← Unit + integration + E2E
  9. RAG Evaluation            ← Measure before calling it done
 10. Production Readiness      ← Latency, cost, observability, fallbacks
```

---

## Why AISkills?

| Without AISkills | With AISkills |
|-----------------|---------------|
| Agent jumps straight to code | Agent discovers requirements first |
| Architecture invented from thin air | Architecture grounded in actual codebase |
| No evaluation plan | Evaluation designed before implementation |
| Security afterthought | Security review is a mandatory workflow stage |
| RAG "works" but quality unknown | RAG evaluated on faithfulness, relevancy, recall |
| Agent makes destructive changes silently | Human-in-the-loop required for risky actions |
| One-off prompt per project | Reusable skills across every project |

---

## Features

- **14 production-quality skills** covering software engineering and AI engineering
- **6 workflow templates** for common engineering scenarios
- **AI-engineering first**: RAG, agent design, evaluation, hallucination analysis, prompt injection
- **Tool-agnostic**: works with Claude Code, Gemini CLI, Cursor, Codex, and any SKILL.md-compatible agent
- **CLI** (`aiskills`) for discovery, validation, and project initialization
- **Quality gates**: each skill must pass schema validation before inclusion
- **Security by design**: AI security grounded in OWASP GenAI LLM Top 10 (2026)
- **Human-in-the-loop**: explicit approval required for destructive and high-risk actions
- **Local-first**: the framework itself transmits nothing to external services

---

## Supported Agents

| Agent | Integration Method | Guide |
|-------|--------------------|-------|
| Claude Code | Auto-discovers `SKILL.md` files in `.claude/skills/` | [adapters/claude-code](adapters/claude-code/README.md) |
| Gemini CLI | Loads skills via `.agents/skills/` | [adapters/gemini](adapters/gemini/README.md) |
| Cursor | Via `.cursorrules` + skills directory | [adapters/cursor](adapters/cursor/README.md) |
| OpenAI Codex | Via system prompt injection | [adapters/codex](adapters/codex/README.md) |
| Generic agents | SKILL.md format + manual loading | [adapters/generic](adapters/generic/README.md) |

---

## Installation

### Option 1: Install the CLI

```bash
pip install aiskills
```

Requires Python 3.10+.

### Option 2: Clone the repository

```bash
git clone https://github.com/karthikrshet/aiskills.git
cd aiskills
pip install -e ".[dev]"
```

### Option 3: Use skills directly

Copy individual `SKILL.md` files into your agent's skills directory. No installation required.

---

## Quick Start

### 1. Initialize AISkills in your project

```bash
cd your-project
aiskills init
```

This creates:
- `AGENTS.md` — instructions for your AI coding agent
- `CONTEXT.md` — template to describe your project architecture and constraints

Fill in `CONTEXT.md` with your project details. Your agent will use this as grounding context.

### 2. List available skills

```bash
aiskills list
```

```
SKILL                     CATEGORY          RISK    STATUS
repository-discovery      discovery         low     alpha
requirements-analysis     requirements      low     alpha
requirement-clarification requirements      low     alpha
architecture-design       architecture      medium  alpha
implementation-planning   implementation    medium  alpha
tdd                       testing           low     alpha
bug-diagnosis             debugging         low     alpha
code-review               review            low     alpha
agent-design              ai/agents         medium  alpha
rag-architecture          ai/rag            medium  alpha
rag-evaluation            ai/evaluation     low     alpha
context-engineering       ai/context        low     alpha
ai-security-review        ai/security       low     alpha
production-readiness      ai/production     high    alpha
```

### 3. Search for a skill

```bash
aiskills search "RAG retrieval"
```

```
Matches:
  rag-architecture     Design end-to-end RAG systems
  rag-evaluation       Evaluate RAG pipeline quality
  context-engineering  Manage context selection and compression
```

### 4. Get skill details

```bash
aiskills info rag-evaluation
```

### 5. Use a skill with your agent

Tell your agent:

```
Use the rag-evaluation skill to evaluate the retrieval quality of our documentation RAG system.
```

Or with Claude Code, place skills in `.claude/skills/` and they are auto-discovered.

### 6. Validate your skills

```bash
aiskills validate
```

---

## Skill Examples

### repository-discovery

Before writing a single line of code, an agent using this skill will:

1. Map the repository structure (directories, key files, entry points)
2. Identify the language, framework, and build system
3. Find existing tests, CI configuration, and linting rules
4. Locate documentation, ADRs, and architecture notes
5. Produce a grounded `CONTEXT.md` summary

**Outcome:** Agent understands the codebase. No hallucinated architecture.

---

### rag-evaluation

Instead of declaring "RAG works," this skill guides the agent to:

1. Define evaluation dimensions: faithfulness, answer relevancy, context precision, context recall
2. Build or select an evaluation dataset (question + ground truth + retrieved context)
3. Run evaluations (referencing RAGAS-style methodology)
4. Report results honestly — if not measured, report `NOT MEASURED`
5. Identify retrieval failures and propose improvements

**Outcome:** RAG quality is measured, not assumed.

---

### ai-security-review

Grounded in OWASP GenAI LLM Top 10 (2026), this skill guides the agent to:

1. Check for prompt injection vectors (direct and indirect)
2. Audit tool call permissions and scope
3. Identify sensitive data exposure risks
4. Review retrieved content for malicious instruction injection
5. Verify output sanitization
6. Produce a security report with findings and mitigations

**Outcome:** AI security is a workflow stage, not an afterthought.

---

## Workflow Examples

### Feature Development

```
Discovery → Requirements → Clarification → Specification → Architecture
→ Implementation Plan → Implementation → Tests → Code Review
→ Security Review → Documentation → Production Readiness
```

### RAG Development

```
Use Case → Data Analysis → Ingestion Design → Chunking Strategy
→ Embedding Selection → Retrieval Design → Reranking → Context Construction
→ Generation → Evaluation → Production Monitoring
```

### Agent Development

```
Goal Definition → Agent Boundary → Tool Design → Memory Design
→ State Management → Planning → Guardrails → Evaluation
→ Observability → Production
```

See [workflows/](workflows/) for detailed guides.

---

## AI Engineering Capabilities

AISkills provides first-class support for AI/ML/agent engineering:

| Capability | Skill |
|-----------|-------|
| Agent architecture | `agent-design` |
| RAG design | `rag-architecture` |
| RAG evaluation | `rag-evaluation` |
| Context management | `context-engineering` |
| AI security | `ai-security-review` |
| Production AI | `production-readiness` |
| Prompt injection | covered in `ai-security-review` |
| Hallucination analysis | covered in `rag-evaluation` |
| Evaluation framework | `rag-evaluation` + EVALUATION.md template |
| Observability | covered in `production-readiness` |

---

## Architecture

```
AISkills
├── skills/          Composable skill library (SKILL.md format)
│   ├── discovery/
│   ├── requirements/
│   ├── architecture/
│   ├── implementation/
│   ├── testing/
│   ├── debugging/
│   ├── code-review/
│   └── ai/          AI engineering skills
│       ├── agent-design/
│       ├── rag/
│       ├── evaluation/
│       ├── context-engineering/
│       ├── ai-security/
│       └── production-ai/
│
├── workflows/       Multi-skill workflow definitions
├── templates/       Specification and review templates
├── adapters/        Agent-specific integration guides
├── examples/        Complete worked examples
├── tests/           Test suite
├── docs/            Documentation
└── cli/             Python CLI (aiskills)
```

Each skill follows the canonical AISkills format defined in [`docs/SKILL_SPEC.md`](docs/SKILL_SPEC.md).

---

## CLI Reference

```bash
aiskills init                 # Initialize AISkills in current repository
aiskills list                 # List all skills with metadata
aiskills search <query>       # Search skills by keyword or tag
aiskills info <skill-name>    # Display full skill metadata
aiskills validate             # Validate all skills against the schema
aiskills doctor               # Check repository health
```

See [`docs/cli.md`](docs/cli.md) for full reference.

---

## Contributing

Contributions are welcome. See [`CONTRIBUTING.md`](CONTRIBUTING.md) for:

- How to create a new skill
- Skill naming conventions
- Metadata requirements
- Testing requirements
- Pull request process
- Licensing expectations

---

## Security

See [`SECURITY.md`](SECURITY.md) for vulnerability reporting and responsible disclosure guidelines.

---

## License

Apache 2.0. See [`LICENSE`](LICENSE).

Copyright (c) 2026 Karthik Rajesh Shet.

---

## Inspiration

AISkills builds upon ideas from the broader ecosystem of:

- **AI coding agents** (Claude Code, Gemini CLI, Cursor, OpenAI Codex)
- **Agent skill systems** (the open SKILL.md format standard)
- **AI evaluation research** (RAGAS, DeepEval methodologies)
- **AI security** (OWASP GenAI LLM Top 10)
- **Software engineering automation** and structured agent workflows

All skill content in this repository is original. AISkills does not copy prompts, documentation, or implementations from other repositories.

---

## Roadmap

### v0.1 (current — alpha)
- 14 core skills
- 6 workflow templates
- CLI with validation and discovery
- Generic + agent-specific adapters
- CI/CD with skill validation

### v0.2
- Additional AI engineering skills (memory design, tool-use evaluation, prompt testing)
- Workflow engine (compose skills into automated pipelines)
- Richer CLI discovery and tagging

### v0.3
- Evaluation framework integration (RAGAS, DeepEval references)
- Expanded agent adapter support
- Detailed diagnostic output from `aiskills doctor`

### v1.0
Stable release after community validation and real-world use feedback.

---

*AISkills is alpha software. APIs, skill formats, and workflow structures may change before v1.0.*
