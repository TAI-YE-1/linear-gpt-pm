---
name: codex-delivery-guardrails
description: 管理 Codex 工程任务中的 Git 授权、worktree、原生 SDD checkpoint commits、无 commit 适配、测试去重、GitHub Actions、生产与外部副作用、完成声明和分支收尾。用于任何可能修改仓库状态、触发 CI、提交、推送、归档或发布的任务。
---

# Codex Delivery Guardrails

本 Skill 管交付治理，不替代开发方法。流程仍由 Superpowers、OpenSpec bridge 和 Codex subagent routing 决定。

## 1. 开始前检查

执行可能写入的任务前检查：

```bash
git status --short
git branch --show-current
git rev-parse --show-toplevel
```

并确认：

- 当前工作树是否已有用户修改；
- 当前分支和上游关系；
- 是否处于 worktree；
- 是否存在 merge、rebase、cherry-pick 或冲突状态；
- 项目测试入口和真实依赖；
- 是否涉及 `.github/workflows`；
- 是否涉及生产、真实数据、权限、费用或外部副作用。

用户已有修改必须保留。无法与当前任务安全共存时，说明具体重叠点后再请求处理方式。

## 2. 授权矩阵

### 默认允许

在用户要求的任务范围内：

- 读取文件、配置、日志和 Git 元数据；
- 修改工作树文件；
- 运行本地静态检查和测试；
- 创建临时文件；
- 生成未执行的 migration、查询、部署和回滚方案；
- 使用不会改变真实外部状态的 dry-run。

### 需要明确授权

- `git commit`、amend、cherry-pick；
- push、force-push、创建或更新远程 PR；
- merge、rebase、改写历史；
- 切换、创建、删除分支或 worktree；
- 修改 `.gitignore` 以服务工具流程；
- 安装或升级依赖；
- 触发产生明显额度消耗的 CI；
- 部署和真实外部动作。

用户当前消息已经明确要求某项具体动作时，不重复索要同一授权。

## 3. Worktree

`using-git-worktrees` 可提供隔离方法，但覆盖以下默认动作：

- 不自动选择目录；
- 不自动修改 `.gitignore`；
- 不自动 commit `.gitignore`；
- 不因发现 manifest 就执行 `npm install`、`pip install`、`cargo build` 等；
- 不在未确认成本和必要性时运行全量 baseline tests。

正确流程：

1. 检查当前是否已隔离；
2. 说明为什么需要 worktree；
3. 获得创建和分支授权；
4. 选择项目既有位置，或使用明确批准的位置；
5. 检查目录是否被 ignore；
6. 需要修改 ignore 时单独说明；
7. 只运行项目真实要求的依赖和 baseline 验证。

## 4. SDD 模式选择

开始 `subagent-driven-development` 前，选择一种模式并明确记录。

### Native checkpoint-commit mode

仅在以下全部成立时使用：

- 用户明确允许本地 checkpoint commits；
- 使用隔离 worktree；
- 不自动 push；
- commit 粒度和最终整理方式已说明；
- 工作树没有会被误纳入 commit 的用户改动。

保持上游 SDD 的 task commit、Base SHA、review package 和 progress ledger。

### No-commit adapter mode

用户不允许 commit，但仍需要 fresh implementer + task reviewer 时，显式调用 `$sdd-no-commit-adapter`。

该模式：

- 使用临时 Git index 写 tree objects；
- 不修改真实 index；
- 不创建 commit 或 ref；
- 以 task start tree 和 end tree 生成 review package；
- 仍保留 task review、fix/re-review 和 whole-change review。

这是适配流程，不是原生 SDD。

### Sequential mode

任务强耦合、工具不支持 subagent、adapter 条件不满足或工作树风险过高时，由主线程顺序实施并使用常规 review。

不得在未授权 commit 时悄悄执行原生 SDD，也不得删除其 commit 步骤后声称采用原生 SDD。

