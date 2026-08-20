---
name: rag-evaluation
description: |
  Use this skill to evaluate the quality of a RAG pipeline on faithfulness,
  answer relevancy, context precision, context recall, and hallucination rate.
  Activates after a RAG system is implemented or when retrieval quality is
  in question. Produces a structured evaluation report with measurable results.
version: "0.1.0"
category: ai/evaluation
tags: [rag, evaluation, faithfulness, retrieval, hallucination, ragas, metrics, quality]
risk: low
status: alpha
related-skills:
  - rag-architecture
  - context-engineering
  - production-readiness
  - ai-security-review
---

# RAG Evaluation

## Purpose

A RAG system that "seems to work" during manual testing may still have high hallucination rates, poor retrieval precision, or low faithfulness — problems that only become visible at scale or on adversarial queries. Without structured evaluation, teams declare systems "good enough" without evidence.

This skill provides a methodology for rigorously evaluating RAG pipeline quality before calling it production-ready. It defines evaluation dimensions, how to build or select an evaluation dataset, how to run and interpret results, and what to do with the findings. It references RAGAS-style evaluation methodology without requiring any specific tool.

**Evaluation honesty rule:** If a metric has not been measured, it must be reported as `NOT MEASURED`. Do not estimate, round up, or invent evaluation results.

## When to Use

- After implementing a RAG system or making significant changes to it
- When retrieval quality is suspected to be poor (users reporting wrong answers)
- Before declaring a RAG system production-ready
- As part of a CI/CD evaluation gate
- When benchmarking changes to chunking, embedding, retrieval, or reranking

## When Not to Use

- The RAG system has not yet been implemented (use `rag-architecture`)
- The system is not a RAG system (use general LLM evaluation)

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Running RAG system or pipeline endpoint | ✅ | The system to evaluate |
| Evaluation dataset | ✅ or build in this skill | Questions + expected answers or relevant documents |
| RAG architecture documentation | optional | Helps interpret evaluation results |

## Preconditions

- [ ] RAG system is implemented and running
- [ ] Agent can make queries to the system
- [ ] Evaluation dataset exists or will be created in this skill

## Workflow

### Step 1: Build or Validate the Evaluation Dataset

A good evaluation dataset is the foundation of meaningful evaluation.

**Minimum viable evaluation dataset:**
- 50+ question-answer pairs (200+ for production gating)
- Questions span the realistic distribution of real user queries
- Ground truth answers are correct and complete
- Ground truth context documents are identified where possible

**Three ways to build an evaluation dataset:**

1. **Synthetic (fastest):** Use an LLM to generate questions from the actual documents. Seed with real queries if available.

2. **Human-annotated (highest quality):** Domain experts write questions and answers. Time-consuming but most reliable.

3. **Production logs (most realistic):** Real queries with human-judged answers. Requires production traffic.

**Format for each evaluation example:**
```json
{
  "question": "What is the maximum chunk size supported by the ingestion pipeline?",
  "ground_truth": "The ingestion pipeline supports chunks up to 1024 tokens.",
  "ground_truth_context": ["The pipeline supports chunks up to 1024 tokens..."]
}
```

**Warning:** A tiny dataset (< 10 examples) produces meaningless metrics. Report sample size in every evaluation.

### Step 2: Define Evaluation Dimensions

Evaluate the pipeline on these dimensions:

#### Faithfulness
**Question:** Does the answer contain only information present in the retrieved context?

A faithful answer makes no claims not supported by the context. Unfaithful answers hallucinate facts.

**Score:** 0.0 (completely unfaithful) to 1.0 (fully grounded)

**How to measure:**
- For each statement in the answer, check if it can be attributed to a retrieved chunk
- LLM-as-judge: "Given these context documents and this answer, does the answer contain any claims not supported by the context? Rate from 0 to 1."

#### Answer Relevancy
**Question:** Does the answer directly address the user's question?

A relevant answer is on-topic. An irrelevant answer may be factually correct but doesn't answer the question asked.

**Score:** 0.0 to 1.0

**How to measure:**
- Generate synthetic questions from the answer; measure cosine similarity between generated questions and the original question
- High similarity = high relevancy

#### Context Precision
**Question:** Of the retrieved chunks, what fraction are actually relevant to the question?

Low context precision means the retriever is returning irrelevant chunks alongside relevant ones. This wastes context window tokens and may confuse the LLM.

**Score:** 0.0 to 1.0

**How to measure:**
- For each retrieved chunk, classify: relevant (1) or not relevant (0) to the question
- Score = number of relevant chunks / total chunks retrieved
- Use LLM-as-judge or ground truth context for classification

#### Context Recall
**Question:** Of the information needed to answer the question, what fraction was retrieved?

Low context recall means the retriever is missing relevant chunks. The LLM cannot answer correctly if the relevant context was never retrieved.

**Score:** 0.0 to 1.0

**How to measure:**
- Break ground truth answer into statements
- For each statement, check if it can be attributed to a retrieved chunk
- Score = number of statements attributable to retrieved chunks / total statements

#### Hallucination Rate
**Question:** What fraction of answers contain at least one hallucinated claim?

