# Example: Building a RAG Pipeline with AISkills

This example demonstrates how an AI coding agent works through the **RAG Development Workflow** in AISkills.

---

## Scenario

**User Request:**  
> "We want to build a documentation search tool for our internal engineering docs (Markdown & PDF) using Python and FastAPI."

---

## Execution Walkthrough

### 1. Discovery (`skills/discovery/repository-discovery`)
The agent starts by reading [CONTEXT.md](../../CONTEXT.md) and discovering the repository:
- Identifies Python 3.11 + FastAPI + `pgvector` environment.
- Verifies that no `.env` or credentials are read.
- Maps existing endpoints in `src/api/`.

### 2. Requirements & Clarification (`skills/requirements/requirements-analysis`)
The agent produces a structured specification following [templates/SPEC.md](../../templates/SPEC.md):
- **FR-001**: Ingest Markdown and PDF technical documentation.
- **FR-002**: Hybrid search (dense embeddings + BM25 keyword matching).
- **FR-003**: Return answers with source citations and section links.
- **NFR-001**: P95 retrieval latency < 500ms; total response < 3.0s.

### 3. Architecture Design (`skills/ai/rag/rag-architecture`)
The agent drafts [templates/DESIGN.md](../../templates/DESIGN.md) and [templates/ADR.md](../../templates/ADR.md):
- **Chunking**: Semantic section-aware chunking (512 tokens max, 50-token overlap).
- **Embeddings**: `text-embedding-3-small` with batching.
- **Vector DB**: `pgvector` in existing PostgreSQL database.
- **Indirect Prompt Injection Defense**: Delimiting context with XML tags `<retrieved_context>` and strict instruction boundary.

### 4. Implementation & TDD (`skills/testing/tdd`)
The agent writes tests first:
- Unit tests for chunking boundary logic.
- Integration tests with mock embedding client.
- Passes all unit tests before connecting the FastAPI endpoint.

### 5. Evaluation (`skills/ai/evaluation/rag-evaluation`)
Using a golden dataset of 50 internal queries, the agent measures:
- **Faithfulness**: 0.92
- **Context Precision**: 0.85
- **Answer Relevancy**: 0.88
- **Hallucination Rate**: 0.08
- Produces report using [templates/EVALUATION.md](../../templates/EVALUATION.md).

### 6. Security Audit (`skills/ai/ai-security/ai-security-review`)
- Audited against OWASP GenAI LLM Top 10 (2026).
- Validated prompt injection mitigations and least-privilege database roles.
- Produces report using [templates/SECURITY.md](../../templates/SECURITY.md).

### 7. Production Gate (`skills/ai/production-ai/production-readiness`)
- Completed 11-step production checklist.
- Human signs off on deployment.
