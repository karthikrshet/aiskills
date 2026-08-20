# AI Engineering with AISkills

AISkills provides first-class skills for AI and ML engineering — the primary differentiator from generic coding-agent skill collections.

---

## Why AI Engineering Needs Its Own Skills

Software engineering skills (requirements, architecture, testing) apply to all software. But AI/ML systems have unique failure modes:

| AI-Specific Failure | Generic skill misses it | AISkills skill covers it |
|--------------------|------------------------|--------------------------|
| RAG retrieves irrelevant chunks | Code review doesn't catch this | `rag-evaluation` |
| Agent calls wrong tool | Testing doesn't catch planning failures | `agent-design` |
| Context window overflow | Implementation planning ignores token budgets | `context-engineering` |
| Prompt injection via retrieved docs | Security review focuses on code, not content | `ai-security-review` |
| LLM hallucination in production | Code review can't catch fabrication | `rag-evaluation` |
| Model costs exceed budget | No budget model in standard implementation | `production-readiness` |
| No observability on LLM calls | Logging checks miss LLM-specific traces | `production-readiness` |

---

## AI Engineering Skill Map

```
AI Engineering Skills
│
├── System Design
│   ├── agent-design          Design single/multi-agent systems
│   └── rag-architecture      End-to-end RAG system design
│
├── Context & Prompts
│   └── context-engineering   Context selection, compression, budgeting
│
├── Evaluation
│   └── rag-evaluation        RAG quality evaluation
│
├── Security
│   └── ai-security-review    OWASP GenAI LLM Top 10 security audit
│
└── Production
    └── production-readiness  Pre-production AI system checklist
```

---

## Agent Engineering

### What is an AI agent?

An AI agent is a system that uses an LLM to reason about a goal, select and call tools, manage state, and take multi-step actions to accomplish the goal.

### Key design questions the `agent-design` skill addresses:

**Agent boundary:**
- What is the agent responsible for? What is outside its scope?
- Where does human control end and agent autonomy begin?

**Tool design:**
- What tools does the agent need?
- What are the permissions and side effects of each tool?
- How does the agent recover from tool failures?

**Memory:**
- What does the agent need to remember within a session? (short-term)
- What does the agent need to remember across sessions? (long-term)
- How is memory retrieved? How is memory updated?

**Planning:**
- Does the agent plan explicitly (write a plan, then execute)?
- Or act reactively (observe → think → act)?

**Guardrails:**
- What actions must be blocked regardless of agent reasoning?
- What triggers a human escalation?

**Evaluation:**
- How do we know the agent completed the task correctly?
- How do we measure tool-use accuracy?
- How do we detect when the agent is stuck in a loop?

---

## RAG Engineering

### What is RAG?

Retrieval-Augmented Generation (RAG) connects an LLM to a knowledge base. Instead of relying on training data, the LLM retrieves relevant documents at query time and uses them as context for generation.

### Key design questions the `rag-architecture` skill addresses:

**Document ingestion:**
- What formats? (PDF, HTML, Markdown, structured data)
- How often does data change?
- What preprocessing is needed?

**Chunking:**
- Fixed-size or semantic chunks?
- What chunk size? (trade-off: too large = irrelevant context, too small = incomplete information)
- Overlap strategy?

**Embedding:**
- Which embedding model? (trade-offs in quality, cost, latency, dimensionality)
- How often do embeddings need to be refreshed?

**Retrieval:**
- Dense retrieval (semantic similarity)?
- Sparse retrieval (keyword matching, BM25)?
- Hybrid retrieval?
- What k (number of chunks to retrieve)?

**Reranking:**
- Should retrieved chunks be reranked before passing to LLM?
- Which reranking model?

**Context construction:**
- How are retrieved chunks assembled into the LLM context?
- What is the token budget?
- How are citations handled?

### RAG Evaluation Dimensions

The `rag-evaluation` skill measures:

