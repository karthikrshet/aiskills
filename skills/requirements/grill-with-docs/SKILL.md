---
name: grill-with-docs
description: |
  Use this skill to conduct an interactive requirements grilling session that
  builds a shared ubiquitous domain language, updates CONTEXT.md with domain
  glossaries, and records hard-to-explain architectural decisions into ADRs.
version: "0.1.0"
category: requirements
tags: [interview, domain-driven-design, ubiquitous-language, context, adr, requirements]
risk: low
status: alpha
related-skills:
  - grill-me
  - requirements-analysis
  - architecture-design
---

# Grill with Docs (Domain Language & ADR Alignment)

## Purpose

The single biggest failure mode in AI coding is misalignment and verbosity. When coding agents don't understand the project's specific domain jargon, they write 20 vague words where 1 precise domain term would suffice, causing confusion, conversational bloat, and architectural drift.

This skill conducts a deep interactive interview that achieves two critical outcomes simultaneously:
1. **Uncovers hidden edge cases** and aligns on what to build before code is written.
2. **Builds a Ubiquitous Language** (Domain-Driven Design), updating `CONTEXT.md` with domain terms and capturing complex trade-offs in Architecture Decision Records (`templates/ADR.md`).

## When to Use

- Starting any non-trivial feature, refactor, or greenfield system
- When the human wants to think deeply through requirements before coding
- When introducing a new domain concept or entity into the codebase
- Before writing a PRD, SPEC, or implementing architecture

## When Not to Use

- Trivial, 1-line typo fixes
- Pure exploration where code will be completely thrown away

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Feature request / idea | ✅ | What the human wants to build |
| CONTEXT.md | optional | Current project domain terminology |
| Existing ADRs | optional | Historical decisions in the repository |

## Preconditions

- [ ] Agent has read `CONTEXT.md` to see existing terms and conventions
- [ ] Agent is in interactive mode with the human

## Workflow

### Step 1: Probe the Requirements

Ask 3–4 focused, architectural questions about:
- **Domain nouns & verbs:** What are the exact terms for this feature?
- **State transitions:** What states can this entity exist in?
- **Boundary conditions:** What are the non-happy paths, error states, and permissions?

### Step 2: Extract Ubiquitous Domain Language

Identify recurring complex descriptions that can be replaced with concise, unambiguous domain terms:
- *Before:* "When a lesson inside a course section gets created on disk..."
- *After (Ubiquitous Term):* **"Materialization Cascade"**

### Step 3: Update `CONTEXT.md` Glossary

Add newly agreed terms and their definitions to `CONTEXT.md` under the Domain Glossary section. This ensures every future agent session speaks the exact same language.

### Step 4: Draft Architecture Decision Records (ADRs)

For every significant technical trade-off decided during the interview (e.g. database choice, sync vs. async, storage format), draft an ADR in `templates/ADR.md` or `.agents/adr/`.

### Step 5: Summarize Aligned Plan

Present the finalized specification summary and confirm alignment with the human before starting implementation.

## Decision Points

| Condition | Tier | Action |
|-----------|------|--------|
| A decision involves non-obvious trade-offs | Consult | Draft an ADR and ask human to confirm the chosen alternative |
| New domain term conflicts with existing codebase term | Consult | Clarify the distinction and record both in `CONTEXT.md` |

## Safety Constraints

- Never start writing code until grilling is complete and domain terms are recorded
- Never introduce ambiguous jargon without defining it in `CONTEXT.md`
- Keep questions focused on architectural and domain boundaries

## Expected Output

- Updated `CONTEXT.md` with new Ubiquitous Language terms
- One or more drafted ADRs for key decisions
- Completed feature spec ready for `task-decomposition` or `tdd`

## Validation

- [ ] At least 3 deep questions were asked and answered
- [ ] At least one domain term was defined or confirmed in `CONTEXT.md`
- [ ] Non-obvious trade-offs are documented in an ADR
- [ ] Human confirmed the final aligned plan

## Failure Handling

| Failure | What to do |
|---------|------------|
| Human is unsure of terminology | Propose 2 concise industry-standard domain terms and let human pick |

## Examples

### Example 1: Defining Domain Jargon

**Human:** "We need a way for users to save a draft of their report, but if they don't touch it for 7 days, it gets archived, but they can still restore it unless the workspace admin purges it."

**Agent alignment:**
- Ubiquitous Terms defined:
  - `Draft Staging`: active editing state (< 7 days).
  - `Dormant Archive`: auto-archived state (7–30 days).
  - `Tombstone Purge`: permanent admin deletion.
- Added terms to `CONTEXT.md`.
- Drafted ADR-003: "Two-stage draft retention and purging policy".

## Related Skills

- `grill-me` — rapid interview for non-code tasks
- `requirements-analysis` — formal requirements documentation
- `architecture-design` — system architecture modeling
