# Tasks: Add AI Builder Pack Maker

## Implementation Tasks

- [x] Confirm the repository layout and choose the minimal Python CLI entry point.
- [x] Add a failing test or verification fixture for generating all four Markdown outputs from `inputs/problem_pack.md`.
- [x] Implement local UTF-8 input loading with clear errors for missing or empty input.
- [x] Implement deterministic Markdown section extraction or source-content fallback.
- [x] Implement `one_page_summary.md` generation.
- [x] Implement `recording_script.md` generation.
- [x] Implement `defense_qa.md` generation.
- [x] Implement `materials_index.md` generation.
- [x] Ensure `outputs/latest/` is created automatically and generated files are overwritten on each run.
- [x] Add or update command documentation for running the generator locally.
- [x] Run the local generator against `inputs/problem_pack.md`.
- [x] Verify the four required files exist and are non-empty.
- [x] Run project tests or the minimal verification command.
- [x] Run `openspec validate add-ai-builder-pack-maker --strict`.

## Non-Implementation Guardrails

- [x] Do not add model API integration.
- [x] Do not add a web UI.
- [x] Do not add database dependencies.
- [x] Do not add Feishu integration.
- [x] Do not write implementation code until this OpenSpec change validates.
