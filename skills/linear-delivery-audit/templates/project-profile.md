# Audit Project Profile

Copy this template into an accessible project document or embed the completed values in the Codex Automation instruction. Replace every required placeholder before scheduling an audit.

## Identity

- Profile version: `1`
- Project key: `<stable-short-key>`
- Project name: `<exact-project-name>`
- Timezone: `<IANA-timezone>`
- Accountable owner: `<person-or-role>`
- Last reviewed: `<YYYY-MM-DD>`

## Linear scope

- Team or workspace: `<exact-team-or-workspace>`
- Governance project: `<exact-name-or-id>`
- Delivery project: `<exact-name-or-id>`
- Audit report destination: `<document-project-issue-or-status-update-target>`
- Included states: `<exact-state-names>`
- Excluded archived or historical scope: `<rules>`

## Optional software evidence

- Repositories: `<owner/repository, one per line or none>`
- Default branches: `<repository=branch>`
- In-scope pull requests or release: `<rule-or-none>`

## Audit policy

- Stale In Progress threshold: `<number-of-days>`
- Approved operational-maintenance exception marker: `<label-or-rule>`
- Evidence access limitations: `<known-limitations>`
- Authorized audit writes: `<report-document/comment/status-update only>`
- Prohibited writes: `formal requirements, change approvals, risk acceptance, business closure, destructive cleanup`

## Idempotency

- Report title pattern: `Governance Audit | <project-key> | YYYY-MM`
- Existing-report behavior: `update the same period's report; do not create a duplicate`

## Configuration gate

An automated audit must stop with a configuration error when any required Linear target, timezone, report destination, or authorization boundary is unresolved. It must not broaden scope by guessing.
