---
name: openspec-superpowers-sop
description: 在 Codex 中执行 OpenSpec 与 Superpowers 标准开发流程。
---

# OpenSpec + Superpowers SOP

## 用途

这个 Skill 用于在 Codex 中执行规范化 AI 开发流程。

它组合三件事：

1. OpenSpec：先固定需求、设计、任务和验收标准。
2. Superpowers：使用子代理规划、小步实现、测试优先、完成前验证。
3. Codex：执行代码修改、运行命令、总结结果。

## 总流程

所有非简单代码修改，都必须按以下顺序执行：

1. Explore：先理解项目，不改代码。
2. Propose：创建或读取 OpenSpec change。
3. Subagent Plan：使用子代理分工分析并形成计划。
4. Apply：按确认后的计划小步实现。
5. Verify：运行验证命令和测试。
6. Review：检查 git diff 和风险。
7. Archive：整理证据和复盘材料。

## 阶段一：Explore

目标：先理解项目和问题。

必须做：
- 读取 README。
- 读取 OpenSpec 相关文件。
- 查看当前目录结构。
- 找到可能相关的文件。
- 不修改业务代码。

输出：
- 问题摘要；
- 相关文件；
- 当前不确定点；
- 风险点。

## 阶段二：Propose

目标：先创建 OpenSpec change，不直接写代码。

必须创建或读取：

- openspec/changes/<change-id>/proposal.md
- openspec/changes/<change-id>/design.md
- openspec/changes/<change-id>/tasks.md
- openspec/changes/<change-id>/specs/**/spec.md

必须运行：

```powershell
openspec validate <change-id> --strict
```

如果 validate 不通过，先修 OpenSpec 文件，不进入代码实现。

## 阶段三：Subagent Plan

目标：使用 Superpowers 的子代理方式进行计划。

需要分配四个角色：

需求代理

职责：

- 检查 proposal.md、design.md、tasks.md、spec.md 是否完整。
- 检查验收标准是否可测试。
- 检查 OpenSpec validate 是否通过。

架构代理

职责：

- 设计最小实现方案。
- 避免不必要的框架和依赖。
- 确认第一版不做无关扩展。

测试代理

职责：

- 设计测试用例。
- 明确验证命令。
- 确认输出结果可检查。

审查代理

职责：

- 检查 git diff。
- 检查是否有无关改动。
- 检查是否遗漏测试。
- 检查是否有敏感信息泄露。
- 检查任务是否完成。

每个代理先输出独立结论。
主 Codex 再汇总成一个实现计划。
用户确认前，不修改业务代码。

## 阶段四：Apply

目标：按计划小步实现。

规则：

- 只改当前 OpenSpec change 相关内容。
- 不做无关重构。
- 不引入没有必要的依赖。
- 不跳过测试。
- 每完成一个任务，更新 tasks.md。


## 阶段五：Verify

目标：完成前必须验证。

必须运行：

- openspec validate <change-id> --strict
- 项目运行命令
- 单元测试或最小验证命令

验证结果必须包含：

- 命令；
- 是否成功；
- 失败原因；
- 输出文件是否生成。

验证失败时，不能说完成。

## 阶段六：Review

目标：检查实际改动。

必须运行或查看：

- git status --short
- git diff --stat
- git diff

检查：

- 是否有无关文件；
- 是否超出需求范围；
- 是否缺少测试；
- 是否有硬编码或临时调试代码；
- 是否有敏感信息泄露。

## 阶段七：Archive

目标：沉淀复盘材料。

输出：

- 问题背景；
- 方案设计；
- AI 执行过程；
- 修改文件；
- 验证命令；
- 测试结果；
- 交付结果；
- 剩余风险；
- 可复用经验。
- 停止条件

遇到以下情况必须暂停并询问用户：

- 需求不清楚；
- OpenSpec validate 多次失败；
- 测试失败且原因超出当前范围；
- 需要修改生产执行、安全、权限、认证、价格等高风险逻辑；
- 任务范围变大。
