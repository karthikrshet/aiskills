---
name: rapid-prototyping
description: |
  Use this skill to build disposable, rapid proof-of-concept prototypes and
  spikes to test feasibility, validate API designs, or explore library
  capabilities before committing to a full production architecture.
version: "0.1.0"
category: architecture
tags: [prototype, spike, feasibility, experiment, rapid, disposable]
risk: low
status: alpha
related-skills:
  - architecture-design
  - repository-discovery
  - implementation-planning
---

# Rapid Prototyping (Disposable Spikes)

## Purpose

When tackling unknown technologies, new third-party APIs, or uncertain UX flows, designing a heavyweight production architecture up-front leads to analysis paralysis or bad assumptions.

This skill provides a structured workflow for executing rapid, time-boxed, disposable prototypes (spikes). The objective is not to write production-ready code, but to **answer a specific technical or feasibility question** in the fastest possible manner, extract learnings, and then discard or rebuild cleanly.

## When to Use

- Evaluating an unfamiliar library or external API
- Testing whether a complex algorithm or query performance is viable
- Building a quick UI/UX proof of concept for human feedback
- Comparing two competing technical approaches before writing an ADR
- When the human explicitly requests a quick spike or prototype

## When Not to Use

- Building production features that require strict TDD, security audits, and full test suites
- Routine changes with well-understood existing patterns
- Bug fixes in existing production systems

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Feasibility question / Spike goal | ✅ | What exact question must this prototype answer? |
| Timebox constraint | optional | Maximum time/steps allocated (e.g. 1 hour or 5 steps) |
| Target dependencies | optional | Specific libraries or APIs to test |

## Preconditions

- [ ] A dedicated prototype branch or scratch directory is created
- [ ] The human understands that prototype code is exploratory and not production-ready

## Workflow

### Step 1: Formulate the Core Hypothesis

**Define the single question the spike must answer:**
- *"Can library X parse 100-page complex PDF tables without losing column alignment?"*
- *"Can we achieve sub-100ms vector search latency with pgvector on 1M rows?"*
- *"Does the third-party OAuth provider support token refresh via PKCE?"*

### Step 2: Isolate the Prototype Environment

**Create an isolated workspace:**
- Create a dedicated experiment branch: `git checkout -b spike/<feature-name>`
- Or create an isolated sandbox directory: `scratch/spike_<name>/`
- Never pollute the main application directory with exploratory dependencies.

### Step 3: Implement the Minimal Viable Proof

- Write minimal, direct, un-refactored code focused strictly on proving the hypothesis.
- Mock non-essential downstreams.
- Bypass complex auth/DB setup if not relevant to the core hypothesis.

### Step 4: Measure and Record Findings

- Run the spike against realistic test data.
- Benchmark latency, memory, or quality metrics.
- Record failure modes, quirks, and undocumented API behaviors.

### Step 5: Synthesize Learnings and Decide

**Evaluate against the hypothesis:**
- **Feasible:** Proceed to formal requirements, ADR, and production architecture.
- **Unfeasible / High Risk:** Document why and explore alternative options.

### Step 6: Clean Up / Discard

- Document findings in `templates/ADR.md` or a spike summary.
- Discard exploratory code or mark it explicitly as a scratch reference.

## Decision Points

| Condition | Tier | Action |
|-----------|------|--------|
| Prototype succeeds and user wants to merge it directly to main | Consult | Recommend rewriting cleanly using TDD and `implementation-planning` to avoid technical debt |
| Spike exceeds timebox without proving hypothesis | Consult | Stop; present findings and ask whether to pivot or allocate more time |

## Safety Constraints

- Never deploy raw prototype spike code directly to production
- Never use production customer data or real credentials in exploratory spikes
- Never bypass git branch isolation for spikes

## Expected Output

- A working proof-of-concept script or demo branch
- A written spike report answering the core hypothesis
- Concrete input for an Architecture Decision Record (`templates/ADR.md`)

## Validation

- [ ] Core hypothesis was explicitly tested with real data
- [ ] Latency, memory, or feasibility metrics were recorded
- [ ] Clean recommendation (proceed / pivot) was provided
- [ ] Code was isolated from main branch

## Failure Handling

| Failure | What to do |
|---------|------------|
| Third-party API fails or rate-limits | Log raw error payload; evaluate alternative SDKs or providers |
| Hypothesis is disproven | Document the negative result as a valuable finding that saved production rework |

## Examples

### Example 1: Testing PDF Table Extraction

**Hypothesis:** Can `pdfplumber` extract multi-page financial tables accurately?
1. Agent creates `scratch/spike_pdf/`.
2. Tests extraction on 3 sample financial PDFs.
3. Finds that merged header cells lose column context.
4. **Learning:** Standard extraction fails; requires section-aware custom pre-parser.
5. Feeds findings directly into `rag-architecture` ADR.

## Related Skills

- `architecture-design` — turn prototype learnings into formal design
- `rag-architecture` — evaluate retrieval/ingestion feasibility
- `implementation-planning` — clean production rewrite
