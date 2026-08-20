---
name: production-readiness
description: |
  Use this skill to verify that an AI system is ready for production before
  deployment. Covers model abstraction, cost/latency, retries, fallbacks,
  structured logging, tracing, observability, evaluation in CI/CD, monitoring,
  and rollback planning. Activates as a mandatory gate before production
  deployment of any AI/LLM application or agent.
version: "0.1.0"
category: ai/production-ai
tags: [production, readiness, observability, cost, latency, fallback, monitoring, deployment]
risk: high
status: alpha
related-skills:
  - ai-security-review
  - rag-evaluation
  - agent-design
  - rag-architecture
---

# Production Readiness

## Purpose

An AI system that passes tests in development frequently has unresolved production concerns: no latency budget, no fallback when the LLM API is unavailable, no cost monitoring, no observability into what the model is actually doing, and no rollback plan when a new model version produces worse results.

Declaring a system "production ready" because "it works on my machine" is a fast path to an incident. This skill provides a structured checklist of production readiness requirements specific to AI/LLM systems, covering operational concerns that are often absent from standard software deployment checklists.

**Risk level: High.** This skill gates production deployment. Human approval is required before any production deployment.

## When to Use

- Before deploying any AI/LLM system, agent, or RAG pipeline to production
- When "it works in staging" and production deployment is being discussed
- When an AI system is scaling from prototype to production
- When assessing the operational maturity of an existing AI system

## When Not to Use

- The system is a prototype or development environment
- The system is a local tool with no production deployment

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| System architecture / design | ✅ | What has been built |
| Evaluation results | ✅ | Output of `rag-evaluation` or equivalent |
| Security review results | ✅ | Output of `ai-security-review` |
| Deployment plan | optional | How the system will be deployed |

## Preconditions

- [ ] Security review is complete (no unresolved critical/high findings)
- [ ] Evaluation results are available (metrics are measured, not estimated)
- [ ] Code review is complete

## Workflow

Work through each checklist section. Every ❌ is a blocker. Every ⚠️ requires a documented acceptance of risk before deployment.

### Section 1: Model and Provider Abstraction

- [ ] **Model abstraction layer exists:** The application does not hardcode `openai.ChatCompletion.create(model="gpt-4o")` in 50 places. Model is referenced via a configuration value or abstraction layer.
- [ ] **Provider can be swapped:** If the primary LLM provider becomes unavailable, can a fallback provider be configured without code changes?
- [ ] **Model version is pinned:** A specific model version is specified, not just `gpt-4-latest` or equivalent. Unpinned models can change behavior without warning.
- [ ] **Deprecation timeline known:** The selected model version's end-of-life date is known and planned for.

### Section 2: Cost Management

- [ ] **Cost per query estimated:** An estimate of cost per query (input tokens + output tokens × price per token) is documented.
- [ ] **Monthly cost projection:** At expected query volume, what is the estimated monthly cost? Is this within budget?
- [ ] **Cost alert configured:** An alert fires when daily/monthly spend exceeds a defined threshold.
- [ ] **Cost anomaly detection:** If cost doubles overnight, will someone know?
- [ ] **Caching implemented (if appropriate):** Are identical or semantically equivalent queries cached to reduce redundant LLM calls?

### Section 3: Latency

- [ ] **P50/P95/P99 latency measured:** Latency is measured and documented (not estimated).
- [ ] **Latency within requirement:** P95 latency is within the requirement from `SPEC.md` (or requirement is explicitly documented here).
- [ ] **Latency attribution:** Latency breakdown is known — how much is retrieval? How much is LLM generation? How much is post-processing?
- [ ] **Streaming implemented (if needed):** For user-facing responses with generation > 1s, streaming is implemented to avoid perceived latency.
- [ ] **Timeout configured:** All LLM API calls have a timeout. No request can hang indefinitely.

### Section 4: Reliability and Error Handling

- [ ] **Retry with exponential backoff:** Transient failures (rate limit, 429, 503) are retried with exponential backoff and jitter.
- [ ] **Max retries defined:** Retry loop has a maximum count. Infinite retries are a bug.
- [ ] **Fallback model configured:** If the primary model is unavailable, a fallback model or degraded response is triggered.
- [ ] **Circuit breaker implemented (or planned):** Repeated failures do not cascade; circuit breaker stops requests to a failing upstream.
- [ ] **Error messages don't expose internals:** LLM API errors return user-friendly messages, not raw API error objects.
- [ ] **Graceful degradation defined:** If the AI component fails entirely, what does the system do? (return cached result, use fallback, show maintenance message)

### Section 5: Rate Limits

- [ ] **Provider rate limits known:** The token-per-minute and requests-per-minute limits for the model tier in use are documented.
- [ ] **Rate limit handling implemented:** 429 responses are handled gracefully with retry.
- [ ] **User-level rate limiting implemented:** Individual users cannot exhaust the system's rate limit for all users.

### Section 6: Structured Logging

All LLM interactions must be logged. Each log entry should include:

- [ ] Request ID (correlatable across services)
- [ ] Model name and version
- [ ] Input token count
- [ ] Output token count
- [ ] Latency (milliseconds)
- [ ] Cost (computed)
- [ ] Status (success / error / timeout)
- [ ] Error type if applicable
- [ ] Agent task ID (for agent workflows)

