# superpowers-openspec

`superpowers-openspec` 是 `superpowers` 体系里的规范阶段子技能，用于把需求整理成可执行的中文 OpenSpec，并在规范完成前卡住实现、拆解和测试。

## 使用顺序

推荐顺序如下：

```mermaid
flowchart LR
    A[using-superpowers] --> B[brainstorming]
    B --> C[superpowers-openspec]
    C --> D[writing-plans]
    D --> E[实现与测试]
    E --> F[verification-before-completion]
    F --> G[requesting-code-review]
```

## 怎么调用这个 skill

如果你希望明确触发 `superpowers-openspec`，可以直接使用下面这类命令：

- `请使用 superpowers-openspec，基于下面的需求产出中文 OpenSpec 初稿。`
- `请使用 superpowers-openspec，先列出已知事实、缺失信息和待确认项，再输出 spec。`
- `请使用 superpowers-openspec，把会议纪要整理成可执行规范，并补齐 Mermaid 图。`
- `请使用 superpowers-openspec，先分析现有规则与新需求的差异，再输出变更 spec。`
- `请使用 superpowers-openspec，对下面这份 spec 做 review，并给出明确结论。`

更完整的调用方式见 `references/openspec-command-examples.md`。

## 各技能职责

- `using-superpowers`
  - 先判断当前任务该使用哪个技能。

- `brainstorming`
  - 先把需求想清楚，再进入设计。

- `superpowers-openspec`
  - 把需求整理成可执行的中文 OpenSpec。

- `writing-plans`
  - 把已确认的设计转成执行计划。

- `verification-before-completion`
  - 在宣布完成前做证据校验。

- `requesting-code-review`
  - 在合并前请求代码审查。

## A/B 对比结论

下面这 6 组样例用于比较“使用 skill”和“不使用 skill”时的输出差异：

| 题号 | `with_skill` 表现 | `without_skill` 表现 | 结论 |
|---|---|---|---|
| q1 | 先进入规范阶段，先列事实和待确认项 | 只给通用建议，偏口头整理 | `with_skill` 更像规范输出 |
| q2 | 明确 OpenSpec 结构、异常、review | 只做会议纪要总结 | `with_skill` 明显更完整 |
| q3 | 停在 spec/review，不往后走 | 仍然会继续往拆解/实现延伸 | `with_skill` 门禁更强 |
| q4 | 先写差异、边界和冲突 | 只是提示先梳理，再给方案 | `with_skill` 更能控制规范质量 |
| q5 | 明确不应强制走完整 spec | 直接给修复建议 | 这里 `without_skill` 更自然，说明负边界有效 |
| q6 | 先抽事实，再补待确认项，输出 OpenSpec | 只是整理成简单流程 | `with_skill` 更适合交给后续开发 |

一句话结论：`superpowers-openspec` 的价值主要体现在“规范门禁”和“输出结构”上，尤其对 `q2/q3/q4/q6` 这种场景差异明显；而 `q5` 说明它现在没有把纯 bug 修复误拉进 OpenSpec，这个边界是对的。

## 本地对照目录

本地比较样例放在 `.abtest/`，并通过 git 忽略：

- `.abtest/with_skill/`
- `.abtest/without_skill/`
- `.abtest/generated/`

这些目录不会进入提交。
