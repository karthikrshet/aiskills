---
name: agent-design
description: |
  Use this skill to design single-agent or multi-agent AI systems with defined
  boundaries, tools, memory, state, planning, and guardrails. Activates when
  building an AI agent, autonomous workflow, or multi-agent orchestration system.
  Ensures agent scope, permissions, and failure modes are explicitly designed.
version: "0.1.0"
category: ai/agent-design
tags: [agent, multi-agent, tools, memory, planning, guardrails, orchestration, ai]
risk: medium
status: alpha
related-skills:
  - rag-architecture
  - ai-security-review
  - production-readiness
  - context-engineering
---

# Agent Design

## Purpose

AI agents built without explicit design frequently suffer from scope creep, excessive permissions, unhandled tool failures, missing human escalation paths, and no observability. An agent that "almost works" in development can cause serious harm in production by taking unintended actions with real side effects.

This skill provides a structured methodology for designing AI agents before implementation begins — defining what the agent is, what it can do, what it cannot do, how it handles failures, and how humans maintain oversight.

## When to Use

- Building a new AI agent or autonomous workflow
- Adding agency (autonomous decision-making) to an existing system
- Designing a multi-agent orchestration system
- Evaluating the scope and permissions of an existing agent
- Before implementing tool calling, memory, or planning components

## When Not to Use

- Building a simple LLM wrapper with no autonomous behavior (use `rag-architecture`)
- The agent architecture is already fully documented and approved

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Agent goal / task description | ✅ | What the agent is supposed to accomplish |
| Available tools / APIs | optional | What external capabilities are available |
| Constraints | optional | What the agent must never do |

## Preconditions

- [ ] Agent goal is clearly stated and approved
- [ ] Repository discovery complete (to understand existing system context)
- [ ] Requirements documented

## Workflow

### Step 1: Define the Agent Boundary

The most important design decision: **what is this agent responsible for, and what is outside its scope?**

**Define:**
- **In scope:** What tasks, domains, and actions the agent may take
- **Out of scope:** What the agent must never attempt (explicit blocklist)
- **Escalation boundary:** What triggers a hand-off to a human

**Agent types — identify which applies:**
- **Single-step executor:** Takes one action; no planning or state
- **ReAct agent:** Observe → Reason → Act loop; handles multi-step tasks
- **Plan-and-execute:** Generates a full plan before acting; more predictable
- **Multi-agent:** Coordinates with other agents; requires orchestration design

**Produce:**
- Agent boundary document: in-scope, out-of-scope, escalation conditions

### Step 2: Design the Tool Inventory

For each tool the agent may use:

| Tool | Purpose | Permissions | Side effects | Failure behavior |
|------|---------|------------|-------------|-----------------|
| [tool name] | [what it does] | [read/write/exec] | [real-world effects] | [what to do if it fails] |

**Principles:**
- Apply least privilege: grant only the permissions the agent needs for the current task
- Distinguish read tools (safe, no side effects) from write/exec tools (risky, require more caution)
- Every tool that has real-world side effects (sends emails, modifies data, calls APIs) must have explicit human approval requirements

**For each write/exec tool, define:**
- What triggers a human approval request
- What constitutes an irrecoverable action (if so, require approval before every use)

### Step 3: Design Memory Architecture

**Short-term memory (within a session):**
- What does the agent need to remember between steps?
- How is state passed between tool calls?
- What is the context window budget?

**Long-term memory (across sessions):**
- Does the agent need to remember anything across conversations?
- If yes: what? How is it stored? How is it retrieved? How is it updated? When is it deleted?
- Privacy: does long-term memory store user data? What is the retention policy?

**Episodic memory:**
- Does the agent need to recall past tasks?
- What format? (summary, raw transcript, structured log?)

**Produce:**
- Memory architecture table: type, what is stored, storage mechanism, retrieval trigger, retention policy

### Step 4: Design the Planning Approach

**Choose a planning style:**
- **Reactive (ReAct):** Useful for open-ended tasks; less predictable; harder to interrupt
- **Plan-first:** Generate full plan, present to human, then execute; more predictable and auditable
- **Hierarchical:** High-level planner decomposes into sub-tasks for specialist agents

