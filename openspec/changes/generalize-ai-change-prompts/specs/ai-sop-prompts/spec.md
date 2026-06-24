# AI SOP Prompts Spec

## ADDED Requirements

### Requirement: Generated prompt stage references point to generated files

`scripts/new-ai-change-prompt.ps1` SHALL generate prompt content whose stage transition instructions reference the actual generated prompt files for the selected `-OutputPrefix`.

#### Scenario: Default output prefix

- **GIVEN** the user runs `scripts/new-ai-change-prompt.ps1` without `-OutputPrefix`
- **WHEN** the script generates prompt files
- **THEN** generated stage instructions reference `current-01-propose.md`, `current-02-subagent-plan.md`, `current-03-apply.md`, `current-04-verify.md`, and `current-05-review-archive.md`

#### Scenario: Custom output prefix

- **GIVEN** the user runs `scripts/new-ai-change-prompt.ps1 -OutputPrefix sprint-a`
- **WHEN** the script generates prompt files
- **THEN** generated stage instructions reference `sprint-a-01-propose.md`, `sprint-a-02-subagent-plan.md`, `sprint-a-03-apply.md`, `sprint-a-04-verify.md`, and `sprint-a-05-review-archive.md`
- **AND** generated stage instructions do not hardcode `current-*`

### Requirement: Prompt templates are generic workflow assets

Prompt templates under `docs/prompts` SHALL avoid project-specific or assessment-specific deliverable requirements unless they are expressed as optional user-provided requirements.

#### Scenario: Review/archive prompt is generic

- **GIVEN** a generated review/archive prompt
- **WHEN** the user reads the archive instructions
- **THEN** it does not require assessment materials such as a one-page explanation or three-minute recording order
- **AND** it describes generic review/archive evidence instead

#### Scenario: Apply prompt respects current change scope

- **GIVEN** a generated apply prompt
- **WHEN** it describes non-goals
- **THEN** it instructs the agent not to implement out-of-scope work
- **AND** it does not hardcode a fixed list of unrelated technologies as universal exclusions

### Requirement: Bootstrap assets stay synchronized

`scripts/bootstrap-ai-sop.ps1` SHALL embed the same updated SOP assets that exist in the repository source files.

#### Scenario: Rebuilding embedded assets

- **GIVEN** prompt templates or generator scripts are changed
- **WHEN** `scripts/rebuild-bootstrap-assets.ps1` runs
- **THEN** `scripts/bootstrap-ai-sop.ps1` contains regenerated embedded assets
- **AND** newly bootstrapped projects receive the updated generic templates and generator behavior
