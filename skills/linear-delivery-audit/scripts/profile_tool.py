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
GOVERNANCE_TYPES = ("REQ", "PROB", "DEC", "CR", "RISK", "Q")
EXECUTION_TYPES = ("Analysis", "Implementation", "Validation", "Collaboration")
SEMANTIC_STATES = ("Backlog", "Todo", "InProgress", "InReview", "Done", "Canceled", "Duplicate")
COPY_POLICIES = {"link-only", "summary", "redacted-excerpt", "prohibited"}
PERIOD_RULES = {"previous-calendar-month", "fixed-range", "release-candidate-scope"}


def canonical_profile_bytes(profile_body: dict[str, Any]) -> bytes:
    return json.dumps(profile_body, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def profile_sha256(profile_body: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_profile_bytes(profile_body)).hexdigest()


def load_document(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read JSON Profile {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("Profile document must be a JSON object")
    return data


def write_document(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def is_placeholder(value: Any) -> bool:
    return isinstance(value, str) and value.startswith("<") and value.endswith(">")


def contains_placeholder(value: Any) -> bool:
    if is_placeholder(value):
        return True
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
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError(f"timestamp requires timezone: {value}")
    return parsed


def valid_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip()) and not is_placeholder(value)


def validate_exact_mapping(mapping: Any, keys: tuple[str, ...], label: str, errors: list[str]) -> None:
    if not isinstance(mapping, dict):
        errors.append(f"{label} must be an object")
        return
    missing = [key for key in keys if key not in mapping or not valid_text(mapping.get(key))]
    if missing:
        errors.append(f"{label} missing usable mappings: {', '.join(missing)}")


def validate_profile_body(profile: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if contains_placeholder(profile):
        errors.append("Profile contains unresolved placeholders")

    identity = profile.get("identity")
    if not isinstance(identity, dict):
        errors.append("profile.identity must be an object")
    else:
        for key in ("project_key", "project_name", "timezone", "accountable_owner"):
            if not valid_text(identity.get(key)):
                errors.append(f"profile.identity.{key} is required")
        timezone_name = identity.get("timezone")
        if valid_text(timezone_name):
            try:
                ZoneInfo(str(timezone_name))
            except KeyError:
                errors.append(f"unknown IANA timezone: {timezone_name}")

    structure = profile.get("linear_structure")
    if not isinstance(structure, dict):
        errors.append("profile.linear_structure must be an object")
    else:
        mode = structure.get("structure_mode")
        if mode not in {"single-project", "dual-project"}:
            errors.append("structure_mode must be single-project or dual-project")
        for key in (
            "team_or_workspace",
            "governance_project",
            "delivery_project",
            "source_field_heading",
            "native_source_relation",
            "authoritative_governance_document",
        ):
            if not valid_text(structure.get(key)):
                errors.append(f"profile.linear_structure.{key} is required")
        if mode == "single-project" and structure.get("governance_project") != structure.get("delivery_project"):
            errors.append("single-project mode must use the same governance and delivery project")
        validate_exact_mapping(structure.get("governance_type_label_mapping"), GOVERNANCE_TYPES, "governance type mapping", errors)
        validate_exact_mapping(structure.get("execution_type_label_mapping"), EXECUTION_TYPES, "execution type mapping", errors)
        validate_exact_mapping(structure.get("status_mapping"), SEMANTIC_STATES, "status mapping", errors)

    authority = profile.get("report_and_write_authority")
    if not isinstance(authority, dict):
        errors.append("profile.report_and_write_authority must be an object")
    else:
        for key in ("audit_report_destination", "destination_audience", "destination_data_classification"):
            if not valid_text(authority.get(key)):
                errors.append(f"profile.report_and_write_authority.{key} is required")
        writes = authority.get("authorized_audit_writes")
        if not isinstance(writes, list):
            errors.append("authorized_audit_writes must be a list")
        if authority.get("audit_report_destination") != "return-only" and not writes:
            errors.append("a non-return-only destination requires an explicit authorized audit write")

    data_flow = profile.get("data_flow_policy")
    if not isinstance(data_flow, dict):
        errors.append("profile.data_flow_policy must be an object")
    else:
        if data_flow.get("copy_policy") not in COPY_POLICIES:
            errors.append("copy_policy is invalid")
        if not isinstance(data_flow.get("source_classifications"), dict) or not data_flow.get("source_classifications"):
            errors.append("source_classifications must be a non-empty object")
        if not isinstance(data_flow.get("allowed_source_to_destination_flows"), list) or not data_flow.get("allowed_source_to_destination_flows"):
            errors.append("allowed_source_to_destination_flows must be a non-empty list")
        quoted = data_flow.get("maximum_quoted_characters")
        if not isinstance(quoted, int) or quoted < 0:
            errors.append("maximum_quoted_characters must be a non-negative integer")

    period = profile.get("audit_period")
    if not isinstance(period, dict):
        errors.append("profile.audit_period must be an object")
    elif period.get("rule") not in PERIOD_RULES:
        errors.append("audit period rule is invalid")

    collection = profile.get("collection")
    if not isinstance(collection, dict):
        errors.append("profile.collection must be an object")
    else:
        for key in (
            "expected_item_count_source",
            "pagination_or_cursor_strategy",
            "required_comment_document_relation_access",
            "consistent_snapshot_strategy",
        ):
            if not valid_text(collection.get(key)):
                errors.append(f"profile.collection.{key} is required")
        gap = collection.get("maximum_project_wide_collection_gap")
        if gap != 0:
            errors.append("maximum_project_wide_collection_gap must be 0")

    policy = profile.get("audit_policy")
    if not isinstance(policy, dict):
        errors.append("profile.audit_policy must be an object")
    else:
        minimum = policy.get("minimum_observability")
        if not isinstance(minimum, dict):
            errors.append("minimum_observability must be an object")
        else:
            if minimum.get("source", 0) < 1.0 or minimum.get("disposition", 0) < 1.0 or minimum.get("done_evidence", 0) < 0.95:
                errors.append("minimum_observability weakens bundled thresholds")
        if not valid_text(policy.get("approved_operational_maintenance_marker")):
            errors.append("approved_operational_maintenance_marker is required")

    prior = profile.get("prior_report_comparison")
    if not isinstance(prior, dict):
        errors.append("profile.prior_report_comparison must be an object")
    else:
        for key in ("lookup_location", "title_pattern", "existing_period_behavior", "ruleset_compatibility"):
            if not valid_text(prior.get(key)):
                errors.append(f"profile.prior_report_comparison.{key} is required")

    return errors


def validate_document(document: dict[str, Any], now: datetime | None = None) -> list[str]:
    errors: list[str] = []
    if document.get("profile_schema_version") != SCHEMA_VERSION:
        errors.append(f"profile_schema_version must be {SCHEMA_VERSION}")
    if not valid_text(document.get("profile_id")):
        errors.append("profile_id is required and cannot be a placeholder")
    revision = document.get("profile_revision")
    if not isinstance(revision, int) or revision < 1:
        errors.append("profile_revision must be a positive integer")

    approval = document.get("approval")
    profile = document.get("profile")
    if not isinstance(profile, dict):
        errors.append("profile must be an object")
        profile = {}
    else:
        errors.extend(validate_profile_body(profile))
    if not isinstance(approval, dict):
        errors.append("approval must be an object")
        approval = {}

    for key in (
        "approved_by",
        "approved_at",
        "approval_record",
        "allowed_editors",
        "maximum_profile_age_days",
        "approved_profile_body_sha256",
    ):
        if key not in approval:
            errors.append(f"approval.{key} is required")

    if approval.get("approved_profile_body_sha256") != profile_sha256(profile):
        errors.append("approved Profile body SHA-256 does not match Profile content")
    if not valid_text(approval.get("approved_by")) or not valid_text(approval.get("approval_record")):
        errors.append("approval approver and record must be usable values")
    editors = approval.get("allowed_editors")
    if not isinstance(editors, list) or not editors or any(not valid_text(item) for item in editors):
        errors.append("approval.allowed_editors must be a non-empty list of usable values")
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
                errors.append("Profile approval has expired")
        except ValueError as exc:
            errors.append(str(exc))
    else:
        errors.append("approval.approved_at must be an RFC3339 string")
    return errors


def resolve_period(document: dict[str, Any], now: datetime | None = None) -> dict[str, str]:
    profile = require_mapping(document, "profile")
    identity = require_mapping(profile, "identity")
    period = require_mapping(profile, "audit_period")
    timezone_name = identity.get("timezone")
    if not valid_text(timezone_name):
        raise ValueError("profile.identity.timezone is required")
    zone = ZoneInfo(str(timezone_name))
    current = (now or datetime.now(timezone.utc)).astimezone(zone)
    rule = period.get("rule")

    if rule == "previous-calendar-month":
        end = current.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        start = end.replace(year=end.year - 1, month=12) if end.month == 1 else end.replace(month=end.month - 1)
    elif rule == "fixed-range":
        start_raw, end_raw = period.get("fixed_start"), period.get("fixed_end")
        if not isinstance(start_raw, str) or not isinstance(end_raw, str):
            raise ValueError("fixed-range requires fixed_start and fixed_end")
        start, end = parse_rfc3339(start_raw).astimezone(zone), parse_rfc3339(end_raw).astimezone(zone)
        if end <= start:
            raise ValueError("fixed_end must be later than fixed_start")
    elif rule == "release-candidate-scope":
        candidate = require_mapping(profile, "software_evidence").get("candidate_scope")
        if not valid_text(candidate) or candidate == "none":
            raise ValueError("release-candidate-scope requires an exact candidate_scope")
        return {"rule": rule, "timezone": str(timezone_name), "candidate_scope": str(candidate)}
    else:
        raise ValueError(f"unsupported audit period rule: {rule}")
    return {
        "rule": str(rule),
        "timezone": str(timezone_name),
        "start_inclusive": start.isoformat(),
        "end_exclusive": end.isoformat(),
    }


def template_document(args: argparse.Namespace | None = None) -> dict[str, Any]:
    args = args or argparse.Namespace()
    project_key = getattr(args, "project_key", None) or "<stable-profile-id>"
    project_name = getattr(args, "project_name", None) or "<exact-project-name>"
    timezone_name = getattr(args, "timezone", None) or "<IANA-timezone>"
    owner = getattr(args, "owner", None) or "<person-or-role>"
    team = getattr(args, "team", None) or "<exact-team-or-workspace>"
    mode = getattr(args, "structure_mode", None) or "single-project"
    project = getattr(args, "project", None) or "<exact-project-name-or-id>"
    governance_project = getattr(args, "governance_project", None) or project
    delivery_project = getattr(args, "delivery_project", None) or project
    if mode == "single-project":
        delivery_project = governance_project

    return {
        "profile_schema_version": SCHEMA_VERSION,
        "profile_id": project_key,
        "profile_revision": 1,
        "approval": {
            "approved_by": "<generated-by-seal-command>",
            "approved_at": "<generated-by-seal-command>",
            "approval_record": "<generated-by-seal-command>",
            "allowed_editors": ["<generated-by-seal-command>"],
            "maximum_profile_age_days": 90,
            "approved_profile_body_sha256": "<generated-by-seal-command>",
        },
        "profile": {
            "identity": {
                "project_key": project_key,
                "project_name": project_name,
                "timezone": timezone_name,
                "accountable_owner": owner,
            },
            "linear_structure": {
                "team_or_workspace": team,
                "structure_mode": mode,
                "governance_project": governance_project,
                "delivery_project": delivery_project,
                "governance_type_label_mapping": {key: key for key in GOVERNANCE_TYPES},
                "execution_type_label_mapping": {key: key for key in EXECUTION_TYPES},
                "status_mapping": {key: key.replace("InProgress", "In Progress").replace("InReview", "In Review") for key in SEMANTIC_STATES},
                "source_field_heading": "Source",
                "native_source_relation": "relatedTo",
                "authoritative_governance_document": "project-governance-document",
            },
            "report_and_write_authority": {
                "audit_report_destination": "return-only",
                "destination_audience": "project-team",
                "destination_data_classification": "internal",
                "authorized_audit_writes": [],
                "prohibited_writes": ["formal-requirement-change", "change-approval", "risk-acceptance", "business-closure", "destructive-cleanup", "ci-rerun", "merge", "deployment"],
            },
            "data_flow_policy": {
                "source_classifications": {"Linear": "internal", "GitHub": "internal"},
                "allowed_source_to_destination_flows": ["internal-to-internal-link-or-summary"],
                "copy_policy": "link-only",
                "required_redactions": ["secrets", "personal-data", "source-code", "private-logs", "security-details"],
                "maximum_quoted_characters": 500,
                "allowed_linked_domains_or_evidence_systems": ["Linear", "GitHub"],
            },
            "software_evidence": {"repositories": [], "default_branches": {}, "candidate_scope": "none", "deployment_or_runtime_evidence_systems": []},
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
                "expected_item_count_source": "project-list-count",
                "pagination_or_cursor_strategy": "iterate-all-cursors",
                "required_comment_document_relation_access": "required-for-in-scope-items",
                "maximum_project_wide_collection_gap": 0,
                "consistent_snapshot_strategy": "updated-at-recheck",
            },
            "audit_policy": {
                "stale_in_progress_days": 14,
                "approved_operational_maintenance_marker": "maintenance",
                "minimum_observability": {"source": 1.0, "disposition": 1.0, "done_evidence": 0.95},
                "evidence_access_limitations": "none-known",
                "prompt_injection_reporting_destination": "audit-report",
            },
            "prior_report_comparison": {
                "lookup_location": "configured-report-destination",
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
    write_document(output, template_document(args))
    print(f"created Profile template: {output}")
    return 0


def command_hash(args: argparse.Namespace) -> int:
    print(profile_sha256(require_mapping(load_document(Path(args.profile)), "profile")))
    return 0


def command_seal(args: argparse.Namespace) -> int:
    source = Path(args.profile)
    document = load_document(source)
    profile = require_mapping(document, "profile")
    body_errors = validate_profile_body(profile)
    if body_errors:
        raise ValueError("cannot seal invalid Profile:\n- " + "\n- ".join(body_errors))
    sealed = deepcopy(document)
    sealed["profile_schema_version"] = SCHEMA_VERSION
    if args.increment_revision:
        revision = sealed.get("profile_revision", 0)
        if not isinstance(revision, int):
            raise ValueError("profile_revision must be an integer")
        sealed["profile_revision"] = revision + 1
    approved_at = args.approved_at or datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    sealed["approval"] = {
        "approved_by": args.approved_by,
        "approved_at": approved_at,
        "approval_record": args.approval_record,
        "allowed_editors": args.allowed_editor or [args.approved_by],
        "maximum_profile_age_days": args.maximum_profile_age_days,
        "approved_profile_body_sha256": profile_sha256(profile),
    }
    errors = validate_document(sealed)
    if errors:
        raise ValueError("cannot seal invalid Profile:\n- " + "\n- ".join(errors))
    output = Path(args.output) if args.output else source
    write_document(output, sealed)
    print(f"sealed Profile: {output}")
    print(f"Profile SHA-256: {sealed['approval']['approved_profile_body_sha256']}")
    return 0


def command_validate(args: argparse.Namespace) -> int:
    errors = validate_document(load_document(Path(args.profile)), now=parse_rfc3339(args.now) if args.now else None)
    if errors:
        for error in errors:
            print(f"[FAIL] {error}")
        return 1
    print("[OK] Profile schema, mappings, approval, hash, and expiry are valid")
    return 0


def command_resolve_period(args: argparse.Namespace) -> int:
    document = load_document(Path(args.profile))
    print(json.dumps(resolve_period(document, now=parse_rfc3339(args.now) if args.now else None), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate, seal, validate, and resolve Linear GPT PM audit Profiles.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    init_parser = subparsers.add_parser("init", help="Create a mostly prefilled JSON Profile.")
    init_parser.add_argument("output")
    init_parser.add_argument("--project-key")
    init_parser.add_argument("--project-name")
    init_parser.add_argument("--timezone")
    init_parser.add_argument("--owner")
    init_parser.add_argument("--team")
    init_parser.add_argument("--structure-mode", choices=("single-project", "dual-project"), default="single-project")
    init_parser.add_argument("--project")
    init_parser.add_argument("--governance-project")
    init_parser.add_argument("--delivery-project")
    init_parser.add_argument("--force", action="store_true")
    init_parser.set_defaults(func=command_init)
    hash_parser = subparsers.add_parser("hash", help="Print the canonical Profile body SHA-256.")
    hash_parser.add_argument("profile")
    hash_parser.set_defaults(func=command_hash)
    seal_parser = subparsers.add_parser("seal", help="Approve and seal a completed Profile.")
    seal_parser.add_argument("profile")
    seal_parser.add_argument("--output")
    seal_parser.add_argument("--approved-by", required=True)
    seal_parser.add_argument("--approval-record", required=True)
    seal_parser.add_argument("--approved-at")
    seal_parser.add_argument("--allowed-editor", action="append")
    seal_parser.add_argument("--maximum-profile-age-days", type=int, default=90)
    seal_parser.add_argument("--increment-revision", action="store_true")
    seal_parser.set_defaults(func=command_seal)
    validate_parser = subparsers.add_parser("validate", help="Validate a sealed Profile.")
    validate_parser.add_argument("profile")
    validate_parser.add_argument("--now")
    validate_parser.set_defaults(func=command_validate)
    period_parser = subparsers.add_parser("resolve-period", help="Resolve the absolute audit period.")
    period_parser.add_argument("profile")
    period_parser.add_argument("--now")
    period_parser.set_defaults(func=command_resolve_period)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return int(args.func(args))
    except (KeyError, ValueError) as exc:
        print(f"[FAIL] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