## 5. Commit 设计

用户授权 commit 后：

- 默认按可审查交付单位形成 1～3 个清晰提交；
- 不为每个两分钟步骤制造永久提交；
- 不混入无关用户改动；
- commit message 准确描述实际内容；
- 不 amend 用户已有 commit，除非明确要求；
- push 前重新检查将触发的 Actions。

Native SDD checkpoint commits 如果只是内部审查机制，应在最终交付前按用户授权的方式整理；不得自行 rebase、squash 或改写历史。

## 6. 验证 ledger

记录每个重要验证：

```text
command
working directory
tree / diff identity
started_at
finished_at
exit code
result summary
relevant files changed afterwards
```

重复运行规则：

- 相关代码和环境未变化，且已有新鲜完整证据：不重复同一重型测试；
- task 内运行聚焦测试；
- package、change、阶段关闭或发布前再运行必要组合或全量测试；
- reviewer 默认评估已有测试证据，除非发现证据缺失、过期或可疑；
- subagent 的“通过”文字不算证据，父线程必须读取实际输出或可靠产物。

`verification-before-completion` 仍是最终门。

## 7. 测试与实现

- 不修改测试来掩盖实现缺陷；
- 先判断失败来自实现、错误测试假设、环境、依赖还是版本变化；
- 行为变更和 Bug 回归优先 TDD；
- 文档、生成代码、纯格式或无法稳定自动化的外部行为可采用等价验证，但要说明；
- 数据库、权限、并发、migration 和生产路径需要额外负面、回滚和幂等验证；
- 未运行的验证必须明确披露。

## 8. GitHub Actions

修改 `.github/workflows` 或准备 push 可能触发 Actions 时检查：

```text
触发器
分支与路径过滤
workflow_dispatch
push / pull_request 重复运行
permissions
secrets
environment
concurrency
cache
artifact retention
matrix 规模
timeout
额度和替代本地验证
```

默认不：

- 新增每次 push 或 PR 都运行的重型全量测试；
- 创建重复 workflow；
- 创建自动 commit、自动 push 或自修改仓库的 workflow；
- 为本地可验证问题消耗 CI；
- 把 CI 当作唯一调试环境。

用户明确要求仓库级 CI 时，说明预计触发范围和额度影响。

## 9. OpenSpec 与 Git

OpenSpec 状态动作不隐含 Git 授权：

| OpenSpec 动作 | 不自动授权 |
|---|---|
| propose / artifact write | commit |
| apply task complete | commit / push |
| verify | PR / merge |
| sync | commit |
| archive | 删除分支 / merge / deploy |

完成一个 change、Phase 或 Package 时，不自动调用 `finishing-a-development-branch`。只有用户真正准备集成、保留或丢弃开发分支时才调用。

## 10. 生产与外部副作用

以下真实执行必须在执行前给出对象、范围、风险、回滚和验证方式，并获得授权：

- 生产部署；
- 生产数据库 schema 或数据写入；
- 删除、覆盖、迁移或批量更新真实数据；
- 修改真实权限、认证、密钥、证书；
- 调用计费或产生真实副作用的 API；
- 发送真实邮件、消息、通知；
- 修改价格、订单、支付、退款、结算；
- 强推和历史改写。

只读生产检查也要最小权限，不输出 secrets 和不必要的个人数据。

## 11. 完成与汇报

完成前：

```bash
git status --short
git diff --stat
```

必要时检查 staged 和 untracked 内容。

最终汇报准确列出：

- 已检查内容；
- 实际修改；
- 实际验证及结果；
- 未运行验证及原因；
- commit、push、PR、merge、archive、deploy 的真实状态；
- 残余风险和未完成项。

只有主线程取得新鲜证据后才能声称完成。

默认不发送完成邮件、消息或通知。只有用户在当前任务中明确要求、指定渠道和接收方，且相应工具可用时才执行；发送失败时准确报告失败。
