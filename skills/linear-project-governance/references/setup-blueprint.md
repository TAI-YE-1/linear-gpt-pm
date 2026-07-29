# Linear Governance Setup Blueprint

## Purpose

Provide a deterministic, repeatable baseline for adapting a Linear workspace without silently overwriting existing structures.

## Standard structure

When separation is useful, prefer two projects:

- `<Project>｜需求与决策`
- `<Project>｜执行与交付`

The first project contains `REQ`, `PROB`, `DEC`, `CR`, `RISK`, and `Q`. The second contains Analysis, Implementation, Validation, and Collaboration tasks.

## Labels

Prefer two label groups when the workspace supports grouped labels:

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

Labels are the authoritative machine-readable classification. A title prefix such as `[REQ]` is recommended for human scanning but must not become a second identifier system.

## Status mapping

Reuse the workspace's existing statuses when they can be mapped to:

- Backlog
- Todo
- In Progress
- In Review
- Done
- Canceled
- Duplicate

Do not create near-duplicate statuses merely to match spelling. Record the chosen mapping in an accessible governance document.

## Baseline documents

Recommend the following documents or equivalent accessible records:

- governance standard;
- issue and execution templates;
- project baseline and authoritative sources;
- audit rules and report destination.

Raw facts and evidence remain in descriptions, comments, documents, or links. Do not create a separate `FACT` issue type.

## Idempotent setup sequence

1. Read current projects, labels, statuses, documents, active items, and naming conventions.
2. Produce a diff between the current workspace and this blueprint.
3. Reuse exact semantic matches even when names differ slightly.
4. Present every proposed creation, update, relation, or structural change.
5. Execute only the explicitly confirmed scope.
6. Create missing objects only; never recreate an object that already satisfies the same role.
7. Read back every affected object and verify names, states, labels, and relations.
8. Report created, reused, skipped, conflicted, and failed objects separately.

## Conflict handling

- Same name, different meaning: stop and request a naming decision.
- Same meaning, different name: reuse and document the mapping.
- Duplicate labels or projects: do not create another duplicate; propose consolidation for human approval.
- Unsupported parent relation across projects: use `relatedTo` instead.
- Partial write failure: do not claim setup completed; report the exact completed subset and safe resume point.

## Destructive boundaries

Never delete, archive, merge, rename, or migrate existing projects, labels, statuses, issues, or documents unless the user explicitly identifies the exact targets and authorizes that action.
