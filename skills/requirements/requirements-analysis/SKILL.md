---
name: requirements-analysis
description: |
  Use this skill to analyze, structure, and document ambiguous or incomplete
  requirements before any design or implementation work begins. Activates when
  the human has described a feature, task, or problem that needs to be built,
  but the requirements are not yet fully specified or structured.
version: "0.1.0"
category: requirements
tags: [requirements, analysis, specification, planning, clarification]
risk: low
status: alpha
related-skills:
  - requirement-clarification
  - architecture-design
  - implementation-planning
  - repository-discovery
---

# Requirements Analysis

## Purpose

Vague requirements are the most common root cause of wasted engineering effort. An agent that begins implementation without structured requirements will either build the wrong thing, or discover mid-implementation that critical decisions were never made.

This skill transforms a natural-language task description into a structured, documented requirement set that can drive architecture, implementation planning, and validation. It identifies gaps before any design work begins.

## When to Use

- The human has described a feature, product, or task in natural language
- Requirements appear incomplete, ambiguous, or contradictory
- The agent is about to begin architecture or implementation but has no written requirements
- Multiple interpretations of the request are possible
- The task involves user-facing behavior (not a pure refactor)

## When Not to Use

- The task is a trivial one-liner (e.g., "fix this typo") — do it directly
- Formal requirements already exist in a spec document
- The task is purely technical with no ambiguity (e.g., "upgrade this dependency")

Use `requirement-clarification` alongside this skill to resolve ambiguities.

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Task/feature description | ✅ | The human's original request |
| Repository context | optional | Output of `repository-discovery` skill |
| Existing documentation | optional | PRDs, tickets, user stories already available |

## Preconditions

- [ ] Repository discovery has been completed (or agent has adequate context)
- [ ] Agent has read `CONTEXT.md` if present

## Workflow

### Step 1: Identify the Core Problem

**Ask:**
- What problem is the human actually trying to solve?
- Who experiences this problem? (end user, developer, system)
- Why is this problem worth solving now?

**Produce:**
- A single, clear problem statement: "The system currently [X], which causes [Y] for [Z]."

### Step 2: Extract Functional Requirements

**Analyze the request for:**
- What must the system do? (verbs: create, read, update, delete, notify, validate)
- What must the system NOT do? (explicit exclusions)
- What are the acceptance criteria? (how will we know it's done?)

**Produce:**
- A numbered list of functional requirements in the format: "The system MUST/SHOULD/MAY [action]"
- Use MoSCoW priority: Must Have / Should Have / Could Have / Won't Have

### Step 3: Identify Non-Functional Requirements

**Inspect the request for implicit NFRs:**
- Performance: latency, throughput, load requirements
- Scalability: expected growth, volume
- Security: authentication, data sensitivity, compliance
- Reliability: availability, fault tolerance
- Operability: logging, monitoring, alerting

**Produce:**
- Explicit NFRs with measurable targets where possible
- Note: "NOT SPECIFIED" for NFRs that are implied but not yet defined

### Step 4: Identify Constraints

**Inspect:**
- Technology constraints (must use existing stack, can't add new dependencies)
- Time constraints (deadline)
- Compliance constraints (GDPR, SOC 2, HIPAA)
- Budget constraints (cost per query, infrastructure budget)
- AI-specific constraints: context window limits, model provider restrictions, cost caps

**Produce:**
- List of hard constraints that cannot be violated
- List of soft constraints (preferences, not requirements)

### Step 5: Define Success Criteria

**Ask:**
- How will the human verify this requirement is met?
- What is the minimum viable output?
- What would constitute failure?

**Produce:**
- Acceptance criteria for each major requirement
- Definition of done

### Step 6: Identify Gaps and Ambiguities

**Review each requirement for:**
- Ambiguous language ("fast", "good", "secure", "simple" — not measurable)
- Missing decisions ("authentication" — what method?)
- Unstated assumptions ("will work on mobile" — never mentioned)
- Conflicting requirements

**Produce:**
- A numbered list of gaps and open questions
- Priority: blocking (must resolve before design) vs. non-blocking (can decide during implementation)

## Decision Points

| Condition | Tier | Action |
|-----------|------|--------|
| Blocking ambiguity identified | Consult | Use `requirement-clarification` skill; do not proceed until resolved |
| Requirements seem to describe two separate features | Consult | "This seems like two separate features. Should we scope this to X only?" |
| NFRs are entirely absent | Inform | Note they need to be defined; make conservative assumptions explicit |
| Requirement contradicts existing system behavior | Consult | Flag the contradiction; ask which takes precedence |

## Safety Constraints

- Never begin implementation before requirements are documented
- Never make architectural decisions to resolve requirement ambiguity — always ask the human
- Never assume unstated requirements are out of scope — ask first
- Always make assumptions explicit in writing

## Expected Output

A completed feature specification using `templates/SPEC.md`, containing:

- Clear problem statement
- Numbered functional requirements with MoSCoW priority
- Non-functional requirements with measurable targets
- Explicit constraints
- Success/acceptance criteria
- List of open questions requiring human input

## Validation

- [ ] Every requirement is testable (has a verifiable acceptance criterion)
- [ ] No requirement contains ambiguous qualifiers ("fast", "simple") without a metric
- [ ] All blocking open questions are listed
- [ ] Constraints are distinguished from requirements
- [ ] Definition of done is documented

## Failure Handling

| Failure | What to do |
|---------|------------|
| Task description is a single sentence with no detail | Ask 3 targeted clarifying questions before proceeding |
| Human is unavailable to resolve blocking ambiguities | Document the assumptions made; mark as `UNVERIFIED ASSUMPTION`; flag for review |
| Requirements keep expanding during analysis | Apply scope boundary: document what is in scope and explicitly list what is out of scope |

## Examples

### Example 1: RAG system requirement

**Input:** "We need a RAG system for our internal documentation."

**Agent actions:**
1. Identifies: Who are the users? (internal engineers) What documentation? (Confluence, Notion, PDFs?) What's the search interface? (chat, search bar?) What's the latency requirement? (not specified)
2. Produces functional requirements: system must ingest Confluence pages, system must answer questions in natural language, system must cite sources
3. Identifies NFRs: response time NOT SPECIFIED, accuracy NOT SPECIFIED
4. Identifies constraints: must use existing AWS infrastructure
5. Lists blocking open questions: What's the acceptable hallucination rate? Is PII in the docs? What's the daily query volume?

**Output:** Draft SPEC.md with all fields populated, 5 open questions requiring human input.

## Related Skills

- `requirement-clarification` — resolve specific ambiguities detected in this skill
- `architecture-design` — run after requirements are approved
- `repository-discovery` — run before this skill if codebase context is needed
