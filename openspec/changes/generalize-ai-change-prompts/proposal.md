# Proposal: Generalize AI Change Prompts

## 背景

当前 `scripts/new-ai-change-prompt.ps1` 会为每个 change 生成 `current-*` 或自定义前缀的提示词文件，但模板正文中仍保留裸阶段名，例如 `01-propose` 到 `05-review-archive`。这会让生成后的提示词指向模板阶段，而不是当前生成文件。

同时，通用 SOP 模板中混入了特定考核场景话术，例如“如果用户需要考核材料，请额外输出一页纸说明、三分钟录屏讲解顺序”。这类内容不适合出现在通用提示词模板中。

## 目标

- 让生成后的提示词正文引用实际生成的提示词文件名。
- 支持默认 `current` 和自定义 `-OutputPrefix`。
- 移除或泛化考核、网页、数据库、模型 API 等场景化模板要求。
- 同步更新文档、测试和 `bootstrap-ai-sop.ps1` 内嵌资产。

## 非目标

- 不修改 `ai_builder_pack_maker` 业务 CLI 行为。
- 不修改全局 Codex skills。
- 不引入新的运行时依赖。
- 不改变 OpenSpec/Superpowers 五阶段流程本身。

## 验收标准

- 运行生成脚本后，生成文件中的阶段跳转应指向 `docs/prompts/<OutputPrefix>-NN-name.md` 或至少明确输出的 `<OutputPrefix>-NN-name.md` 文件名。
- 使用自定义 `-OutputPrefix` 时，生成提示词不得残留 `current-*` 硬编码。
- 通用提示词模板不得包含“考核材料”“一页纸说明”“三分钟录屏”等考核交付要求。
- 模板中不得使用固定项目限制替代当前 change 范围约束。
- `scripts/bootstrap-ai-sop.ps1` 的内嵌资产应由更新后的源文件重新生成。
- 相关自动化测试通过。
