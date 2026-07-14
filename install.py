#!/usr/bin/env python3
"""Safe installer for the Codex × Superpowers × OpenSpec workflow package."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import subprocess
import sys


START = "<!-- CODEX-SUPERPOWERS-OPENSPEC-V4:START -->"
END = "<!-- CODEX-SUPERPOWERS-OPENSPEC-V4:END -->"
SKILLS = [
    "openspec-superpowers-bridge",
    "codex-subagent-routing",
    "codex-delivery-guardrails",
    "sdd-no-commit-adapter",
]


def replace_marked_block(existing: str, block: str) -> str:
    start = existing.find(START)
    end = existing.find(END)
    if start >= 0 and end >= 0 and end >= start:
        end += len(END)
        prefix = existing[:start].rstrip()
        suffix = existing[end:].lstrip()
        pieces = [part for part in (prefix, block.strip(), suffix) if part]
        return "\n\n".join(pieces).rstrip() + "\n"
    if start >= 0 or end >= 0:
        raise RuntimeError("AGENTS.md contains only one workflow marker; repair it manually")
    if not existing.strip():
        return block.strip() + "\n"
    return existing.rstrip() + "\n\n" + block.strip() + "\n"


def backup_destination(target: Path, home: Path, backup_root: Path) -> Path:
    """Return a compact backup path rooted under the selected home directory."""
    try:
        relative = target.relative_to(home)
    except ValueError as exc:
        raise RuntimeError(f"refusing to back up path outside home: {target}") from exc
    return backup_root / relative


def copy_with_backup(
    source: Path,
    target: Path,
    home: Path,
    backup_root: Path,
    apply: bool,
) -> dict:
    item = {"source": str(source), "target": str(target), "exists": target.exists()}
    if not apply:
        return item

    if target.exists():
        backup = backup_destination(target, home, backup_root)
        backup.parent.mkdir(parents=True, exist_ok=True)
        if target.is_dir():
            shutil.copytree(target, backup, dirs_exist_ok=True)
            shutil.rmtree(target)
        else:
            shutil.copy2(target, backup)
        item["backup"] = str(backup)

    target.parent.mkdir(parents=True, exist_ok=True)
    if source.is_dir():
        shutil.copytree(source, target)
    else:
        shutil.copy2(source, target)
    return item


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="perform writes; default is dry-run")
    parser.add_argument("--home", type=Path, help="override home directory for testing")
    args = parser.parse_args()

    package = Path(__file__).resolve().parent
    home = (args.home or Path.home()).resolve()
    codex_home = home / ".codex"
    agents_home = home / ".agents"
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    backup_root = codex_home / "workflow-backups" / timestamp

    validator = package / "tests" / "validate_package.py"
    result = subprocess.run([sys.executable, str(validator), "--package", str(package)])
    if result.returncode != 0:
        return result.returncode

    actions: list[dict] = []
    for skill in SKILLS:
        actions.append(
            copy_with_backup(
                package / "skills" / skill,
                agents_home / "skills" / skill,
                home,
                backup_root,
                args.apply,
            )
        )

    for role in sorted((package / "roles").glob("*.toml")):
        actions.append(
            copy_with_backup(
                role,
                codex_home / "agents" / role.name,
                home,
                backup_root,
                args.apply,
            )
        )

    agents_target = codex_home / "AGENTS.md"
    existing = agents_target.read_text(encoding="utf-8") if agents_target.exists() else ""
    block = (package / "config" / "AGENTS.block.md").read_text(encoding="utf-8")
    merged = replace_marked_block(existing, block)
    agents_action = {
        "target": str(agents_target),
        "exists": agents_target.exists(),
        "operation": "replace marked block" if START in existing else "append marked block",
    }

    if args.apply:
        if agents_target.exists():
            backup = backup_root / ".codex" / "AGENTS.md"
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(agents_target, backup)
            agents_action["backup"] = str(backup)
        agents_target.parent.mkdir(parents=True, exist_ok=True)
        agents_target.write_text(merged, encoding="utf-8")

    actions.append(agents_action)
    payload = {
        "mode": "apply" if args.apply else "dry-run",
        "home": str(home),
        "backupRoot": str(backup_root) if args.apply else None,
        "actions": actions,
        "configTomlModified": False,
        "networkUsed": False,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    if not args.apply:
        print("\nDry-run only. Re-run with --apply to install.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
