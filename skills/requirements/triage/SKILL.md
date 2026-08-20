---
name: triage
description: |
  Use this skill to systematically triage, categorize, prioritize, and label
  incoming issues, bug reports, and feature requests. Verifies reproducibility,
  identifies affected components, and assigns standardized workflow labels.
version: "0.1.0"
category: requirements
tags: [triage, issues, tickets, labels, priority, bug-reports, backlog]
risk: low
status: alpha
related-skills:
  - bug-diagnosis
  - task-decomposition
  - requirements-analysis
---

# Issue and Ticket Triage

## Purpose

Un-triaged backlogs become chaotic dumping grounds where critical bugs get lost and poorly specified feature requests stall engineering progress.

This skill provides a structured methodology for triaging new issues, bug reports, and tickets. The agent analyzes the problem description, verifies steps to reproduce, maps the affected codebase components, estimates severity and priority, and applies standard triage labels.

## When to Use

- Triaging new GitHub Issues, Linear tickets, or local issue files
- Processing customer bug reports or error telemetry alerts
- Grooming and prioritizing a feature backlog before sprint planning

## When Not to Use

- Writing code to fix a bug (use `bug-diagnosis` and `tdd`)
- High-level architecture design (use `architecture-design`)

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Issue title & description | ✅ | The raw reported issue or feature request |
| Existing project labels | optional | Standard triage labels configured in the repo |
| Codebase context | optional | `CONTEXT.md` to map affected modules |

## Preconditions

- [ ] Agent has read `CONTEXT.md` to understand system architecture
- [ ] Agent has access to the codebase to check referenced files

## Workflow

### Step 1: Classify Issue Type

Determine the fundamental category:
- `type:bug` — Defect in existing expected behavior.
- `type:feature` — Request for new capability.
- `type:enhancement` — Improvement to existing working feature.
- `type:security` — Vulnerability or access-control issue.
- `type:docs` — Documentation gap or error.

### Step 2: Verify Completeness & Reproducibility (For Bugs)

Check whether the report contains:
1. Expected vs. Actual behavior
2. Minimal steps to reproduce
3. Environment details (OS, Python version, dependencies)
4. Stack trace or error log snippet

If critical reproduction details are missing, flag with `status:needs-info`.

### Step 3: Map Affected Components

Inspect repository structure to identify likely affected files or packages (e.g. `area:rag`, `area:auth`, `area:cli`).

### Step 4: Assess Impact & Assign Priority

Assign priority based on severity and blast radius:
- `priority:critical` — System down, data loss, security vulnerability.
- `priority:high` — Core workflow blocked with no workaround.
- `priority:medium` — Non-blocking bug or standard feature.
- `priority:low` — Cosmetic issue, typo, minor polish.

### Step 5: Produce Triage Summary

Output a clean structured triage recommendation:
```markdown
### Triage Summary: [Issue Title]
- **Type:** `type:bug`
- **Area:** `area:retrieval`
- **Priority:** `priority:high`
- **Reproducible:** Yes (reproduction script confirmed)
- **Affected Files:** `src/rag/retrieval.py`
- **Recommended Action:** Execute `bug-diagnosis` on `retrieval.py:L48`.
```

## Decision Points

| Condition | Tier | Action |
|-----------|------|--------|
| Issue is a suspected security vulnerability | Approve | Tag `type:security` and flag for private human review before publishing publicly |
| Issue request conflicts with an existing ADR | Consult | Note the conflict with ADR-XXX and ask human whether to re-open the decision |

## Safety Constraints

- Never close an issue automatically without human confirmation
- Never post credentials or sensitive customer data found in bug logs to public trackers
- Do not apply priority labels without explicit rationale

## Expected Output

- Categorized issue with assigned labels (`type:*`, `area:*`, `priority:*`)
- Verified reproduction notes
- Clear recommended next skill or action

## Validation

- [ ] Issue type correctly identified
- [ ] Affected repository components identified
- [ ] Priority assigned with justified blast radius
- [ ] Clear next step documented

## Failure Handling

| Failure | What to do |
|---------|------------|
| Cannot reproduce reported bug | Label `status:cannot-reproduce` and formulate a polite comment requesting exact environment details |

## Examples

### Example 1: Triaging a RAG Timeout Issue

**Report:** "Search API hangs on queries longer than 50 words."
**Triage Output:**
- `type:bug`
- `area:rag`
- `priority:high`
- **Root Cause Hypothesis:** Tokenizer infinite loop on unhandled punctuation sequence.
- **Next Step:** Run `bug-diagnosis` with a 60-word test query fixture.

## Related Skills

- `bug-diagnosis` — deep root-cause diagnosis
- `task-decomposition` — breaking triaged features into tickets
- `requirements-analysis` — analyzing feature requests
