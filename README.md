# Codex × Superpowers × OpenSpec 全局工作流 v4 RC1

> Status: release candidate. Automated package tests pass, while real Codex session compatibility still requires the manual smoke cases in `tests/manual-smoke-cases.md`.

这是基于官方上游源码审计重构的候选安装包。它不复制 Superpowers 或 OpenSpec，而是在两者之上增加 Codex 适配和交付治理。

## 审计文档

- [源码审计摘要](docs/SOURCE-AUDIT.md)
- [完整上游源码审计原文](docs/SOURCE-AUDIT-FULL.md)

完整原文是 RC1 实现前形成的历史审计快照；涉及“下一阶段”或“尚未生成安装包”的表述反映审计时点。当前实现和限制以本 README、`CHANGELOG.md` 与 `tests/manual-smoke-cases.md` 为准。

完整原文固定审计了以下官方仓库版本：

```text
openai/codex@80c6cd3014e4236e99bd06e67f31fcb95c9ee906
obra/superpowers@d884ae04edebef577e82ff7c4e143debd0bbec99
Fission-AI/OpenSpec@0a99f410457271aa773d8b106f03f637f7c6b3c0
```

## 包含内容

```text
config/AGENTS.block.md
roles/sp_*.toml
skills/openspec-superpowers-bridge/
skills/codex-subagent-routing/
skills/codex-delivery-guardrails/
skills/sdd-no-commit-adapter/
tests/
install.py
uninstall.py
Install-CodexWorkflow.ps1
Uninstall-CodexWorkflow.ps1
```

核心原则：

- 全局 `AGENTS` 只保留跨项目稳定基线，简单任务由主线程直接处理；
- 复杂、多步骤或明确要求工作流的任务，才按需使用 `using-superpowers`，且不再建立第二套顶层路由器；
- OpenSpec artifacts 是规格事实来源；
- 同一批 tasks 只有一个实现控制器；
- subagent role 不固定模型，模型按当前工具、availability 和 backend 动态选择；
- 共享工作树只允许一个主要写入所有者；
- 未授权 commit 时不伪装使用原生 commit-centric SDD；
- 完成声明必须有主线程读取的新鲜证据。

## 轻量路由策略

安装后的全局规则不会让每个编程请求都自动进入完整 Skill 链：

- 简单、明确、低风险且可快速验证的任务不启动 Skill、subagent、OpenSpec 或完整计划；
- 只有任务确实需要时才读取 `using-superpowers`；
- OpenSpec bridge、subagent routing、delivery guardrails 和 no-commit adapter 都按真实动作触发，而不是会话启动时预加载；
- 项目级规则和用户当前指令仍可为具体任务启用更严格的流程。

`tests/validate_package.py` 会限制全局块大小，并阻止重新引入“所有编程任务必须先走工作流”的写法。

## 不会自动做什么

安装器不会：

- 安装或升级 Codex、Superpowers、OpenSpec；
- 修改 `~/.codex/config.toml`；
- 启用 `multi_agent_v2` 或任何实验 feature；
- 修改项目仓库；
- 创建 branch、worktree、commit、push、PR 或 workflow；
- 使用网络；
- 覆盖未标记的 `~/.codex/AGENTS.md` 内容。

## 前置条件

- 当前 Codex 支持 Skills 和 subagent；
- Superpowers 已按其官方方式安装，才能使用其原生 Skills；
- 使用 OpenSpec 项目时，OpenSpec CLI 已安装并在 `PATH`；
- Python 3 可用；
- Windows PowerShell 安装入口需要 `python` 或 `py`。

## 安装

先解压并进入目录。

### 只预览

```powershell
.\Install-CodexWorkflow.ps1
```

默认是 dry-run，只显示将写入的位置并运行包校验。

### 实际安装

```powershell
.\Install-CodexWorkflow.ps1 -Apply
```

安装到：

```text
~/.agents/skills/<skill>/
~/.codex/agents/sp_*.toml
~/.codex/AGENTS.md
```

已有同名文件会先备份到：

```text
~/.codex/workflow-backups/<UTC timestamp>/
```

