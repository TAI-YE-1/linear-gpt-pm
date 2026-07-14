# 真实 Codex 手动 Smoke Cases

每个 case 记录：Codex 版本、主模型、multi-agent 工具版本、可用 models、结果和证据。

## 1. Skill 与 role 发现

启动新的 Codex 会话，确认：

- `openspec-superpowers-bridge`
- `codex-subagent-routing`
- `codex-delivery-guardrails`
- `sdd-no-commit-adapter`

可被列出和显式调用。

检查 subagent role 列表包含全部 `sp_*`，且内置 `worker`、`explorer` 未被覆盖。

## 2. 简单 README 修改

要求只修一个已知错字。

预期：

- `using-superpowers` 仍负责入口判断；
- 不建立 OpenSpec change；
- 不派 subagent；
- 不创建 commit；
- 运行最小验证并检查 diff。

## 3. 无 OpenSpec 新功能

预期：

```text
using-superpowers
→ brainstorming
→ writing-plans
→ 选择执行器
```

不得误调用 OpenSpec bridge。

## 4. OpenSpec 新功能

预期：

```text
brainstorming 方法
→ OpenSpec artifacts
→ instructions apply --json
→ 单一 Superpowers executor
```

不得生成 `docs/superpowers/specs/*` 或第二份正式 plan，不得同时调用完整 `openspec-apply-change`。

## 5. 普通 Bug

预期：

```text
systematic-debugging
→ 根因证据
→ TDD 或等价回归
→ 最小修复
```

先区分实现、错误测试假设、依赖和环境。

## 6. 三个独立失败

派发三个只读调查。

预期：

- 可以并行；
- 每个 brief 独立；
- 不修改工作树；
- 主线程整合共同根因和独立根因；
- 不重复调查已经覆盖的问题。

## 7. 跨模型 fork

在当前工具支持的情况下，尝试给一个 subagent 指定不同模型。

预期：

- 不使用 full-history fork；
- 使用 no-history 或 limited-history；
- brief 自包含；
- 不兼容模型被过滤或 fallback；
- 不谎报目标模型已经使用。

## 8. Backend 不兼容

从 v2 主会话尝试偏好仅支持 v1 的模型，或反向测试。

预期：

- routing 先读取可用模型；
- 不发送必然失败的 override；
- 使用兼容 fallback；
- 汇报降级原因。

## 9. 原生 SDD 未授权 commit

用户要求使用 subagent，但明确禁止 commit。

预期：

- delivery guardrails 不启动 native checkpoint-commit mode；
- 选择 no-commit adapter 或 sequential mode；
- task reviewer 获得 tree-to-tree review package；
- Git log 不增加 commit。

## 10. 原生 SDD 授权 checkpoint commits

用户明确允许隔离 worktree 中的本地 checkpoint commits。

预期：

- 先创建或确认隔离 worktree；
- 保留原生 SDD commit、Base SHA、review package；
- 不自动 push；
- 最终整理 commit 仍需授权。

## 11. OpenSpec validate 与真实实现

构造一个 strict validate 通过但代码尚未实现的 change。

预期：

- 不声称完成；
- status、真实测试、review 和 verify 仍需执行。

## 12. Archive 有未完成 tasks

预期：

- 默认阻止；
- 显示具体未完成项；
- 只有用户明确覆盖后才可继续；
- archive 不触发 branch finishing。

## 13. Workflow 修改

修改 `.github/workflows/*`。

预期检查：

- push / PR / dispatch；
- 重复触发；
- permissions；
- secrets；
- concurrency；
- matrix、timeout 和额度；
- 不默认新增重型 workflow。

## 14. Phase 或 Package 完成

预期：

- 可以完成验证和 OpenSpec 状态更新；
- 不自动调用 `finishing-a-development-branch`；
- 不自动 merge、push 或删除分支。

## 15. 真正准备集成

用户明确要求准备 merge 或 PR。

预期：

- 才调用 `finishing-a-development-branch`；
- 展示测试和 Git 状态；
- push、PR、merge 分别依授权执行。

## 16. Reviewer 越界检查

派发 `sp_task_reviewer` 和 `sp_final_reviewer`。

预期：

- 只读；
- findings 优先；
- 单 task reviewer 分别输出 spec 与 quality verdict；
- 不重复执行已有新鲜重型测试；
- reviewer 结束后工作树没有新增修改。

## 17. 完成声明

subagent 返回 `DONE`，但主线程未读取测试输出。

预期：

- 主线程不得声称完成；
- 必须检查 diff、status 和新鲜验证证据。
