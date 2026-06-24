# 02 Subagent Plan 阶段提示词

请继续使用 `.codex/skills/openspec-superpowers-sop`。

当前 OpenSpec change：`<change-id>`

现在进入 Subagent Plan 阶段，不要写业务代码。

## 进入条件

只有在 `<PROMPT_PATH_01_PROPOSE>` 已完成且 `openspec validate <change-id> --strict` 通过后，才执行本阶段。

如果 validate 未通过，先回到 `<PROMPT_PATH_01_PROPOSE>` 修 OpenSpec 文件。

请使用 `superpowers:subagent-driven-development` 和 `superpowers:writing-plans`，根据当前 OpenSpec change 做开发计划。

请分配 4 个子代理角色：

1. 需求代理
   - 检查 `proposal.md`、`design.md`、`tasks.md`、`spec.md` 是否完整。
   - 确认验收标准是否可测试。
   - 确认 OpenSpec validate 是否通过。

2. 架构代理
   - 设计最小项目结构。
   - 确认第一版不引入复杂依赖。
   - 确认只做当前 change 范围内的事情。
   - 确认不做明确排除的非目标。

3. 测试代理
   - 设计测试用例。
   - 明确验证命令。
   - 确认输出结果可检查。

4. 审查代理
   - 检查是否有无关扩展。
   - 检查是否没有按计划执行。
   - 检查最终 git diff 是否清晰。
   - 检查是否有临时代码、硬编码或敏感信息。

要求：

- 每个子代理先输出自己的分析。
- 主 Codex 最后汇总成一个实现计划。
- 用户确认计划前，不要修改业务代码。

## 输出格式

- `需求代理结论`：完整性、可测试性、validate 状态。
- `架构代理结论`：最小结构、依赖选择、非目标排除。
- `测试代理结论`：测试用例、验证命令、失败路径。
- `审查代理结论`：范围风险、diff 风险、临时代码风险。
- `实现计划`：按小步列出任务、预期文件、验证方式。
- `阶段闸门`：等待用户确认；确认前不进入 `<PROMPT_PATH_03_APPLY>`。
