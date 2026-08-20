# RAG Development Workflow

This workflow guides an AI coding agent through designing, implementing, evaluating, and deploying a production RAG system.

---

## When to Use

Use this workflow when building a new RAG system or significantly redesigning an existing one.

---

## Workflow Stages

```
Stage 1: Use Case Analysis
    ↓
Stage 2: Data Analysis
    ↓
Stage 3: RAG Architecture Design
    ↓
[Architecture Gate] ← Human review required
    ↓
Stage 4: Ingestion Pipeline
    ↓
Stage 5: Chunking + Embedding
    ↓
Stage 6: Retrieval Design
    ↓
Stage 7: Reranking (optional)
    ↓
Stage 8: Context Construction
    ↓
Stage 9: Generation + System Prompt
    ↓
Stage 10: Evaluation Planning + Dataset
    ↓
Stage 11: Implementation (per implementation-planning)
    ↓
Stage 12: RAG Evaluation
    ↓
[Evaluation Gate]
    ↓
Stage 13: AI Security Review
    ↓
[Security Gate]
    ↓
Stage 14: Production Readiness
    ↓
[Production Gate] ← Human approval required
    ↓
Stage 15: Production Monitoring
```

---

## Stage Details

### Stage 1: Use Case Analysis (`requirements-analysis`)

**Define:**
- What questions must the system answer?
- Who are the users?
- What quality is required? (accuracy, citation, latency)
- What is the cost budget?

**Exit criterion:** Requirements documented in `templates/SPEC.md`.

---

### Stage 2: Data Analysis

**Analyze:**
- Data sources: types, formats, volumes
- Update frequency
- Language and domain characteristics
- Access control requirements
- PII/sensitive content presence

**Exit criterion:** Data profile documented.

---

### Stage 3: RAG Architecture Design (`rag-architecture`)

**Design all pipeline stages:**
- Ingestion and connectors
- Chunking strategy and parameters
- Embedding model selection
- Vector database selection
- Retrieval strategy (dense / sparse / hybrid)
- Reranking decision
- Context construction and token budget
- Generation and system prompt design
- Evaluation criteria (defined before implementation)

**Write ADRs for:** embedding model, vector database, retrieval strategy.

---

### Architecture Gate ✅ — Human Review Required

> ⚠️ **STOP. Present RAG architecture to human. Do not implement until approved.**

| Check | Required |
|-------|---------|
| All pipeline stages designed | ✅ |
| ADRs written for major decisions | ✅ |
| Evaluation criteria defined (before implementation) | ✅ |
| Security considerations documented | ✅ |
| Human has approved | ✅ |

---

### Stages 4–9: Implementation

Follow `implementation-planning` to order implementation:

1. **Ingestion pipeline** — connectors, parsers, metadata extraction
2. **Chunking** — chunk size, overlap, strategy
3. **Embedding** — batch embedding, storage
4. **Vector database** — schema, indexes
5. **Retrieval** — query embedding, search, filtering
6. **Reranking** — if selected
7. **Context construction** — assembly, token budget enforcement
8. **Generation** — system prompt, citation, unanswerable handling

Use `tdd` at each stage. Run tests before proceeding.

---

### Stage 10: Evaluation Dataset

**Build or validate:**
- Minimum 50 question-answer pairs (200+ for production)
- Covers realistic query distribution
- Includes edge cases and adversarial queries
- Ground truth is correct and complete

---

### Stage 12: RAG Evaluation (`rag-evaluation`)

**Measure:**
- Faithfulness
- Answer Relevancy
- Context Precision
- Context Recall
- Hallucination Rate
- Latency
- Cost per query

**Honesty rule:** Report `NOT MEASURED` for any unmeasured dimension.

---

### Evaluation Gate ✅

| Check | Status |
|-------|--------|
| Evaluation dataset ≥ 50 examples | ✅ / ❌ |
| Faithfulness meets target | ✅ / ❌ |
| Context Precision meets target | ✅ / ❌ |
| Hallucination rate within target | ✅ / ❌ |
| No metric is estimated (all measured) | ✅ / ❌ |

**Do not proceed to production if evaluation gate fails.**

---

### Stage 13: AI Security Review (`ai-security-review`)

**Focus areas for RAG systems:**
- Indirect prompt injection via retrieved documents (LLM01)
- Sensitive data in retrieved content (LLM02)
- Data poisoning in the knowledge base (LLM04)
- Embedding manipulation (LLM08)

---

### Security Gate ✅

No unresolved critical/high security findings.

---

### Stage 14: Production Readiness (`production-readiness`)

Full checklist including:
- Model abstraction
- Cost monitoring
- Latency SLOs
- Retry and fallback
- Structured logging of retrieval and generation
- Evaluation in CI/CD
- Rollback plan (for embedding model or retrieval config changes)

---

### Production Gate ✅ — Human Approval Required

> ⚠️ **STOP. Human approval required before production deployment.**

---

### Stage 15: Production Monitoring

**Monitor continuously:**
- Evaluation metrics on production sample (weekly)
- Cost per query
- Retrieval latency
- Error rate
- User feedback (thumbs up/down if applicable)

**Alert on:**
- Evaluation metric drop > 5% from baseline
- Cost spike > 2× baseline
- Error rate > [threshold]

---

*Part of AISkills v0.1.0 — see [skills/ai/rag/](../../skills/ai/rag/) for skill details.*
