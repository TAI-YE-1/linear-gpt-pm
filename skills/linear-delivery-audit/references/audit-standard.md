# Audit and Evidence Standard

## Severity

- Critical: false completion, destructive conflict, security/compliance exposure or release-blocking evidence gap.
- High: active work lacks source, material change is not propagated, or required validation is missing.
- Medium: ownership, staleness, duplication or traceability weakness that can degrade delivery.
- Low: formatting, clarity or maintenance issue without immediate delivery impact.

## Core rules

### Source coverage

Every execution task must relate to at least one current `REQ`, `PROB`, `DEC`, `CR`, `RISK` or `Q`, unless explicitly marked as approved operational maintenance.

### Disposition coverage

Every active governance item must have an owner, next decision/action, accepted disposition or explicit backlog rationale.

### Done evidence

A Done task requires evidence appropriate to the deliverable. A description that says "completed" is not evidence by itself.

### Change propagation

A material CR must identify affected governance items, execution tasks, tests, documentation and release conditions. Open work using the old baseline is an exception.

### Cancellation consistency

Canceled source items must not retain active dependent work without an explicit reason.

### Question closure

A Q closes only after the answer, authority and downstream impact are recorded.

### Staleness

Use the project's own cadence when available. Otherwise flag In Progress items with no meaningful update for 14 days as candidates for review, not automatic failures.

### Duplicates and oversized work

Flag probable duplicates for human confirmation. Flag tasks whose deliverable and verification cannot be independently stated.

## GitHub verification

For software projects, compare Linear claims with:

- current branch and commit;
- PR status and target branch;
- changed files or patch scope;
- checks and tests associated with the claimed commit;
- explicit deployment/runtime evidence when deployment is claimed.

Do not run CI or merge code merely to complete an audit unless separately authorized.

## Stable reporting

Use deterministic ordering:

1. severity;
2. project;
3. item identifier;
4. rule name.

Use exact identifiers and timestamps. Separate facts from inference.
