#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
import subprocess
import sys
import tempfile


def run(args: list[str], cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(
        args,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        errors="replace",
    )
    if check and proc.returncode != 0:
        raise RuntimeError(
            f"command failed: {args}\nstdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"
        )
    return proc


def sha(path: Path) -> str | None:
    if not path.exists():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def adapter_test(package: Path, work: Path) -> dict:
    work.mkdir(parents=True, exist_ok=True)
    repo = work / "repo"
    repo.mkdir()
    run(["git", "init"], repo)
    run(["git", "config", "user.email", "smoke@local"], repo)
    run(["git", "config", "user.name", "Smoke Test"], repo)
    (repo / "app.txt").write_text("line 1\n", encoding="utf-8")
    run(["git", "add", "app.txt"], repo)
    run(["git", "commit", "-m", "baseline"], repo)

    # User state that must be part of the baseline, not attributed to the task.
    (repo / "app.txt").write_text("line 1\nuser change\n", encoding="utf-8")
    (repo / "preexisting.txt").write_text("user file\n", encoding="utf-8")
    (repo / "staged.txt").write_text("staged before task\n", encoding="utf-8")
    run(["git", "add", "staged.txt"], repo)

    index_path_raw = run(["git", "rev-parse", "--git-path", "index"], repo).stdout.strip()
    index_path = Path(index_path_raw)
    if not index_path.is_absolute():
        index_path = repo / index_path
    index_before = sha(index_path)
    head_before = run(["git", "rev-parse", "HEAD"], repo).stdout.strip()

    adapter = package / "skills" / "sdd-no-commit-adapter" / "scripts" / "sdd_adapter.py"
    base = work / "base.json"
    head = work / "head.json"
    review = work / "review.md"

    run([sys.executable, str(adapter), "snapshot", "--repo", str(repo), "--label", "start", "--output", str(base)])
    (repo / "app.txt").write_text("line 1\nuser change\ntask change\n", encoding="utf-8")
    (repo / "task.txt").write_text("task file\n", encoding="utf-8")
    run([sys.executable, str(adapter), "snapshot", "--repo", str(repo), "--label", "end", "--output", str(head)])
    run([sys.executable, str(adapter), "review", "--base", str(base), "--head", str(head), "--output", str(review)])

    index_after = sha(index_path)
    head_after = run(["git", "rev-parse", "HEAD"], repo).stdout.strip()
    review_text = review.read_text(encoding="utf-8")

    assertions = {
        "realIndexUnchanged": index_before == index_after,
        "headUnchanged": head_before == head_after,
        "taskFileInReview": "task.txt" in review_text,
        "taskChangeInReview": "+task change" in review_text,
        "preexistingFileNotAttributed": "preexisting.txt" not in review_text,
        "stagedFileNotAttributed": "staged.txt" not in review_text,
        "noNewCommit": run(["git", "rev-list", "--count", "HEAD"], repo).stdout.strip() == "1",
    }
    return {
        "passed": all(assertions.values()),
        "assertions": assertions,
        "review": str(review),
    }


def installer_test(package: Path, work: Path) -> dict:
    work.mkdir(parents=True, exist_ok=True)
    home = work / "home"
    home.mkdir()
    codex = home / ".codex"
    codex.mkdir()
    original = "# Existing user rule\n\nKeep me.\n"
    (codex / "AGENTS.md").write_text(original, encoding="utf-8")

    install = run([sys.executable, str(package / "install.py"), "--apply", "--home", str(home)])
    agents_text = (codex / "AGENTS.md").read_text(encoding="utf-8")
    installed = {
        "existingTextPreserved": "Keep me." in agents_text,
        "markerInstalledOnce": agents_text.count("CODEX-SUPERPOWERS-OPENSPEC-V4:START") == 1,
        "noHardcodedRecipient": re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", agents_text) is None,
        "languageFollowsUserOrProject": "使用用户当前语言或项目明确约定的语言" in agents_text,
        "notificationsDefaultOff": "默认不发送完成邮件、消息或通知" in agents_text,
        "skillsInstalled": all((home / ".agents" / "skills" / name / "SKILL.md").is_file() for name in [
            "openspec-superpowers-bridge",
            "codex-subagent-routing",
            "codex-delivery-guardrails",
            "sdd-no-commit-adapter",
        ]),
        "rolesInstalled": (codex / "agents" / "sp_architect.toml").is_file(),
        "configUntouched": not (codex / "config.toml").exists(),
    }

    # Reinstall must replace the marked block rather than duplicate it.
    run([sys.executable, str(package / "install.py"), "--apply", "--home", str(home)])
    agents_text2 = (codex / "AGENTS.md").read_text(encoding="utf-8")
    installed["idempotentMarker"] = agents_text2.count("CODEX-SUPERPOWERS-OPENSPEC-V4:START") == 1
    install_backups = [
        path
        for path in (codex / "workflow-backups").iterdir()
        if path.is_dir() and not path.name.startswith("uninstall-")
    ]
    installed["relativeSkillBackup"] = any(
        (path / ".agents" / "skills" / "openspec-superpowers-bridge" / "SKILL.md").is_file()
        for path in install_backups
    )
    installed["relativeRoleBackup"] = any(
        (path / ".codex" / "agents" / "sp_architect.toml").is_file()
        for path in install_backups
    )

    run([sys.executable, str(package / "uninstall.py"), "--apply", "--home", str(home)])
    final_text = (codex / "AGENTS.md").read_text(encoding="utf-8")
    uninstalled = {
        "existingTextStillPreserved": "Keep me." in final_text,
        "markerRemoved": "CODEX-SUPERPOWERS-OPENSPEC-V4:START" not in final_text,
        "skillsRemoved": not (home / ".agents" / "skills" / "codex-subagent-routing").exists(),
        "rolesRemoved": not (codex / "agents" / "sp_architect.toml").exists(),
    }
    uninstall_backups = [
        path
        for path in (codex / "workflow-backups").iterdir()
        if path.is_dir() and path.name.startswith("uninstall-")
    ]
    uninstalled["relativeUninstallBackup"] = any(
        (path / ".agents" / "skills" / "codex-subagent-routing" / "SKILL.md").is_file()
        and (path / ".codex" / "agents" / "sp_architect.toml").is_file()
        for path in uninstall_backups
    )
    assertions = {**installed, **uninstalled}
    return {
        "passed": all(assertions.values()),
        "assertions": assertions,
        "installOutput": install.stdout,
    }


def main() -> int:
    package = Path(__file__).resolve().parents[1]
    static = run([sys.executable, str(package / "tests" / "validate_package.py"), "--package", str(package)])
    static_report = json.loads(static.stdout)

    with tempfile.TemporaryDirectory(prefix="codex-workflow-smoke-") as temp:
        work = Path(temp)
        adapter = adapter_test(package, work / "adapter")
        installer = installer_test(package, work / "installer")

    report = {
        "static": static_report,
        "adapter": adapter,
        "installer": installer,
    }
    report["passed"] = bool(static_report["valid"] and adapter["passed"] and installer["passed"])
    output = package / "tests" / "last-smoke-report.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
