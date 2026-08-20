# OpenAI Codex Adapter

This guide explains how to use AISkills with OpenAI Codex and Codex-based tools.

---

## Setup

Codex does not have a built-in skill discovery mechanism. Use one of these approaches:

### Option 1: System prompt integration

Include skill content in the system prompt or initial context:

```python
import openai

with open("skills/discovery/repository-discovery/SKILL.md") as f:
    skill_content = f.read()

response = openai.responses.create(
    model="codex-mini-latest",
    instructions=f"""
You are an AI coding agent. Follow this skill for the current task:

{skill_content}

Always respect human approval gates marked with ⚠️ REQUIRES APPROVAL.
""",
    input=user_task
)
```

### Option 2: Reference skills explicitly in the prompt

```
Before starting, read and follow the methodology in:
skills/implementation/implementation-planning/SKILL.md

Then plan the implementation for: [task description]
```

### Option 3: AISkills CLI pre-processing

Use `aiskills search` to find the relevant skill, then include it:

```bash
# Find relevant skill
aiskills search "RAG design"
# → rag-architecture

# Get skill content for injection
cat skills/ai/rag/rag-architecture/SKILL.md
```

---

## Recommended Workflow

```python
# 1. Initialize project
# aiskills init → creates AGENTS.md and CONTEXT.md

# 2. Read CONTEXT.md
with open("CONTEXT.md") as f:
    context = f.read()

# 3. Select and load relevant skill
with open("skills/discovery/repository-discovery/SKILL.md") as f:
    skill = f.read()

# 4. Construct system prompt
system_prompt = f"""
Project context:
{context}

Engineering skill to follow:
{skill}
"""
```

---

## Notes

- Codex works best with explicit skill inclusion in the prompt
- Keep skill content focused — use single skills, not entire directories
- For multi-step workflows, chain skills one at a time

---

*AISkills v0.1.0 — OpenAI Codex adapter guide*
