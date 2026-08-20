# AISkills Skill Specification

**Version:** 0.1.0  
**Status:** Alpha

This document defines the canonical format for AISkills skill definitions. All skills in this repository and all community contributions must conform to this specification.

---

## 1. What is a Skill?

A skill is a **composable, reusable engineering workflow definition** for AI coding agents.

A skill is **not:**
- A single-shot prompt
- A code snippet
- A configuration file

A skill **is:**
- A structured, documented methodology for solving a specific engineering problem
- Machine-readable (YAML frontmatter for agent discovery)
- Human-readable (Markdown body for engineering depth)
- Composable (connects to other skills via `related-skills`)
- Validated (must pass `aiskills validate`)

---

## 2. Skill Directory Structure

A skill lives in its own directory:

```
skills/<category>/<skill-name>/
├── SKILL.md          # Required — the skill definition
├── references/       # Optional — supplementary documentation
│   └── *.md
├── scripts/          # Optional — helper scripts
│   └── *.sh / *.py
└── examples/         # Optional — worked examples
    └── *.md
```

**Rules:**
- `SKILL.md` is always required
- The directory name must match the `name` field in frontmatter
- Directory names follow the same rules as skill names (lowercase-hyphenated)
- Scripts in `scripts/` are treated as untrusted by default — document what each script does

---

## 3. SKILL.md Format

### 3.1 Structure

```
---
[YAML frontmatter]
---

[Markdown body]
```

The YAML frontmatter is separated from the Markdown body by `---` delimiters.

### 3.2 YAML Frontmatter Schema

```yaml
---
name: string              # Required
description: string       # Required
version: string           # Required
category: string          # Required
tags: list[string]        # Required
risk: enum                # Required
status: enum              # Required
related-skills: list[str] # Optional
---
```

#### Field Specifications

**`name`** (required)
- Type: string
- Format: `lowercase-hyphenated`
- Pattern: `^[a-z][a-z0-9-]{1,48}[a-z0-9]$`
- Max length: 50 characters
- Must be unique across all skills in the registry
- Examples: `repository-discovery`, `rag-evaluation`, `bug-diagnosis`

**`description`** (required)
- Type: string (may be multi-line YAML block scalar using `|`)
- Purpose: Used by agents to decide whether to activate this skill
- Content: Describe *when and why* an agent should use this skill. Be specific.
- Max length: 500 characters (enforced)
- Good example:
  ```yaml
  description: |
    Use this skill to systematically explore an unfamiliar codebase before
    making any changes. Activates when the task involves an unknown repository,
    new feature addition, or debugging without prior context.
  ```
- Bad example:
  ```yaml
  description: Helps with code.
  ```

**`version`** (required)
- Type: string
- Format: semantic version in quotes: `"0.1.0"`
- Increment patch version for content improvements
- Increment minor version for new sections or structural changes
- Major version reserved for breaking format changes

**`category`** (required)
- Type: string
- Format: `category` or `category/subcategory`
- Valid top-level categories:
  - `discovery`
  - `requirements`
  - `architecture`
  - `implementation`
  - `testing`
  - `debugging`
  - `code-review`
  - `security`
  - `performance`
  - `documentation`
  - `ai/agent-design`
  - `ai/rag`
  - `ai/memory`
  - `ai/prompting`
  - `ai/context-engineering`
  - `ai/evaluation`
  - `ai/hallucination`
  - `ai/guardrails`
  - `ai/ai-security`
  - `ai/production-ai`

**`tags`** (required)
- Type: list of strings
- Count: 1–10 tags
- Format: lowercase, single words or hyphenated phrases
- Purpose: keyword search and discovery
- Examples: `[rag, retrieval, evaluation, faithfulness]`

**`risk`** (required)
- Type: enum
- Values:
  - `low` — read-only, analysis, no side effects on the codebase
  - `medium` — creates or modifies files; human review recommended before executing suggestions
  - `high` — can result in destructive actions; explicit human approval required at each destructive step

**`status`** (required)
- Type: enum
- Values:
  - `experimental` — concept only; subject to complete redesign
  - `alpha` — working but format/content may change
  - `beta` — stable format, undergoing community validation
  - `stable` — validated by real-world use; no breaking changes without major version bump

**`related-skills`** (optional)
- Type: list of strings
- Each entry must be a valid skill `name` that exists in the registry
- Used by `aiskills validate` to check for dangling references
- Used by `aiskills info` to suggest next skills

---

## 4. Markdown Body

### 4.1 Required Sections

All 13 sections below are required. `aiskills validate` will fail if any are missing.

Sections must appear in this order:

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

### 4.2 Section Specifications

#### `## Purpose`

**What it is:** A concise description of the engineering problem this skill solves.

**Format:** 1–3 paragraphs of prose. No bullet lists.

**Requirements:**
- Must answer: "What engineering problem does this solve?"
- Must explain *why* a structured skill is needed (vs. just doing the task ad hoc)

**Anti-patterns to avoid:**
- Vague statements: "This skill helps with development"
- Scope creep: "This skill handles requirements AND architecture AND testing"

---

#### `## When to Use`

**What it is:** Specific conditions under which an agent should activate this skill.

**Format:** Bullet list of concrete situations.

**Requirements:**
- At least 3 specific conditions
- Each condition should be actionable (an agent can evaluate it as true/false)

**Example:**
```markdown
## When to Use

- The task involves adding a feature to an unfamiliar codebase
- The human has not described the current architecture
- No `CONTEXT.md` exists or it has not been read yet
- Debugging a problem in a repository the agent has not seen before
```

---

#### `## When Not to Use`

