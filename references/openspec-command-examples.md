# superpowers 到 OpenSpec / OPSX 的命令映射示例

本文件用于说明：当用户在 superpowers 体系里表达“先分析、先写 spec、先整理需求”时，`superpowers-openspec` 应如何桥接到官方 `/opsx:*` 命令。

## 常见映射

### 1. 先探索，再决定怎么规范

用户表达：

- `先分析一下再开发`
- `我这边需求还比较乱，先帮我理一下`
- `先把问题空间摸清楚`

推荐桥接：

- 优先进入 `/opsx:explore`
- 形成较稳定方向后，再进入 `/opsx:propose`

### 2. 需求已经比较完整，直接进入规划

用户表达：

- `先写 spec`
- `先做详细设计`
- `需求已经确定，直接按 OpenSpec 走`

推荐桥接：

- 优先进入 `/opsx:propose`

### 3. 输入是会议纪要、聊天记录、口语描述

用户表达：

- `这是会议纪要，你先整理需求`
- `下面是零散讨论，先沉淀规范`
- `先从这些聊天记录里提炼规则`

推荐桥接：

- 优先进入 `/opsx:explore`
- 或明确说明需要先收敛，再进入 `/opsx:propose`

### 4. 用户希望按步骤生成 proposal / spec / design / tasks

用户表达：

- `我想一步一步来`
- `先建 change，再逐步补 proposal 和 design`
- `不要一次全出，按阶段推进`

推荐桥接：

- 使用 `/opsx:new`
- 然后使用 `/opsx:continue`
- 若用户想一次补齐，也可改为 `/opsx:ff`

### 5. 用户希望一次把规划产物生成完

用户表达：

- `直接把 proposal、spec、design、tasks 一次搞出来`
- `我不需要分步看，先生成完整规划产物`

推荐桥接：

- 使用 `/opsx:ff`

### 6. 用户已经确认规划，准备进入实现

用户表达：

- `规划好了，开始做`
- `按 tasks 开始实现`
- `进入实现阶段`

推荐桥接：

- 使用 `/opsx:apply`

### 7. 用户要校验实现是否符合规范

用户表达：

- `检查实现有没有偏离 spec`
- `验证这次改动是否和规划一致`

推荐桥接：

- 在 profile 支持时使用 `/opsx:verify`

### 8. 用户要把变更规范同步回主规范

用户表达：

- `把这次变更 spec 合回主规范`
- `同步 changes 里的规范到主 specs`

推荐桥接：

- 在 profile 支持时使用 `/opsx:sync`

### 9. 用户希望保留原始输入或对话过程

用户表达：

- `把我原始需求也记录下来`
- `保留这次会议纪要原文`
- `把对话过程一起存档`

推荐桥接：

- 正常进入对应的 `/opsx:*` 规范流程
- 同时说明可选补充文件：
  - `openspec/changes/<change-name>/source-notes.md`
  - `openspec/changes/<change-name>/transcript.md`

说明原则：

- 这两个文件是可选补充
- 不属于 OpenSpec 官方默认强制 artifact
- 只在用户明确要求保留原始输入时建议使用

## 不推荐的桥接方式

以下表达说明桥接方向错了：

- 把用户直接导向 `docs/specs/<feature>/openspec.md`
- 把 Mermaid 三图当作固定强制输出
- 把 `superpowers-openspec` 写成一套独立命令体系
- 在规范阶段还没完成前就直接进入实现建议

## 对外可用话术

必要时可直接给出这种说明：

- `当前任务应先进入官方 OpenSpec / OPSX 规范阶段。`
- `如果需求还比较散，先用 /opsx:explore；如果需求已经清晰，直接用 /opsx:propose。`
- `如果你想按步骤生成 proposal / spec / design / tasks，可以使用 /opsx:new + /opsx:continue。`
- `如果你想一次生成规划产物，可以使用 /opsx:ff。`
- `如果你还想保留原始输入或对话过程，可以在 change 目录下可选增加 source-notes.md 或 transcript.md。`
