# 复用指南

两个 Skills 与具体项目无关。迁移到新项目时，原则上只调整 Linear 项目结构、标签映射、证据来源和审查配置，不需要修改 Skill 源码。

## 最简单的复用方式

对于一次性需求整理或只读审查，不需要建立复杂配置。

### 需求整理

提供：

- 目标 Linear 团队或项目；
- 当前会议、反馈、文档或需求材料；
- 是否允许写入。

然后使用：

```text
使用 $linear-project-governance 分析这些材料，
先与当前 Linear 事项对账，只返回候选，不要写入。
```

### 只读审查

提供：

- Linear 项目；
- 可选 GitHub 仓库；
- 时间窗口。

然后使用：

```text
使用 $linear-delivery-audit 审查这个项目最近 30 天的情况，
保持只读，返回问题、证据和建议动作。
```

## 选择单项目还是双项目

### 单项目模式

适合规模较小、需求与执行关系简单的项目。

一个 Linear 项目同时承载：

- 需求、问题、决策、变更和风险；
- 分析、实施、验证和协作任务。

必须通过标签、关系和模板区分治理事项与执行任务。

### 双项目模式

适合长期、复杂或需要严格追溯的项目。

推荐结构：

```text
项目 A：需求与决策
  ├─ 需求
  ├─ 问题
  ├─ 决策
  ├─ 变更
  ├─ 风险
  └─ 待确认问题

项目 B：执行与交付
  ├─ 分析任务
  ├─ 实施任务
  ├─ 验证任务
  └─ 协作任务
```

执行任务通过 Linear 原生关系连接来源事项。

Infinite Canvas 的真实应用采用双项目模式。

## 每个项目需要确定的内容

基础项目映射包括：

- 项目名称、用途、时区和责任人；
- 单项目或双项目模式；
- 精确的 Linear 团队和项目；
- 需求、问题、决策、变更、风险和待确认事项对应的标签；
- 分析、实施、验证和协作任务对应的标签；
- Todo、In Progress、Done、Canceled 等状态映射；
- 执行任务记录来源的字段和原生关系；
- 谁可以批准需求、变更、风险和验收；
- 可选 GitHub 仓库和其他证据来源；
- 允许写入的审查目标。

这些内容应记录在项目自己的治理文档或配置中，不要硬编码进共享 Skill。

## 定期审查的 Profile

只有定期报告、计划任务或自动写入审查结果时，才需要 Profile Schema v4。

可以使用工具生成：

```powershell
cd <installed-linear-delivery-audit-skill>
python -m pip install -r requirements-runtime.txt
python scripts/profile_tool.py init project-profile.json `
  --project-key "demo" `
  --project-name "Demo Project" `
  --timezone "Asia/Shanghai" `
  --owner "Project Owner" `
  --team "Demo Team" `
  --project "Demo Delivery"
```

检查内容后封存：

```powershell
python scripts/profile_tool.py seal project-profile.json `
  --approved-by "Project Owner" `
  --approval-record "APPROVAL-123"
python scripts/profile_tool.py validate project-profile.json
python scripts/profile_tool.py resolve-period project-profile.json
```

Profile 需要明确：

- 项目身份和责任人；
- Linear 项目、标签、状态和关系映射；
- 可选 GitHub 仓库；
- 数据可从哪里流向哪里；
- 审查周期、回看范围和分页方式；
- 报告写入位置；
- 自动化可以写什么、禁止写什么；
- 批准人、修订号和有效期。

Profile 内容变化后需要重新检查和批准。

## 推荐迁移步骤

1. 从同一固定版本安装两个 Skills；
2. 读取现有 Linear 项目、标签、状态和权限；
3. 决定使用单项目还是双项目模式；
4. 先运行一次只返回候选的真实需求整理；
5. 检查分类、重复项和关系是否符合项目习惯；
6. 选择一个低风险计划，确认 Plan ID 并执行；
7. 回读 Linear，确认事项、任务和关系正确；
8. 运行一次只读交付审查；
9. 修正项目自己的标签、模板或映射，不修改共享 Skill 规则；
10. 手动流程稳定后，再启用定期审查。

## 判断是否真正复用成功

成功复用不只是“复制了两段提示词”，而应满足：

- 两个 Skills 不修改源码即可用于新项目；
- 新输入能与现有 Linear 记录对账；
- 正式写入经过人工确认和回读；
- 执行任务能追溯到需求、决策或风险来源；
- 软件任务能够关联 GitHub 代码与测试证据；
- 审查能够发现证据缺失、状态冲突或长期停滞；
- 项目差异只存在于 Linear 结构、标签映射、Profile 和证据来源中。

## 真实参考：Infinite Canvas

Infinite Canvas 已使用相同 Skills 思路建立：

- `Infinite Canvas｜需求与决策`
- `Infinite Canvas｜执行与交付`

其中包含真实决策、实施任务、仓库分析和风险事项，并将 GitHub PR #4 作为软件交付证据来源。这一结构可以作为复杂软件项目迁移时的参考，但其他项目不必复制相同名称或标签。
