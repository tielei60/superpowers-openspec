# 中文意图到 OpenSpec 的映射

本文件说明：当用户在 `superpowers` 体系里使用中文表达“需求沟通、方案、计划、规范、实现”时，`superpowers-openspec` 应如何把这些意图稳定映射到 OpenSpec / OPSX。

目标不是重新发明一套命令，而是减少上层 `superpowers` 把本应进入规范阶段的请求过早吞掉。

## 核心原则

- `superpowers` 负责识别是否需要进入规范阶段
- `superpowers-openspec` 负责把中文意图映射到官方 OpenSpec 命令与产物
- 只要本轮核心诉求是“方案、计划、规范、需求沟通”，就不应因为句子里出现“实现”而直接进入编码
- 除非用户明确要求其他语言，否则生成的 `proposal.md`、`spec.md`、`design.md`、`tasks.md` 内容本身也应使用中文

## 常见中文意图映射

| 中文意图 | 典型说法 | OpenSpec 含义 | 主要产物/重点 | 推荐入口 |
| --- | --- | --- | --- | --- |
| 需求沟通 / 先分析 / 先梳理 | `先沟通需求` `先分析一下` `先帮我梳理` | 先收敛问题空间 | 假设、待确认问题、依赖、边界 | `/opsx:explore` |
| 先写方案 / 先定方案 | `先把方案定下来` `先写方案` | 说明为什么做、做什么、怎么设计 | `proposal.md` + `design.md` | `/opsx:propose` 或 `/opsx:ff` |
| 先写计划 / 开发计划 | `先写计划` `先把开发计划定下来` | 形成执行拆解 | `tasks.md` | 若前置未定，先 `/opsx:explore` 或 `/opsx:new` + `/opsx:continue` |
| 先定规范 / 规则 / 行为 | `先把规则写清楚` `先定规范` | 明确行为约束与场景定义 | `spec.md` | `/opsx:propose` |
| 方案 + 计划一起做 | `先把方案和开发计划定下来` | 先规划，再拆执行 | `proposal.md` + `design.md` + `tasks.md` | `/opsx:new` + `/opsx:continue` 或 `/opsx:ff` |
| 设计并实现 / 规划并落地 | `帮我设计并实现短信发送功能` | 带实现诉求的规范入口 | 先确定 proposal/spec/design/tasks，再实现 | 先 `/opsx:propose` 或 `/opsx:explore`，不要直接编码 |
| 直接全出 | `proposal、spec、design、tasks 一次生成` | 一次性生成完整规划产物 | `proposal.md` `spec.md` `design.md` `tasks.md` | `/opsx:ff` |
| 开始实现 | `按 tasks 开始做` `进入实现阶段` | 规范阶段已完成 | 消费现有规划产物进入实现 | `/opsx:apply` |
| 归档 | `这次变更做完了，归档` | 变更结束，不再活跃 | 归档当前 change | `/opsx:archive` |

## 路由优先级

当用户同时表达“规范意图”和“实现意图”时，按以下顺序判断：

1. 先判断是否涉及新功能、规则、接口、交互、数据结构、状态或角色变化
2. 如果是，再判断本轮是否出现 `方案`、`计划`、`规范`、`需求沟通` 这些关键词或等价表达
3. 只要出现，就优先路由到 `superpowers-openspec`
4. 在 OpenSpec 产物明确前，不进入直接实现建议

## 典型反例

以下做法说明路由错了：

- 用户说 `先把方案和开发计划定下来`，却直接返回编码步骤
- 用户说 `帮我设计并实现...`，却因为含有 `实现` 就跳过规范阶段
- 用户说 `先写规范`，却只给通用需求摘要，没有映射到 OpenSpec 命令与产物

## 推荐对外话术

- `当前请求虽然包含“实现”，但本轮核心诉求仍然是先定方案/计划，因此应先进入 OpenSpec 规范阶段。`
- `你说的“方案”默认对应 proposal.md 和 design.md；“计划”默认对应 tasks.md；“规范”默认对应 spec.md。`
- `如果关键信息还不完整，我会先建议 /opsx:explore，而不是直接开始实现。`
