# 01 Propose 阶段提示词

请继续使用 `.codex/skills/openspec-superpowers-sop`。

当前 OpenSpec change：`<change-id>`

现在进入 Explore 和 Propose 阶段，不要写业务代码。

## 进入条件

只有满足以下任一条件，才执行本阶段：

- `00-router` 判断为 `implementation-change`。
- 用户明确要求创建 OpenSpec change。
- 已存在相关 OpenSpec change，需要补齐或修正。

如果本次目标只是 `simple-answer`、`read-only-review` 或 `process-assets`，请先说明不进入本阶段的原因，并回到对应轻量流程。

## 必须完成

- 读取 README、现有 OpenSpec 文件、相关目录结构和可能相关文件。
- 明确目标、范围、非目标、约束和验收标准。
- 创建或更新：
  - `openspec/changes/<change-id>/proposal.md`
  - `openspec/changes/<change-id>/design.md`
  - `openspec/changes/<change-id>/tasks.md`
  - `openspec/changes/<change-id>/specs/**/spec.md`
- 验收标准必须可测试。
- validate 通过前不要写业务代码。

## 必须运行

```powershell
openspec validate <change-id> --strict
```

如果全局 `openspec` 不可用，可以使用：

```powershell
npx --yes @fission-ai/openspec@1.4.1 validate <change-id> --strict
```

必须说明实际使用了哪条命令。

## 输出格式

- `任务类型`：来自 `00-router` 的判断。
- `Explore 摘要`：项目背景、相关文件、不确定点、风险。
- `OpenSpec 文件`：新增或修改文件清单。
- `验收标准`：可测试条目。
- `validate 结果`：命令、退出状态、关键输出。
- `阶段闸门`：是否允许进入 `<PROMPT_PATH_02_SUBAGENT_PLAN>`，以及原因。
