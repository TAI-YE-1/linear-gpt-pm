# Governance Standard

## Purpose

Create a single, traceable chain from real input to formal governance, execution and evidence without allowing AI to silently redefine business intent.

## Item definitions

### REQ

Use when an outcome, capability, constraint or acceptance condition has been explicitly accepted. A proposed idea is not automatically a REQ.

Minimum content:

- current accepted content;
- source evidence;
- owner or decision authority;
- acceptance criteria;
- current disposition.

### PROB

Use only when the problem is currently confirmed. Historical reports that have not been reproduced on the current version should normally be `Q` or an investigation task.

Minimum content:

- observable behavior;
- impact;
- environment or scope;
- reproduction or evidence status;
- treatment.

### DEC

Records a governing choice and its rationale. Completed decisions can be Done while related implementation remains open.

### CR

Use for material changes to accepted scope, behavior, interfaces, constraints or acceptance criteria. Do not silently overwrite a REQ when downstream work may be affected.

### RISK

Records uncertainty, probability or impact, treatment, owner and review condition. AI cannot accept the risk on behalf of the accountable owner.

### Q

Records an unresolved question whose answer may change decisions or execution. Close only after the answer and its consequences are recorded.

## Execution-task types

- Analysis: investigation, design or decision support.
- Implementation: build or change the product/process.
- Validation: independently verify acceptance and evidence.
- Collaboration: obtain access, decisions, data or coordination.

## State gates

- Backlog: valid but not committed for near-term action.
- Todo: ready enough to start and has an owner or clear next action.
- In Progress: active work with current responsibility.
- In Review: delivery exists and awaits technical or business review.
- Done: task completion evidence exists; for governance items, the relevant decision or acceptance is recorded.
- Canceled: intentionally stopped with reason and impact recorded.
- Duplicate: points to the authoritative item.

A Done execution task never automatically closes its source REQ or PROB.

## Evidence standard

Useful evidence includes:

- current source document or user confirmation;
- Linear description/comment history;
- PR, commit, test result or deployment record;
- screenshot, log or reproducible observation;
- acceptance record from an accountable human.

Evidence should be linked or summarized in the authoritative record. Do not rely on inaccessible local paths or ephemeral chat context alone.

## AI boundaries

AI may classify, propose, reconcile, create confirmed records and verify structure.

AI may not independently:

- approve business scope;
- accept risk;
- approve a material change;
- claim deployment or tests passed without evidence;
- delete records because they look obsolete;
- convert uncertainty into a confirmed problem.
