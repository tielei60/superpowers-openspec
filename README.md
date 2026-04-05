# superpowers-openspec

`superpowers-openspec` 是一个桥接 skill，用于把 `superpowers` 体系里的“先分析、先写 spec、先整理需求、先做详细设计”意图，映射到官方 OpenSpec / OPSX 工作流。

本仓库不重新定义 OpenSpec。本仓库的职责，是让 superpowers 的调度能力和 OpenSpec 的规范能力协同工作。

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

真正给 agent 的触发边界、默认映射和执行规则，以 `SKILL.md` 为准。

## 参考文档

- `references/openspec-directory-structure.md`
- `references/openspec-command-examples.md`
- `references/skill-usage-sequence.md`
- `references/spec-template.md`
- `references/spec-checklist.md`
- `references/source-input-recording.md`
- `references/output-example.md`
