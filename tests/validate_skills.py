from __future__ import annotations

import hashlib
import re
import subprocess
import sys
import zipfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
CURRENT_VERSION = "0.1.0-alpha.3"
PROFILE_SCHEMA_VERSION = "4"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
VERSION_RE = re.compile(r"Skill package version: `([^`]+)`")
PINNED_INSTALL_RE = re.compile(r"linear-gpt-pm/tree/([0-9a-f]{40})/skills/")
TEXT_SUFFIXES = {".md", ".py", ".yaml", ".yml", ".json", ".txt"}

SKILLS = {
    "linear-project-governance": {
        "required": [
            "SKILL.md",
            "LICENSE.txt",
            "agents/openai.yaml",
            "references/standard.md",
            "references/setup-blueprint.md",
            "references/security-boundaries.md",
            "references/ruleset-version.md",
            "templates/issues.md",
            "examples/examples.md",
            "scripts/plan_tool.py",
        ],
        "must_contain": [
            "Analyze only",
            "Propose a write",
            "Execute a confirmed write",
            "scripts/plan_tool.py",
            "PLAN-<first 10 uppercase SHA-256 characters>",
            "do not require the user to retype",
            "Concurrent change",
            "untrusted data",
        ],
    },
    "linear-delivery-audit": {
        "required": [
            "SKILL.md",
            "LICENSE.txt",
            "agents/openai.yaml",
            "references/audit-standard.md",
            "references/security-boundaries.md",
            "references/ruleset-version.md",
            "references/monthly-automation.md",
            "references/pre-release-audit.md",
            "templates/audit-report.md",
            "templates/project-profile.md",
            "examples/examples.md",
            "scripts/profile_tool.py",
        ],
        "must_contain": [
            "Level 1 — quick read-only audit",
            "Level 2 — repeatable manual audit",
            "Level 3 — scheduled or write-enabled audit",
            "Profile Schema v4",
            "scripts/profile_tool.py",
            "Operate read-only by default",
            "untrusted data",
            "Audit confidence",
        ],
    },
}

PROHIBITED = ["Infinite Canvas", "TAI-", "Superpowers", "OpenSpec", "workflow-backups"]
ALLOWED_AGENT_TOP_LEVEL = {"interface", "dependencies"}


def fail(message: str) -> None:
    print(f"[FAIL] {message}")
    raise SystemExit(1)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_lf(path: Path) -> None:
    if b"\r\n" in path.read_bytes():
        fail(f"text file must use LF line endings: {path.relative_to(ROOT)}")


def run_command(command: list[str]) -> None:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        fail(f"command failed: {' '.join(command)}\n{result.stdout}\n{result.stderr}")


def run_official_validator(skill_dir: Path) -> None:
    run_command([sys.executable, str(ROOT / "scripts/vendor/openai_quick_validate.py"), str(skill_dir)])


def parse_frontmatter(path: Path, expected_name: str) -> None:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        fail(f"missing YAML frontmatter: {path.relative_to(ROOT)}")
    values = yaml.safe_load(match.group(1))
    if not isinstance(values, dict) or set(values) != {"name", "description"}:
        fail(f"frontmatter must contain exactly name and description: {path.relative_to(ROOT)}")
    if values["name"] != expected_name or not NAME_RE.fullmatch(values["name"]):
        fail(f"frontmatter name must match directory: {path.relative_to(ROOT)}")
    if len(values["name"]) > 64:
        fail(f"Skill name exceeds 64 characters: {values['name']}")
    if not isinstance(values["description"], str) or not 20 <= len(values["description"]) <= 1024:
        fail(f"description length out of range: {path.relative_to(ROOT)}")


def validate_agent_metadata(path: Path, skill_name: str) -> None:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or set(data) - ALLOWED_AGENT_TOP_LEVEL:
        fail(f"invalid agents/openai.yaml top-level structure: {path.relative_to(ROOT)}")
    interface = data.get("interface")
    required = {"display_name", "short_description", "default_prompt"}
    if not isinstance(interface, dict) or not required.issubset(interface):
        fail(f"agents/openai.yaml missing interface fields: {path.relative_to(ROOT)}")
    if not 25 <= len(str(interface["short_description"])) <= 64:
        fail(f"short_description must be 25-64 characters: {path.relative_to(ROOT)}")
    if f"${skill_name}" not in str(interface["default_prompt"]):
        fail(f"default_prompt must mention ${skill_name}: {path.relative_to(ROOT)}")


def runtime_markdown(skill_dir: Path) -> list[Path]:
    files: list[Path] = []
    for folder in ("references", "templates", "examples"):
        root = skill_dir / folder
        if root.exists():
            files.extend(sorted(root.rglob("*.md")))
    return files


def validate_resource_navigation(skill_dir: Path) -> None:
    skill_md = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    for path in runtime_markdown(skill_dir):
        relative = path.relative_to(skill_dir).as_posix()
        if relative not in skill_md:
            fail(f"runtime resource is not directly routed from SKILL.md: {skill_dir.name}/{relative}")


def validate_licenses() -> str:
    root_license = (ROOT / "LICENSE").read_text(encoding="utf-8")
    for phrase in (
        "TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION",
        "1. Definitions.",
        "9. Accepting Warranty or Additional Liability.",
        "END OF TERMS AND CONDITIONS",
    ):
        if phrase not in root_license:
            fail(f"root LICENSE missing section: {phrase}")
    if len(root_license) < 10_000:
        fail("root LICENSE is not the complete Apache-2.0 text")
    return root_license


