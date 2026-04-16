# 原始输入记录约定

本文件说明如何在 `superpowers-openspec` 中可选记录用户原始输入、会议纪要原文或对话过程。

## 定位

这不是 OpenSpec 官方默认 artifact。
这是本仓库在面向 OpenSpec 的方案、规范与计划工作流中提供的可选补充约定。

只有在用户明确要求保留原始输入时，才建议使用。

它和 `docs/solutions/*.md` 的职责不同：

- `source-notes.md` / `transcript.md` 记录原始输入、会议纪要或对话过程
- `docs/solutions/*.md` 记录讨论后形成、便于用户评审的已确认方案

默认不保存完整对话过程。真正用于生成 OpenSpec change 的上游方案，应优先沉淀到 `docs/solutions/*.md`。

## 推荐文件

### `openspec/changes/<change-name>/source-notes.md`

适用场景：

- 只想保留原始需求摘录
- 只想记录会议纪要中的关键片段
- 只想保留来源、背景材料和关键决策依据

建议内容：

- 原始输入摘要
- 关键原文摘录
- 需求来源说明
- 已确认事实
- 尚未确认但需要保留的上下文

### `openspec/changes/<change-name>/transcript.md`

适用场景：

- 需要保留更完整的对话过程
- 需要保留多轮澄清记录
- 需要把会议讨论原文作为变更附件保存

建议内容：

- 对话原文
- 会议纪要全文
- 多轮澄清记录
- 决策发生的上下文过程

## 使用原则

- 这两个文件都是可选补充
- 不替代 `proposal.md`、`spec.md`、`design.md`、`tasks.md`
- 不替代 `docs/solutions/*.md`
- 不应被描述成 OpenSpec 官方强制产物
- 仅在用户明确要求保留原始输入时添加

## 选择建议

优先使用 `source-notes.md`：

- 当你只需要保留关键输入证据，而不是完整聊天全文

使用 `transcript.md`：

- 当用户明确要求保留完整过程
- 当后续审计、复盘或追溯需要完整上下文

同时使用两者也可以，但建议职责分开：

- `source-notes.md` 保留摘要和重点
- `transcript.md` 保留全文

## 对外说明示例

可以这样说明：

- `如果你希望保留原始需求摘录，我可以在当前 change 下可选增加 source-notes.md。`
- `如果你希望保留完整对话过程，我可以在当前 change 下可选增加 transcript.md。`
- `这两个文件只是补充记录，不是 OpenSpec 官方默认强制 artifact。`
