# AGENTS.md

本文件面向在本仓库中工作的 AI agent，帮助快速理解仓库定位、关键约束和最短工作路径。

## 仓库定位

本仓库提供 `superpowers-openspec` skill。

目标不是重新定义 OpenSpec，而是把用户用中文表达的“方案、规范、计划、需求沟通”稳定路由到合适的 OpenSpec / OPSX 阶段，并补足方案先行、来源引用、图示建议和同步门禁。

核心原则：

- 方案先确认，规范再承接，计划再落地
- OpenSpec 官方语义以 `openspec/` 目录和 `/opsx:*` 命令为准
- `docs/solutions/*.md` 是本 skill 约定的上游方案来源，不是 OpenSpec 官方 artifact

## 先看哪些文件

开始修改前，优先阅读这些文件：

- [SKILL.md](/Users/tielei/workspace/skills/superpowers-openspec/SKILL.md)：skill 主说明，包含路由规则、门禁和停止条件
- [README.md](/Users/tielei/workspace/skills/superpowers-openspec/README.md)：对外使用说明和示例
- [references/planning-workflow.md](/Users/tielei/workspace/skills/superpowers-openspec/references/planning-workflow.md)：完整方案文档先行流程
- [references/spec-template.md](/Users/tielei/workspace/skills/superpowers-openspec/references/spec-template.md)：OpenSpec 产物承载建议
- [scripts/qa.sh](/Users/tielei/workspace/skills/superpowers-openspec/scripts/qa.sh)：仓库自检脚本

如需检查示例和预期输出，再看：

- [references/output-example.md](/Users/tielei/workspace/skills/superpowers-openspec/references/output-example.md)
- [references/openspec-command-examples.md](/Users/tielei/workspace/skills/superpowers-openspec/references/openspec-command-examples.md)
- [evals/evals.json](/Users/tielei/workspace/skills/superpowers-openspec/evals/evals.json)

## 关键规则

### 语言和命名

- 除非用户明确要求其他语言，否则说明和产物正文都必须使用中文
- `docs/solutions/*.md` 的文件名也必须使用中文
- 不使用英文方案文件名，不使用纯数字方案文件名
- 示例文件名应写成 `docs/solutions/示例方案.md`、`docs/solutions/方案一.md`、`docs/solutions/方案二.md` 这类形式

### 方案先行门禁

- 如果用户要求先落地完整 markdown 方案，先生成 `docs/solutions/<主题>.md`
- 在用户确认方案文档之前，不创建或更新 OpenSpec change
- 在请求用户确认前，先询问是否需要“方案文档自我闭环验证”
- 自我闭环验证由用户决定，不是强制门禁

### OpenSpec 产物约束

- 不要把 `docs/solutions/*.md` 写成 OpenSpec 官方 artifact
- 不要新增 `sources.md` 或 `source-docs.md`
- 如果 OpenSpec change 来源于方案文档，`proposal.md` 必须包含“来源方案文档”章节
- `proposal.md`、`spec.md`、`design.md`、`tasks.md` 仍是官方工作区中的核心产物

### 图示规则

- 架构、流程、状态、时序等复杂关系优先用 Mermaid
- 页面、表单、列表、弹窗结构优先用 ASCII 文本布局图
- 如果输出 Mermaid，交付前要自检语法和结构
- 不要把 Mermaid 图重新定义成独立强制 artifact

### 同步规则

- 如果方案文档发生实质变化，检查并同步 `proposal.md`、`spec.md`、`design.md`、`tasks.md`
- 如果 OpenSpec 产物发生实质变化，检查是否需要回写方案文档
- 如果只改任务拆分、未改变已确认方案，可以只更新 `tasks.md`，但仍要确认 `proposal.md` 与方案文档一致

## 推荐工作方式

处理这类修改时，通常按这个顺序：

1. 先改 [SKILL.md](/Users/tielei/workspace/skills/superpowers-openspec/SKILL.md) 或相关 `references/*.md`
2. 再同步 [README.md](/Users/tielei/workspace/skills/superpowers-openspec/README.md) 中的对外说明
3. 如规则有变化，更新 [evals/evals.json](/Users/tielei/workspace/skills/superpowers-openspec/evals/evals.json) 和 [scripts/qa.sh](/Users/tielei/workspace/skills/superpowers-openspec/scripts/qa.sh)
4. 最后全文搜索旧示例、旧占位符和相互矛盾的说法

建议优先搜索这些模式：

- `docs/solutions/<topic>.md`
- `example-solution.md`
- `docs/solutions/1.md`
- `docs/solutions/2.md`
- `sources.md`
- `source-docs.md`

## 验证

完成修改后，至少执行：

```bash
./scripts/qa.sh
```

如果 QA 失败，先修正规则文案、示例、评测和脚本之间的不一致，再结束本次修改。

## 不要做什么

- 不要重定义 OpenSpec 官方目录和 artifact
- 不要绕过方案确认门禁，直接进入 OpenSpec change
- 不要只改一处文档而忽略 README、reference、eval、QA 之间的一致性
- 不要把“必须中文”退化成“尽量中文”
