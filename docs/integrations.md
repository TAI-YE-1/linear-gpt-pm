# Integrations

This project describes capability requirements and failure boundaries. It intentionally does not reproduce platform account-registration, OAuth or token tutorials.

## Linear

Recommended core capability.

Useful read capabilities:

- projects, issues, labels and statuses;
- descriptions, comments and documents;
- owners and native relations.

Useful write capabilities for interactive governance:

- create/update issues;
- create documents and comments;
- add `relatedTo`, `blocks`, `blockedBy` and `duplicateOf` relations.

Failure behavior:

- no connection: output candidates or reports only;
- read-only: do not claim writes;
- partial failure: report exact successful and failed actions;
- destructive actions: require explicit target-level authorization.

## GitHub

Optional evidence source for software projects.

Useful read capabilities:

- repository, branch and commit metadata;
- PR state and changed files;
- checks, tests and review evidence.

GitHub write permissions are not required for normal governance audits. Creating branches, commits, PRs, rerunning CI or merging code is outside the default audit scope.

## Codex Automation

Provides timing and recurrence. It does not define governance rules. Configure it to invoke `linear-delivery-audit` and use the repository's automation templates.
