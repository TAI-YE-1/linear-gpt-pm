# Codex × Superpowers × OpenSpec 上游源码审计报告

审计日期：2026-07-14  
审计目标：设计一套全局 Codex 工程工作流，使不同类型的 subagent 可按任务选择不同模型，同时兼容 Superpowers、OpenSpec 和用户的 Git、测试、CI、生产安全规则。

## 1. 固定审计基线

本报告只依据以下官方仓库及固定 commit：

| 仓库 | 固定 commit |
|---|---|
| `openai/codex` | `80c6cd3014e4236e99bd06e67f31fcb95c9ee906` |
| `obra/superpowers` | `d884ae04edebef577e82ff7c4e143debd0bbec99` |
| `Fission-AI/OpenSpec` | `0a99f410457271aa773d8b106f03f637f7c6b3c0` |

不使用博客、搜索摘要、第三方教程或 Fork 作为架构依据。

---

## 2. 总结结论

原先“`AGENTS.md` + Superpowers + OpenSpec bridge + Codex model policy”的分层方向成立，但早期 v1～v3 设计不能安装，原因有六项：

1. Superpowers 的 `brainstorming`、`writing-plans`、`subagent-driven-development`、`using-git-worktrees` 和 `finishing-a-development-branch` 含有真实的自动写文档、commit、依赖安装、全量测试和分支操作假设，与你的全局规则直接冲突。
2. OpenSpec 的 `openspec-apply-change` 本身是完整实现控制器，不能再让 SDD 对同一批 tasks 实现一次。
3. `openspec validate <change> --strict` 主要验证 delta specs，不验证 proposal、design、tasks 和真实实现是否完成。
4. Codex 当前的 subagent 能力有 v1/v2 两套工具面；Superpowers 自带的 `codex-tools.md` 已不能作为唯一事实来源。
5. Codex 的 custom role 同名会覆盖内置 `worker`、`explorer`，因此全局 profile 必须带命名空间前缀。
6. 不同模型的 multi-agent backend 版本可能不同。固定把 Sol、Terra、Luna 任意互相派发并不可靠，模型路由必须读取当前 `spawn_agent` 暴露的可用模型和 backend 兼容性。

最终系统不应重写一套新的 feature/bug 顶层流程，而应：

```text
AGENTS.md
└─ using-superpowers
   ├─ 原生 Superpowers 方法
   ├─ openspec-superpowers-bridge
   ├─ codex-subagent-routing
   └─ codex-delivery-guardrails
```

其中原生 Superpowers 管开发方法；两个 bridge/policy 解决 OpenSpec、Codex 和用户治理冲突。

---

## 3. Superpowers 13 个 Skill 的源码结论

### 3.1 `using-superpowers`

源码：

