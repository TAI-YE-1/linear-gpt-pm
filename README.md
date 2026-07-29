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
   - 按幂等初始化蓝图适配现有 Linear；
   - 正式写入前必须确认目标、范围和影响。

2. `linear-delivery-audit`
   - 只读优先的交付核验与反向审查；
   - 检查孤立任务、无处置事项、Done 无证据、变更未传播、状态冲突和长期停滞；
   - 使用确定性的覆盖率、可观测性和健康判定规则；
   - 软件项目可选核验 GitHub 分支、PR、提交与测试证据；
   - 可由 Codex Automation 周期调用。

## 外部能力

- **Linear**：主要正式台账。推荐连接，但 Skill 在无写权限时会降级为候选方案或只读审查。
- **GitHub**：软件项目的可选证据源。没有 GitHub 时，不得声称完成代码核验。
- **Codex Automation**：只负责调度；审查逻辑由 `linear-delivery-audit` Skill 定义。

本仓库不包含 Linear/GitHub API 客户端，不要求重复配置 API Token，也不替代 Linear、GitHub 或人工业务验收。

## 安装

当前仓库为私有仓库，使用者必须已有仓库访问权限。若后续公开，下面的 GitHub 安装路径可以直接供更多用户使用。

### Codex

在 Codex 中调用 Skill 安装能力，并安装以下两个 GitHub 目录：

```text
https://github.com/TAI-YE-1/linear-gpt-pm/tree/main/skills/linear-project-governance
https://github.com/TAI-YE-1/linear-gpt-pm/tree/main/skills/linear-delivery-audit
```

也可以明确指令：

```text
Use $skill-installer to install both Skills from TAI-YE-1/linear-gpt-pm:
skills/linear-project-governance
skills/linear-delivery-audit
```

安装后重新启动或刷新 Codex 的 Skill 发现环境。

### ChatGPT

在支持自定义 Skills 的账号或工作区中，可构建单个 Skill ZIP：

```powershell
python scripts/build_skill_archives.py
python tests/validate_skills.py
```

生成文件位于 `dist/`：

```text
dist/linear-project-governance.zip
dist/linear-delivery-audit.zip
dist/SHA256SUMS.txt
```

每个ZIP包含独立的`SKILL.md`、`LICENSE.txt`、`agents/openai.yaml`及全部运行时资源。具体上传能力取决于当前产品、套餐和工作区权限。

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

治理结构初始化或适配时读取：

```text
skills/linear-project-governance/references/setup-blueprint.md
```

配置定时审查前，复制并完整填写：

```text
skills/linear-delivery-audit/templates/project-profile.md
```

然后使用 `automation/monthly-audit.md` 配置 Codex Automation。缺少精确项目、时区、报告位置或授权边界时，自动化必须停止而不是猜测。

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
python scripts/build_skill_archives.py
python tests/validate_skills.py
```

GitHub Actions会执行同一套轻量检查。校验覆盖：

- Skill frontmatter、名称和必需资源；
- Skill内部相对引用；
- 完整许可证及ZIP内许可证一致性；
- `agents/openai.yaml` UI元数据；
- 治理写入与自动审查安全边界；
- 自动化项目配置门禁；
- ZIP布局与SHA-256校验。

这些是静态与分发校验，不等同于真实安装、Linear/GitHub连接或Codex Automation运行验收。真实运行仍需单独保存烟雾测试证据。

详细说明见 `docs/`，自动化模板见 `automation/`。
