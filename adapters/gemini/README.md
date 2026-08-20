# Gemini CLI Adapter

This guide explains how to use AISkills with Gemini CLI.

---

## How Gemini CLI Discovers Skills

Gemini CLI (the `agy` CLI / Antigravity IDE) auto-discovers skills from `.agents/skills/` in the workspace root. Skills with SKILL.md format are loaded on demand based on task context.

---

## Setup

### Install skills in your workspace

```bash
# In your project root
mkdir -p .agents/skills

# Copy specific skills
cp -r /path/to/aiskills/skills/discovery/repository-discovery .agents/skills/
cp -r /path/to/aiskills/skills/ai/rag/rag-architecture .agents/skills/

# Or copy all AISkills
cp -r /path/to/aiskills/skills/* .agents/skills/
```

### Initialize project context

```bash
aiskills init
# Creates AGENTS.md and CONTEXT.md in project root
```

Gemini CLI reads `AGENTS.md` before starting tasks.

---

## Using Skills with Gemini CLI

### Auto-discovery

```
User: Evaluate the RAG pipeline quality.
Gemini CLI: [activates rag-evaluation skill]
```

### Explicit reference

```
User: Use the ai-security-review skill to audit this system before deployment.
```

---

## Recommended AGENTS.md for Gemini CLI

```markdown
# AGENTS.md

Before any task:
1. Read CONTEXT.md
2. Apply repository-discovery skill
3. Select relevant AISkills workflow
4. Respect all human approval gates
```

---

## Notes

- Gemini CLI works well with the full skill set
- `CONTEXT.md` provides strong grounding for Gemini's context understanding
- Skills in `.agents/skills/` are auto-discovered; no configuration needed

---

*AISkills v0.1.0 — Gemini CLI adapter guide*
