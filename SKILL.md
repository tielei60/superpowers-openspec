---
name: superpowers-openspec
description: superpowers 的规范阶段子技能。用于把需求整理成可执行的中文 OpenSpec，并在规范完成前卡住实现、拆解和测试。
---

# Superpowers OpenSpec

这是 `superpowers` 在规范阶段调用的子技能。它只做一件事：把需求收敛成可执行的 spec，并确保在 spec 完成前不进入实现。

## 什么时候用

在这些情况下使用本 skill：

- 用户要求先分析、先写 spec、先做详细设计再开发
- 用户要求把会议纪要、口语需求或草稿整理成规范文档
- 用户明确提到 `OpenSpec`、规范阶段、详细设计、需求分析
- `superpowers` 已经进入规范阶段，当前任务是产出 spec

## 核心职责

1. 先收敛事实，再写规范。
2. 产出中文 OpenSpec 风格文档。
3. 补齐必要的架构图、流程图、时序图。
4. 做 Spec Review，发现问题就回改。
5. spec 未完成前，不进入拆解、实现、测试。

## 执行方式

- 输入不完整时，先列出已知事实、缺失信息和待确认项。
- 按参考文档中的 OpenSpec 结构写作。
- 如果现有规则、接口、状态或页面会受影响，先把冲突和差异写清楚。
- review 结论必须明确：通过、退回修改，或仍需补充。

## 停止条件

当 spec 已写完并完成 review 后，停在规范阶段，把后续工作交还给 `superpowers`。
如果用户只要求规范产物，不要顺手继续拆任务或写实现建议。

## 参考

- `references/chinese-governed-doc-writing.md`
