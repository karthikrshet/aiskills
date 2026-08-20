---
name: code-review
description: |
  Use this skill to systematically review code changes for correctness, security,
  performance, maintainability, and test coverage. Activates after implementation,
  before merging, or when asked to review a pull request or code change.
  Produces a structured review report with findings categorized by severity.
version: "0.1.0"
category: code-review
tags: [code-review, quality, security, correctness, maintainability, testing]
risk: low
status: alpha
related-skills:
  - tdd
  - bug-diagnosis
  - ai-security-review
  - implementation-planning
---

# Code Review

## Purpose

AI-generated code is frequently correct in isolation but problematic in context: it may introduce subtle bugs, miss security implications, bypass established project conventions, or lack adequate test coverage for edge cases. Standard "does it compile and pass tests?" validation misses these issues.

This skill provides a structured, multi-dimensional code review methodology that covers correctness, security, performance, maintainability, and documentation. It produces a categorized report of findings, distinguishing blocking issues from minor improvements.

## When to Use

- After implementing a feature or bug fix, before merging
- When reviewing a pull request from another agent or developer
- When asked to "review this code" or "check for issues"
- Before declaring implementation complete
- When implementation involves security-sensitive logic

## When Not to Use

- The code has already been reviewed and approved
- The change is purely documentation or configuration (use appropriate checklist instead)

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Code change or set of files | ✅ | The diff, files, or PR to review |
| Requirements / acceptance criteria | ✅ | What the code is supposed to do |
| Repository conventions | optional | Output of `repository-discovery` |

## Preconditions

- [ ] Agent has access to the full diff or changed files
- [ ] Agent has access to relevant existing code for context
- [ ] Test suite can be run

## Workflow

### Step 1: Run Automated Checks First

Before manual review, run all automated checks:

```bash
# Linting
ruff check .          # Python
eslint src/           # JS/TS
golangci-lint run     # Go

# Formatting
ruff format --check . # Python

# Type checking
mypy src/             # Python
tsc --noEmit          # TypeScript

# Tests
pytest tests/ -v      # Python
npm test              # JS/TS
```

**Record:** pass/fail for each check.

### Step 2: Review for Correctness

**For each changed function or method, ask:**

- Does it do what the requirement says it should do?
- Are all code paths handled? (check all `if/elif/else` branches)
- Is the logic correct for edge cases: null/None, empty string, empty list, zero, negative numbers?
- Are error cases handled? Are exceptions caught appropriately (not silently swallowed)?
- Are all function inputs validated?
- Is the output format and type correct?

**Flag:**
- Missing branches
- Unchecked null/None values
- Silent exception swallowing (`except: pass`)
- Wrong algorithmic logic
- Off-by-one errors

### Step 3: Review for Security

**Check:**

- [ ] No hardcoded secrets, API keys, or credentials
- [ ] User inputs are validated before use
- [ ] Database queries use parameterized queries (not string formatting)
- [ ] Shell commands are not constructed from user input
- [ ] File paths from user input are sanitized (path traversal check)
- [ ] Sensitive data is not logged
- [ ] Authentication and authorization are checked at the right layer
- [ ] LLM outputs are sanitized before use in downstream systems
- [ ] Retrieved content is not executed or evaluated

### Step 4: Review for Performance

**Check:**

- [ ] No N+1 database queries (query in a loop without batching)
- [ ] Appropriate use of caching
- [ ] No blocking I/O in async contexts
- [ ] Large data structures loaded into memory unnecessarily
- [ ] LLM token usage reasonable (not sending entire codebase as context)
- [ ] Embedding calls batched, not per-item in a loop

### Step 5: Review for Maintainability

**Check:**

- [ ] Function/class names clearly describe their purpose
- [ ] Functions do one thing (single responsibility)
- [ ] No magic numbers or magic strings — use named constants
- [ ] No dead code (commented-out code, unused imports, unreachable branches)
- [ ] Complex logic has explanatory comments
- [ ] Follows project naming conventions
- [ ] No unnecessary complexity (over-engineering)
- [ ] No copy-paste duplication

### Step 6: Review Tests

**Check:**

- [ ] Tests exist for new functionality
- [ ] Tests cover happy path AND edge cases AND error cases
- [ ] Test names describe what is being tested
- [ ] Tests do not use real external services or credentials
- [ ] Tests are deterministic (no timing dependencies, no random behavior without seeding)
- [ ] No test asserts only that no exception was thrown (assert something meaningful)

### Step 7: Review Documentation

**Check:**

- [ ] Public APIs have docstrings
- [ ] README updated if setup/install/usage changed
- [ ] CHANGELOG updated if the change is user-facing
- [ ] ADRs updated if architectural decisions were made or changed
- [ ] Inline comments explain *why*, not *what*

### Step 8: Produce Review Report

Using `templates/REVIEW.md`, produce a structured review report:

- Categorize findings: Blocking / Major / Minor / Nit
- For each finding: location, description, suggested fix
- Final decision: Approved / Changes Required / Rejected

## Decision Points

| Condition | Tier | Action |
|-----------|------|--------|
| Security finding (hardcoded credential, injection vector) | Approve | Stop; report immediately; do not suggest it's a "nice to fix" |
| Blocking correctness issue | Inform | Mark as blocking; implementation must fix before merge |
| Missing tests for critical path | Inform | Mark as major; do not approve without tests for critical logic |

## Safety Constraints

- Never approve code with hardcoded credentials
- Never approve code with unhandled injection vectors
- Never approve code that silently swallows exceptions in security-sensitive paths
- Always run automated checks before manual review — do not skip linting/tests

## Expected Output

A completed review report (`templates/REVIEW.md`) with:
- Automated check results
- Categorized findings (Blocking/Major/Minor/Nit)
- Specific file + line references for each finding
- Suggested fixes
- Final review decision

## Validation

- [ ] All 7 review dimensions were checked (not just correctness)
- [ ] Automated checks were run and results recorded
- [ ] Every blocking issue has a specific suggested fix
- [ ] Review decision is clearly stated

## Failure Handling

| Failure | What to do |
|---------|------------|
| Code is too large to review in one pass | Review the highest-risk components first; note that full review is incomplete |
| Automated checks cannot run (environment issue) | Note it in the review; flag as a setup problem; proceed with manual review |
| Code change contradicts an ADR | Flag as blocking: "This change contradicts ADR-001. Please review." |

## Examples

### Example 1: Review of RAG retrieval function

**Finding CR-001 (Blocking — Security):**
> `retrieval.py:47`: User query is embedded directly in a PostgreSQL `LIKE` query using string formatting. This creates a SQL injection vector. Use parameterized queries.

**Finding CR-002 (Major — Correctness):**
> `retrieval.py:89`: If `results` is empty, `results[0]` raises `IndexError`. Add an empty-list check.

**Finding CR-003 (Minor — Maintainability):**
> `retrieval.py:12`: Magic number `0.8` — document this threshold as a named constant `MINIMUM_RELEVANCE_SCORE`.

**Decision:** Changes Required — resolve CR-001 and CR-002 before merge.

## Related Skills

- `tdd` — ensures tests exist before review
- `ai-security-review` — deeper AI-specific security review if AI components are involved
- `bug-diagnosis` — investigate any correctness issues found during review
