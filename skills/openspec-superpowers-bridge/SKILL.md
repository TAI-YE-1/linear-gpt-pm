---
name: openspec-superpowers-bridge
description: 在采用 OpenSpec 的软件项目中桥接 Superpowers 方法与 OpenSpec artifact 生命周期。用于新功能、行为变化、复杂 Bug、规格更新、实施、验证、同步或归档；确保只有一个实现控制器，不生成第二份权威设计或计划。
---

# OpenSpec × Superpowers Bridge

本 Skill 是适配层，不替代 `using-superpowers`、`brainstorming`、`systematic-debugging`、`test-driven-development`、`subagent-driven-development` 或 OpenSpec CLI。

## 1. 触发与边界

在以下任一情况显式使用：

- 当前项目存在可解析的 OpenSpec root；
- 用户点名 OpenSpec、change、artifact、spec、sync 或 archive；
- 当前任务需要建立或更新行为契约；
- 项目规则要求非简单变更必须经过 OpenSpec。

不因目录名猜测固定路径。OpenSpec 可能使用 repo-local root、声明式 store 或外部 store。

开始时读取：

```bash
openspec --version
openspec status --change "<change>" --json
openspec schemas --json
```

需要实施时再运行：

```bash
openspec instructions apply --change "<change>" --json
```

若 change 未确定，使用 `openspec list --json`。存在多个候选时不得猜选。

若 CLI 不存在、root 无法解析或 JSON contract 与本 Skill 不兼容，报告缺口并停止 OpenSpec 写入；可以继续做只读代码调查。

## 2. 权威来源

OpenSpec 模式下：

```text
proposal / specs / design / tasks
= 唯一规格事实来源
```

禁止同时创建或维护：

- 第二份 `docs/superpowers/specs/*` 正式设计；
- 第二份 `docs/superpowers/plans/*` 正式实施计划；
- 与 artifacts 内容不同步的长期 task checklist。

允许创建临时 execution brief，但它只是 artifacts 的可丢弃执行投影，不得引入新业务决策。

## 3. 与 `brainstorming` 的衔接

新功能、行为变化和复杂设计仍使用 `brainstorming` 的方法：

1. 读取真实项目上下文；
2. 逐步澄清目标和约束；
3. 比较重要方案和取舍；
4. 获得设计认可。

在 OpenSpec 模式下覆盖其默认交付动作：

- 不写 `docs/superpowers/specs/*`；
- 不自动 commit；
- 不强制进入 `writing-plans`；
- 将认可后的内容写入当前 schema 要求的 OpenSpec artifacts。

使用 `openspec status --json` 和 `openspec instructions <artifact> --change "<name>" --json` 获取真实 artifact 顺序、模板、依赖、输出路径、context 和 rules。不得硬编码 `proposal → specs → design → tasks`，即使当前默认 schema 通常如此。

`context` 和 `rules` 是生成约束，不复制进 artifact 正文。

## 4. 与 `systematic-debugging` 的衔接

Bug 先执行根因调查，不因项目使用 OpenSpec 就跳过：

1. 复现或读取可靠失败证据；
2. 跟踪真实调用链和数据流；
3. 区分实现缺陷、错误测试假设、环境、依赖、版本和权限问题；
4. 形成可验证的单一根因假设。

以下情况建立或更新 OpenSpec change：

- 修复改变外部行为、接口或数据契约；
- 需要 migration、兼容策略或回滚设计；
- 项目规则要求；
- 风险高且需要可审计决策。

纯环境恢复、错误配置修正或不改变契约的局部实现缺陷，不必机械创建 change，除非项目规则另有要求。

## 5. 选择唯一实现控制器

同一批 OpenSpec tasks 只能由一个实现控制器执行。

### Superpowers 控制实施

这是推荐模式。运行：

```bash
openspec instructions apply --change "<name>" --json
```

读取：

- `schemaName`
- `changeDir`
- `contextFiles`
- `progress`
- `tasks`
- `state`
- `instruction`
- `root`

然后由以下之一实施：

