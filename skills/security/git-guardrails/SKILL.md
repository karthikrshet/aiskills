---
name: git-guardrails
description: |
  Use this skill to enforce strict safety boundaries on git operations, branch
  management, and destructive shell commands. Prevents accidental force pushes,
  hard resets, secret commits, unstashed code loss, and unauthorized production
  branch modifications.
version: "0.1.0"
category: security
tags: [git, guardrails, safety, security, destructive-actions, protection]
risk: high
status: alpha
related-skills:
  - ai-security-review
  - code-review
  - implementation-planning
---

# Git Guardrails

## Purpose

AI coding agents given shell access can accidentally execute catastrophic version control commands: force-pushing over main branches, running `git reset --hard` and wiping uncommitted human work, committing `.env` files containing live API keys, or deleting untracked files with `git clean -fd`.

This skill defines non-negotiable safety guardrails that every AI coding agent must enforce whenever running git and filesystem commands.

## When to Use

- Before running any git commit, push, reset, checkout, branch, or stash command
- When setting up an agent's terminal safety policies
- When automating CI/CD or multi-step repository modification scripts

## When Not to Use

- Read-only inspection commands (`git status`, `git log`, `git diff`)
- Non-git development tasks

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Proposed git command | ✅ | The exact shell command the agent intends to run |
| Current git status | ✅ | Staged, unstaged, and untracked file listing |
| Current branch name | ✅ | Active branch (e.g. `main`, `master`, `feature/...`) |

## Preconditions

- [ ] Agent has verified the active branch name (`git branch --show-current`)
- [ ] Agent has verified unstaged changes (`git status --short`)

## Workflow

### Step 1: Check Command Against Prohibited Blocklist

The following commands are **strictly prohibited** unless explicit written human approval with the exact command is given:

1. `git push --force` or `git push -f` (to any remote or branch)
2. `git reset --hard` (destroys working tree changes)
3. `git clean -fd` or `git clean -f` (destroys untracked files)
4. `git branch -D` (force-deletes unmerged branches)
5. `git stash drop` or `git stash clear`
6. `git rebase` on public/shared branches (`main`, `master`, `release`)
7. Direct commits or pushes to protected branches (`main`, `master`, `prod`) without review

### Step 2: Pre-Commit Secret Scan

Before running `git add .` or `git commit`, inspect staged files for:
- `.env`, `.env.local`, `.env.production`
- Files containing tokens, private keys (`*.pem`, `*.key`), AWS credentials, or OAuth secrets
- Credentials matching patterns: `api_key = "..."`, `secret = "..."`, `bearer ...`

**Rule:** If any credential or environment file is staged, abort immediately.

### Step 3: Branch Isolation Verification

- Verify that new features or bug fixes are developed on dedicated feature branches (`feature/...` or `fix/...`).
- Never make speculative code changes directly on `main` or `master`.

### Step 4: Atomic Commit Generation

When committing:
- Write clear, conventional commit messages: `feat: ...`, `fix: ...`, `docs: ...`, `refactor: ...`, `test: ...`.
- Stage only files relevant to the specific commit. Never run blind `git add -A` if unrelated working files exist.

### Step 5: Safe Push Execution

- Check remote target: `git push origin <branch-name>`.
- Never use wildcard pushes (`git push --all`).

## Decision Points

| Condition | Tier | Action |
|-----------|------|--------|
| Agent needs to discard broken changes | Consult | Suggest `git stash` instead of `git reset --hard` to preserve recovery options |
| Staging contains a file ending in `.env` | Approve | **Stop immediately**. Notify user and remove file from staging (`git restore --staged <file>`) |
| Command would overwrite remote history | Approve | **Full stop**. Present risks to human and require explicit confirmation |

## Safety Constraints

- Never commit real secrets, API keys, private keys, or passwords
- Never run `git reset --hard` without creating a backup branch or stash first
- Never force-push to `main` or `master`
- Never delete untracked files without listing each file to the human
- Never bypass pre-commit hooks (`--no-verify`) without explicit user instruction

## Expected Output

- Clean, verified git commands executed safely
- Atomic commits with clear conventional messages
- Zero lost code, zero wiped stashes, zero leaked credentials

## Validation

- [ ] Active branch was checked before modifying code
- [ ] Staged files were scanned for secrets before committing
- [ ] No prohibited git commands were executed without approval
- [ ] Working tree status is clean and verifiable

## Failure Handling

| Failure | What to do |
|---------|------------|
| Working tree in detached HEAD state | Create a new recovery branch (`git checkout -b recovery-branch`) before making edits |
| Merge conflict during pull/rebase | Stop and present conflicting files to the human; do not auto-resolve blindly |

## Examples

### Example 1: Preventing an accidental secret commit

**Scenario:** Agent runs `git add .` in a repo where `.env` was recently created with `OPENAI_API_KEY=sk-...`.

**Agent action:**
1. Scans staged list: detects `.env`.
2. Runs `git restore --staged .env`.
3. Adds `.env` to `.gitignore`.
4. Commits only source files: `git commit -m "feat: add OpenAI client config"`.

## Related Skills

- `ai-security-review` — secret scanning and OWASP security
- `code-review` — pre-commit review
- `implementation-planning` — ordered changes
