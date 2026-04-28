# 仓库指南

## 项目结构与模块组织

本仓库提供 `superpowers-openspec` skill。`SKILL.md` 是权威行为说明，`README.md` 是对外快速使用说明。工作流参考文档放在 `references/`，回归评测配置放在 `evals/`，可执行检查脚本放在 `scripts/`，Python 单元测试和夹具放在 `tests/`。`docs/superpowers/` 用于内部方案和计划产物。`.abtest/` 是本地生成工作区，不应当作源文件维护。

## 构建、测试与开发命令

- `./scripts/qa.sh`：运行完整质量门禁，包含 JSON 校验、文档一致性、A/B 配置检查、评分冒烟和单元测试。
- `python3 -m unittest discover -s tests -v`：只运行 Python 单元测试。
- `python3 scripts/abtest_regression.py check`：校验 `evals/evals.json`、`evals/abtest_cases.json` 和提示集是否一致。
- `python3 scripts/abtest_regression.py sync`：重新生成 `.abtest/with_skill/questions.json` 和 `.abtest/without_skill/questions.json`。
- `python3 scripts/abtest_regression.py score --abtest-dir tests/fixtures/abtest --mode both --only q1,q6 --require-complete`：运行可复现的评分冒烟测试。

## 代码风格与命名约定

skill 和参考文档使用 Markdown，脚本和测试使用 Python 3，质量门禁使用 Bash。Python 保持 4 空格缩进，函数名应清楚表达行为，必要时补充类型标注。JSON 使用 2 空格缩进。除非用户明确要求其他语言，面向 skill 的说明和示例应使用中文。方案文档示例必须使用中文文件名，例如 `docs/solutions/示例方案.md`，不要使用纯英文或纯数字文件名。

## 测试指南

当路由规则、门禁、示例或评分逻辑变化时，同步新增或更新回归用例。单元测试基于 `unittest`，主要位于 `tests/test_abtest_regression.py`；测试名应描述被保护的行为。任何实质性修改完成前，都应运行 `./scripts/qa.sh`。

## 提交与 Pull Request 指南

近期提交使用简洁的 Conventional Commit 风格前缀，常见为 `docs:` 和 `feat:`。提交标题应使用祈使语气并说明范围，例如 `docs: clarify planning workflow gate`。Pull Request 应说明行为变化、列出受影响的文件或规则区域、注明 eval 或 fixture 更新，并附上验证命令输出，通常是 `./scripts/qa.sh`。

## Agent 专用说明

不要重定义 OpenSpec 官方 artifact 或目录。如果规则发生变化，需要检查相关文档、reference、eval、QA 脚本和示例是否一致。不要新增 `sources.md` 或 `source-docs.md`；来源方案文档应写入 `proposal.md`。
