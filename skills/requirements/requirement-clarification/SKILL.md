---
name: requirement-clarification
description: |
  Use this skill to detect and resolve specific requirement ambiguities through
  structured questioning. Activates when requirements contain vague language,
  conflicting statements, unstated assumptions, or missing decisions. Run after
  requirements-analysis identifies gaps, or before design begins.
version: "0.1.0"
category: requirements
tags: [requirements, clarification, ambiguity, questions, scoping]
risk: low
status: alpha
related-skills:
  - requirements-analysis
  - architecture-design
---

# Requirement Clarification

## Purpose

Requirement ambiguity is expensive to discover during implementation. Each ambiguous decision left unresolved becomes a hidden assumption that may need to be reversed later, at high cost.

This skill provides a structured methodology for identifying ambiguities in requirements and formulating precise, targeted questions to resolve them — before design or implementation begins. The goal is one well-formed question per ambiguity, not a questionnaire that overwhelms the human.

## When to Use

- `requirements-analysis` has identified open questions
- Requirements contain language like: "fast", "secure", "scalable", "simple", "modern", "standard", "normal"
- A requirement could be interpreted in more than one valid way
- Assumptions are being made that are not explicitly confirmed
- The agent is about to make a design decision that should be a human decision

## When Not to Use

- Requirements are already fully specified and unambiguous
- The ambiguity is trivially resolved by inspecting the codebase
- The question is a technical implementation choice, not a requirement decision

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Requirements document or description | ✅ | The requirements to analyze for ambiguity |
| Open questions list | optional | Output from `requirements-analysis` |

## Preconditions

- [ ] Requirements have been collected in some form
- [ ] Agent has read `CONTEXT.md` if present (some ambiguities are answered there)

## Workflow

### Step 1: Identify All Ambiguous Language

**Scan requirements for:**
- **Vague qualifiers:** "fast", "slow", "good", "bad", "simple", "complex", "large", "small", "robust", "secure" — none of these are measurable
- **Missing subjects:** "should be authenticated" — authenticated by whom? via what mechanism?
- **Missing scope boundaries:** "handles all file types" — all file types in existence?
- **Implicit assumptions:** "the user" — which user? authenticated? anonymous?
- **Competing interpretations:** two technically valid readings of the same sentence

**Produce:**
- A numbered list of ambiguities, each with the problematic phrase quoted

### Step 2: Classify Each Ambiguity

Classify each ambiguity by type:

| Type | Description | Example |
|------|-------------|---------|
| **Measurement** | Qualifier without metric | "Fast" — fast means different things |
| **Scope** | Boundary not defined | "All users" — all users where? |
| **Decision** | Choice not yet made | "Authentication" — which method? |
| **Assumption** | Unstated belief | "Will run on mobile" — never mentioned |
| **Conflict** | Two requirements contradict | FR-001 says X; FR-003 implies not-X |
| **Missing** | Required information entirely absent | Latency target never mentioned |

### Step 3: Prioritize by Impact

Classify each ambiguity:

- **Blocking:** Cannot proceed with design/implementation until resolved
- **Non-blocking:** Can make a reasonable default; document the assumption; revisit if wrong

Skip non-blocking ambiguities in the question list — just document the assumption made.

### Step 4: Formulate Targeted Questions

For each blocking ambiguity, write one precise question:

**Bad question format:**
> "Can you tell me more about the authentication requirements?"

**Good question format:**
> "FR-003 requires authentication. Should this use the existing OAuth 2.0 SSO system, API key authentication, or a new username/password flow? (Context: the current codebase already has OAuth 2.0 implemented in `src/auth/`.)"

**Question formula:**
1. Reference the specific requirement (FR-003)
2. State the specific ambiguity (which auth method)
3. Offer concrete options where possible (not open-ended)
4. Add relevant context (existing system)

### Step 5: Present Questions in Priority Order

Present only blocking questions to the human, ordered by architectural impact (decisions that affect the most other decisions come first).

Limit: present a maximum of 5 questions at once. If there are more, address the top 5 first.

### Step 6: Process Answers and Update Requirements

For each answer received:
- Update the requirements document with the clarified requirement
- Remove or close the corresponding open question
- Check if the answer creates new ambiguities (if yes, restart from Step 1)

## Decision Points

| Condition | Tier | Action |
|-----------|------|--------|
| Human is unavailable | Inform | Document assumption as `UNVERIFIED ASSUMPTION [date]` and proceed; flag for review |
| Human gives a vague answer | Consult | Ask for a more specific answer: "To confirm — does 'fast' mean < 200ms for the average response?" |
| Human's answer conflicts with existing system | Consult | "This answer would conflict with [existing system behavior X]. Should we change that?" |
| 10+ questions pile up | Consult | Present only the top 3 blocking ones; explain the rest are non-blocking |

## Safety Constraints

- Never make architectural decisions to resolve requirement ambiguity — always ask the human
- Never proceed with design while blocking ambiguities are unresolved
- Never present more than 5 questions at once
- Always document the assumption made when proceeding without a human answer
- Never re-ask a question the human has already answered

## Expected Output

- A list of resolved ambiguities with the human's answers
- Updated requirements document with ambiguities resolved
- A list of documented assumptions (non-blocking ambiguities resolved by assumption)

## Validation

- [ ] All blocking ambiguities have human answers
- [ ] All non-blocking ambiguities have documented assumptions
- [ ] No requirement still contains unmeasured qualifiers
- [ ] Updated requirements are consistent (no new conflicts introduced)
- [ ] Human has confirmed the final requirements summary

## Failure Handling

| Failure | What to do |
|---------|------------|
| Human cannot answer a blocking question | Document it as a high-priority open question; do not proceed with design in that area |
| New ambiguities appear after each answer | Iterate; limit to 3 cycles before escalating to a synchronous design session |
| Requirements keep changing | Establish a scope freeze; document what is in scope as of [date] and resist scope creep |

## Examples

### Example 1: Clarifying "fast" in a RAG system

**Ambiguity detected:** FR-NFR-001 states "responses should be fast."

**Crafted question:**
> "FR-NFR-001 requires 'fast' responses. Can you specify a target latency? For reference: simple database queries typically take < 50ms; LLM generation typically takes 1–5 seconds. Is the target for the full end-to-end response (including LLM generation), or just for retrieval alone?"

**Human answer:** "Full response under 3 seconds P95 for 90% of queries."

**Output:** FR-NFR-001 updated to: "P95 end-to-end response time MUST be < 3 seconds for the 90th percentile of production queries."

## Related Skills

- `requirements-analysis` — run before this skill to identify all ambiguities
- `architecture-design` — run after ambiguities are resolved
