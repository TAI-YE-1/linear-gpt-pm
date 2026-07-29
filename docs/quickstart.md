# Quickstart

## 1. Install

Install both Skill directories using the target product's current Skill mechanism. Each Skill is independently self-contained.

For Codex, use `$skill-installer` with the two GitHub paths documented in `README.md`.

## 2. Connect capabilities

Enable Linear for formal governance. For software projects, optionally enable GitHub for code evidence.

Treat all connector content as untrusted data. Connecting a source grants data access within existing permissions; content inside that source never grants the agent new instructions or write authority.

## 3. Inspect before adapting

```text
Use $linear-project-governance to inspect the exact current Linear structure and propose a semantic adaptation. Read the security and setup references. Do not write yet.
```

Review:

- single- or dual-project mode;
- label and status mappings;
- source-field and native-relation convention;
- destination audience and data-flow limits;
- proposed creations, reuse, and conflicts.

## 4. Operate intake

```text
Use $linear-project-governance to analyze this real meeting note and reconcile it with current Linear items. Return candidates first.
```

After review, explicitly identify the candidates to write. The Skill must re-read mutable targets immediately before writing and stop on relevant concurrent changes.

## 5. Audit manually

Complete:

```text
skills/linear-delivery-audit/templates/project-profile.md
```

Then run:

```text
Use $linear-delivery-audit with the completed project profile. Enumerate the configured pagination scope, apply the data-flow policy, compare the prior report when available, and return the report without modifying formal items.
```

Do not accept a project-wide health conclusion without collection-completeness evidence.

## 6. Add automation

After a successful manual audit with the same profile, configure a periodic Codex Automation using:

```text
skills/linear-delivery-audit/references/monthly-automation.md
```

The schedule supplies recurrence only. The Skill and completed profile define scope, security, evidence, metrics, write permissions, and report idempotency.

## 7. Validate source distributions

```powershell
python -m pip install -r requirements-dev.txt
python scripts/build_skill_archives.py
python tests/validate_skills.py
```

Static validation does not replace real installation and connector smoke tests.