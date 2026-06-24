# Design: AI Builder Pack Maker

## Overview

The first version is a small local Python CLI that transforms one Markdown input file into four deterministic Markdown output files.

```text
inputs/problem_pack.md
        |
        v
Python CLI
        |
        +--> outputs/latest/one_page_summary.md
        +--> outputs/latest/recording_script.md
        +--> outputs/latest/defense_qa.md
        +--> outputs/latest/materials_index.md
```

## Constraints

- Local-only execution.
- Markdown in, Markdown out.
- No model API calls.
- No web server or frontend.
- No database.
- No Feishu integration.
- Prefer Python standard library for the initial version.

## Proposed Architecture

### CLI Entry Point

The command accepts default paths:

- Input: `inputs/problem_pack.md`
- Output directory: `outputs/latest`

Optional flags may be added during implementation if they remain local-only and do not expand the product scope, for example:

- `--input`
- `--output-dir`

### Parsing Strategy

The input is treated as Markdown text. The generator should preserve useful source content instead of attempting complex semantic extraction in the first version.

Minimal parsing responsibilities:

- Read the full input as UTF-8.
- Detect Markdown headings and their following content blocks when useful.
- Fall back to the full source text if a specific expected heading is absent.

### Generation Strategy

Each output file is produced from a fixed template:

- `one_page_summary.md`: concise assessment summary with background, problem, solution, delivery result, verification effect, and reusable value.
- `recording_script.md`: three-minute recording script organized by time segment.
- `defense_qa.md`: likely defense questions and suggested answers based on the input pack.
- `materials_index.md`: index of evidence materials and generated deliverables.

The first version should not attempt natural-language rewriting through an external model. It should structure, excerpt, and frame the provided input content deterministically.

## Error Handling

- If the input file does not exist, the command exits non-zero with a clear message.
- If the input file is empty or whitespace-only, the command exits non-zero with a clear message.
- If output directory creation or file writing fails, the command exits non-zero with a clear message.

## Verification Strategy

Implementation should include local verification that checks:

- The CLI exits successfully for a valid input file.
- The four expected output files are created.
- Each output file is non-empty.
- The missing-input path fails clearly.
- The generator uses no network or external model API dependency.

## Future Extensions

These are intentionally excluded from the first version but may be proposed later:

- Optional model-assisted rewriting.
- Multiple input packs.
- Additional output formats.
- Web interface.
- Feishu or other collaboration tool export.
- Assessment archive history.
