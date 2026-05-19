---
name: superpowers-openspec
description: >
  适用于：用户要求先分析、先写 spec、先整理需求、先做详细设计、先写完整 markdown 方案、先写方案或计划，或提出功能改造、功能优化、流程优化、模块重构、能力升级，
  或把"设计/方案/计划"和"实现/开发/落地"混在一起表达，但任务本质涉及新功能、规则变更、接口或交互变更、数据模型变更、状态或角色流转变化。
---

# superpowers-openspec

面向 OpenSpec 的方案、规范与计划工作流 skill。
职责：帮助用户把方案、规范和计划的阶段边界说清楚，再将已确认内容落到官方 OpenSpec / OPSX 工作流。

## 权威来源

以下内容以上游 OpenSpec / OPSX 为准，不由本 skill 重定义：

- 目录结构：`openspec/specs/` 与 `openspec/changes/`
- 命令体系：`openspec init`、`openspec update` 与 `/opsx:*`
- 变更产物：`proposal.md`、`spec.md`、`design.md`、`tasks.md`

## 触发与不触发

满足任一即触发：

- 用户要求先分析、先整理需求、先写 spec、先做详细设计、先写方案或计划
- 用户要求先写完整 markdown 方案、先确认完整方案文档
- 任务属于新功能、功能改造、功能优化、流程优化、模块重构、能力升级
- 任务涉及业务规则、接口、交互、数据结构、状态流转或模块边界变更
- 用户把"设计/方案/计划"和"实现/开发/落地"混在一起表达

最小判断规则：只要涉及规则、流程、接口、状态、角色、模块边界或数据结构变化，就进入 OpenSpec 阶段。

不触发：

- 纯 bug 修复（不涉及新规则、流程、接口或状态）
- 纯文案、样式、配置值调整
- 局部性能优化，影响范围明确且无需新增规范
- 用户只要求快速定位问题或直接给出修复建议

## 混合意图优先级

当同时出现"设计/方案/计划"和"实现/开发/落地"信号时：

1. 先判断任务是否涉及新功能、规则、接口、数据结构、状态或角色变化
2. 如果是，优先进入 `superpowers-openspec`
3. 规范阶段完成后，再交由实现入口承接

`帮我设计并实现短信发送功能`、`先沟通需求，再把功能做出来` 等表达，都是"带实现诉求的规范阶段入口"。

## 整体流程

```text
触发判断 → 方案设计 → 用户确认 → OpenSpec 承接 → 实现入口
```

核心边界：**方案文档确认前不进 OpenSpec，规范完成前不进实现。**

## 默认映射

| 场景 | 推荐入口 | 重点产物 |
|------|----------|----------|
| 输入完整、边界清晰 | `/opsx:propose` | proposal + spec + design + tasks |
| 输入零散、需收敛 | `/opsx:explore` → `/opsx:propose` | 先补齐假设和边界 |
| 用户要完整方案文档 | 先 `docs/solutions/*.md` | 确认后再进 `/opsx:*` |
| 用户要方案 | `/opsx:propose` 或 `/opsx:ff` | proposal + design |
| 用户要计划 | 前置未定则先 explore | tasks |
| 用户要规范 | `/opsx:propose` | spec |
| 分步生成 | `/opsx:new` + `/opsx:continue` | 逐步补齐 |
| 一次全出 | `/opsx:ff` | 全部产物 |
| 关键未决项存在 | `/opsx:explore` | 先收敛再规划 |
| 规范已完成 | `/opsx:apply` | 进入实现 |
| 变更已完成 | `/opsx:archive` | 归档 |
| 验证一致性 | `/opsx:verify`（profile 支持时） | — |
| 同步回主规范 | `/opsx:sync`（profile 支持时） | — |

详见 `references/intent-to-openspec-mapping.md`。

## 完整方案文档先行

当用户要求先写完整方案文档时，执行以下门禁：

1. 先生成 `docs/solutions/<主题>.md`，正文和文件名必须使用中文
2. 方案至少覆盖：背景、目标、非目标、已确认决策、关键取舍、方案设计、风险、待确认问题、验收标准
3. 复杂结构补充 Mermaid 或 ASCII 图示
4. 请求确认前，询问用户是否需要"方案文档自我闭环验证"（由用户决定，不是强制门禁）
5. 闭环验证后，询问是否需要创建 `docs/solutions/references/<主题>-OpenSpec-拆分设计.md`（由用户决定，不是强制门禁）
6. **用户确认前，不应创建或更新 OpenSpec change，不进入 `/opsx:*`**
7. 确认后，`proposal.md` 必须靠前包含"来源方案文档"章节
8. 多方案来源时全部列出，不新增 `sources.md` 或 `source-docs.md`

同步规则：方案文档与 OpenSpec 产物发生实质变化时，需检查并同步另一侧。

