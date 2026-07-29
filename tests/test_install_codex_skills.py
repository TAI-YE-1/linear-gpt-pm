from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts/install_codex_skills.py"
SPEC = importlib.util.spec_from_file_location("install_codex_skills", MODULE_PATH)
assert SPEC and SPEC.loader
installer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(installer)


class InstallerTests(unittest.TestCase):
    def test_install_and_replace_with_backup(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            codex_home = Path(temporary) / ".codex"
            first = installer.install_skills(codex_home, replace=False, dry_run=False, source_ref="test-ref")
            self.assertEqual(first["installed"], list(installer.SKILLS))
            for skill in installer.SKILLS:
                self.assertTrue((codex_home / "skills" / skill / "SKILL.md").is_file())

            with self.assertRaises(ValueError):
                installer.install_skills(codex_home, replace=False, dry_run=False, source_ref="test-ref")

            second = installer.install_skills(codex_home, replace=True, dry_run=False, source_ref="test-ref-2")
            self.assertEqual(second["backed_up"], list(installer.SKILLS))
            manifest = json.loads((codex_home / "skills" / ".linear-gpt-pm-install.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["source_ref"], "test-ref-2")

    def test_dry_run_writes_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            codex_home = Path(temporary) / ".codex"
            result = installer.install_skills(codex_home, replace=False, dry_run=True, source_ref="dry")
            self.assertTrue(result["dry_run"])
            self.assertFalse(codex_home.exists())


if __name__ == "__main__":
    unittest.main()
