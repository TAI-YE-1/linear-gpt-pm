bootstrap-ai-sop.ps1 的作用总结

这个脚本是一个自解压式 AI 开发 SOP 资产包分发器。运行它之后，目标项目会获得一套完整的、规范化的 AI 辅助开发流程资产。

核心思路：先定义，再实现


核心思路：先定义，再实现

传统 AI 编程是「丢需直接写代码」，容易导致方向偏差、范围蔓延。这套 SOP 的核心主张是：

▎ 需求不清不写代码、设计不确定不写代码、验证不通过不宣称完成。

脚本做了什么

bootstrap-ai-sop.ps1 ZIP包。运行后解压出以下资产到目标项目：

┌───────────────────────────────────────┬────────────────────────────┐
│                 资产                  │            用途            │
├───────────────────────────────────────┤
│ AGENTS.md                             │ 仓库级 AI 行为规则（告诉   │
│                    项目遵循什么流程） │
├───────────────────────────────────────┼────────────────────────────┤
│ .codex/skills/opens置 Skill，定义 7   │
│ p/SKILL.md                            │ 阶段 SOP                   │
├───────────────────────────────────────┤
│ docs/prompts/00-router.md ~           │ 6 个提示词模板，对应完整流 │
│ 05-review-archive.md                  │ 程的每一步                 │
├───────────────────────────────────────┤
│ docs/ai-sop-usage.md                  │ 使用教程                   │
├───────────────────────────────────────┼────────────────────────────┤
│ scripts/new-ai-change-prompt.ps1      │ 为具体需求生成定制化提示词 │
└───────────────────────────────────────┴────────────────────────────┘

三个组件的分工

1. OpenSpec（@fission-ai/openspec）— 需求规范工具
  - 强制在写代码前先 gn.md（设计）、tasks.md（任务）、spec.md（验收标准）
  - 提供 openspec validate --strict 命令检查规范完整性
  - validate 不通过 →
2. Superpowers（github.com/obra/superpowers）— 子代理协作方法论
  - 将分析工作拆给 4 个角色子代理：需求代理、架构代理、测试代理、审查代理
  - 每个代理独立输出结论，主 Codex 汇总成计划
  - 用户确认后才开始
3. Codex — AI 编程助手
  - 按确认后的计划小
  - 每完成一个任务更新 tasks.md
  - 执行验证命令、检

7 阶段流程

00-Router → 01-Propose → 02-Subagent-Plan → 03-Apply → 04-Verify →
05-Review-Archive
   ↓              ↓               ↓               ↓            ↓              ↓
 任务分流    创建OpenSpec    4角色子代理     小步实现      验证+测试
git diff审查
             规范文件         并行分析                                 +
复盘归档

实际使用方式

# 1. 跑一次，给新项目装上所有资产
powershell -NoProfilee.\bootstrap-ai-sop.ps1 -TargetRoot D:\test2

# 2. 写需求文件
# 3. 生成当前 change 的定制提示词                                    powershell -NoProfilee.\scripts\new-ai-change-prompt.ps1 `                                     -ChangeId add-my-
                                                                     # 4. 在 Codex 中按顺 5 提示词
                                                                     一句话总结

这套系统把「接到需求 → 分析 → 设计 → 实现 → 验证 → 归档」的软件工程标准流程，固化为 Codex AI 必须遵守的可执行 SOP。它用 OpenSpec 锁定需求边界进行多角度评审、用Codex 执行具体的代码修改—— 可追溯证据链，而不是 AI 无约束地直接输出代码。