**For any plan-first or hierarchical design:**
- Plans must be human-readable
- Plans must be presented for review before execution begins
- Plans must be revisable

### Step 5: Design Guardrails

**Guardrails are hard constraints that override agent reasoning:**

| Guardrail type | Example | Implementation |
|---------------|---------|----------------|
| Input guardrail | Block prompt injection patterns | Pre-process all inputs |
| Output guardrail | Never output PII | Post-process all outputs |
| Action guardrail | Never delete files without approval | Check before every delete |
| Escalation guardrail | Escalate if uncertainty > threshold | Check confidence before acting |

**Required guardrails for any production agent:**
- [ ] Prompt injection detection on all external inputs
- [ ] Action approval for all irreversible or high-impact actions
- [ ] Escalation to human when confidence is low
- [ ] Rate limiting and budget enforcement on LLM calls and tool calls
- [ ] Output sanitization before passing to downstream systems

### Step 6: Design Observability

**For each agent execution, log:**
- Agent goal and initial context
- Each reasoning step
- Each tool call: tool name, arguments, result, duration
- Planning output (if plan-first)
- Final output
- Total token usage and cost
- Errors and escalations

**Never log:** raw user PII, credentials, or sensitive source content (unless with explicit consent and data classification)

### Step 7: Define Evaluation Criteria

Before building, define how the agent will be evaluated:

- Task completion rate
- Tool-call accuracy (correct tool with correct arguments)
- Unnecessary tool calls (efficiency)
- Human escalation rate (too high = underconfident, too low = overconfident)
- Latency
- Cost per task

## Decision Points

| Condition | Tier | Action |
|-----------|------|--------|
| Agent requires access to production data or systems | Approve | "This agent requires access to [production system]. Confirm scope and permissions." |
| Agent can send external communications (email, Slack) | Approve | "This agent can send [emails/messages]. All sends must require approval until validated." |
| Multi-agent design with agents delegating to agents | Consult | "This creates an agent chain. Confirm escalation and human oversight at each level." |

## Safety Constraints

- Never give an agent permissions it doesn't need for the current task
- Never design an agent that can modify its own system prompt or guardrails
- Never design an agent that bypasses human approval for irreversible actions
- Never store sensitive user data in agent memory without explicit consent and retention policy
- Never assume an agent will "just work" — define failure modes for every tool

## Expected Output

- Agent boundary document
- Tool inventory with permissions and failure behaviors
- Memory architecture design
- Planning approach
- Guardrails specification
- Observability plan
- Evaluation criteria
- Architecture diagram or component list for implementation

## Validation

- [ ] Agent boundary is explicit (in-scope and out-of-scope both defined)
- [ ] Every tool has a defined failure behavior
- [ ] Guardrails cover input, output, and action dimensions
- [ ] Observability plan covers all tool calls and reasoning steps
- [ ] Evaluation criteria are measurable (not "works well")
- [ ] Human approval gates are defined for all irreversible actions

## Failure Handling

| Failure | What to do |
|---------|------------|
| Agent goal is too vague to bound | Return to `requirements-analysis` |
| Tools have excessive permissions | Apply least-privilege; redesign tool interface |
| No clear human escalation path | Define escalation conditions before proceeding |

## Examples

### Example 1: Code review agent

**Goal:** Automatically review PRs for style violations and security issues.

**Boundary:** In scope: read files, run linters, check for known patterns. Out of scope: modify code, approve PRs, send external communications.

**Tools:** `read_file`, `run_linter`, `post_review_comment`. No write-file or approve-PR tools.

**Memory:** Short-term only (within a single PR review session).

**Guardrails:** Never post a comment labeling code as "vulnerable" without citing a specific pattern. Never auto-approve. Never self-modify review criteria.

## Related Skills

- `rag-architecture` — if the agent uses RAG for knowledge retrieval
- `context-engineering` — for managing agent context window budget
- `ai-security-review` — security audit of the designed agent
- `production-readiness` — before deploying to production
