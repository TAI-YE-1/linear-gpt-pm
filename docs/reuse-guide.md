# Reuse Guide

The Skills are project-independent. Reuse should require changing the project baseline and completed profile, not editing Skill rules.

## Inputs per project

Provide:

- project key, name, purpose, timezone, and accountable owner;
- single- or dual-project structure mode;
- exact Linear project targets;
- semantic governance/execution label mappings;
- semantic status mappings;
- structured source heading and native relation convention;
- decision authority and review cadence;
- data classifications and allowed source-to-destination flows;
- optional software repositories and evidence systems;
- audit period, lookback windows, pagination/count strategy, and staleness threshold;
- report destination and exact authorized writes;
- explicit exceptions such as approved operational maintenance.

Record these values in the authoritative governance mapping and `skills/linear-delivery-audit/templates/project-profile.md`.

## Recommended adoption

1. Inspect the existing structure and permissions.
2. Map semantic roles before creating anything.
3. Adapt rather than overwrite.
4. Run one real intake without writing.
5. Confirm and execute one low-risk write with pre-write re-reading.
6. Run one manual audit with collection-completeness evidence.
7. Correct project-specific mappings in the project's own documents and profile, not in shared Skill source.
8. Configure Automation only after the manual workflow and data-flow policy are stable.

## Evidence of successful reuse

A second project should use the same installed Skill package and ruleset versions without source edits. Only the completed mappings, targets, evidence systems, security policy, audit windows, and cadence should differ.

Retain the runtime evidence using `tests/runtime-smoke-template.md`.