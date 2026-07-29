from __future__ import annotations

import hashlib
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
SKILLS = ["linear-project-governance", "linear-delivery-audit"]
REQUIRED_IN_ARCHIVE = ["SKILL.md", "LICENSE.txt", "agents/openai.yaml"]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_archive(archive: Path, skill: str) -> None:
    with zipfile.ZipFile(archive) as handle:
        names = set(handle.namelist())
    for relative in REQUIRED_IN_ARCHIVE:
        expected = f"{skill}/{relative}"
        if expected not in names:
            raise SystemExit(f"archive missing required file: {expected}")
    unexpected_roots = {name.split("/", 1)[0] for name in names if name}
    if unexpected_roots != {skill}:
        raise SystemExit(f"archive contains unexpected roots: {sorted(unexpected_roots)}")


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

        archive_base = DIST / skill
        archive = Path(
            shutil.make_archive(
                str(archive_base),
                "zip",
                root_dir=source.parent,
                base_dir=source.name,
            )
        )
        validate_archive(archive, skill)
        sums.append(f"{sha256(archive)}  {archive.name}")
        print(f"[OK] {archive.relative_to(ROOT)}")

    sums_path.write_text("\n".join(sums) + "\n", encoding="utf-8")
    print("[OK] dist/SHA256SUMS.txt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
