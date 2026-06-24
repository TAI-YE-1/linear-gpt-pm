# 一页纸考核材料扩写 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 `outputs/latest/one_page_summary.md` 扩写为一页内可快速阅读、信息完整且有事实依据的结构化考核材料。

**Architecture:** 仅编辑现有 Markdown 输出文档，按“背景、问题、方法、过程、交付、验证、复用”重组与扩充内容。所有描述以当前文档和仓库内已有交付事实为边界，不修改生成器、输入材料或测试代码。

**Tech Stack:** Markdown、PowerShell、`rg`、Git。

---

### Task 1: 扩写一页纸考核材料

**Files:**

- Modify: `outputs/latest/one_page_summary.md`
- Reference: `docs/superpowers/specs/2026-06-23-one-page-summary-expansion-design.md`

- [x] **Step 1: 核对可引用事实与范围**

Run:

```powershell
Get-Content -Raw -Encoding utf8 'outputs\\latest\\one_page_summary.md'
```

Expected: 目标材料以 `order-helper.html` 的离线点餐推荐交付和规范开发流程为主；不引用考核材料生成工具相关描述，也不添加未经证实的量化指标。

- [x] **Step 2: 重写目标文档的结构化内容**

将 `outputs/latest/one_page_summary.md` 组织为以下部分，并保持所有结论可追溯：

```markdown
# AI Builder 考核材料一页纸

## 项目背景
## 真实问题与风险
## 解决方案与职责分工
## 执行闭环
## 交付成果
## 验证与改进
## 可复用价值
```

每节补充与标题直接相关的事实：说明 OpenSpec、Superpowers、Codex 和 Git 证据链的分工；列出 Explore 至 Archive 的闭环；描述 `order-helper.html` 接收预算、人数、荤菜和素菜数量并在前端生成推荐结果。不得新增百分比、次数、生产效果或用户反馈等未验证数据。

- [x] **Step 3: 检查内容完整性和篇幅**

Run:

```powershell
$text = Get-Content -Raw -Encoding utf8 'outputs\\latest\\one_page_summary.md'
$text.Length
rg -n '^## (项目背景|真实问题与风险|解决方案与职责分工|执行闭环|交付成果|验证与改进|可复用价值)$|TBD|TODO|待定' 'outputs\\latest\\one_page_summary.md'
```

Expected: 包含七个规定标题；不含 `TBD`、`TODO` 或“待定”；总字符数处于约 900–1200 的目标区间，若因 Markdown 标记略有浮动，以一页可读性优先。

- [x] **Step 4: 检查改动范围**

Run:

```powershell
git status --short
git diff --stat -- 'outputs/latest/one_page_summary.md'
git diff --check -- 'outputs/latest/one_page_summary.md'
```

Expected: 目标文档的改动无尾随空格和冲突标记；除本任务已记录的设计和计划文档外，无无关修改。

- [x] **Step 5: 暂不提交，交由用户决定版本控制操作**

本仓库当前尚无提交历史且用户未要求提交，因此不要执行 `git add` 或 `git commit`。在交付时报告 `git status --short` 与 `git diff --stat` 的实际输出。
