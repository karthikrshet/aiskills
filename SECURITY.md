# Security Policy

## Overview

AISkills is a collection of reusable AI engineering skill definitions and workflow templates for AI coding agents. This document covers vulnerability reporting, responsible disclosure, and security scope for the AISkills project.

---

## Supported Versions

| Version | Security Fixes |
|---------|---------------|
| 0.1.x   | ✅ Yes        |

---

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

If you discover a security vulnerability in AISkills, please report it privately:

1. **GitHub Security Advisories:** Use the private [Report a vulnerability](https://github.com/karthikrshet/aiskills/security/advisories/new) flow.
2. **Fallback:** If the private reporting flow is unavailable, contact a repository maintainer privately through GitHub and do not open a public issue.

Include in your report:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested remediation (if any)

You will receive an acknowledgment within **72 hours**.

---

## Responsible Disclosure

We follow a **90-day responsible disclosure** policy:

1. You report the vulnerability privately
2. We acknowledge receipt within 72 hours
3. We investigate and develop a fix
4. We release a fix and publish a security advisory
5. You may publish your findings after 90 days from the initial report, or after the fix is released (whichever is sooner)

We will credit researchers who report valid vulnerabilities in our security advisories, unless they prefer to remain anonymous.

---

## Security Scope

### In scope

- **CLI vulnerabilities** — arbitrary code execution, path traversal, command injection in the `aiskills` CLI
- **Skill validation bypass** — techniques that allow malicious skills to pass validation
- **Prompt injection via skill content** — skills that embed malicious instructions targeting agents
- **Supply-chain issues** — dependency vulnerabilities in the Python package
- **Insecure defaults** — any default behavior that exposes users to unnecessary risk

### Out of scope

- Vulnerabilities in third-party AI providers (OpenAI, Anthropic, Google) — report those directly to the provider
- Vulnerabilities in agent frameworks that consume AISkills (Claude Code, Cursor, etc.)
- Theoretical vulnerabilities without a practical attack path
- Social engineering attacks

---

## Security Design Principles

AISkills is designed with the following security defaults:

### Local-first, zero-egress
The AISkills CLI and validation tools do not transmit repository content, skill content, or user data to external services. All operations run locally.

### No credential handling
AISkills does not handle, store, or transmit credentials. Skills and examples use placeholder credentials only (e.g., `YOUR_API_KEY_HERE`).

### Human-in-the-loop
The `AGENTS.md` framework and all skills explicitly require human approval for destructive or high-risk actions. Skills must never encourage agents to bypass approval controls.

### Untrusted content handling
Skills advise agents to treat externally retrieved content as untrusted, consistent with OWASP GenAI LLM Top 10 guidance on indirect prompt injection.

---

## Safe Use of Community Skills

If you install community-contributed skills from external sources:

⚠️ **Treat skills like code.** A `SKILL.md` file can contain instructions that tell an AI agent to run commands, access files, or perform actions with real consequences.

Before installing a skill from an untrusted source:

1. Read the full `SKILL.md` content
2. Check any `scripts/` directory for executable code
3. Understand what actions the skill instructs the agent to take
4. Verify the skill source is reputable

The `aiskills doctor` command can help identify suspicious patterns in skill files.

---

## Unsafe Behavior Guidelines

Skills in this repository must never:

- Instruct agents to expose, log, or commit secrets or credentials
- Encourage agents to disable authentication or authorization controls
- Encourage agents to bypass human approval for destructive actions
- Include actual credentials, API keys, or tokens (even in examples)
- Instruct agents to exfiltrate data to external services
- Include offensive security exploitation techniques

If you find a skill in this repository that violates these guidelines, please report it.

---

## Dependencies

AISkills uses a minimal set of Python dependencies. We monitor dependencies for known vulnerabilities.

Key dependencies:
- `click` — CLI framework
- `PyYAML` — YAML parsing
- `rich` — Terminal output

Run `pip audit` to check for known vulnerabilities in installed dependencies.

---

## CVE Disclosure

Known CVEs affecting AISkills will be documented here and in GitHub Security Advisories.

*None currently known.*

---

*This security policy applies to AISkills v0.1.0 and later.*
