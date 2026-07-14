#!/usr/bin/env python3
"""Create Git tree snapshots and review packages without touching the real index.

This tool writes blob/tree objects to Git's object database through a temporary
GIT_INDEX_FILE. It does not create commits, refs, branches, or tags.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from typing import Any


class AdapterError(RuntimeError):
    pass


def run_git(
    repo: Path,
    args: list[str],
    *,
    env: dict[str, str] | None = None,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(
        ["git", *args],
        cwd=repo,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        errors="replace",
    )
    if check and proc.returncode != 0:
        rendered = " ".join(["git", *args])
        raise AdapterError(
            f"{rendered} failed with exit code {proc.returncode}\n"
            f"stdout:\n{proc.stdout}\n"
            f"stderr:\n{proc.stderr}"
        )
    return proc


def resolve_repo(cwd: Path) -> Path:
    probe = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        errors="replace",
    )
    if probe.returncode != 0:
        raise AdapterError(f"not a Git repository: {cwd}\n{probe.stderr}")
    return Path(probe.stdout.strip()).resolve()


def sha256_file(path: Path) -> str | None:
    if not path.exists():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def real_index_path(repo: Path) -> Path:
    raw = run_git(repo, ["rev-parse", "--git-path", "index"]).stdout.strip()
    path = Path(raw)
    if not path.is_absolute():
        path = repo / path
    return path.resolve()


def current_head(repo: Path) -> str | None:
    proc = run_git(repo, ["rev-parse", "--verify", "HEAD"], check=False)
    return proc.stdout.strip() if proc.returncode == 0 else None


def ensure_no_unmerged(repo: Path) -> None:
    proc = run_git(repo, ["diff", "--name-only", "--diff-filter=U"])
    names = [line for line in proc.stdout.splitlines() if line.strip()]
    if names:
        raise AdapterError(
            "cannot snapshot a repository with unmerged paths:\n"
            + "\n".join(f"- {name}" for name in names)
        )


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def snapshot(args: argparse.Namespace) -> int:
    repo = resolve_repo(Path(args.repo or os.getcwd()))
    ensure_no_unmerged(repo)

    index_path = real_index_path(repo)
    index_before = sha256_file(index_path)
    head_before = current_head(repo)

    fd, temp_name = tempfile.mkstemp(prefix="codex-sdd-index-")
    os.close(fd)
    temp_index = Path(temp_name)
    temp_index.unlink(missing_ok=True)

    env = os.environ.copy()
    env["GIT_INDEX_FILE"] = str(temp_index)

    try:
        if head_before:
            run_git(repo, ["read-tree", "HEAD"], env=env)
        else:
            run_git(repo, ["read-tree", "--empty"], env=env)

        run_git(repo, ["add", "-A", "--", "."], env=env)
        tree = run_git(repo, ["write-tree"], env=env).stdout.strip()
        run_git(repo, ["cat-file", "-e", f"{tree}^{{tree}}"])

        status = run_git(repo, ["status", "--short", "--untracked-files=all"]).stdout.splitlines()
        head_after = current_head(repo)
        index_after = sha256_file(index_path)

        if head_before != head_after:
            raise AdapterError(
                f"HEAD changed during snapshot: before={head_before}, after={head_after}"
            )
        if index_before != index_after:
            raise AdapterError(
                "the real Git index changed during snapshot; refusing to continue"
            )

        payload = {
            "version": 1,
            "kind": "codex-sdd-tree-snapshot",
            "label": args.label,
            "repositoryRoot": str(repo),
            "head": head_before,
            "tree": tree,
            "realIndexPath": str(index_path),
            "realIndexSha256": index_after,
            "status": status,
        }
        output = Path(args.output).resolve()
        write_json(output, payload)
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    finally:
        temp_index.unlink(missing_ok=True)


def load_snapshot(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise AdapterError(f"cannot read snapshot {path}: {exc}") from exc

    required = {"version", "kind", "repositoryRoot", "tree"}
    missing = sorted(required - payload.keys())
    if missing:
        raise AdapterError(f"snapshot {path} is missing keys: {', '.join(missing)}")
    if payload["kind"] != "codex-sdd-tree-snapshot":
        raise AdapterError(f"unsupported snapshot kind in {path}: {payload['kind']}")
    return payload


def review(args: argparse.Namespace) -> int:
    base_path = Path(args.base).resolve()
    head_path = Path(args.head).resolve()
    base = load_snapshot(base_path)
    head = load_snapshot(head_path)

    base_repo = Path(base["repositoryRoot"]).resolve()
    head_repo = Path(head["repositoryRoot"]).resolve()
    if base_repo != head_repo:
        raise AdapterError(
            f"snapshot repositories differ: {base_repo} != {head_repo}"
        )

    repo = resolve_repo(base_repo)
    base_tree = str(base["tree"])
    head_tree = str(head["tree"])
    run_git(repo, ["cat-file", "-e", f"{base_tree}^{{tree}}"])
    run_git(repo, ["cat-file", "-e", f"{head_tree}^{{tree}}"])

    stat = run_git(
        repo,
        ["diff", "--stat", "--find-renames", base_tree, head_tree],
    ).stdout.rstrip()
    names = run_git(
        repo,
        ["diff", "--name-status", "--find-renames", base_tree, head_tree],
    ).stdout.rstrip()
    diff = run_git(
        repo,
        ["diff", "--binary", "--find-renames", "-U10", base_tree, head_tree],
    ).stdout.rstrip()

    lines = [
        "# SDD no-commit review package",
        "",
        f"- Repository: `{repo}`",
        f"- Base snapshot: `{base_path}`",
        f"- Head snapshot: `{head_path}`",
        f"- Base tree: `{base_tree}`",
        f"- Head tree: `{head_tree}`",
        f"- Base HEAD: `{base.get('head')}`",
        f"- Head HEAD: `{head.get('head')}`",
        "",
        "## Changed files",
        "",
        names or "(no file changes)",
        "",
        "## Diff stat",
        "",
        stat or "(no changes)",
        "",
        "## Diff",
        "",
        "```diff",
        diff or "(no changes)",
        "```",
        "",
    ]

    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")

    result = {
        "version": 1,
        "kind": "codex-sdd-review-package",
        "repositoryRoot": str(repo),
        "baseTree": base_tree,
        "headTree": head_tree,
        "changed": base_tree != head_tree,
        "output": str(output),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create SDD task snapshots and review packages without commits."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    snapshot_parser = subparsers.add_parser("snapshot", help="write a tree snapshot")
    snapshot_parser.add_argument("--repo", help="repository path; defaults to cwd")
    snapshot_parser.add_argument("--label", required=True)
    snapshot_parser.add_argument("--output", required=True)
    snapshot_parser.set_defaults(func=snapshot)

    review_parser = subparsers.add_parser("review", help="write a review package")
    review_parser.add_argument("--base", required=True)
    review_parser.add_argument("--head", required=True)
    review_parser.add_argument("--output", required=True)
    review_parser.set_defaults(func=review)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return int(args.func(args))
    except AdapterError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
