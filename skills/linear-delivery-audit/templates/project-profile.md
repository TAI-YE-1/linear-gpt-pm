# Audit Project Profile

Use this only for repeatable manual reports, scheduled audits, or audit writes. A quick read-only audit in the current conversation does not require a persistent Profile.

## Fast path

Run from the installed `linear-delivery-audit` Skill directory:

```powershell
python scripts/profile_tool.py init project-profile.json
```

Edit the generated JSON values, then seal it:

```powershell
python scripts/profile_tool.py seal project-profile.json `
  --approved-by "<person-or-authorized-role>" `
  --approval-record "<stable-approval-record-id>"
```

Validate and resolve the current period:

```powershell
python scripts/profile_tool.py validate project-profile.json
python scripts/profile_tool.py resolve-period project-profile.json
```

The tool calculates the canonical SHA-256. Users should not calculate or paste hashes manually.

## Profile Schema v4

The generated JSON document contains:

- `profile_schema_version`, stable Profile ID, and revision;
- approval identity, timestamp, record, allowed editors, expiry, and generated body SHA-256;
- project identity and timezone;
- single/dual Linear project targets;
- governance, execution, status, source-field, and relation mappings;
- exact report destination and allowed writes;
- data classifications, redactions, and source-to-destination flow rules;
- optional repositories and candidate scope;
- rolling, fixed, or release-candidate audit period rules;
- pagination, expected counts, evidence access, and snapshot strategy;
- evidence and observability policy;
- prior-report lookup and idempotent report behavior.

## Integrity rules

`profile_tool.py seal` serializes only the top-level `profile` body as canonical JSON using UTF-8, sorted object keys, no insignificant whitespace, and arrays in declared order. It computes SHA-256 and writes the digest into the separate approval envelope.

Any change to the `profile` body requires:

1. a higher `profile_revision`;
2. a new approval record and timestamp;
3. a newly generated body SHA-256;
4. revalidation before use.

Scheduled execution must stop when Profile parsing, hash, approval, expiry, required metadata, scope, destination, or authorization cannot be verified.

## Period rules

- `previous-calendar-month`: calculate the previous calendar month on every run in the configured IANA timezone;
- `fixed-range`: require exact RFC3339 start and end timestamps;
- `release-candidate-scope`: require an exact candidate in the software evidence section.

Use an inclusive start and exclusive end. Write the resolved absolute range and timezone into every report.

## Usage boundary

- Quick read-only audit: current conversation scope is enough; no Profile required.
- Repeatable manual audit: validated Profile recommended.
- Scheduled or write-enabled audit: sealed and approved Profile required.
