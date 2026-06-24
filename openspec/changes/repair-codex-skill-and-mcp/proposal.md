## Why

项目内的 `openspec-superpowers-sop` 技能缺少 Codex 所需的 YAML frontmatter，导致启动时被跳过；同时，bootstrap 脚本内嵌的同一份资产会将该错误传播到新项目。开发环境中用户级 Codex CLI 安装路径失效，导致 `node_repl` MCP 无法启动。

## What Changes

- 为 `openspec-superpowers-sop` 添加有效的 YAML frontmatter，并保持 UTF-8 编码。
- 重新生成 `scripts/bootstrap-ai-sop.ps1` 的内嵌资产，使新项目获得相同的有效技能文件。
- 恢复用户级 `@fission-ai/openspec` 与 `@openai/codex` CLI 安装，并记录对 MCP 启动的验证方法。

## Capabilities

### New Capabilities

- `codex-environment-repair`: 确保项目技能模板有效，并提供可验证的 Codex/OpenSpec 本地工具恢复流程。

### Modified Capabilities

- 无。

## Impact

- 受影响文件：`.codex/skills/openspec-superpowers-sop/SKILL.md`、`scripts/bootstrap-ai-sop.ps1`。
- 受影响环境：用户级 npm 全局目录中的 `@fission-ai/openspec` 与 `@openai/codex`。
- 不修改业务代码、数据结构、认证或生产配置。
