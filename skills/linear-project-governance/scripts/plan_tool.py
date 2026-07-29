from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

REQUIRED_OPERATION_FIELDS = {
    "operation_id",
    "action",
    "target_id",
    "baseline_revision",
    "fields",
    "relations",
    "idempotency_key",
    "data_destination",
    "redactions",
    "expected_effect",
}


def load_plan(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read plan JSON {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("plan must be a JSON object")
    return data


def canonical_plan_bytes(plan: dict[str, Any]) -> bytes:
    body = {key: value for key, value in plan.items() if key not in {"plan_id", "plan_sha256"}}
    return json.dumps(body, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def plan_sha256(plan: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_plan_bytes(plan)).hexdigest()


def plan_id(digest: str) -> str:
    return f"PLAN-{digest[:10].upper()}"


def validate_plan(plan: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    operations = plan.get("operations")
    if not isinstance(operations, list) or not operations:
        return ["operations must be a non-empty list"]

    operation_ids: set[str] = set()
    for index, operation in enumerate(operations, start=1):
        if not isinstance(operation, dict):
            errors.append(f"operation {index} must be an object")
            continue
        missing = sorted(REQUIRED_OPERATION_FIELDS - set(operation))
        if missing:
            errors.append(f"operation {index} missing fields: {', '.join(missing)}")
        operation_id = operation.get("operation_id")
        if not isinstance(operation_id, str) or not operation_id:
            errors.append(f"operation {index} requires operation_id")
        elif operation_id in operation_ids:
            errors.append(f"duplicate operation_id: {operation_id}")
        else:
            operation_ids.add(operation_id)

    digest = plan_sha256(plan)
    if "plan_sha256" in plan and plan.get("plan_sha256") != digest:
        errors.append("plan_sha256 does not match canonical plan content")
    if "plan_id" in plan and plan.get("plan_id") != plan_id(digest):
        errors.append("plan_id does not match canonical plan content")
    return errors


def seal_plan(plan: dict[str, Any]) -> dict[str, Any]:
    errors = validate_plan({key: value for key, value in plan.items() if key not in {"plan_id", "plan_sha256"}})
    if errors:
        raise ValueError("invalid plan:\n- " + "\n- ".join(errors))
    sealed = dict(plan)
    digest = plan_sha256(plan)
    sealed["plan_id"] = plan_id(digest)
    sealed["plan_sha256"] = digest
    return sealed


def write_plan(path: Path, plan: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(plan, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def command_seal(args: argparse.Namespace) -> int:
    source = Path(args.plan)
    sealed = seal_plan(load_plan(source))
    output = Path(args.output) if args.output else source
    write_plan(output, sealed)
    print(f"Plan ID: {sealed['plan_id']}")
    print(f"Plan SHA-256: {sealed['plan_sha256']}")
    return 0


def command_validate(args: argparse.Namespace) -> int:
    plan = load_plan(Path(args.plan))
    errors = validate_plan(plan)
    if args.expected_sha and plan_sha256(plan) != args.expected_sha:
        errors.append("canonical plan SHA-256 differs from --expected-sha")
    if errors:
        for error in errors:
            print(f"[FAIL] {error}")
        return 1
    digest = plan_sha256(plan)
    print(f"[OK] {plan_id(digest)} {digest}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Seal and verify immutable Linear governance operation plans.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    seal = subparsers.add_parser("seal", help="Add a short Plan ID and full SHA-256 to a plan JSON file.")
    seal.add_argument("plan")
    seal.add_argument("--output")
    seal.set_defaults(func=command_seal)

    validate = subparsers.add_parser("validate", help="Validate a sealed plan before execution.")
    validate.add_argument("plan")
    validate.add_argument("--expected-sha")
    validate.set_defaults(func=command_validate)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return int(args.func(args))
    except ValueError as exc:
        print(f"[FAIL] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
