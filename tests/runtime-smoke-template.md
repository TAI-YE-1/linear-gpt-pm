# Runtime Smoke Evidence

Use one copy per environment and retain exact timestamps, IDs, hashes, and redacted evidence.

## Environment

- Date and timezone:
- Product and version:
- Account/workspace type:
- Skill package/ruleset version:
- Installation source commit/ref:
- Archive SHA-256 values:

## Installation

- Installation method: `$skill-installer / local installer / upload`
- Dry-run result:
- Existing-version backup/replace result:
- Both Skills discovered after refresh:
- Installation manifest location/content:
- Failure or workaround:

## Basic governance usability

- Natural-language input:
- Candidate output required no Profile: `yes/no`
- Number of unnecessary setup questions:
- Proposed readable operations:
- Short Plan ID:
- Full plan SHA-256 retained internally:
- User confirmation used only the short Plan ID: `yes/no`
- Pre-write re-read and hash verification:
- Created/updated IDs and read-back:
- Concurrent-change invalidation test:

## Quick read-only audit usability

- Exact project/repository/window:
- Persistent Profile required: `yes/no` (expected `no`)
- Number of setup questions:
- Findings and limitations:
- Prohibited writes observed: `yes/no`

## Profile Schema v4 tooling

- `profile_tool.py init` result:
- Profile completion effort/issues:
- `profile_tool.py seal` result:
- Generated body SHA-256:
- `profile_tool.py validate` result:
- `profile_tool.py resolve-period` result:
- Manual hash calculation required: `yes/no` (expected `no`)
- Tampered-profile validation result:
- Expired-profile validation result:

## Repeatable audit

- Exact Linear and optional GitHub scope:
- Resolved period rule/range/timezone:
- Collection start/finish:
- Expected/fetched counts and cursors:
- Snapshot recheck:
- Stable exception IDs:
- Evidence-matrix rows:
- Audit confidence and project health:
- Report write/read-back or return-only result:

## Scheduled run

- First scheduled run:
- Same-period rerun updated existing report: `yes/no`
- Duplicate report created: `yes/no`
- Later-period window rolled correctly: `yes/no`
- Profile hash/revision reverified each run: `yes/no`
- Prohibited mutations observed: `yes/no`

## ChatGPT/workspace upload

- Interface and account/workspace:
- Accepted artifact format:
- Upload and trigger result:

## Second-project reuse

- Second project:
- Same immutable Skill package used:
- Skill source modified: `yes/no`
- Only Profile/mappings changed: `yes/no`

## Verdict

- Basic governance usability score:
- Quick audit usability score:
- Advanced automation usability score:
- Passed checks:
- Failed checks:
- Unverified checks:
- Blocking defects:
- Evidence locations:
