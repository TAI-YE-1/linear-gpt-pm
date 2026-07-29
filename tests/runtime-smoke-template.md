# Runtime Smoke Evidence

Use one copy per environment and retain exact timestamps, identifiers, hashes, and redacted evidence.

## Environment

- Date and timezone:
- Product and version:
- Account/workspace type:
- Skill package version:
- Governance ruleset version:
- Audit ruleset version:
- Installation source commit/ref:
- Governance archive SHA-256:
- Audit archive SHA-256:

## Installation

- `$skill-installer` or upload action:
- Immutable source used:
- Both Skills discovered after refresh:
- Discovery output or screenshot:
- Existing-version upgrade behavior:
- Failure or workaround:

## Profile Schema v3 approval

- Profile location:
- Profile ID:
- Profile revision:
- Approved by:
- Approved at:
- Approval record:
- Allowed editors:
- Maximum age:
- Recomputed canonical profile-body SHA-256:
- Approved SHA-256 matched:
- Current editor/revision check:
- Expiry check:

## Governance smoke

- Linear workspace and test project:
- Input case:
- Candidate output:
- Plan ID:
- Full plan SHA-256:
- Operation IDs:
- User confirmation referencing exact Plan ID/digest:
- Baseline identifiers and update timestamps:
- Pre-write re-read result:
- Recomputed plan hash matched:
- Created/updated identifiers:
- Configured source field and native relation match:
- Read-back result:
- Sensitive data redacted:

## Audit smoke

- Exact Linear and optional GitHub scope:
- Audit period rule:
- Resolved absolute start/end/timezone:
- Collection started at:
- Collection finished at:
- Expected and fetched counts:
- Pages/cursors consumed:
- Objects changed during collection:
- Snapshot recheck result:
- Collection completeness:
- Snapshot consistency:
- Prior report used:
- Stable exception IDs and full hashes:
- Evidence-matrix rows exercised:
- Audit confidence:
- Overall health and metric counts:
- Prompt-injection or data-flow test result:
- Report write and read-back result:

## Scheduled run

- Schedule:
- First run timestamp:
- Period rule and resolved period:
- Report destination:
- Same-period rerun timestamp:
- Existing report updated:
- Duplicate report created: `yes/no`
- Next-period run timestamp:
- Next-period resolved range rolled correctly: `yes/no`
- Profile hash/revision reverified on each run: `yes/no`
- Prohibited mutations observed: `yes/no`

## ChatGPT/workspace upload

- Interface and account/workspace:
- Accepted artifact format:
- Upload result:
- Skill trigger result:

## Second-project reuse

- Second project:
- Same immutable Skill commit/archive versions:
- Skill source modified: `yes/no`
- Only profile/mappings changed: `yes/no`
- Governance and audit result:

## Verdict

- Passed checks:
- Failed checks:
- Unverified checks:
- Blocking defects:
- Evidence locations:
