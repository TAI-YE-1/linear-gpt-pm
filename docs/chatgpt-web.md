# ChatGPT 网页端上传与验证

本文说明如何在 ChatGPT 网页端上传 Linear GPT PM 的两个 Skills，以及如何判断它们是否真正可用。

## 1. 上传文件

分别上传两个独立的 Skill ZIP：

```text
linear-project-governance.zip
linear-delivery-audit.zip
```

每个 ZIP 应只包含一个 Skill 目录，并在该目录根部包含：

```text
<skill-name>/
├── SKILL.md
├── agents/openai.yaml
├── LICENSE.txt
├── references/
├── templates/
└── scripts/          # 仅当该 Skill 需要脚本时存在
```

`SKILL.md` 必须以 YAML frontmatter 开始，并包含与目录名一致的 `name` 和清晰的 `description`。

## 2. “已安装”代表什么

当技能出现在 ChatGPT 的 Installed 列表中，至少说明：

- ZIP 已被上传；
- ChatGPT 已完成基础扫描；
- 技能元数据已被系统识别；
- 技能可以进入后续触发和使用流程。

但“已安装”不等于：

- 当前聊天一定会向模型暴露技能目录路径；
- `read_resource` 可以浏览该技能的所有文件；
- 该技能已经连接 Linear 或 GitHub；
- 技能在每个聊天中都会自动触发；
- 技能的业务写入权限已经获得授权。

## 3. 不要用这些方式判断技能是否安装成功

### 不要用 `read_resource` 猜路径

类似：

```text
skills://plugins/<plugin-slug>/<skill-slug>/skill.md
```

的 URI 只适用于运行时已经明确暴露的技能资源。用户上传的个人 Skill 不保证拥有可猜测的 Plugin URI，也不保证向普通聊天暴露源码资源树。

因此，读取失败只能说明当前路径或资源挂载不可用，不能证明 `SKILL.md` 不存在。

### 不要用 `Linear.list_agent_skills`

该接口查询的是 Linear 服务端自己的 Agent Skills 注册表，不是 ChatGPT 的 Skills 安装列表。返回空数组与 ChatGPT 中是否安装这两个 Skills 没有直接关系。

### 不要搜索公开 Plugin 目录来证明个人 Skill 不存在

个人上传、工作区共享或未公开发布的 Skill 不一定拥有公开 Plugin 条目。`plugin_not_found` 只表示未找到对应的公开目录条目。

## 4. 正确的验证方法

验证时应在新聊天中运行一个真实、低风险任务。

### 验证需求治理 Skill

先确认 ChatGPT 已连接 Linear，然后输入：

```text
请使用 linear-project-governance，读取 <Linear团队或项目> 的当前事项。
分析下面这段真实项目材料，与现有事项对账，只返回候选、重复项和建议关系，不要写入。

<粘贴一段真实但不敏感的反馈、会议记录或项目材料>
```

有效触发后，输出应体现以下行为：

- 先读取当前 Linear 状态；
- 区分需求、问题、决策、变更、风险和待确认问题；
- 与现有事项对账，而不是直接创建重复事项；
- 在未确认写入前只返回候选；
- 如提议写入，应展示可读操作和短 Plan ID。

### 验证交付审查 Skill

输入：

```text
请使用 linear-delivery-audit，审查 <Linear项目名称> 最近 30 天的情况。
保持只读；如已连接 GitHub，可结合 <owner/repo> 的代码、PR 和测试证据。
返回发现的问题、证据、影响、限制和建议动作。
```

有效触发后，输出应体现以下行为：

- 默认只读；
- 检查任务来源、负责人、完成标准和交付证据；
- 区分“代码存在”“测试通过”“已经验收”；
- 缺少权限时标记为不可访问，而不是宣称证据不存在；
- 不自动关闭事项、接受风险、合并代码或发布系统。

## 5. 如何确认使用了 Skill

不要只问“你能看到 SKILL.md 吗”。更可靠的判断是检查输出是否稳定遵循 Skill 的独特规则。

建议检查：

- 是否出现规定的分类体系；
- 是否执行写前读取和重复检查；
- 是否要求确认短 Plan ID 后才写入；
- 审查是否默认只读；
- 是否披露证据范围、访问限制和未验证内容；
- 是否避免把 GitHub 状态直接等同于业务验收。

如果输出没有这些特征：

1. 在提示中明确写出技能名称；
2. 新建聊天后重试；
3. 检查技能是否已安装在当前网页端；
4. 检查 Linear 和 GitHub 是否已连接且当前账号有权限；
5. 在技能详情页确认技能未被禁用、阻止或标记为 Needs Review；
6. 重新上传最新 ZIP。

## 6. 查看技能源码

需要查看完整 `SKILL.md` 或其他资源时，应使用：

- ChatGPT Skills 编辑器；
- 技能详情页提供的下载或导出功能；
- 本仓库中的对应 Skill 目录；
- 本地解压后的 ZIP 内容。

聊天中的通用资源读取器不是个人 Skill 源码浏览器。

## 7. ChatGPT 与 Codex 的差异

ChatGPT 网页端上传和 Codex 本地安装是两套独立安装面：

- ChatGPT 网页端：通过 Skills 页面上传或创建；
- Codex：安装到 Codex 的 Skills 目录，或通过 Skill Installer 从仓库安装。

个人 Skills 可能需要在不同产品或界面分别添加，不能假设网页端上传后会自动同步到本地 Codex，反之亦然。

## 8. 最小验收标准

两个 Skills 可以认为在 ChatGPT 网页端完成基础验收，需要至少保留以下证据：

- 两个技能均显示为 Installed；
- 需求治理 Skill 完成一次真实只读对账；
- 交付审查 Skill 完成一次真实只读审查；
- 至少一次低风险写入经过 Plan ID 确认并回读成功；
- 输出明确区分已验证、未验证和不可访问内容；
- 未发生未确认的正式写入。