| Dimension | Question |
|-----------|---------|
| **Faithfulness** | Does the answer contain only information from the retrieved context? |
| **Answer Relevancy** | Does the answer directly address the question? |
| **Context Precision** | Are the retrieved chunks relevant to the question? |
| **Context Recall** | Does the retrieved context contain the information needed to answer? |
| **Hallucination rate** | How often does the LLM generate information not in the context? |

Inspired by RAGAS methodology. Tools like RAGAS, DeepEval, and Promptfoo can be used to run these evaluations.

**Evaluation honesty rule:** If a metric has not been measured, report `NOT MEASURED`. Never estimate or fabricate evaluation numbers.

---

## Context Engineering

Context engineering is the discipline of selecting, compressing, and prioritizing information for the LLM context window.

### Why it matters:

- Context windows are finite (and expensive)
- Irrelevant context degrades response quality
- Ordering and formatting of context affects LLM performance
- Context contamination (injected malicious instructions) is a security risk

### What the `context-engineering` skill addresses:

- **Discovery:** What information exists in the repository/knowledge base?
- **Selection:** Which information is relevant to *this specific task*?
- **Compression:** How can selected content be summarized without losing key information?
- **Prioritization:** What goes in the context first? (recency bias, relevance ranking)
- **Budgeting:** How many tokens are available? What fits? What must be excluded?
- **Contamination analysis:** Does any retrieved content contain prompt injection?

---

## AI Security

AI systems face security threats that don't apply to traditional software:

| Threat | Description |
|--------|-------------|
| **Prompt injection** | Malicious instructions in user input hijack agent behavior |
| **Indirect prompt injection** | Malicious instructions embedded in retrieved documents |
| **System prompt leakage** | Attacker extracts the system prompt |
| **Excessive agency** | Over-permissioned agent takes unintended destructive actions |
| **Data poisoning** | Training or retrieval data is corrupted |
| **Insecure output handling** | LLM output used unsanitized in downstream systems |

The `ai-security-review` skill provides a structured audit covering OWASP GenAI LLM Top 10 (2026).

**Key principle:** Treat all externally retrieved content as untrusted. RAG retrieval is a significant indirect prompt injection vector.

---

## Production AI Engineering

Moving an AI system to production requires more than passing unit tests:

| Concern | Coverage in `production-readiness` skill |
|---------|----------------------------------------|
| Model abstraction | Can the model be swapped without rewriting application code? |
| Cost | What is the cost per query? Is it within budget? |
| Latency | What is P50/P95/P99 latency? Is it acceptable? |
| Retries and fallbacks | What happens when the LLM API is unavailable? |
| Rate limiting | How does the system behave at rate limit? |
| Structured logging | Are all LLM calls logged with inputs, outputs, latency, cost? |
| Tracing | Are multi-step agent workflows traceable end-to-end? |
| Evaluation in CI/CD | Are quality regressions caught before deployment? |
| Rollback | Can the system be rolled back to a previous model/prompt version? |

---

## Evaluation Framework

AISkills defines a general evaluation model for AI systems:

| Dimension | How to measure |
|-----------|---------------|
| Correctness | Does the output solve the problem? |
| Relevance | Is the output on-topic? |
| Groundedness | Is the output supported by retrieved context? |
| Faithfulness | Does the output contradict the source? |
| Retrieval quality | Context precision + recall |
| Hallucination rate | Frequency of fabricated information |
| Tool-call accuracy | Correct tool selected with correct arguments |
| Latency | P50/P95/P99 response time |
| Cost | Token usage and API cost per query |
| Robustness | Performance on edge cases and adversarial inputs |
| Security | Resistance to prompt injection and other attacks |
| Consistency | Determinism across repeated identical queries |

See `templates/EVALUATION.md` for the evaluation report template.

---

*AISkills v0.1.0 — see [skills/ai/](../skills/ai/) for the AI engineering skill library.*
