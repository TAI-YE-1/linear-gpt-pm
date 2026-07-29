# Audit Project Profile

Use a persistent Profile only for repeatable reports, scheduled audits, or audit writes. A quick read-only audit in the current conversation does not require one.

## Prepare the Profile tool

On Windows, or on any system without an IANA timezone database, install the bundled runtime dependency first:

```powershell
python -m pip install -r requirements-runtime.txt
```

## Create a mostly prefilled Profile

From the installed `linear-delivery-audit` Skill directory:

```powershell
python scripts/profile_tool.py init project-profile.json `
  --project-key "demo" `
  --project-name "Demo Project" `
  --timezone "Asia/Shanghai" `
  --owner "Project Owner" `
  --team "Demo Team" `
  --project "Demo Delivery"
```

The command supplies safe defaults for:

- semantic governance, execution, and status mappings;
- the `Source` field and `relatedTo` relation;
- return-only audit output;
- internal link-or-summary data flow;
- previous-calendar-month period resolution;
- all-cursor pagination and updated-at snapshot rechecks;
- bundled observability thresholds and maintenance marker.

Review and adapt the generated JSON to the real workspace. For dual-project mode, use `--structure-mode dual-project`, `--governance-project`, and `--delivery-project`.

## Seal and validate

```powershell
python scripts/profile_tool.py seal project-profile.json `
  --approved-by "Project Owner" `
  --approval-record "APPROVAL-123"
python scripts/profile_tool.py validate project-profile.json
python scripts/profile_tool.py resolve-period project-profile.json
```

The tool computes and verifies the canonical Profile-body SHA-256. Users do not calculate or paste hashes manually.

## Profile Schema v4

The JSON document records:

- stable Profile ID, revision, approver, approval record, editors, expiry, and generated hash;
- project identity, timezone, Linear targets, mappings, source convention, and governance document;
- report destination and exact authorized writes;
- classifications, redactions, copy policy, and allowed evidence systems;
- optional repositories and candidate scope;
- rolling, fixed, or release-candidate period rules;
- expected counts, pagination, evidence access, and snapshot strategy;
- evidence/observability policy and prior-report comparison.

## Integrity rules

`profile_tool.py seal` canonicalizes only the top-level `profile` body as UTF-8 JSON with sorted object keys, no insignificant whitespace, and arrays in declared order. Any Profile-body change requires a higher revision, a new approval record/timestamp, and resealing.

Scheduled execution must stop when parsing, mappings, hash, approval, expiry, scope, destination, data flow, or authorization cannot be verified.

## Usage boundary

- Quick read-only audit: current conversation scope; no Profile.
- Repeatable manual audit: validated Profile recommended.
- Scheduled or write-enabled audit: sealed and approved Profile required.
