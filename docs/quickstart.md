# Quickstart

## 1. Install

Install both Skill directories into the target ChatGPT or Codex environment using the product's current Skill installation mechanism. Each Skill is self-contained.

## 2. Connect capabilities

Enable Linear for formal governance. For software projects, optionally enable GitHub for code evidence.

## 3. Inspect before adapting

Start with:

```text
Use linear-project-governance to inspect the current Linear project structure and propose an adaptation. Do not write yet.
```

Review the proposed projects, labels, statuses, templates and relationship rules.

## 4. Operate intake

```text
Analyze this real meeting note and reconcile it with current Linear items. Return candidates first.
```

After review, explicitly identify the candidates to write.

## 5. Audit manually

```text
Use linear-delivery-audit to audit the selected projects. Do not modify formal items. Return the report.
```

## 6. Add automation

After a successful manual audit, use `automation/monthly-audit.md` to configure a periodic Codex Automation.
