from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ("linear-project-governance", "linear-delivery-audit")
VERSION_RE = re.compile(r"Skill package version: `([^`]+)`")


def package_version(skill_dir: Path) -> str:
    text = (skill_dir / "references" / "ruleset-version.md").read_text(encoding="utf-8")
    match = VERSION_RE.search(text)
    if not match:
        raise ValueError(f"cannot determine package version for {skill_dir.name}")
    return match.group(1)


def verify_source() -> str:
    versions = {package_version(ROOT / "skills" / skill) for skill in SKILLS}
    if len(versions) != 1:
        raise ValueError(f"Skill package versions differ: {sorted(versions)}")
    for skill in SKILLS:
        source = ROOT / "skills" / skill
        for relative in ("SKILL.md", "LICENSE.txt", "agents/openai.yaml"):
            if not (source / relative).is_file():
                raise ValueError(f"missing source file: {skill}/{relative}")
    return versions.pop()


def default_codex_home() -> Path:
    configured = os.environ.get("CODEX_HOME")
    return Path(configured).expanduser() if configured else Path.home() / ".codex"


def install_skills(
    codex_home: Path,
    *,
    replace: bool,
    dry_run: bool,
    source_ref: str,
) -> dict[str, object]:
    version = verify_source()
    skills_root = codex_home.expanduser().resolve() / "skills"
    backup_root = codex_home.expanduser().resolve() / "skills-backups" / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    existing = [skill for skill in SKILLS if (skills_root / skill).exists()]
    if existing and not replace:
        raise ValueError(
            "installed Skill directories already exist: "
            + ", ".join(existing)
            + "; rerun with --replace to create backups and upgrade"
        )

    actions = {
        "version": version,
        "source_ref": source_ref,
        "codex_home": str(codex_home),
        "installed": list(SKILLS),
        "backed_up": existing,
        "dry_run": dry_run,
    }
    if dry_run:
        return actions

    skills_root.mkdir(parents=True, exist_ok=True)
    if existing:
        backup_root.mkdir(parents=True, exist_ok=False)

    installed_now: list[Path] = []
    moved_backups: list[tuple[Path, Path]] = []
    try:
        for skill in SKILLS:
            source = ROOT / "skills" / skill
            destination = skills_root / skill
            if destination.exists():
                backup = backup_root / skill
                shutil.move(str(destination), str(backup))
                moved_backups.append((backup, destination))

            temp_parent = skills_root
            temp_dir = Path(tempfile.mkdtemp(prefix=f".{skill}.install-", dir=temp_parent))
            staged = temp_dir / skill
            shutil.copytree(source, staged)
            if destination.exists():
                raise ValueError(f"destination unexpectedly exists: {destination}")
            os.replace(staged, destination)
            temp_dir.rmdir()
            installed_now.append(destination)

        manifest = {
            "package_version": version,
            "source_ref": source_ref,
            "installed_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "skills": list(SKILLS),
            "backup_location": str(backup_root) if existing else None,
        }
        (skills_root / ".linear-gpt-pm-install.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    except Exception:
        for destination in installed_now:
            if destination.exists():
                shutil.rmtree(destination)
        for backup, destination in reversed(moved_backups):
            if backup.exists() and not destination.exists():
                shutil.move(str(backup), str(destination))
        raise

    return actions


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Install both Linear GPT PM Skills into Codex safely.")
    parser.add_argument("--codex-home", type=Path, default=default_codex_home())
    parser.add_argument("--replace", action="store_true", help="Back up and replace existing Skill directories.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--source-ref", default="local-checkout")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = install_skills(
            args.codex_home,
            replace=args.replace,
            dry_run=args.dry_run,
            source_ref=args.source_ref,
        )
    except (OSError, ValueError) as exc:
        print(f"[FAIL] {exc}", file=sys.stderr)
        return 1

    verb = "would install" if args.dry_run else "installed"
    print(f"[OK] {verb} {', '.join(SKILLS)}")
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    if not args.dry_run:
        print("Restart or refresh Codex Skill discovery before use.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
