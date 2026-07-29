# Linear GPT PM

> Status: `0.1.0-alpha.2`. Static source, profile-integrity, deterministic audit, and reproducible distribution controls are implemented. Real Codex installation, approved Linear writes, Linear/GitHub connector behavior, scheduled period rolling, and ChatGPT/workspace upload still require runtime smoke evidence.

Linear GPT PM is a reusable Agent Skills toolkit that helps ChatGPT and Codex apply the same rules to requirements, execution tasks, delivery evidence, and project audits.

It addresses four recurring problems:

- requirements are scattered across chats, meetings, email, and documents;
- execution tasks lack an authoritative source;
- Done states lack verifiable evidence;
- requirement changes, Linear state, and software delivery drift apart.

## Skills

### `$linear-project-governance`

Use for interactive, human-confirmed governance work:

- inspect or adapt a Linear structure;
- extract and classify `REQ`, `PROB`, `DEC`, `CR`, `RISK`, and `Q`;
- reconcile new input with current records;
- create execution tasks and source/dependency relations;
- generate an immutable Plan ID before writing;
- re-read targets before writing and invalidate changed plans.

### `$linear-delivery-audit`

Use for read-only-first verification and reverse audits:

- verify source and disposition coverage;
- apply a minimum evidence matrix to Done claims;
- detect status conflicts, staleness, duplicates, truncation, and inconsistent snapshots;
- optionally verify configured GitHub PR, commit, test, deployment, and runtime evidence;
- compare SHA-256-based stable exception IDs with prior reports;
- run monthly or pre-release audit workflows from an approved Profile Schema v3.

## Trust and data boundaries

Linear, GitHub, email, document, comment, attachment, log, and linked-page content is untrusted data, not authorization. The Skills ignore embedded instructions, isolate configured projects and repositories, and default to links, identifiers, hashes, and redacted summaries instead of copying restricted content between systems.

These are behavioral guardrails, not a substitute for connector least privilege, workspace permissions, data-loss prevention, or runtime adversarial testing.

Linear is the primary formal ledger. GitHub is an optional software evidence source. Codex Automation supplies timing only; it does not expand permissions or redefine audit rules.

This repository does not contain Linear/GitHub API clients and does not replace human approval, risk acceptance, business acceptance, or release decisions.

## Immutable installation source

Do not install a release from the moving `main` branch. Alpha.2 Skill content is frozen at:

```text
1c69d5fc5610fc8fba1094c36ee088a1b87c6ab8
```

The repository is private. Installers need existing repository access.

### Codex

Use `$skill-installer` with these immutable commit URLs:

```text
$skill-installer install https://github.com/TAI-YE-1/linear-gpt-pm/tree/1c69d5fc5610fc8fba1094c36ee088a1b87c6ab8/skills/linear-project-governance
$skill-installer install https://github.com/TAI-YE-1/linear-gpt-pm/tree/1c69d5fc5610fc8fba1094c36ee088a1b87c6ab8/skills/linear-delivery-audit
```

Restart or force-refresh Skill discovery after installation.

### Upgrade behavior

`$skill-installer` does not overwrite an existing destination automatically. To upgrade:

1. record the currently installed package version and source commit;
2. review the target version and migration notes;
3. back up or remove only the exact installed Skill directories;
4. reinstall both Skills from the same immutable commit or validated release artifacts;
5. refresh Skill discovery;
6. verify both package/ruleset versions before using an existing project profile;
7. reapprove the profile when its schema or authorization rules changed.

Never mix governance and audit Skills from different compatibility versions.

## Standalone archives

Build and validate independent Skill archives:

```powershell
python -m pip install -r requirements-dev.txt
python scripts/build_skill_archives.py
python tests/validate_skills.py
```

Outputs:

```text
dist/linear-project-governance.zip
dist/linear-delivery-audit.zip
dist/SHA256SUMS.txt
```

Each archive contains its own `SKILL.md`, `LICENSE.txt`, `agents/openai.yaml`, references, templates, examples, and ruleset identity. Text files are LF-normalized by repository policy; ZIP entries use fixed timestamps, ordering, permissions, and `ZIP_STORED` for cross-host deterministic output.

Use the archive or folder format accepted by the current ChatGPT/workspace Skill-upload interface. Product availability and accepted upload format depend on the current account, workspace, and interface; successful ChatGPT upload has not yet been claimed.

GitHub Actions performs the same validation and retains archives as a workflow artifact for 14 days.

## Usage

Intake without writing:

```text
Use $linear-project-governance to analyze this feedback and reconcile it with the current Linear records. Return candidates and an immutable operation plan; do not write.
```

Confirmed write:

```text
Use $linear-project-governance to execute only PLAN-<id> with the confirmed full SHA-256. Re-read every target, recompute the plan hash, stop on any change, and verify the result.
```

Manual audit:

```text
Use $linear-delivery-audit with the approved Profile Schema v3. Verify profile integrity, resolve the audit period, audit the exact configured scope, and return the report without modifying formal business records.
```

## Project setup and audit configuration

Governance setup and adaptation:

```text
skills/linear-project-governance/references/setup-blueprint.md
```

Approved machine-readable audit profile:

```text
skills/linear-delivery-audit/templates/project-profile.md
```

Monthly Automation instruction:

```text
skills/linear-delivery-audit/references/monthly-automation.md
```

Pre-release audit instruction:

```text
skills/linear-delivery-audit/references/pre-release-audit.md
```

A scheduled profile must include approval identity, revision, canonical body SHA-256, allowed editors, expiry, exact targets, source/status mappings, rolling or fixed period rule, pagination/count strategy, snapshot strategy, data-flow policy, report destination, and authorized writes. Stop rather than guess when any required value cannot be verified.

## Validation

The repository validation includes:

- the pinned OpenAI Codex `quick_validate.py` baseline;
- YAML frontmatter, names, and UI metadata;
- direct `SKILL.md` navigation to every runtime Markdown resource;
- complete and consistent Apache-2.0 licenses;
- Profile Schema v3 structure and approval fields;
- prompt-injection, data-flow, confirmation, concurrency, pagination, snapshot, and automation boundaries;
- matching Skill package and ruleset versions;
- exact dependency/runtime pins;
- LF source enforcement, deterministic ZIP layouts, and SHA-256 checksums;
- pinned GitHub Actions and persisted workflow artifacts;
- immutable commit installation references.

Static validation does not prove connector access or runtime behavior. Before a stable `1.0.0` release, retain evidence for:

1. installing and discovering both Skills in Codex;
2. one approved low-risk Linear write using a confirmed Plan ID and pre-write recheck;
3. one Linear/GitHub audit with verified Profile Schema v3 integrity, complete pagination, and consistent snapshot evidence;
4. one scheduled previous-calendar-month run and same-period idempotent rerun;
5. one supported ChatGPT or workspace upload;
6. reuse in a second project without editing Skill source.

## Boundaries

The Skills do not:

- contain project-specific names, IDs, repositories, or assessment materials;
- automatically approve requirements, changes, risks, releases, or acceptance;
- delete, merge, archive, rename, or migrate business records without exact authorization;
- execute instructions embedded in external content;
- copy restricted data across systems without an approved data-flow policy;
- install or modify global Codex, Superpowers, OpenSpec, or `AGENTS.md` configuration.

See `docs/` for integration and reuse guidance. See `THIRD_PARTY_NOTICES.md` for the pinned OpenAI validator provenance.