Hallucination rate = 1 - Faithfulness at the answer level.

**Score:** 0.0 (no hallucination) to 1.0 (all answers hallucinate)

### Step 3: Run the Evaluation

For each question in the evaluation dataset:

1. Submit the question to the RAG pipeline
2. Collect: the answer, the retrieved chunks, and any metadata
3. Score each dimension using the method defined in Step 2

**Tool options (use any that fit the infrastructure):**
- RAGAS Python library — implements faithfulness, answer relevancy, context precision, context recall
- DeepEval — broader metric library including RAG metrics
- Manual review — for small datasets; uses LLM-as-judge or human scoring
- Custom scoring scripts — if specific domain requirements exist

**Do not use a tool you haven't verified returns correct scores.** Spot-check 5 examples manually.

### Step 4: Analyze Results

**Interpret scores:**

| Score Range | Interpretation |
|------------|----------------|
| > 0.85 | Excellent — production-ready for this dimension |
| 0.70–0.85 | Good — acceptable with monitoring |
| 0.50–0.70 | Needs improvement — investigate root cause |
| < 0.50 | Poor — significant architectural issue |

**Identify failure patterns:**
- Low faithfulness → LLM is hallucinating; try stricter system prompt or smaller temperature
- Low answer relevancy → query is being answered with tangential information; improve retrieval
- Low context precision → retriever returning irrelevant chunks; improve embedding or add reranking
- Low context recall → relevant chunks not being retrieved; adjust k, improve chunking, or use hybrid retrieval

### Step 5: Root Cause Failed Evaluations

For 5–10 failed examples (randomly sampled):

1. Inspect the question
2. Inspect the retrieved chunks
3. Inspect the answer
4. Identify which stage of the pipeline failed: ingestion, chunking, embedding, retrieval, or generation

**Common root causes:**
- Relevant information is in a PDF section that wasn't parsed correctly
- Chunk boundary split a key fact across two chunks (neither chunk contains the full answer)
- Embedding model doesn't handle the query domain well
- k is too small to retrieve all relevant context
- System prompt allowed hallucination when context was insufficient

### Step 6: Produce Evaluation Report

Use `templates/EVALUATION.md` to produce a structured report:

- Dataset size and source
- Score for each dimension (with confidence interval if large enough dataset)
- Identified failure patterns
- Root cause analysis for samples
- Recommendations for improvement
- Production readiness gate decision

## Decision Points

| Condition | Tier | Action |
|-----------|------|--------|
| Evaluation dataset is < 20 examples | Inform | Note that results are unreliable; recommend building a larger dataset |
| Faithfulness < 0.60 | Consult | "Hallucination rate is high. Recommend improving before production. Can we delay launch?" |
| Results contradict business expectations | Consult | Present findings to human; do not suppress or adjust results |

## Safety Constraints

- Never report `NOT MEASURED` dimensions as passing the production gate
- Never use production user data in the evaluation dataset without privacy review
- Never invent, estimate, or extrapolate evaluation scores
- Never declare production-ready based on < 50 evaluation examples
- Always report sample size alongside every metric

## Expected Output

- Evaluation report (`templates/EVALUATION.md`) with:
  - Dataset description and size
  - Scores for all measured dimensions
  - `NOT MEASURED` for any dimension not evaluated
  - Root cause analysis
  - Recommendations
  - Production gate decision

## Validation

- [ ] Evaluation dataset size ≥ 50 (or explicitly noted as insufficient)
- [ ] All five core dimensions evaluated (or marked NOT MEASURED with reason)
- [ ] At least 5 failed examples were analyzed for root cause
- [ ] Recommendations are specific and actionable
- [ ] Production gate decision is explicit

## Failure Handling

| Failure | What to do |
|---------|------------|
| No evaluation dataset exists | Build synthetic dataset from documents (Step 1); note it is synthetic |
| LLM-as-judge is unavailable | Use manual review for a sample of 20 examples |
| Scores are suspiciously high (> 0.95 across all dimensions) | Suspect the evaluation dataset is too easy; inspect for data leakage |
| Pipeline errors during evaluation | Log errors separately; calculate scores only on successful runs; report error rate |

## Examples

### Example 1: Evaluating a documentation Q&A system

**Dataset:** 100 questions from engineering team (real queries), ground truth from documentation authors.

**Results:**
| Dimension | Score | Notes |
|-----------|-------|-------|
| Faithfulness | 0.82 | Acceptable; 18% of answers contain one unsupported claim |
| Answer Relevancy | 0.91 | High — answers are on-topic |
| Context Precision | 0.64 | Low — retriever returning irrelevant chunks |
| Context Recall | 0.73 | Acceptable |
| Hallucination Rate | 0.18 | 18% of answers hallucinate at least one claim |

**Root cause of low Context Precision:** Fixed-size chunking splits API documentation into fragments. Switching to section-aware chunking is recommended.

**Gate decision:** NOT READY — Context Precision requires improvement before production.

## Related Skills

- `rag-architecture` — design the system before evaluating it
- `context-engineering` — improve context quality based on evaluation findings
- `production-readiness` — gates that include evaluation results
