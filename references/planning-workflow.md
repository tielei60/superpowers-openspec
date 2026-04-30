# 面向 OpenSpec 的方案、规范与计划工作流

本文件说明如何先沉淀便于用户评审的中文方案文档，再基于一个或多个已确认方案文档创建或更新 OpenSpec change。

## 定位

`docs/solutions/*.md` 是本 skill 约定的方案文档，不是 OpenSpec 官方 artifact。

OpenSpec 仍然以官方产物为准：

- `proposal.md` 与 `design.md` 承接方案
- `spec.md` 承接规范
- `tasks.md` 承接计划

## 何时使用

使用该工作流：

- 用户要求先写完整 markdown 方案
- 用户希望先确认可完整评审的方案，再生成 OpenSpec 任务
- 一个 OpenSpec change 需要基于多个方案文档合并生成
- 用户担心 OpenSpec artifact 分散，无法完整看到方案全貌

不使用该工作流：

- 用户只要求直接进入已有 OpenSpec change 的实现
- 用户只要求小范围 bug 修复，且不涉及新规则、流程、接口或状态
- 用户明确不需要方案文档，只希望直接使用 `/opsx:propose` 或 `/opsx:ff`

## 执行流程

```text
讨论需求与约束
  -> 生成 docs/solutions/<主题>.md
  -> 询问用户是否需要方案文档自我闭环验证
  -> 询问用户是否需要先创建 OpenSpec 拆分设计
  -> 用户确认方案文档
  -> 创建或更新 OpenSpec change
  -> proposal.md 引用来源方案文档
  -> 生成或更新 spec.md / design.md / tasks.md
```

关键门禁：

- 方案文档确认前，不应创建或更新 OpenSpec change
- 方案文档确认前，不应直接进入 `/opsx:*`
- 自我闭环验证不是强制门禁；在请求用户确认前应询问用户是否需要，由用户决定是否执行
- 闭环验证完成后，应询问用户是否需要先创建 `docs/solutions/references/<主题>-OpenSpec-拆分设计.md`；该拆分设计由用户决定，不是强制步骤
- OpenSpec 产物发生实质变化时，需要检查是否应同步回方案文档

## 方案文档模板

`docs/solutions/*.md` 必须使用中文，文件名本身也必须使用中文，不使用英文文件名或纯数字文件名。

可读性要求：

- 使用人类易读语义，避免 AI 式套话
- 术语首次出现需解释
- 优先短句，先说结论
- 对比、枚举、状态映射优先用表格
- 避免内部缩写和未解释代号

建议结构：

```md
# 方案：<标题>

## 背景

## 目标

## 非目标

## 已确认决策

## 关键取舍

## 方案设计

## 流程 / 架构 / 状态图

## OpenSpec 拆分建议

## 风险与兼容性影响

## 待确认问题

## 验收标准
```

如果某些章节不适用，明确写“本方案不涉及”，不要留空。

## 可选自我闭环验证

在请求用户确认 `docs/solutions/*.md` 前，先询问用户是否需要进行方案文档自我闭环验证。

推荐问法：

```text
是否需要我先对这份方案文档做一次自我闭环验证，再交给你确认？
```

如果用户选择需要，检查：

- 背景是否解释清楚
- 目标和非目标是否明确
- 已确认决策是否完整
- 关键取舍是否说明原因
- 方案设计是否可落地
- 待确认问题是否显式列出
- 风险、兼容性、迁移或回滚影响是否覆盖
- 验收标准是否可验证
- Mermaid 或 ASCII 图示是否必要且完整
- OpenSpec 拆分建议是否能承接到 `proposal.md`、`spec.md`、`design.md`、`tasks.md`

如果发现缺失、矛盾、不可验证、图示缺失或范围不清，应先修正 `docs/solutions/*.md`，再交给用户确认。

如果用户选择不需要，直接进入用户确认环节；不要把该验证设为强制步骤。

## 可选 OpenSpec 拆分设计

在闭环验证完成后、请求用户确认 `docs/solutions/*.md` 前，询问用户是否需要先创建拆分设计：

```text
是否需要我先基于当前方案，补一份 OpenSpec 拆分设计？
```

拆分设计流程详见 `references/solution-to-openspec-workflow.md`。

用户选择需要则进入拆分设计流程，选择不需要则直接进入方案文档确认环节。拆分设计由用户决定，不是强制门禁。

## 图示要求

方案文档继承本 skill 的完整性要求：

- 架构边界、模块关系、依赖方向或数据流复杂时，补 Mermaid 架构图或流程图
- 流程分支、异常回路、状态流转复杂时，补 Mermaid `flowchart` 或 `stateDiagram`
- 跨角色、跨系统、异步通知或前后端交互复杂时，补 Mermaid `sequenceDiagram`
- 页面、表单、列表、弹窗或信息区块布局需要说明时，补 ASCII 文本布局图
- Mermaid 图必须自检 fence 闭合、图类型声明、节点标识一致和连线完整

图示是方案文档表达完整性的组成部分，不是 OpenSpec 官方新增 artifact。

## `proposal.md` 来源引用

OpenSpec change 不新增 `sources.md` 或 `source-docs.md`。来源关系写入 `proposal.md`。

单文档来源：

```md
## 来源方案文档

本变更基于以下已确认方案文档生成：

- `docs/solutions/示例方案.md`
```

多文档来源：

```md
## 来源方案文档

本变更基于以下已确认方案文档生成：

- `docs/solutions/方案一.md`
- `docs/solutions/方案二.md`
```

该章节应靠近 `proposal.md` 顶部，保证用户和 agent 都能先看到变更来源。

## 同步规则

- 如果方案文档发生实质变化，检查并更新对应 OpenSpec change 的 `proposal.md`、`spec.md`、`design.md` 和 `tasks.md`
- 如果 OpenSpec 产物在执行过程中发生实质变化，回写或更新对应方案文档
- 如果某个变化只影响执行拆分，不改变已确认方案，可以只更新 `tasks.md`，但应确认 `proposal.md` 与方案文档仍然一致
- 如果方案文档和 OpenSpec 产物暂时不同步，必须明确告知用户，不能假装两者已经一致

## 使用示例

单方案：

```text
先帮我写一个完整方案文档，确认后再生成 OpenSpec change。
```

预期先生成：

```text
docs/solutions/<主题>.md
```

用户确认后再生成或更新：

```text
openspec/changes/<change-name>/proposal.md
openspec/changes/<change-name>/design.md
openspec/changes/<change-name>/tasks.md
openspec/changes/<change-name>/specs/<capability>/spec.md
```

多方案：

```text
请基于 `docs/solutions/方案一.md` 和 `docs/solutions/方案二.md` 创建一个 OpenSpec change。
```

预期：

- 校验两个方案文档均已确认
- 在 `proposal.md` 中列出两个来源
- 不新增 `sources.md`
