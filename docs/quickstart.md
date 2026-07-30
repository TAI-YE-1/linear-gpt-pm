# 快速开始

Linear GPT PM 包含两个可以配合使用、也可以单独调用的 Agent Skills：

- `$linear-project-governance`：把会议、反馈、文档和现有项目记录整理成 Linear 候选事项；
- `$linear-delivery-audit`：检查 Linear 任务是否有来源、负责人、完成标准和可核验的交付证据。

基础使用不需要配置文件，也不需要手工计算哈希。

## 你需要什么

至少需要：

- 一个支持 Agent Skills 的 Codex 或兼容环境；
- 已连接的 Linear 工作区。

软件项目建议再连接 GitHub，用于核验代码、PR、测试和发布证据。没有 GitHub 时仍可使用需求治理和 Linear 结构审查，但不能宣称已经核验代码交付。

## 安装

从同一固定提交安装两个 Skills：

```text
$skill-installer install https://github.com/TAI-YE-1/linear-gpt-pm/tree/92561c1aa36c18ede37474185170ec3faa7d8c33/skills/linear-project-governance
$skill-installer install https://github.com/TAI-YE-1/linear-gpt-pm/tree/92561c1aa36c18ede37474185170ec3faa7d8c33/skills/linear-delivery-audit
```

也可以使用仓库中的安装脚本：

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

`--replace` 会先备份旧 Skill 目录。安装完成后刷新或重启 Skill 发现环境。

## 第一次使用：整理一段真实反馈

先保持只读：

```text
使用 $linear-project-governance 分析下面的用户反馈。
请先读取当前 Linear 项目并对账，只返回候选事项、重复项和建议关系，不要写入。

<粘贴真实反馈、会议记录或项目材料>
```

Skill 会：

1. 读取你指定范围内的 Linear 项目和事项；
2. 判断内容属于需求、问题、决策、变更、风险还是待确认问题；
3. 查找重复、冲突或已经存在的事项；
4. 提议需要创建、更新或关联的事项和执行任务；
5. 等待确认，不会直接写入。

需要执行时，Skill 会展示可读计划，例如：

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

用户只需要确认短 Plan ID。Skill 会在写入前重新读取目标，避免覆盖期间发生的变化，并在写入后回读结果。

## 第二次使用：运行一次只读审查

```text
使用 $linear-delivery-audit 审查这个 Linear 项目最近 30 天的情况。
保持只读，返回问题、证据、影响和建议动作。
GitHub 仓库为：<可选仓库>
```

一次性审查不需要 Profile，只需要明确：

- Linear 项目；
- 可选 GitHub 仓库；
- 时间窗口。

审查重点包括：

- 执行任务是否有需求、决策、风险或其他明确来源；
- 是否有负责人、完成标准和交付证据；
- Done 任务是否有可核验结果；
- 需求变化是否同步到相关任务；
- Linear 状态是否与 GitHub 代码、PR 或测试证据冲突；
- 是否存在长期停滞、重复、阻塞或未处理风险。

## 推荐的 Linear 结构

小型项目可以使用一个 Linear 项目，通过标签区分治理事项和执行任务。

长期或复杂项目建议使用双项目模式：

```text
项目 A：需求与决策
  ├─ REQ 需求
  ├─ PROB 问题
  ├─ DEC 决策
  ├─ CR 变更
  ├─ RISK 风险
  └─ Q 待确认问题

项目 B：执行与交付
  ├─ 分析任务
  ├─ 实施任务
  ├─ 验证任务
  └─ 协作任务
```

执行任务通过 Linear 原生关系连接来源事项。GitHub 链接、Commit、PR、测试和运行记录作为交付证据附在任务中。

## 定期自动审查

先完成一次成功的手动审查，再配置定期审查。

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

检查生成的配置后封存并验证：

```powershell
python scripts/profile_tool.py seal project-profile.json `
  --approved-by "Project Owner" `
  --approval-record "APPROVAL-123"
python scripts/profile_tool.py validate project-profile.json
python scripts/profile_tool.py resolve-period project-profile.json
```

定期审查模板位于：

```text
skills/linear-delivery-audit/references/monthly-automation.md
```

自动审查只能读取批准范围并生成已授权的审查产物，不能自行批准需求、接受风险、合并代码或发布系统。

## 本地验证仓库

```powershell
python -m pip install -r requirements-dev.txt
python -m compileall -q scripts skills tests
python -m unittest discover -s tests -p "test_*.py" -v
python scripts/build_skill_archives.py
python tests/validate_skills.py
```

输出：

```text
dist/linear-project-governance.zip
dist/linear-delivery-audit.zip
dist/SHA256SUMS.txt
```

## 下一步

- [查看 Linear / GitHub / Codex 集成方式](integrations.md)
- [查看 Infinite Canvas 真实应用案例](examples/infinite-canvas-case-study.md)
- [迁移到其他项目](reuse-guide.md)
- [了解人、AI、Linear 和 GitHub 的职责边界](capability-boundaries.md)
