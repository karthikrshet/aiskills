---
name: bug-diagnosis
description: |
  Use this skill to systematically diagnose the root cause of a bug before
  attempting a fix. Activates when a bug is reported, a test is failing, or
  unexpected behavior is observed. Prevents guess-and-check debugging that
  introduces additional bugs while chasing symptoms.
version: "0.1.0"
category: debugging
tags: [debugging, bug, root-cause, diagnosis, investigation, testing]
risk: low
status: alpha
related-skills:
  - tdd
  - code-review
  - repository-discovery
---

# Bug Diagnosis

## Purpose

Guess-and-check debugging is the most common form of technical debt. An agent that modifies code without understanding the root cause may suppress the symptom while leaving the underlying problem intact — or introduce new bugs while fixing the first one.

This skill provides a systematic debugging methodology: reproduce the bug, isolate its scope, trace causation, identify root cause, verify the diagnosis, then fix. The fix only happens after the root cause is confirmed.

## When to Use

- A bug has been reported by a user or test
- A test is failing unexpectedly
- Behavior observed in production differs from expected behavior
- A recent change appears to have broken something
- An exception or error message is being investigated

## When Not to Use

- The bug has already been diagnosed and the fix is known
- The issue is a configuration problem (not a code bug)
- The "bug" is actually an undocumented feature or design choice

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Bug description or error message | ✅ | What is wrong and how it manifests |
| Steps to reproduce | ✅ or derive them | The sequence of events that trigger the bug |
| Error output / stack trace | optional | Logs, exceptions, or test output |
| Commit or version where it started | optional | Helps narrow the search |

## Preconditions

- [ ] Agent has access to the codebase and test suite
- [ ] Agent has read `CONTEXT.md` for architecture context

## Workflow

### Step 1: Reproduce the Bug

Before investigating cause, confirm the bug is reproducible.

**Actions:**
- If a test is failing: run it — `pytest tests/path/to/test.py::test_name -v`
- If a user report: write the smallest possible test case that reproduces it
- If a production issue: identify the input that triggers it

**If the bug cannot be reproduced:**
- Do not attempt to fix it — ask the human for more information
- Note: "I cannot reproduce this bug with the provided description. To proceed I need [X]."

**Produce:**
- A minimal reproduction case (ideally a failing test)

### Step 2: Read the Error — Carefully

**Inspect:**
- The full error message (not just the last line)
- The full stack trace (trace from the bottom up — the bottom is where the error originated)
- Any surrounding log context

**Common mistakes to avoid:**
- Focusing on the top of the stack trace (the call site) instead of the bottom (the origin)
- Misreading the error type (e.g., `AttributeError: 'NoneType'` means an unexpected `None`, not an attribute bug)

**Produce:**
- The exact error type and message
- The file and line number where the error originated
- The call chain that led to the error

### Step 3: Isolate the Scope

**Determine:**
- Is this bug in a single function? A module? A service interaction? An integration?
- Is it deterministic (always fails) or intermittent (sometimes fails)?
- Does it fail with all inputs or specific inputs? What is special about the failing input?
- Is it a regression (worked before, broke after a change)?

**For regressions:**
- Identify recent commits touching the affected area: `git log --oneline -20 -- path/to/file`
- Consider using `git bisect` for persistent codebases

**Produce:**
- Scope characterization: "This bug occurs in `src/rag/retrieval.py:retrieve()` when the query is empty."

### Step 4: Trace Causation

Working from the reproduction case, trace backward:

1. **What is the final wrong state?** (wrong output, exception, wrong database record)
2. **What produced that state?** (which function call, which branch, which calculation)
3. **What produced that?** (what was the incorrect input to that function)
4. Continue backward until you reach the origin of the incorrect value

**Useful techniques:**
- Add temporary `print()` / `console.log()` statements (remove before committing)
- Use the debugger step-through if available
- Inspect variable values at each step in the call chain

