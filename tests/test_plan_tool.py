from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "skills/linear-project-governance/scripts/plan_tool.py"
SPEC = importlib.util.spec_from_file_location("plan_tool", MODULE_PATH)
assert SPEC and SPEC.loader
plan_tool = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(plan_tool)


class PlanToolTests(unittest.TestCase):
    def sample_plan(self) -> dict:
        return {
            "operations": [
                {
                    "operation_id": "OP-1",
                    "action": "create",
                    "target_id": "new",
                    "baseline_revision": None,
                    "fields": {"title": "Example"},
                    "relations": [],
                    "idempotency_key": "REQ:source:1",
                    "data_destination": "Linear project demo",
                    "redactions": [],
                    "expected_effect": "Create one requirement",
                }
            ]
        }

    def test_seal_and_validate(self) -> None:
        sealed = plan_tool.seal_plan(self.sample_plan())
        self.assertTrue(sealed["plan_id"].startswith("PLAN-"))
        self.assertEqual(len(sealed["plan_sha256"]), 64)
        self.assertEqual(plan_tool.validate_plan(sealed), [])

    def test_change_invalidates_plan(self) -> None:
        sealed = plan_tool.seal_plan(self.sample_plan())
        sealed["operations"][0]["fields"]["title"] = "Changed"
        self.assertIn("plan_sha256 does not match canonical plan content", plan_tool.validate_plan(sealed))

    def test_key_order_does_not_change_hash(self) -> None:
        first = self.sample_plan()
        second = {"operations": [dict(reversed(list(first["operations"][0].items())))]}
        self.assertEqual(plan_tool.plan_sha256(first), plan_tool.plan_sha256(second))


if __name__ == "__main__":
    unittest.main()
