---
name: sdd-no-commit-adapter
description: 在用户未授权 Git commit、但仍需要 Superpowers fresh implementer、task reviewer、fix/re-review 和 final review 闭环时，为每个 task 生成无 commit 的 Git tree snapshot 与 review package。仅由 codex-delivery-guardrails 显式选择。
---

# SDD No-Commit Adapter

本 Skill 是可选适配器，不是原生 `subagent-driven-development`。

它只替换原生 SDD 对 task commit、Base SHA 和 commit-based review package 的依赖，保留：

```text
pre-flight review
→ fresh implementer
→ tests + self-review
→ task reviewer
→ fix / re-review
→ next task
→ final whole-change review
```

## 1. 前提

使用前确认：

- 当前目录是 Git repository；
- 没有 unresolved merge conflicts；
- 用户未授权 commit；
- 同一工作树只有一个写入所有者；
- Python 3 可用；
- Git object database 可写；
- 用户理解此模式会写入无引用的 blob/tree objects，但不会创建 commit、branch、tag 或修改真实 index。

若 repository 使用复杂 submodule、sparse checkout、自定义 clean/smudge filter 或大型二进制文件，先评估 snapshot 成本和保真度；不确定时改用主线程顺序实施。

## 2. 安全模型

脚本使用临时 `GIT_INDEX_FILE`：

```text
HEAD 或 empty tree
→ git add -A 到临时 index
→ git write-tree
→ 删除临时 index
```

它会：

- 包含 tracked、staged、unstaged 和未忽略的 untracked 文件；
- 保留 task 开始前已有用户修改作为 baseline；
- 不修改真实 `.git/index`；
- 不移动 HEAD；
- 不创建 commit 或 ref；
- 只在 object database 写入可由 Git GC 清理的对象。

脚本在 snapshot 前后计算真实 index 的 SHA-256；若变化则失败并报告。

## 3. 每个 task 的流程

### Task start

```bash
python "<skill>/scripts/sdd_adapter.py" snapshot \
  --label "task-<id>-start" \
  --output "<workspace>/task-<id>-start.json"
```

保存 start tree。

### Implement

派发 fresh implementer，给出明确所有权、禁止 commit/push、聚焦测试和状态协议。

### Task end

```bash
python "<skill>/scripts/sdd_adapter.py" snapshot \
  --label "task-<id>-end" \
  --output "<workspace>/task-<id>-end.json"
```

### Review package

```bash
python "<skill>/scripts/sdd_adapter.py" review \
  --base "<workspace>/task-<id>-start.json" \
  --head "<workspace>/task-<id>-end.json" \
  --output "<workspace>/task-<id>-review.md"
```

reviewer 读取：

- OpenSpec task 或 plan task；
- relevant requirements / design；
- review package；
- implementer test evidence。

### Fix / re-review

修复前再次 snapshot 作为新 base，修复后生成新的 package。不要复用旧 review package。

## 4. Workspace

默认使用 repository 外的临时目录，或项目已经 ignore 的工作目录。

不要：

- 自动修改 `.gitignore`；
- 将 snapshots 和 review packages commit；
- 把临时文件作为权威计划；
- 在多个写入 agent 间共享同一个 task snapshot 名称。

## 5. 进度 ledger

每个 task 记录：

```text
task id
start snapshot
end snapshot
tree hashes
review package
implementer status
tests
review verdicts
fix snapshot / re-review
final accepted tree
```

任务通过后再更新 OpenSpec checkbox 或外部进度。

## 6. 限制

- tree snapshot 记录文件内容，不记录运行时数据库、服务、环境变量或外部状态；
- ignored files 不进入 snapshot；
- Git filters 可能影响 object 内容；
- 无 commit tree 没有 author、message 和 parent；
- review package 不能替代真实测试；
- final delivery 仍按用户授权决定是否形成 1～3 个 commit。

## 7. 失败处理

出现以下情况停止 adapter：

- index hash 异常变化；
- snapshot tree 无法验证；
- repository root 不一致；
- unmerged files；
- Git 命令失败；
- review package 为空但实现声称有修改；
- task 修改与所有权范围明显不符。

不得通过删除用户修改或重置工作树修复 adapter 问题。
