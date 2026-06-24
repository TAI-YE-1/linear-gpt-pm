# AI SOP 使用教程

这套资产用于把一个新项目接入“OpenSpec + Superpowers + Codex”的分阶段开发流程。目标是先固定需求和验收标准，再计划、实现、验证和归档。

## 一、准备条件

- Windows PowerShell。
- 已安装 Codex。
- 可选：Git，用于版本管理。
- 可选：Node.js/npm，用于通过 `npx --yes @fission-ai/openspec@1.4.1` 运行 OpenSpec。

## 二、在新项目初始化 SOP 资产

把 `bootstrap-ai-sop.ps1` 放到任意位置，然后运行：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\bootstrap-ai-sop.ps1 -TargetRoot D:\path\to\new-project
```

如果希望脚本顺便初始化 Git：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\bootstrap-ai-sop.ps1 -TargetRoot D:\path\to\new-project -InitGit
```

如果希望脚本顺便初始化 OpenSpec：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\bootstrap-ai-sop.ps1 -TargetRoot D:\path\to\new-project -InitOpenSpec
```

如果目标文件已经存在，默认会跳过。需要覆盖时加 `-Force`。

初始化后建议先建立一次 Git 基线提交。否则所有文件都是未跟踪状态，`git diff` 和 `git diff --stat` 不能展示实际内容差异，后续 Review 阶段只能靠文件清单和人工扫描判断范围。

```powershell
git status --short
git add .
git commit -m "chore: initialize ai dev sop assets"
```

## 三、脚本会生成什么

- `AGENTS.md`：仓库级 AI 开发规则，告诉 Codex 如何使用技能、规划、验证和处理权限问题。
- `.codex/skills/openspec-superpowers-sop/SKILL.md`：本项目内置 SOP skill。
- `docs/prompts/00-router.md`：任务分流提示词模板，用于判断是否需要完整 OpenSpec 五阶段。
- `docs/prompts/01-propose.md`：Explore / Propose 阶段提示词模板。
- `docs/prompts/02-subagent-plan.md`：Subagent Plan 阶段提示词模板。
- `docs/prompts/03-apply.md`：Apply 阶段提示词模板。
- `docs/prompts/04-verify.md`：Verify 阶段提示词模板。
- `docs/prompts/05-review-archive.md`：Review / Archive 阶段提示词模板。
- `docs/ai-sop-usage.md`：这份使用教程。
- `scripts/new-ai-change-prompt.ps1`：为每个新 change 生成当前可直接投喂 Codex 的提示词。

## 四、为一个新需求生成提示词

进入新项目目录：

```powershell
cd D:\path\to\new-project
```

把本次需求写到 `需求.md`。需求里可以包含大段结构化文本、JSON、字典、代码或双引号。

```powershell
Get-Content -Raw -Encoding UTF8 .\需求.md
```

如果能看到需求文件内容，说明读取成功。然后用一行命令生成当前 change 的提示词。

注意：下面这条命令里，`-File .\scripts\new-ai-change-prompt.ps1` 不要换行拆开。

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\new-ai-change-prompt.ps1 -ChangeId add-example-feature -GoalFile .\需求.md
```

脚本默认使用以下限制条件：只修改当前需求明确要求的范围；不做无关重构；不引入不必要依赖；不修改生产配置。

如果需要自定义限制条件，可以直接传 `-Constraints`：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\new-ai-change-prompt.ps1 -ChangeId add-example-feature -GoalFile .\需求.md -Constraints "只要最简单的单个 HTML 文件；不需要后端；不需要数据库；不需要框架。"
```

也可以把限制条件写到 `约束.md`：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\new-ai-change-prompt.ps1 -ChangeId add-example-feature -GoalFile .\需求.md -ConstraintsFile .\约束.md
```

生成后会得到：

- `docs/prompts/current-00-router.md`
- `docs/prompts/current-01-propose.md`
- `docs/prompts/current-02-subagent-plan.md`
- `docs/prompts/current-03-apply.md`
- `docs/prompts/current-04-verify.md`
- `docs/prompts/current-05-review-archive.md`
- `docs/prompts/current-README.md`

## 五、推荐执行顺序

1. 打开 Codex，确认工作目录是新项目根目录。
2. 对 Codex 说：请读取 `docs/prompts/current-00-router.md`，并按里面的要求执行。
3. 如果 Router 判断为 `simple-answer`、`read-only-review` 或 `process-assets`，按 Router 给出的轻量流程执行。
4. 如果 Router 判断为 `implementation-change`，对 Codex 说：请读取 `docs/prompts/current-01-propose.md`，并按里面的要求执行。
5. 等 OpenSpec change 创建并 validate 通过。
6. 对 Codex 说：请读取 `docs/prompts/current-02-subagent-plan.md`，并按里面的要求执行。
7. 确认计划后，再让 Codex 读取 `docs/prompts/current-03-apply.md`。
8. 实现完成后，让 Codex 读取 `docs/prompts/current-04-verify.md`。
9. 验证通过后，让 Codex 读取 `docs/prompts/current-05-review-archive.md`。

## 六、常用验证命令

如果全局 `openspec` 可用：

```powershell
openspec validate add-your-feature --strict
```

如果全局 `openspec` 不可用：

```powershell
npx --yes @fission-ai/openspec@1.4.1 validate add-your-feature --strict
```

如果 `npx` 因沙箱、权限或网络无法访问 npm registry，必须记录失败原因和质量风险，并按当前环境的权限规则请求授权后重试同一条命令。离线环境建议预装 OpenSpec CLI，或提前准备 npm 缓存。

项目测试命令按项目实际技术栈选择，例如：

```powershell
python -m unittest discover tests
```

收尾检查：

```powershell
git status --short
git diff --stat
```

如果仓库尚未建立基线提交，`git diff` 可能为空但 `git status --short` 显示大量未跟踪文件。此时不能把空 diff 当作无改动，必须说明审查限制，并尽快建立初始提交。

## 七、使用原则

- validate 通过前，不写业务代码。
- 计划确认前，不写业务代码。
- 不必所有目标都机械执行完整五阶段；先由 `00-router` 判断任务类型。
- 新增或修改业务行为、项目结构、测试、配置或用户可见功能时，必须走完整 OpenSpec 流程。
- Apply 阶段只做当前 OpenSpec change 范围内的事。
- Verify 失败时，不宣称完成。
- Review 阶段必须检查是否有无关扩展、临时代码、硬编码或敏感信息。
- 读取或写入中文文件时显式使用 UTF-8，例如 `Get-Content -Raw -Encoding UTF8 <path>` 和 `Set-Content -Encoding UTF8 <path>`。
- 跨 PowerShell 和 Node 做中文行为验证时，避免在一行 inline 命令里写复杂中文正则；优先使用 UTF-8 测试文件，或用 ASCII 条件配合中文静态检查。
- 如果全局个人规则要求 `planning-with-files`，但本项目已定义 OpenSpec 流程，则以 OpenSpec `proposal.md`、`design.md`、`tasks.md` 和 `specs/**/spec.md` 作为任务状态来源；只有在项目没有更具体流程时再使用 `task_plan.md`、`findings.md`、`progress.md`。
