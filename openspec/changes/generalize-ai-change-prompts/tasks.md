# Tasks: Generalize AI Change Prompts

## Implementation Tasks

- [x] Add regression tests for generated prompt file references with a custom `-OutputPrefix`.
- [x] Add regression tests that generated generic prompts do not contain assessment-specific wording.
- [x] Update `scripts/new-ai-change-prompt.ps1` to replace generated prompt file/path placeholders.
- [x] Update `docs/prompts/*.md` to use generated prompt placeholders for stage transitions.
- [x] Remove assessment-specific and project-specific wording from generic prompt templates.
- [x] Update `docs/ai-sop-usage.md` to describe generic prompt generation.
- [x] Rebuild `scripts/bootstrap-ai-sop.ps1` embedded assets.
- [x] Run prompt generator verification.
- [x] Run project tests.
- [x] Run OpenSpec validation.
- [x] Review `git status --short` and `git diff --stat`.

## Guardrails

- [x] Do not modify business CLI behavior.
- [x] Do not modify global skills.
- [x] Do not leave temporary generated prompt files in the repository.
- [x] Do not add unnecessary dependencies.
