from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = {
    "linear-project-governance": {
        "required": [
            "SKILL.md",
            "references/standard.md",
            "templates/issues.md",
            "examples/examples.md",
        ],
        "must_contain": [
            "explicit user instruction",
            "Read back",
            "must not independently approve",
        ],
    },
    "linear-delivery-audit": {
        "required": [
            "SKILL.md",
            "references/audit-standard.md",
            "templates/audit-report.md",
            "examples/examples.md",
        ],
        "must_contain": [
            "Operate read-only by default",
            "Do not automatically modify formal requirements",
            "GitHub",
        ],
    },
}

PROHIBITED = [
    "Infinite Canvas",
    "TAI-",
    "Superpowers",
    "OpenSpec",
    "workflow-backups",
]


def fail(message: str) -> None:
    print(f"[FAIL] {message}")
    raise SystemExit(1)


def validate_frontmatter(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        fail(f"missing YAML frontmatter: {path.relative_to(ROOT)}")
    header = match.group(1)
    if "name:" not in header or "description:" not in header:
        fail(f"frontmatter requires name and description: {path.relative_to(ROOT)}")


def main() -> int:
    for name, config in SKILLS.items():
        skill_dir = ROOT / "skills" / name
        if not skill_dir.is_dir():
            fail(f"missing skill directory: {skill_dir.relative_to(ROOT)}")

        for relative in config["required"]:
            path = skill_dir / relative
            if not path.is_file():
                fail(f"missing required file: {path.relative_to(ROOT)}")

        skill_md = skill_dir / "SKILL.md"
        validate_frontmatter(skill_md)
        text = skill_md.read_text(encoding="utf-8")
        for phrase in config["must_contain"]:
            if phrase not in text:
                fail(f"missing guardrail '{phrase}' in {skill_md.relative_to(ROOT)}")

        for path in skill_dir.rglob("*"):
            if not path.is_file():
                continue
            contents = path.read_text(encoding="utf-8")
            for term in PROHIBITED:
                if term in contents:
                    fail(f"project-specific or legacy term '{term}' in {path.relative_to(ROOT)}")

    monthly = (ROOT / "automation" / "monthly-audit.md").read_text(encoding="utf-8")
    if "linear-delivery-audit" not in monthly:
        fail("monthly automation must invoke linear-delivery-audit")
    if "linear-project-governance" in monthly:
        fail("monthly automation must not invoke the write-oriented governance Skill")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for required in ("linear-project-governance", "linear-delivery-audit", "scripts/build_skill_archives.py"):
        if required not in readme:
            fail(f"README missing required reference: {required}")

    print("[OK] Skill structure, self-containment and safety boundaries validated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
