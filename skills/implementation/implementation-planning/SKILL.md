---
name: implementation-planning
description: |
  Use this skill to convert an approved architecture into a safe, ordered,
  reviewable implementation plan before writing any code. Activates after
  architecture has been designed and approved. Produces a step-by-step plan
  that the human can review and approve before implementation begins.
version: "0.1.0"
category: implementation
tags: [planning, implementation, steps, ordering, risk-management]
risk: medium
status: alpha
related-skills:
  - architecture-design
  - tdd
  - code-review
  - repository-discovery
---

# Implementation Planning

## Purpose

An agent without an implementation plan tends to make the largest possible change in the fewest steps. This maximizes the risk of introducing difficult-to-revert changes, breaking unrelated functionality, or losing track of progress mid-implementation.

This skill produces a structured, ordered implementation plan that decomposes the work into small, independently reviewable steps. Each step produces a working (or at minimum, stable) state. The plan is presented to the human for approval before any code is written.

## When to Use

- Architecture has been approved and implementation is about to begin
- A feature is large enough to span multiple files or components
- The change requires modifying existing public interfaces
- The change involves multiple developers or multiple sessions
- The change is risky enough that step-by-step reversibility matters

## When Not to Use

- The change is a single-file, single-function, low-risk fix
- The human has explicitly asked for a quick implementation without planning
- A plan already exists and is up-to-date

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Approved architecture / design document | ✅ | What is being built |
| Requirements document | ✅ | What success looks like |
| Repository discovery summary | ✅ | What exists and what must be respected |

## Preconditions

- [ ] Architecture is approved by the human
- [ ] Requirements are documented and approved
- [ ] Agent has current understanding of the codebase

## Workflow

### Step 1: Identify the Full Set of Changes

**List every file or component that needs to be:**
- Created (new files)
- Modified (existing files with changes)
- Deleted (files to remove — flag for explicit approval)
- Configured (environment variables, build files, CI/CD changes)

**Produce:**
- A flat change inventory: `[CREATE/MODIFY/DELETE] path/to/file — reason`

### Step 2: Identify Dependencies Between Changes

**For each change, ask:**
- Does this change depend on another change being done first?
- Does this change break anything that must be fixed in the same step?
- Can this change be deployed independently, or does it require other changes to be in production simultaneously?

**Produce:**
- A dependency graph (even a simple ordered list suffices)

### Step 3: Order Changes to Minimize Risk

**Principles:**
1. Infrastructure and interfaces before implementations
2. Tests before or alongside implementation (TDD style)
3. Independent changes before dependent ones
4. Lower-risk changes first to build confidence
5. Changes that can be feature-flagged are lower risk

**Anti-patterns to avoid:**
- Giant refactors in a single step
- Deleting things before replacement is confirmed working
- Changing public interfaces while their callers are also being changed

### Step 4: Define Each Step

For each ordered step:

```
## Step N: [Descriptive name]

**Type:** [Create / Modify / Delete / Configure]
**Files:** [list of files affected]
**Description:** [What this step does and why]
**Output:** [What the codebase looks like after this step — should still compile/run]
**Validation:** [How to verify this step is correct before proceeding]
**Reversibility:** [How easy is this to undo? Low/Medium/High risk]
**Approval required:** [Yes / No — flag destructive steps]
```

### Step 5: Identify Approval Gates

Every step that involves:
- Deleting files
- Modifying database schema
- Changing authentication/authorization
- Changing public APIs (breaking changes)
- Modifying CI/CD pipelines

...requires explicit human approval before execution.

Mark these steps with `⚠️ REQUIRES APPROVAL`.

### Step 6: Present the Plan for Human Review

Present the complete plan and explicitly request human approval before beginning.

Ask: "Please review this implementation plan. Reply 'proceed' to begin, or provide feedback to revise the plan."

**Do not begin Step 1 until the human approves.**

## Decision Points

| Condition | Tier | Action |
|-----------|------|--------|
| A step requires deleting files | Approve | Explicitly list files to be deleted; require confirmation |
| A step requires a database migration | Approve | "Step X requires a migration. This is irreversible in production. Confirm?" |
| A step requires changing a public API | Approve | List all callers affected; request confirmation |
| The plan would take more than ~20 steps | Consult | Suggest phasing the work; ask human which phase to implement first |

## Safety Constraints

- Never begin implementation without an approved plan
- Never delete any file without explicit human confirmation of that specific deletion
- Never make a change that leaves the codebase in a broken state at the end of a step
- Flag every step that cannot be easily reversed
- Never modify `.env`, production configuration, or CI/CD without human approval

## Expected Output

A numbered implementation plan document containing:
- Change inventory
- Ordered steps, each with description, files, validation, and reversibility
- Clearly marked approval gates
- Explicit request for human review and approval

## Validation

- [ ] Every file to be changed is listed
- [ ] Steps are ordered correctly (dependencies satisfied)
- [ ] Each step leaves the codebase in a working state
- [ ] Destructive steps are flagged
- [ ] Human has approved before Step 1 begins

## Failure Handling

| Failure | What to do |
|---------|------------|
| Dependency analysis reveals circular dependencies | Flag to human; redesign may be needed |
| Step list grows to 30+ steps | Recommend phasing; implement Phase 1 only |
| Human makes changes mid-plan that invalidate later steps | Stop, re-plan from the current state |

## Examples

### Example 1: Adding email notifications to an existing service

**Step 1:** Add `EmailService` interface + `SendGridEmailService` implementation
- Files: `src/notifications/email_service.py` [CREATE]
- Validation: `pytest tests/unit/test_email_service.py` passes

**Step 2:** Add unit tests for `EmailService`
- Files: `tests/unit/test_email_service.py` [CREATE]
- Validation: Tests pass with mock SendGrid client

**Step 3:** Wire `EmailService` into report completion handler
- Files: `src/reports/completion_handler.py` [MODIFY]
- Validation: Existing completion handler tests still pass

**Step 4:** Add integration test for full notification flow
- Files: `tests/integration/test_report_notification.py` [CREATE]

**Step 5:** ⚠️ REQUIRES APPROVAL — Add `SENDGRID_API_KEY` to environment configuration
- Files: `.env.example` [MODIFY], deployment config [MODIFY]

## Related Skills

- `architecture-design` — must run and be approved before this skill
- `tdd` — use alongside implementation for test-driven development
- `code-review` — run after each step or at end of implementation
