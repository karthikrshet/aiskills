# AISkills

> **Reusable AI Engineering Skills for Coding Agents**

[![CI](https://github.com/karthikrshet/aiskills/actions/workflows/ci.yml/badge.svg)](https://github.com/karthikrshet/aiskills/actions/workflows/ci.yml)
[![Validate Skills](https://github.com/karthikrshet/aiskills/actions/workflows/validate-skills.yml/badge.svg)](https://github.com/karthikrshet/aiskills/actions/workflows/validate-skills.yml)
[![Tests](https://img.shields.io/badge/tests-66%20passed-brightgreen.svg)](tests/)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](pyproject.toml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.1.0--alpha-orange.svg)](CHANGELOG.md)

---

## What is AISkills?

AI coding agents are powerful executors, but they are inconsistent engineers:

- They **jump straight to writing code** without clarifying requirements.
- They **invent architecture** without inspecting existing patterns.
- They **skip tests, security audits, and evaluation**.
- They have **no structured process** for AI-native challenges (RAG, agent boundaries, context budgets, hallucination, indirect prompt injection).

**AISkills** solves this by providing a standardized, tool-agnostic **engineering playbook** for AI coding agents. It encodes disciplined engineering workflows into the machine-readable open `SKILL.md` format.

```text
LLM          = Brain (Reasoning & Code Generation)
Coding Agent = Worker (File I/O, Terminal, Tools)
AISkills     = Engineering Playbook (Requirements → Architecture → TDD → Evaluation → Security → Production)
```

---

## 🎯 The AISkills Difference

```text
User: "Build a document Q&A RAG application for our team."

Without AISkills:
└── Agent immediately writes boilerplate code using unverified libraries.

With AISkills:
└── 1. Requirements Analysis   → [SPEC.md] (What queries? Latency & cost limits?)
    2. Repository Discovery    → Inspect existing stack (Postgres + pgvector)
    3. RAG Architecture Design → [DESIGN.md + ADR.md] (Chunking, embeddings, hybrid retrieval)
    4. Implementation Planning → Ordered, reviewable steps with human approval gates
    5. TDD Implementation      → Tests written first for parsers & retrievers
    6. RAG Evaluation          → [EVALUATION.md] (Faithfulness, answer relevancy, precision)
    7. AI Security Audit       → [SECURITY.md] (OWASP GenAI LLM Top 10 defense)
    8. Production Readiness    → 11-point pre-deploy verification
```

---

## 📚 14 Canonical Skills

All skills follow the [canonical SKILL.md specification](docs/SKILL_SPEC.md) (YAML frontmatter + 13 mandatory sections).

### 🛠️ Software Engineering Skills (8)

| Skill | Category | Risk | Purpose |
|---|---|---|---|
| [`repository-discovery`](skills/discovery/repository-discovery/SKILL.md) | `discovery` | Low | Ground agent context in existing codebase patterns before touching code |
| [`requirements-analysis`](skills/requirements/requirements-analysis/SKILL.md) | `requirements` | Low | Transform ambiguous requests into structured, testable specifications |
| [`requirement-clarification`](skills/requirements/requirement-clarification/SKILL.md) | `requirements` | Low | Formulate targeted questions to resolve blocking ambiguities |
| [`architecture-design`](skills/architecture/architecture-design/SKILL.md) | `architecture` | Medium | System design with explicit trade-offs and Architecture Decision Records (ADRs) |
| [`implementation-planning`](skills/implementation/implementation-planning/SKILL.md) | `implementation` | Medium | Ordered, step-by-step implementation plans with risk mitigation |
| [`tdd`](skills/testing/tdd/SKILL.md) | `testing` | Low | Test-driven development workflow (write failing tests first) |
| [`bug-diagnosis`](skills/debugging/bug-diagnosis/SKILL.md) | `debugging` | Low | Systematic root-cause isolation before attempting code fixes |
| [`code-review`](skills/code-review/code-review/SKILL.md) | `code-review` | Low | Multi-dimensional review (correctness, security, perf, maintainability) |

### 🤖 AI Engineering Skills (6)

| Skill | Category | Risk | Purpose |
|---|---|---|---|
| [`agent-design`](skills/ai/agent-design/agent-design/SKILL.md) | `ai/agent-design` | Medium | Design single/multi-agent boundaries, tool permissions, memory, and guardrails |
| [`rag-architecture`](skills/ai/rag/rag-architecture/SKILL.md) | `ai/rag` | Medium | End-to-end RAG architecture (chunking, embeddings, hybrid search, context assembly) |
| [`rag-evaluation`](skills/ai/evaluation/rag-evaluation/SKILL.md) | `ai/evaluation` | Low | Measure faithfulness, relevancy, context precision/recall, and hallucination |
| [`context-engineering`](skills/ai/context-engineering/context-engineering/SKILL.md) | `ai/context-engineering` | Low | Token budgeting, context compression, prioritization, and injection detection |
| [`ai-security-review`](skills/ai/ai-security/ai-security-review/SKILL.md) | `ai/ai-security` | Low | Security audit grounded in **OWASP GenAI LLM Top 10 (2026)** |
| [`production-readiness`](skills/ai/production-ai/production-readiness/SKILL.md) | `ai/production-ai` | High | Pre-deploy gating for model abstraction, cost SLOs, latency, and rollbacks |

---

## 📋 Engineering Document Templates (7)

Standardized markdown templates produced by skills during execution:

- [`templates/SPEC.md`](templates/SPEC.md) — Feature specification and acceptance criteria.
- [`templates/ADR.md`](templates/ADR.md) — Architecture Decision Records with alternatives and trade-offs.
- [`templates/DESIGN.md`](templates/DESIGN.md) — System design with dedicated AI/LLM architecture section.
- [`templates/EVALUATION.md`](templates/EVALUATION.md) — AI evaluation report with RAG, agent, and latency metrics.
- [`templates/SECURITY.md`](templates/SECURITY.md) — Security review report mapping OWASP LLM01–LLM10.
- [`templates/PRD.md`](templates/PRD.md) — Product requirements document.
- [`templates/REVIEW.md`](templates/REVIEW.md) — Code review report with categorized findings.

---

## 🔄 End-to-End Workflows (6)

- [`workflows/feature-development`](workflows/feature-development/README.md) — Discovery through production release.
- [`workflows/rag-development`](workflows/rag-development/README.md) — Use case analysis through production monitoring.
- [`workflows/agent-development`](workflows/agent-development/README.md) — Agent boundaries, tools, and guardrails.
- [`workflows/bug-fixing`](workflows/bug-fixing/README.md) — Reproduction, root cause analysis, regression test, and fix.
- [`workflows/security-review`](workflows/security-review/README.md) — AI security audit pipeline.
- [`workflows/production-readiness`](workflows/production-readiness/README.md) — Mandatory pre-deploy checklist.

---

## 🔌 Agent Adapters (5)

AISkills is tool-agnostic and works with any agent platform:

| Platform | Integration Method | Guide |
|---|---|---|
| **Claude Code** | Auto-discovers `SKILL.md` in `.claude/skills/` | [adapters/claude-code](adapters/claude-code/README.md) |
| **Gemini CLI / AGY** | Auto-discovers `SKILL.md` in `.agents/skills/` | [adapters/gemini](adapters/gemini/README.md) |
| **Cursor** | Configured via `.cursorrules` + `.aiskills/` | [adapters/cursor](adapters/cursor/README.md) |
| **OpenAI Codex** | Direct system prompt injection | [adapters/codex](adapters/codex/README.md) |
| **Generic Agents** | Universal instructions for any agent | [adapters/generic](adapters/generic/README.md) |

---

## 🚀 Quick Start

### 1. Install AISkills

```bash
# Clone the repository
git clone https://github.com/karthikrshet/aiskills.git
cd aiskills

# Install with development dependencies
pip install -e ".[dev]"
```

### 2. Initialize in Your Project

```bash
cd your-project
aiskills init
```

This creates:
- `AGENTS.md` — Instructions for coding agents working in your repository.
- `CONTEXT.md` — Project context template (tech stack, architecture, conventions).

### 3. Explore & Search Skills

```bash
# List all 14 skills
aiskills list

# Search by keyword or tag (with deterministic ranking)
aiskills search "RAG evaluation"
aiskills search "security"

# View skill details
aiskills info rag-evaluation
```

### 4. Validate Repository & Skills

```bash
# Validate skill schemas and required sections
aiskills validate

# Health check repository grounding context
aiskills doctor
```

---

## 🛡️ Security & Evaluation Principles

### 🔒 AI Security by Design
AISkills security reviews are grounded in **OWASP GenAI LLM Top 10 (2026)**:
- **LLM01**: Prompt Injection (Direct & Indirect)
- **LLM02**: Sensitive Information Disclosure
- **LLM03**: Supply Chain Vulnerabilities
- **LLM04**: Data and Model Poisoning
- **LLM05**: Improper Output Handling
- **LLM06**: Excessive Agency
- **LLM07**: System Prompt Leakage
- **LLM08**: Vector and Embedding Weaknesses
- **LLM09**: Misinformation & Hallucination
- **LLM10**: Unbounded Consumption

### ⚖️ Evaluation Honesty Rule
If a quality metric has not been measured:
- Report: `NOT MEASURED`
- Never estimate, round up, or fabricate evaluation scores.
- Quality must be verified, not assumed.

---

## 🧪 Testing & CI/CD

```bash
# Run 66 unit & integration tests
pytest tests/ -v

# Run linting and format checking
ruff check cli/ tests/
ruff format --check cli/ tests/
```

GitHub Actions automatically runs multi-version matrix tests (Python 3.10, 3.11, 3.12), Ruff formatting checks, and automated skill schema validation on every push and pull request.

---

## 🗺️ Roadmap

- **v0.1 (Current — Alpha)**: 14 core skills, 7 templates, 6 workflows, 5 adapters, Python CLI with ranked search and validation, 100% test coverage.
- **v0.2**: Memory design skills, tool-use evaluation benchmarks, automated skill chaining engine.
- **v0.3**: Native RAGAS / DeepEval evaluation runners, expanded IDE plugins.
- **v1.0**: Stable release following community feedback and production validation.

---

## 🤝 Contributing

Contributions are welcome! See [`CONTRIBUTING.md`](CONTRIBUTING.md) and [`docs/skill-authoring.md`](docs/skill-authoring.md) for skill authoring guidelines, schema rules, and PR workflows.

---

## 📄 License

Apache License 2.0. See [`LICENSE`](LICENSE) for details.  
Copyright © 2026 Karthik Rajesh Shet.
