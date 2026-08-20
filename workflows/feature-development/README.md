# Feature Development Workflow

This workflow guides an AI coding agent through the complete feature development lifecycle — from understanding a codebase to production readiness.

---

## When to Use

Use this workflow when implementing a new feature in an existing codebase.

---

## Workflow Stages

```
Stage 1: Discovery
    ↓
Stage 2: Requirements
    ↓
Stage 3: Clarification
    ↓
[Requirements Gate]
    ↓
Stage 4: Specification
    ↓
Stage 5: Architecture
    ↓
[Architecture Gate] ← Human review required
    ↓
Stage 6: Implementation Planning
    ↓
[Plan Gate] ← Human approval required
    ↓
Stage 7: Implementation + TDD
    ↓
Stage 8: Code Review
    ↓
Stage 9: Security Review (if AI components)
    ↓
[Testing Gate]
    ↓
Stage 10: Documentation
    ↓
[Production Gate] ← Human approval required
```

---

## Stage Details

### Stage 1: Discovery (`repository-discovery`)

**Goal:** Understand the codebase before touching it.

**Actions:**
- Map the repository structure
- Read `CONTEXT.md` and `AGENTS.md`
- Identify language, framework, conventions, CI/CD
- Identify constraints and no-go zones

**Exit criterion:** Repository summary produced; key conventions documented.

---

### Stage 2: Requirements Analysis (`requirements-analysis`)

**Goal:** Structure the feature request into documented requirements.

**Actions:**
- Extract functional and non-functional requirements
- Define success criteria
- Identify constraints
- List open questions

**Exit criterion:** Requirements documented using `templates/SPEC.md`.

---

### Stage 3: Requirement Clarification (`requirement-clarification`)

**Goal:** Resolve blocking ambiguities before design.

**Actions:**
- Identify unmeasurable qualifiers
- Formulate targeted questions (max 5 at a time)
- Get human answers
- Update requirements

**Exit criterion:** All blocking ambiguities resolved.

---

### Requirements Gate ✅

| Check | Required |
|-------|---------|
| All functional requirements documented | ✅ |
| Non-functional requirements have measurable targets | ✅ |
| All blocking ambiguities resolved | ✅ |
| Constraints documented | ✅ |

**Proceed only if gate passes.**

---

### Stage 4: Specification

**Goal:** Produce a complete feature specification.

**Actions:**
- Finalize `templates/SPEC.md`
- Define acceptance criteria for each requirement
- Document definition of done

---

### Stage 5: Architecture Design (`architecture-design`)

**Goal:** Design the technical solution with documented decisions.

**Actions:**
- Identify architectural decisions required
- Evaluate alternatives with trade-offs
- Write ADRs for significant decisions
- Produce system design document
- **Present to human for review**

**Exit criterion:** Human has reviewed and approved architecture.

---

### Architecture Gate ✅ — Human Review Required

> ⚠️ **STOP: Present architecture to human. Do not begin implementation until human approves.**

| Check | Required |
|-------|---------|
| ADR(s) written for significant decisions | ✅ |
| Trade-offs documented | ✅ |
| Design is consistent with existing architecture | ✅ |
| No hard constraints violated | ✅ |
| **Human has approved** | ✅ |

---

### Stage 6: Implementation Planning (`implementation-planning`)

**Goal:** Produce a safe, ordered, step-by-step implementation plan.

**Actions:**
- List all files to create, modify, delete
- Order changes to minimize risk
- Flag destructive steps for approval
- **Present plan to human**

---

### Plan Gate ✅ — Human Approval Required

> ⚠️ **STOP: Present plan to human. Do not write a single line of code until human approves.**

---

### Stage 7: Implementation + TDD (`tdd`)

**Goal:** Implement the feature using test-driven development.

**Process per step:**
1. Write failing test
2. Write minimal implementation to pass
3. Refactor under green tests
4. Run full test suite
5. Proceed to next step

**At each destructive step:** Stop and ask human for explicit approval.

---

### Stage 8: Code Review (`code-review`)

**Goal:** Review implementation for correctness, security, performance, and maintainability.

**Actions:**
- Run automated checks (lint, format, type check, tests)
- Manual review: correctness, security, performance, maintainability
- Produce `templates/REVIEW.md`

**Exit criterion:** All blocking findings resolved.

---

### Stage 9: Security Review (`ai-security-review`)

**When:** Required if the feature involves LLMs, agents, or retrieval.

**Actions:**
- Audit against OWASP GenAI LLM Top 10
- Produce `templates/SECURITY.md`

**Exit criterion:** No unresolved critical/high security findings.

---

### Testing Gate ✅

| Check | Required |
|-------|---------|
| All tests pass | ✅ |
| New functionality has tests | ✅ |
| Edge cases and error cases tested | ✅ |
| Code review approved | ✅ |
| Security review complete (if applicable) | ✅ |

---

### Stage 10: Documentation

**Actions:**
- Update README if needed
- Update CHANGELOG
- Update `CONTEXT.md` if architecture changed
- Write or update docstrings

---

### Production Gate ✅ — Human Approval Required

> ⚠️ **STOP: Present production readiness to human. Do not deploy without explicit approval.**

Run `production-readiness` skill if this is an AI/LLM feature.

| Check | Required |
|-------|---------|
| All quality gates passed | ✅ |
| Documentation updated | ✅ |
| Production readiness checklist complete | ✅ |
| **Human has approved deployment** | ✅ |

---

*Part of AISkills v0.1.0 — see [skills/](../../skills/) for individual skill details.*
