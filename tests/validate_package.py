#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
import tomllib


REQUIRED_SKILLS = {
    "openspec-superpowers-bridge",
    "codex-subagent-routing",
    "codex-delivery-guardrails",
    "sdd-no-commit-adapter",
}
REQUIRED_ROLES = {
    "sp_readonly_researcher",
    "sp_mechanical_worker",
    "sp_implementation_worker",
    "sp_senior_implementation",
    "sp_task_reviewer",
    "sp_final_reviewer",
    "sp_architect",
}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def parse_frontmatter(path: Path) -> tuple[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, flags=re.DOTALL)
    if not match:
        raise ValueError("missing YAML frontmatter")
    block = match.group(1)
    values: dict[str, str] = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values.get("name", ""), values.get("description", "")


def validate(package: Path) -> dict:
    errors: list[str] = []
    warnings: list[str] = []

    block_path = package / "config" / "AGENTS.block.md"
    if not block_path.is_file():
        fail(errors, "missing config/AGENTS.block.md")
    else:
        block = block_path.read_bytes()
        if len(block) >= 8 * 1024:
            fail(errors, f"AGENTS block is {len(block)} bytes; must stay below 8 KiB")
        text = block.decode("utf-8")
        if text.count("CODEX-SUPERPOWERS-OPENSPEC-V4:START") != 1:
            fail(errors, "AGENTS start marker missing or duplicated")
        if text.count("CODEX-SUPERPOWERS-OPENSPEC-V4:END") != 1:
            fail(errors, "AGENTS end marker missing or duplicated")
        if "编程任务开始时" in text:
            fail(errors, "AGENTS block must not force every coding task through a workflow router")
        if "简单、明确、低风险" not in text:
            fail(errors, "AGENTS block must preserve a direct path for simple tasks")
        if re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text):
            fail(errors, "AGENTS block must not contain a hard-coded email address")
        if "Gmail connector" in text:
            fail(errors, "AGENTS block must not contain connector-specific notification rules")
        if "默认使用中文" in text:
            fail(errors, "AGENTS block must not hard-code a user language preference")

    discovered_skills: set[str] = set()
    for skill_dir in sorted((package / "skills").glob("*")):
        if not skill_dir.is_dir():
            continue
        skill_file = skill_dir / "SKILL.md"
        metadata = skill_dir / "agents" / "openai.yaml"
        if not skill_file.is_file():
            fail(errors, f"missing {skill_dir.name}/SKILL.md")
            continue
        try:
            name, description = parse_frontmatter(skill_file)
        except Exception as exc:
            fail(errors, f"{skill_file}: {exc}")
            continue
        discovered_skills.add(name)
        if name != skill_dir.name:
            fail(errors, f"{skill_file}: frontmatter name {name!r} != directory name")
        if not name or len(name) > 64:
            fail(errors, f"{skill_file}: invalid name length")
        if not description or len(description) > 1024:
            fail(errors, f"{skill_file}: invalid description length")
        if not metadata.is_file():
            fail(errors, f"missing {metadata}")
        else:
            meta_text = metadata.read_text(encoding="utf-8")
            if not re.search(r"allow_implicit_invocation:\s*false\b", meta_text):
                fail(errors, f"{metadata}: implicit invocation must be false")

    missing_skills = REQUIRED_SKILLS - discovered_skills
    extra_skills = discovered_skills - REQUIRED_SKILLS
    if missing_skills:
        fail(errors, f"missing required skills: {sorted(missing_skills)}")
    if extra_skills:
        warnings.append(f"extra skills: {sorted(extra_skills)}")

    role_names: set[str] = set()
    for role_path in sorted((package / "roles").glob("*.toml")):
        try:
            data = tomllib.loads(role_path.read_text(encoding="utf-8"))
        except Exception as exc:
            fail(errors, f"{role_path}: TOML parse failed: {exc}")
            continue
        for key in ("name", "description", "developer_instructions"):
            if not isinstance(data.get(key), str) or not data[key].strip():
                fail(errors, f"{role_path}: missing non-empty {key}")
        name = data.get("name", "")
        if isinstance(name, str):
            role_names.add(name)
            if not name.startswith("sp_"):
                fail(errors, f"{role_path}: role name must use sp_ prefix")
            if name in {"worker", "explorer", "default"}:
                fail(errors, f"{role_path}: role collides with built-in {name}")
        if "model" in data or "model_reasoning_effort" in data:
            fail(errors, f"{role_path}: model must be selected dynamically, not fixed in role")
        if "sandbox_mode" in data:
            warnings.append(
                f"{role_path}: sandbox_mode is not treated as the only safety boundary"
            )

    if role_names != REQUIRED_ROLES:
        fail(
            errors,
            f"role set mismatch: missing={sorted(REQUIRED_ROLES-role_names)}, "
            f"extra={sorted(role_names-REQUIRED_ROLES)}",
        )

    adapter = package / "skills" / "sdd-no-commit-adapter" / "scripts" / "sdd_adapter.py"
    if not adapter.is_file():
        fail(errors, "missing sdd_adapter.py")

    required_release_files = (
        "install.py",
        "uninstall.py",
        "Install-CodexWorkflow.ps1",
        "Uninstall-CodexWorkflow.ps1",
        "LICENSE",
        "NOTICE",
        "THIRD_PARTY_NOTICES.md",
        "CONTRIBUTING.md",
        "SECURITY.md",
        "CHANGELOG.md",
        ".gitignore",
    )
    for required in required_release_files:
        if not (package / required).is_file():
            fail(errors, f"missing {required}")

    license_path = package / "LICENSE"
    if license_path.is_file() and "Apache License" not in license_path.read_text(encoding="utf-8", errors="replace"):
        fail(errors, "LICENSE must contain the Apache License 2.0 text")

    gitignore_path = package / ".gitignore"
    if gitignore_path.is_file() and "tests/last-smoke-report.json" not in gitignore_path.read_text(encoding="utf-8"):
        fail(errors, ".gitignore must exclude tests/last-smoke-report.json")

    readme_path = package / "README.md"
    if readme_path.is_file() and "历史审计快照" not in readme_path.read_text(encoding="utf-8"):
        fail(errors, "README must label the full source audit as a historical snapshot")

    all_text = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in package.rglob("*")
        if path.is_file()
        and path.resolve() != Path(__file__).resolve()
        and path.suffix.lower() in {".md", ".toml", ".yaml", ".py", ".ps1"}
    )
    banned = [
        "[features]\nmulti_agent_v2 = true",
        "/mnt/data/codex-superpowers-openspec-v4-rc1",
        "/tmp/codex-workflow-smoke-",
    ]
    for pattern in banned:
        if pattern in all_text:
            fail(errors, f"banned static configuration found: {pattern!r}")

    if re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", all_text):
        fail(errors, "release text must not contain hard-coded email addresses")
    if re.search(r"[A-Za-z]:\\Users\\[^\\]+\\", all_text):
        fail(errors, "release text must not contain a user-specific Windows home path")

    return {
        "package": str(package),
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "skills": sorted(discovered_skills),
        "roles": sorted(role_names),
        "agentsBlockBytes": block_path.stat().st_size if block_path.exists() else None,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    report = validate(args.package.resolve())
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
