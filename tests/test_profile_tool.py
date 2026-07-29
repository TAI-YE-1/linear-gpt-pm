from __future__ import annotations

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
        document = profile_tool.template_document()
        document["profile_id"] = "demo-profile"
        profile = document["profile"]
        profile["identity"] = {
            "project_key": "demo",
            "project_name": "Demo",
            "timezone": "Asia/Shanghai",
            "accountable_owner": "owner",
        }
        structure = profile["linear_structure"]
        structure.update(
            {
                "team_or_workspace": "team",
                "structure_mode": "single-project",
                "governance_project": "project",
                "delivery_project": "project",
                "governance_type_label_mapping": {"REQ": "REQ"},
                "execution_type_label_mapping": {"Implementation": "Implementation"},
                "status_mapping": {"Done": "Done"},
                "authoritative_governance_document": "doc-1",
            }
        )
        profile["report_and_write_authority"].update(
            {
                "destination_audience": "project-team",
                "destination_data_classification": "internal",
            }
        )
        profile["data_flow_policy"].update(
            {
                "source_classifications": {"Linear": "internal"},
                "allowed_source_to_destination_flows": ["internal-to-internal"],
                "allowed_linked_domains_or_evidence_systems": ["linear"],
            }
        )
        profile["collection"].update(
            {
                "expected_item_count_source": "project-count",
                "pagination_or_cursor_strategy": "all-cursors",
                "required_comment_document_relation_access": "required",
            }
        )
        profile["audit_policy"]["approved_operational_maintenance_marker"] = "maintenance"
        profile["prior_report_comparison"]["lookup_location"] = "project-documents"
        return document

    def test_canonical_hash_ignores_key_order(self) -> None:
        first = {"b": 2, "a": {"y": 2, "x": 1}}
        second = {"a": {"x": 1, "y": 2}, "b": 2}
        self.assertEqual(profile_tool.profile_sha256(first), profile_tool.profile_sha256(second))

    def test_previous_calendar_month(self) -> None:
        document = self.completed_document()
        result = profile_tool.resolve_period(document, now=datetime.fromisoformat("2026-03-15T12:00:00+08:00"))
        self.assertEqual(result["start_inclusive"], "2026-02-01T00:00:00+08:00")
        self.assertEqual(result["end_exclusive"], "2026-03-01T00:00:00+08:00")

    def test_sealed_profile_validates(self) -> None:
        document = self.completed_document()
        document["approval"] = {
            "approved_by": "owner",
            "approved_at": "2026-07-01T00:00:00Z",
            "approval_record": "approval-1",
            "allowed_editors": ["owner"],
            "maximum_profile_age_days": 90,
            "approved_profile_body_sha256": profile_tool.profile_sha256(document["profile"]),
        }
        errors = profile_tool.validate_document(document, now=datetime.fromisoformat("2026-07-29T00:00:00+00:00"))
        self.assertEqual(errors, [])

    def test_cli_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "profile.json"
            profile_tool.write_document(path, self.completed_document())
            loaded = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(loaded["profile_schema_version"], 4)


if __name__ == "__main__":
    unittest.main()
