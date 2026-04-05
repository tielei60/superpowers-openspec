---
name: superpowers-openspec
description: >
  适用于：用户要求先分析、先写 spec、先整理需求、先做详细设计，或任务涉及新功能、规则变更、接口或交互变更、
  数据模型变更、状态或角色流转变化，需要先进入 OpenSpec 规范阶段。
---

# superpowers-openspec

这是一个用于 `superpowers` 体系的桥接 skill。
它的职责不是重新定义 OpenSpec，而是把“先分析、先写规范、先整理需求”的用户意图，映射到官方 OpenSpec / OPSX 工作流。

## 权威来源

以下内容以上游 OpenSpec / OPSX 为准：

- 目录结构：`openspec/specs/` 与 `openspec/changes/`
- 命令体系：`openspec init`、`openspec update` 与 `/opsx:*`
- 变更产物：`proposal.md`、`spec.md`、`design.md`、`tasks.md`

本 skill 不重新定义 OpenSpec 的目录、文件名或命令集合。

## 适用场景

满足任一情况时，进入本 skill：

1. 用户明确要求先做规范工作，例如：
   - 先分析
   - 先写 spec
   - 先整理需求
   - 先做详细设计
   - 先沉淀规范再开发

2. 任务本身涉及规范阶段判断，例如：
   - 新功能
   - 业务规则变更
   - 接口或交互变更
   - 数据结构变更
   - 状态流转变化
   - 模块边界调整
   - 多角色协作流程

3. 用户明确提到 OpenSpec、详细设计、规范阶段、需求文档等表达，并希望先定义再实现。

## 不适用场景

以下情况不要强制进入本 skill：

- 纯 bug 修复，且不涉及新规则、流程、接口或状态
- 纯文案修改、样式微调、配置值调整
- 单点技术修复，影响范围明确且无需新增规范
- 用户只要求快速定位问题或直接给出修复建议

若无法判断，先做最小边界判断：

- 只要涉及规则、流程、接口、状态、角色或数据结构变化，就进入 OpenSpec 阶段
- 否则交还上层 superpowers skill 或按普通任务处理

## 核心职责

本 skill 只负责桥接和门禁：

1. 在上层 superpowers 已决定进入规范阶段后，选择合适的官方 OPSX 入口
2. 把用户输入映射到合适的官方 OPSX 命令
3. 明确当前应生成或更新哪些 OpenSpec 产物
4. 在规范阶段未完成前，阻止直接进入实现

它不负责发明新的 OpenSpec 目录格式，也不负责取代 OpenSpec 的命令工作流。

## 为什么有时必须补图

有些方案和需求，只靠连续文字并不能完整表达真实约束。尤其在以下情况中，图示不是“锦上添花”，而是降低歧义的必要补充：

- 架构边界多，只写文字容易看不出模块关系、依赖方向和数据流向
- 流程分支多，只写步骤容易漏掉判断条件、异常回路和回退路径
- 涉及跨角色、跨系统、异步通知或状态推进时，只写描述容易看不出时序关系
- 涉及页面、表单、列表、弹窗或信息区块时，只写段落说明很难准确表达布局

可以把原因理解为：

- 文字擅长解释“是什么、为什么”
- 图更擅长表达“谁和谁有关、先后顺序、分支回路、页面结构”

因此，当桥接到 OpenSpec 阶段时，如果判断“仅靠文字不足以完整说明”，就应明确建议在后续产物中补充图示，而不是把复杂关系压缩成大段文字。

## 图示表达策略

图示属于 OpenSpec 产物里的表达方式，不是本 skill 新定义的独立官方 artifact。默认放在 `design.md`，必要时也可在相关 `spec.md` 场景说明中引用。

- 架构图
  - 适用于模块边界、系统关系、依赖方向、数据流向
  - 优先使用 Mermaid
- 流程图 / 状态图
  - 适用于业务流程、审批路径、异常分支、状态流转
  - 优先使用 Mermaid `flowchart` 或 `stateDiagram`
- 时序图
  - 适用于多角色、多服务、前后端交互、异步调用、事件通知
  - 优先使用 Mermaid `sequenceDiagram`
- 文本布局图
  - 适用于列表页、详情页、表单页、弹窗、信息面板等页面结构说明
  - 优先使用 ASCII 文本布局图

默认策略：

- 优先 Mermaid，因为它更适合表达结构、流程和时序，也更便于后续继续维护
- 当环境不便渲染 Mermaid、需要在纯终端快速审阅、或目标本质上是页面文本布局时，使用 ASCII 作为退化方案
- 不要把 `architecture.mermaid`、`flowchart.mermaid`、`sequence.mermaid` 重新定义为独立强制文件；图示应作为 `design.md` 或相关设计说明的一部分
- 不要在明明需要图示时只给一段纯文字总结

## 减少返工的完整性要求

进入 OpenSpec 阶段的目标，不只是把事情“写下来”，而是把那些会在开发阶段反复返工的问题尽量前置暴露出来。

当桥接到 OpenSpec / OPSX 时，如果存在以下任一情况，不应把方案误判为“已经足够完整，可以直接开发”：

