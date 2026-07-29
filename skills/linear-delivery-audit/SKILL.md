---
name: linear-delivery-audit
description: Verify delivery evidence and audit Linear project governance. Use for orphan-task checks, Done evidence validation, change propagation, stale work, status conflicts, GitHub evidence checks, periodic reports and pre-release audits.
---

# Linear Delivery Audit

Use this Skill for independent evidence verification and reverse project audits.

## Default trust boundary

Operate read-only by default.

An interactive user or approved automation may explicitly permit writing only:

- an audit report document;
- an audit Issue;
- an audit comment;
- a project status update.

Do not automatically modify formal requirements, approve change requests, accept risks, close business items, delete records or declare business acceptance.

## Configuration gate

For interactive audits, resolve exact scope with the user or current project context. For scheduled audits, require a completed profile based on `templates/project-profile.md`.

A scheduled audit must stop with a configuration error rather than guess when any required Linear target, timezone, report destination, or write boundary is unresolved.

## Required sequence

1. Resolve the audit scope, current timestamp, timezone, authoritative projects, report destination, and allowed writes.
2. Read all in-scope active governance items, execution tasks, states, labels, owners, descriptions, comments and native relations.
3. For software delivery claims, read available GitHub branch, PR, commit and test evidence.
4. Apply the checks and deterministic metric rules in `references/audit-standard.md`.
5. Distinguish confirmed exceptions from missing evidence, unavailable evidence, and uncertainty.
6. Produce a stable report with identifiers, metric counts, evidence and suggested actions.
7. Write the report only when explicitly requested or when the automation profile already authorizes that exact report destination.
8. Read back any written report and disclose failures.

## Audit checks

At minimum check:

- execution tasks without a governance source;
- active REQ or PROB without disposition or related execution;
- Done tasks without delivery evidence;
- material CR not propagated to affected tasks;
- canceled governance items with active dependent work;
- answered Q items still open;
- missing owners or unclear next actions;
- stale In Progress work;
- blocked work without an identifiable blocker;
- probable duplicates;
- oversized tasks that cannot be independently verified;
- Linear completion claims that conflict with available GitHub evidence.

## Evidence discipline

Do not infer code delivery from a title or branch name alone. Prefer, in order:

1. current repository and PR metadata;
2. commit and changed-file evidence;
3. test or check results tied to the current commit;
4. deployment or runtime evidence;
5. Linear comments or user statements.

A lower-ranked source may explain intent but must not override stronger contradictory evidence.

## Degraded operation

- No Linear access: audit only user-provided records and state the limitation.
- No GitHub access: audit Linear structure and evidence completeness, but do not claim code verification.
- Missing comments or attachments: mark evidence as unavailable rather than absent when the connector cannot retrieve them.
- Conflicting evidence: report the conflict and avoid a pass/fail claim until resolved.
- Insufficient scope or observability: return `Unknown` health rather than inventing a percentage or conclusion.

## Output

Use the report template in this Skill directory.

Every exception must contain:

- severity;
- item identifier;
- violated rule;
- evidence;
- consequence;
- suggested human action.

Conclude with:

- project health summary and deterministic metric counts;
- new exceptions;
- unresolved prior exceptions;
- resolved exceptions;
- human decisions required;
- limitations and observability of the audit.
