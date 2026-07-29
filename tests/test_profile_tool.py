from __future__ import annotations

import argparse
import importlib.util
import json
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "skills/linear-delivery-audit/scripts/profile_tool.py"
SPEC = importlib.util.spec_from_file_location("profile_tool", MODULE_PATH)
assert SPEC and SPEC.loader
profile_tool = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(profile_tool)


class ProfileToolTests(unittest.TestCase):
    def completed_document(self) -> dict:
        args = argparse.Namespace(
            project_key="demo",
            project_name="Demo Project",
            timezone="Asia/Shanghai",
            owner="owner",
            team="team",
            structure_mode="single-project",
            project="project",
            governance_project=None,
            delivery_project=None,
        )
        return profile_tool.template_document(args)

    def seal_document(self, document: dict) -> dict:
        document["approval"] = {
            "approved_by": "owner",
            "approved_at": "2026-07-01T00:00:00Z",
            "approval_record": "approval-1",
            "allowed_editors": ["owner"],
            "maximum_profile_age_days": 90,
            "approved_profile_body_sha256": profile_tool.profile_sha256(document["profile"]),
        }
        return document

    def test_canonical_hash_ignores_key_order(self) -> None:
        first = {"b": 2, "a": {"y": 2, "x": 1}}
        second = {"a": {"x": 1, "y": 2}, "b": 2}
        self.assertEqual(profile_tool.profile_sha256(first), profile_tool.profile_sha256(second))

    def test_prefilled_profile_body_is_valid(self) -> None:
        self.assertEqual(profile_tool.validate_profile_body(self.completed_document()["profile"]), [])

    def test_previous_calendar_month(self) -> None:
        result = profile_tool.resolve_period(
            self.completed_document(),
            now=datetime.fromisoformat("2026-03-15T12:00:00+08:00"),
        )
        self.assertEqual(result["start_inclusive"], "2026-02-01T00:00:00+08:00")
        self.assertEqual(result["end_exclusive"], "2026-03-01T00:00:00+08:00")

    def test_sealed_profile_validates_and_tampering_fails(self) -> None:
        document = self.seal_document(self.completed_document())
        errors = profile_tool.validate_document(
            document,
            now=datetime.fromisoformat("2026-07-29T00:00:00+00:00"),
        )
        self.assertEqual(errors, [])
        document["profile"]["identity"]["project_name"] = "Tampered"
        self.assertIn(
            "approved Profile body SHA-256 does not match Profile content",
            profile_tool.validate_document(
                document,
                now=datetime.fromisoformat("2026-07-29T00:00:00+00:00"),
            ),
        )

    def test_expired_profile_fails(self) -> None:
        document = self.seal_document(self.completed_document())
        document["approval"]["maximum_profile_age_days"] = 1
        errors = profile_tool.validate_document(
            document,
            now=datetime.fromisoformat("2026-07-29T00:00:00+00:00"),
        )
        self.assertIn("Profile approval has expired", errors)

    def test_json_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "profile.json"
            profile_tool.write_document(path, self.completed_document())
            loaded = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(loaded["profile_schema_version"], 4)


if __name__ == "__main__":
    unittest.main()