**Produce:**
- A causation chain: "empty query → `vectorize("")` returns zero vector → cosine similarity returns 1.0 for all documents → all documents returned → first result is irrelevant"

### Step 5: Identify Root Cause

Root cause is the **earliest point in the causation chain where the logic is wrong**, not merely where the error is thrown.

**Common root cause categories:**
- Missing validation (null/empty/out-of-range input not checked)
- Off-by-one error
- Wrong assumption about external system behavior
- Race condition or state mutation
- Incorrect algorithm or formula
- Configuration mismatch between environments

**Produce:**
- A root cause statement: "Root cause: `retrieve()` does not validate empty queries before vectorization. Empty string produces a zero vector which has maximum cosine similarity with all stored vectors."

### Step 6: Verify the Diagnosis Before Fixing

Before writing the fix:

1. Write a test that reproduces the bug (if one doesn't exist)
2. Confirm the test fails for the root cause reason
3. Make only the change that addresses the root cause
4. Confirm the test passes
5. Run the full test suite — ensure no regressions

**Do not fix symptoms. Fix root causes.**

## Decision Points

| Condition | Tier | Action |
|-----------|------|--------|
| Bug cannot be reproduced | Inform | Report to human; ask for more information or access to logs |
| Root cause is in a third-party library | Consult | "The root cause is in [library]. We can work around it by [X] or upgrade to version [Y]. Which do you prefer?" |
| Fix requires changing a public API | Approve | "The fix requires changing [API]. This affects [N callers]. Proceed?" |
| Bug is in production system | Approve | Before any fix, present diagnosis and proposed fix; do not apply directly to production |

## Safety Constraints

- Never apply a fix before root cause is confirmed
- Never remove a test to make the test suite pass
- Never suppress an exception without understanding why it's thrown
- Never add a null check "to be safe" without understanding what the null represents
- Remove all temporary debugging statements before committing

## Expected Output

- A written root cause analysis:
  ```
  ## Bug Diagnosis: [Bug title]

  **Symptom:** [What was observed]
  **Root cause:** [The earliest incorrect point in causation]
  **Causation chain:** [step-by-step from input to failure]
  **Fix:** [What to change and why]
  **Regression test:** [Test that will prevent recurrence]
  ```
- A failing test that reproduces the bug
- A fix that makes the test pass without breaking others

## Validation

- [ ] Reproduction case exists and is deterministic
- [ ] Root cause statement names a specific location in code
- [ ] A test for this specific bug has been written
- [ ] Fix addresses root cause, not just symptom
- [ ] Full test suite passes after fix

## Failure Handling

| Failure | What to do |
|---------|------------|
| Bug is non-deterministic (race condition, network timing) | Document reproduction conditions; consider adding retry logic or load testing |
| Causation trace leads outside the repository (external service) | Capture the exact request/response; document it; report to human |
| Multiple plausible root causes | Write a test for each hypothesis; run each test to determine which is correct |

## Examples

### Example 1: RAG returning empty results

**Bug report:** "The RAG search returns no results for single-word queries."

**Step 1 — Reproduce:** `curl -X POST /api/search -d '{"query": "python"}' → []`

**Step 2 — Error:** No error thrown; empty list returned silently.

**Step 3 — Isolate:** Occurs with all single-word queries. Multi-word queries work.

**Step 4 — Trace:** Single-word query → `chunk_text(query)` → returns single chunk → `embed_chunks()` → embedding request with `texts=["python"]` → API returns 1536-dim vector → `search_vectors(embedding, top_k=5)` → `WHERE score > 0.8` → 0 results returned.

**Root cause:** Single-word queries produce embeddings with lower cosine similarity to chunks (which are paragraphs). The threshold `0.8` is too high for short queries. The threshold should be adaptive or the fallback should be triggered.

**Fix:** Lower threshold for short queries (< 3 tokens) to `0.6`; add test for single-word query.

## Related Skills

- `tdd` — write a regression test for the confirmed bug
- `code-review` — review the fix before committing
