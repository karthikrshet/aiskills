# Cursor Adapter

This guide explains how to use AISkills with Cursor.

---

## Setup

### Option 1: Via `.cursorrules`

Add to your `.cursorrules` file:

```
# AISkills Integration

Before starting any task:
1. Read AGENTS.md and CONTEXT.md in this project
2. Check .aiskills/skills/ for relevant skills for the task
3. Follow the workflow defined in the relevant skill's SKILL.md
4. Respect all human approval gates (marked with ⚠️ REQUIRES APPROVAL)

Available skills in .aiskills/skills/:
- repository-discovery: Explore the codebase first
- requirements-analysis: Structure requirements
- implementation-planning: Create a plan before coding
- tdd: Write tests first
- rag-architecture: Design RAG systems
- ai-security-review: Security audit before production

Never start implementation without reading the relevant skill first.
```

### Option 2: Copy skills to project directory

```bash
mkdir -p .aiskills/skills
cp -r /path/to/aiskills/skills/* .aiskills/skills/
```

### Option 3: Reference skills by path

In your task description to Cursor:

```
Follow the skill at .aiskills/skills/rag-architecture/SKILL.md to design
our documentation Q&A system.
```

---

## Recommended Project Files

```bash
aiskills init
# Creates AGENTS.md and CONTEXT.md
```

Add to `.cursorrules`:
```
Read AGENTS.md at the start of every conversation.
```

---

## Notes

- Cursor does not auto-discover skills — explicit reference is required
- Include the most relevant 2–3 skills in `.cursorrules` for best results
- `CONTEXT.md` provides strong grounding for Cursor's understanding

---

*AISkills v0.1.0 — Cursor adapter guide*
