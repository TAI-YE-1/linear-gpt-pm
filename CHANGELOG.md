# Changelog

## Unreleased

- Repositioned the public README as an AI project-governance toolkit centered on Linear, optional GitHub evidence, and human-confirmed decisions.
- Added public badges, quick navigation, 60-second usage examples, maturity boundaries, and adoption guidance.
- Reworked the quickstart into a five-minute install, first governance run, first read-only audit, and optional scheduled-audit path.
- Expanded the integration guide with Linear, GitHub, Codex, permission, degraded-operation, and data-flow guidance.
- Added a public, redacted Infinite Canvas case study showing real Linear projects, governance items, delivery tasks, risks, and GitHub evidence semantics.
- Reworked the reuse guide into phased adoption steps and a project migration checklist.
- Expanded the contribution guide for bug reports, connector differences, test scenarios, public examples, and security boundaries.

These documentation changes do not change the frozen `0.1.0-alpha.3` Skill package behavior.

## 0.1.0-alpha.3 - 2026-07-29

- Added a safe cross-platform local Codex installer with dry-run, backups, atomic replacement, and installation manifests.
- Added deterministic `plan_tool.py`; users confirm a short readable Plan ID while the full digest is verified internally.
- Added standard-library `profile_tool.py` to create, seal, validate, hash, and resolve Profile periods without manual SHA calculations.
- Replaced the advanced Profile workflow with JSON Profile Schema v4.
- Split usage into basic governance, quick read-only audit, repeatable manual audit, and advanced scheduled audit paths.
- Made persistent Profiles optional for one-time read-only audits.
- Added unit tests for installation, Plan hashing, Profile hashing, validation, expiry, and rolling month resolution.
- Extended CI to compile tools, run unit tests, exercise CLI help paths, build archives, and run source/distribution validation.

## 0.1.0-alpha.2 - 2026-07-29

- Added machine-readable Profile Schema v3 with approval identity, revision, canonical body SHA-256, allowed editors, and expiry checks.
- Added rolling `previous-calendar-month`, fixed-range, and release-candidate audit period rules.
- Changed health evaluation to confidence-first: incomplete configuration, collection, or snapshots force project-wide health to `Unknown`.
- Added a minimum evidence matrix and SHA-256-based stable exception IDs.
- Added collection start/finish timestamps and snapshot-consistency rechecks.
- Added immutable governance operation plans.
- Enforced LF sources, exact validation dependency pinning, fixed Python CI, deterministic archives, and workflow concurrency.

## 0.1.0-alpha.1 - 2026-07-29

- Rebuilt the repository as two self-contained Agent Skills.
- Added human-confirmed Linear governance and read-only-first delivery audit workflows.
- Added deterministic setup, classification, source, evidence, metric, health, and exception rules.
- Added prompt-injection resistance, project isolation, cross-system data-flow controls, concurrency checks, and idempotent creation rules.
- Bundled monthly and pre-release automation instructions inside the audit Skill.
- Added standalone licenses, ruleset identity, reproducible ZIP packaging, checksums, CI artifacts, and a pinned OpenAI validation baseline.
- Removed the previous Codex × Superpowers × OpenSpec package from the active tree.

## Stability note

This remains an alpha release. Stable `1.0.0` requires retained evidence for real Codex installation, approved Linear writes, connector behavior, scheduled rolling/idempotent reports, supported ChatGPT/workspace upload, and reuse in a second project.
