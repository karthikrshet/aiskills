# Agent Development Workflow

This workflow guides an AI coding agent through designing, implementing, evaluating, and deploying a production AI agent.

---

## Workflow Stages

```
Stage 1: Goal Definition
    ↓
Stage 2: Agent Boundary
    ↓
Stage 3: Tool Design
    ↓
Stage 4: Memory Design
    ↓
Stage 5: Planning Approach
    ↓
Stage 6: Guardrails
    ↓
[Design Gate] ← Human review required
    ↓
Stage 7: Implementation (per implementation-planning + tdd)
    ↓
Stage 8: Evaluation
    ↓
[Evaluation Gate]
    ↓
Stage 9: Security Review
    ↓
[Security Gate]
    ↓
Stage 10: Observability
    ↓
Stage 11: Production Readiness
    ↓
[Production Gate] ← Human approval required
```

---

## Stage Details

### Stage 1: Goal Definition (`requirements-analysis`)

**Define:**
- What task(s) does the agent accomplish?
- Who triggers the agent and when?
- What does success look like?
- What is the acceptable failure mode?

---

### Stage 2–6: Agent Design (`agent-design`)

Run the `agent-design` skill. Produce:

- **Agent boundary:** in-scope, out-of-scope, escalation conditions
- **Tool inventory:** permissions, side effects, failure behavior
- **Memory design:** short-term and long-term; retention policy
- **Planning approach:** reactive / plan-first / hierarchical
- **Guardrails:** input, output, action, escalation

---

### Design Gate ✅ — Human Review Required

> ⚠️ **STOP. Present agent design to human before implementation.**

| Check | Required |
|-------|---------|
| Agent boundary is explicit | ✅ |
| All tools have defined permissions and failure behavior | ✅ |
| Guardrails cover input, output, and actions | ✅ |
| Human approval gates defined for all irreversible actions | ✅ |
| Human has approved design | ✅ |

---

### Stage 7: Implementation + TDD

Implement using `implementation-planning` + `tdd`.

Test:
- Unit tests for each tool's behavior
- Integration tests for tool + agent interaction
- Agent simulation: does the agent complete tasks correctly?
- Failure tests: how does the agent behave when tools fail?
- Guardrail tests: does the guardrail block what it should?

---

### Stage 8: Evaluation

Measure:
- Task completion rate
- Tool-call accuracy (correct tool, correct arguments)
- Unnecessary tool calls (inefficiency)
- Human escalation rate
- Latency per task
- Cost per task

Use `templates/EVALUATION.md` to report.

---

### Evaluation Gate ✅

| Metric | Target | Result |
|--------|--------|--------|
| Task completion rate | ≥ [X]% | |
| Tool-call accuracy | ≥ [X]% | |
| Human escalation rate | Within expected range | |

---

### Stage 9: Security Review (`ai-security-review`)

**Focus areas for agents:**
- LLM01: Prompt injection via user input or tool outputs
- LLM06: Excessive agency — over-permissioned tools
- LLM05: Unsafe output handling — agent output used in downstream systems

---

### Stage 10: Observability

Ensure every agent execution logs:
- Task and goal
- Each reasoning step
- Each tool call (name, args, result, duration)
- Total token usage and cost
- Errors and escalations

---

### Production Gate ✅ — Human Approval Required

> ⚠️ **Run `production-readiness` skill. Obtain human approval. Do not deploy without sign-off.**

---

*Part of AISkills v0.1.0 — see [skills/ai/agent-design/](../../skills/ai/agent-design/) for skill details.*
