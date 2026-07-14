# Contributing

Contributions are welcome. Keep changes focused, evidence-based, and compatible with the repository's safety model.

## Development workflow

1. Create a branch from `main`.
2. Read the real implementation and applicable documentation before changing behavior.
3. Add or update focused tests for behavioral changes.
4. Run:

   ```powershell
   python .\tests\validate_package.py
   python .\tests\run_smoke_tests.py
   ```

5. Review the diff and document any tests that could not be run.
6. Open a pull request describing the problem, approach, validation, and remaining risks.

## Compatibility principles

- Do not hard-code personal email addresses, usernames, home-directory paths, language preferences, credentials, or connector-specific notification behavior.
- Do not enable experimental Codex features automatically.
- Do not lock models in role files; model selection remains runtime-dependent.
- Preserve user content outside the managed `AGENTS.md` marker block.
- Do not add automatic commit, push, merge, deployment, or paid external actions.

## Generated files

`tests/last-smoke-report.json` is generated locally and must not be committed.
