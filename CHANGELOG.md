# Changelog

All notable changes to this project are documented here.

## [4.0.0-rc1] - 2026-07-14

### Added

- OpenSpec and Superpowers bridge Skill.
- Dynamic Codex subagent routing Skill and namespaced role profiles.
- Delivery guardrails for Git, CI, verification, and branch lifecycle.
- No-commit SDD adapter using temporary Git index snapshots.
- Safe dry-run installer and uninstaller with backups.
- Static validation, automated smoke tests, and manual Codex test cases.
- Upstream source audit and architecture decisions.
- Apache-2.0 licensing and third-party notices.

### Fixed

- Windows backup paths no longer embed an entire absolute path.
- Global `AGENTS.md` content no longer contains personal email addresses, fixed language preferences, or connector-specific notification behavior.
- Reinstallation replaces only the managed marker block and preserves user content outside it.

### Known limitations

- Real Codex model availability and multi-agent backend compatibility require testing in the user's installed Codex version.
- PowerShell wrappers and OpenSpec schema/store behavior should be verified in the target environment.
