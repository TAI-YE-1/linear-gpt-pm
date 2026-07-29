# Audit Project Profile

Copy this template into an accessible project document or embed the completed values in the Codex Automation instruction. Replace every required placeholder before scheduling an audit.

## Identity and versions

- Profile schema version: `2`
- Project key: `<stable-short-key>`
- Project name: `<exact-project-name>`
- Timezone: `<IANA-timezone>`
- Accountable owner: `<person-or-role>`
- Last reviewed: `<YYYY-MM-DD>`
- Governance ruleset version: `<version>`
- Audit ruleset version: `<version>`

## Linear structure

- Team or workspace: `<exact-team-or-workspace>`
- Structure mode: `<single-project-or-dual-project>`
- Governance project: `<exact-name-or-id>`
- Delivery project: `<exact-name-or-id; may equal governance project in single-project mode>`
- Governance type label mapping: `<semantic-type=exact-label>`
- Execution type label mapping: `<semantic-type=exact-label>`
- Status mapping: `<semantic-state=exact-status>`
- Source field heading: `<exact-heading>`
- Native source relation: `<relatedTo-or-approved-fallback>`
- Authoritative governance document: `<exact-document-location>`

## Report destination and write authority

- Audit report destination: `<document-project-issue-or-status-update-target>`
- Destination audience and data classification: `<classification>`
- Authorized audit writes: `<exact-report-document-comment-or-status-update>`
- Prohibited writes: `formal requirements, change approvals, risk acceptance, business closure, destructive cleanup, CI reruns, merges, deployments`

## Data-flow policy

- Source classifications: `<Linear/GitHub/documents/logs classifications>`
- Allowed source-to-destination flows: `<rules>`
- Copy policy: `<link-only-summary-redacted-excerpt-or-prohibited>`
- Required redactions: `<secrets-personal-data-code-security-details-or-other>`
- Maximum quoted content: `<limit>`
- Allowed linked domains or evidence systems: `<exact list>`

## Optional software evidence

- Repositories: `<owner/repository, one per line or none>`
- Default branches: `<repository=branch>`
- In-scope pull requests, release, or candidate commit: `<rule-or-none>`
- Deployment or runtime evidence systems: `<exact sources-or-none>`

## Audit period and collection

- Current audit period: `<start-and-end>`
- Active-item scope: `<all-active-or-explicit-filter>`
- Done evidence lookback: `<number-of-days-or-explicit-release-scope>`
- Changed-item lookback: `<number-of-days>`
- Historical baseline treatment: `<rules>`
- Expected item counts or count source: `<method>`
- Pagination or cursor strategy: `<method>`
- Required comment/document/relation access: `<requirements>`
- Maximum acceptable collection gap: `0 for project-wide source and disposition conclusions`

## Audit policy

- Stale In Progress threshold: `<number-of-days>`
- Approved operational-maintenance exception marker: `<label-or-rule>`
- Core observability thresholds: `source=100%, disposition=100%, Done evidence>=95% unless stricter values are declared`
- Evidence access limitations: `<known-limitations>`
- Prompt-injection reporting destination: `<report-section-or-security-channel>`

## Prior-report comparison

- Prior report lookup location: `<exact-location>`
- Valid report title pattern: `Governance Audit | <project-key> | YYYY-MM`
- Stable exception key: `project-key + item-id + rule-id + evidence-scope`
- Existing-period behavior: `update the same period's report; do not create a duplicate`
- Ruleset compatibility rule: `<same-ruleset-or-explicit-migration>`

## Configuration gate

Stop with a configuration error when any required Linear target, structure mapping, timezone, audit period, collection rule, report destination, data-flow policy, or authorization boundary is unresolved.

Do not broaden scope, infer mappings, downgrade classification, or copy content by guessing.