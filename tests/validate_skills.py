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
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
VERSION_RE = re.compile(r"Skill package version: `([^`]+)`")

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
        ],
        "must_contain": [
            "explicit user instruction",
            "Immediately before writing",
            "references/security-boundaries.md",
            "references/setup-blueprint.md",
            "references/ruleset-version.md",
            "templates/issues.md",
            "examples/examples.md",
            "must not independently approve",
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
        ],
        "must_contain": [
            "Operate read-only by default",
            "Do not automatically modify formal requirements",
            "references/security-boundaries.md",
            "references/monthly-automation.md",
            "references/pre-release-audit.md",
            "templates/project-profile.md",
            "templates/audit-report.md",
            "examples/examples.md",
            "stable exception ID",
            "collection completeness",
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


def run_official_validator(skill_dir: Path) -> None:
    validator = ROOT / "scripts" / "vendor" / "openai_quick_validate.py"
    result = subprocess.run(
        [sys.executable, str(validator), str(skill_dir)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        fail(
            f"OpenAI quick_validate failed for {skill_dir.relative_to(ROOT)}: "
            f"{result.stdout.strip()} {result.stderr.strip()}"
        )


def parse_frontmatter(path: Path, expected_name: str) -> None:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        fail(f"missing YAML frontmatter: {path.relative_to(ROOT)}")
    try:
        values = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        fail(f"invalid YAML frontmatter in {path.relative_to(ROOT)}: {exc}")
    if not isinstance(values, dict):
        fail(f"frontmatter must be a mapping: {path.relative_to(ROOT)}")
    if set(values) != {"name", "description"}:
        fail(f"frontmatter must contain exactly name and description: {path.relative_to(ROOT)}")
    if values["name"] != expected_name or not NAME_RE.fullmatch(values["name"]):
        fail(f"frontmatter name must match the hyphen-case directory: {path.relative_to(ROOT)}")
    if len(values["name"]) > 64:
        fail(f"Skill name exceeds 64 characters: {values['name']}")
    if not isinstance(values["description"], str) or not 20 <= len(values["description"]) <= 1024:
        fail(f"description length out of range: {path.relative_to(ROOT)}")


def validate_agent_metadata(path: Path, skill_name: str) -> None:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        fail(f"invalid agents/openai.yaml in {path.relative_to(ROOT)}: {exc}")
    if not isinstance(data, dict):
        fail(f"agents/openai.yaml must be a mapping: {path.relative_to(ROOT)}")
    unexpected = set(data) - ALLOWED_AGENT_TOP_LEVEL
    if unexpected:
        fail(f"unsupported agents/openai.yaml keys in {path.relative_to(ROOT)}: {sorted(unexpected)}")
    interface = data.get("interface")
    if not isinstance(interface, dict):
        fail(f"agents/openai.yaml requires interface: {path.relative_to(ROOT)}")
    required = {"display_name", "short_description", "default_prompt"}
    if not required.issubset(interface):
        fail(f"agents/openai.yaml missing interface fields: {path.relative_to(ROOT)}")
    if not str(interface["display_name"]).strip():
        fail(f"empty display_name: {path.relative_to(ROOT)}")
    short_description = str(interface["short_description"])
    if not 25 <= len(short_description) <= 64:
        fail(f"short_description must be 25-64 characters: {path.relative_to(ROOT)}")
    if f"${skill_name}" not in str(interface["default_prompt"]):
        fail(f"default_prompt must mention ${skill_name}: {path.relative_to(ROOT)}")
    if "dependencies" in data and not isinstance(data["dependencies"], dict):
        fail(f"dependencies must be a mapping: {path.relative_to(ROOT)}")


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
    required_sections = [
        "TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION",
        "1. Definitions.",
        "9. Accepting Warranty or Additional Liability.",
        "END OF TERMS AND CONDITIONS",
    ]
    if len(root_license) < 10_000:
        fail("root LICENSE is not the complete Apache-2.0 text")
    for section in required_sections:
        if section not in root_license:
            fail(f"root LICENSE missing section: {section}")
    return root_license


def validate_archive(skill: str, root_license: str) -> None:
    archive = DIST / f"{skill}.zip"
    if not archive.is_file():
        fail(f"missing built archive: {archive.relative_to(ROOT)}")
    source = ROOT / "skills" / skill
    expected = {
        f"{skill}/{path.relative_to(source).as_posix()}"
        for path in source.rglob("*")
        if path.is_file()
    }
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
        if not line.strip():
            continue
        try:
            digest, filename = line.split("  ", 1)
        except ValueError:
            fail(f"invalid checksum line: {line}")
        recorded[filename] = digest
    expected_names = {f"{skill}.zip" for skill in SKILLS}
    if set(recorded) != expected_names:
        fail(f"checksum file names mismatch: {sorted(recorded)}")
    for filename, digest in recorded.items():
        if sha256(DIST / filename) != digest:
            fail(f"checksum mismatch: {filename}")


def skill_package_version(skill_dir: Path) -> str:
    text = (skill_dir / "references" / "ruleset-version.md").read_text(encoding="utf-8")
    match = VERSION_RE.search(text)
    if not match:
        fail(f"missing Skill package version: {skill_dir.name}")
    return match.group(1)


def main() -> int:
    root_license = validate_licenses()
    package_versions: set[str] = set()

    for name, config in SKILLS.items():
        skill_dir = ROOT / "skills" / name
        if not skill_dir.is_dir():
            fail(f"missing skill directory: {skill_dir.relative_to(ROOT)}")
        for relative in config["required"]:
            path = skill_dir / relative
            if not path.is_file():
                fail(f"missing required file: {path.relative_to(ROOT)}")

        run_official_validator(skill_dir)
        parse_frontmatter(skill_dir / "SKILL.md", name)
        text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        for phrase in config["must_contain"]:
            if phrase not in text:
                fail(f"missing guardrail '{phrase}' in {name}/SKILL.md")

        validate_agent_metadata(skill_dir / "agents" / "openai.yaml", name)
        validate_resource_navigation(skill_dir)
        package_versions.add(skill_package_version(skill_dir))

        if (skill_dir / "LICENSE.txt").read_text(encoding="utf-8") != root_license:
            fail(f"Skill LICENSE.txt differs from root LICENSE: {name}")

        for path in skill_dir.rglob("*"):
            if not path.is_file() or path.name == "LICENSE.txt":
                continue
            contents = path.read_text(encoding="utf-8")
            for term in PROHIBITED:
                if term in contents:
                    fail(f"project-specific or legacy term '{term}' in {path.relative_to(ROOT)}")

        validate_archive(name, root_license)

    if len(package_versions) != 1:
        fail(f"Skill package versions do not match: {sorted(package_versions)}")

    if (ROOT / "automation").exists():
        fail("root automation directory creates a second runtime source; keep templates inside the audit Skill")

    audit_standard = (ROOT / "skills/linear-delivery-audit/references/audit-standard.md").read_text(encoding="utf-8")
    for required in ("COL-001", "SEC-001", "stable exception ID", "100.0%", "95.0%"):
        if required not in audit_standard:
            fail(f"audit standard missing deterministic boundary: {required}")

    report = (ROOT / "skills/linear-delivery-audit/templates/audit-report.md").read_text(encoding="utf-8")
    for required in ("Collection completeness", "Ruleset", "Candidate-resolved", "Suspected prompt injection"):
        if required not in report:
            fail(f"audit report missing field: {required}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for required in (
        "$linear-project-governance",
        "$linear-delivery-audit",
        "references/monthly-automation.md",
        "0.1.0-alpha.1",
    ):
        if required not in readme:
            fail(f"README missing required reference: {required}")

    workflow = (ROOT / ".github/workflows/validate-skills.yml").read_text(encoding="utf-8")
    for required in ("actions/upload-artifact@", "dist/*.zip", "requirements-dev.txt"):
        if required not in workflow:
            fail(f"validation workflow missing distribution step: {required}")

    validate_checksums()
    print("[OK] Official and repository-specific Skill source and distribution validation passed.")
    print("[INFO] Runtime installation, connector access, data-flow authorization, and scheduled execution require separate smoke evidence.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
