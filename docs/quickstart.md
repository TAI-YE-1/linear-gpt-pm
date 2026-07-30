# 快速开始

Linear GPT PM 包含两个配合使用的 Agent Skills：

- `$linear-project-governance`：把真实工作输入整理为 Linear 候选事项，并在人工确认后写入；
- `$linear-delivery-audit`：检查 Linear 中的任务来源、完成标准、证据和项目风险，默认只读。

## 1. 准备环境

建议连接：

- **Linear**：必需，用于承载需求、决策、任务、状态和审查结果；
- **GitHub**：软件项目建议连接，用于核验代码、PR、测试和发布证据。

没有 GitHub 连接时，仍可以完成 Linear 需求治理和结构审查，但不能宣称已经核验代码交付。

## 2. 安装两个 Skills

公开仓库可直接从固定提交安装：

```text
$skill-installer install https://github.com/TAI-YE-1/linear-gpt-pm/tree/92561c1aa36c18ede37474185170ec3faa7d8c33/skills/linear-project-governance
$skill-installer install https://github.com/TAI-YE-1/linear-gpt-pm/tree/92561c1aa36c18ede37474185170ec3faa7d8c33/skills/linear-delivery-audit
```

或者使用仓库自带安装脚本：

```powershell
git clone https://github.com/TAI-YE-1/linear-gpt-pm.git
cd linear-gpt-pm
git checkout 92561c1aa36c18ede37474185170ec3faa7d8c33
python scripts/install_codex_skills.py --dry-run --source-ref 92561c1aa36c18ede37474185170ec3faa7d8c33
python scripts/install_codex_skills.py --source-ref 92561c1aa36c18ede37474185170ec3faa7d8c33
```

升级已安装版本：

```powershell
python scripts/install_codex_skills.py --replace --source-ref 92561c1aa36c18ede37474185170ec3faa7d8c33
```

旧 Skill 目录会在替换前备份。安装后刷新或重启 Skill 发现环境。

## 3. 路径 A：基础需求治理

适合会议纪要、用户反馈、需求变更、风险和任务拆解。

```text
使用 $linear-project-governance 分析下面的会议记录，
与当前 Linear 项目中的事项对账，先只返回候选，不要写入。
```

Skill 会：

1. 读取当前范围内的 Linear 项目和事项；
2. 判断输入属于需求、问题、决策、变更、风险还是待确认问题；
3. 查找重复或冲突事项；
4. 提议需要创建或更新的事项和执行任务；
5. 等待用户确认。

写入前会展示可读计划：

```text
PLAN-A1B2C3D4E5
1. 创建一个需求事项
2. 创建一个验证任务
3. 建立来源关系
```

确认：

```text
执行 PLAN-A1B2C3D4E5
```

用户只需要确认短 Plan ID。完整摘要和目标版本由 Skill 内部校验。

## 4. 路径 B：一次性只读审查

适合阶段复盘、发布前检查或快速了解项目健康状态。

```text
使用 $linear-delivery-audit 审查这个 Linear 项目最近 30 天的情况。
保持只读，在聊天中返回问题、证据、影响和建议动作。
```

一次性审查不需要 Profile。只需提供缺失的：

- Linear 项目范围；
- 可选 GitHub 仓库；
- 时间窗口。

审查重点包括：

- 执行任务是否有明确来源；
- 是否有负责人、完成标准和交付证据；
- 已完成任务是否有可核验结果；
- 需求变化是否传播到相关任务；
- Linear 状态是否与 GitHub 代码或测试证据冲突；
- 是否存在长期停滞、重复、阻塞或未处理风险。

## 5. 路径 C：定期自动审查

完成至少一次成功的手动审查后，再配置定期审查。

进入已安装的 `linear-delivery-audit` Skill 目录：

```powershell
python -m pip install -r requirements-runtime.txt
python scripts/profile_tool.py init project-profile.json `
  --project-key "demo" `
  --project-name "Demo Project" `
  --timezone "Asia/Shanghai" `
  --owner "Project Owner" `
  --team "Demo Team" `
  --project "Demo Delivery"
```

检查生成的项目配置后封存：

```powershell
python scripts/profile_tool.py seal project-profile.json `
  --approved-by "Project Owner" `
  --approval-record "APPROVAL-123"
python scripts/profile_tool.py validate project-profile.json
python scripts/profile_tool.py resolve-period project-profile.json
```

然后使用：

```text
skills/linear-delivery-audit/references/monthly-automation.md
```

定期审查必须明确：

- 读取哪些 Linear 项目；
- 是否读取 GitHub；
- 审查哪个时间范围；
- 报告写到哪里；
- 允许写入哪些审查产物；
- 哪些正式决策仍必须由人确认。

## 6. 真实应用结构

Infinite Canvas 项目采用双项目结构：

```text
Infinite Canvas｜需求与决策
  ├─ 需求
  ├─ 问题
  ├─ 决策
  ├─ 变更
  ├─ 风险
  └─ 待确认问题

Infinite Canvas｜执行与交付
  ├─ 分析任务
  ├─ 实施任务
  ├─ 验证任务
  └─ 协作任务
```

执行任务通过 Linear 原生关系连接来源事项，并通过链接或编号关联 GitHub PR、Commit、测试和运行证据。

## 7. 本地构建与验证

```powershell
python -m pip install -r requirements-dev.txt
python -m compileall -q scripts skills tests
python -m unittest discover -s tests -p "test_*.py" -v
python scripts/build_skill_archives.py
python tests/validate_skills.py
```

构建输出：

```text
dist/linear-project-governance.zip
dist/linear-delivery-audit.zip
dist/SHA256SUMS.txt
```

## 8. 使用原则

- 基础使用无需 Profile、JSON 或手工计算哈希；
- 所有正式 Linear 写入必须经过人工确认；
- 审查默认只读；
- GitHub 的代码完成不自动等于业务验收；
- AI 提供整理、对账和检查能力，人保留最终决策权。
