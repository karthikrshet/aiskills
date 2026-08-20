# Claude Code Adapter

This guide explains how to use AISkills with Claude Code.

---

## How Claude Code Discovers Skills

Claude Code automatically discovers and loads `SKILL.md` files from a `skills/` directory. When you describe a task, Claude Code reads skill `name` and `description` fields to decide which skills to activate — no explicit invocation needed.

**Supported directories:**
- `.claude/skills/` — project-level skills (recommended)
- Global skills directory (check your Claude Code version docs)

---

## Setup

### Option 1: Copy skills to your project

```bash
# In your project root
mkdir -p .claude/skills

# Copy specific skills
cp -r /path/to/aiskills/skills/discovery/repository-discovery .claude/skills/
cp -r /path/to/aiskills/skills/ai/rag/rag-architecture .claude/skills/
```

### Option 2: Copy all AISkills

```bash
mkdir -p .claude/skills
cp -r /path/to/aiskills/skills/* .claude/skills/
```

### Option 3: Symlink (development)

```bash
ln -s /path/to/aiskills/skills .claude/skills/aiskills
```

---

## Using Skills with Claude Code

### Auto-discovery (preferred)

With skills installed, Claude Code activates them automatically based on task context:

```
You: Build a RAG system for our documentation.

Claude Code: [automatically activates rag-architecture skill based on the task]
```

### Explicit invocation

You can also explicitly reference a skill:

```
You: Use the requirements-analysis skill to analyze this feature request.
```

### Chaining skills

```
You: Follow the RAG development workflow to design and implement a Q&A system.
```

Claude Code will work through the workflow stages using the appropriate skills.

---

## Recommended Project Setup

In your project root, create:

**`AGENTS.md`** — tells Claude Code how to use AISkills:

```markdown
# Agent Instructions

Before starting any task:
1. Read this file
2. Read CONTEXT.md
3. Use the repository-discovery skill
4. Select the appropriate AISkills workflow
5. Follow the workflow gates and approval requirements
```

**`CONTEXT.md`** — project context (run `aiskills init` to generate a template):

```bash
aiskills init
```

---

## Skills That Work Best with Claude Code

| Skill | Why it works well |
|-------|-----------------|
| `repository-discovery` | Claude Code has file system access for deep exploration |
| `implementation-planning` | Claude Code can present plans before executing |
| `tdd` | Claude Code can run tests directly |
| `code-review` | Claude Code can run linters and test suites |
| `rag-evaluation` | Claude Code can execute evaluation scripts |

---

## Notes

- Keep `SKILL.md` files under 400 lines for optimal Claude Code performance
- Use `references/` subdirectories for detailed documentation
- Skills with `risk: high` will prompt Claude Code to ask for human confirmation

---

*AISkills v0.1.0 — Claude Code adapter guide*
