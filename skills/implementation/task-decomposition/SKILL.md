---
name: task-decomposition
description: |
  Use this skill to break down complex feature specifications, PRDs, or
  architectural designs into small, atomic, independently verifiable tasks and
  tickets. Ensures each task has clear acceptance criteria, dependencies, and
  validation steps.
version: "0.1.0"
category: implementation
tags: [tickets, tasks, decomposition, planning, atomic-steps, execution]
risk: low
status: alpha
related-skills:
  - requirements-analysis
  - implementation-planning
  - tdd
---

# Task Decomposition

## Purpose

Large features fail when implemented as monolithic, all-at-once code changes. Massive diffs are difficult to review, hard to test, and prone to hidden regressions.

This skill provides a structured methodology for decomposing an approved feature specification or architecture document into a set of atomic, self-contained development tasks (tickets). Each task produces a working, testable state in the repository and can be executed independently.

## When to Use

- After a PRD, SPEC, or architecture design has been approved
- Before starting code implementation on a multi-file or multi-step feature
- When preparing tickets for team issue trackers (GitHub Issues, Jira, Linear)
- When structuring an agent execution plan to prevent context loss

## When Not to Use

- Single-function or trivial one-line bug fixes
- Pure research or conceptual exploratory spikes
- When an atomic implementation plan is already detailed in `implementation-planning`

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Approved Feature Spec / PRD | ✅ | Detailed requirements and acceptance criteria |
| System Design / Architecture | ✅ | Component and interface layout |
| Target Issue Tracker format | optional | GitHub Issues, Linear, or Markdown tasks |

## Preconditions

- [ ] Requirements and system design documents are finalized and approved
- [ ] Existing codebase conventions and file structure are mapped

## Workflow

### Step 1: Identify System Layers and Seams

**Deconstruct the feature along architectural seams:**
1. Database schemas and migrations
2. Core domain entities and business logic
3. Data access and persistence layers
4. External API clients and integrations
5. HTTP / RPC controllers and middleware
6. UI components and state management
7. End-to-end integration and load tests

### Step 2: Slice into Atomic Increments

Ensure each task obeys the **INVEST** principle:
- **Independent:** Can be developed and merged with minimal coupling.
- **Negotiable:** Scope is clear and bounded.
- **Valuable:** Leaves the codebase in a functioning or clean state.
- **Estimable:** Small enough to understand completely.
- **Small:** Takes a single focused session.
- **Testable:** Has explicit verification commands.

### Step 3: Format Each Ticket

For every atomic task, define:
```markdown
### Task [ID]: [Concise Title]

- **Description:** What code is added or modified and why.
- **Target Files:** List of files created or edited.
- **Dependencies:** Prerequisite tasks that must be merged first.
- **Acceptance Criteria:** Bulleted list of verifiable behaviors.
- **Verification Command:** Exact test or lint command (e.g. `pytest tests/unit/test_auth.py`).
```

### Step 4: Map the Dependency DAG

Order tasks sequentially or identify parallelizable tracks to prevent blocking dependencies.

## Decision Points

| Condition | Tier | Action |
|-----------|------|--------|
| A single task touches more than 5 distinct files | Consult | Split the task into domain logic vs. interface wiring |
| Task introduces a schema migration that breaks existing code | Approve | Require a two-phase rollout task (expand and contract pattern) |
| Feature generates more than 15 tasks | Consult | Group into milestone phases (Phase 1 MVP vs. Phase 2 Advanced) |

## Safety Constraints

- Never combine a breaking database migration and an API change in the same atomic task
- Never create a task without an explicit verification command
- Never leave orphan tasks without a defined consumer or test
- Ensure every task leaves the main test suite green

## Expected Output

- A numbered list of atomic tickets formatted for GitHub Issues, Linear, or markdown task lists
- Dependency order graph
- Clear acceptance criteria and test verification commands for every task

## Validation

- [ ] Every task has target files specified
- [ ] Every task has a concrete verification command
- [ ] No circular dependencies exist between tasks
- [ ] All requirements from the source specification are covered

## Failure Handling

| Failure | What to do |
|---------|------------|
| Tasks are too tightly coupled to separate | Re-examine the interface design; introduce an abstraction or adapter layer |
| Requirement missing in spec during decomposition | Pause decomposition; ask the human to clarify the missing requirement |

## Examples

### Example 1: Decomposing a Rate Limiting Feature

- **Task 1: Redis Token Bucket Algorithm Core**
  - Files: `src/security/rate_limiter.py`, `tests/unit/test_rate_limiter.py`
  - Verification: `pytest tests/unit/test_rate_limiter.py`
- **Task 2: HTTP Middleware Integration**
  - Files: `src/middleware/rate_limit_middleware.py`, `tests/integration/test_rate_limit_middleware.py`
  - Verification: `pytest tests/integration/test_rate_limit_middleware.py`
- **Task 3: Rate Limit Configuration & Headers**
  - Files: `src/config.py`, `src/middleware/rate_limit_middleware.py`
  - Verification: `pytest tests/ -k rate_limit`

## Related Skills

- `requirements-analysis` — source requirements for decomposition
- `implementation-planning` — execution sequencing
- `tdd` — executing individual tasks test-first
