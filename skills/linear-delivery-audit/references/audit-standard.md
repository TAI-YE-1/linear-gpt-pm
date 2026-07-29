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

## Deterministic metric definitions

Use the completed project profile to determine scope. Report both numerator and denominator, not only a percentage.

### Eligible execution tasks

Include execution tasks in Backlog, Todo, In Progress, In Review, or Done. Exclude Canceled and Duplicate tasks. Exclude operational-maintenance tasks only when the project profile defines an explicit approved marker.

### Source coverage

`source coverage = eligible execution tasks with at least one valid governance relation / eligible execution tasks`

A valid source relation points to an in-scope `REQ`, `PROB`, `DEC`, `CR`, `RISK`, or `Q`. A prose-only reference does not count when native relations are available.

### Eligible governance items

Include in-scope governance items in Backlog, Todo, In Progress, or In Review. Exclude Done, Canceled, and Duplicate items from disposition coverage.

### Disposition coverage

`disposition coverage = eligible governance items with an owner and a recorded next action, accepted disposition, related execution, or explicit backlog rationale / eligible governance items`

### Done evidence coverage

`Done evidence coverage = observable Done execution tasks with sufficient evidence / observable Done execution tasks`

A Done task is observable when the audit can access the evidence channels required by the claim. If a connector cannot retrieve a required attachment or repository, classify the task as `Unknown`, exclude it from this denominator, and report observability separately. Do not treat unavailable evidence as confirmed absence.

### Observability

`observability = eligible items with sufficient accessible data for the relevant check / eligible items for that check`

Always report observability when exclusions caused by missing capabilities affect a coverage metric.

### Empty and rounding rules

- A zero denominator produces `N/A`, not 100%.
- Show raw counts as `numerator/denominator`.
- Round percentages to one decimal place.
- Keep exclusions and Unknown items visible in the limitations section.

## Overall health mapping

Apply this deterministic order:

1. `Off track`: at least one confirmed Critical exception.
2. `At risk`: no Critical exception, but at least one confirmed High exception, or any calculated core coverage metric is below 90.0% with a denominator of at least 5.
3. `On track`: no Critical or High exception, all calculated core coverage metrics are at least 90.0%, and core observability is sufficient for the stated conclusion.
4. `Unknown`: required scope, core Linear data, or observability is insufficient to apply the rules above.

Do not downgrade or upgrade health based only on formatting issues. Explain every health result using exact exceptions and metric counts.

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
