# OpenSpec 对齐检查清单

本清单用于检查当前输出是否仍然符合官方 OpenSpec / OPSX 语义，而不是旧的自定义模型。

## 目录检查

- 是否使用 `openspec/specs/` 表示当前事实规范
- 是否使用 `openspec/changes/` 表示单次变更工作区
- 是否避免把 `docs/specs/<feature>/openspec.md` 当作官方标准

## 命令检查

- 是否使用 `openspec init`
- 是否使用 `openspec update`
- 是否正确使用 `/opsx:explore`
- 是否正确使用 `/opsx:propose`
- 是否在需要时说明 `/opsx:new`、`/opsx:continue`、`/opsx:ff`
- 是否在实现阶段使用 `/opsx:apply`
- 是否在归档阶段使用 `/opsx:archive`

## 产物检查

- 如果用户要求完整方案文档，是否先生成并确认 `docs/solutions/*.md`
- 在请求用户确认方案文档前，是否询问用户是否需要方案文档自我闭环验证
- 是否避免把方案文档自我闭环验证写成强制步骤
- 闭环验证完成后，是否询问用户是否需要先创建 `docs/solutions/references/<主题>-OpenSpec-拆分设计.md`
- 是否避免把 OpenSpec 拆分设计写成强制步骤
- 是否明确 `docs/solutions/*.md` 不是 OpenSpec 官方 artifact
- 如果 OpenSpec change 来源于方案文档，`proposal.md` 是否包含“来源方案文档”章节
- 如果来源是多个方案文档，`proposal.md` 是否列出全部来源
- 是否避免新增 `sources.md` 或 `source-docs.md` 作为来源关系文件
- 如果方案文档或 OpenSpec 产物发生实质变化，是否检查并同步另一侧
- 是否以 `proposal.md`、`spec.md`、`design.md`、`tasks.md` 为主
- 是否把 Mermaid 图当作设计补充，而不是重新定义为官方强制产物
- 当架构边界、流程分支、时序关系或页面布局仅靠文字难以说清时，是否明确要求补充图示
- 是否默认优先 Mermaid，并在页面文本布局或纯文本审阅场景下使用 ASCII
- 是否明确当前应生成或更新哪些 OpenSpec 产物
- 是否显式列出关键假设，而不是默认大家都已理解
- 是否显式列出待确认问题、缺失输入或未决边界
- 是否说明外部依赖、上游接口或第三方约束
- 是否说明兼容性、数据迁移、状态延续、回滚或降级关注点
- 是否说明验收标准与验证方式
- 如果用户要求保留原始输入，是否使用可选的 `source-notes.md` 或 `transcript.md`
- 是否明确这些原始输入记录文件只是可选补充，而不是官方默认 artifact

## 边界检查

- 是否清楚说明 `superpowers` 负责调度
- 是否清楚说明 OpenSpec / OPSX 负责规范
- 是否清楚说明 `superpowers-openspec` 负责组织方案、规范与计划
- 是否避免把本 skill 写成独立规范体系

## 误触发检查

- 纯 bug 修复时，是否避免强制进入 OpenSpec
- 纯文案、纯样式、纯配置修改时，是否避免强制进入 OpenSpec
- 只有在规则、流程、接口、状态或数据结构变化时，才进入规范阶段

## 可读性检查

- 是否避免 AI 式套话和生硬堆叠
- 术语首次出现是否解释
- 是否优先短句、先说结论
- 对比、枚举、状态映射是否优先用表格
- 是否避免内部缩写和未解释代号
- 技术细节是否说明实际含义
