## Context

`SKILL.md` 文件必须以 `---` 分隔的 YAML frontmatter 开始，当前项目技能与 bootstrap 压缩资产中的对应文件均未满足该约束。用户级 npm 前缀保留了不存在或无法由当前会话访问的旧 Codex 安装引用，`node_repl` 因此无法启动。

## Goals / Non-Goals

**Goals:**

- 让仓库技能与 bootstrap 生成的技能均可被 Codex 加载。
- 将 OpenSpec 和 Codex CLI 恢复到用户级 npm 前缀，并验证命令可执行。
- 用启动后的 Codex 进程验证 `node_repl` MCP 不再报告路径缺失。

**Non-Goals:**

- 不修改业务功能或其他技能。
- 不修改 MCP 的功能、权限或网络配置。
- 不删除仍被正在运行的 Codex 锁定的旧安装目录。

## Decisions

- 使用最小 frontmatter（`name` 与 `description`）修复技能，而非改写 SOP 正文；前者直接满足加载器契约并保留现有流程内容。
- 使用 `scripts/rebuild-bootstrap-assets.ps1` 重建内嵌 ZIP，而非手工编辑 Base64；该脚本是仓库中唯一的资产来源同步机制。
- 使用 npm 全局安装 `@fission-ai/openspec@latest` 与 `@openai/codex@latest`；Node.js 已存在，故不重装 Node.js。
- 对 `node_repl` 采用重启 Codex 后的启动日志验证；其注册并不位于仓库或可见的 `config.toml` 中。

## Risks / Trade-offs

- [旧 `codex.exe` 被运行中的进程锁定] → 不强制删除，重启 Codex 后再验证并由 npm 后续清理。
- [npm 全局目录未出现在当前 shell 的 PATH] → 使用绝对 `.cmd` 路径验证安装，并在新终端中确认 PATH 传播。
- [MCP 注册来源不可见] → 若重启后仍失败，收集新的启动日志，避免猜测性修改 MCP 配置。
