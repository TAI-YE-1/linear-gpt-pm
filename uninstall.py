#!/usr/bin/env python3
"""Remove files installed by the Codex workflow package.

The command is dry-run by default. It removes only known skill directories,
known role files, and the marked AGENTS.md block.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil


START = "<!-- CODEX-SUPERPOWERS-OPENSPEC-V4:START -->"
END = "<!-- CODEX-SUPERPOWERS-OPENSPEC-V4:END -->"
SKILLS = [
    "openspec-superpowers-bridge",
    "codex-subagent-routing",
    "codex-delivery-guardrails",
    "sdd-no-commit-adapter",
]


def remove_marked_block(text: str) -> str:
    start = text.find(START)
    end = text.find(END)
    if start < 0 and end < 0:
        return text
    if start < 0 or end < 0 or end < start:
        raise RuntimeError("AGENTS.md workflow markers are malformed")
    end += len(END)
    prefix = text[:start].rstrip()
    suffix = text[end:].lstrip()
    pieces = [part for part in (prefix, suffix) if part]
    return "\n\n".join(pieces).rstrip() + ("\n" if pieces else "")


def backup_path(target: Path, backup_root: Path) -> Path:
    relative = Path(*target.parts[1:]) if target.is_absolute() else target
    backup = backup_root / relative
    backup.parent.mkdir(parents=True, exist_ok=True)
    if target.is_dir():
        shutil.copytree(target, backup, dirs_exist_ok=True)
    else:
        shutil.copy2(target, backup)
    return backup


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--home", type=Path)
    args = parser.parse_args()

    package = Path(__file__).resolve().parent
    home = (args.home or Path.home()).resolve()
    codex_home = home / ".codex"
    agents_home = home / ".agents"
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    backup_root = codex_home / "workflow-backups" / f"uninstall-{timestamp}"

    targets = [agents_home / "skills" / name for name in SKILLS]
    targets += [codex_home / "agents" / path.name for path in sorted((package / "roles").glob("*.toml"))]
    actions: list[dict] = []

    for target in targets:
        item = {"target": str(target), "exists": target.exists(), "operation": "remove"}
        if args.apply and target.exists():
            item["backup"] = str(backup_path(target, backup_root))
            if target.is_dir():
                shutil.rmtree(target)
            else:
                target.unlink()
        actions.append(item)

    agents_target = codex_home / "AGENTS.md"
    agents_item = {
        "target": str(agents_target),
        "exists": agents_target.exists(),
        "operation": "remove marked block",
    }
    if agents_target.exists():
        original = agents_target.read_text(encoding="utf-8")
        updated = remove_marked_block(original)
        if args.apply and updated != original:
            agents_item["backup"] = str(backup_path(agents_target, backup_root))
            if updated:
                agents_target.write_text(updated, encoding="utf-8")
            else:
                agents_target.unlink()
    actions.append(agents_item)

    print(json.dumps({
        "mode": "apply" if args.apply else "dry-run",
        "home": str(home),
        "backupRoot": str(backup_root) if args.apply else None,
        "actions": actions,
    }, ensure_ascii=False, indent=2))
    if not args.apply:
        print("\nDry-run only. Re-run with --apply to uninstall.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
