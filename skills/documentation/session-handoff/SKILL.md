---
name: session-handoff
description: |
  Use this skill to compress and serialize the current engineering session state
  into a structured handoff document. Captures completed work, modified files,
  key architectural decisions, test status, open blockers, and exact next steps
  for another agent or future session to resume work without context loss.
version: "0.1.0"
category: documentation
tags: [handoff, session, context, compression, state, resume, continuity]
risk: low
status: alpha
related-skills:
  - repository-discovery
  - implementation-planning
  - context-engineering
---

# Session Handoff

## Purpose

Long-running agent conversations suffer from context window degradation, token exhaustion, and abrupt session termination. When a human resumes work tomorrow, or a new agent session starts, valuable context about what was modified, why certain decisions were made, and what remains to be done is often lost.

This skill provides a structured methodology to compress the full conversational history and working tree status into a dense, high-signal handoff summary. It allows any engineer or agent to resume work seamlessly with zero discovery overhead.

## When to Use

- Ending a working session before switching tasks or closing the IDE
- Context window is approaching capacity (>80% used)
- Passing work from one AI agent to another (e.g. planner to executor)
- When a task is partially completed and awaiting human input or overnight run
- Before compacting or clearing conversation history

## When Not to Use

- After a single, completed trivial query where no work remains
- When no files were modified or investigated

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Current conversation history | ✅ | Recent interactions, decisions, and command outputs |
| Git status & diff summary | ✅ | Working tree changes and modified files |
| Current goal / task description | ✅ | The primary objective being worked on |

## Preconditions

- [ ] Agent has checked `git status` and test suite status
- [ ] Agent knows the current progress state against the original task goal

## Workflow

### Step 1: Inspect Working Tree State

**Run and inspect:**
- `git status` (staged, unstaged, and untracked files)
- Test suite results (passing, failing, or unrun tests)

### Step 2: Extract Completed vs. Remaining Work

**Categorize:**
- **Completed:** Specific files created/modified and behaviors implemented and tested.
- **In Progress:** Half-finished functions, broken tests, or pending refactors.
- **Remaining:** Next immediate tasks in the implementation plan.

### Step 3: Record Key Decisions and Rationale

Document any non-obvious choices made during the session so the next agent does not reverse them or repeat discarded experiments.

### Step 4: Formulate the Resumption Prompt

Draft a clear, single-paragraph prompt that the human or next agent can execute to resume work immediately.

### Step 5: Output the Handoff Document

Output the handoff document formatted in markdown:

```markdown
# Session Handoff: [Task Name]
**Date / Timestamp:** [YYYY-MM-DD HH:MM]
**Branch:** [git branch]

## 1. Goal
[1-2 sentences on the objective]

## 2. Completed Work
- [x] [Item 1 and files touched]
- [x] [Item 2]

## 3. Current Working Tree
- `modified:` [path/to/file]
- `created:` [path/to/file]
- `tests:` [e.g. 14 passed, 1 failing in test_auth.py]

## 4. Key Decisions & Context
- [Decision 1 and reason]

## 5. Immediate Next Steps
1. [Next concrete action]
2. [Following action]

## 6. Resumption Command
```
[Prompt or command to resume]
```
```

## Decision Points

| Condition | Tier | Action |
|-----------|------|--------|
| Tests are currently failing at handoff | Inform | Explicitly highlight the exact failing test and stack trace in the handoff note |
| Uncommitted changes exist on a shared branch | Consult | Ask user whether to create a WIP commit or leave working tree dirty |

## Safety Constraints

- Never include raw credentials, tokens, or private secrets in the handoff document
- Never pretend tests are passing if they were not run or failed
- Keep the handoff concise (under 150 lines) to preserve context budget

## Expected Output

- A clean markdown handoff document (printed in chat or saved to `.aiskills/HANDOFF.md` if requested)
- An actionable resumption prompt

## Validation

- [ ] All modified files are listed
- [ ] Test status is accurately reported
- [ ] Immediate next step is concrete and verifiable
- [ ] No secrets or PII are exposed

## Failure Handling

| Failure | What to do |
|---------|------------|
| Cannot determine git status | Base handoff on files edited during the session and state that git status could not be verified |

## Examples

### Example 1: Handoff during RAG Chunking Optimization

```markdown
# Session Handoff: RAG Section Chunking
**Goal:** Implement section-aware markdown chunker for documentation search.

## Completed Work
- Created `src/rag/chunkers/section_chunker.py`
- Implemented heading hierarchy parser (H1-H4)

## Current State
- `tests/unit/test_section_chunker.py` has 4 passing tests and 1 failing test (`test_table_boundary_preservation`)

## Immediate Next Step
- Fix table boundary preservation in `section_chunker.py:L84` so multi-row tables are not split across chunks.
```

## Related Skills

- `context-engineering` — context budget management
- `repository-discovery` — codebase onboarding
- `implementation-planning` — task sequencing
