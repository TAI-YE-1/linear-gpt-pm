# Architecture Decisions

## AD-1: `using-superpowers` remains the top-level method router

The package does not create feature, bug, or review workflow replacements.

## AD-2: OpenSpec artifacts are authoritative

Superpowers may derive disposable execution briefs, but no second formal design or implementation plan is maintained.

## AD-3: One implementation controller

A task set is implemented either by OpenSpec apply or a Superpowers executor, never both.

## AD-4: Roles do not lock models

Models and reasoning efforts are selected at spawn time after availability and backend checks.

## AD-5: Custom role names use `sp_`

This avoids overriding Codex built-in `worker`, `explorer`, or `default`.

## AD-6: Cross-model delegation uses a self-contained brief

Full-history forks inherit model and reasoning settings, so cross-model work uses no-history or limited-history context.

## AD-7: Shared-worktree writes are serial

Parallelism is the default only for independent read-only research.

## AD-8: Native SDD is commit-centric

Without explicit checkpoint-commit authorization, use the no-commit adapter or sequential execution.

## AD-9: OpenSpec archive and Git branch closeout are separate

A completed or archived change does not automatically trigger merge, push, branch deletion, or deployment.

## AD-10: No experimental feature is enabled by the installer

The installer detects capabilities at runtime and does not modify `config.toml`.
