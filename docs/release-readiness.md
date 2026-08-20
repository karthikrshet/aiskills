# Release Readiness

This checklist is the release gate for AISkills. It is evidence, not a promise: a release is approved only when every required item is verified and a maintainer gives written approval.

## Automated gate

- [ ] `python -m pytest tests/ -v --tb=short` passes on the supported Python versions.
- [ ] `python -m ruff check cli/ tests/` passes.
- [ ] `python -m ruff format --check cli/ tests/` passes.
- [ ] `python -m aiskills validate --skills-dir skills/` reports no errors or warnings.
- [ ] `python -m aiskills doctor --project-dir .` reports no warnings or errors.
- [ ] `pip-audit` reports no known vulnerabilities in the resolved release environment.
- [ ] CI is green for the release commit.

## Manual security gate

- [ ] GitHub private vulnerability reporting is enabled and the link in `SECURITY.md` works.
- [ ] Dependency updates and GitHub Action updates have been reviewed.
- [ ] New or changed third-party skills, prompts, and scripts have been manually reviewed as untrusted content.
- [ ] No credentials, private keys, or `.env` files are included in the release.
- [ ] The release notes accurately state all unmeasured metrics as **NOT MEASURED**.

## Release decision

| Field | Required value |
|---|---|
| Version | Semantic version to publish |
| Commit | Immutable commit SHA that passed CI |
| Approver | Named maintainer |
| Approval date | YYYY-MM-DD |
| Security exceptions | None, or explicit written risk acceptance |

Do not publish a release if any required item is unchecked or a security exception remains unresolved.
