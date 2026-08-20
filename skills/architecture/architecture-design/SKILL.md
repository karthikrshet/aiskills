---
name: architecture-design
description: |
  Use this skill to design system architecture with documented trade-offs and
  decisions before any implementation begins. Activates when a feature, system,
  or component requires non-trivial structural decisions about how components
  interact, what data stores to use, or how to decompose a problem.
version: "0.1.0"
category: architecture
tags: [architecture, design, system-design, ADR, trade-offs, components]
risk: medium
status: alpha
related-skills:
  - repository-discovery
  - requirements-analysis
  - implementation-planning
  - architecture-design
---

# Architecture Design

## Purpose

Poorly designed architecture is expensive to reverse. An agent that begins implementation without an architecture design produces code that is correct in isolation but incoherent as a system — leading to rework, tight coupling, missing interfaces, and undocumented decisions that future engineers cannot understand.

This skill provides a structured process for producing an architecture design grounded in the actual codebase, with documented decisions, trade-offs, and an Architecture Decision Record (ADR) for each significant choice.

## When to Use

- A new system, service, or significant component is being designed
- An existing system is being significantly changed or extended
- Multiple valid architectural approaches exist and one must be chosen
- The task involves introducing a new data store, external service, or AI component
- An ADR is needed for an architectural decision

## When Not to Use

- The change is a small bug fix or minor feature with no architectural implications
- Architecture has already been designed and documented
- The task is a refactor of existing structure (use `refactoring` skill instead)

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Requirements document | ✅ | Completed output of `requirements-analysis` |
| Repository context | ✅ | Output of `repository-discovery` |
| Existing architecture documentation | optional | ADRs, design docs, CONTEXT.md |

## Preconditions

- [ ] Requirements are documented and major ambiguities resolved
- [ ] Repository discovery is complete
- [ ] Agent has read existing ADRs if present

## Workflow

### Step 1: Identify Architectural Decisions Required

**Analyze requirements for decisions about:**
- Component decomposition: how to split the system into parts
- Data persistence: what data stores, schemas, and access patterns
- Service boundaries: what is in this system vs. external
- Communication patterns: synchronous (REST, gRPC), asynchronous (queue, event), or direct
- AI-specific decisions: which model, which provider, RAG vs. fine-tuning, retrieval strategy

**Produce:**
- A numbered list of architectural decisions to be made, ordered by dependency (decisions that other decisions depend on come first)

### Step 2: For Each Decision — Evaluate Alternatives

For each decision:

1. **State the decision clearly:** "We need to choose a vector database for storing embeddings."
2. **Identify concrete alternatives:** List 2–4 real options (not "Option A" / "Option B")
3. **Evaluate each against:** requirements, constraints, existing stack, team familiarity, cost, operational complexity
4. **Identify trade-offs:** No option is perfect — what does each sacrifice?
5. **Make a recommendation:** Based on the requirements, which alternative is best?

**Never evaluate an alternative without naming it specifically.**

### Step 3: Check Against Existing Architecture

**Inspect the codebase:**
- Does a similar component already exist? Can it be reused?
- Does the proposed design contradict existing patterns?
- Does it introduce a new technology that duplicates something already in the stack?
- Does it require a change to an existing public interface?

**Produce:**
- Confirmation that the design is consistent with existing architecture, or a list of conflicts to discuss

### Step 4: Create Architecture Decision Records

For each significant architectural decision, write an ADR using `templates/ADR.md`.

A decision is "significant" if:
- It affects more than one component
- It introduces a new technology or dependency
- It is difficult to reverse
- Future engineers are likely to question it

### Step 5: Produce System Design Document

Using `templates/DESIGN.md`, document:
- System context and actors
- Component breakdown with responsibilities
- Data architecture and key data flows
- API design (if applicable)
- Non-functional design (performance, reliability, observability)
- Security design
- Open decisions requiring human input

### Step 6: Get Human Approval Before Implementation

**Required gate:** Present the architecture to the human and obtain explicit approval.

Include:
- Summary of the design
- List of significant decisions and their rationale
- Known trade-offs being accepted
- What is not yet decided (open questions)

**Do not begin implementation until the human approves the architecture.**

## Decision Points

| Condition | Tier | Action |
|-----------|------|--------|
| Two alternatives are equally valid | Consult | Present both with trade-offs; let human decide |
| Proposed design requires changing an existing public API | Approve | "This design requires changing [API X]. This affects [Y callers]. Confirm?" |
| Design introduces a new cloud provider or significant external dependency | Approve | "This design requires [new service]. This adds cost/complexity. Confirm?" |
| No clear winner between alternatives | Consult | Ask human which constraint takes priority |

## Safety Constraints

- Never begin implementation before architecture is approved
- Never propose an architecture that contradicts hard constraints without explicitly surfacing the conflict
- Never invent architectural facts — always inspect the codebase first
- Never omit trade-offs from a recommendation — every choice sacrifices something

## Expected Output

- One or more ADRs for significant decisions (`templates/ADR.md`)
- System design document (`templates/DESIGN.md`)
- Written request for human architecture review and approval

## Validation

- [ ] Every significant decision has an ADR
- [ ] Each ADR includes at least 2 alternatives with explicit trade-offs
- [ ] Design is grounded in actual codebase inspection (not invented)
- [ ] No hard constraints are violated
- [ ] Human has been asked to approve before implementation proceeds

## Failure Handling

| Failure | What to do |
|---------|------------|
| Requirements are insufficiently specified to design | Return to `requirements-analysis` |
| All alternatives violate a hard constraint | Report to human; constraints may need revision |
| Existing architecture is so complex that discovery is insufficient | Ask human for an architecture walkthrough before proceeding |

## Examples

### Example 1: RAG system architecture for a document Q&A system

**Decisions identified:**
1. Embedding model (affects retrieval quality and cost)
2. Vector database (affects query performance and operational complexity)
3. Chunking strategy (affects retrieval precision)
4. Retrieval method (dense vs. hybrid)

**Decision 2 — Vector database:**
- Option A: Pinecone (fully managed, $$$, fast setup)
- Option B: pgvector (Postgres extension, already in stack, lower cost, some performance limits)
- Option C: Qdrant (open-source, self-hosted, excellent performance, operational overhead)

Recommendation: pgvector — already in stack, avoids new dependency, cost-effective at anticipated scale. Trade-off: may need to migrate to Qdrant if query volume exceeds 10M vectors.

**ADR-001 written. DESIGN.md updated. Human approval requested.**

## Related Skills

- `repository-discovery` — must run before this skill
- `requirements-analysis` — provides the requirements that constrain design choices
- `implementation-planning` — runs after architecture approval
- `rag-architecture` — specialized architecture skill for RAG systems
- `agent-design` — specialized architecture skill for AI agents
