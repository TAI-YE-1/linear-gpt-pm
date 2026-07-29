# Reuse Guide

The Skills are project-independent. Reuse should require changing the approved project baseline and Profile Schema v3, not editing Skill rules.

## Inputs per project

Provide:

- project key, name, purpose, timezone, and accountable owner;
- single- or dual-project structure mode;
- exact Linear project targets;
- semantic governance/execution label mappings;
- semantic status mappings;
- configured structured source heading and native relation convention;
- decision authority and review cadence;
- data classifications and allowed source-to-destination flows;
- optional software repositories and evidence systems;
- audit period rule, lookback windows, pagination/count strategy, snapshot strategy, and staleness threshold;
- report destination and exact authorized writes;
- approved operational exceptions.

Record these values in the authoritative governance mapping and the canonical YAML block in `skills/linear-delivery-audit/templates/project-profile.md`.

## Profile approval

Before scheduled use:

1. assign a stable profile ID and revision;
2. calculate the canonical profile-body SHA-256;
3. record approver, approval timestamp, approval record, allowed editors, and maximum age;
4. store the profile at an exact revisioned location;
5. configure Automation with the expected profile ID, revision, hash, and approval record;
6. require reapproval after any profile-body change or schema migration.

## Recommended adoption

1. Install both Skills from the same immutable commit or validated archive set.
2. Inspect the existing structure and permissions.
3. Map semantic roles before creating anything.
4. Adapt rather than overwrite.
5. Run one real intake without writing.
6. Confirm one low-risk immutable Plan ID and execute it with pre-write re-reading.
7. Run one manual audit with complete pagination, snapshot-consistency, and profile-integrity evidence.
8. Correct project-specific mappings in the project's own documents/profile, not in shared Skill source.
9. Configure monthly Automation only after the manual workflow and data-flow policy are stable.
10. Test period rolling and same-period idempotent reruns.

## Evidence of successful reuse

A second project should use the same immutable Skill package/ruleset versions without source edits. Only the approved profile, mappings, targets, evidence systems, security policy, audit periods, and cadence should differ.

Retain runtime evidence using `tests/runtime-smoke-template.md`, including installation commit/archive hashes, profile approval/hash, Plan ID, collection snapshot, rolling period calculation, and idempotent rerun result.
