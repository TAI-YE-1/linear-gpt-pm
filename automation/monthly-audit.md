# Monthly Governance Audit

## Purpose

Configure a Codex Automation to invoke `linear-delivery-audit` once per month with an explicit, stable scope.

## Before scheduling

Complete `skills/linear-delivery-audit/templates/project-profile.md` and either:

- store the completed profile in a document the automation can read; or
- embed all completed profile values directly in the automation instruction.

Do not leave placeholders unresolved.

## Recommended schedule

Run monthly during normal working hours in the accountable team's declared IANA timezone. The schedule is configured in Codex Automation, not by this repository.

## Automation instruction

```text
Use the linear-delivery-audit Skill.

Read the completed audit project profile at: <exact accessible profile location or embedded profile>.

Before auditing, verify the exact Linear governance project, delivery project, timezone, report destination, optional GitHub repositories, staleness threshold, exception marker, and authorized report writes. If any required value is unresolved, stop with a configuration error. Do not guess or broaden scope.

Audit only the profile's configured Linear scope. Read in-scope issues, states, labels, owners, descriptions, comments and native relations. For software projects, also read only the configured GitHub repositories and current PR/commit/test evidence when available.

Apply the deterministic checks and metric formulas defined by linear-delivery-audit. Report raw numerator/denominator counts, N/A cases, Unknown items, observability, and the evidence behind overall health.

Generate an idempotent report named "Governance Audit | <project-key> | YYYY-MM" in the exact authorized destination. If a report for the same project and month already exists, update it rather than creating a duplicate.

The report must include exact item identifiers, evidence, severity, consequences, suggested human actions and audit limitations.

Do not modify formal requirements, approve changes, accept risks, close business items, delete records or declare business acceptance. If report write access is unavailable, return the report without claiming it was written.
```

## Required proof before relying on automation

- one successful manual audit using the same completed profile;
- one successful scheduled run or saved schedule configuration;
- a retrievable idempotent report;
- confirmation that prohibited business mutations did not occur.
