# 复用指南

两个 Skills 与具体项目解耦。迁移到新项目时，通常只调整 Linear 项目结构、标签、关系、证据来源和审查配置，不需要修改 Skill 源码。

## 先选择使用深度

### 只整理一次需求

适合会议纪要、用户反馈或一次需求变更。

只需提供：

- 目标 Linear 团队或项目；
- 当前工作材料；
- 是否允许写入。

```text
使用 $linear-project-governance 分析这些材料。
先与当前 Linear 事项对账，只返回候选，不要写入。
```

### 只做一次交付审查

适合阶段复盘或发布前检查。

只需提供：

- Linear 项目；
- 可选 GitHub 仓库；
- 时间窗口。

```text
使用 $linear-delivery-audit 审查这个项目最近 30 天的情况。
保持只读，返回问题、证据和建议动作。
```

### 建立长期治理流程

适合持续开发、多人协作或需要定期报告的项目。需要明确项目结构、关系、证据标准和权限边界。

## 单项目还是双项目

### 单项目模式

适合规模较小、需求与执行关系简单的项目。

一个 Linear 项目同时承载：

- 需求、问题、决策、变更和风险；
- 分析、实施、验证和协作任务。

需要使用标签、关系和模板区分治理事项与执行任务。

### 双项目模式

适合长期、复杂或需要严格追溯的项目。

```text
项目 A：需求与决策
  ├─ REQ 需求
  ├─ PROB 问题
  ├─ DEC 决策
  ├─ CR 变更
  ├─ RISK 风险
  └─ Q 待确认问题

项目 B：执行与交付
  ├─ 分析任务
  ├─ 实施任务
  ├─ 验证任务
  └─ 协作任务
```

执行任务通过 Linear 原生关系连接来源事项。

Infinite Canvas 的真实应用采用双项目模式，详见 [案例页](examples/infinite-canvas-case-study.md)。

## 新项目需要决定什么

### 项目身份

- 项目名称和稳定短标识；
- Linear 团队；
- 项目负责人；
- 项目时区；
- 单项目或双项目模式。

### 分类与状态

- REQ、PROB、DEC、CR、RISK、Q 使用哪些标签；
- 分析、实施、验证、协作任务使用哪些标签；
- Todo、In Progress、Done、Canceled 等状态如何映射；
- 哪些标签互斥；
- 哪些状态允许被视为活动、完成或取消。

### 关系与来源

- 执行任务如何记录来源事项；
- 使用哪个 Linear 原生关系；
- 阻塞、重复和父子关系如何使用；
- 外部反馈、文档或客户请求如何记录稳定来源编号。

### 证据

- 软件项目使用哪些 GitHub 仓库；
- 哪些代码、测试、发布或运行记录可以作为证据；
- 非软件项目使用哪些文档、审批或业务结果；
- 哪些证据可以复制，哪些只能链接或脱敏摘要。

### 权限

- 谁可以批准需求；
- 谁可以批准变更；
- 谁可以接受风险；
- 谁确认验收和发布；
- AI 可以创建或更新哪些记录；
- 定期审查可以写到哪里。

这些差异应记录在项目自己的治理文档或 Profile 中，不要硬编码进共享 Skill。

## 推荐迁移步骤

### 阶段 1：只读试用

1. 安装同一版本的两个 Skills；
2. 连接 Linear；
3. 软件项目再连接 GitHub；
4. 读取现有项目、标签、状态和权限；
5. 选择一段真实输入运行候选分析，不写入；
6. 运行一次只读交付审查。

通过条件：AI 能正确理解当前项目结构，并明确披露无法访问的数据。

### 阶段 2：低风险写入

1. 选择一个不涉及删除、验收或重大变更的候选；
2. 检查操作列表和 Plan ID；
3. 确认执行；
4. 回读 Linear 中的新事项、字段和关系；
5. 人工检查是否符合项目习惯。

通过条件：写入目标准确，没有重复创建，来源关系可追溯。

### 阶段 3：建立项目标准

1. 确定单项目或双项目模式；
2. 固定标签和状态映射；
3. 固定事项和任务模板；
4. 定义证据要求；
5. 明确人和 AI 的职责边界；
6. 将这些内容记录为项目治理文档。

通过条件：同类输入可以被稳定地分类、拆分和关联。

### 阶段 4：定期审查

1. 先稳定运行手动审查；
2. 使用工具生成项目 Profile；
3. 检查审查范围、报告目标和数据流；
4. 封存并验证 Profile；
5. 配置定期审查；
6. 测试同一周期重复运行不会生成重复报告；
7. 测试下一周期能够正确滚动。

通过条件：定期报告可重复、范围不漂移、不会擅自修改正式业务事项。

## Profile：只在高级使用时需要

只有定期报告、计划任务或自动写入审查结果时，才需要 Profile Schema v4。

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

检查后封存：

```powershell
python scripts/profile_tool.py seal project-profile.json `
  --approved-by "Project Owner" `
  --approval-record "APPROVAL-123"
python scripts/profile_tool.py validate project-profile.json
python scripts/profile_tool.py resolve-period project-profile.json
```

Profile 变化后需要重新检查和批准。

## 采用检查清单

- [ ] 两个 Skills 使用同一版本；
- [ ] Linear 团队和项目范围明确；
- [ ] 标签、状态和关系约定明确；
- [ ] 一次真实候选分析结果可用；
- [ ] 一次低风险写入完成并回读；
- [ ] 执行任务可以追溯到来源事项；
- [ ] 软件任务能够关联代码和测试证据；
- [ ] 一次只读审查能够发现真实问题或确认没有异常；
- [ ] AI 没有自动批准需求、风险、验收或发布；
- [ ] 项目差异只存在于映射、Profile 和证据来源中，而不是修改共享 Skill。

## 判断是否真正复用成功

成功复用不只是复制提示词，而应满足：

- 两个 Skills 不修改源码即可用于新项目；
- 新输入能够与现有 Linear 记录对账；
- 正式写入经过确认和回读；
- 执行任务能够追溯到需求、决策或风险来源；
- 审查能够发现证据缺失、状态冲突或长期停滞；
- 项目差异由 Linear 结构、标签映射、Profile 和证据来源表达。

## 相关文档

- [快速开始](quickstart.md)
- [集成说明](integrations.md)
- [Infinite Canvas 真实应用案例](examples/infinite-canvas-case-study.md)
- [能力与职责边界](capability-boundaries.md)
