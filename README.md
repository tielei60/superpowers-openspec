# superpowers-openspec

`superpowers-openspec` 是一个**面向 OpenSpec 的方案、规范与计划工作流**。

它解决的问题是：用户经常会先说“帮我分析、写方案、写规范、写计划”，但 OpenSpec 的产物会分散在 `proposal.md`、`spec.md`、`design.md`、`tasks.md` 中。这个 skill 负责先判断当前应该沉淀方案、定义规范、拆解计划，还是进入官方 `/opsx:*` 流程。

一句话概括：

```text
方案先确认，规范再承接，计划再落地。
```

## 适合什么时候用

使用本 skill：

- 用户要求先分析、先整理需求、先写 spec、先做详细设计
- 用户要求先写完整 markdown 方案，再生成 OpenSpec 任务
- 用户要求先定方案、规范或开发计划，再进入实现
- 用户提出功能改造、功能优化、流程优化、模块重构或能力升级，并且会影响规则、流程、接口、状态、数据结构或模块边界
- 用户把“设计 / 方案 / 计划”和“实现 / 开发 / 落地”写在同一句里
- 任务涉及新功能、业务规则、接口、交互、数据结构、状态流转或角色流程变化

不强制使用本 skill：

- 纯 bug 修复，且不涉及新规则、流程、接口或状态
- 纯文案、纯样式、纯配置值调整
- 单点技术修复或局部性能优化，影响范围明确且无需新增规范
- 用户只要求快速定位问题或直接给出修复建议

## 核心工作流

```text
用户意图
  -> 判断是否需要完整方案文档
  -> 判断应进入哪个 OpenSpec / OPSX 阶段
  -> 生成或更新 proposal / spec / design / tasks
  -> 规范确认后再进入实现
```

如果用户要求先确认完整方案文档，则多一步：

```text
用户意图
  -> docs/solutions/<主题>.md
  -> 询问是否需要方案文档自我闭环验证
  -> 用户确认方案文档
  -> openspec/changes/<change-name>/
  -> proposal.md 引用来源方案文档
  -> spec.md / design.md / tasks.md
```

## 方案文档先行

当用户希望先完整确认方案，再进入 OpenSpec 规范和计划拆解时，先生成：

```text
docs/solutions/<主题>.md
```

要求：

- 方案文档必须使用中文
- 方案文档文件名也必须使用中文，不使用英文文件名或纯数字文件名
- 内容应便于用户完整评审
- 请求用户确认前，应询问是否需要先做方案文档自我闭环验证
- 自我闭环验证由用户决定，不是强制步骤
- 用户确认前，不创建或更新 OpenSpec change
- 用户确认后，再进入 `/opsx:*`
- `docs/solutions/*.md` 不是 OpenSpec 官方 artifact，而是本 skill 约定的上游方案来源

方案文档应覆盖：

- 背景
- 目标
- 非目标
- 已确认决策
- 关键取舍
- 方案设计
- 风险与兼容性影响
- 待确认问题
- 验收标准

如果方案涉及复杂架构、流程、状态、时序或页面结构，应补 Mermaid 或 ASCII 图示。

### 可选的自我闭环验证

在把方案文档交给用户确认前，agent 应先询问：

```text
是否需要我先对这份方案文档做一次自我闭环验证，再交给你确认？
```

如果用户选择需要，验证重点包括：

- 目标和非目标是否清楚
- 已确认决策是否完整
- 关键取舍是否说明原因
- 方案设计是否可落地
- 待确认问题是否显式列出
- 风险、兼容性和迁移影响是否覆盖
- 验收标准是否可验证
- Mermaid 或 ASCII 图示是否必要且完整
- OpenSpec 拆分建议是否能承接到 `proposal.md`、`spec.md`、`design.md`、`tasks.md`

如果用户选择不需要，直接进入用户确认环节。

## 来源关系

OpenSpec change 来源于方案文档时，不新增 `sources.md` 或 `source-docs.md`。

来源关系写在 `proposal.md` 中：

```md
## 来源方案文档

本变更基于以下已确认方案文档生成：

- `docs/solutions/示例方案.md`
```

多个方案文档生成一个 change 时：

```md
## 来源方案文档

本变更基于以下已确认方案文档生成：

- `docs/solutions/方案一.md`
- `docs/solutions/方案二.md`
```

## 方案、规范、计划的对应关系

