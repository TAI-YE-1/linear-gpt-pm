# Audit Project Profile

Use one completed profile per governed project. Store it at an exact immutable or revisioned location accessible to the audit runtime. Do not schedule an audit with placeholders.

## Canonical machine-readable profile

Complete this YAML block. Keep the `approval` envelope separate from the `profile` body so the body can be hashed deterministically.

```yaml
profile_schema_version: 3
profile_id: "<stable-profile-id>"
profile_revision: 1

approval:
  approved_by: "<person-or-authorized-role>"
  approved_at: "<RFC3339 timestamp>"
  approval_record: "<stable approval comment/document/issue ID>"
  allowed_editors:
    - "<person-or-authorized-role>"
  maximum_profile_age_days: 90
  approved_profile_body_sha256: "<64 lowercase hexadecimal characters>"

profile:
  identity:
    project_key: "<stable-short-key>"
    project_name: "<exact-project-name>"
    timezone: "<IANA-timezone>"
    accountable_owner: "<person-or-role>"

  linear_structure:
    team_or_workspace: "<exact-team-or-workspace>"
    structure_mode: "<single-project-or-dual-project>"
    governance_project: "<exact-name-or-id>"
    delivery_project: "<exact-name-or-id>"
    governance_type_label_mapping:
      REQ: "<exact-label>"
      PROB: "<exact-label>"
      DEC: "<exact-label>"
      CR: "<exact-label>"
      RISK: "<exact-label>"
      Q: "<exact-label>"
    execution_type_label_mapping:
      Analysis: "<exact-label>"
      Implementation: "<exact-label>"
      Validation: "<exact-label>"
      Collaboration: "<exact-label>"
    status_mapping:
      Backlog: "<exact-status>"
      Todo: "<exact-status>"
      InProgress: "<exact-status>"
      InReview: "<exact-status>"
      Done: "<exact-status>"
      Canceled: "<exact-status>"
      Duplicate: "<exact-status>"
    source_field_heading: "<exact-structured-heading>"
    native_source_relation: "<relatedTo-or-approved-fallback>"
    authoritative_governance_document: "<exact-document-location>"

  report_and_write_authority:
    audit_report_destination: "<exact-document-project-issue-or-status-target>"
    destination_audience: "<exact-audience>"
    destination_data_classification: "<classification>"
    authorized_audit_writes:
      - "<exact-report-document-comment-or-status-update>"
    prohibited_writes:
      - formal-requirement-change
      - change-approval
      - risk-acceptance
      - business-closure
      - destructive-cleanup
      - ci-rerun
      - merge
      - deployment

  data_flow_policy:
    source_classifications:
      Linear: "<classification>"
      GitHub: "<classification-or-not-applicable>"
      Documents: "<classification>"
      Logs: "<classification-or-not-applicable>"
    allowed_source_to_destination_flows:
      - "<exact rule>"
    copy_policy: "<link-only-summary-redacted-excerpt-or-prohibited>"
    required_redactions:
      - secrets
      - personal-data
      - source-code
      - private-logs
      - security-details
    maximum_quoted_characters: 500
    allowed_linked_domains_or_evidence_systems:
      - "<exact-domain-or-system>"

  software_evidence:
    repositories:
      - "<owner/repository-or-none>"
    default_branches:
      "<owner/repository>": "<branch>"
    candidate_scope: "<pull-request-release-commit-rule-or-none>"
    deployment_or_runtime_evidence_systems:
      - "<exact-source-or-none>"

  audit_period:
    rule: "<previous-calendar-month-fixed-range-or-release-candidate-scope>"
    fixed_start: "<RFC3339-or-null>"
    fixed_end: "<RFC3339-or-null>"
    report_period_naming: "<audited-period>"
    active_item_scope: "<all-active-or-explicit-filter>"
    done_evidence_lookback_days: 31
    changed_item_lookback_days: 31
    historical_baseline_treatment: "<rule>"

  collection:
    expected_item_count_source: "<exact-method>"
    pagination_or_cursor_strategy: "<exact-method>"
    required_comment_document_relation_access: "<requirements>"
    maximum_project_wide_collection_gap: 0
    consistent_snapshot_strategy: "<updated-at-recheck-or-connector-snapshot>"

  audit_policy:
    stale_in_progress_days: 14
    approved_operational_maintenance_marker: "<label-or-rule>"
    minimum_observability:
      source: 1.0
      disposition: 1.0
      done_evidence: 0.95
    evidence_access_limitations: "<known-limitations>"
    prompt_injection_reporting_destination: "<report-section-or-security-channel>"

  prior_report_comparison:
    lookup_location: "<exact-location>"
    title_pattern: "Governance Audit | <project-key> | YYYY-MM"
    existing_period_behavior: "update-existing-report"
    ruleset_compatibility: "<same-ruleset-or-explicit-migration>"
```

## Integrity algorithm

1. Parse the YAML block.
2. Serialize only the value of the top-level `profile` mapping as canonical JSON using UTF-8, lexicographically sorted object keys, no insignificant whitespace, JSON booleans/null, and arrays in declared order.
3. Compute SHA-256 over those canonical JSON bytes.
4. Require the lowercase hexadecimal digest to equal `approval.approved_profile_body_sha256`.
5. Require `profile_revision`, `approved_by`, `approved_at`, `approval_record`, `allowed_editors`, and `maximum_profile_age_days` to be present.
6. When the connector exposes the current editor or document revision, require the editor to be allowed and the revision to match the approved revision. When scheduled execution cannot verify required approval metadata, stop rather than treating the profile as approved.
7. Stop when the approval is older than `maximum_profile_age_days`, unless a newer approval record explicitly renews it.

Any change inside `profile` requires a new revision, new body hash, new approval timestamp, and new approval record. Automation must not silently accept a changed profile.

## Period resolution

- `previous-calendar-month`: calculate the first and last instant of the previous calendar month in `profile.identity.timezone` on every run.
- `fixed-range`: require `fixed_start` and `fixed_end` and never move them automatically.
- `release-candidate-scope`: resolve the exact candidate from `software_evidence.candidate_scope`; do not infer a release candidate.

Write the resolved absolute start, end, timezone, and rule into every report.

## Configuration gate

Stop with a configuration error when:

- YAML parsing fails or placeholders remain;
- profile integrity, approval, editor, revision, or age cannot be verified as required;
- any Linear target, mapping, timezone, period rule, collection rule, report destination, data-flow policy, or authorization boundary is unresolved;
- `single-project` mode does not map both semantic roles to the intended project;
- a weaker observability threshold than the bundled minimum is supplied.

Do not broaden scope, infer mappings, downgrade classification, or copy content by guessing.
