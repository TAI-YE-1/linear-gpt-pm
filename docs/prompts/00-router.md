# 00 Router 阶段提示词

请使用 `.codex/skills/openspec-superpowers-sop`。

当前候选变更 ID：`<change-id>`

目标：

<在这里填写本次新功能或修复目标>

约束：

<在这里填写限制条件，例如不接 API、不做网页、不改生产配置等>

现在先做任务分流，不要修改业务代码。

## 判断任务类型

请先读取项目基础上下文，然后判断本次目标属于哪一类：

1. `simple-answer`：只需要解释、建议、命令说明，不修改文件。
2. `read-only-review`：只读审查、盘点、风险分析，不修改业务代码。
3. `process-assets`：只修改流程资产、提示词、文档或脚本，不修改业务代码。
4. `implementation-change`：新增/修改/删除业务行为、项目结构、测试、配置或用户可见功能。
5. `high-risk-change`：涉及生产执行、认证权限、安全策略、支付价格、数据库结构或删除数据。

## 分流规则

- `simple-answer`：直接回答，不创建 OpenSpec change，但如有验证命令应说明是否运行。
- `read-only-review`：执行只读检查，输出发现和风险，不创建 OpenSpec change，除非审查后需要改代码。
- `process-assets`：可以不创建业务 OpenSpec change；必须说明只改流程资产，并在完成前运行脚本解析/生成器验证。
- `implementation-change`：必须进入 `<PROMPT_PATH_01_PROPOSE>`，创建或读取 OpenSpec change，validate 通过前不写业务代码。
- `high-risk-change`：必须暂停并询问用户确认范围、权限和风险，确认前不修改文件。

## 必须输出

- 任务类型判断。
- 判断依据。
- 是否需要 OpenSpec change。
- 是否需要完整执行 `<PROMPT_PATH_01_PROPOSE>` 到 `<PROMPT_PATH_05_REVIEW_ARCHIVE>`。
- 下一步要读取的提示词文件，必须使用生成后的文件路径，例如 `<PROMPT_PATH_01_PROPOSE>`。
- 如果不走完整五阶段，说明省略哪些阶段以及质量风险如何被验证覆盖。
