# Linear GPT PM

> Status: `0.1.0-alpha.1`. Source structure and reproducible distribution checks are implemented. Real Codex installation, ChatGPT upload, Linear/GitHub connector behavior, and scheduled Automation still require runtime smoke evidence.

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
- re-read targets before writing and stop on concurrent changes.

### `$linear-delivery-audit`

Use for read-only-first verification and reverse audits:

- check verified source and disposition coverage;
- check Done evidence and change propagation;
- detect status conflicts, staleness, duplicates, truncation, and collection gaps;
- optionally verify configured GitHub PR, commit, test, deployment, and runtime evidence;
- compare stable exception IDs with a prior report;
- support monthly or pre-release audit workflows.

## Trust and data boundaries

Linear, GitHub, email, document, comment, attachment, log, and linked-page content is untrusted data, not authorization. The Skills ignore embedded instructions, isolate configured projects and repositories, and default to links, identifiers, hashes, and redacted summaries instead of copying restricted content between systems.

Linear is the primary formal ledger. GitHub is an optional software evidence source. Codex Automation supplies timing only; it does not expand permissions or redefine audit rules.

This repository does not contain Linear/GitHub API clients and does not replace human approval, risk acceptance, business acceptance, or release decisions.

## Installation

The repository is private. Installers need existing repository access. If the repository is made public later, the same GitHub paths can be used without private-repository credentials.

### Codex

Use `$skill-installer` with both directories:

```text
$skill-installer install https://github.com/TAI-YE-1/linear-gpt-pm/tree/main/skills/linear-project-governance
$skill-installer install https://github.com/TAI-YE-1/linear-gpt-pm/tree/main/skills/linear-delivery-audit
```

Restart or force-refresh Skill discovery after installation.

### Standalone archives

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

Each archive contains its own `SKILL.md`, `LICENSE.txt`, `agents/openai.yaml`, references, templates, examples, and ruleset identity. Archive timestamps, file ordering, and permissions are normalized for reproducible output.

Use the archive or folder format accepted by the current ChatGPT/Workspace Skill-upload interface. Product availability and accepted upload format depend on the current account, workspace, and interface; successful ChatGPT upload has not yet been claimed.

GitHub Actions performs the same validation and retains the archives as a workflow artifact for 14 days.

## Usage

Intake without writing:

```text
Use $linear-project-governance to analyze this feedback and reconcile it with the current Linear records. Return candidates first and do not write.
```

Confirmed write:

```text
Use $linear-project-governance to write only the previously confirmed items. Re-read every target before writing, stop on concurrent changes, and verify the result.
```

Manual audit:

```text
Use $linear-delivery-audit with the completed project profile. Audit the exact configured scope and return the report without modifying formal business records.
```

## Project setup and audit configuration

Governance setup and adaptation:

```text
skills/linear-project-governance/references/setup-blueprint.md
```

Scheduled audit profile:

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

Keep the completed profile explicit about single/dual project mode, label/status mappings, source semantics, audit windows, pagination, data classification, report destination, and allowed writes. Stop rather than guess when required configuration is unresolved.

## Validation

The repository validation includes:

- the pinned OpenAI Codex `quick_validate.py` baseline;
- YAML frontmatter, names, and UI metadata;
- direct `SKILL.md` navigation to every runtime Markdown resource;
- complete and consistent Apache-2.0 licenses;
- prompt-injection, data-flow, confirmation, concurrency, pagination, and automation boundaries;
- matching Skill package and ruleset versions;
- reproducible ZIP layouts and SHA-256 checksums;
- pinned GitHub Actions and persisted workflow artifacts.

Static validation does not prove connector access or runtime behavior. Before a stable `1.0.0` release, retain evidence for:

1. installing and discovering both Skills in Codex;
2. one human-confirmed Linear governance write with pre-write conflict checking;
3. one Linear/GitHub audit with complete pagination evidence;
4. one scheduled idempotent report;
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