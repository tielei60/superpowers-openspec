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

- 是否以 `proposal.md`、`spec.md`、`design.md`、`tasks.md` 为主
- 是否把 Mermaid 图当作设计补充，而不是重新定义为官方强制产物
- 是否明确当前应生成或更新哪些 OpenSpec 产物
- 如果用户要求保留原始输入，是否使用可选的 `source-notes.md` 或 `transcript.md`
- 是否明确这些原始输入记录文件只是可选补充，而不是官方默认 artifact

## 边界检查

- 是否清楚说明 `superpowers` 负责调度
- 是否清楚说明 OpenSpec / OPSX 负责规范
- 是否清楚说明 `superpowers-openspec` 负责桥接
- 是否避免把本 skill 写成独立规范体系

## 误触发检查

- 纯 bug 修复时，是否避免强制进入 OpenSpec
- 纯文案、纯样式、纯配置修改时，是否避免强制进入 OpenSpec
- 只有在规则、流程、接口、状态或数据结构变化时，才进入规范桥接
