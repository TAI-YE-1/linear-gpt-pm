# Changelog

## 0.1.0-alpha.2 - 2026-07-29

- Added a machine-readable project profile schema v3 with approval identity, revision, canonical body SHA-256, allowed editors, and expiry checks.
- Added rolling `previous-calendar-month`, fixed-range, and release-candidate audit period rules.
- Changed health evaluation to confidence-first: incomplete configuration, collection, or snapshots force project-wide health to `Unknown`.
- Added a minimum evidence matrix for code, documentation, configuration, deployment, research, operational, and validation deliverables.
- Added canonical evidence-scope normalization and SHA-256-based stable exception IDs.
- Added collection start/finish timestamps and snapshot-consistency rechecks.
- Added immutable governance operation plans with Plan IDs and confirmation hashes.
- Enforced LF source files, exact PyYAML pinning, Python 3.11.9 CI, ZIP_STORED archives, and workflow concurrency.
- Changed installation guidance from moving `main` paths to an immutable commit reference and documented clean upgrades.

## 0.1.0-alpha.1 - 2026-07-29

- Rebuilt the repository as two self-contained Agent Skills.
- Added human-confirmed Linear governance and read-only-first delivery audit workflows.
- Added deterministic setup, classification, source, evidence, metric, health, and exception-identity rules.
- Added prompt-injection resistance, project isolation, cross-system data-flow controls, pre-write concurrency checks, and idempotent creation rules.
- Added single/dual-project mappings, pagination and collection-completeness gates, audit windows, and prior-report comparison.
- Bundled monthly and pre-release automation instructions inside the audit Skill.
- Added complete standalone licenses, ruleset identity, reproducible ZIP packaging, SHA-256 checksums, and persisted CI artifacts.
- Added the OpenAI Codex Skill `quick_validate.py` baseline pinned to commit `fe01054a28fa4bd04716d9ceadb410f2443a50ce` plus repository-specific validation.
- Removed the previous Codex × Superpowers × OpenSpec package from the active tree.

## Stability note

This remains an alpha release. Static source and distribution validation are implemented. Stable `1.0.0` requires retained evidence for real Codex installation, approved Linear writes, Linear/GitHub connector behavior, scheduled period rolling and idempotent reports, supported ChatGPT/workspace upload, and reuse in a second project.
