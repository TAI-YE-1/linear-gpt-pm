from __future__ import annotations

import argparse
import hashlib
import json
import sys
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

SCHEMA_VERSION = 4


def canonical_profile_bytes(profile_body: dict[str, Any]) -> bytes:
    return json.dumps(
        profile_body,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def profile_sha256(profile_body: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_profile_bytes(profile_body)).hexdigest()


def load_document(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read JSON profile {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("profile document must be a JSON object")
    return data


def write_document(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def contains_placeholder(value: Any) -> bool:
    if isinstance(value, str):
        return value.startswith("<") and value.endswith(">")
    if isinstance(value, dict):
        return any(contains_placeholder(item) for item in value.values())
    if isinstance(value, list):
        return any(contains_placeholder(item) for item in value)
    return False


def require_mapping(container: dict[str, Any], key: str) -> dict[str, Any]:
    value = container.get(key)
    if not isinstance(value, dict):
        raise ValueError(f"missing or invalid mapping: {key}")
    return value


def parse_rfc3339(value: str) -> datetime:
    normalized = value.replace("Z", "+00:00")
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        raise ValueError(f"timestamp requires timezone: {value}")
    return parsed


def validate_document(document: dict[str, Any], now: datetime | None = None) -> list[str]:
    errors: list[str] = []
    if document.get("profile_schema_version") != SCHEMA_VERSION:
        errors.append(f"profile_schema_version must be {SCHEMA_VERSION}")

    profile_id = document.get("profile_id")
    if not isinstance(profile_id, str) or not profile_id.strip():
        errors.append("profile_id is required")
    revision = document.get("profile_revision")
    if not isinstance(revision, int) or revision < 1:
        errors.append("profile_revision must be a positive integer")

    approval = document.get("approval")
    profile = document.get("profile")
    if not isinstance(approval, dict):
        errors.append("approval must be an object")
        approval = {}
    if not isinstance(profile, dict):
        errors.append("profile must be an object")
        profile = {}

    if contains_placeholder(profile):
        errors.append("profile contains unresolved placeholders")

    required_approval = (
        "approved_by",
        "approved_at",
        "approval_record",
        "allowed_editors",
        "maximum_profile_age_days",
        "approved_profile_body_sha256",
    )
    for key in required_approval:
        if key not in approval:
            errors.append(f"approval.{key} is required")

    expected_hash = profile_sha256(profile)
    if approval.get("approved_profile_body_sha256") != expected_hash:
        errors.append("approved profile body SHA-256 does not match profile content")

    allowed_editors = approval.get("allowed_editors")
    if not isinstance(allowed_editors, list) or not allowed_editors:
        errors.append("approval.allowed_editors must be a non-empty list")

    max_age = approval.get("maximum_profile_age_days")
    if not isinstance(max_age, int) or max_age < 1:
        errors.append("approval.maximum_profile_age_days must be a positive integer")

    approved_at = approval.get("approved_at")
    if isinstance(approved_at, str) and isinstance(max_age, int) and max_age > 0:
        try:
            approved_time = parse_rfc3339(approved_at)
            current = now or datetime.now(timezone.utc)
            age_seconds = (current.astimezone(timezone.utc) - approved_time.astimezone(timezone.utc)).total_seconds()
            if age_seconds < 0:
                errors.append("approval.approved_at is in the future")
            elif age_seconds > max_age * 86400:
                errors.append("profile approval has expired")
        except ValueError as exc:
            errors.append(str(exc))
    elif approved_at is not None:
        errors.append("approval.approved_at must be an RFC3339 string")

    try:
        identity = require_mapping(profile, "identity")
        timezone_name = identity.get("timezone")
        if not isinstance(timezone_name, str):
            errors.append("profile.identity.timezone is required")
        else:
            ZoneInfo(timezone_name)
    except (ValueError, KeyError) as exc:
        errors.append(str(exc))

    for key in (
        "linear_structure",
        "report_and_write_authority",
        "data_flow_policy",
        "audit_period",
        "collection",
        "audit_policy",
        "prior_report_comparison",
    ):
        try:
            require_mapping(profile, key)
        except ValueError as exc:
            errors.append(str(exc))

    return errors


def resolve_period(document: dict[str, Any], now: datetime | None = None) -> dict[str, str]:
    profile = require_mapping(document, "profile")
    identity = require_mapping(profile, "identity")
    period = require_mapping(profile, "audit_period")
    timezone_name = identity.get("timezone")
    if not isinstance(timezone_name, str):
        raise ValueError("profile.identity.timezone is required")
    zone = ZoneInfo(timezone_name)
    current = (now or datetime.now(timezone.utc)).astimezone(zone)
    rule = period.get("rule")

    if rule == "previous-calendar-month":
        current_month_start = current.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if current_month_start.month == 1:
            start = current_month_start.replace(year=current_month_start.year - 1, month=12)
        else:
            start = current_month_start.replace(month=current_month_start.month - 1)
        end = current_month_start
    elif rule == "fixed-range":
        start_raw = period.get("fixed_start")
        end_raw = period.get("fixed_end")
        if not isinstance(start_raw, str) or not isinstance(end_raw, str):
            raise ValueError("fixed-range requires fixed_start and fixed_end")
        start = parse_rfc3339(start_raw).astimezone(zone)
        end = parse_rfc3339(end_raw).astimezone(zone)
        if end <= start:
            raise ValueError("fixed_end must be later than fixed_start")
    elif rule == "release-candidate-scope":
        candidate = require_mapping(profile, "software_evidence").get("candidate_scope")
        if not isinstance(candidate, str) or not candidate or contains_placeholder(candidate):
            raise ValueError("release-candidate-scope requires an exact candidate_scope")
        return {
            "rule": rule,
            "timezone": timezone_name,
            "candidate_scope": candidate,
        }
    else:
        raise ValueError(f"unsupported audit period rule: {rule}")

    return {
        "rule": str(rule),
        "timezone": timezone_name,
        "start_inclusive": start.isoformat(),
        "end_exclusive": end.isoformat(),
    }


def template_document() -> dict[str, Any]:
    return {
        "profile_schema_version": SCHEMA_VERSION,
        "profile_id": "<stable-profile-id>",
        "profile_revision": 1,
        "approval": {
            "approved_by": "<person-or-authorized-role>",
            "approved_at": "<RFC3339-timestamp>",
            "approval_record": "<stable-record-id>",
            "allowed_editors": ["<person-or-authorized-role>"],
            "maximum_profile_age_days": 90,
            "approved_profile_body_sha256": "<generated-by-seal-command>",
        },
        "profile": {
            "identity": {
                "project_key": "<stable-short-key>",
                "project_name": "<exact-project-name>",
                "timezone": "<IANA-timezone>",
                "accountable_owner": "<person-or-role>",
            },
            "linear_structure": {
                "team_or_workspace": "<exact-team-or-workspace>",
                "structure_mode": "<single-project-or-dual-project>",
                "governance_project": "<exact-name-or-id>",
                "delivery_project": "<exact-name-or-id>",
                "governance_type_label_mapping": {},
                "execution_type_label_mapping": {},
                "status_mapping": {},
                "source_field_heading": "Source",
                "native_source_relation": "relatedTo",
                "authoritative_governance_document": "<exact-document-location>",
            },
            "report_and_write_authority": {
                "audit_report_destination": "return-only",
                "destination_audience": "<exact-audience>",
                "destination_data_classification": "<classification>",
                "authorized_audit_writes": [],
                "prohibited_writes": [
                    "formal-requirement-change",
                    "change-approval",
                    "risk-acceptance",
                    "business-closure",
                    "destructive-cleanup",
                    "ci-rerun",
                    "merge",
                    "deployment",
                ],
            },
            "data_flow_policy": {
                "source_classifications": {},
                "allowed_source_to_destination_flows": [],
                "copy_policy": "link-only",
                "required_redactions": [
                    "secrets",
                    "personal-data",
                    "source-code",
                    "private-logs",
                    "security-details",
                ],
                "maximum_quoted_characters": 500,
                "allowed_linked_domains_or_evidence_systems": [],
            },
            "software_evidence": {
                "repositories": [],
                "default_branches": {},
                "candidate_scope": "none",
                "deployment_or_runtime_evidence_systems": [],
            },
            "audit_period": {
                "rule": "previous-calendar-month",
                "fixed_start": None,
                "fixed_end": None,
                "report_period_naming": "audited-period",
                "active_item_scope": "all-active",
                "done_evidence_lookback_days": 31,
                "changed_item_lookback_days": 31,
                "historical_baseline_treatment": "track-unresolved-prior-exceptions",
            },
            "collection": {
                "expected_item_count_source": "<exact-method>",
                "pagination_or_cursor_strategy": "<exact-method>",
                "required_comment_document_relation_access": "<requirements>",
                "maximum_project_wide_collection_gap": 0,
                "consistent_snapshot_strategy": "updated-at-recheck",
            },
            "audit_policy": {
                "stale_in_progress_days": 14,
                "approved_operational_maintenance_marker": "<label-or-rule>",
                "minimum_observability": {
                    "source": 1.0,
                    "disposition": 1.0,
                    "done_evidence": 0.95,
                },
                "evidence_access_limitations": "none-known",
                "prompt_injection_reporting_destination": "audit-report",
            },
            "prior_report_comparison": {
                "lookup_location": "<exact-location>",
                "title_pattern": "Governance Audit | <project-key> | YYYY-MM",
                "existing_period_behavior": "update-existing-report",
                "ruleset_compatibility": "same-ruleset",
            },
        },
    }


def command_init(args: argparse.Namespace) -> int:
    output = Path(args.output)
    if output.exists() and not args.force:
        raise ValueError(f"refusing to overwrite existing file: {output}")
    write_document(output, template_document())
    print(f"created profile template: {output}")
    return 0


def command_hash(args: argparse.Namespace) -> int:
    document = load_document(Path(args.profile))
    profile = require_mapping(document, "profile")
    print(profile_sha256(profile))
    return 0


def command_seal(args: argparse.Namespace) -> int:
    source = Path(args.profile)
    document = load_document(source)
    profile = require_mapping(document, "profile")
    if contains_placeholder(profile):
        raise ValueError("complete all profile placeholders before sealing")

    sealed = deepcopy(document)
    sealed["profile_schema_version"] = SCHEMA_VERSION
    if args.increment_revision:
        current_revision = sealed.get("profile_revision", 0)
        if not isinstance(current_revision, int):
            raise ValueError("profile_revision must be an integer")
        sealed["profile_revision"] = current_revision + 1

    approved_at = args.approved_at or datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    editors = args.allowed_editor or [args.approved_by]
    sealed["approval"] = {
        "approved_by": args.approved_by,
        "approved_at": approved_at,
        "approval_record": args.approval_record,
        "allowed_editors": editors,
        "maximum_profile_age_days": args.maximum_profile_age_days,
        "approved_profile_body_sha256": profile_sha256(profile),
    }

    errors = validate_document(sealed)
    if errors:
        raise ValueError("cannot seal invalid profile:\n- " + "\n- ".join(errors))
    output = Path(args.output) if args.output else source
    write_document(output, sealed)
    print(f"sealed profile: {output}")
    print(f"profile SHA-256: {sealed['approval']['approved_profile_body_sha256']}")
    return 0


def command_validate(args: argparse.Namespace) -> int:
    document = load_document(Path(args.profile))
    now = parse_rfc3339(args.now) if args.now else None
    errors = validate_document(document, now=now)
    if errors:
        for error in errors:
            print(f"[FAIL] {error}")
        return 1
    print("[OK] profile schema, approval, hash, and expiry are valid")
    return 0


def command_resolve_period(args: argparse.Namespace) -> int:
    document = load_document(Path(args.profile))
    now = parse_rfc3339(args.now) if args.now else None
    print(json.dumps(resolve_period(document, now=now), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate, seal, validate, and resolve Linear GPT PM audit profiles.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Create a JSON profile template.")
    init_parser.add_argument("output")
    init_parser.add_argument("--force", action="store_true")
    init_parser.set_defaults(func=command_init)

    hash_parser = subparsers.add_parser("hash", help="Print the canonical profile-body SHA-256.")
    hash_parser.add_argument("profile")
    hash_parser.set_defaults(func=command_hash)

    seal_parser = subparsers.add_parser("seal", help="Approve and seal a completed profile.")
    seal_parser.add_argument("profile")
    seal_parser.add_argument("--output")
    seal_parser.add_argument("--approved-by", required=True)
    seal_parser.add_argument("--approval-record", required=True)
    seal_parser.add_argument("--approved-at")
    seal_parser.add_argument("--allowed-editor", action="append")
    seal_parser.add_argument("--maximum-profile-age-days", type=int, default=90)
    seal_parser.add_argument("--increment-revision", action="store_true")
    seal_parser.set_defaults(func=command_seal)

    validate_parser = subparsers.add_parser("validate", help="Validate a sealed profile.")
    validate_parser.add_argument("profile")
    validate_parser.add_argument("--now")
    validate_parser.set_defaults(func=command_validate)

    period_parser = subparsers.add_parser("resolve-period", help="Resolve the profile's absolute audit period.")
    period_parser.add_argument("profile")
    period_parser.add_argument("--now")
    period_parser.set_defaults(func=command_resolve_period)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except ValueError as exc:
        print(f"[FAIL] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
