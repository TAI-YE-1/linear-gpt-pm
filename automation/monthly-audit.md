# Monthly Governance Audit

## Purpose

Configure a Codex Automation to invoke `linear-delivery-audit` once per month.

## Recommended schedule

Run monthly during normal working hours in the accountable team's timezone. The schedule is configured in Codex Automation, not by this repository.

## Automation instruction

```text
Use the linear-delivery-audit Skill.

Audit the configured Linear governance and delivery projects. Read active issues, states, labels, owners, descriptions, comments and native relations. For software projects, also read the configured GitHub repository and current PR/commit/test evidence when available.

Check source coverage, disposition coverage, Done evidence, change propagation, cancellation consistency, answered questions, ownership, staleness, blockers, probable duplicates, oversized tasks and Linear/GitHub conflicts.

Generate an idempotent monthly report named "Governance Audit | YYYY-MM". If a report for the same month already exists, update it rather than creating a duplicate.

The report must include exact item identifiers, evidence, severity, consequences, suggested human actions and audit limitations.

Do not modify formal requirements, approve changes, accept risks, close business items, delete records or declare business acceptance. If report write access is unavailable, return the report without claiming it was written.
```

## Required proof before relying on automation

- one successful manual audit;
- one successful scheduled run or saved schedule configuration;
- a retrievable report;
- confirmation that prohibited business mutations did not occur.
