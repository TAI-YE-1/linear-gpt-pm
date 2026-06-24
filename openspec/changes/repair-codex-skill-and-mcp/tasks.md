## 1. 技能与模板修复

- [x] 1.1 为 `openspec-superpowers-sop/SKILL.md` 添加有效 YAML frontmatter。
- [x] 1.2 运行资产重建脚本并检查 bootstrap 内嵌资产包含修复后的技能。

## 2. 开发环境恢复

- [x] 2.1 验证用户级 `openspec` 与 `codex` CLI 可执行。
- [ ] 2.2 重启 Codex 并验证 `node_repl` MCP 启动结果。

## 3. 验证与审查

- [x] 3.1 运行 `openspec validate repair-codex-skill-and-mcp --strict`。
- [x] 3.2 检查 bootstrap 生成资产、`git status --short` 与 `git diff --stat`。
