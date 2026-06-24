# 仓库级 AI 开发规则

## 沟通规则

- 默认使用中文说明问题、计划、风险和结果。
- 文件名、命令名、函数名、配置项、路径名保留英文。
- 命令、路径、文件内容、提示词必须使用 Markdown 代码块或行内代码标明。
- 如果需求不清楚，先提问，不要猜。
- 发现验证失败、权限失败、依赖缺失或命令不可用时，必须说明失败原因和质量风险。

## 标准流程

所有非简单修改必须按以下顺序执行：

1. Explore：先理解项目和问题，不修改业务代码。
2. Propose：创建或读取 OpenSpec change。
3. Subagent Plan：使用子代理做需求、架构、测试、审查分析，并形成实现计划。
4. Apply：用户确认计划后再小步实现。
5. Verify：完成前运行验证命令和测试。
6. Review：检查 `git status`、`git diff`、范围、风险和临时代码。
7. Archive：沉淀问题、方案、执行、验证和复用经验。

如果全局个人规则与本仓库流程冲突，以本仓库 OpenSpec 流程为准。OpenSpec 的 `proposal.md`、`design.md`、`tasks.md` 和 `specs/**/spec.md` 是本项目的主要计划和进度来源；不要因为全局规则重复创建 `task_plan.md`、`findings.md`、`progress.md`，除非用户明确要求。

## OpenSpec 规则

- `openspec validate <change-id> --strict` 通过前，不要写业务代码。
- 每个功能或修复必须有独立 change id。
- change id 使用英文短横线命名，例如 `add-ai-builder-pack-maker`。
- 每个 change 至少包含：
  - `proposal.md`
  - `design.md`
  - `tasks.md`
  - `specs/**/spec.md`
- OpenSpec 文件中文为主，必要的文件名、命令名、路径名保留英文。

## Superpowers 子代理规则

复杂任务必须分配以下角色：

### 需求代理

- 检查 `proposal.md`、`design.md`、`tasks.md`、`spec.md` 是否完整。
- 检查验收标准是否可测试。
- 检查 OpenSpec validate 是否通过。

### 架构代理

- 设计最小实现方案。
- 避免不必要的框架和依赖。
- 确认第一版不做无关扩展。
- 确认项目结构清晰。

### 测试代理

- 设计测试用例。
- 明确验证命令。
- 覆盖正常路径和失败路径。
- 确认输出结果可检查。

### 审查代理

- 检查 `git status --short`、`git diff --stat` 和实际改动范围。
- 检查是否有无关文件、临时代码、硬编码或敏感信息。
- 检查是否遗漏测试。
- 检查 `tasks.md` 是否按任务完成情况更新。

## 实现规则

- 不要在没有 OpenSpec change 和确认计划的情况下直接改业务代码。
- 不要做无关重构。
- 不要引入没有必要的依赖。
- 不要为了通过测试写死演示值。
- 不要泄露 API key、token、数据库连接、账号、路径等敏感信息。
- 每次修改尽量小步完成。
- 每完成一个任务，应更新对应 OpenSpec `tasks.md`。

## 验证规则

完成前必须运行或记录：

- OpenSpec validate。
- 项目相关测试。
- 最小运行命令。
- `git status --short`。
- `git diff --stat`。

如果验证失败，不能说完成。必须说明失败原因、影响范围和下一步修复建议。

## 高风险停止条件

遇到以下情况必须暂停并询问用户：

- 涉及生产执行。
- 涉及价格、支付、权限、认证、安全策略。
- 涉及数据库结构变更或删除数据。
- 涉及密钥或配置文件。
- 需求范围明显扩大。
- 测试失败且原因超出当前 change 范围。
