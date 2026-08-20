---
name: grill-me
description: |
  Use this skill to conduct an intensive, interactive requirements interview
  with the human. Interrogates assumptions, edge cases, domain models, data
  shapes, error states, and UX subtleties before any specification or design is
  finalized.
version: "0.1.0"
category: requirements
tags: [interview, requirements, interrogation, assumptions, scoping, edge-cases]
risk: low
status: alpha
related-skills:
  - requirements-analysis
  - requirement-clarification
  - architecture-design
---

# Grill Me (Interactive Requirements Interview)

## Purpose

Humans often describe features with high-level goals ("add OAuth login", "build a real-time notification system") while leaving dozens of critical operational, boundary, and domain assumptions unspoken. If an AI agent attempts to build without resolving these, it makes arbitrary assumptions that lead to rework and architectural mismatches.

This skill turns the agent into a relentless, disciplined engineering interviewer. The agent systematically interrogates the user across domain modeling, edge cases, failure states, permission boundaries, and integration constraints until no ambiguity remains.

## When to Use

- Starting a new non-trivial feature or greenfield component
- The user gives a short or ambiguous high-level prompt ("build X for me")
- Designing complex domain models or state machines
- Before writing a PRD, SPEC, or architecture design document
- When the human explicitly asks to be interviewed or grilled on a plan

## When Not to Use

- Trivial, single-line bug fixes or typo corrections
- When comprehensive, unambiguous requirements are already documented and approved
- When the user explicitly requests an immediate rapid prototype without discussion

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Initial idea / feature statement | ✅ | The user's initial high-level request |
| Project context | optional | `CONTEXT.md` or repository discovery findings |
| Existing domain models | optional | Relevant schemas or API definitions |

## Preconditions

- [ ] Agent has read `CONTEXT.md` if available
- [ ] Agent is in interactive mode with the human

## Workflow

### Step 1: Analyze the High-Level Request for Blind Spots

**Inspect the prompt for missing dimensions:**
- **Entity boundaries:** What are the exact nouns, their relationships, and lifetimes?
- **State transitions:** What states can an entity take, and what triggers transitions?
- **Authorization & Multi-tenancy:** Who can see, edit, or delete what?
- **Error & Failure cases:** What happens when downstreams timeout or inputs fail?
- **Scale & Performance:** What are the throughput, volume, and latency expectations?

### Step 2: Formulate 3 to 5 Deep Probing Questions

Formulate questions that force concrete decisions rather than vague generalities:

**Good Question Patterns:**
- *"What should happen when [edge case occurs]? Should it (A) fail silently, (B) retry with backoff, or (C) raise a blocking error to the user?"*
- *"Does entity X belong strictly to a single tenant, or can it be shared across workspaces?"*
- *"If the external payment webhook arrives before the user's checkout session completes, how should state resolve?"*

### Step 3: Present Questions in Batches (Max 4 at a time)

Never overwhelm the user with 20 questions at once. Ask the top 3–4 highest-impact architectural questions first.

### Step 4: Synthesize Answers into Domain Definitions

As the user answers:
1. Confirm the agreed rule.
2. Update the working domain model and state transition table.
3. Identify secondary edge cases surfaced by the answers.

### Step 5: Stop Condition (Convergence)

Continue questioning until:
- All entity relationships and state transitions are explicitly defined.
- Error behaviors for all external integrations are specified.
- The human confirms: *"Requirements are complete."*

## Decision Points

| Condition | Tier | Action |
|-----------|------|--------|
| User gives a vague answer (e.g. "make it standard") | Consult | Propose 2 concrete industry-standard options and ask user to select one |
| User answers contradict existing repository conventions | Consult | Highlight the discrepancy with existing code patterns and ask for preference |
| Interview has reached 4 rounds without convergence | Consult | Propose scoping the feature down to a minimal initial phase |

## Safety Constraints

- Never start writing production code during an interview
- Never ask open-ended questions like "tell me more" without proposing concrete options
- Never proceed with unresolved security or authorization boundaries
- Always record user answers explicitly in notes

## Expected Output

- A finalized domain glossary and entity relationship summary
- State transition matrix
- Documented edge-case rules
- Output ready to feed directly into `requirements-analysis` and `templates/SPEC.md`

## Validation

- [ ] At least 3 deep architectural or boundary questions were asked
- [ ] All entity states and valid transitions are mapped
- [ ] Error behaviors for failure cases are explicitly chosen
- [ ] Human explicitly agreed with the summarized specification

## Failure Handling

| Failure | What to do |
|---------|------------|
| User doesn't know the answer | Provide a recommended default based on existing project conventions and note it as an assumption |
| Scope expands uncontrollably | Flag scope creep; suggest splitting into MVP vs. Phase 2 |

## Examples

### Example 1: Grilling an auth feature request

**User:** "Add Google OAuth login to our web app."

**Agent questions:**
1. *"When a user logs in with Google, if an account already exists with that email address via password login, should we automatically link the accounts or reject the login with an account-linking prompt?"*
2. *"What scopes are required? Just openid/email, or do we need offline refresh tokens for background sync?"*
3. *"If a user's Google domain is not in the allowed corporate whitelist, what exact error message and redirect should they see?"*

## Related Skills

- `requirements-analysis` — use to produce the formal `SPEC.md` after grilling
- `requirement-clarification` — targeted question formulation
- `architecture-design` — technical architecture following requirements alignment
