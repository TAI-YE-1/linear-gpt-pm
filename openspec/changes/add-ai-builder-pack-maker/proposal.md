# Add AI Builder Pack Maker

## Summary

Create a local Python command-line tool that reads `inputs/problem_pack.md` and generates four Markdown deliverables under `outputs/latest/`:

- `one_page_summary.md`
- `recording_script.md`
- `defense_qa.md`
- `materials_index.md`

## Motivation

Preparing AI Builder assessment materials currently requires manually converting project notes, execution evidence, verification output, and delivery artifacts into a one-page summary, recording script, defense Q&A, and materials index. This is repetitive, slow, and easy to make inconsistent.

The first version should provide a deterministic local Markdown generator so a standard input pack can be turned into a review-ready draft package in minutes.

## Scope

### In Scope

- Read a local Markdown input file from `inputs/problem_pack.md`.
- Generate the four required Markdown files into `outputs/latest/`.
- Create missing output directories when needed.
- Overwrite the four generated files on each run so `outputs/latest/` always represents the latest package.
- Use deterministic template-based generation from the input content.
- Provide enough command-line behavior for local execution and verification.

### Out of Scope

- Model API integration.
- Web UI or frontend.
- Database storage.
- Feishu integration.
- Multi-user workflow.
- Cloud deployment.
- Automatic media generation.
- Non-Markdown output formats.

## User Impact

The user can maintain a single `inputs/problem_pack.md` file and run one local command to produce a complete first draft of the AI Builder assessment material package.

## Success Criteria

- Running the CLI with a valid `inputs/problem_pack.md` produces all four required files under `outputs/latest/`.
- Generated files are non-empty Markdown documents with clear section headings.
- The generator does not call external model APIs or require network access.
- The project can be verified locally with documented commands.
