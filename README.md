# superpowers-openspec

`superpowers-openspec` 是一个桥接 skill，用于把 `superpowers` 体系里的“先分析、先写 spec、先整理需求、先做详细设计、先写方案或计划”意图，映射到官方 OpenSpec / OPSX 工作流。

它也处理一种很常见的混合表达：用户把“设计 / 方案 / 计划”和“实现 / 开发 / 落地”写在同一句里，例如“帮我设计并实现短信发送功能”。只要任务本质上涉及新功能、规则、接口、交互、数据结构、状态或角色流转变化，就应先命中本 skill，再进入后续实现阶段。

本仓库不重新定义 OpenSpec。本仓库的职责，是让 superpowers 的调度能力和 OpenSpec 的规范能力协同工作。

更具体地说，这个项目希望借用 `superpowers` 的“识别与分流”能力，把“需求沟通、方案管理、计划拆解、规范沉淀”统一落到 OpenSpec 的官方产物和命令体系里。

## 角色定位

- `superpowers`
  - 负责技能选择、阶段门禁和后续调度

- OpenSpec / OPSX
  - 负责规范产物、变更目录和命令工作流

- `superpowers-openspec`
  - 负责把 superpowers 侧的规范意图桥接到官方 OpenSpec / OPSX

## 官方目录模型

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

## 官方命令模型

仓库说明与示例统一对齐以下常用命令：

- `openspec init`
- `openspec update`
- `/opsx:explore`
- `/opsx:propose`
- `/opsx:new`
- `/opsx:continue`
- `/opsx:ff`
- `/opsx:apply`
- `/opsx:archive`

如所选 profile 支持，高级命令还包括：

- `/opsx:verify`：验证实现是否符合规范，需当前 profile 明确支持此命令
- `/opsx:sync`：把变更 spec 同步回主规范，需当前 profile 明确支持此命令

若所选 profile 不支持，不要主动引导用户使用上述两个命令。

默认理解如下：

- 需求零散，先探索：`/opsx:explore`
- 需求完整，直接进入规划：`/opsx:propose`
- 需要按步骤生成产物：`/opsx:new` + `/opsx:continue`
- 需要一次生成规划产物：`/opsx:ff`
- 进入实现：`/opsx:apply`
- 完成归档：`/opsx:archive`

## 这个 skill 解决什么问题

它主要解决两个问题：

1. 避免在 superpowers 里把“先写规范”直接做成自定义格式，偏离 OpenSpec 官方结构
2. 让 superpowers 的调度层可以稳定地把用户意图导入官方 `/opsx:*` 工作流

更落地地说，这个桥接层最终会输出三类结果：

- 当前最合适的 `/opsx:*` 命令
- 当前应生成或更新的 OpenSpec 产物
- 当前是否仍应停留在规范阶段，而不是直接实现

当方案中的架构边界、流程分支、时序关系或页面布局仅靠文字难以完整表达时，这个 skill 还应明确提醒：

- 在后续 OpenSpec 产物中补充图示
- 默认优先 Mermaid
- 页面文本布局优先使用 ASCII 文本布局图
- 图示属于 `design.md` 或相关设计说明的一部分，而不是本仓库重新定义的独立官方 artifact

当方案看起来“差不多能做”，但仍存在关键假设、待确认问题、外部依赖、兼容性影响、历史数据迁移或验收方式未定时，这个 skill 也应明确提醒：

- 先把这些未决项列出来
- 不要把未决方案包装成“已经完整可执行”
- 必要时优先使用 `/opsx:explore` 或 `/opsx:new` + `/opsx:continue` 分步补齐

如果用户明确要求保留原始输入、会议纪要原文或对话过程，也可以在当前 change 目录下可选补充：

- `source-notes.md`
- `transcript.md`

这两个文件是本仓库约定的可选补充，不是官方默认强制 artifact。

## 使用入口

如果你是在 superpowers 体系里使用这个仓库：

- 由 `using-superpowers` 判断是否可能需要进入规范阶段
- 由 `brainstorming` 先澄清目标和边界
- 由 `superpowers-openspec` 把意图桥接到官方 OpenSpec / OPSX

如果用户同时说了“设计”和“实现”，不要仅因为出现了“实现”就跳过本 skill。对于新功能或规则/接口/状态变化，这类表达应优先被理解为“先进入规范阶段，再继续实现”。