`AGENTS.md` 使用标记块更新，不覆盖其他内容。安装后重新启动 Codex，让 Skills、roles 和全局指令重新加载。

### `AGENTS.md` 合并规则

安装目标是用户级 `~/.codex/AGENTS.md`，不是当前业务项目中的 `AGENTS.md`：

- 文件不存在时：创建文件并写入本包标记块；
- 文件已存在但没有本包标记块时：在原内容后追加本包标记块；
- 文件已存在且包含本包标记块时：只替换该标记块；
- 标记块之外的用户内容始终保留；
- 每次实际写入前都会备份原文件。

本包不包含固定邮箱、用户名、语言或其他个人信息。个人偏好应写在本包标记块之外，或写在项目自己的 `AGENTS.md` / `AGENTS.override.md` 中；后续重新安装不会覆盖这些内容。

## 卸载

预览：

```powershell
.\Uninstall-CodexWorkflow.ps1
```

执行：

```powershell
.\Uninstall-CodexWorkflow.ps1 -Apply
```

卸载器只删除本包已知 Skill 目录、`sp_*.toml` role 和标记的 `AGENTS.md` 区块，并先创建备份。

## 运行校验

```powershell
python .\tests\validate_package.py
python .\tests\run_smoke_tests.py
```

`run_smoke_tests.py` 会：

- 校验 Skill frontmatter、metadata、role TOML 和 AGENTS 大小；
- 在临时 Git repo 验证无 commit snapshot；
- 验证真实 index 和 HEAD 不变；
- 验证 task diff 不包含 task 开始前已有修改；
- 在临时 HOME 验证安装、重复安装和卸载。

`tests/last-smoke-report.json` 是本地生成产物，已由 `.gitignore` 排除，不属于发布源码。

## 无 commit SDD adapter

`sdd-no-commit-adapter` 使用临时 `GIT_INDEX_FILE`：

```text
task start working tree
→ tree object
→ implement
→ task end working tree
→ tree object
→ tree-to-tree review package
```

它不创建 commit、branch、tag 或 ref，也不修改真实 index，但会向 Git object database 写入无引用的 blob/tree objects。

该 adapter 只替换原生 SDD 的 task commit 和 Base..Head diff 机制。它不会替代：

- fresh implementer；
- task reviewer；
- fix / re-review；
- final review；
- 测试；
- 最终交付 commit 决策。

## 角色与模型

包内 role 只定义职责：

```text
sp_readonly_researcher
sp_mechanical_worker
sp_implementation_worker
sp_senior_implementation
sp_task_reviewer
sp_final_reviewer
sp_architect
```

role 文件不写死 `model` 或 `model_reasoning_effort`。`codex-subagent-routing` 会先检查当前工具实际暴露的模型和 multi-agent backend，再尝试以下偏好：

```text
调查：Terra
机械任务：Luna
普通实现：Terra
复杂实现与架构：Sol
最终审查：Sol
```

模型不可用、backend 不兼容或工具不允许覆盖时，会选择兼容 fallback 并披露降级。

## RC1 限制

自动 smoke tests 只能验证文件结构、安装行为和 Git adapter。以下仍需要在真实 Codex 会话中手动验证：

- 当前 Codex 版本能否发现四个 Skills；
- 七个 role 是否出现在当前 `spawn_agent` role 列表；
- 当前主模型能暴露哪些可派发模型；
- v1/v2 生命周期工具是否按 routing Skill 正确选择；
- Superpowers 和 OpenSpec 的实际安装路径是否与当前环境一致；
- 真实项目中 OpenSpec store/profile/schema 的动态解析。

详见 `tests/manual-smoke-cases.md`。

## 开源许可与第三方项目

本项目以 [Apache License 2.0](LICENSE) 开源。第三方项目归属和许可证见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

本仓库不打包复制 Codex、Superpowers 或 OpenSpec 的上游源码。用户需要分别按上游官方方式安装和更新它们。本仓库提供兼容层、Codex roles、workflow Skills、安装器、测试和审计文档。

参与贡献前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)，安全问题请按 [SECURITY.md](SECURITY.md) 提交。版本变化见 [CHANGELOG.md](CHANGELOG.md)。
