from __future__ import annotations

import hashlib
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REFERENCE_RE = re.compile(r"(?:references|templates|examples)/[A-Za-z0-9._/-]+\.md")

SKILLS = {
    "linear-project-governance": {
        "required": [
            "SKILL.md",
            "LICENSE.txt",
            "agents/openai.yaml",
            "references/standard.md",
            "references/setup-blueprint.md",
            "templates/issues.md",
            "examples/examples.md",
        ],
        "must_contain": [
            "explicit user instruction",
            "Read back",
            "must not independently approve",
            "references/setup-blueprint.md",
        ],
    },
    "linear-delivery-audit": {
        "required": [
            "SKILL.md",
            "LICENSE.txt",
            "agents/openai.yaml",
            "references/audit-standard.md",
            "templates/audit-report.md",
            "templates/project-profile.md",
            "examples/examples.md",
        ],
        "must_contain": [
            "Operate read-only by default",
            "Do not automatically modify formal requirements",
            "GitHub",
            "templates/project-profile.md",
            "deterministic metric",
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


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_frontmatter(path: Path, expected_name: str) -> None:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        fail(f"missing YAML frontmatter: {path.relative_to(ROOT)}")

    values: dict[str, str] = {}
    for raw_line in match.group(1).splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if ":" not in line:
            fail(f"invalid frontmatter line in {path.relative_to(ROOT)}: {raw_line}")
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key in values:
            fail(f"duplicate frontmatter key '{key}' in {path.relative_to(ROOT)}")
        values[key] = value

    if set(values) != {"name", "description"}:
        fail(
            f"frontmatter must contain exactly name and description in "
            f"{path.relative_to(ROOT)}; found {sorted(values)}"
        )
    if values["name"] != expected_name:
        fail(f"frontmatter name must match directory: {path.relative_to(ROOT)}")
    if not NAME_RE.fullmatch(values["name"]):
        fail(f"invalid skill name: {values['name']}")
    if not 20 <= len(values["description"]) <= 1024:
        fail(f"description length out of range: {path.relative_to(ROOT)}")


def quoted_interface_value(text: str, key: str, path: Path) -> str:
    match = re.search(rf'^  {re.escape(key)}: "([^"]+)"$', text, re.M)
    if not match:
        fail(f"agents/openai.yaml requires quoted interface.{key}: {path.relative_to(ROOT)}")
    return match.group(1)


def validate_agent_metadata(path: Path, skill_name: str) -> None:
    text = path.read_text(encoding="utf-8")
    if "\t" in text:
        fail(f"tabs are not allowed in agents/openai.yaml: {path.relative_to(ROOT)}")

    top_level = [
        line.strip()
        for line in text.splitlines()
        if line.strip() and not line.startswith(" ")
    ]
    if top_level != ["interface:"]:
        fail(
            f"unsupported top-level agents/openai.yaml keys in {path.relative_to(ROOT)}: "
            f"{top_level}"
        )

    display_name = quoted_interface_value(text, "display_name", path)
    short_description = quoted_interface_value(text, "short_description", path)
    default_prompt = quoted_interface_value(text, "default_prompt", path)

    if not display_name.strip():
        fail(f"empty display_name: {path.relative_to(ROOT)}")
    if not 25 <= len(short_description) <= 64:
        fail(f"short_description must be 25-64 characters: {path.relative_to(ROOT)}")
    if f"${skill_name}" not in default_prompt:
        fail(f"default_prompt must mention ${skill_name}: {path.relative_to(ROOT)}")


def validate_references(skill_dir: Path) -> None:
    for path in skill_dir.rglob("*.md"):
        contents = path.read_text(encoding="utf-8")
        for reference in REFERENCE_RE.findall(contents):
            target = skill_dir / reference
            if not target.is_file():
                fail(
                    f"broken Skill-relative reference '{reference}' in "
                    f"{path.relative_to(ROOT)}"
                )


def validate_licenses() -> str:
    root_license_path = ROOT / "LICENSE"
    root_license = root_license_path.read_text(encoding="utf-8")
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

    with zipfile.ZipFile(archive) as handle:
        names = {name for name in handle.namelist() if name and not name.endswith("/")}
        roots = {name.split("/", 1)[0] for name in names}
        if roots != {skill}:
            fail(f"archive has unexpected roots for {skill}: {sorted(roots)}")
        for relative in SKILLS[skill]["required"]:
            expected = f"{skill}/{relative}"
            if expected not in names:
                fail(f"archive missing required file: {expected}")
        packed_license = handle.read(f"{skill}/LICENSE.txt").decode("utf-8")
        if packed_license != root_license:
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
        archive = DIST / filename
        if sha256(archive) != digest:
            fail(f"checksum mismatch: {filename}")


def main() -> int:
    root_license = validate_licenses()

    for name, config in SKILLS.items():
        skill_dir = ROOT / "skills" / name
        if not skill_dir.is_dir():
            fail(f"missing skill directory: {skill_dir.relative_to(ROOT)}")

        for relative in config["required"]:
            path = skill_dir / relative
            if not path.is_file():
                fail(f"missing required file: {path.relative_to(ROOT)}")

        skill_md = skill_dir / "SKILL.md"
        parse_frontmatter(skill_md, name)
        text = skill_md.read_text(encoding="utf-8")
        for phrase in config["must_contain"]:
            if phrase not in text:
                fail(f"missing guardrail '{phrase}' in {skill_md.relative_to(ROOT)}")

        validate_agent_metadata(skill_dir / "agents" / "openai.yaml", name)
        validate_references(skill_dir)

        skill_license = (skill_dir / "LICENSE.txt").read_text(encoding="utf-8")
        if skill_license != root_license:
            fail(f"Skill LICENSE.txt differs from root LICENSE: {name}")

        for path in skill_dir.rglob("*"):
            if not path.is_file() or path.name == "LICENSE.txt":
                continue
            contents = path.read_text(encoding="utf-8")
            for term in PROHIBITED:
                if term in contents:
                    fail(
                        f"project-specific or legacy term '{term}' in "
                        f"{path.relative_to(ROOT)}"
                    )

        validate_archive(name, root_license)

    monthly = (ROOT / "automation" / "monthly-audit.md").read_text(encoding="utf-8")
    monthly_required = [
        "linear-delivery-audit",
        "project-profile.md",
        "configuration error",
        "Do not guess or broaden scope",
        "<project-key>",
    ]
    for phrase in monthly_required:
        if phrase not in monthly:
            fail(f"monthly automation missing boundary: {phrase}")
    if "linear-project-governance" in monthly:
        fail("monthly automation must not invoke the write-oriented governance Skill")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for required in (
        "linear-project-governance",
        "linear-delivery-audit",
        "scripts/build_skill_archives.py",
        "templates/project-profile.md",
    ):
        if required not in readme:
            fail(f"README missing required reference: {required}")

    workflow = ROOT / ".github" / "workflows" / "validate-skills.yml"
    if not workflow.is_file():
        fail("missing validation workflow")

    validate_checksums()

    print(
        "[OK] Static Skill source, licenses, references, automation boundaries, "
        "archive layouts and checksums validated."
    )
    print("[INFO] Runtime installation, connector access and scheduled execution require separate smoke evidence.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
