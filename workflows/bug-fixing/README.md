# Bug Fixing Workflow

This workflow guides an AI coding agent through systematically diagnosing and fixing a bug.

---

## Workflow Stages

```
Stage 1: Reproduce the Bug
    ↓
Stage 2: Root Cause Analysis
    ↓
Stage 3: Write Regression Test
    ↓
Stage 4: Implement Fix
    ↓
Stage 5: Verify Fix
    ↓
Stage 6: Code Review
    ↓
Stage 7: Document
```

---

## Stage Details

### Stage 1: Reproduce (`bug-diagnosis` — Step 1)

- Confirm the bug is reproducible
- Write the smallest possible reproduction case
- If not reproducible: ask human for more information

**Exit criterion:** Deterministic reproduction case exists.

---

### Stage 2: Root Cause Analysis (`bug-diagnosis`)

- Read the error carefully (full stack trace, error type)
- Isolate scope (which component, which input triggers it)
- Trace causation backward from symptom to origin
- Identify root cause (earliest incorrect point in the chain)

**Exit criterion:** Root cause statement written: "Root cause: [specific location and reason]"

---

### Stage 3: Write Regression Test (`tdd`)

Before writing the fix:
- Write a test that fails because of the root cause
- Confirm the test fails for the right reason

**Exit criterion:** Failing regression test exists.

---

### Stage 4: Implement Fix

- Fix only the root cause — not the symptoms
- Make the smallest change that addresses the root cause
- Do not refactor unrelated code in the same commit

---

### Stage 5: Verify Fix

- Run the regression test — must pass
- Run the full test suite — no new failures
- Manually verify the original bug scenario if needed

---

### Verification Gate ✅

| Check | Required |
|-------|---------|
| Regression test passes | ✅ |
| Full test suite passes | ✅ |
| Fix addresses root cause (not symptom) | ✅ |
| No new failures introduced | ✅ |

---

### Stage 6: Code Review (`code-review`)

- Review the fix for correctness, edge cases, side effects
- Ensure no debugging artifacts remain (print statements, etc.)

---

### Stage 7: Document

- Add clear commit message: "fix: [description of what was fixed and why]"
- Update CHANGELOG if user-facing
- Note: "Fixes #[issue number]" in commit if applicable

---

*Part of AISkills v0.1.0*