- `subagent-driven-development`
- `executing-plans`
- 主线程顺序实施

禁止再调用完整 `openspec-apply-change` Skill 实现相同 tasks。

### OpenSpec 控制实施

只有用户明确选择 OpenSpec 原生 apply 流程时，才调用 `openspec-apply-change`。此时不要再让 SDD 或其他执行器对同一 tasks 重复实施。

## 6. Execution brief

OpenSpec 标准 `tasks.md` 可能不够细。Superpowers executor 可以从 artifacts 派生临时 brief，每个 task 至少包含：

```text
change 名称和 schema
原始 task id 与原文
相关 requirement / scenario / design decision
已确认的真实代码路径和调用链
拥有的文件或模块
禁止修改的范围
RED 验证或现有失败证据
最小实现步骤
GREEN 验证命令
文档或 artifact 同步要求
停止条件
```

约束：

- brief 不得改变业务含义；
- 路径和测试命令必须通过真实仓库确认；
- 无法从 artifacts 和代码推出的重要决策必须返回主线程；
- brief 默认放临时目录或 `.gitignore` 已覆盖的工作目录，不作为长期权威文档；
- 不自动 commit brief。

## 7. Task 状态同步

完成一个 task 后：

1. 读取实际修改和聚焦验证结果；
2. 确认 task 的全部验收条件已满足；
3. 再将对应 checkbox 从 `- [ ]` 改为 `- [x]`；
4. 重新读取 `openspec instructions apply --json` 或 status，确认进度一致。

不得仅因代码写完、subagent 返回 `DONE` 或测试部分通过就勾选 task。

## 8. Artifact drift

实施发现以下情况时暂停当前实现：

- 规格与真实系统约束冲突；
- 设计决策不可实施或成本显著变化；
- task 缺少必要 migration、回滚或兼容步骤；
- 用户需求发生实质变化；
- 新证据否定原设计。

处理顺序：

```text
记录证据
→ 更新相关 artifact
→ 重新运行 status / instructions
→ 运行 validate
→ 重新生成受影响 brief
→ 继续实施
```

禁止只改代码而让 artifacts 保持已知错误状态。

## 9. 验证门

OpenSpec change 完成至少需要四类证据：

### Artifact 状态

```bash
openspec status --change "<name>" --json
```

确认 apply-required artifacts 和 tasks 状态。

### 规格结构

```bash
openspec validate "<name>" --type change --strict --json
```

`--strict` 代表 warning 也失败，但它主要验证 specs 结构和内容，不证明代码已实现。

### 真实实现

运行风险相称的：

- 静态检查；
- 聚焦测试；
- 集成或 migration 验证；
- 必要时全量回归；
- runtime 或生产等价 dry-run。

### 实现映射

使用 `openspec-verify-change` 或等价过程检查 completeness、correctness 和 coherence。其关键词搜索与推断只能作为辅助证据，不能替代测试和 code review。

最后仍执行 `verification-before-completion`，由主线程读取新鲜输出。

## 10. Sync 与 archive

Sync 前比较 delta specs 与主 specs，说明新增、修改、删除和重命名影响。

默认 archive 门：

- artifacts 完成；
- tasks 全部完成；
- strict validate 通过；
- 必要测试通过；
- blocking review findings 已解决；
- verify 无 CRITICAL；
- 用户已看到未验证项和残余风险。

OpenSpec 上游允许在警告后继续 archive，但本 Skill 默认阻止带未完成 tasks、未解决 CRITICAL 或阻塞验证结果的 archive。只有用户在看到具体风险后明确覆盖，才可继续。

Archive 不授权：

- commit；
- push；
- PR；
- merge；
- 删除分支；
- 部署。

这些动作由 `$codex-delivery-guardrails` 管理。

## 11. 输出要求

每次阶段性汇报必须准确区分：

```text
artifact 已创建
artifact 已验证
task 已勾选
代码已实现
测试已通过
change 已 verify
specs 已 sync
change 已 archive
Git 已 commit / push / merge
```

任何未完成状态不得混写成“OpenSpec 已完成”。
