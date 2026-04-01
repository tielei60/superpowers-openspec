# OpenSpec 官方目录结构

本文件只说明一件事：在 `superpowers-openspec` 里，OpenSpec 的目录结构以上游 `openspec/` 模型为准。

## 官方结构

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

## 目录语义

- `openspec/specs/`
  - 当前事实规范
  - 表示系统当前已经成立或应被视为真相的行为定义

- `openspec/changes/<change-name>/`
  - 单次变更工作区
  - 用于承载本次变更的 proposal、design、tasks 以及变更 spec

## 主要产物

- `proposal.md`
  - 说明为什么改、改什么、影响什么

- `specs/<capability>/spec.md`
  - 说明该能力的行为要求与场景

- `design.md`
  - 说明实现思路、边界、技术取舍和必要设计补充

- `tasks.md`
  - 说明实现清单

## 本仓库中的废弃写法

以下写法不再被本仓库视为 OpenSpec 官方标准：

- `docs/specs/<feature>/openspec.md`
- 强制要求独立 `architecture.mermaid`
- 强制要求独立 `flowchart.mermaid`
- 强制要求独立 `sequence.mermaid`

Mermaid 图仍然可以存在，但应作为 `design.md` 或相关设计说明的补充，而不是在本仓库里被重新定义为官方强制产物。

## 命名建议

- capability 目录使用有语义的英文短名
  - 例如：`auth`、`payments`、`approval-flow`

- change 目录使用描述性 kebab-case
  - 例如：`add-dark-mode`
  - 例如：`refine-approval-routing`
  - 例如：`fix-refund-state-transition`

## 使用本文件时的判断标准

如果某份文档、示例或评估仍然把 OpenSpec 说成：

- 规范文档固定放在 `docs/specs/...`
- 主文档固定叫 `openspec.md`
- Mermaid 三图必须是独立同级文件

那么它表达的就不是当前官方 OpenSpec / OPSX 目录语义，应视为旧模型残留并继续清理。