**What it is:** Conditions where this skill is NOT appropriate. Prevents misapplication.

**Format:** Bullet list. Include alternative skill where applicable.

**Requirements:**
- At least 2 conditions
- Reference alternative skills where relevant

---

#### `## Inputs`

**What it is:** The information an agent needs to execute this skill.

**Format:** Table.

```markdown
| Input | Required | Description |
|-------|----------|-------------|
| Repository path | ✅ | Root directory of the codebase |
| Task description | ✅ | What the human wants to accomplish |
| CONTEXT.md | optional | Project context if available |
```

---

#### `## Preconditions`

**What it is:** What must be true or done before this skill can run.

**Format:** Checklist.

```markdown
- [ ] Agent has read `CONTEXT.md` if present
- [ ] Agent has identified the programming language
- [ ] `repository-discovery` skill has been completed (or equivalent)
```

---

#### `## Workflow`

**What it is:** The step-by-step engineering process.

**Format:** Numbered steps. Each step should have:
- A descriptive heading
- What the agent inspects or does
- What the agent produces

**Requirements:**
- At least 3 steps
- Each step must produce a concrete artifact or decision
- No step can be vague ("analyze the code")

**Example step format:**
```markdown
### Step 1: Map Repository Structure

**Inspect:**
- List top-level directories and their apparent purpose
- Identify entry points (`main.py`, `index.ts`, `cmd/`, etc.)
- Find configuration files (`pyproject.toml`, `package.json`, `.env.example`)

**Produce:**
- A directory map with a one-line description of each major directory
```

---

#### `## Decision Points`

**What it is:** Situations where the agent must pause and consult or get approval from the human.

**Format:** Table or bullet list with tier classification.

```markdown
| Condition | Tier | Question to Ask |
|-----------|------|----------------|
| Requirements are ambiguous | Consult | "The requirement says X — do you mean Y or Z?" |
| Proposed change affects production config | Approve | "This change modifies production config. Confirm?" |
```

Tiers: `Inform` / `Consult` / `Approve`

**Requirements:**
- At least 2 decision points
- All destructive actions must be classified as `Approve`

---

#### `## Safety Constraints`

**What it is:** Hard rules the agent must never violate when executing this skill.

**Format:** Bullet list starting with "Never" or "Always".

**Requirements:**
- At least 3 constraints
- Must include constraints relevant to the skill's risk level

---

#### `## Expected Output`

**What it is:** The concrete artifacts or decisions the agent produces by completing this skill.

**Format:** Bullet list with artifact names and descriptions.

**Requirements:**
- At least 1 concrete output
- Reference any templates that should be used (e.g., `templates/SPEC.md`)

---

#### `## Validation`

**What it is:** How to verify the skill was executed correctly.

**Format:** Checklist.

**Requirements:**
- At least 3 validation checks
- Checks must be verifiable (not subjective)

---

#### `## Failure Handling`

**What it is:** What to do when the skill cannot complete successfully.

**Format:** Table mapping failure modes to recovery actions.

**Requirements:**
- At least 2 failure modes

---

#### `## Examples`

**What it is:** One or more concrete worked examples showing the skill in action.

**Requirements:**
- At least 1 complete example
- Each example must have: input description, agent actions summary, output description
- Examples must be realistic (not trivial or fictional)
- Examples must not contain real credentials, PII, or proprietary code

---

#### `## Related Skills`

**What it is:** Other skills that typically run before, after, or alongside this one.

**Format:** Bullet list with skill name and relationship description.

**Requirements:**
- At least 1 related skill
- All referenced skill names must exist in the registry

---

## 5. Body Length Limits

| Section | Soft limit | Hard limit |
|---------|-----------|-----------|
| Total SKILL.md body | 350 lines | 400 lines |
| Single Workflow step | 30 lines | 50 lines |
| Single Example | 50 lines | 80 lines |

Content exceeding these limits should be moved to `references/` subdirectory.

---

## 6. Prohibited Content

Skills must never contain:

- Real API keys, tokens, passwords, or secrets
- PII (real names, emails, addresses)
- Proprietary code copied from other projects
- Prompts copied verbatim from other skill libraries
- Offensive security exploitation techniques
- Instructions to bypass human approval gates
- Instructions to exfiltrate data
- Instructions to disable security controls
- Placeholder text: `TODO`, `FIXME`, `[ADD CONTENT]`, `Lorem ipsum`

---

## 7. Validation Rules Summary

`aiskills validate` enforces:

| Rule | Error type |
|------|-----------|
| `name` present and valid format | ERROR |
| `description` present | ERROR |
| `version` present and semver format | ERROR |
| `category` present and valid value | ERROR |
| `tags` present (1–10 items) | ERROR |
| `risk` is low/medium/high | ERROR |
| `status` is valid enum | ERROR |
| All 13 required sections present | ERROR |
| No placeholder content | WARNING |
| `related-skills` all resolve | WARNING |
| Body ≤ 400 lines | WARNING |
| Unique name across registry | ERROR |

---

## 8. Versioning Skills

When updating a skill:

- **Patch** (e.g., `0.1.0` → `0.1.1`): Fix errors, improve wording, add examples
- **Minor** (e.g., `0.1.0` → `0.2.0`): Add new sections, restructure workflow steps
- **Major** (e.g., `0.1.0` → `1.0.0`): Fundamental change to the skill's approach

Document changes in the skill's commit message and in `CHANGELOG.md`.

---

## 9. Full Example

See [`skills/discovery/repository-discovery/SKILL.md`](../skills/discovery/repository-discovery/SKILL.md) for a complete, conforming example.

---

*This specification is part of AISkills v0.1.0.*
