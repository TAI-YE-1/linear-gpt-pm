---
name: linear-project-governance
description: Convert real project communication into confirmed, traceable Linear requirements, problems, decisions, changes, risks, questions and execution tasks. Use for governance setup, intake, reconciliation and human-confirmed writes.
---

# Linear Project Governance

Use this Skill when the user needs to establish or operate a traceable project-governance workflow in Linear.

## Scope

This Skill handles:

- governance structure inspection and setup planning;
- intake from real chats, meetings, email, documents and feedback;
- classification into `REQ`, `PROB`, `DEC`, `CR`, `RISK`, `Q`;
- reconciliation against existing Linear records;
- execution-task decomposition into analysis, implementation, validation and collaboration;
- native Linear relations and dependency planning;
- human-confirmed creation or update of formal records.

It does not perform unattended monthly audits. Use `linear-delivery-audit` for that.

## Required operating sequence

1. Read the current source material and the relevant current Linear state.
2. Separate facts from actionable governance items.
3. Reconcile candidates with existing items before proposing new ones.
4. Present the proposed writes, updates and relationships.
5. Treat an explicit user instruction to perform those exact actions as confirmation. Otherwise wait for confirmation.
6. Execute only the confirmed scope.
7. Read back the affected records and report the verified result.

Never describe a planned write as completed.

## Classification

Read `references/standard.md` before classifying or writing.

Use exactly one formal type for each governance item:

- `REQ`: an accepted outcome, capability or constraint;
- `PROB`: a currently confirmed problem with impact;
- `DEC`: a decision that governs future work;
- `CR`: a material change to accepted scope, behavior or constraints;
- `RISK`: an uncertain event or condition requiring treatment;
- `Q`: an unresolved question blocking or changing a decision.

Raw facts, observations and evidence remain in descriptions, comments or documents unless they require a decision, owner, treatment or acceptance.

## Linear structure and setup

For setup or structural adaptation, read `references/setup-blueprint.md` in addition to the governance standard.

Prefer two projects when the organization benefits from separation:

- `<Project>｜需求与决策`
- `<Project>｜执行与交付`

Do not force this structure onto an existing workspace without first inspecting the current structure and presenting an adaptation diff. Setup must be idempotent: reuse semantic matches, create only confirmed missing objects, and report conflicts or partial completion precisely.

## Relationship rules

- Governance item ↔ execution task: `relatedTo`.
- Real dependency: `blocks` / `blockedBy`.
- Duplicate: `duplicateOf`.
- Parent/child only when the platform and project boundary support it and the child can be independently closed.
- Do not encode dependencies only in prose.

## Write safety

Before destructive, bulk or structural writes:

- enumerate targets;
- identify naming conflicts and duplicates;
- avoid deleting or archiving existing records unless explicitly requested;
- avoid partial claims if a multi-step operation fails;
- re-read results after every batch.

AI must not independently approve requirements, accept risks, approve change requests or declare business acceptance.

## Degraded operation

- No Linear connection: output candidates and an exact write plan only.
- Read-only Linear: perform reconciliation and produce suggested changes only.
- Missing source context: mark uncertainty and avoid inventing facts.
- Write failure: report what succeeded, what failed and what remains unchanged.

## Output

For intake, use:

```text
Type:
Title:
Source:
Current evidence:
Decision or acceptance needed:
Proposed execution:
Proposed relations:
Confidence / uncertainty:
```

For confirmed writes, report:

- created or updated identifiers;
- verified states and relations;
- skipped or failed actions;
- remaining human decisions.

Use the templates and examples in this Skill directory when useful.
