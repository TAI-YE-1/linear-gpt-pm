# Quickstart

## 1. Install one immutable version

Install both Skills from the same pinned commit:

```text
https://github.com/TAI-YE-1/linear-gpt-pm/tree/341189cb726f0fae89f623e8f6e1a79c25cd8190/skills/linear-project-governance
https://github.com/TAI-YE-1/linear-gpt-pm/tree/341189cb726f0fae89f623e8f6e1a79c25cd8190/skills/linear-delivery-audit
```

Do not mix package versions. The installer does not overwrite existing Skill directories automatically; back up and replace only the exact Skill folders during an approved upgrade.

## 2. Connect minimum capabilities

Enable Linear for formal governance. For software projects, optionally enable GitHub for code evidence. Use least privilege and keep GitHub read-only for normal audits.

## 3. Inspect before adapting

```text
Use $linear-project-governance to inspect the current Linear structure and propose an adaptation. Return an immutable operation plan and do not write.
```

Review projects, labels, statuses, templates, source conventions, and security/data-flow rules against `skills/linear-project-governance/references/setup-blueprint.md`.

## 4. Execute one low-risk confirmed write

Confirm the displayed Plan ID and full SHA-256. The Skill must re-read targets, recompute the plan hash, stop on changes, execute only the unchanged plan, and read back the result.

## 5. Create and approve Profile Schema v3

Complete:

```text
skills/linear-delivery-audit/templates/project-profile.md
```

Parse the canonical YAML, calculate the profile-body SHA-256, record approver, approval record, revision, allowed editors, expiry, exact targets, mappings, period rule, collection strategy, data-flow policy, report destination, and authorized writes.

## 6. Audit manually

```text
Use $linear-delivery-audit with the approved Profile Schema v3. Verify profile integrity, resolve the audit period, enumerate all pages, establish snapshot consistency, and return the report without changing formal business records.
```

## 7. Add monthly Automation

After a successful manual audit with the same approved profile revision/hash, use:

```text
skills/linear-delivery-audit/references/monthly-automation.md
```

For `previous-calendar-month`, verify that every run calculates a new absolute range in the configured timezone. Run the same period twice and confirm the second run updates the existing report instead of creating a duplicate.

## 8. Validate the repository

```powershell
python -m pip install -r requirements-dev.txt
python scripts/build_skill_archives.py
python tests/validate_skills.py
```

Static validation covers structure, profile schema, rules, deterministic archives, and immutable installation references. Runtime installation and connector behavior require evidence using `tests/runtime-smoke-template.md`.