| 用户说法 | 默认含义 | 主要产物 |
| --- | --- | --- |
| 完整方案文档 | 先形成便于用户评审的上游方案 | `docs/solutions/*.md` |
| 方案 | 为什么做、做什么、怎么设计 | `proposal.md`、`design.md` |
| 规范 / 规则 / 行为定义 | 行为约束、场景和边界 | `spec.md` |
| 计划 / 开发计划 | 可执行任务拆解 | `tasks.md` |
| 需求沟通 / 先分析 / 先梳理 | 先收敛问题空间 | `/opsx:explore` |

## OpenSpec 官方目录

OpenSpec 的官方目录语义以 `openspec/` 为准：

```text
openspec/
├── specs/
│   └── <capability>/
│       └── spec.md
└── changes/
    └── <change-name>/
        ├── proposal.md
        ├── design.md
        ├── tasks.md
        └── specs/
            └── <capability>/
                └── spec.md
```

其中：

- `openspec/specs/` 表示当前事实规范
- `openspec/changes/` 表示单次变更工作区
- `docs/solutions/*.md` 是本 skill 的方案来源文档，不是 OpenSpec 官方 artifact

## OPSX 命令选择

| 场景 | 建议入口 |
| --- | --- |
| 需求零散，需要先探索 | `/opsx:explore` |
| 需求清晰，直接进入规划 | `/opsx:propose` |
| 希望分步生成产物 | `/opsx:new` + `/opsx:continue` |
| 希望一次生成全部规划产物 | `/opsx:ff` |
| 规范已确认，开始实现 | `/opsx:apply` |
| 变更完成，准备归档 | `/opsx:archive` |

如所选 profile 支持，还可以使用：

- `/opsx:verify`：验证实现是否符合规范
- `/opsx:sync`：把变更 spec 同步回主规范

## 使用示例

单方案：先写完整方案文档

```text
先帮我写一个完整方案文档，确认后再生成 OpenSpec change。
/superpowers-openspec
```

多方案：基于多个方案文档生成 OpenSpec change

```text
请基于 `docs/solutions/方案一.md` 和 `docs/solutions/方案二.md` 创建一个 OpenSpec change。
/superpowers-openspec
```

先定方案和计划：

```text
先把这个功能的方案和开发计划定下来，后面再落地。
/superpowers-openspec
```

设计并实现，但先进入规范阶段：

```text
帮我设计并实现短信发送功能。
/superpowers-openspec
```

输入零散，先探索：

```text
这是会议纪要，你先帮我整理需求，再决定怎么规范。
/superpowers-openspec
```

## 同步规则

方案文档和 OpenSpec 产物允许表达形式不同，但不应语义漂移。

- 如果方案文档发生实质变化，需要检查并更新对应 OpenSpec change 的 `proposal.md`、`spec.md`、`design.md` 和 `tasks.md`
- 如果 OpenSpec 产物发生实质变化，需要回写或更新对应方案文档
- 如果变化只影响执行拆分，不改变已确认方案，可以只更新 `tasks.md`，但仍需确认 `proposal.md` 与方案文档一致
- 如果两者暂时不同步，必须明确告知用户，不能假装已经一致

## 图示要求

如果仅靠文字不足以完整表达方案，应补图：

- 架构关系、模块边界、数据流：优先 Mermaid
- 业务流程、审批路径、状态流转：优先 Mermaid `flowchart` 或 `stateDiagram`
- 多角色、多服务、异步交互：优先 Mermaid `sequenceDiagram`
- 页面、表单、列表、弹窗结构：优先 ASCII 文本布局图

图示是 `docs/solutions/*.md`、`design.md` 或相关设计说明的一部分，不是 OpenSpec 官方新增 artifact。

如果输出 Mermaid 图，最后必须自检：代码块 fence、图类型、节点标识、括号与连线是否正确。

## 原始输入记录

如果用户明确要求保留原始输入、会议纪要原文或对话过程，可以在当前 change 目录下可选补充：

- `source-notes.md`
- `transcript.md`

这两个文件只是可选补充，不是 OpenSpec 官方默认 artifact，也不替代 `docs/solutions/*.md`、`proposal.md`、`spec.md`、`design.md` 或 `tasks.md`。

## 语言要求

除非用户明确要求其他语言，否则所有说明和文档正文都必须使用中文，包括：

- `docs/solutions/*.md`
- `proposal.md`
- `spec.md`
- `design.md`
- `tasks.md`
- 相关补充说明

## 参考文档

- `references/planning-workflow.md`
- `references/openspec-directory-structure.md`
- `references/openspec-command-examples.md`
- `references/intent-to-openspec-mapping.md`
- `references/skill-usage-sequence.md`
- `references/spec-template.md`
- `references/spec-checklist.md`
- `references/source-input-recording.md`
- `references/output-example.md`
