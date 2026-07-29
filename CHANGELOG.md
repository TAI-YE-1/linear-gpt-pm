# Changelog

## 1.0.2 - 2026-07-29

- Aligned `agents/openai.yaml` with the current OpenAI Skill interface schema.
- Removed the unsupported legacy `policy` block from both Skills.
- Added validation for quoted interface values, Skill references and UI description length.

## 1.0.1 - 2026-07-29

- Restored the complete Apache-2.0 license and added standalone `LICENSE.txt` files to both Skills.
- Added Skill UI metadata under `agents/openai.yaml`.
- Added an idempotent Linear setup blueprint and conflict-handling rules.
- Added an explicit audit project profile for scheduled automation.
- Defined deterministic coverage, observability and project-health calculations.
- Strengthened source, reference, archive and checksum validation.
- Added a lightweight GitHub Actions validation workflow.
- Clarified that runtime installation, connector access and scheduled execution require separate smoke evidence.

## 1.0.0 - 2026-07-29

- Rebuilt the repository as a reusable Agent Skills toolkit.
- Added `linear-project-governance` for human-confirmed governance writes.
- Added `linear-delivery-audit` for evidence verification and reverse audits.
- Added Codex Automation templates, integration boundaries, examples, validation and ZIP packaging.
- Removed the previous Codex × Superpowers × OpenSpec workflow package from the active tree.
