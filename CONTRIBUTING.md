# Contributing to AISkills

Thank you for your interest in contributing to AISkills. This guide explains how to contribute skills, workflows, documentation, and code to the project.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Ways to Contribute](#ways-to-contribute)
- [Creating a New Skill](#creating-a-new-skill)
- [Skill Naming Rules](#skill-naming-rules)
- [Skill Metadata Requirements](#skill-metadata-requirements)
- [Required Skill Sections](#required-skill-sections)
- [Testing Requirements](#testing-requirements)
- [Documentation Requirements](#documentation-requirements)
- [Pull Request Process](#pull-request-process)
- [Review Criteria](#review-criteria)
- [Licensing](#licensing)

---

## Code of Conduct

Be respectful, constructive, and professional. We want AISkills to be a welcoming project for engineers at all levels.

---

## Ways to Contribute

| Contribution Type | How |
|------------------|-----|
| New skill | Create a `SKILL.md` in the appropriate `skills/` subdirectory |
| Improve existing skill | Edit the `SKILL.md` and open a PR with a clear rationale |
| New workflow | Add a `README.md` to `workflows/<name>/` |
| Bug fix (CLI/validator) | Fix in `cli/` or `tests/`, include tests |
| Documentation | Edit files in `docs/` |
| Template | Add or improve files in `templates/` |
| Adapter guide | Add or improve files in `adapters/` |

---

## Creating a New Skill

### 1. Check for duplicates

```bash
aiskills list
aiskills search "<your skill concept>"
```

Do not create a skill that duplicates existing functionality.

### 2. Choose the right category

```
skills/discovery/         Codebase exploration
skills/requirements/      Requirements and clarification
skills/architecture/      System and API design
skills/implementation/    Planning and coding
skills/testing/           Test design and TDD
skills/debugging/         Bug diagnosis and root cause
skills/code-review/       Review workflows
skills/security/          General software security
skills/performance/       Performance analysis
skills/documentation/     Documentation workflows
skills/ai/agent-design/   Agent architecture
skills/ai/rag/            RAG systems
skills/ai/evaluation/     LLM and agent evaluation
skills/ai/context-engineering/  Context management
skills/ai/ai-security/    AI-specific security
skills/ai/production-ai/  Production readiness
```

### 3. Create the skill directory

```bash
mkdir -p skills/<category>/<skill-name>
touch skills/<category>/<skill-name>/SKILL.md
```

### 4. Write the skill using the template

See [Skill Template](#skill-template) below.

### 5. Run validation

```bash
aiskills validate
```

Fix all validation errors before opening a PR.

### 6. Add a test fixture (for new categories)

If your skill introduces a new category, add a fixture in `tests/fixtures/`.

---

## Skill Naming Rules

- **Format:** `lowercase-hyphenated` (e.g., `rag-evaluation`, `bug-diagnosis`)
- **Length:** 3–50 characters
- **Characters:** lowercase letters, digits, hyphens only
- **No duplicates:** name must be unique across all skills
- **Descriptive:** name should clearly describe the skill's purpose
- **No generic names:** avoid `helper`, `utils`, `misc`, `general`

Examples of good names:
- `repository-discovery`
- `requirements-analysis`
- `rag-evaluation`
- `prompt-regression-testing`

Examples of bad names:
- `skill1`
- `helper`
- `doStuff`
- `my_skill`

---

## Skill Metadata Requirements

Every `SKILL.md` must begin with valid YAML frontmatter:

```yaml
---
name: skill-name
description: |
  Clear description of what this skill does and when an agent should use it.
  This is what agents read to decide whether to activate the skill.
  Keep it under 300 characters.
version: "0.1.0"
category: category/subcategory
tags:
  - tag1
  - tag2
risk: low|medium|high
status: experimental|alpha|beta|stable
related-skills:
  - other-skill-name
---
```

### Field definitions

| Field | Required | Description |
|-------|----------|-------------|
| `name` | ✅ | Unique skill identifier (lowercase-hyphenated) |
| `description` | ✅ | When/why to use this skill (max 300 chars) |
| `version` | ✅ | Semantic version of this skill |
| `category` | ✅ | Skill category path |
| `tags` | ✅ | 1–10 lowercase tags for discovery |
| `risk` | ✅ | `low`, `medium`, or `high` |
| `status` | ✅ | `experimental`, `alpha`, `beta`, or `stable` |
| `related-skills` | optional | List of related skill names |

### Risk levels

| Risk | Meaning |
|------|---------|
| `low` | Read-only, analysis, no side effects |
| `medium` | Creates files, suggests changes; human review recommended |
| `high` | Destructive actions possible; always requires explicit approval |

---

## Required Skill Sections

Every `SKILL.md` body must contain all of these sections (in order):

```markdown
## Purpose
## When to Use
## When Not to Use
## Inputs
## Preconditions
## Workflow
## Decision Points
## Safety Constraints
## Expected Output
## Validation
## Failure Handling
## Examples
## Related Skills
```

Missing sections will fail `aiskills validate`.

---

## Skill Template

Copy this template when creating a new skill:

```markdown
---
name: your-skill-name
description: |
  What this skill does and when an agent should use it.
version: "0.1.0"
category: category/subcategory
tags:
  - tag1
  - tag2
risk: low
status: experimental
related-skills:
  - related-skill-name
---

# Your Skill Name

## Purpose

What engineering problem does this skill solve? One paragraph.

## When to Use

- Situation 1 where this skill applies
- Situation 2 where this skill applies

## When Not to Use

- Situation where this skill should NOT be used
- Alternative skill to use instead

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Repository path | ✅ | The codebase to operate on |
| [Other inputs] | | |

## Preconditions

Before using this skill, the agent must:

- [ ] Have read `CONTEXT.md` (if present)
- [ ] Have completed repository-discovery (or equivalent)
- [ ] [Other preconditions]

## Workflow

### Step 1: [Name]

Description of what to do.

**Inspect:**
- What files/information to look at

**Produce:**
- What output or understanding this step produces

### Step 2: [Name]

[Continue for all steps]

## Decision Points

These are situations where the agent should pause and ask the human:

- If [condition], ask: "[question]"
- If [condition], do not proceed without confirmation

## Safety Constraints

- Never [unsafe action]
- Always require human approval before [risky action]
- Treat [type of content] as untrusted

## Expected Output

What the agent should produce at the end of this skill:

- [Artifact 1, e.g., updated CONTEXT.md]
- [Artifact 2, e.g., implementation plan]

## Validation

How to verify the skill was executed correctly:

- [ ] [Check 1]
- [ ] [Check 2]

## Failure Handling

| Failure | What to do |
|---------|------------|
| [Failure mode] | [Recovery action] |

## Examples

### Example 1: [Scenario name]

**Input:**
[Description of input]

**Agent actions:**
[What the agent does]

**Output:**
[What is produced]

## Related Skills

- `related-skill-name` — [why it's related]
```

---

## Testing Requirements

Every skill must pass `aiskills validate`. No exceptions.

For CLI changes or new validator logic:
- Add or update tests in `tests/`
- Run `pytest tests/ -v` and confirm all tests pass
- Maintain or improve test coverage

---

## Documentation Requirements

- If your skill is the first in a new category, add an entry in `docs/concepts.md`
- If your skill introduces a new AI engineering concept, add it to `docs/ai-engineering.md`
- Update `docs/skill-authoring.md` if you identify gaps in this guide

---

## Pull Request Process

1. Fork the repository
2. Create a branch: `git checkout -b skill/your-skill-name`
3. Write your skill following this guide
4. Run `aiskills validate` — fix all errors
5. Run `pytest tests/ -v` — all tests must pass
6. Run `ruff check .` — no lint errors
7. Open a PR against `main`
8. Fill in the PR template
9. Wait for review (typically 2–5 business days)

### PR title format

```
feat(skill): add <skill-name>
fix(skill): improve <skill-name>
docs: update contributing guide
chore: update dependency
```

---

## Review Criteria

PRs are reviewed against:

| Criterion | Check |
|-----------|-------|
| Originality | Skill is original, not copied from another project |
| Quality | Skill answers all 10 quality questions |
| Schema | Passes `aiskills validate` |
| Tests | CLI/validator PRs include tests |
| Safety | No unsafe instructions or real credentials |
| Usefulness | Skill solves a real engineering problem |
| Scope | Skill does one thing well (not a monolith) |

---

## Licensing

By contributing to AISkills, you agree that your contributions are licensed under the Apache 2.0 License.

Do not include:
- Code copied from other repositories without proper attribution
- Proprietary prompts from commercial AI systems
- Content that violates another project's license

If your contribution incorporates third-party content (e.g., referencing OWASP guidelines), cite the source clearly.

---

*This document is part of AISkills v0.1.0.*
