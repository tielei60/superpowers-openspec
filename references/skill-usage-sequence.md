# 技能使用顺序

本文件说明 `superpowers-openspec` 在整体流程中的位置。

## 推荐顺序

```mermaid
flowchart LR
    A[using-superpowers] --> B[brainstorming]
    B --> C[superpowers-openspec]
    C --> D[OpenSpec / OPSX]
    D --> E[后续执行与验证]
```

## 分工关系

- `using-superpowers`
  - 负责识别当前任务是否可能需要进入规范阶段

- `brainstorming`
  - 负责把目标、范围和约束先澄清清楚

- `superpowers-openspec`
  - 负责把已确认的规范意图桥接到官方 OpenSpec / OPSX
  - 重点是选择合适的 `/opsx:*` 入口，而不是重写 OpenSpec

- OpenSpec / OPSX
  - 负责生成和维护官方规范产物
  - 例如 `proposal.md`、`spec.md`、`design.md`、`tasks.md`

- 后续执行与验证
  - 负责消费上述 OpenSpec 产物继续推进实现、验证和收尾

## 使用原则

- superpowers 负责调度
- OpenSpec 负责规范
- `superpowers-openspec` 负责桥接

如果某份说明把 `superpowers-openspec` 写成“OpenSpec 的替代规范体系”，那就是定位错误。
