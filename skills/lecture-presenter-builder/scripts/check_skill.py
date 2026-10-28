#!/usr/bin/env python3
"""Lightweight structural checks for lecture-presenter-builder."""
from pathlib import Path
import re
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
errors = []

skill = root / "SKILL.md"
if not skill.is_file():
    errors.append("Missing SKILL.md")
else:
    text = skill.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\nname: lecture-presenter-builder\n" not in text:
        errors.append("SKILL.md front matter/name is missing or malformed")
    for required in ["PRESENTER ONLY", "SHOW THE AUDIENCE", "Quality gate", "source-workflow.md", "presenter-template.md"]:
        if required not in text:
            errors.append(f"SKILL.md missing required text: {required}")

for rel in ["README.md", "TESTING.md", "references/presenter-template.md", "references/source-workflow.md", "references/methods.md"]:
    if not (root / rel).is_file():
        errors.append(f"Missing required file: {rel}")

cases = sorted(p for p in (root / "evals").iterdir() if p.is_dir()) if (root / "evals").is_dir() else []
if len(cases) < 5:
    errors.append(f"Expected at least 5 evaluation cases; found {len(cases)}")
for case in cases:
    if not (case / "prompt.md").is_file():
        errors.append(f"{case.name} missing prompt.md")
    grader_files = list((case / "graders").glob("*")) if (case / "graders").is_dir() else []
    if not any(p.is_file() for p in grader_files):
        errors.append(f"{case.name} missing at least one file under graders/")

if errors:
    print("FAIL")
    print("\n".join(f"- {e}" for e in errors))
    sys.exit(1)

print("PASS: front matter, required references, and all evaluation-case files exist.")
print(f"Cases found: {len(cases)}")
print("Note: this checks structure only; behavioural evaluation is separate.")
