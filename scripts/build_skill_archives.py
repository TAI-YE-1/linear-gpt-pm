from __future__ import annotations

import hashlib
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
SKILLS = ["linear-project-governance", "linear-delivery-audit"]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    DIST.mkdir(exist_ok=True)
    sums: list[str] = []

    for skill in SKILLS:
        source = ROOT / "skills" / skill
        if not source.is_dir():
            raise SystemExit(f"missing skill directory: {source}")
        archive_base = DIST / skill
        archive = Path(shutil.make_archive(str(archive_base), "zip", root_dir=source.parent, base_dir=source.name))
        sums.append(f"{sha256(archive)}  {archive.name}")
        print(f"[OK] {archive.relative_to(ROOT)}")

    (DIST / "SHA256SUMS.txt").write_text("\n".join(sums) + "\n", encoding="utf-8")
    print("[OK] dist/SHA256SUMS.txt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
