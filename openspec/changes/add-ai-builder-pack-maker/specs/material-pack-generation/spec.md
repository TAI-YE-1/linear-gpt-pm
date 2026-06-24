## ADDED Requirements

### Requirement: Generate AI Builder assessment material package

The system SHALL provide a local Python command-line workflow that reads `inputs/problem_pack.md` and generates the AI Builder assessment material package in Markdown format.

#### Scenario: Generate all required Markdown deliverables

- **GIVEN** `inputs/problem_pack.md` exists and contains non-empty Markdown content
- **WHEN** the user runs the local generator command
- **THEN** the system SHALL create `outputs/latest/one_page_summary.md`
- **AND** the system SHALL create `outputs/latest/recording_script.md`
- **AND** the system SHALL create `outputs/latest/defense_qa.md`
- **AND** the system SHALL create `outputs/latest/materials_index.md`
- **AND** each generated file SHALL be non-empty Markdown

#### Scenario: Create missing output directory

- **GIVEN** `inputs/problem_pack.md` exists and contains non-empty Markdown content
- **AND** `outputs/latest/` does not exist
- **WHEN** the user runs the local generator command
- **THEN** the system SHALL create `outputs/latest/`
- **AND** the system SHALL write all four required Markdown files into it

#### Scenario: Overwrite latest generated files

- **GIVEN** previous generated files exist under `outputs/latest/`
- **AND** `inputs/problem_pack.md` exists and contains non-empty Markdown content
- **WHEN** the user runs the local generator command again
- **THEN** the system SHALL overwrite the four required generated files so they represent the latest input

### Requirement: Keep first version local and deterministic

The system SHALL keep the first version limited to local deterministic Markdown generation.

#### Scenario: Run without model API integration

- **GIVEN** the user runs the local generator command
- **WHEN** generation is performed
- **THEN** the system SHALL NOT call external model APIs
- **AND** the system SHALL NOT require network access

#### Scenario: Avoid out-of-scope integrations

- **GIVEN** the first version is implemented
- **WHEN** the project dependencies and runtime behavior are inspected
- **THEN** the system SHALL NOT include a web UI
- **AND** the system SHALL NOT include database storage
- **AND** the system SHALL NOT include Feishu integration

### Requirement: Report input errors clearly

The system SHALL fail clearly when the required input is unavailable or unusable.

#### Scenario: Missing input file

- **GIVEN** `inputs/problem_pack.md` does not exist
- **WHEN** the user runs the local generator command
- **THEN** the command SHALL exit with a non-zero status
- **AND** the error message SHALL identify the missing input file

#### Scenario: Empty input file

- **GIVEN** `inputs/problem_pack.md` exists but contains only whitespace
- **WHEN** the user runs the local generator command
- **THEN** the command SHALL exit with a non-zero status
- **AND** the error message SHALL explain that the input file is empty
