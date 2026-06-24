# Design: Generalize AI Change Prompts

## 方案概述

本次修复属于流程资产修复。核心做法是在提示词模板中使用显式占位符表达“下一阶段生成提示词文件”，由 `scripts/new-ai-change-prompt.ps1` 在生成时根据 `-OutputPrefix` 替换为实际文件名。

模板内容同步泛化，删除特定考核材料输出要求，并把固定技术限制改写为“不得做当前 change 未明确要求的扩展”。

## 文件边界

- `scripts/new-ai-change-prompt.ps1`：增加提示词文件名占位符替换。
- `docs/prompts/*.md`：把裸阶段跳转替换为生成文件占位符，移除场景化话术。
- `docs/ai-sop-usage.md`：更新说明，明确生成提示词引用的是 `OutputPrefix-*` 文件。
- `tests/test_prompt_generator.py`：新增回归测试，运行 PowerShell 生成器并检查输出。
- `scripts/bootstrap-ai-sop.ps1`：通过 `scripts/rebuild-bootstrap-assets.ps1` 重新嵌入最新资产。
- `openspec/changes/generalize-ai-change-prompts/tasks.md`：跟踪实施进度。

## 数据流

```text
docs/prompts/*.md templates
        |
        v
new-ai-change-prompt.ps1
        |
        v
docs/prompts/<OutputPrefix>-*.md generated prompts
```

`new-ai-change-prompt.ps1` 负责替换：

- change id
- goal
- constraints
- generated prompt file names
- generated prompt file paths

## 错误处理

- 如果模板缺失，占用现有脚本的 `Template not found` 错误。
- 如果 `OutputPrefix` 非 kebab-case，保留现有校验。
- 测试使用临时目录复制必要资产，避免污染仓库中的 `docs/prompts`。

## 验证策略

- 新增测试先覆盖当前失败场景：自定义 `-OutputPrefix` 生成后，router 和后续阶段必须引用自定义生成文件。
- 测试检查生成文件不含考核场景词。
- 运行现有 CLI 测试，确保业务生成器不受影响。
- 运行 `scripts/rebuild-bootstrap-assets.ps1` 后检查 `bootstrap-ai-sop.ps1` 已更新。
