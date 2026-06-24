## ADDED Requirements

### Requirement: 技能模板必须可被 Codex 加载
仓库 SHALL 在 `.codex/skills/openspec-superpowers-sop/SKILL.md` 提供有效的 YAML frontmatter。bootstrap 脚本生成同一技能文件时 MUST 保留该 frontmatter 与 UTF-8 文本。

#### Scenario: 加载仓库技能
- **WHEN** Codex 扫描项目技能目录
- **THEN** 不得因该 `SKILL.md` 缺少 YAML frontmatter 而跳过该技能

#### Scenario: 生成新项目资产
- **WHEN** 执行 `scripts/bootstrap-ai-sop.ps1` 生成 SOP 资产
- **THEN** 输出的 `openspec-superpowers-sop/SKILL.md` 必须包含有效 YAML frontmatter

### Requirement: 本地工具恢复必须可验证
环境恢复流程 SHALL 验证 OpenSpec 与 Codex CLI 的实际可执行路径。`node_repl` 的恢复 MUST 通过重启 Codex 后的 MCP 启动结果确认。

#### Scenario: 验证 CLI 安装
- **WHEN** 用户级 npm 安装完成
- **THEN** `openspec --version` 与 `codex --version` 必须由新安装的 CLI 成功执行

#### Scenario: 验证 MCP 启动
- **WHEN** 重启 Codex 客户端
- **THEN** 启动输出不得包含 `node_repl` 的路径不存在错误
