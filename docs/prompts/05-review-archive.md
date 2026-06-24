# 05 Review / Archive 阶段提示词

请继续使用 `.codex/skills/openspec-superpowers-sop`。

当前 OpenSpec change：`<change-id>`

现在进入 Review 和 Archive 阶段。

## 进入条件

只有在 `<PROMPT_PATH_04_VERIFY>` 已运行并给出可接受证据后，才进入本阶段。

如果本次是 `simple-answer`，不需要归档。  
如果本次是 `read-only-review`，只输出审查结论，不归档为实现 change。  
如果本次是 `process-assets`，归档时明确说明没有修改业务代码。

必须检查：

```powershell
git status --short
git diff --stat
git diff
```

必须总结：

- 本次新增或修改了哪些文件。
- 每个文件的作用。
- 哪些 `git status` 文件不属于本次改动。
- 运行了哪些验证命令。
- 验证结果是否通过。
- 是否有无关扩展。
- 是否有临时代码、硬编码或敏感信息。
- `tasks.md` 是否已更新。
- 剩余风险和后续建议。

归档材料应包含：

- 问题背景。
- 方案设计。
- AI 执行过程。
- 修改文件。
- 验证命令。
- 测试结果。
- 交付结果。
- 剩余风险。
- 可复用经验。

## 输出格式

- `改动摘要`
- `文件清单`
- `验证证据`
- `范围审查`
- `临时代码/硬编码/敏感信息检查`
- `tasks.md 状态`
- `归档摘要`
- `后续建议`
