# Research Notes — AI Skill Systems and Agent Workflows

*Part of AISkills documentation. This document records research observations that informed the design of AISkills.*

---

## 1. Existing Agent Skill Systems

### 1.1 The SKILL.md Format (agentskills.io)

The open SKILL.md standard is the dominant format for agent skill definition. It consists of:

**YAML frontmatter** (machine-readable metadata for agent discovery):
- `name` — unique identifier (lowercase-hyphenated)
- `description` — activates the skill when an agent reads it
- `license`, `compatibility`, `metadata`, `allowed-tools` (optional)

**Markdown body** (human and agent-readable instructions)

Key insight: agents load `name` + `description` first to decide whether to activate a skill, then load the full body. This progressive disclosure pattern keeps token usage low.

**Adopted by AISkills:** Yes — with extended frontmatter fields for richer validation and discovery.

### 1.2 Community Collections (awesome-agent-skills)

Large community collections (VoltAgent/awesome-agent-skills, heilcheng/awesome-agent-skills) contain 1000+ skills contributed by engineers from Anthropic, Google, Vercel, and Stripe.

**Observations:**
- Most skills are framework-specific (e.g., "write Next.js components", "use Stripe API")
- Very few skills address *engineering process* (requirements, architecture, testing discipline)
- **AI engineering skills are almost entirely absent** — no skills for RAG evaluation, agent memory design, hallucination analysis, prompt injection detection, context engineering

**Opportunity identified:** AISkills can differentiate by focusing on *AI engineering workflows* rather than framework-specific coding patterns.

### 1.3 Agent Frameworks

Major open-source agent frameworks:
- **OpenHands (formerly OpenDevin)** — autonomous software engineer agent
- **LangGraph** — stateful multi-agent workflows
- **Cline** — IDE-integrated autonomous coding agent

These frameworks provide the *execution engine*. AISkills provides the *engineering methodology* — what the agent should do at each stage, regardless of which framework executes it.

---

## 2. Evaluation Ecosystem

### 2.1 RAG Evaluation

Key frameworks:
- **RAGAS** — reference-free RAG evaluation (faithfulness, answer relevancy, context precision, context recall). Most widely used for RAG-specific metrics.
- **DeepEval** — Pytest-style integration; 50+ metrics; excellent for CI/CD gating.
- **Promptfoo** — prompt testing, model comparison, regression suites.

**Observation:** These frameworks are mature but require technical setup. Many AI engineers evaluate RAG by testing end-to-end manually, missing retrieval-specific failures.

**AISkills contribution:** The `rag-evaluation` skill provides a structured methodology for evaluation — tool-agnostic, referencing RAGAS dimensions without hard-coding any specific tool.

### 2.2 Agent Evaluation

Emerging trend (2025–2026): evaluating agent *trajectories* (intermediate steps, tool calls, reasoning) rather than just final outputs.

LLM-as-a-judge is now standard for qualitative evaluation at scale.

**AISkills contribution:** The evaluation framework documented in `templates/EVALUATION.md` and referenced in skills provides a dimension-based model applicable to both RAG and agents.

### 2.3 Observability

Leading tools: **Arize Phoenix** (OpenTelemetry-native), **Langfuse** (tracing + evaluation).

**Design decision:** AISkills does not embed observability tooling. The `production-readiness` skill guides engineers to *integrate* appropriate observability — it does not prescribe a specific tool.

---

## 3. AI Security Landscape

### 3.1 OWASP GenAI LLM Top 10 (2026 edition)

Current authoritative standard for LLM application security. Key risks relevant to AISkills:

1. **Prompt Injection** (LLM01) — direct and indirect injection remain the top risk
2. **Sensitive Information Disclosure** (LLM02) — model memorization and context leakage
3. **Supply Chain** (LLM03) — model and plugin supply chain risks
4. **Data and Model Poisoning** (LLM04) — training and retrieval data attacks
5. **Improper Output Handling** (LLM05) — unsanitized LLM output fed to downstream systems
6. **Excessive Agency** (LLM06) — over-permissioned agents
7. **System Prompt Leakage** (LLM07) — extraction of system prompts
8. **Vector and Embedding Weaknesses** (LLM08) — retrieval-specific attacks
9. **Misinformation** (LLM09) — hallucination and fabrication
10. **Unbounded Consumption** (LLM10) — resource exhaustion and DoS

