# Generic Agent Adapter

This guide explains how to use AISkills with any AI coding agent that supports Markdown instructions.

---

## The Universal Pattern

Any agent that accepts text instructions can use AISkills. The pattern is:

1. Include `AGENTS.md` content in your system prompt or conversation start
2. Include `CONTEXT.md` for your project
3. Include the relevant `SKILL.md` content for the current task
4. Let the agent follow the skill's workflow

---

## Method 1: System Prompt Injection

Add to your system prompt:

```
You are an AI coding agent. Before any task:

1. You follow the AISkills engineering methodology.
2. You always start by reading CONTEXT.md and AGENTS.md.
3. For each task, you select and follow the appropriate skill from the AISkills library.
4. You never start implementation without understanding requirements and architecture.
5. You always ask for human approval before destructive or production actions.

When asked to implement a feature, follow the feature-development workflow.
When asked to build a RAG system, follow the rag-development workflow.
When asked to fix a bug, follow the bug-fixing workflow.
```

---

## Method 2: Paste Skill Content

For any task, paste the relevant skill content into your conversation:

```
User: I need to build a RAG system for our docs.
      Follow this skill: [paste contents of skills/ai/rag/rag-architecture/SKILL.md]
```

---

## Method 3: Reference the Skill Path

If the agent has file system access:

```
User: Read the skill at skills/ai/evaluation/rag-evaluation/SKILL.md and
      evaluate our RAG pipeline using that methodology.
```

---

## Skill Selection Guide

| Task | Recommended skill |
|------|-----------------|
| Explore a new codebase | `repository-discovery` |
| Analyze requirements | `requirements-analysis` |
| Design a system | `architecture-design` |
| Plan implementation | `implementation-planning` |
| Write tests | `tdd` |
| Debug a bug | `bug-diagnosis` |
| Review code | `code-review` |
| Build a RAG system | `rag-architecture` |
| Evaluate RAG quality | `rag-evaluation` |
| Design an agent | `agent-design` |
| Security audit | `ai-security-review` |
| Production checklist | `production-readiness` |

---

## Minimal Setup for Any Project

```bash
# Install CLI
pip install aiskills

# Generate AGENTS.md and CONTEXT.md
cd your-project
aiskills init

# Fill in CONTEXT.md with your project details
```

Then tell your agent: "Read AGENTS.md and CONTEXT.md before starting."

---

*AISkills v0.1.0 — Generic adapter guide*