- 关键假设还没有被明确写出
- 仍有待确认问题，但没有列出来
- 外部依赖、上游接口、第三方约束没有被识别
- 兼容性影响、历史数据迁移、状态延续规则没有说明
- 验收标准、完成判断、验证方式不清楚

因此，桥接输出除了命令和产物外，必要时还应明确指出这些“防返工信息”：

- 已知事实与关键假设
- 待确认问题与缺失输入
- 外部依赖与约束来源
- 兼容性、迁移、回滚或降级关注点
- 验收标准与验证方式

如果这些信息还明显不完整：

- 优先使用 `/opsx:explore` 先收敛问题空间
- 或使用 `/opsx:new` + `/opsx:continue` 分步补齐
- 不要直接把任务推进到“完整 tasks 已可执行”的假象

## 可选的原始输入记录

如果用户明确要求保留原始输入，可在当前 change 目录下可选补充 `source-notes.md`（摘录/来源）或 `transcript.md`（完整对话过程）。两者均为可选补充，不是官方强制 artifact。

详见 `references/source-input-recording.md`。

## 默认映射

进入本 skill 后，优先使用以下映射：

- 输入完整、需求边界较清晰
  - 优先进入 `/opsx:propose`

- 输入零散、来自会议纪要、聊天记录或口语描述
  - 优先进入 `/opsx:explore`
  - 收敛后进入 `/opsx:propose`

- 关键信息存在明显未决项，例如假设未写清、依赖不明、迁移或验收口径未定
  - 优先进入 `/opsx:explore`
  - 或使用 `/opsx:new` + `/opsx:continue` 分步补齐

- 用户希望按步骤生成 proposal / spec / design / tasks
  - 使用 `/opsx:new`
  - 然后使用 `/opsx:continue`
  - 或一次性使用 `/opsx:ff`

- 规范已完成，开始实现
  - 交给 `/opsx:apply`

- 变更已完成，准备归档
  - 交给 `/opsx:archive`

- 需要验证实现与规范一致性，或把变更 spec 同步回主规范
  - 在所选 profile 支持时使用 `/opsx:verify` 与 `/opsx:sync`

## 对外说明方式

必要时可直接向上层 agent 或用户说明：

- 当前任务应先进入 OpenSpec 阶段
- 该阶段使用官方 `openspec/` 目录和 `/opsx:*` 命令
- `superpowers-openspec` 的职责是桥接，不是重写 OpenSpec
- 如果仅靠文字不足以完整表达方案，应在后续 OpenSpec 产物中补充 Mermaid 图或 ASCII 文本布局图
- 如果当前方案仍有假设、依赖、迁移、兼容性或验收口径未定，应先显式列出，再决定是否继续进入更细的规划产物

## 语言要求

本 skill 的默认工作语言不是“尽量中文”，而是“必须中文”。

- 桥接结论必须使用中文
- 命令建议必须使用中文说明
- 产物说明、门禁提示、未决项提醒、图示建议都必须使用中文
- 只有当用户明确要求其他语言时，才可以切换

这样做的目的，是避免在多轮对话中逐渐漂移成中英混杂、术语不一致或说明风格前后失配。

因此，除非用户明确要求其他语言，否则必须使用中文说明桥接结论、命令建议和产物去向。

更具体地说，桥接后的输出应当包含以下三类必要结果，以及一个可选补充：

- 选择当前应执行的 `/opsx:*` 命令
- 说明当前应生成或更新的 OpenSpec 产物，例如 `proposal.md`、`spec.md`、`design.md`、`tasks.md`
- 明确当前仍处于规范阶段，因此不应直接进入实现
- 如果当前需求仅靠文字难以完整说明，明确指出建议补充的图示类型，以及它应进入 `design.md` 或相关设计说明
- 如果当前方案存在关键未决项，显式列出假设、待确认问题、依赖、迁移/兼容性影响与验收方式
- （可选）如果用户明确要求保留原始输入，建议增加 `source-notes.md` 或 `transcript.md`

## 停止条件

本 skill 在完成以下三件事后即停止，不再继续展开：

1. 已明确给出当前应执行的 `/opsx:*` 命令
2. 已说明当前阶段应生成或更新哪些 OpenSpec 产物
3. 已声明当前仍处于规范阶段，不应直接进入实现
4. 如有必要，已说明后续产物中应补充哪些 Mermaid 图或 ASCII 文本布局图
5. 如有必要，已点出仍需补齐的关键假设、依赖、迁移/兼容性或验收信息

停止后的接力由 OpenSpec / OPSX 承接，而不是由本 skill 继续推进产物内容。

如果用户继续追问具体的规范内容（如"帮我写 proposal.md"），应说明：这属于 OpenSpec 工作流本身的职责，当前 skill 的职责已完成。

## 与 superpowers 的关系

superpowers 负责调度 → `superpowers-openspec` 负责桥接 → OpenSpec / OPSX 负责规范产物。

详见 `references/skill-usage-sequence.md`。

## 参考文件

如需具体示例，按需查看：

- `references/openspec-directory-structure.md`
- `references/openspec-command-examples.md`
- `references/skill-usage-sequence.md`
- `references/spec-template.md`
- `references/spec-checklist.md`
- `references/source-input-recording.md`
- `references/output-example.md`