详细模板和示例见 `references/planning-workflow.md`。

## 基于方案文档生成 OpenSpec 计划

硬门禁：

- 只处理已确认方案文档；未确认时回到 `references/planning-workflow.md`
- 必须先输出"方案提取摘要"，再生成产物
- 摘要至少覆盖：来源方案、变更目标、范围、非目标、关键规则、设计要点、风险与兼容、验收标准、是否可生成
- 存在关键未决项时，不直接生成完整 `tasks.md`

最小产物边界：

| 产物 | 内容 |
|------|------|
| `proposal.md` | 为什么做、做什么、范围、非目标、来源方案文档 |
| `spec.md` | 业务规则、功能行为、异常路径、验收场景 |
| `design.md` | 架构、流程、模块边界、数据流、图示、设计取舍 |
| `tasks.md` | 可执行任务、迁移任务、验证任务；每项有"完成判断" |

摘要模板和对齐检查表见 `references/solution-to-openspec-workflow.md`。

## 为什么有时必须补图

图示不是锦上添花，而是降低歧义的必要补充。文字擅长"是什么、为什么"，图擅长"谁和谁有关、先后顺序、分支回路、页面结构"。

| 场景 | 优先方式 | 落点 |
|------|----------|------|
| 架构图：模块边界、依赖方向、数据流 | Mermaid | `design.md` |
| 流程图 / 状态图：审批路径、异常分支、状态流转 | Mermaid flowchart/stateDiagram | `design.md` |
| 时序图：多角色交互、异步调用、事件通知 | Mermaid sequenceDiagram | `design.md` |
| 页面、表单、列表、弹窗布局 | ASCII 文本布局图 | `design.md` |

规则：
- 优先 Mermaid，页面布局退化为 ASCII
- 如果输出 Mermaid 图，最后必须做一次自检（fence 闭合、图类型、节点标识、连线成对）
- 图示是 `design.md` 的组成部分，不是独立强制文件
- 不要在明明需要图示时只给纯文字总结

## 减少返工的完整性要求

进入 OpenSpec 时，如果以下任一信息缺失，不应声称方案已完整：

- 关键假设未写明
- 待确认问题未列出
- 外部依赖、上游接口、第三方约束未识别
- 兼容性、迁移、状态延续、回滚规则未说明
- 验收标准、验证方式不清楚

信息不完整时，优先 `/opsx:explore` 收敛，或 `/opsx:new` + `/opsx:continue` 分步补齐。

## 语言要求

默认工作语言是**必须中文**：工作流判断、命令建议、产物说明、门禁提示，以及输出的文档内容本身也必须使用中文，包括 `docs/solutions/*.md`、`proposal.md`、`spec.md`、`design.md`、`tasks.md`。只有当用户明确要求其他语言时，才可以切换。

## 文档可读性要求

输出文档应使用人类易读语义，避免 AI 式套话和内部缩写。

- 术语首次出现需解释
- 优先短句，先说结论
- 对比、枚举、状态映射优先用表格
- 避免模板化套话、内部缩写和未解释代号

## 常见错误

| 错误 | 正确做法 |
|------|----------|
| 用户说"设计并实现"就直接编码 | 先进入规范阶段 |
| 不应输出 `docs/specs/<feature>/openspec.md` | 使用 `openspec/changes/` |
| 把 Mermaid 文件列为独立强制产物 | 图示放在 `design.md` 内 |
| 跳过 `docs/solutions/*.md` 直接生成 change | 先写方案文档，确认后再进 OpenSpec |
| 新增 `sources.md` 记录来源 | 来源写入 `proposal.md` |
| 未决项明显时仍给完整 tasks | 先 `/opsx:explore` 收敛 |
| 同时推荐多个 `/opsx:*` 不做取舍 | 给出唯一推荐命令 |

## 停止条件

本 skill 完成以下事项后即停止：

1. 已说明应生成 `docs/solutions/<主题>.md` 或已给出 `/opsx:*` 命令
2. 已说明当前应生成或更新哪些产物
3. 已声明当前处于规范阶段，不进入实现
4. 如有必要，已点出未决项、图示建议、来源关系或可选的 `source-notes.md`/`transcript.md`

停止后由 OpenSpec / OPSX 承接。详见 `references/skill-usage-sequence.md`。

## 参考文件

- `references/openspec-directory-structure.md` — 官方目录结构
- `references/intent-to-openspec-mapping.md` — 中文意图映射与命令示例
- `references/planning-workflow.md` — 方案文档先行流程与模板
- `references/solution-to-openspec-workflow.md` — 方案转 OpenSpec 计划
- `references/skill-usage-sequence.md` — skill 使用顺序
- `references/spec-template.md` — 产物承载建议
- `references/spec-checklist.md` — 对齐检查清单
- `references/source-input-recording.md` — 原始输入记录约定
- `references/output-example.md` — 输出示例