**AISkills contribution:** The `ai-security-review` skill maps directly to these risks, guiding agents through a structured security audit grounded in this framework.

### 3.2 Indirect Prompt Injection

A particularly important attack for RAG systems and agents with web access: malicious instructions embedded in retrieved documents that hijack the agent.

**AISkills contribution:** Both `rag-architecture` and `ai-security-review` skills explicitly address this risk.

---

## 4. Competing Approaches

### 4.1 Large Prompt Libraries

**Approach:** Collections of standalone prompts (e.g., "You are a senior engineer, please review this code...")

**Limitations:**
- No structured workflow
- No composability
- No validation
- Inconsistent quality
- No AI engineering focus

### 4.2 Framework-Specific Rules (`.cursorrules`, `.claude/settings/`)

**Approach:** Project-level rules files that modify agent behavior globally.

**Limitations:**
- Rules apply to all tasks, not selected for task-specific relevance
- Hard to compose and reuse across projects
- No structured skill format
- No discovery mechanism

### 4.3 Agent Memory Systems (LangGraph, custom memory)

**Approach:** Agent stores and retrieves past decisions as context.

**Not competing with AISkills:** Memory is an *execution mechanism*. AISkills defines the *engineering methodology*. They are complementary.

### 4.4 Code Generation Fine-tuning

**Approach:** Fine-tune models on high-quality code.

**Not competing with AISkills:** Fine-tuning improves code quality at generation time. AISkills improves *engineering process* (requirements, architecture, testing, evaluation). Complementary.

---

## 5. Gaps and Differentiation Opportunities

Based on this research, AISkills addresses these unmet needs:

| Gap | AISkills Response |
|-----|------------------|
| No structured engineering process for AI agents | Composable skill library covering full SDLC |
| No AI engineering skills in existing collections | First-class RAG, agent design, evaluation, security skills |
| No evaluation discipline built into workflows | Evaluation planning is a required workflow stage |
| No AI security workflow | `ai-security-review` skill grounded in OWASP GenAI Top 10 |
| Agents skip requirements analysis | `requirements-analysis` and `requirement-clarification` as mandatory early stages |
| Agents invent architecture without inspection | `repository-discovery` skill required before any implementation |
| No human-in-the-loop enforcement | `AGENTS.md` and all skills explicitly define approval gates |
| No quality validation for skills themselves | CLI validation (`aiskills validate`) and CI enforcement |

---

## 6. Design Decisions Derived from Research

1. **Adopt standard SKILL.md format** — maximizes compatibility with Claude Code, Cursor, Codex, Gemini CLI without code wrappers
2. **Extend SKILL.md frontmatter** — add `category`, `tags`, `risk`, `status`, `related-skills` for AISkills-specific discovery and validation
3. **Python CLI** — AI/ML audience is Python-native; provides real value via validation and scaffolding
4. **Tool-agnostic evaluation references** — reference RAGAS methodology, not RAGAS the library; engineers choose their own tooling
5. **OWASP grounding** — ground AI security content in the authoritative public standard, properly attributed
6. **14 high-quality skills for v0.1** — quality over quantity; each skill must be genuinely useful, not a stub
7. **Apache 2.0 license** — enterprise-friendly, includes patent grant, compatible with community contributions

---

## 7. Attribution

The following external resources informed the design of AISkills:

- **agentskills.io** — SKILL.md format specification (open standard, adopted for interoperability)
- **OWASP GenAI LLM Top 10** — AI security risk taxonomy (referenced, not reproduced)
- **RAGAS** — RAG evaluation dimensions (methodology referenced, library not bundled)
- **DeepEval** — evaluation patterns (conceptually referenced)
- **VoltAgent/awesome-agent-skills** — ecosystem overview (studied, not copied)

All skill content in AISkills is original. No prompts, instructions, or documentation have been copied from other repositories.
