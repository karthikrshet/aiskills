# AISkills Concepts

This document explains the core concepts of AISkills.

---

## The Core Problem

AI coding agents are capable executors but inconsistent engineers.

Given a task like "build a user authentication system," a capable agent may:
- Immediately write code without understanding requirements
- Invent an architecture without inspecting the existing codebase
- Skip tests, security review, and evaluation
- Produce correct code with the wrong architecture
- Repeat different mistakes on similar tasks in different projects

The root cause is not model capability — it is **missing engineering process**.

AISkills encodes engineering process as composable, reusable, agent-readable skills.

---

## The AISkills Model

```
LLM = brain (language understanding, code generation)
Coding agent = worker (executes tasks, reads/writes files)
AISkills = engineering playbook (structured methodology)
```

An analogy: a skilled contractor doesn't just start hammering when given a blueprint. They inspect the site, review plans, identify constraints, plan the sequence of work, and get approval before demolition. AISkills gives AI coding agents the same discipline.

---

## Skills

A **skill** is a composable, reusable engineering workflow definition.

Each skill answers:
1. What problem does it solve?
2. When should an agent use it?
3. What information does it need?
4. What should the agent inspect?
5. What steps should the agent follow?
6. What should the agent produce?
7. How can the output be validated?
8. What can go wrong?
9. When should the agent ask the human?
10. What related skills should run next?

### Skill Format

Skills use the open **SKILL.md format** — compatible with Claude Code, Gemini CLI, Cursor, Codex, and any agent that supports this standard.

```
skills/rag-evaluation/
├── SKILL.md       ← Machine-readable + human-readable skill definition
└── references/    ← Supplementary documentation (loaded on demand)
```

See [SKILL_SPEC.md](SKILL_SPEC.md) for the complete format specification.

### Skill Categories

**Software Engineering:**
- `discovery` — Explore codebases before modifying them
- `requirements` — Analyze and clarify requirements
- `architecture` — Design systems with documented decisions
- `implementation` — Plan and execute changes safely
- `testing` — Design tests; practice TDD
- `debugging` — Diagnose bugs systematically
- `code-review` — Review code for correctness, security, performance

**AI Engineering:**
- `ai/rag` — RAG system design and evaluation
- `ai/agent-design` — Agent architecture and orchestration
- `ai/context-engineering` — Context selection and compression
- `ai/evaluation` — LLM and agent evaluation
- `ai/ai-security` — AI security review
- `ai/production-ai` — Production AI readiness

---

## Workflows

A **workflow** composes multiple skills into an ordered pipeline for a specific engineering scenario.

### Example: Feature Development Workflow

```
1. repository-discovery     ← Understand the codebase first
2. requirements-analysis    ← Structure the requirement
3. requirement-clarification ← Resolve ambiguities
4. architecture-design      ← Design the solution
5. implementation-planning  ← Plan safe, reviewable steps
6. [Human approval gate]    ← ✋ Stop for review
7. tdd                      ← Write tests first
8. implementation
9. code-review              ← Review your own output
10. ai-security-review      ← If AI components involved
11. production-readiness    ← Pre-deploy checklist
```

Workflows enforce **quality gates** — checkpoints that must pass before proceeding to the next stage.

### Example: RAG Development Workflow

```
Use Case → Data Analysis → Ingestion → Chunking → Embedding
→ Retrieval → Reranking → Context Construction → Generation
→ Evaluation → Production Monitoring
```

The evaluation stage is not optional. RAG quality must be *measured*, not assumed.

---

## Quality Gates

AISkills defines workflow gates that must pass before claiming a stage is complete:

| Gate | Passes When |
|------|------------|
| Requirements Gate | Requirements documented, ambiguities resolved |
| Architecture Gate | ADR created, trade-offs documented |
| Implementation Gate | Plan approved by human |
| Testing Gate | Tests written and passing |
| Security Gate | Security review completed with findings addressed |
| AI Evaluation Gate | Metrics measured (not estimated) |
| Production Gate | Readiness checklist complete, human approved |

**A workflow cannot claim "production ready" because the code compiles.**

---

## Human-in-the-Loop

AISkills defines three tiers of human interaction:

| Tier | When | Required action |
|------|------|----------------|
| **Inform** | Low-risk findings | Report to human, continue |
| **Consult** | Ambiguous requirements, design decisions | Ask question, wait for answer |
| **Approve** | Destructive actions, production deployments, releases | Full stop, explicit approval |

Every skill defines its decision points and classifies them into one of these tiers.

**Approve-tier actions that always require explicit human approval:**
- Deleting files or directories
- Modifying production configuration
- Changing credentials
- Publishing packages or releases
- Running destructive database migrations
- Pushing to production

---

## Templates

Templates are structured document formats that skills produce as output:

| Template | Purpose |
|----------|---------|
| `SPEC.md` | Feature specification |
| `ADR.md` | Architecture decision record |
| `DESIGN.md` | System design document |
| `EVALUATION.md` | AI evaluation report |
| `SECURITY.md` | Security review report |
| `PRD.md` | Product requirements |
| `REVIEW.md` | Code review report |

Templates ensure consistent output across projects and teams.

---

## Adapters

Adapters explain how to integrate AISkills with specific agent platforms.

Since skills use the open SKILL.md format, they work natively with platforms that auto-discover skills (Claude Code, Gemini CLI). For other platforms, adapters explain how to manually load skills.

---

## Context Engineering

Before any skill can run effectively, the agent needs context:

1. **`CONTEXT.md`** — your project's architecture, conventions, constraints
2. **`AGENTS.md`** — how this project uses AISkills (present in every AISkills project)
3. **Repository structure** — discovered via `repository-discovery` skill

Context is the foundation. All skills depend on it.

---

## Evaluation as a First-Class Concern

AISkills treats evaluation as a required engineering stage — not an optional afterthought.

For AI systems:
- RAG quality is measured on faithfulness, relevancy, context precision, and recall
- Agent quality is measured on task completion, tool-use accuracy, and trajectory correctness
- Hallucination is analyzed, not assumed absent

**Honesty rule:** If a metric has not been measured, it is reported as `NOT MEASURED`. AISkills never invents evaluation results.

---

## Security by Design

Every AISkills skill includes Safety Constraints. The `ai-security-review` skill applies OWASP GenAI LLM Top 10 (2026) to AI systems.

Core security principles encoded in AISkills:
- Never expose, log, or commit secrets
- Treat all externally retrieved content as untrusted (indirect prompt injection defense)
- Require human approval for all destructive actions
- Apply least-privilege to agent tool permissions
- Sanitize all LLM outputs before they reach downstream systems

---

*AISkills v0.1.0 — see [SKILL_SPEC.md](SKILL_SPEC.md) for the technical format specification.*
