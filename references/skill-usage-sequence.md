# 技能使用顺序

> 用于说明在 `superpowers` 体系下，各技能的推荐调用顺序。

## 推荐顺序

```mermaid
flowchart LR
    A[using-superpowers] --> B[brainstorming]
    B --> C[superpowers-openspec]
    C --> D[writing-plans]
    D --> E[实现与测试]
    E --> F[verification-before-completion]
    F --> G[requesting-code-review]
```

## 各技能职责

- `using-superpowers`
  - 作用：先判断当前任务该使用哪个技能。
  - 场景：任何新对话或新任务开始时优先使用。

- `brainstorming`
  - 作用：先把需求想清楚，再进入设计。
  - 场景：需要澄清目标、约束、范围或方案时使用。

- `superpowers-openspec`
  - 作用：把需求整理成可执行的中文 OpenSpec。
  - 场景：任务进入分析/规范阶段，或用户明确要求先写 spec 时使用。

- `writing-plans`
  - 作用：把已确认的设计转成执行计划。
  - 场景：spec 已确认，准备拆解实施步骤时使用。

- `verification-before-completion`
  - 作用：在宣布完成前做证据校验。
  - 场景：准备提交、收尾或宣布完成时使用。

- `requesting-code-review`
  - 作用：在合并前请求代码审查。
  - 场景：重要改动完成后、或合并前使用。

## 使用原则

- 先选对技能，再推进工作。
- 需要先定义问题的，先走 `brainstorming`。
- 需要先写规范的，先走 `superpowers-openspec`。
- 需要先拆执行步骤的，先走 `writing-plans`。
- 需要确认完成质量的，先走 `verification-before-completion`。
- 需要外部审查的，先走 `requesting-code-review`。
