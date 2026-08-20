# Production Readiness Workflow

This workflow provides a structured checklist for verifying an AI system is ready for production deployment.

---

## When to Use

Run this workflow before any production deployment of an AI/LLM application.

---

## Pre-requisites

Before running this workflow, the following must be complete:

| Pre-requisite | Skill |
|--------------|-------|
| Feature implementation complete | `implementation-planning` + `tdd` |
| Code review complete | `code-review` |
| Evaluation results available | `rag-evaluation` (for RAG systems) |
| Security review complete | `ai-security-review` |

---

## Workflow

Run the `production-readiness` skill and complete all 11 checklist sections:

1. **Model and Provider Abstraction** — model is configurable, not hardcoded
2. **Cost Management** — cost per query estimated; alerts configured
3. **Latency** — P50/P95/P99 measured; within requirements
4. **Reliability** — retry, fallback, circuit breaker, graceful degradation
5. **Rate Limits** — provider limits known; user-level rate limiting
6. **Structured Logging** — all LLM calls logged with token counts and latency
7. **Tracing** — distributed traces include LLM calls
8. **Monitoring and Alerts** — error rate, latency, cost, quality alerts
9. **Evaluation in CI/CD** — quality gated in CI; prompt regression tested
10. **Security Clearance** — no unresolved critical/high findings
11. **Rollback Plan** — model and prompt rollback documented; feature flag if possible

---

## Production Gate ✅ — Human Approval Required

> ⚠️ **STOP. Present the completed checklist to the human.**
> **Every ❌ item must be resolved or accepted with documented risk.**
> **Human must give explicit written approval.**

| Check | Result |
|-------|--------|
| All 11 sections reviewed | |
| No unresolved security findings | |
| Evaluation gate passed | |
| Human approval received | |

---

*Part of AISkills v0.1.0 — see [skills/ai/production-ai/](../../skills/ai/production-ai/) for skill details.*
