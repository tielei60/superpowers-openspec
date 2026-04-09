# superpowers-openspec 桥接输出示例

本文件提供两个端到端的完整桥接输出示例，帮助使用者快速判断当前 skill 的输出是否正确。

每个示例包含：用户输入 → 触发判断 → 命令建议 → 产物说明 → 阶段门禁声明。

---

## 示例一：输入零散，走 `/opsx:explore` 路径

### 用户输入

> 这是上午开会的纪要，大概说的是要做一个新的消息通知中心，支持站内信、邮件和 push，还讨论了一些偏好设置，但很多细节没定。你先帮我整理一下，再决定怎么规范。

### 触发判断

- 输入来源：会议纪要，口语描述，细节未定
- 涉及：新功能、多渠道交互、用户偏好状态
- 判断：满足适用场景（新功能 + 接口/状态变化），进入 `superpowers-openspec`
- 输入零散程度：高 → 优先 `/opsx:explore`

### 桥接输出

**当前建议的命令：**

```
/opsx:explore
```

输入比较零散，建议先通过 `/opsx:explore` 把问题空间收敛清楚，再进入 `/opsx:propose` 生成正式规划产物。

**当前阶段应生成或更新的产物：**

`/opsx:explore` 阶段通常不直接生成固定产物，而是帮助确认以下内容后再推进：

- 能力边界：消息通知中心的职责范围
- 渠道拆分：站内信 / 邮件 / push 是否统一抽象，还是各自独立
- 偏好设置：属于用户配置，还是通知规则的一部分
- 关键约束：是否涉及已有系统的接口变更

探索收敛后，进入 `/opsx:propose`，在 `openspec/changes/<change-name>/` 下生成：

- `proposal.md`
- `specs/<capability>/spec.md`
- `design.md`
- `tasks.md`

**阶段门禁：**

当前仍处于规范阶段，不应直接进入实现。请在 `/opsx:explore` 完成、方向收敛后，再执行 `/opsx:propose` 生成正式产物，然后才能进入 `/opsx:apply`。

---

## 示例二：输入完整，走 `/opsx:propose` 路径

### 用户输入

> 我要做一个审批流模块。规则是：金额 5000 以下由直属 leader 审批，5000 到 50000 需要再加 CFO 审批，50000 以上还需要 CEO。审批人可以拒绝并填写原因，发起人可以撤回未完成的审批单。先别写代码，先帮我按 OpenSpec 走。

### 触发判断

- 输入完整，边界清晰
- 涉及：新功能、业务规则（金额阈值）、多角色流程、状态流转（发起 / 审批中 / 拒绝 / 撤回）
- 判断：满足适用场景，进入 `superpowers-openspec`
- 输入完整程度：高 → 优先 `/opsx:propose`

### 桥接输出

**当前建议的命令：**

```
/opsx:propose
```

需求边界清晰，可以直接进入 `/opsx:propose` 生成本次变更的规划产物。

**当前阶段应生成或更新的产物：**

在 `openspec/changes/add-approval-flow/` 下生成以下产物：

| 产物 | 路径 | 主要内容 |
|---|---|---|
| `proposal.md` | `openspec/changes/add-approval-flow/proposal.md` | 为什么加审批流、改什么、影响哪些模块 |
| `spec.md` | `openspec/changes/add-approval-flow/specs/approval-flow/spec.md` | 审批规则、状态机、角色行为、边界场景 |
| `design.md` | `openspec/changes/add-approval-flow/design.md` | 实现思路、模块边界、时序说明、关键设计取舍 |
| `tasks.md` | `openspec/changes/add-approval-flow/tasks.md` | 按顺序拆分的实现清单 |

当前事实规范（`openspec/specs/`）在变更通过后，由 `/opsx:sync` 更新（需 profile 支持）。

**阶段门禁：**

当前仍处于规范阶段，不应直接进入实现。请在上述产物生成并确认后，再执行 `/opsx:apply` 进入实现阶段。

---

## 正确输出的共同特征

一个符合 `superpowers-openspec` 预期的桥接输出应具备以下特征：

1. **明确说明推荐的 `/opsx:*` 命令**，不含糊、不列多个并列选项作为"都可以"
2. **说明当前应生成或更新哪些产物**，给出具体路径（`openspec/changes/<name>/...`）
3. **显式声明当前仍在规范阶段**，不提前进入实现建议
4. **不使用旧的自定义目录**，不出现 `docs/specs/<feature>/openspec.md` 表述
5. **不把 Mermaid 图列为强制产物**，只在 `design.md` 语义下作为补充提及
6. **当仅靠文字不足以完整表达时，明确指出建议补充的图示类型**，默认优先 Mermaid，页面文本布局优先 ASCII
7. **当存在关键未决项时，明确列出假设、依赖、迁移/兼容性影响或验收方式**，而不是直接把规划说成已完整可执行
8. **如果输出 Mermaid 图，最后做一次自检**，确认图类型、节点/参与者标识、括号与连线、代码块 fence 等没有明显语法错误
9. **除非用户明确要求其他语言，文档内容本身必须使用中文**，而不只是桥接说明使用中文

## 示例三：一次性生成全部产物，走 `/opsx:ff` 路径

### 用户输入

> 需求我已经想清楚了，不想一步一步来，直接把 proposal、spec、design、tasks 一次性都生成出来。

### 触发判断

- 输入完整，用户明确不需要分步推进
- 目标：一次性生成全部规划产物
- 判断：满足适用场景，进入 `superpowers-openspec`
- 特征：用户明确拒绝分步 → 优先 `/opsx:ff`，而非 `/opsx:new` + `/opsx:continue`

### 桥接输出

**当前建议的命令：**

```
/opsx:ff
```

需求已经清晰，且不需要分步确认，直接使用 `/opsx:ff` 一次性生成本次变更的全部规划产物。

**当前阶段应生成的产物（落在 `openspec/changes/<change-name>/` 下）：**

| 产物 | 说明 |
|---|---|
| `proposal.md` | 为什么做、改什么、影响范围 |
| `specs/<capability>/spec.md` | 行为要求与场景定义 |
| `design.md` | 实现思路、模块边界、关键设计取舍 |
| `tasks.md` | 可执行的实现清单 |

**与 `/opsx:new` + `/opsx:continue` 的区别：**

- `/opsx:ff`：适合需求已定、不需要逐步确认的场景，一次输出全部产物
- `/opsx:new` + `/opsx:continue`：适合需要分步审阅、每个产物生成后人工确认再继续的场景

**阶段门禁：**

当前仍处于规范阶段，不进入实现。请在上述产物生成并确认后，再执行 `/opsx:apply` 进入实现阶段。

---

## 常见错误输出特征

以下输出说明 skill 触发或映射存在问题：

- 直接给出代码实现，没有先经过规范阶段
- 输出 `docs/specs/<feature>/openspec.md` 路径
- 把 `architecture.mermaid` 列为必须生成的独立强制文件
- 面对复杂架构、流程、时序或页面布局，仍然只给纯文字说明
- 假设、依赖、迁移或验收口径明显未定时，仍然直接给出最终任务清单
- 同时推荐多个 `/opsx:*` 命令而不做取舍（如"你可以用 explore 也可以用 propose"）
- 没有阶段门禁声明，直接进入实现建议
- 用户明确说"不想分步"时，仍然给出 `/opsx:new` + `/opsx:continue` 分步方案
