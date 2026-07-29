# Quickstart

## Path A — Basic use

Install both Skills from the same version, refresh Codex, and start with natural language:

```text
Use $linear-project-governance to analyze this meeting note, reconcile it with current Linear records, and return candidates only.
```

No Profile or hash setup is required.

When a write is proposed, review the numbered operations and confirm only the short Plan ID:

```text
执行 PLAN-A1B2C3D4E5
```

The Skill verifies the full digest and current target versions internally.

## Path B — Quick manual audit

```text
Use $linear-delivery-audit to audit this Linear project for the last 30 days. Keep it read-only and return the findings in chat.
```

Provide the exact project, optional repository, and time window if they are not already clear. A persistent Profile is not required.

## Path C — Advanced automation

Create and seal Profile Schema v4 only after one successful manual audit:

```powershell
cd <installed-linear-delivery-audit-skill>
python scripts/profile_tool.py init project-profile.json
# Edit project-profile.json.
python scripts/profile_tool.py seal project-profile.json `
  --approved-by "Project Owner" `
  --approval-record "APPROVAL-123"
python scripts/profile_tool.py validate project-profile.json
python scripts/profile_tool.py resolve-period project-profile.json
```

Then use `skills/linear-delivery-audit/references/monthly-automation.md` to configure recurrence. Verify one same-period rerun and one later-period rolling-window run.

## Safe installation from a private checkout

From repository commit `fc1fc6aa75b5d9ebec4613f37c21a868b1e9f751`:

```powershell
python scripts/install_codex_skills.py --dry-run --source-ref fc1fc6aa75b5d9ebec4613f37c21a868b1e9f751
python scripts/install_codex_skills.py --source-ref fc1fc6aa75b5d9ebec4613f37c21a868b1e9f751
```

Use `--replace` for a reviewed upgrade; the installer backs up existing Skill directories first.

## Repository validation

```powershell
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -p "test_*.py" -v
python scripts/build_skill_archives.py
python tests/validate_skills.py
```

Static and unit validation does not replace real connector smoke evidence. Record runtime results in `tests/runtime-smoke-template.md`.
