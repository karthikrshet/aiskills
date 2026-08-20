"""Repository health checker for AISkills (aiskills doctor)."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

PLACEHOLDER_CONTEXT_PATTERNS = [
    re.compile(r"\[Your project name\]", re.IGNORECASE),
    re.compile(r"\[One paragraph", re.IGNORECASE),
    re.compile(r"\[e\.g\.,", re.IGNORECASE),
    re.compile(r"\[date\]", re.IGNORECASE),
]

SUSPICIOUS_SKILL_PATTERNS = [
    re.compile(r"ignore (all |previous )?instructions", re.IGNORECASE),
    re.compile(r"you are now", re.IGNORECASE),
    re.compile(r"system:\s*override", re.IGNORECASE),
    re.compile(r"exfiltrate", re.IGNORECASE),
    re.compile(r"send (your |the )?(system )?prompt", re.IGNORECASE),
    re.compile(r"disable (security|guardrails|authentication)", re.IGNORECASE),
]


@dataclass
class DoctorFinding:
    """A single finding from the doctor check."""

    level: str  # "OK", "WARNING", "ERROR"
    check: str
    message: str

    def __str__(self) -> str:
        tag = {"OK": "[OK]", "WARNING": "[WARN]", "ERROR": "[FAIL]"}.get(self.level, "    ")
        return f"{tag} {self.check}: {self.message}"


@dataclass
class DoctorReport:
    """Aggregated results from repository health checks."""

    findings: list[DoctorFinding] = field(default_factory=list)

    @property
    def has_errors(self) -> bool:
        return any(f.level == "ERROR" for f in self.findings)

    @property
    def has_warnings(self) -> bool:
        return any(f.level == "WARNING" for f in self.findings)

    def ok_count(self) -> int:
        return sum(1 for f in self.findings if f.level == "OK")

    def warning_count(self) -> int:
        return sum(1 for f in self.findings if f.level == "WARNING")

    def error_count(self) -> int:
        return sum(1 for f in self.findings if f.level == "ERROR")


def run_doctor(project_root: Path, skills_root: Path) -> DoctorReport:
    """Run all repository health checks and return a DoctorReport."""
    report = DoctorReport()

    _check_agents_md(project_root, report)
    _check_context_md(project_root, report)
    _check_skills_directory(skills_root, report)
    _check_skill_files_for_injection(skills_root, report)

    return report


def _check_agents_md(root: Path, report: DoctorReport) -> None:
    agents_md = root / "AGENTS.md"
    if agents_md.exists():
        report.findings.append(
            DoctorFinding("OK", "AGENTS.md", "Present — AI coding agents will read this file")
        )
    else:
        report.findings.append(
            DoctorFinding(
                "WARNING",
                "AGENTS.md",
                "Not found — run 'aiskills init' to create it. "
                "AI coding agents won't have project instructions.",
            )
        )


def _check_context_md(root: Path, report: DoctorReport) -> None:
    context_md = root / "CONTEXT.md"
    if not context_md.exists():
        report.findings.append(
            DoctorFinding(
                "WARNING",
                "CONTEXT.md",
                "Not found — run 'aiskills init' to create a template. "
                "Without it, agents lack project context.",
            )
        )
        return

    content = context_md.read_text(encoding="utf-8")

    # Check if it still contains placeholder text from the template
    has_placeholders = any(p.search(content) for p in PLACEHOLDER_CONTEXT_PATTERNS)
    if has_placeholders:
        report.findings.append(
            DoctorFinding(
                "WARNING",
                "CONTEXT.md",
                "Present but appears to still contain template placeholder text. "
                "Fill in your project details for best agent performance.",
            )
        )
    else:
        report.findings.append(
            DoctorFinding("OK", "CONTEXT.md", "Present and appears to be filled in")
        )


def _check_skills_directory(skills_root: Path, report: DoctorReport) -> None:
    if not skills_root.exists():
        report.findings.append(
            DoctorFinding(
                "ERROR",
                "Skills directory",
                f"Not found at '{skills_root}'. "
                "The skill registry cannot operate without a skills directory.",
            )
        )
        return

    skill_files = list(skills_root.rglob("SKILL.md"))
    count = len(skill_files)

    if count == 0:
        report.findings.append(
            DoctorFinding(
                "WARNING",
                "Skills directory",
                f"Found at '{skills_root}' but contains no SKILL.md files.",
            )
        )
    else:
        report.findings.append(
            DoctorFinding(
                "OK",
                "Skills directory",
                f"Found {count} skill(s) at '{skills_root}'",
            )
        )


def _check_skill_files_for_injection(skills_root: Path, report: DoctorReport) -> None:
    """Scan skill files for suspicious patterns that might indicate prompt injection."""
    if not skills_root.exists():
        return

    suspicious_files: list[str] = []

    for skill_md in skills_root.rglob("SKILL.md"):
        try:
            content = skill_md.read_text(encoding="utf-8")
            # Only check the body (after frontmatter), not the workflow description
            parts = content.split("---", 2)
            body = parts[2] if len(parts) >= 3 else content

            for pattern in SUSPICIOUS_SKILL_PATTERNS:
                if pattern.search(body):
                    suspicious_files.append(str(skill_md))
                    break
        except OSError:
            pass

    if suspicious_files:
        report.findings.append(
            DoctorFinding(
                "WARNING",
                "Skill content scan",
                f"The following skills contain patterns that may indicate prompt injection. "
                f"Review before use: {', '.join(suspicious_files[:3])}",
            )
        )
    else:
        report.findings.append(
            DoctorFinding(
                "OK",
                "Skill content scan",
                "No suspicious patterns detected in skill files",
            )
        )
