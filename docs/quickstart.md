# Quickstart

## 1. Install

Install both Skill directories into the target ChatGPT or Codex environment using the product's current Skill installation mechanism. Each Skill is self-contained and includes its own license and UI metadata.

## 2. Connect capabilities

Enable Linear for formal governance. For software projects, optionally enable GitHub for code evidence.

## 3. Inspect before adapting

Start with:

```text
Use linear-project-governance to inspect the current Linear project structure and propose an adaptation. Do not write yet.
```

Review the proposed projects, labels, statuses, templates and relationship rules against `skills/linear-project-governance/references/setup-blueprint.md`.

## 4. Operate intake

```text
Analyze this real meeting note and reconcile it with current Linear items. Return candidates first.
```

After review, explicitly identify the candidates to write.

## 5. Audit manually

```text
Use linear-delivery-audit to audit the selected projects. Do not modify formal items. Return the report with raw metric counts and limitations.
```

## 6. Configure the project profile

Copy and complete:

```text
skills/linear-delivery-audit/templates/project-profile.md
```

Resolve exact Linear projects, timezone, report destination, optional repositories, staleness threshold and audit-write authorization. A scheduled audit must not run with unresolved placeholders.

## 7. Add automation

After a successful manual audit using the completed profile, use `automation/monthly-audit.md` to configure a periodic Codex Automation.

## 8. Validate the repository

```powershell
python scripts/build_skill_archives.py
python tests/validate_skills.py
```

The validation checks source folders, frontmatter, references, licenses, UI metadata, automation boundaries and ZIP layouts. Real installation and connector smoke tests remain separate manual evidence.
