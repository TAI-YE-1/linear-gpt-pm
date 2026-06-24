# 04 Verify 阶段提示词

请继续使用 `.codex/skills/openspec-superpowers-sop`。

当前 OpenSpec change：`<change-id>`

现在进入 Verify 阶段。

请使用 `superpowers:verification-before-completion` 做完成前验证。

## 进入条件

本阶段用于完成前验证。以下情况必须执行：

- 刚完成 `<PROMPT_PATH_03_APPLY>`。
- 修改了流程资产、脚本、文档模板，需要证明生成链路可用。
- 用户要求确认当前状态是否可交付。

必须运行：

```powershell
openspec validate <change-id> --strict
<项目最小运行命令>
<项目测试命令>
git status --short
git diff --stat
```

如果本次没有 OpenSpec change，必须说明原因，并用等价验证替代，例如脚本解析、模板生成、哈希一致性或只读检查命令。

还必须检查：

- 目标输出文件是否生成。
- 输出文件是否非空。
- `tasks.md` 是否按实际完成情况更新。
- 是否存在测试缓存、临时文件或无关产物。

输出：

- 每条命令：命令、退出状态、关键输出、是否通过。
- 失败原因和影响范围。
- 输出文件或生成资产检查结果。
- `git status --short` 中哪些文件属于本次范围，哪些不属于。
- 是否可以进入 `<PROMPT_PATH_05_REVIEW_ARCHIVE>`。

如果验证失败，不要说完成，先修复或说明失败原因。
