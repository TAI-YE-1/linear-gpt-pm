# 03 Apply 阶段提示词

请继续使用 `.codex/skills/openspec-superpowers-sop`。

当前 OpenSpec change：`<change-id>`

现在进入 Apply 阶段。

请使用 `superpowers:executing-plans` 按已确认的计划小步实现。

## 进入条件

只有满足以下全部条件，才执行本阶段：

- `<PROMPT_PATH_01_PROPOSE>` 已通过 strict validate。
- `<PROMPT_PATH_02_SUBAGENT_PLAN>` 已输出实现计划。
- 用户已经明确确认计划。

如果任一条件不满足，停止并说明缺少哪一项。

要求：

- 只实现当前 OpenSpec change 的范围。
- 优先使用项目已有模式和标准库能力。
- 不引入不必要依赖。
- 不做当前 change 未明确要求的扩展、集成、配置或用户可见功能。
- 先写失败测试，再写实现。
- 每完成一项，更新 `openspec/changes/<change-id>/tasks.md`。
- 不要在没有验证前宣称完成。

## 小步执行规则

对每个计划任务按以下顺序执行：

1. 写或更新最小测试，先运行并确认失败原因正确。
2. 写最小实现让测试通过。
3. 运行相关测试。
4. 更新 `tasks.md` 对应项。
5. 检查是否偏离 OpenSpec 范围。

实现后必须运行：

```powershell
<项目最小运行命令>
<项目测试命令>
openspec validate <change-id> --strict
```

如果验证失败，先修复或说明失败原因，不要说完成。

## 输出格式

- `已执行任务`：对应 `tasks.md` 条目。
- `测试证据`：失败测试、通过测试、关键输出。
- `修改文件`：文件及作用。
- `范围检查`：是否只实现当前 change。
- `阶段闸门`：是否可以进入 `<PROMPT_PATH_04_VERIFY>`。
