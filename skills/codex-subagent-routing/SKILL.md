---
name: codex-subagent-routing
description: 在 Codex 准备派发 subagent 时，按任务职责、当前工具版本、模型可用性和 multi-agent backend 兼容性选择 role、模型、推理强度、上下文模式、并发方式和状态处理。适用于 SDD、并行调查、架构、实现和代码审查；不替代 using-superpowers。
---

# Codex Subagent Routing

本 Skill 只负责 Codex subagent 的职责、模型、上下文和生命周期。流程顺序仍由已选中的 Superpowers Skill 或 OpenSpec bridge 决定。

## 1. 先检查当前能力

首次派发前读取当前会话实际暴露的 collaboration / multi-agent 工具 schema，确认：

- 使用 v1 还是 v2 工具面；
- `spawn_agent` 支持哪些参数；
- 当前可用 role；
- 当前可选 model 与 reasoning effort；
- 是否支持 full-history、limited-history 或 no-history fork；
- 可用 wait、message、follow-up、interrupt、close 或 list 操作；
- 当前线程和深度限制。

不要：

- 依赖旧版 `codex-tools.md` 推断当前工具；
- 无条件修改 `[features]`；
- 擅自启用 `multi_agent_v2`；
- 假设 Sol、Terra、Luna 在当前 backend 都可派发；
- 假设 v1 和 v2 生命周期命令相同。

若 subagent 工具不可用，返回主流程，由主线程完成任务或说明能力缺口。

## 2. Role 只定义职责

优先使用以下自定义 role：

| Role | 职责 |
|---|---|
| `sp_readonly_researcher` | 只读代码、配置、测试、日志和调用链取证 |
| `sp_mechanical_worker` | 边界明确的机械修改 |
| `sp_implementation_worker` | 普通功能、Bug 和多文件实现 |
| `sp_senior_implementation` | 并发、事务、迁移、状态机和高复杂度实现 |
| `sp_task_reviewer` | 单 task 的 spec compliance 与 code quality 审查 |
| `sp_final_reviewer` | whole-change、阶段关闭和发布前审查 |
| `sp_architect` | 架构、数据库、权限、部署和重大重构分析 |

role 文件不固定 model。若当前工具不支持 `agent_type` 或 role 未加载，将相同职责约束完整写入 task brief，不伪造 role 已生效。

不要创建或调用同名自定义 `worker`、`explorer` 覆盖 Codex 内置角色。

## 3. 动态模型选择

先按任务确定能力等级，再从当前 `spawn_agent` 实际暴露且 backend 兼容的模型中选择。

推荐优先级：

| 任务 | 首选 |
|---|---|
| 只读调查 | Terra `medium` |
| 机械任务 | Luna `medium` |
| 普通实现 | Terra `high` |
| 复杂实现 | Sol `high` |
| 单 task review | Terra `high` |
| 高风险 task review | Sol `high` |
| whole-change / release review | Sol `high` 或 `xhigh` |
| 架构 | Sol `high` 或 `xhigh` |

这些只是偏好，不是静态保证。

选择顺序：

```text
任务风险与复杂度
→ 当前工具暴露的模型
→ 当前 multi-agent backend 兼容过滤
→ reasoning effort 支持检查
→ 首选模型
→ 同职责 fallback
```

fallback 规则：

- Luna 不可用或 backend 不兼容：机械任务使用 Terra `low/medium` 或当前兼容的最低合理模型；
- Terra 不可用：普通任务使用当前兼容的日常模型；
- Sol 不可用：使用当前最强兼容模型，并披露降级；
- 不允许模型覆盖：继承父模型，但仍应用职责 prompt；
- 同一输入因推理不足 `BLOCKED`：升级能力等级，不原样重复派发。

## 4. Context 模式

### Full-history fork

只在以下全部成立时使用：

- 子任务确实依赖完整父会话；
- 不需要覆盖 role、model 或 reasoning effort；
- 上下文污染风险可接受；
- 当前工具明确支持。

full-history fork 继承父 agent type、model 和 reasoning effort。不得同时请求这些覆盖。

### Limited-history 或 no-history fork

以下情况必须使用：

- 需要切换模型或 reasoning effort；
- 需要选择特定 role；
- SDD fresh implementer / reviewer；
- 多个独立调查；
- 父会话包含大量无关历史；
- 希望可复现、可审计的 task brief。