**Must NOT log by default:**
- Full prompt content (may contain PII)
- Full completion content (may contain PII)
- User credentials
- API keys

If prompt/completion logging is needed for debugging: implement with explicit consent, access controls, and retention limits.

### Section 7: Tracing and Observability

- [ ] **Distributed tracing implemented:** Each request through the system is traceable end-to-end with a trace ID.
- [ ] **LLM calls appear in traces:** LLM API calls are instrumented as spans in the trace.
- [ ] **Tool calls traced (agents):** Each tool call by an agent is a traced span with arguments and result.
- [ ] **Retrieval traced (RAG):** Each retrieval query, its results, and relevance scores are traceable.
- [ ] **Observability tool selected:** Langfuse, Arize Phoenix, OpenTelemetry, or equivalent is configured.

### Section 8: Monitoring and Alerts

- [ ] **Error rate alert:** Alert if error rate exceeds [X]% over [Y] minutes.
- [ ] **Latency alert:** Alert if P95 latency exceeds [target]ms.
- [ ] **Cost alert:** Alert if daily cost exceeds [threshold].
- [ ] **Evaluation regression alert:** Alert if key quality metrics (faithfulness, relevancy) drop below threshold.
- [ ] **Dashboard exists:** Key metrics (error rate, latency, cost, quality) are visible on a dashboard.

### Section 9: Evaluation in CI/CD

- [ ] **Evaluation dataset exists:** A test set of queries is committed to the repository.
- [ ] **Evaluation runs on PRs:** Quality metrics are computed on every PR affecting prompts, retrieval, or generation logic.
- [ ] **Evaluation gate defined:** PRs are blocked if metrics fall below defined thresholds.
- [ ] **Prompt regression testing:** Changes to system prompts are tested for quality regression before merge.

### Section 10: Security Clearance

- [ ] **AI security review complete:** `ai-security-review` skill has been run; no unresolved critical/high findings.
- [ ] **Prompt injection defense implemented:** At least one mitigation for direct and indirect prompt injection is in place.
- [ ] **Output sanitization implemented:** LLM output is sanitized before use in downstream systems.

### Section 11: Rollback Plan

- [ ] **Model version rollback plan:** If a new model version produces worse quality, how do we rollback to the previous version? (config change? code change? data change?)
- [ ] **Prompt rollback plan:** If a prompt change degrades quality, can we revert? Are prompts version-controlled?
- [ ] **Feature flag or canary deployment:** New model versions or significant prompt changes are tested on a subset of traffic before full rollout.

---

### Final Step: Human Approval Required

Present the completed checklist to the human. Obtain explicit written approval before proceeding to production deployment.

**Every ❌ (unchecked required item) must be resolved or explicitly accepted with documented reasoning before approval.**

## Decision Points

| Condition | Tier | Action |
|-----------|------|--------|
| Any security review finding is unresolved | Approve | Full stop — no production deployment |
| Evaluation results show NOT MEASURED | Approve | "Key quality metrics are not measured. Deploying uninformed. Confirm you accept this risk." |
| Fallback is not implemented | Approve | "No fallback model or degraded mode exists. LLM outage = full outage. Confirm?" |
| Cost projection exceeds budget | Approve | "Estimated monthly cost is $[X]. This exceeds the $[budget]. Confirm?" |

## Safety Constraints

- **Never deploy to production without this checklist being reviewed**
- **Never deploy without human explicit approval**
- **Never deploy with unresolved critical/high security findings**
- **Never deploy without at least a cost estimate**
- Never log full prompts containing PII without user consent and access controls

## Expected Output

- Completed production readiness checklist with pass/fail/not applicable for each item
- List of blockers to resolve before deployment
- Documented risk acceptances (for items accepted as-is)
- Written request for human approval
- Production deployment sign-off (from human)

## Validation

- [ ] All 11 checklist sections reviewed
- [ ] Every ❌ has a remediation plan or risk acceptance
- [ ] Human has given explicit written approval
- [ ] Approval is recorded with date and name

## Failure Handling

| Failure | What to do |
|---------|------------|
| System fails multiple checklist items | Prioritize: security and reliability first; cost/observability second |
| Human wants to deploy despite blockers | Document each blocker and the accepted risk; add monitoring to detect issues immediately |
| Evaluation is incomplete | Document which metrics are NOT MEASURED; add monitoring to measure them in production |

## Examples

### Example 1: First production deployment of a RAG system

**Checklist summary:**
- ✅ Model abstraction: yes, model is in config
- ✅ Cost estimate: $0.002/query × 5,000 queries/day = ~$300/month within budget
- ✅ P95 latency: 1.8s measured in load test (requirement: < 3s)
- ❌ Fallback model: not implemented — BLOCKER
- ✅ Retry with backoff: implemented
- ⚠️ Evaluation in CI: partially implemented — faithfulness measured, recall not measured
- ✅ Security review: complete, no critical/high findings
- ❌ Rollback plan: not documented — BLOCKER

**Action before deployment:** Implement fallback model (degraded mode: return cached results); document rollback procedure.

## Related Skills

- `ai-security-review` — required before this skill
- `rag-evaluation` — evaluation results required as input
- `agent-design` — agent-specific readiness considerations
