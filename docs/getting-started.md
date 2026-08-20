# Getting Started with AISkills

This guide helps you get AISkills running in your project in under 10 minutes.

---

## Prerequisites

- Python 3.10 or later
- pip
- An AI coding agent (Claude Code, Gemini CLI, Cursor, Codex, or any SKILL.md-compatible agent)

---

## Installation

### Install the CLI

```bash
pip install aiskills
```

Verify installation:

```bash
aiskills --version
# aiskills 0.1.0
```

### Or use skills without installing

If you just want to use individual skills without the CLI:

```bash
git clone https://github.com/karthikrshet/aiskills.git
```

Then copy the skill files you need into your project.

---

## Initialize AISkills in Your Project

```bash
cd your-project
aiskills init
```

This creates two files:

```
your-project/
├── AGENTS.md     ← Instructions for your AI coding agent
└── CONTEXT.md    ← Template to describe your project
```

**Next step:** Open `CONTEXT.md` and fill in your project details.

The more detail you provide in `CONTEXT.md`, the better your agent will perform. At minimum, fill in:
- Project purpose
- Primary language and framework
- Architecture type
- Key conventions

---

## Point Your Agent to AISkills

### Claude Code

```bash
# Copy skills to your project's Claude skills directory
mkdir -p .claude/skills
cp -r /path/to/aiskills/skills/* .claude/skills/
```

Claude Code will auto-discover skills in `.claude/skills/` and activate them based on your task.

### Gemini CLI

```bash
mkdir -p .agents/skills
cp -r /path/to/aiskills/skills/* .agents/skills/
```

### Cursor

Add to your `.cursorrules`:

```
When starting a new task, check the skills in .aiskills/skills/ and use the
most relevant skill to guide your approach.
```

Then copy skills:

```bash
mkdir -p .aiskills/skills
cp -r /path/to/aiskills/skills/* .aiskills/skills/
```

### Generic agents

For any agent, include the skill content in your task description:

```
[Paste the content of SKILL.md here, or instruct the agent to read it]
```

See [adapters/](../adapters/) for agent-specific setup guides.

---

## Your First AISkills-Powered Task

### Example: Adding a feature with the right process

Instead of:
```
"Add a user authentication feature"
```

Tell your agent:
```
"Before starting, read AGENTS.md and CONTEXT.md in this repository.
Then use the requirements-analysis skill to analyze the authentication
feature requirement, then the architecture-design skill to design the
solution, then create an implementation plan."
```

Or if your agent auto-discovers skills:
```
"Add a user authentication feature"
```
*(The agent will automatically use the requirements-analysis and
implementation-planning skills based on the task context.)*

---

## Explore Available Skills

```bash
aiskills list
```

```
SKILL                     CATEGORY          RISK    STATUS
────────────────────────────────────────────────────────────
repository-discovery      discovery         low     alpha
requirements-analysis     requirements      low     alpha
requirement-clarification requirements      low     alpha
architecture-design       architecture      medium  alpha
implementation-planning   implementation    medium  alpha
tdd                       testing           low     alpha
bug-diagnosis             debugging         low     alpha
code-review               review            low     alpha
agent-design              ai/agent-design   medium  alpha
rag-architecture          ai/rag            medium  alpha
rag-evaluation            ai/evaluation     low     alpha
context-engineering       ai/context-eng.   low     alpha
ai-security-review        ai/ai-security    low     alpha
production-readiness      ai/production-ai  high    alpha
```

---

## Search for Relevant Skills

```bash
aiskills search "RAG"
# → rag-architecture, rag-evaluation, context-engineering

aiskills search "security"
# → ai-security-review, code-review

aiskills search "testing"
# → tdd, code-review
```

---

## Get Skill Details

```bash
aiskills info rag-evaluation
```

---

## Run Validation

Check that all skills in your local copy are valid:

```bash
aiskills validate
```

---

## Check Repository Health

```bash
aiskills doctor
```

This checks:
- `AGENTS.md` present
- `CONTEXT.md` present and filled in
- No placeholder content in CONTEXT.md
- Skills directory accessible

---

## Next Steps

- Read [Concepts](concepts.md) to understand the AISkills model
- Explore [AI Engineering](ai-engineering.md) for RAG, agent, and evaluation skills
- See [Workflows](workflows.md) for end-to-end engineering pipelines
- Read [Skill Authoring](skill-authoring.md) to create your own skills

---

## Quick Reference

```bash
aiskills init                    # Initialize in current project
aiskills list                    # List all skills
aiskills search <query>          # Search by keyword
aiskills info <skill-name>       # Skill details
aiskills validate                # Validate all skills
aiskills doctor                  # Repository health check
```

---

*AISkills v0.1.0 — alpha. See [CHANGELOG.md](../CHANGELOG.md) for what's new.*
