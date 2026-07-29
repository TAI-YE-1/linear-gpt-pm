# Linear Governance Setup Blueprint

## Purpose

Create a deterministic, repeatable baseline without silently overwriting an existing Linear workspace.

## Semantic roles

Use semantic roles as the standard. Localize names to the user's language and existing workspace conventions.

- Governance project: accepted requirements, confirmed problems, decisions, material changes, risks, and unresolved questions.
- Delivery project: analysis, implementation, validation, and collaboration work.

Examples only:

- Chinese: `<Project>｜需求与决策`, `<Project>｜执行与交付`
- English: `<Project> | Governance`, `<Project> | Delivery`

Do not require either language or delimiter.

## Structure modes

### Dual-project

Use separate Governance and Delivery projects when separation improves ownership, reporting, permissions, or lifecycle management.

### Single-project

Use one project when the existing workspace already manages both categories effectively. Distinguish governance and execution using explicit label mappings. The audit profile must identify `single-project` mode and may point both semantic roles to the same project.

Do not create a second project merely to match this blueprint.

## Classification labels

Prefer two semantic label groups when the workspace supports them.

### Governance item type

- `REQ`
- `PROB`
- `DEC`
- `CR`
- `RISK`
- `Q`

### Execution task type

- `Analysis`
- `Implementation`
- `Validation`
- `Collaboration`

Map existing localized labels to these semantic roles instead of creating near-duplicates. Labels are the authoritative machine-readable classification. A title prefix such as `[REQ]` is optional for human scanning and must not become a second identifier system.

## Status mapping

Map existing statuses to these semantic states:

- Backlog
- Todo
- In Progress
- In Review
- Done
- Canceled
- Duplicate

Do not create duplicate statuses merely to match spelling. Record the exact mapping in an accessible governance document and in the audit project profile.

## Source convention

For each execution task:

1. Record the authoritative governance item ID in a structured `Source` section.
2. Add a native `relatedTo` relation to the same item when supported.
3. Treat the source as verified only when the structured field and relation agree.
4. If the platform cannot support a native relation, define one explicit fallback in the project profile and report the limitation.

Use `blocks` or `blockedBy` only for real dependencies and `duplicateOf` only for duplicates.

## Baseline documents

Recommend these accessible records or equivalents:

- governance standard and ruleset version;
- issue and execution templates;
- semantic project, label, and status mappings;
- authoritative sources and decision owners;
- source relation convention;
- security and cross-system data-flow policy;
- audit profile, rules, window, and report destination.

Keep raw facts and evidence in descriptions, comments, documents, or links. Do not create a separate `FACT` issue type.

## Idempotent setup sequence

1. Read current projects, labels, statuses, documents, active items, naming conventions, and available update timestamps.
2. Produce a semantic diff between the current workspace and this blueprint.
3. Reuse exact semantic matches even when names differ.
4. Present every proposed creation, update, relation, mapping, or structural change.
5. Record the baseline identifiers and versions used for the proposal.
6. Execute only the explicitly confirmed scope.
7. Immediately before each write batch, re-read targets and stop on relevant concurrent changes.
8. Create missing objects only; never recreate an object that already satisfies the same role.
9. Before retrying an uncertain create, search for the intended semantic role and stable creation key.
10. Read back every affected object and verify names, states, labels, mappings, and relations.
11. Report created, reused, skipped, conflicted, failed, and unchanged objects separately.

## Stable creation keys

When an external source identifier exists, use a stable key based on:

```text
semantic type + normalized source system + external source identifier
```

When no external identifier exists, use:

```text
semantic type + normalized authoritative source reference + normalized accepted title
```

Never assume a timed-out create failed. Search before retrying.

## Conflict handling

- Same name, different meaning: stop and request a naming decision.
- Same meaning, different name: reuse and document the mapping.
- Duplicate labels or projects: do not create another duplicate; propose consolidation for human approval.
- Unsupported parent relation across projects: use `relatedTo` instead.
- Structured Source and native relation disagree: stop the affected closeout or audit pass and request correction.
- Target changed after proposal: stop the affected write and display the baseline-to-current difference.
- Partial write failure: do not claim setup completed; report the exact completed subset and safe resume point.

## Destructive boundaries

Never delete, archive, merge, rename, or migrate existing projects, labels, statuses, issues, or documents unless the user identifies exact targets and explicitly authorizes that action.