# Security Review Workflow

This workflow provides a structured process for performing an AI security review before production deployment.

---

## When to Use

Run this workflow for any AI/LLM application, agent, or RAG system before production deployment.

---

## Workflow Stages

```
Stage 1: Scope Definition
    ↓
Stage 2: Traditional Code Security Review
    ↓
Stage 3: AI-Specific Security Review (OWASP GenAI LLM Top 10)
    ↓
Stage 4: Secret and Dependency Scan
    ↓
Stage 5: Produce Security Report
    ↓
[Security Gate]
    ↓
Stage 6: Remediation (if needed)
    ↓
Stage 7: Human Sign-off
```

---

## Stage Details

### Stage 1: Scope Definition

- What is being reviewed? (codebase, architecture, prompts, data)
- What is explicitly out of scope?
- What environments? (staging, production)

---

### Stage 2: Traditional Code Security (`code-review` — Security section)

- Input validation
- SQL/command injection
- Authentication/authorization
- Sensitive data in logs
- Hardcoded credentials

---

### Stage 3: AI Security Review (`ai-security-review`)

Cover all 10 OWASP GenAI LLM risks:

| Risk | Check |
|------|-------|
| LLM01: Prompt Injection | Direct and indirect injection vectors |
| LLM02: Sensitive Info Disclosure | System prompt, context, output |
| LLM03: Supply Chain | Third-party models, plugins |
| LLM04: Data Poisoning | Knowledge base integrity |
| LLM05: Improper Output Handling | LLM output in SQL, HTML, shell |
| LLM06: Excessive Agency | Agent tool permissions |
| LLM07: System Prompt Leakage | Extraction resistance |
| LLM08: Embedding Weaknesses | Retrieval manipulation |
| LLM09: Misinformation | Hallucination and citation |
| LLM10: Unbounded Consumption | Rate limits and cost controls |

---

### Stage 4: Secret and Dependency Scan

```bash
# Check for secrets
git grep -i "api_key\|api_secret\|password\|token" -- '*.py' '*.ts' '*.env*'

# Check dependencies for known CVEs
pip audit           # Python
npm audit           # Node.js
```

---

### Stage 5: Security Report (`templates/SECURITY.md`)

Document all findings with:
- Severity (Critical / High / Medium / Low)
- OWASP LLM reference
- Location
- Remediation

---

### Security Gate ✅

| Check | Required |
|-------|---------|
| All 10 OWASP LLM risks evaluated | ✅ |
| No unresolved Critical findings | ✅ |
| No unresolved High findings | ✅ |
| No hardcoded secrets | ✅ |
| No known CVEs in dependencies | ✅ |

---

### Stage 6: Remediation

Fix all Critical and High findings. Document Medium/Low acceptance.

---

### Stage 7: Human Sign-off

> ⚠️ **Security sign-off required from a human before production deployment.**

---

*Part of AISkills v0.1.0 — grounded in OWASP GenAI LLM Top 10 (2026): https://genai.owasp.org/*
