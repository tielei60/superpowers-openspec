---
name: superpowers-openspec
description: >
  适用：用户要求先分析/先写 spec/先整理需求/先做详细设计；或任务涉及新功能、规则变更、接口变更、数据结构变更、状态流转变化。
  职责：把 superpowers 意图桥接到官方 OpenSpec / OPSX，映射到 /opsx:explore、/opsx:propose、/opsx:new、/opsx:continue 或 /opsx:ff，并在规范阶段完成前阻止进入实现。
  不适用：纯 bug 修复、纯文案/样式/配置修改，且不涉及规则、流程、接口或状态变化。
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

默认使用中文说明桥接结论、命令建议和产物去向，除非用户明确要求其他语言。

更具体地说，桥接后的输出应当包含以下三类必要结果，以及一个可选补充：

- 选择当前应执行的 `/opsx:*` 命令
- 说明当前应生成或更新的 OpenSpec 产物，例如 `proposal.md`、`spec.md`、`design.md`、`tasks.md`
- 明确当前仍处于规范阶段，因此不应直接进入实现
- （可选）如果用户明确要求保留原始输入，建议增加 `source-notes.md` 或 `transcript.md`

## 停止条件

本 skill 在完成以下三件事后即停止，不再继续展开：

1. 已明确给出当前应执行的 `/opsx:*` 命令
2. 已说明当前阶段应生成或更新哪些 OpenSpec 产物
3. 已声明当前仍处于规范阶段，不应直接进入实现

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