def validate_archive(skill: str, root_license: str) -> None:
    archive = DIST / f"{skill}.zip"
    source = ROOT / "skills" / skill
    expected = {f"{skill}/{path.relative_to(source).as_posix()}" for path in source.rglob("*") if path.is_file()}
    if not archive.is_file():
        fail(f"missing built archive: {archive.relative_to(ROOT)}")
    with zipfile.ZipFile(archive) as handle:
        names = {name for name in handle.namelist() if name and not name.endswith("/")}
        if names != expected:
            fail(f"archive content differs from source for {skill}")
        if handle.read(f"{skill}/LICENSE.txt").decode("utf-8") != root_license:
            fail(f"archive license differs from root LICENSE: {archive.name}")


def validate_checksums() -> None:
    sums_path = DIST / "SHA256SUMS.txt"
    if not sums_path.is_file():
        fail("missing dist/SHA256SUMS.txt")
    recorded: dict[str, str] = {}
    for line in sums_path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            digest, filename = line.split("  ", 1)
            recorded[filename] = digest
    expected = {f"{skill}.zip" for skill in SKILLS}
    if set(recorded) != expected:
        fail(f"checksum file names mismatch: {sorted(recorded)}")
    for filename, digest in recorded.items():
        if sha256(DIST / filename) != digest:
            fail(f"checksum mismatch: {filename}")


def skill_package_version(skill_dir: Path) -> str:
    text = (skill_dir / "references/ruleset-version.md").read_text(encoding="utf-8")
    match = VERSION_RE.search(text)
    if not match:
        fail(f"missing Skill package version: {skill_dir.name}")
    return match.group(1)


def validate_product_tools() -> None:
    required = (
        ROOT / "scripts/install_codex_skills.py",
        ROOT / "skills/linear-project-governance/scripts/plan_tool.py",
        ROOT / "skills/linear-delivery-audit/scripts/profile_tool.py",
    )
    for path in required:
        if not path.is_file():
            fail(f"missing product tool: {path.relative_to(ROOT)}")
        require_lf(path)
    run_command([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"])


def validate_repository_controls() -> None:
    attributes = (ROOT / ".gitattributes").read_text(encoding="utf-8")
    if "* text=auto eol=lf" not in attributes or "*.zip binary" not in attributes:
        fail(".gitattributes must enforce LF text and binary ZIP files")
    if (ROOT / "requirements-dev.txt").read_text(encoding="utf-8").strip() != "PyYAML==6.0.2":
        fail("requirements-dev.txt must pin PyYAML==6.0.2")
    build = (ROOT / "scripts/build_skill_archives.py").read_text(encoding="utf-8")
    for phrase in ("ZIP_STORED", "text file must use LF line endings", "FIXED_TIMESTAMP"):
        if phrase not in build:
            fail(f"archive builder missing deterministic control: {phrase}")
    workflow = (ROOT / ".github/workflows/validate-skills.yml").read_text(encoding="utf-8")
    for phrase in (
        'python-version: "3.11.9"',
        "cancel-in-progress: true",
        "Run productization unit tests",
        "Exercise tool help paths",
        "actions/upload-artifact@",
    ):
        if phrase not in workflow:
            fail(f"validation workflow missing control: {phrase}")


def main() -> int:
    root_license = validate_licenses()
    validate_repository_controls()
    validate_product_tools()
    package_versions: set[str] = set()

    for name, config in SKILLS.items():
        skill_dir = ROOT / "skills" / name
        for relative in config["required"]:
            if not (skill_dir / relative).is_file():
                fail(f"missing required file: {name}/{relative}")
        run_official_validator(skill_dir)
        parse_frontmatter(skill_dir / "SKILL.md", name)
        text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        for phrase in config["must_contain"]:
            if phrase not in text:
                fail(f"missing guardrail '{phrase}' in {name}/SKILL.md")
        validate_agent_metadata(skill_dir / "agents/openai.yaml", name)
        validate_resource_navigation(skill_dir)
        package_versions.add(skill_package_version(skill_dir))
        if (skill_dir / "LICENSE.txt").read_text(encoding="utf-8") != root_license:
            fail(f"Skill LICENSE.txt differs from root LICENSE: {name}")
        for path in skill_dir.rglob("*"):
            if not path.is_file() or path.name == "LICENSE.txt":
                continue
            if path.suffix.lower() in TEXT_SUFFIXES:
                require_lf(path)
            contents = path.read_text(encoding="utf-8")
            for term in PROHIBITED:
                if term in contents:
                    fail(f"project-specific or legacy term '{term}' in {path.relative_to(ROOT)}")
        validate_archive(name, root_license)

    if package_versions != {CURRENT_VERSION}:
        fail(f"Skill package versions must equal {CURRENT_VERSION}: {sorted(package_versions)}")

    profile_template = (ROOT / "skills/linear-delivery-audit/templates/project-profile.md").read_text(encoding="utf-8")
    for phrase in ("Profile Schema v4", "profile_tool.py init", "profile_tool.py seal", "Users should not calculate"):
        if phrase not in profile_template:
            fail(f"Profile template missing usability control: {phrase}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for phrase in (CURRENT_VERSION, "$linear-project-governance", "$linear-delivery-audit", "Basic use", "Advanced automation"):
        if phrase not in readme:
            fail(f"README missing usability reference: {phrase}")
    pinned_refs = PINNED_INSTALL_RE.findall(readme)
    if len(pinned_refs) < 2 or len(set(pinned_refs)) != 1:
        fail("README must install both Skills from one immutable 40-character commit")

    validate_checksums()
    print("[OK] Skill source, product tools, unit tests, and distributions validated.")
    print("[INFO] Real connector access and scheduled execution still require runtime smoke evidence.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
