# superpowers-openspec 输出示例

本文件只关注一件事：`superpowers-openspec` 的响应应该长什么样。

命令选择本身见 `references/intent-to-openspec-mapping.md`，完整方案文档先行流程见 `references/planning-workflow.md`。这里不重复讲整套路由规则，只展示合格输出的最小结构和代表性示例。

## 标准输出骨架

一次合格输出，通常至少包含以下三部分：

1. 当前建议的命令或第一步
2. 当前阶段应生成或更新的产物
3. 阶段门禁声明

必要时再补：

- 假设、依赖、迁移、兼容性或验收口径等未决项
- 应补充的 Mermaid 图或 ASCII 文本布局图
- `proposal.md` 中的”来源方案文档”关系

可读性要求：文档需使用人类易读语义，避免 AI 式套话。术语需解释，先说结论，对比枚举优先用表格，避免内部缩写和未解释代号。

## 示例一：输入零散，优先 `/opsx:explore`

### 用户输入

> 这是会议纪要，你先帮我整理需求，再决定怎么规范。

### 合格输出

**当前建议的命令：**

```text
/opsx:explore
```

输入仍然零散，建议先通过 `/opsx:explore` 收敛问题空间，再进入 `/opsx:propose`。

**当前阶段应生成或更新的产物：**

- 当前重点不是直接生成固定产物，而是先补齐能力边界、关键假设、依赖和待确认问题
- 收敛后，再在 `openspec/changes/<change-name>/` 下生成 `proposal.md`、`specs/<capability>/spec.md`、`design.md`、`tasks.md`

**阶段门禁：**

当前仍处于规范阶段，不应直接进入实现。

## 示例二：输入完整，优先 `/opsx:propose`

### 用户输入

> 审批流规则已经明确，先别写代码，直接按 OpenSpec 走。

### 合格输出

**当前建议的命令：**

```text
/opsx:propose
```

需求边界已经清晰，可以直接进入 `/opsx:propose` 生成本次变更的规划产物。

**当前阶段应生成或更新的产物：**

- `openspec/changes/<change-name>/proposal.md`
- `openspec/changes/<change-name>/specs/<capability>/spec.md`
- `openspec/changes/<change-name>/design.md`
- `openspec/changes/<change-name>/tasks.md`

如果架构、流程或时序复杂，应在 `design.md` 中补 Mermaid 图；页面结构说明优先 ASCII 文本布局图。

**阶段门禁：**

当前仍处于规范阶段，应在上述产物确认后再进入 `/opsx:apply`。

## 示例三：完整方案文档先行

### 用户输入

> 先帮我写一个完整 markdown 方案文档，确认没问题后再生成 OpenSpec change。

### 合格输出

**当前建议的第一步：**

```text
生成 docs/solutions/<主题>.md
```

**当前阶段应生成或更新的产物：**

- 先生成便于用户完整评审的 `docs/solutions/<主题>.md`
- 方案文档正文和文件名都必须使用中文
- 如果方案涉及复杂架构、流程、状态、时序或页面结构，应补 Mermaid 或 ASCII 图示

**阶段门禁：**

- 在请求用户确认前，应先询问是否需要方案文档自我闭环验证
- 自我闭环验证由用户决定，不是强制步骤
- 闭环验证完成后，应询问是否需要先创建 `docs/solutions/references/<主题>-OpenSpec-拆分设计.md`
- 用户确认前，不应创建或更新 OpenSpec change，也不应直接进入 `/opsx:*`

**确认后的来源关系：**

`proposal.md` 必须包含“来源方案文档”章节，例如：

```md
## 来源方案文档

本变更基于以下已确认方案文档生成：

- `docs/solutions/<主题>.md`
```

## 示例四：一次性生成全部规划产物

### 用户输入

> 需求已经想清楚了，不想分步，直接把 proposal、spec、design、tasks 一次性都生成出来。

### 合格输出

**当前建议的命令：**

```text
/opsx:ff
```

**当前阶段应生成或更新的产物：**

- `proposal.md`
- `specs/<capability>/spec.md`
- `design.md`
- `tasks.md`

**阶段门禁：**

当前仍处于规范阶段，不直接进入实现；应在产物确认后再执行 `/opsx:apply`。

## 共同特征

一个符合 `superpowers-openspec` 预期的输出，通常具备以下特征：

- 明确给出当前最推荐的 `/opsx:*` 命令，或明确给出“先生成 `docs/solutions/*.md`”
- 说明当前应生成或更新哪些产物，而不是只给泛化建议
- 显式声明当前仍处于规范阶段，不提前进入实现
- 当关键未决项仍存在时，显式列出假设、依赖、迁移/兼容性影响或验收方式
- 当仅靠文字不足以完整表达时，明确指出应补充的图示类型
- 当 OpenSpec change 来源于方案文档时，说明 `proposal.md` 需要写入“来源方案文档”

## 常见错误输出特征

以下输出说明 skill 触发或映射存在问题：

- 直接给出代码实现，没有先经过规范阶段
- 输出 `docs/specs/<feature>/openspec.md` 路径
- 把 `architecture.mermaid` 列为必须生成的独立强制文件
- 用户要求完整方案文档时，跳过 `docs/solutions/*.md` 直接生成 OpenSpec change
- 新增 `sources.md` 或 `source-docs.md` 记录来源方案，而不是写入 `proposal.md`
- 假设、依赖、迁移或验收口径明显未定时，仍然直接给出最终任务清单
- 同时推荐多个 `/opsx:*` 命令而不做取舍
- 没有阶段门禁声明，直接进入实现建议
