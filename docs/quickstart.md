# Quickstart

## Path A — Basic use

Install both Skills, refresh Codex, and start with natural language:

```text
Use $linear-project-governance to analyze this meeting note, reconcile it with current Linear records, and return candidates only.
```

No Profile or hash setup is required.

When a write is proposed, review the numbered operations and confirm only the short Plan ID:

```text
执行 PLAN-A1B2C3D4E5
```

The Skill verifies the full digest and target versions internally.

## Path B — Quick manual audit

```text
Use $linear-delivery-audit to audit this Linear project for the last 30 days. Keep it read-only and return findings in chat.
```

Provide exact project, optional repository, and time window only when missing. No persistent Profile is required.

## Path C — Advanced automation

After one successful manual audit:

```powershell
cd <installed-linear-delivery-audit-skill>
python -m pip install -r requirements-runtime.txt
python scripts/profile_tool.py init project-profile.json `
  --project-key "demo" `
  --project-name "Demo Project" `
  --timezone "Asia/Shanghai" `
  --owner "Project Owner" `
  --team "Demo Team" `
  --project "Demo Delivery"
# Review project-profile.json.
python scripts/profile_tool.py seal project-profile.json `
  --approved-by "Project Owner" `
  --approval-record "APPROVAL-123"
python scripts/profile_tool.py validate project-profile.json
python scripts/profile_tool.py resolve-period project-profile.json
```

Then use `skills/linear-delivery-audit/references/monthly-automation.md`. Verify one same-period rerun and one later-period rolling-window run.

## Safe installation from a private checkout

Use immutable commit `92561c1aa36c18ede37474185170ec3faa7d8c33`:

```powershell
python scripts/install_codex_skills.py --dry-run --source-ref 92561c1aa36c18ede37474185170ec3faa7d8c33
python scripts/install_codex_skills.py --source-ref 92561c1aa36c18ede37474185170ec3faa7d8c33
```

Use `--replace` for a reviewed upgrade; old Skill directories are backed up first.

## Local validation

```powershell
python -m pip install -r requirements-dev.txt
python -m compileall -q scripts skills tests
python -m unittest discover -s tests -p "test_*.py" -v
python scripts/build_skill_archives.py
python tests/validate_skills.py
```

The GitHub Actions workflow is manual until repository runners are available. Record runtime evidence in `tests/runtime-smoke-template.md`.