同样地，如果用户说的是“先写方案”“先写计划”“先把规范定下来”“先沟通需求”，也应优先把这些中文意图映射到 OpenSpec 的官方产物：

- `方案` → `proposal.md` + `design.md`
- `计划` → `tasks.md`
- `规范 / 规则` → `spec.md`
- `需求沟通 / 先分析 / 先梳理` → 先收敛问题空间，再决定进入 `/opsx:explore`、`/opsx:propose` 或分步流程

这部分映射规则详见 `references/intent-to-openspec-mapping.md`。

除非用户明确要求其他语言，否则这些产物的文档内容本身也应使用中文，而不只是桥接说明使用中文。

真正给 agent 的触发边界、默认映射和执行规则，以 `SKILL.md` 为准。

## 命令方式使用

如果当前环境支持 skill 命令方式，优先通过本项目 skill 入口使用：

```text
/superpowers-openspec
```

这个命令的作用不是直接替代 `/opsx:*`，而是先进入本桥接 skill，由它根据你的中文意图给出下一步应该使用的官方 OpenSpec / OPSX 命令。

推荐用法：

- 先输入你的真实需求
- 再通过 `/superpowers-openspec` 进入桥接层
- 由桥接层判断下一步应走 `/opsx:explore`、`/opsx:propose`、`/opsx:new`、`/opsx:ff`、`/opsx:apply` 或 `/opsx:archive`

例如：

```text
帮我设计并实现短信发送功能
/superpowers-openspec
```

```text
先把这个功能的方案和开发计划定下来
/superpowers-openspec
```

```text
先沟通需求，再决定怎么规范
/superpowers-openspec
```

进入 `/superpowers-openspec` 之后，后续通常会得到如下官方命令建议：

### 1. 先探索需求

适用场景：

- 需求零散
- 来自会议纪要、聊天记录或口语描述
- 还有很多假设、依赖、验收口径没定

建议命令：

```text
/opsx:explore
```

典型说法：

- `先帮我整理需求，再决定怎么规范`
- `先沟通一下需求`
- `先把问题空间摸清楚`

### 2. 直接进入规划

适用场景：

- 需求边界清晰
- 已明确要先写方案、规范或设计

建议命令：

```text
/opsx:propose
```

典型说法：

- `先写 spec`
- `先做详细设计`
- `先把方案定下来`

### 3. 分步生成 proposal / spec / design / tasks

适用场景：

- 想先建 change
- 希望边生成边确认

建议命令：

```text
/opsx:new
/opsx:continue
```

典型说法：

- `我想一步一步来`
- `先建 change，再逐步补 proposal 和 design`

### 4. 一次性生成完整规划产物

适用场景：

- 需求已经清楚
- 不想分步确认

建议命令：

```text
/opsx:ff
```

典型说法：

- `直接把 proposal、spec、design、tasks 一次搞出来`
- `不想一步一步来，直接全出`

### 5. 开始实现

前提：

- `proposal.md`
- `spec.md`
- `design.md`
- `tasks.md`

已经确认完成。

建议命令：

```text
/opsx:apply
```

### 6. 归档

适用场景：

- 本次变更已经完成
- 不再作为活跃 change 继续推进

建议命令：

```text
/opsx:archive
```

### 命令方式的使用原则

- 优先用 `/superpowers-openspec` 作为本项目 skill 的命令入口
- `/superpowers-openspec` 负责桥接，真正落地执行时再进入官方 `/opsx:*`
- 如果一句话里同时出现“设计 / 方案 / 计划”和“实现 / 落地”，不要直接跳到实现命令，先用 `/superpowers-openspec`
- 如果输出 Mermaid 图，最后必须做一次自检，确认没有明显语法错误
- 除非用户明确要求其他语言，否则命令生成的文档内容本身也必须使用中文
- 如果不确定该用哪个命令，优先从 `/opsx:explore` 开始

## 参考文档

- `references/openspec-directory-structure.md`
- `references/openspec-command-examples.md`
- `references/intent-to-openspec-mapping.md`
- `references/skill-usage-sequence.md`
- `references/spec-template.md`
- `references/spec-checklist.md`
- `references/source-input-recording.md`
- `references/output-example.md`