跨模型委派默认使用 no-history 或最小有限历史，并传入自包含 brief。

## 5. 自包含 task brief

每次派发至少包含：

```text
任务目标
为什么派发
任务类型和期望 role
OpenSpec change / task id（若适用）
真实代码路径和已确认调用链
允许读取范围
拥有的写入文件或模块
禁止修改范围
用户已有修改和共享工作树提示
已确认事实与证据
待验证假设
实现或审查标准
聚焦验证命令
禁止的外部动作
输出格式
停止条件
```

实现 agent 还要明确：

```text
你不是代码库中的唯一参与者
不得回退或覆盖他人修改
不得 commit / push，除非 brief 明确授权
发现范围外问题只报告，不顺手扩大修改
```

reviewer 还要明确：

```text
默认只读
先 findings，按严重度排序
每项包含文件、符号或行、触发条件、影响、证据和修复建议
区分 blocking finding、warning 和 residual risk
除非 brief 要求，不重复运行 implementer 已提供的新鲜重型测试
```

## 6. 并发与所有权

Codex subagent 共享同一 filesystem 和 cwd。

默认：

```text
只读独立调查：可并行
共享工作树写入：串行
```

并行写入只在以下全部成立时允许：

- 独立 worktree，或文件与状态完全不重叠；
- 每个 agent 有明确所有权；
- 不共享数据库、生成目录、锁文件或服务状态；
- 不会互相运行格式化或全局生成命令；
- 主线程能可靠整合。

不要为了“用了 subagent”而拆分简单任务。

## 7. 任务状态协议

实现 agent 必须返回：

### `DONE`

包括：

- 修改文件；
- 关键实现说明；
- 实际运行的命令；
- 结果摘要；
- 自审发现；
- 未验证内容；
- 是否触碰授权边界。

父线程进入 diff 检查和 review，不直接声明完成。

### `DONE_WITH_CONCERNS`

实现完成但有非阻塞或待判断疑虑。父线程先分类：

- 正确性、范围、安全或数据风险：先处理；
- 非阻塞观察：记录后进入审查。

### `NEEDS_CONTEXT`

缺少真实接口、字段、环境状态、用户决策或必要 artifact。父线程补充后使用新 brief 重派。

### `BLOCKED`

必须给出原因类别：

- capability；
- context；
- task too large；
- reasoning complexity；
- plan/spec defect；
- environment；
- permission；
- external dependency。

同一模型和相同输入不得机械重试。

reviewer 必须返回：

```text
SPEC_VERDICT: PASS | FAIL | NEEDS_CONTEXT
QUALITY_VERDICT: PASS | FAIL | NEEDS_CONTEXT
FINDINGS:
RESIDUAL_RISKS:
TEST_EVIDENCE_ASSESSED:
```

## 8. SDD 适配

使用原生 `subagent-driven-development` 时保持其核心顺序：

```text
pre-flight plan review
→ fresh implementer
→ implementation + tests + self-review
→ task review
→ fix / re-review
→ next task
→ whole-change review
```

但在开始前必须由 `$codex-delivery-guardrails` 选择：

- 原生 checkpoint-commit 模式；
- `$sdd-no-commit-adapter`；
- 主线程顺序实施。

若未授权 commit，不得把原生 SDD 的 commit 和 Base..Head review package 静默删除。

## 9. Lifecycle

### v1

只调用当前实际存在的操作，例如：

- spawn；
- wait；
- send input；
- resume；
- close。

已完成 agent 可能继续占用线程名额时，应在读取结果后关闭。

### v2

使用当前实际存在的 task-path 操作，例如：

- spawn；
- send message；
- follow-up task；
- wait；
- interrupt；
- list。

若没有 close 操作，不调用不存在的命令。按当前 runtime 的完成和并发语义管理 task。

任何版本都不得无限轮询。等待超时后检查状态，继续其他不依赖工作，或报告真实 blocker。

## 10. 主线程责任

主线程始终负责：

- 选择是否委派；
- 生成和审查 brief；
- 判断模型降级是否可接受；
- 检查共享工作树变化；
- 读取 subagent 证据；
- 处理冲突和越界；
- 运行必要的新鲜最终验证；
- 做最终完成判断。

subagent 只提供受限任务结果，不拥有最终事实裁决权。
