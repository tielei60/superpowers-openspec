# superpowers-openspec

`superpowers-openspec` 是一个面向 OpenSpec 的方案、规范与计划工作流 skill。

一句话概括：

```text
方案先确认，规范再承接，计划再落地。
```

## 定位

- 负责把中文的需求沟通、方案、规范、计划意图，稳定路由到官方 OpenSpec / OPSX 工作流
- 不重定义 OpenSpec 官方目录、命令或产物
- 详细规则以 `SKILL.md` 为准；`README.md` 只保留快速使用说明

## 适合什么时候用

使用本 skill：

- 用户要求先分析、先整理需求、先写 spec、先做详细设计
- 用户要求先写完整 markdown 方案，再生成 OpenSpec 任务
- 用户要求先定方案、规范或开发计划，再进入实现
- 用户提出功能改造、功能优化、流程优化、模块重构或能力升级，并且会影响规则、流程、接口、状态、数据结构或模块边界
- 用户把“设计 / 方案 / 计划”和“实现 / 开发 / 落地”写在同一句里
- 任务涉及新功能、业务规则、接口、交互、数据结构、状态流转或角色流程变化

不强制使用本 skill：

- 纯 bug 修复，且不涉及新规则、流程、接口或状态
- 纯文案、纯样式、纯配置值调整
- 单点技术修复或局部性能优化，影响范围明确且无需新增规范
- 用户只要求快速定位问题或直接给出修复建议

## 快速使用

如果环境支持 skill 命令方式，先进入：

```text
/superpowers-openspec
```

然后根据场景选择后续入口：

| 场景 | 建议入口 |
| --- | --- |
| 需求零散，需要先探索 | `/opsx:explore` |
| 需求清晰，直接进入规划 | `/opsx:propose` |
| 希望分步生成产物 | `/opsx:new` + `/opsx:continue` |
| 希望一次生成全部规划产物 | `/opsx:ff` |
| 规范已确认，开始实现 | `/opsx:apply` |
| 校验实现是否符合规范 | `/opsx:verify`（profile 支持时） |
| 把变更规范同步回主规范 | `/opsx:sync`（profile 支持时） |
| 变更完成，准备归档 | `/opsx:archive` |

## 关键门禁

### 完整方案文档先行

当用户要求先确认完整方案文档时，第一步是生成：

```text
docs/solutions/<主题>.md
```

最小要求：

- 正文和文件名都必须使用中文，不使用英文文件名或纯数字文件名
- 请求用户确认前，先询问是否需要方案文档自我闭环验证
- 自我闭环验证由用户决定，不是强制步骤
- 用户确认前，不创建或更新 OpenSpec change，也不直接进入 `/opsx:*`
- 如果 OpenSpec change 来源于方案文档，`proposal.md` 必须包含“来源方案文档”章节

完整流程、模板和同步规则见 `references/planning-workflow.md`。

### 规范阶段门禁

- 还处于方案、规范、计划阶段时，不应直接进入 `/opsx:apply`
- 如果假设、依赖、迁移、兼容性或验收口径仍未明确，优先 `/opsx:explore`，或使用 `/opsx:new` + `/opsx:continue` 分步补齐
- 如果 change 来源于一个或多个方案文档，来源关系写入 `proposal.md`，不要新增 `sources.md` 或 `source-docs.md`

### 表达完整性门禁

- 架构、流程、状态、时序等复杂关系，优先 Mermaid
- 页面、表单、列表、弹窗等结构说明，优先 ASCII 文本布局图
- 如果输出 Mermaid 图，交付前必须自检
- 除非用户明确要求其他语言，否则文档内容本身必须使用中文

### 文档可读性门禁

- 使用人类易读语义，避免 AI 式套话
- 术语首次出现需解释
- 优先短句，先说结论
- 对比、枚举、状态映射优先用表格
- 避免内部缩写和未解释代号

图示和产物分工见 `references/spec-template.md`，输出形态见 `references/output-example.md`。

## 最小映射

| 用户表达 | 默认处理 |
| --- | --- |
| `先沟通需求，再把功能做出来` | 先 `/opsx:explore` |
| `先把方案和开发计划定下来` | 优先进入规范阶段，再决定 `/opsx:propose`、`/opsx:new` + `/opsx:continue` 或 `/opsx:ff` |
| `先帮我写完整方案文档，确认后再生成 change` | 先 `docs/solutions/*.md`，确认后再进入 `/opsx:*` |
| `规划好了，开始实现` | `/opsx:apply` |
| `检查实现有没有偏离 spec` | `/opsx:verify`（profile 支持时） |

更细的中文意图映射与命令判断示例见 `references/intent-to-openspec-mapping.md`。

## 文档分工

- `SKILL.md`
  - 权威规则来源，保留触发条件、门禁、停止条件和默认映射
- `references/planning-workflow.md`
  - 完整方案文档先行流程、模板、自检和同步规则
- `references/intent-to-openspec-mapping.md`
  - 中文意图映射与从用户表达映射到 `/opsx:*` 的命令选择示例
- `references/output-example.md`
  - 标准输出形态和端到端响应示例
- `references/spec-template.md`
  - `proposal.md`、`spec.md`、`design.md`、`tasks.md` 的承载建议
- `references/spec-checklist.md`
  - 对齐检查清单
- `references/source-input-recording.md`
  - `source-notes.md` 与 `transcript.md` 的可选补充约定

## 本地 A/B 回归

仓库提供了一个本地可执行的 A/B benchmark 辅助脚本：

```bash
python3 scripts/abtest_regression.py check
python3 scripts/abtest_regression.py check --report .abtest/generated/check-report.json
python3 scripts/abtest_regression.py sync --report .abtest/generated/sync-report.json
python3 scripts/abtest_regression.py sync
python3 scripts/abtest_regression.py score --mode with_skill
python3 scripts/abtest_regression.py score --abtest-dir tests/fixtures/abtest --mode both --only q1,q6 --require-complete
python3 scripts/abtest_regression.py score --mode both --only q1,q6 --report .abtest/generated/score-report.json
```

- `check`
  - 校验跟踪配置与 `evals/evals.json` 及本地 `.abtest` 提示集是否一致
  - 可通过 `--report <path>` 输出 JSON 报告，便于后续接 CI 或批量比对
- `sync`
  - 从跟踪配置生成本地 `.abtest/with_skill/questions.json` 和 `.abtest/without_skill/questions.json`
  - 可通过 `--report <path>` 输出 JSON 报告；也可通过 `--abtest-dir <dir>` 指定目标目录
- `score`
  - 对 `.abtest/generated/` 下的本地生成输出做机器评分
  - 可通过 `--report <path>` 输出 JSON 报告，便于后续接 CI 或批量比对
  - 可通过 `--abtest-dir <dir>` 指向任意 benchmark 目录，例如仓库内的 `tests/fixtures/abtest`

脚本也支持 `--evals-path` 和 `--cases-path`，便于在测试或临时实验中替换输入配置，而不影响仓库默认文件。

`.abtest/` 是本地工作目录，不属于默认提交内容。

## 参考文档

- `references/planning-workflow.md`
- `references/solution-to-openspec-workflow.md`
- `references/openspec-directory-structure.md`
- `references/intent-to-openspec-mapping.md`
- `references/skill-usage-sequence.md`
- `references/spec-template.md`
- `references/spec-checklist.md`
- `references/source-input-recording.md`
- `references/output-example.md`
