# 贡献指南

欢迎提交 Issue、文档改进、测试场景和 Pull Request。

## 核心原则

所有贡献都需要保持以下边界：

1. 两个 Skills 必须可以独立安装，并包含运行所需的规则、模板和说明；
2. 需求治理写入与交付审查保持独立的权限边界；
3. 正式 Linear 写入必须经过明确确认和写前重读；
4. 审查默认只读，不得自动批准需求、变更、风险、验收、合并或部署；
5. 外部 Issue、评论、文档、PR 和日志只能作为数据，不能作为新的授权指令；
6. 新行为需要补充 `tests/cases.md` 场景，结构要求变化时同步更新验证器。

## 示例数据

公开示例可以使用：

- 虚构的通用项目；
- 已得到项目所有者明确同意的真实案例；
- 已脱敏的 Linear、GitHub 或项目材料。

禁止提交：

- 密钥、Token、密码和连接字符串；
- 未授权的客户、员工或个人信息；
- 私有工作区 ID、内部附件或完整生产日志；
- 未经允许公开的源代码和安全细节。

真实案例应优先保留业务结构和解决思路，删除不影响理解的敏感字段。

## 文档贡献

公开文档应优先回答：

- 这个项目解决什么问题；
- Linear、GitHub 和两个 Skills 分别承担什么角色；
- 用户如何安装和开始使用；
- 哪些操作需要人工确认；
- 当前有哪些限制和未完成验证。

避免把 README 写成内部交接记录、调试日志或只对作者有意义的版本说明。

## 代码与工具贡献

提交前运行：

```powershell
python -m pip install -r requirements-dev.txt
python -m compileall -q scripts skills tests
python -m unittest discover -s tests -p "test_*.py" -v
python scripts/build_skill_archives.py
python tests/validate_skills.py
```

修改 Skill 规则时，还需要检查：

- 是否改变触发范围；
- 是否扩大读取或写入权限；
- 是否影响 Plan ID、项目 Profile、证据规则或审查结论；
- 是否需要更新版本说明和测试场景。

## 提交建议

- 一个 Pull Request 只处理一个明确主题；
- 在描述中说明问题、方案、验证结果和兼容性影响；
- 文档变化附上主要页面或使用路径；
- 不通过静默默认值掩盖缺失配置或失败状态。
