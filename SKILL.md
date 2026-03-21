---
name: superpowers-openspec
description: superpowers 的规范阶段子技能。用户只要要求先分析、先写 spec、先做详细设计、先整理会议纪要/口语需求，或要求把需求变成可执行的中文 OpenSpec 时就使用；在规范完成前卡住实现、拆解和测试。纯代码修复且不涉及新规则、流程、接口或状态时不要使用。
---

# Superpowers OpenSpec

这是 `superpowers` 在规范阶段调用的子技能。它只做一件事：把需求收敛成可执行的 spec，并确保在 spec 完成前不进入实现。

## 什么时候用

在这些情况下使用本 skill：

- 用户要求先分析、先写 spec、先做详细设计再开发
- 用户要求把会议纪要、口语需求或草稿整理成规范文档
- 用户明确提到 `OpenSpec`、规范阶段、详细设计、需求分析
- `superpowers` 已经进入规范阶段，当前任务是产出 spec

## 不该用的时候

以下情况不要强行进入本 skill：

- 纯 bug 修复，且不涉及新规则、流程、接口或状态
- 用户只想快速定位代码问题，不需要规范产物
- 任务本质上是实施、联调、测试或发布，而不是定义需求

## 核心职责

1. 先收敛事实，再写规范。
2. 产出中文 OpenSpec 风格文档。
3. 补齐必要的架构图、流程图、时序图。
4. 做 Spec Review，发现问题就回改。
5. spec 未完成前，不进入拆解、实现、测试。

## 使用方式

### 触发口令

当用户出现以下表达时，直接进入 OpenSpec 工作流，而不是先给实现方案：

- “先分析一下，再开发”
- “先写 spec”
- “帮我整理成 OpenSpec”
- “把这段会议纪要转成详细设计”
- “先不要写代码，先把规则梳理清楚”

### 建议执行命令

将用户诉求转换为类似下面的内部执行命令，并按对应模式产出：

1. `使用 superpowers-openspec：基于以下需求产出中文 OpenSpec 初稿。`
2. `使用 superpowers-openspec：先列出已知事实、缺失信息、待确认项，再输出 spec。`
3. `使用 superpowers-openspec：把会议纪要整理成可执行规范，并补齐 Mermaid 图。`
4. `使用 superpowers-openspec：对现有规则和新需求做差异分析，再输出变更 spec。`
5. `使用 superpowers-openspec：完成 spec 后执行一次 Spec Review，只输出 review 结论与修改项。`

如果用户需求较模糊，优先使用第 2 条；如果输入是会议纪要或聊天记录，优先使用第 3 条；如果是已有系统改造，优先使用第 4 条。

### 可直接给用户的示例话术

必要时可以主动引导用户这样下达命令：

- “请使用 superpowers-openspec，先整理需求再给实现建议。”
- “请使用 superpowers-openspec，把下面内容转成中文 OpenSpec。”
- “请使用 superpowers-openspec，先输出事实、缺口和待确认项。”
- “请使用 superpowers-openspec，补齐流程图、时序图和验收标准。”

更完整的命令示例见 `references/openspec-command-examples.md`。

## 标准工作流

1. 判断输入属于新需求、需求变更、会议纪要整理，还是方案澄清。
2. 先提炼已知事实、缺失信息、待确认项。
3. 根据 `references/spec-template.md` 生成中文 OpenSpec。
4. 若涉及现有规则、接口、状态或页面，先写冲突和差异，再写新规则。
5. 补齐必要图表与验收标准。
6. 根据 `references/spec-checklist.md` 做 Spec Review。
7. 输出 review 结论：通过、退回修改，或仍需补充。
8. 停在规范阶段，把后续工作交还给 `superpowers`。

## 执行要求

- 输入不完整时，先列出已知事实、缺失信息和待确认项。
- 按参考文档中的 OpenSpec 结构写作。
- 如果现有规则、接口、状态或页面会受影响，先把冲突和差异写清楚。
- review 结论必须明确：通过、退回修改，或仍需补充。
- 若用户催促实现，也要先给最小可行 spec，再说明尚未进入实现阶段。

## 输出要求

默认输出应包含：

- 已知事实
- 缺失信息 / 待确认项
- 中文 OpenSpec 正文
- Mermaid 图（架构图、流程图、时序图）
- 验收标准
- Spec Review 结论

如果用户只要求其中一部分，可以裁剪，但必须明确当前是否已经完成规范阶段。

## 停止条件

当 spec 已写完并完成 review 后，停在规范阶段，把后续工作交还给 `superpowers`。
如果用户只要求规范产物，不要顺手继续拆任务或写实现建议。

## 参考

- `references/skill-usage-sequence.md`
- `references/spec-template.md`
- `references/spec-checklist.md`
- `references/openspec-command-examples.md`
