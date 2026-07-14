<!-- CODEX-SUPERPOWERS-OPENSPEC-V4:START -->
# Codex 全局工程协作规则

> 适用于编程、仓库维护、测试、调试、代码审查、技术设计、OpenSpec 和发布准备。
> 项目内更具体的 `AGENTS.override.md`、`AGENTS.md`、安全规则和真实仓库约束优先。

## 入口与分层

- 编程任务开始时，若 `using-superpowers` 可用，先读取并遵循它；不要创建另一套顶层 feature、bug 或 review 路由器。
- 项目存在 OpenSpec root、用户提到 OpenSpec，或当前任务涉及 OpenSpec artifacts 时，显式调用 `$openspec-superpowers-bridge`。
- 任一流程准备派发 Codex subagent 前，显式调用 `$codex-subagent-routing`。
- 涉及 commit、worktree、CI、验证关闭、分支收尾或外部动作时，显式调用 `$codex-delivery-guardrails`。
- 被派发的 subagent 不再调用 `using-superpowers`；它只执行父线程给出的自包含任务。

## 真实证据优先

- 默认使用中文说明计划、发现、风险、修改和验证；路径、命令、函数、接口和配置名保留英文。
- 修改前读取真实代码、配置、测试、调用链、依赖版本和适用文档，不得按常见写法猜测。
- 先区分实现缺陷、错误测试假设、依赖或环境问题、版本变化以及权限或外部系统问题。
- 不得把计划、推测、subagent 报告或未运行的验证描述为已完成。
- 用户已有修改属于用户；不得覆盖、回退或清理无关改动。

## 实现与 subagent

- 简单、明确、低风险且可快速验证的任务由主线程直接完成。
- 只读且真正独立的调查可以并行；共享工作树中的写入默认串行。
- 同一工作树只保留一个主要写入所有者；并行写入必须使用独立 worktree 或完全不重叠的文件与状态。
- 跨模型 subagent 使用无历史或有限历史 fork，并传入自包含 brief；不要复制整个父会话后再要求覆盖模型。
- profile 只定义职责。模型和推理强度由 `$codex-subagent-routing` 根据当前工具暴露的可用模型与 backend 兼容性动态选择。
- 父线程必须核对 diff、验证证据和未确认项，不能直接相信 subagent 的 `DONE`。

## OpenSpec

- OpenSpec artifacts 是规格事实来源；不得同时维护第二份正式设计或实施计划。
- `brainstorming` 可用于澄清、方案比较和设计批准；在 OpenSpec 模式下将结果写入 artifacts，不自动写 `docs/superpowers/specs/*`，不自动 commit，也不强制进入 `writing-plans`。
- 使用 Superpowers executor 时，只通过 `openspec instructions apply --change "<name>" --json` 获取任务和上下文；不要再调用完整 `openspec-apply-change` 实现同一批 tasks。
- `openspec validate --strict`、`openspec verify-change` 和真实测试各自承担不同职责，不能相互替代。
- OpenSpec archive 与 Git branch 生命周期是两件事；归档 change 不等于合并、推送或删除分支。

## Git、测试与 CI

- 未经用户明确授权，不得 commit、push、merge、rebase、强推、切换分支、删除分支、部署、重置或丢弃修改。
- 原生 `subagent-driven-development` 的 checkpoint commits 只有在用户明确允许且使用隔离 worktree 时才可启用。
- 未授权 commit 时，使用主线程顺序实施，或显式调用 `$sdd-no-commit-adapter`；不得假装原生 SDD 不需要 commit。
- 不修改测试来掩盖实现缺陷。
- 普通修改优先运行静态检查和聚焦测试；跨模块、数据库、权限、依赖锁、阶段关闭或发布前再扩大验证。
- 记录验证命令、tree 状态、时间和结果；相关代码未变化时不重复运行同一重型验证。
- 修改 `.github/workflows` 或准备触发 Actions 前，检查触发器、权限、secrets、重复执行和额度；不默认新增每次 push 或 PR 都运行的重型工作流。
- 只有真正准备集成或关闭开发分支时才使用 `finishing-a-development-branch`，完成 Phase、Package 或 OpenSpec change 本身不触发该 Skill。

## 高风险边界

分析、设计、未执行的代码、migration 草案、查询、dry-run 和回滚方案可以继续。

以下真实执行必须先说明风险并获得确认，除非用户当前指令已经明确授权该具体动作：

- 生产部署或生产数据库写入；
- 删除、覆盖、迁移或批量更新真实数据；
- 修改真实权限、认证、密钥或证书；
- 调用会产生费用或真实副作用的外部 API；
- 发送真实邮件、消息或通知；
- 修改价格、订单、支付、退款或结算；
- 强推、改写历史或其他明显不可逆操作。

## 完成标准

声称完成前必须：

- 需求范围已实际处理；
- 修改已落盘；
- 运行与风险相称的新鲜验证并读取结果；
- 检查 `git status --short` 和相关 diff；
- 明确未运行验证、未确认事项和残余风险；
- 准确说明 commit、push、PR、merge、archive、部署和外部动作状态。

任务真正完成、必要验证通过、当前环境存在 Gmail connector，且能够确认本次任务实际耗时不少于 10 分钟时，向 `2622027746@qq.com` 发送真实完成状态提醒。否则不发送，也不得声称已发送。
<!-- CODEX-SUPERPOWERS-OPENSPEC-V4:END -->
