# Linear GPT PM

Linear GPT PM 是一套可复用的 Agent Skills 工具包，让 ChatGPT 与 Codex 按同一套规则管理需求、执行任务、交付证据和项目审查。

它解决四类常见问题：

- 需求散落在聊天、会议、邮件和文档中；
- 执行任务缺少明确来源；
- Done 状态缺少可验证交付证据；
- 需求变化、Linear 状态与代码交付不同步。

## 核心组成

本仓库包含两个自包含 Skill：

1. `linear-project-governance`
   - 交互式治理与正式写入；
   - 需求提取、分类、对账、变更识别；
   - 创建事项、执行任务和原生关系；
   - 正式写入前必须确认目标、范围和影响。

2. `linear-delivery-audit`
   - 只读优先的交付核验与反向审查；
   - 检查孤立任务、无处置事项、Done 无证据、变更未传播、状态冲突和长期停滞；
   - 软件项目可选核验 GitHub 分支、PR、提交与测试证据；
   - 可由 Codex Automation 周期调用。

## 外部能力

- **Linear**：主要正式台账。推荐连接，但 Skill 在无写权限时会降级为候选方案或只读审查。
- **GitHub**：软件项目的可选证据源。没有 GitHub 时，不得声称完成代码核验。
- **Codex Automation**：只负责调度；审查逻辑由 `linear-delivery-audit` Skill 定义。

本仓库不包含 Linear/GitHub API 客户端，不要求重复配置 API Token，也不替代 Linear、GitHub 或人工业务验收。

## 安装

### Codex

使用 Codex 的 Skill 安装能力从本仓库安装以下目录，或将目录复制到当前 Codex 支持的 Skills 位置：

```text
skills/linear-project-governance
skills/linear-delivery-audit
```

安装后重新启动或刷新 Codex 的 Skill 发现环境。

### ChatGPT

在支持自定义 Skills 的账号或工作区中，可将单个 Skill 目录打包为 ZIP 后上传。可运行：

```powershell
python scripts/build_skill_archives.py
```

生成文件位于 `dist/`。具体上传能力取决于当前产品、套餐和工作区权限。

### Plugin

将两个 Skills 与 Linear、GitHub Apps 组合成 Plugin 属于后续分发阶段，不是 V1 完成条件。

## 快速使用

治理入口：

```text
使用 linear-project-governance 分析这段真实反馈，与现有 Linear 事项对账。
先输出候选项，不要直接写入。
```

确认写入：

```text
写入刚才确认的第 1、2 项，并创建必要的执行任务和原生关系。
```

交付核验：

```text
使用 linear-delivery-audit 核验指定任务的完成声明，检查 Linear 证据；
软件项目同时检查 GitHub 的 PR、提交和测试结果。
```

## 项目边界

本仓库不包含：

- 任何特定业务项目名称、Issue ID 或仓库地址；
- 个人考核材料、录屏稿或答辩稿；
- 自动批准需求、变更、风险或业务验收的逻辑；
- 自动删除项目、Issue 或历史记录的逻辑；
- Codex、Superpowers、OpenSpec 安装器；
- 全局 `AGENTS.md` 修改器；
- Linear/GitHub 本地 API 客户端。

## 验证

```powershell
python tests/validate_skills.py
python scripts/build_skill_archives.py
```

详细说明见 `docs/`，自动化模板见 `automation/`。