- [`skills/using-superpowers/SKILL.md`](https://github.com/obra/superpowers/blob/d884ae04edebef577e82ff7c4e143debd0bbec99/skills/using-superpowers/SKILL.md)

原始行为：

- 编程任务采取任何行动前先检查适用 Skill。
- 过程 Skill 优先于实现 Skill。
- 用户指令和 `AGENTS.md` 高于 Skill。
- 被派发的 subagent 不再调用 `using-superpowers`。

结论：**直接保留，作为唯一顶层入口。**

### 3.2 `brainstorming`

源码：

- [`skills/brainstorming/SKILL.md`](https://github.com/obra/superpowers/blob/d884ae04edebef577e82ff7c4e143debd0bbec99/skills/brainstorming/SKILL.md)

原始行为：

- 新功能、组件、行为变化以及“简单配置修改”都先设计。
- 设计获批前禁止实施。
- 设计完成后写入 `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`。
- commit 设计文档。
- 最后只允许进入 `writing-plans`。

冲突：

- OpenSpec 模式会重复生成 proposal/spec/design。
- 自动 commit 与用户规则冲突。
- 强制进入 `writing-plans` 会与 OpenSpec `tasks.md` 形成双计划。

结论：**保留其澄清、方案比较和设计批准方法，但必须增加 OpenSpec 兼容覆盖。**

OpenSpec 模式下：

```text
不写 docs/superpowers/specs/*
不自动 commit
不进入 writing-plans
将获批设计写入 OpenSpec artifacts
```

无 OpenSpec 模式下可保留设计文档，但 commit 仍需授权。

### 3.3 `systematic-debugging`

源码：

- [`skills/systematic-debugging/SKILL.md`](https://github.com/obra/superpowers/blob/d884ae04edebef577e82ff7c4e143debd0bbec99/skills/systematic-debugging/SKILL.md)

原始行为：

- 根因调查前禁止修复。
- 要求复现、检查近期变化、跨组件采集证据、追踪数据流。
- 形成单一假设并最小化验证。
- 修复阶段调用 TDD。
- 连续三次修复失败后讨论架构问题。

结论：**基本可直接保留。**

需要补充用户规则：

- 区分实现、错误测试假设、依赖环境和版本变化。
- 不能为通过测试修改错误测试来掩盖实现缺陷。

### 3.4 `test-driven-development`

源码：

- [`skills/test-driven-development/SKILL.md`](https://github.com/obra/superpowers/blob/d884ae04edebef577e82ff7c4e143debd0bbec99/skills/test-driven-development/SKILL.md)

原始行为：

- 功能、Bug fix、重构、行为变化必须 TDD。
- 必须先看到因缺失行为而正确失败的 RED。
- 已经提前写出的生产代码原则上删除重来。
- prototype、generated code、configuration 等例外需要向用户确认。

结论：**保留，但按任务类型使用。**

应适用：

- 可测试的新行为；
- Bug 回归；
- API、服务和数据逻辑；
- 行为保持型重构。

不应为了流程强行造测试：

- README、文案、格式化；
- generated code；
- 单纯环境修复；
- 无法稳定自动化的外部系统行为。

这些例外仍需适当验证，并按上游要求获得用户认可。

### 3.5 `writing-plans`

源码：

- [`skills/writing-plans/SKILL.md`](https://github.com/obra/superpowers/blob/d884ae04edebef577e82ff7c4e143debd0bbec99/skills/writing-plans/SKILL.md)

原始行为：

- 生成零上下文工程师也能执行的细粒度计划。
- 每个任务拆成约 2～5 分钟步骤。
- 计划包含准确路径、代码、测试、验证和 commit。
- 结尾要求在 SDD 与 `executing-plans` 中选择。

冲突：

- OpenSpec 项目会形成第二份正式实施计划。
- 计划中频繁 commit 与用户 1～3 个交付提交规则冲突。

结论：**只在没有 OpenSpec 且确实需要正式计划时使用。**

OpenSpec 项目以 artifacts 为权威来源；可以派生临时 execution brief，但不得生成第二份权威计划。

### 3.6 `executing-plans`

源码：

- [`skills/executing-plans/SKILL.md`](https://github.com/obra/superpowers/blob/d884ae04edebef577e82ff7c4e143debd0bbec99/skills/executing-plans/SKILL.md)

原始行为：

- 用于在独立会话顺序执行书面计划。
- 当前平台支持 subagent 时，上游建议改用 SDD。
- 遇到阻塞或不明确内容必须停止。
- 完成后强制进入 `finishing-a-development-branch`。

结论：**条件使用。**

适用：

- 已有完整计划；
- 需要独立会话顺序执行；
- 不使用 subagent 或不允许 SDD checkpoint commits。

不适合简单定义为“紧耦合任务执行器”。高度紧耦合时应修订计划或由主线程顺序实施。

### 3.7 `subagent-driven-development`

源码：

- [`skills/subagent-driven-development/SKILL.md`](https://github.com/obra/superpowers/blob/d884ae04edebef577e82ff7c4e143debd0bbec99/skills/subagent-driven-development/SKILL.md)
- [`implementer-prompt.md`](https://github.com/obra/superpowers/blob/d884ae04edebef577e82ff7c4e143debd0bbec99/skills/subagent-driven-development/implementer-prompt.md)
- [`task-reviewer-prompt.md`](https://github.com/obra/superpowers/blob/d884ae04edebef577e82ff7c4e143debd0bbec99/skills/subagent-driven-development/task-reviewer-prompt.md)
- [`scripts/task-brief`](https://github.com/obra/superpowers/blob/d884ae04edebef577e82ff7c4e143debd0bbec99/skills/subagent-driven-development/scripts/task-brief)
- [`scripts/review-package`](https://github.com/obra/superpowers/blob/d884ae04edebef577e82ff7c4e143debd0bbec99/skills/subagent-driven-development/scripts/review-package)

原始行为：

```text
每 task fresh implementer
→ 实现、测试、commit、自审
→ 基于 BASE..HEAD 生成 review package
→ 一个 task reviewer 返回 spec compliance + code quality
→ Critical / Important 修复并 re-review
→ 所有 tasks 后 whole-branch review
```

SDD 还定义：

```text
DONE
DONE_WITH_CONCERNS
NEEDS_CONTEXT
BLOCKED
```

关键事实：

- SDD 是 commit-centric。
- `review-package` 依赖真实 Base/Head commit。
- progress ledger 也依赖 git log。
- 不允许多个实现 subagent 同时修改同一工作树。
- task reviewer 默认不重复运行已有充分证据的重型测试。

冲突：

- 用户默认不允许自动 commit。
- 用户希望任务包只形成 1～3 个清晰提交。

结论：**不能靠一条 AGENTS 规则把 commit 步骤删掉后仍称为原生 SDD。**

可选模式：

#### 模式 A：原生 SDD

前提全部满足：

- 用户明确允许 subagent；
- 用户明确允许隔离 worktree 中的本地 checkpoint commits；
- 不自动 push；
- 最终交付提交如何整理已经事先约定。

#### 模式 B：无 commit 模式

需要显式 fork/adapter，不能假装原生 SDD 支持。

建议以临时 Git index 生成 task 前后 tree object：

```text
task start tree
→ implementer 修改
→ task end tree
→ git diff-tree 生成 task-specific diff package
```

这不会创建 branch commit 或改动真实 index，但属于需要单独实现和测试的 adapter。

### 3.8 `dispatching-parallel-agents`

源码：

- [`skills/dispatching-parallel-agents/SKILL.md`](https://github.com/obra/superpowers/blob/d884ae04edebef577e82ff7c4e143debd0bbec99/skills/dispatching-parallel-agents/SKILL.md)

原始行为：

- 至少两个真正独立的问题域。
- 无共享状态、顺序依赖和重叠写入。
- 同一派发阶段启动所有独立 subagent。

结论：**保留，但全局默认仅并行只读调查。**

写入并行只有在：

- 不重叠文件所有权；
- 独立 worktree；
- 独立数据库或服务状态；

全部成立时才允许。

### 3.9 `requesting-code-review`

源码：

- [`skills/requesting-code-review/SKILL.md`](https://github.com/obra/superpowers/blob/d884ae04edebef577e82ff7c4e143debd0bbec99/skills/requesting-code-review/SKILL.md)
- [`code-reviewer.md`](https://github.com/obra/superpowers/blob/d884ae04edebef577e82ff7c4e143debd0bbec99/skills/requesting-code-review/code-reviewer.md)

原始行为：

- SDD 每 task 后；
- 重大功能完成后；
- 合并 main 前；
- reviewer 默认只读。

问题：

- 示例使用 `HEAD~1`，不能覆盖多 commit task。
- SDD 自己已使用记录的 Base SHA，后者更可靠。

结论：**保留，统一改为记录真实 Base SHA。**

不重复做相同 task-level review；所有 tasks 后仍做 whole-change review。

### 3.10 `receiving-code-review`

源码：

- [`skills/receiving-code-review/SKILL.md`](https://github.com/obra/superpowers/blob/d884ae04edebef577e82ff7c4e143debd0bbec99/skills/receiving-code-review/SKILL.md)

原始行为：

```text
READ
→ UNDERSTAND
→ VERIFY
→ EVALUATE
→ RESPOND
→ IMPLEMENT
```

结论：**直接保留。**

### 3.11 `verification-before-completion`

源码：

- [`skills/verification-before-completion/SKILL.md`](https://github.com/obra/superpowers/blob/d884ae04edebef577e82ff7c4e143debd0bbec99/skills/verification-before-completion/SKILL.md)

原始行为：

- 完成声明前必须在当前消息中得到新鲜完整验证输出。
- 不相信 subagent 的成功声明。
- 检查 VCS diff。
- 在 commit、PR、task 完成和进入下一任务前都适用。

结论：**直接保留，但增加 verification ledger 去重。**

Ledger 至少记录：

```text
命令
工作树或 tree hash
执行时间
结果
之后是否有相关代码变化
```

Task 只跑聚焦测试；包关闭或发布前再运行一次所需全量测试。

### 3.12 `using-git-worktrees`

源码：

- [`skills/using-git-worktrees/SKILL.md`](https://github.com/obra/superpowers/blob/d884ae04edebef577e82ff7c4e143debd0bbec99/skills/using-git-worktrees/SKILL.md)

原始行为：

- 先检测当前隔离。
- 没有偏好时询问位置。
- 默认可选择 `.worktrees/`。
- 若未被 ignore，会修改 `.gitignore` 并 commit。
- 根据 manifest 存在自动执行 `npm install`、`cargo build`、`pip install` 等。
- 运行 baseline tests。

冲突：

- 自动 commit；
- 仅凭 manifest 猜依赖命令；
- 未经必要性判断安装依赖。

结论：**必须由 delivery guardrails 覆盖。**

### 3.13 `finishing-a-development-branch`

源码：

- [`skills/finishing-a-development-branch/SKILL.md`](https://github.com/obra/superpowers/blob/d884ae04edebef577e82ff7c4e143debd0bbec99/skills/finishing-a-development-branch/SKILL.md)

原始行为：

- 重新运行全量测试。
- 提供 merge、push+PR、keep、discard。
- 按用户选择执行 pull/merge/push/删除分支或 worktree。

结论：**只在真正结束或集成分支时调用。**

完成 Phase、Package 或 OpenSpec change 不等于结束长期开发分支。

---

## 4. OpenSpec 源码结论

### 4.1 实际 profile 不能硬编码

源码：

- [`src/core/profiles.ts`](https://github.com/Fission-AI/OpenSpec/blob/0a99f410457271aa773d8b106f03f637f7c6b3c0/src/core/profiles.ts)
- [`src/core/init.ts`](https://github.com/Fission-AI/OpenSpec/blob/0a99f410457271aa773d8b106f03f637f7c6b3c0/src/core/init.ts)
- [`docs/agent-contract.md`](https://github.com/Fission-AI/OpenSpec/blob/0a99f410457271aa773d8b106f03f637f7c6b3c0/docs/agent-contract.md)

事实：

- 源码的 core profile 当前包括 `update`。
- 部分官方文档仍未列出 `update`。
- 支持 custom profile。
- artifact graph、context files、路径和约束都通过 JSON 动态给出。
- OpenSpec 还支持外部 store，不一定是当前仓库内的固定 `openspec/changes` 路径。

结论：bridge 必须先运行：

```bash
openspec --version
openspec status --change "<name>" --json
openspec instructions apply --change "<name>" --json
openspec schemas --json
```

并检查当前实际生成的 `openspec-*` Skills。

### 4.2 `openspec-propose` 与 brainstorming

源码：

- [`src/core/templates/workflows/propose.ts`](https://github.com/Fission-AI/OpenSpec/blob/0a99f410457271aa773d8b106f03f637f7c6b3c0/src/core/templates/workflows/propose.ts)

它会根据 schema 的依赖图生成所有 apply-ready artifacts。

结论：

- `brainstorming` 负责需求澄清、方案和设计批准。
- `openspec-propose` 负责将批准结果写入动态 artifacts。
- 不能各自生成一套正式设计。

### 4.3 `openspec-apply-change` 是完整实现控制器

源码：

- [`src/core/templates/workflows/apply-change.ts`](https://github.com/Fission-AI/OpenSpec/blob/0a99f410457271aa773d8b106f03f637f7c6b3c0/src/core/templates/workflows/apply-change.ts)

它会：

```text
读取 contextFiles
→ 遍历 pending tasks
→ 修改代码
→ 勾选 task
→ 继续下一 task
```

结论：若使用 Superpowers executor，不调用该 Skill 完整实现。

正确做法：

```text
调用 openspec instructions apply --json 获取任务和上下文
→ 生成非权威 execution brief
→ 由唯一 Superpowers executor 实现
→ 同步更新 tasks
```

### 4.4 `tasks.md` 不是足够详细的 SDD plan

源码和文档：

- [`docs/getting-started.md`](https://github.com/Fission-AI/OpenSpec/blob/0a99f410457271aa773d8b106f03f637f7c6b3c0/docs/getting-started.md)

标准 `tasks.md` 通常只是 checklist。

结论：

```text
OpenSpec artifacts
= 唯一规格事实来源

execution brief
= 可丢弃、非权威的执行投影
```

Brief 可以补全准确路径、RED/GREEN、验证命令和文件所有权，但不能引入新业务决策。

### 4.5 `validate --strict` 的真实语义

源码：

- [`src/commands/validate.ts`](https://github.com/Fission-AI/OpenSpec/blob/0a99f410457271aa773d8b106f03f637f7c6b3c0/src/commands/validate.ts)
- [`src/core/validation/validator.ts`](https://github.com/Fission-AI/OpenSpec/blob/0a99f410457271aa773d8b106f03f637f7c6b3c0/src/core/validation/validator.ts)

事实：

- `validate <change>` 当前调用 `validateChangeDeltaSpecs`。
- 主要验证 delta sections、SHALL/MUST、scenarios 等。
- 普通模式只有 ERROR 失败。
- `--strict` 模式 WARNING 也失败。
- 它不验证 proposal/design/tasks 是否完整，不验证代码是否实现。

结论：不能把它当作整个 change 的完成门。

### 4.6 `openspec-verify-change` 是辅助审查，不是测试替代品

源码：

- [`src/core/templates/workflows/verify-change.ts`](https://github.com/Fission-AI/OpenSpec/blob/0a99f410457271aa773d8b106f03f637f7c6b3c0/src/core/templates/workflows/verify-change.ts)

它检查：

```text
completeness
correctness
coherence
```

实现映射主要依赖代码搜索、关键词和合理判断。

结论：必须与真实测试、diff review 和 runtime validation 配套。

### 4.7 archive 默认只警告

源码：

- [`src/core/templates/workflows/archive-change.ts`](https://github.com/Fission-AI/OpenSpec/blob/0a99f410457271aa773d8b106f03f637f7c6b3c0/src/core/templates/workflows/archive-change.ts)

未完成 artifacts/tasks 时默认：

```text
warning
→ 用户确认
→ 仍可 archive
```

结论：你的规则可以更严格，但必须明确这是自定义治理：

```text
默认不允许带未完成 artifacts/tasks 或阻塞验证结果 archive
```

只有用户在看到风险后明确覆盖，才允许继续。

---

## 5. Codex 当前源码结论

### 5.1 subagent 共享同一工作目录

源码：

- [`codex-rs/core/src/config/mod.rs`](https://github.com/openai/codex/blob/80c6cd3014e4236e99bd06e67f31fcb95c9ee906/codex-rs/core/src/config/mod.rs)

当前提示明确：

```text
所有 agent 共享同一 container/filesystem
所有 agent 使用相同 cwd
一个 agent 的编辑立即对其他 agent 可见
```

结论：默认并行写入不安全。

### 5.2 full-history fork 不能切模型

源码：

- [`multi_agents_common.rs`](https://github.com/openai/codex/blob/80c6cd3014e4236e99bd06e67f31fcb95c9ee906/codex-rs/core/src/tools/handlers/multi_agents_common.rs)
- [`multi_agents/spawn.rs`](https://github.com/openai/codex/blob/80c6cd3014e4236e99bd06e67f31fcb95c9ee906/codex-rs/core/src/tools/handlers/multi_agents/spawn.rs)

事实：

- full-history fork 继承父 agent type、model、reasoning effort。
- full-history 时显式覆盖会被拒绝。
- 跨模型 subagent 必须使用无历史或有限历史 fork，并传入自包含 brief。

结论：这与 SDD 的 task brief 设计天然兼容；不能复制整个会话再要求换模型。

### 5.3 v1/v2 工具面不同

源码：

- [`multi_agents_spec.rs`](https://github.com/openai/codex/blob/80c6cd3014e4236e99bd06e67f31fcb95c9ee906/codex-rs/core/src/tools/handlers/multi_agents_spec.rs)

事实：

- v1 暴露 `close_agent`、`resume_agent` 等。
- v2 主要使用 task-path 形式的 `spawn_agent`、`followup_task`、`send_message`、`wait_agent`、`interrupt_agent`、`list_agents`。
- 不能把固定的 `spawn → wait → close` 写死为所有版本生命周期。

结论：model policy 必须运行时检查当前可用工具。

### 5.4 模型 backend 必须兼容

源码：

- [`multi_agents_common.rs`](https://github.com/openai/codex/blob/80c6cd3014e4236e99bd06e67f31fcb95c9ee906/codex-rs/core/src/tools/handlers/multi_agents_common.rs)
- [`models.json`](https://github.com/openai/codex/blob/80c6cd3014e4236e99bd06e67f31fcb95c9ee906/codex-rs/models-manager/models.json)

事实：

- v2 只允许选择支持 v2 backend 的 model。
- 固定目录中 Sol 标注为 v2，Luna 标注为 v1。
- 因此“任何主模型都能任意派发 Sol/Terra/Luna”不成立。

结论：路由顺序必须是：

```text
任务风险分类
→ 查询 spawn_agent 暴露的当前可用模型
→ 过滤 backend 兼容模型
→ 选择首选模型
→ 不可用时选择同职责 fallback
→ 披露降级
```

### 5.5 role 不应固定 model

源码：

- [`agent/role.rs`](https://github.com/openai/codex/blob/80c6cd3014e4236e99bd06e67f31fcb95c9ee906/codex-rs/core/src/agent/role.rs)

事实：

- role 在 spawn 时作为高优先级配置层应用。
- role 中固定的 model/reasoning 会被标记为不可修改。
- user-defined role 优先于 built-in role。

结论：

- profile 只定义职责和行为。
- model/reasoning 由 routing Skill 在 spawn 时动态指定。
- 这样才能支持 availability fallback。

### 5.6 role 名称不能覆盖 built-in

源码同上。

内置：

```text
default
explorer
worker
```

user-defined 同名优先。

结论：自定义名称应使用：

```text
sp_readonly_researcher
sp_implementation_worker
sp_senior_implementation
sp_task_reviewer
sp_final_reviewer
sp_architect
```

### 5.7 role 不是可靠安全边界

源码：

- [`multi_agents/spawn.rs`](https://github.com/openai/codex/blob/80c6cd3014e4236e99bd06e67f31fcb95c9ee906/codex-rs/core/src/tools/handlers/multi_agents/spawn.rs)
- [`multi_agents_common.rs`](https://github.com/openai/codex/blob/80c6cd3014e4236e99bd06e67f31fcb95c9ee906/codex-rs/core/src/tools/handlers/multi_agents_common.rs)

role 配置应用后，Codex 又把 live turn 的 approval policy、permission profile、cwd 等 runtime state 应用到 child。

结论：不能仅靠 role 中的 `sandbox_mode = "read-only"` 声称 reviewer 一定无法写入。

应同时：

- 父线程使用适当权限；
- reviewer prompt 明确只读；
- 完成后检查工作树；
- 不能把 prompt 约束当成安全沙箱。

### 5.8 当前无需强制开启 `multi_agent`

源码：

- [`codex-rs/features/src/lib.rs`](https://github.com/openai/codex/blob/80c6cd3014e4236e99bd06e67f31fcb95c9ee906/codex-rs/features/src/lib.rs)

事实：

- `multi_agent` 当前是 Stable，默认启用。
- `multi_agent_v2` 仍是 UnderDevelopment，默认关闭。

结论：安装器不应无条件重写：

```toml
[features]
multi_agent = true
multi_agent_v2 = true
```

只检测当前能力；不得擅自启用 under-development 功能。

### 5.9 AGENTS.md 必须精简

源码：

- [`agents_md.rs`](https://github.com/openai/codex/blob/80c6cd3014e4236e99bd06e67f31fcb95c9ee906/codex-rs/core/src/agents_md.rs)
- [`config/mod.rs`](https://github.com/openai/codex/blob/80c6cd3014e4236e99bd06e67f31fcb95c9ee906/codex-rs/core/src/config/mod.rs)

事实：

- 项目文档总预算默认 32 KiB，超出会截断。
- 每层目录只选择 `AGENTS.override.md`、`AGENTS.md` 或 fallback 中第一个存在文件。
- 从项目 root 到 cwd 顺序加载。
- 全局用户指令与项目文档合并。

结论：完整流程必须放 Skill，不放全局 `AGENTS.md`。

### 5.10 Skills 的真实加载路径

源码：

- [`core-skills/src/loader.rs`](https://github.com/openai/codex/blob/80c6cd3014e4236e99bd06e67f31fcb95c9ee906/codex-rs/core-skills/src/loader.rs)

当前路径包括：

```text
$HOME/.agents/skills
$CODEX_HOME/skills          # deprecated compatibility
项目 config folder/skills  # 通常 .codex/skills
项目 root 到 cwd 各层 .agents/skills
plugin skill roots
```

`agents/openai.yaml` 支持：

```yaml
policy:
  allow_implicit_invocation: false
```

结论：两个自定义 bridge/policy 应禁止隐式调用，由 `AGENTS.md` 或上游流程显式调用，减少误触发。

---

## 6. 最终建议架构

### 6.1 全局 `AGENTS.md`

只保留：

```text
1. 编程入口使用 using-superpowers
2. OpenSpec 项目显式调用 openspec-superpowers-bridge
3. 派发 subagent 前显式调用 codex-subagent-routing
4. commit/worktree/CI/完成/分支操作遵循 codex-delivery-guardrails
5. 真实代码和证据优先
6. 生产、数据、权限、费用与外部动作停止条件
7. 完成汇报和 Gmail 条件
```

### 6.2 `openspec-superpowers-bridge`

职责：

- 检测实际 OpenSpec root、store、schema、profile 和 generated Skills。
- 将 brainstorming 的获批设计写入 OpenSpec artifacts。
- 禁止生成第二份正式设计和计划。
- 使用 `instructions apply --json` 而不是调用完整 `openspec-apply-change`。
- 从 artifacts 生成临时 execution brief。
- 管理 artifact drift。
- 组合 status、strict validate、tests、review 和 verify。
- 按用户更严格策略门控 archive。

### 6.3 `codex-subagent-routing`

职责：

- 判断任务需要 research、mechanical implementation、normal implementation、senior implementation、task review、final review 或 architecture。
- 检查当前 tool version。
- 检查当前 spawn 可用模型和 backend 兼容性。
- 用无历史或有限历史 fork 派发跨模型 task。
- 传入自包含 brief。
- 处理 `DONE / DONE_WITH_CONCERNS / NEEDS_CONTEXT / BLOCKED`。
- 控制 read parallel / write serial。
- 使用 prefixed role 名称。
- 不在 role TOML 中固定 model。

### 6.4 `codex-delivery-guardrails`

职责：

- 未经授权禁止 commit、push、merge。
- 判断是否允许原生 SDD checkpoint commits。
- 控制 worktree 同意、`.gitignore` 和依赖安装。
- 管理 1～3 个交付提交。
- 审计 GitHub Actions 触发、权限和额度。
- verification ledger 和重型测试去重。
- 只有真正 branch closeout 才调用 `finishing-a-development-branch`。
- 区分 OpenSpec archive 与 Git branch lifecycle。

### 6.5 可选 `sdd-no-commit-adapter`

如果必须在不允许 commit 的情况下使用 fresh implementer + task reviewer，需要单独实现，不能只靠 prompt 覆盖。

它应保留上游 SDD 的：

- pre-flight review；
- fresh implementer；
- task reviewer 双 verdict；
- fix/re-review；
- final review；
- status protocol。

只替换：

- task commit；
- commit-based progress ledger；
- Base..Head review package。

---

## 7. 推荐模型路由

不要将模型写死在 role 文件中。推荐逻辑：

| 任务 | 首选 | 降级原则 |
|---|---|---|
| 只读代码调查 | Terra `medium` | 当前 backend 可用的日常模型 |
| 明确机械任务 | Luna `medium` | Luna backend 不兼容时用 Terra `low/medium` |
| 普通实现 | Terra `high` | 可用日常模型 |
| 复杂事务、并发、迁移 | Sol `high` | 可用最强模型 |
| 单 task review | Terra `high` | 高风险时升级 Sol |
| whole-change / release review | Sol `high` | 极复杂时 `xhigh` |
| 架构 | Sol `high/xhigh` | 根据复杂度调整 |

必须先检查当前模型是否对当前 multi-agent backend 可用。

---

## 8. 必须通过的流程测试

最终安装包生成前，至少验证：

| 场景 | 预期 |
|---|---|
| README 小改 | 不建 OpenSpec、不派 subagent、不 commit |
| 无 OpenSpec 新功能 | brainstorming → writing-plans |
| OpenSpec 新功能 | brainstorming 方法 → OpenSpec，不生成第二份 plan |
| 普通 Bug | systematic-debugging → TDD |
| 三个独立失败 | 可并行只读调查，写入串行 |
| 未授权 commit | 不使用原生 commit-centric SDD |
| 授权 checkpoint commits | isolated worktree + native SDD |
| PR feedback | receiving-code-review，先验证再改 |
| workflow 修改 | 检查触发器、权限、额度 |
| 完成一个 Phase | 不自动 branch finishing |
| 真正准备 merge | finishing-a-development-branch |
| strict validate 通过但代码未实现 | 不得声称完成 |
| verify 只有启发式证据 | 仍要求真实测试 |
| archive 有未完成 tasks | 默认阻止，明确授权后才覆盖 |
| Sol v2 会话想派发 Luna v1 | 路由检测不兼容并 fallback |
| full-history fork + model override | 禁止，改用 self-contained brief |
| custom role 名称 | 不覆盖 `worker`/`explorer` |
| subagent 报告 DONE 无验证 | 主线程不得声称完成 |

---

## 9. 最终判断

应保留：

- `using-superpowers`
- `systematic-debugging`
- `test-driven-development`
- `receiving-code-review`
- `verification-before-completion`
- SDD 的 fresh subagent、双 verdict reviewer、fix/re-review、final review 思想

必须条件化或覆盖：

- `brainstorming`
- `writing-plans`
- `executing-plans`
- `subagent-driven-development`
- `dispatching-parallel-agents`
- `requesting-code-review`
- `using-git-worktrees`
- `finishing-a-development-branch`
- `openspec-apply-change`
- `openspec-archive-change`

必须新增：

- `openspec-superpowers-bridge`
- `codex-subagent-routing`
- `codex-delivery-guardrails`
- 可选 `sdd-no-commit-adapter`

当前不应生成一键安装包。下一阶段应先编写这三项 Skill 的规范、无 commit SDD 是否需要的决策，以及上面的 smoke-test harness，再生成最终全局配置。
