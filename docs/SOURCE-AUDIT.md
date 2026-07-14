# Upstream Source Audit

审计日期：2026-07-14

本项目基于以下官方仓库固定版本设计，不采用第三方教程作为架构依据：

| 仓库 | 固定 commit |
|---|---|
| `openai/codex` | `80c6cd3014e4236e99bd06e67f31fcb95c9ee906` |
| `obra/superpowers` | `d884ae04edebef577e82ff7c4e143debd0bbec99` |
| `Fission-AI/OpenSpec` | `0a99f410457271aa773d8b106f03f637f7c6b3c0` |

## 已审计范围

- Superpowers 的 `using-superpowers`、`brainstorming`、`systematic-debugging`、`test-driven-development`、`writing-plans`、`executing-plans`、`subagent-driven-development`、`dispatching-parallel-agents`、`requesting-code-review`、`receiving-code-review`、`verification-before-completion`、`using-git-worktrees`、`finishing-a-development-branch`。
- SDD 的 implementer、task reviewer、task brief 和 review package 模板及脚本。
- OpenSpec 的 profile、schema、propose、apply、verify、archive、validate 和 JSON contract。
- Codex 的 subagent v1/v2、role 覆盖、模型/backend 兼容、Skill 加载和 `AGENTS.md` 加载。

## 核心结论

1. `using-superpowers` 保持为唯一顶层方法入口。
2. OpenSpec artifacts 是规格事实来源；不维护第二份正式设计或计划。
3. 同一批 tasks 只有一个实现控制器，OpenSpec apply 与 Superpowers executor 不重复执行。
4. 原生 SDD 依赖 task commits；未授权 commit 时使用 no-commit adapter 或顺序实施。
5. Codex subagent 共享工作目录，因此默认只并行只读调查，写入串行。
6. full-history fork 继承模型和推理强度；跨模型委派使用自包含 brief。
7. custom role 使用 `sp_` 前缀，避免覆盖内置 `worker`、`explorer` 和 `default`。
8. role 不锁定模型；路由在 spawn 时检查可用模型和 multi-agent backend。
9. `openspec validate --strict`、真实测试、code review 和 verify 各自承担不同职责。
10. OpenSpec archive 与 Git branch closeout 是独立生命周期。

更完整的设计依据、冲突处理和流程测试见：

- `docs/ARCHITECTURE-DECISIONS.md`
- `tests/manual-smoke-cases.md`
- 四个 `skills/*/SKILL.md`
