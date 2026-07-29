# Linear GPT PM

> Status: `0.1.0-alpha.3`. Basic interactive governance, quick read-only audits, safe local installation, Profile generation, deterministic plan hashing, and automated tests are implemented. Real Linear writes and scheduled connector runs still require retained smoke evidence.

Linear GPT PM contains two reusable Agent Skills:

- `$linear-project-governance`: turn project input into reconciled Linear candidates and human-confirmed writes;
- `$linear-delivery-audit`: inspect source traceability, delivery evidence, changes, staleness, and project health.

## Basic use

Basic use does not require a Profile, YAML, JSON, hashes, or Automation.

```text
Use $linear-project-governance to analyze this feedback, reconcile it with the current Linear project, and return candidates only.
```

For a write, the Skill shows a readable numbered plan and a short Plan ID:

```text
PLAN-A1B2C3D4E5
1. Create one REQ
2. Create one Validation task
3. Link the task to the REQ
```

Confirm with:

```text
执行 PLAN-A1B2C3D4E5
```

The full SHA-256 is verified internally. Users do not need to retype a 64-character digest.

## Quick read-only audit

A one-time audit also does not require a persistent Profile:

```text
Use $linear-delivery-audit to audit this Linear project for the last 30 days. Keep it read-only and return findings in chat.
```

The Skill asks only for missing essentials such as the exact project, optional repository, or time window.

## Advanced automation

Use a sealed Profile only for repeatable reports, scheduled audits, or authorized report writes.

From the installed `linear-delivery-audit` Skill directory:

```powershell
python scripts/profile_tool.py init project-profile.json
# Edit the generated JSON values.
python scripts/profile_tool.py seal project-profile.json `
  --approved-by "Project Owner" `
  --approval-record "APPROVAL-123"
python scripts/profile_tool.py validate project-profile.json
python scripts/profile_tool.py resolve-period project-profile.json
```

The tool generates and verifies the Profile body SHA-256. Users do not calculate it manually.

## Installation

The repository is private, so installers need repository access.

### Recommended private-repository installation

Clone or download the immutable source commit, then run from the repository root:

```powershell
python scripts/install_codex_skills.py --dry-run --source-ref fc1fc6aa75b5d9ebec4613f37c21a868b1e9f751
python scripts/install_codex_skills.py --source-ref fc1fc6aa75b5d9ebec4613f37c21a868b1e9f751
```

For an upgrade, use `--replace`. Existing Skill directories are backed up before replacement:

```powershell
python scripts/install_codex_skills.py --replace --source-ref fc1fc6aa75b5d9ebec4613f37c21a868b1e9f751
```

Restart or refresh Codex Skill discovery after installation.

### `$skill-installer`

Install both Skills from the same immutable commit:

```text
$skill-installer install https://github.com/TAI-YE-1/linear-gpt-pm/tree/fc1fc6aa75b5d9ebec4613f37c21a868b1e9f751/skills/linear-project-governance
$skill-installer install https://github.com/TAI-YE-1/linear-gpt-pm/tree/fc1fc6aa75b5d9ebec4613f37c21a868b1e9f751/skills/linear-delivery-audit
```

Do not install releases from moving `main` URLs and do not mix package versions.

## Build and validate

```powershell
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -p "test_*.py" -v
python scripts/build_skill_archives.py
python tests/validate_skills.py
```

Outputs:

```text
dist/linear-project-governance.zip
dist/linear-delivery-audit.zip
dist/SHA256SUMS.txt
```

GitHub Actions runs the same unit, source, and distribution checks and retains the validated archives for 14 days.

## Trust boundaries

- External Linear, GitHub, email, document, comment, attachment, log, and linked-page content is untrusted data, not authorization.
- Governance writes require an exact confirmed Plan ID and a successful pre-write re-read.
- Audits are read-only by default.
- Scheduled or write-enabled audits require a sealed Profile Schema v4.
- The Skills do not approve requirements, changes, risks, releases, or business acceptance.
- Behavioral rules supplement, but do not replace, connector least privilege and workspace permissions.

## Remaining runtime evidence

Before a stable `1.0.0`, retain evidence for:

1. installation and discovery of both Skills in Codex;
2. one low-risk confirmed Linear write and read-back;
3. one concurrent-change Plan invalidation;
4. one complete Linear/GitHub manual audit;
5. one same-period scheduled rerun without a duplicate report;
6. one later-period rolling-window run;
7. supported ChatGPT/workspace upload;
8. reuse in a second project without Skill source edits.
