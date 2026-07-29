from __future__ import annotations

import hashlib
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
SKILLS = ["linear-project-governance", "linear-delivery-audit"]
REQUIRED_IN_ARCHIVE = ["SKILL.md", "LICENSE.txt", "agents/openai.yaml"]
FIXED_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
REJECTED_NAMES = {".DS_Store", "Thumbs.db"}
REJECTED_SUFFIXES = {".tmp", ".pyc", ".swp", "~"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_files(source: Path) -> list[Path]:
    files: list[Path] = []
    for path in sorted(source.rglob("*"), key=lambda item: item.as_posix()):
        if not path.is_file():
            continue
        relative = path.relative_to(source)
        if any(part.startswith(".") for part in relative.parts):
            raise SystemExit(f"hidden file is not allowed in a Skill package: {path}")
        if "__pycache__" in relative.parts or path.name in REJECTED_NAMES:
            raise SystemExit(f"temporary file is not allowed in a Skill package: {path}")
        if any(path.name.endswith(suffix) for suffix in REJECTED_SUFFIXES):
            raise SystemExit(f"temporary file is not allowed in a Skill package: {path}")
        files.append(path)
    return files


def build_archive(source: Path, archive: Path, skill: str) -> None:
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as handle:
        for path in source_files(source):
            relative = path.relative_to(source).as_posix()
            info = zipfile.ZipInfo(f"{skill}/{relative}", FIXED_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            info.create_system = 3
            handle.writestr(info, path.read_bytes())


def validate_archive(archive: Path, source: Path, skill: str) -> None:
    expected_names = {f"{skill}/{path.relative_to(source).as_posix()}" for path in source_files(source)}
    with zipfile.ZipFile(archive) as handle:
        names = {name for name in handle.namelist() if name and not name.endswith("/")}
        roots = {name.split("/", 1)[0] for name in names}
        if roots != {skill}:
            raise SystemExit(f"archive contains unexpected roots: {sorted(roots)}")
        if names != expected_names:
            missing = sorted(expected_names - names)
            extra = sorted(names - expected_names)
            raise SystemExit(f"archive content mismatch for {skill}; missing={missing}, extra={extra}")
        for relative in REQUIRED_IN_ARCHIVE:
            expected = f"{skill}/{relative}"
            if expected not in names:
                raise SystemExit(f"archive missing required file: {expected}")


def main() -> int:
    DIST.mkdir(exist_ok=True)
    sums: list[str] = []

    for old_archive in DIST.glob("*.zip"):
        old_archive.unlink()
    sums_path = DIST / "SHA256SUMS.txt"
    if sums_path.exists():
        sums_path.unlink()

    for skill in SKILLS:
        source = ROOT / "skills" / skill
        if not source.is_dir():
            raise SystemExit(f"missing skill directory: {source}")
        for relative in REQUIRED_IN_ARCHIVE:
            required = source / relative
            if not required.is_file():
                raise SystemExit(f"missing distribution file: {required}")

        archive = DIST / f"{skill}.zip"
        build_archive(source, archive, skill)
        first_digest = sha256(archive)

        verification_archive = DIST / f".{skill}.reproducibility-check.zip"
        build_archive(source, verification_archive, skill)
        second_digest = sha256(verification_archive)
        verification_archive.unlink()
        if first_digest != second_digest:
            raise SystemExit(f"non-reproducible archive: {skill}")

        validate_archive(archive, source, skill)
        sums.append(f"{first_digest}  {archive.name}")
        print(f"[OK] {archive.relative_to(ROOT)}")

    sums_path.write_text("\n".join(sums) + "\n", encoding="utf-8")
    print("[OK] dist/SHA256SUMS.txt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
