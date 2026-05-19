#!/usr/bin/env bash
# scripts/qa.sh
# superpowers-openspec 结构完整性检查脚本
# 用法：bash scripts/qa.sh
# 退出码：0 = 全部通过，1 = 存在失败项

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

PASS=0
FAIL=0

ok()   { echo "  PASS: $*"; PASS=$((PASS + 1)); }
fail() { echo "  FAIL: $*"; FAIL=$((FAIL + 1)); }
section() { echo; echo "=== $* ==="; }

# ─────────────────────────────────────────────
# [1] JSON 语法检查
# ─────────────────────────────────────────────
section "[1] JSON syntax"
if python3 -m json.tool evals/evals.json > /dev/null 2>&1; then
  ok "evals/evals.json"
else
  fail "evals/evals.json — JSON 解析失败"
fi

# ─────────────────────────────────────────────
# [2] 引用文件存在性检查
# ─────────────────────────────────────────────
section "[2] Reference file existence"
python3 - <<'EOF'
import re, os, sys

files_to_scan = ["SKILL.md", "README.md"]
all_refs = set()
for f in files_to_scan:
    with open(f) as fh:
        for m in re.findall(r'references/[\w\-]+\.md', fh.read()):
            all_refs.add(m)

fail = False
for ref in sorted(all_refs):
    if os.path.isfile(ref):
        print(f"  PASS: {ref}")
    else:
        print(f"  FAIL: {ref} — 文件不存在")
        fail = True

sys.exit(1 if fail else 0)
EOF
if [ $? -ne 0 ]; then FAIL=$((FAIL + 1)); else PASS=$((PASS + 1)); fi

# ─────────────────────────────────────────────
# [3] SKILL.md 核心关键词存在性
# ─────────────────────────────────────────────
section "[3] Core keyword presence (SKILL.md)"
python3 - <<'EOF'
import sys
keywords = [
    "/opsx:explore", "/opsx:propose", "/opsx:new", "/opsx:continue",
    "/opsx:ff", "/opsx:apply", "/opsx:archive",
    "openspec/specs/", "openspec/changes/",
    "proposal.md", "design.md", "tasks.md",
    "docs/solutions/", "来源方案文档",
]
with open("SKILL.md") as f:
    content = f.read()
fail = False
for kw in keywords:
    if kw in content:
        print(f"  PASS: {kw}")
    else:
        print(f"  FAIL: 缺少关键词 [{kw}]")
        fail = True
sys.exit(1 if fail else 0)
EOF
if [ $? -ne 0 ]; then FAIL=$((FAIL + 1)); else PASS=$((PASS + 1)); fi

# ─────────────────────────────────────────────
# [4] 旧模型残留扫描（规范性文件）
# ─────────────────────────────────────────────
section "[4] Old-pattern leak scan (SKILL.md + README.md)"
python3 - <<'EOF'
import re, sys

normative = ["SKILL.md", "README.md"]
bad_patterns = [
    r"docs/specs/<feature>/openspec\.md",
    r"architecture\.mermaid",
    r"flowchart\.mermaid",
    r"sequence\.mermaid",
]
negative_context_markers = ["不要把", "不应", "不是", "而不是", "重新定义", "旧模式", "残留"]

fail = False
for fname in normative:
    with open(fname) as f:
        lines = f.readlines()
    for i, line in enumerate(lines, 1):
        if any(marker in line for marker in negative_context_markers):
            continue
        for pat in bad_patterns:
            if re.search(pat, line):
                print(f"  FAIL: [{fname}:{i}] 旧模式残留 [{pat}]")
                fail = True

if not fail:
    print("  PASS: 无旧模型残留")
sys.exit(1 if fail else 0)
EOF
if [ $? -ne 0 ]; then FAIL=$((FAIL + 1)); else PASS=$((PASS + 1)); fi

# ─────────────────────────────────────────────
# [5] Eval schema 字段完整性
# ─────────────────────────────────────────────
section "[5] Eval schema check"
python3 - <<'EOF'
import json, sys

with open("evals/evals.json") as f:
    data = json.load(f)

required_fields = {"id", "tags", "prompt", "expected_output", "not_expected", "files"}
fail = False
for ev in data["evals"]:
    missing = required_fields - set(ev.keys())
    if missing:
        print(f"  FAIL: eval #{ev['id']} 缺少字段: {missing}")
        fail = True
    else:
        print(f"  PASS: eval #{ev['id']} {ev['tags']}")

sys.exit(1 if fail else 0)
EOF
if [ $? -ne 0 ]; then FAIL=$((FAIL + 1)); else PASS=$((PASS + 1)); fi

# ─────────────────────────────────────────────
# [6] Eval 命令覆盖率检查
# ─────────────────────────────────────────────
section "[6] Eval command coverage"
python3 - <<'EOF'
import json, sys

with open("evals/evals.json") as f:
    data = json.load(f)

required_cmds = [
    "/opsx:explore", "/opsx:propose", "/opsx:ff",
    "/opsx:apply", "/opsx:verify", "/opsx:sync", "/opsx:archive",
]
covered = set()
for ev in data["evals"]:
    combined = ev["expected_output"] + ev["prompt"]
    for cmd in required_cmds:
        if cmd in combined:
            covered.add(cmd)

fail = False
for cmd in required_cmds:
    if cmd in covered:
        print(f"  PASS: {cmd}")
    else:
        print(f"  FAIL: {cmd} — 无 eval 覆盖")
        fail = True

sys.exit(1 if fail else 0)
EOF
if [ $? -ne 0 ]; then FAIL=$((FAIL + 1)); else PASS=$((PASS + 1)); fi

# ─────────────────────────────────────────────
# [7] description frontmatter 质量检查
# ─────────────────────────────────────────────
section "[7] Description frontmatter quality"
python3 - <<'EOF'
import re, sys

with open("SKILL.md") as f:
    content = f.read()

parts = content.split("---", 2)
if len(parts) < 3:
    print("  FAIL: 缺少 YAML frontmatter")
    sys.exit(1)

frontmatter = parts[1]
m = re.search(r"description:\s*>\s*(.*?)\n\s*$", frontmatter, re.S)
if not m:
    m = re.search(r'description:\s*"([^"]+)"', frontmatter, re.S)
if not m:
    print("  FAIL: 缺少 description 字段")
    sys.exit(1)

description = " ".join(m.group(1).split())
checks = {
    "description 以 适用于 开头": description.startswith("适用于"),
    "description 包含触发条件": any(k in description for k in ["新功能", "规则变更", "接口", "交互", "数据模型", "状态", "角色流转", "OpenSpec 规范阶段"]),
    "description 包含功能改造优化触发": any(k in description for k in ["功能改造", "功能优化", "流程优化", "模块重构", "能力升级"]),
    "description 包含方案文档触发": any(k in description for k in ["完整 markdown 方案", "完整方案文档", "方案文档", "docs/solutions"]),
    "description 包含混合意图触发": any(k in description for k in ["方案", "计划", "设计/方案/计划", "实现/开发/落地"]),
    "description 不混入命令流程或旧定位": "/opsx:" not in description and "职责" not in description and "桥接" not in description,
    "正文保留停止条件节": "## 停止条件" in content,
    "正文包含混合意图处理": any(k in content for k in ["帮我设计并实现短信发送功能", "混合意图优先级", "带实现诉求的规范阶段入口"]),
    "正文包含方案规范计划定位": all(k in content for k in ["面向 OpenSpec 的方案、规范与计划工作流", "方案", "计划", "规范"]),
    "正文包含功能改造优化边界": all(k in content for k in ["功能改造", "功能优化", "局部性能优化"]),
}

fail = False
for desc, result in checks.items():
    if result:
        print(f"  PASS: {desc}")
    else:
        print(f"  FAIL: {desc}")
        fail = True

sys.exit(1 if fail else 0)
EOF
if [ $? -ne 0 ]; then FAIL=$((FAIL + 1)); else PASS=$((PASS + 1)); fi

# ─────────────────────────────────────────────
# [8] 图示策略存在性检查
# ─────────────────────────────────────────────
section "[8] Diagram guidance presence"
python3 - <<'EOF'
import sys

with open("SKILL.md") as f:
    skill = f.read()
with open("references/spec-template.md") as f:
    tmpl = f.read()

checks = {
    "SKILL.md 包含补图原因": "为什么有时必须补图" in skill,
    "SKILL.md 包含 Mermaid 优先策略": "优先 Mermaid" in skill,
    "SKILL.md 包含 Mermaid 自检要求": "如果输出 Mermaid 图，最后必须做一次自检" in skill,
    "SKILL.md 包含 ASCII 文本布局图": "ASCII" in skill and "布局图" in skill,
    "SKILL.md 包含架构图/流程图/时序图": all(x in skill for x in ["架构图", "流程图", "时序图"]),
    "spec-template 含图示补充原则": "图示补充原则" in tmpl,
    "spec-template 含 Mermaid 自检要求": "如果输出 Mermaid 图，最后应做一次自检" in tmpl,
}

fail = False
for desc, result in checks.items():
    if result:
        print(f"  PASS: {desc}")
    else:
        print(f"  FAIL: {desc}")
        fail = True

sys.exit(1 if fail else 0)
EOF
if [ $? -ne 0 ]; then FAIL=$((FAIL + 1)); else PASS=$((PASS + 1)); fi

# ─────────────────────────────────────────────
# [9] 防返工完整性检查
# ─────────────────────────────────────────────
section "[9] Anti-rework guidance presence"
python3 - <<'EOF'
import sys

with open("SKILL.md") as f:
    skill = f.read()
with open("references/spec-template.md") as f:
    tmpl = f.read()
with open("references/spec-checklist.md") as f:
    checklist = f.read()

checks = {
    "SKILL.md 含减少返工完整性要求": "减少返工的完整性要求" in skill,
    "SKILL.md 含假设/待确认/依赖/验收": all(x in skill for x in ["假设", "待确认", "依赖", "验收"]),
    "spec-template 含减少返工统一检查维度": "减少返工的统一检查维度" in tmpl,
    "spec-checklist 含防返工检查项": all(x in checklist for x in ["关键假设", "待确认问题", "外部依赖", "兼容性", "验收标准"]),
}

fail = False
for desc, result in checks.items():
    if result:
        print(f"  PASS: {desc}")
    else:
        print(f"  FAIL: {desc}")
        fail = True

sys.exit(1 if fail else 0)
EOF
if [ $? -ne 0 ]; then FAIL=$((FAIL + 1)); else PASS=$((PASS + 1)); fi

# ─────────────────────────────────────────────
# [10] 中文意图映射存在性检查
# ─────────────────────────────────────────────
section "[10] Intent mapping presence"
python3 - <<'EOF'
import sys

with open("references/intent-to-openspec-mapping.md") as f:
    mapping = f.read()

checks = {
    "意图映射文档存在方案映射": "proposal.md" in mapping and "design.md" in mapping,
    "意图映射文档存在计划映射": "tasks.md" in mapping and "开发计划" in mapping,
    "意图映射文档存在规范映射": "spec.md" in mapping and "规范" in mapping,
    "意图映射文档存在路由优先级": "路由优先级" in mapping and "superpowers-openspec" in mapping,
}

fail = False
for desc, result in checks.items():
    if result:
        print(f"  PASS: {desc}")
    else:
        print(f"  FAIL: {desc}")
        fail = True

sys.exit(1 if fail else 0)
EOF
if [ $? -ne 0 ]; then FAIL=$((FAIL + 1)); else PASS=$((PASS + 1)); fi

# ─────────────────────────────────────────────
# [11] 方案先行工作流检查
# ─────────────────────────────────────────────
section "[11] Planning workflow checks"
python3 - <<'EOF'
import sys, pathlib

root = pathlib.Path(".")
skill = (root / "SKILL.md").read_text()
readme = (root / "README.md").read_text()
template = (root / "references/spec-template.md").read_text()
checklist = (root / "references/spec-checklist.md").read_text()
source = (root / "references/source-input-recording.md").read_text()
commands = (root / "references/intent-to-openspec-mapping.md").read_text()
output = (root / "references/output-example.md").read_text()
workflow_path = root / "references/planning-workflow.md"
workflow = workflow_path.read_text() if workflow_path.exists() else ""

checks = {
    "planning-workflow reference 存在": workflow_path.exists(),
    "SKILL.md 含工作流中文定位": "面向 OpenSpec 的方案、规范与计划工作流" in skill,
    "SKILL.md 含 docs/solutions 门禁": "docs/solutions/" in skill and "用户确认" in skill and "不应创建或更新 OpenSpec change" in skill,
    "SKILL.md 含 proposal 来源引用": "来源方案文档" in skill and "proposal.md" in skill,
    "SKILL.md 含可选自检询问": "自我闭环验证" in skill and "询问用户" in skill and "不是强制门禁" in skill,
    "README.md 标明 quickstart 定位": "README.md` 只保留快速使用说明" in readme or "README 只保留快速使用说明" in readme,
    "README.md 含使用说明": "docs/solutions/" in readme and "来源方案文档" in readme and "快速使用" in readme,
    "README.md 含可选自检说明": "自我闭环验证由用户决定" in readme and "不是强制步骤" in readme,
    "README.md 含参考分工": "文档分工" in readme and "references/planning-workflow.md" in readme and "references/output-example.md" in readme,
    "reference 含中文模板": "# 方案：<标题>" in workflow and "必须使用中文" in workflow,
    "reference 含可选自检说明": "自我闭环验证不是强制门禁" in workflow and "由用户决定" in workflow,
    "命令示例含可选自检说明": "询问是否需要先做方案文档自我闭环验证" in commands and "不是强制步骤" in commands,
    "输出示例含可选自检说明": "询问是否需要方案文档自我闭环验证" in output and "不是强制步骤" in output,
    "reference 禁止 sources.md": "不新增 `sources.md`" in workflow and "source-docs.md" in workflow,
    "spec-template 含来源引用": "来源方案文档" in template and "docs/solutions/<主题>.md" in template,
    "spec-checklist 含同步检查": "是否检查并同步另一侧" in checklist,
    "spec-checklist 含可选自检检查": "是否询问用户是否需要方案文档自我闭环验证" in checklist and "强制步骤" in checklist,
    "source-input 区分 transcript 与方案文档": "docs/solutions/*.md" in source and "默认不保存完整对话过程" in source,
}

fail = False
for desc, result in checks.items():
    if result:
        print(f"  PASS: {desc}")
    else:
        print(f"  FAIL: {desc}")
        fail = True

sys.exit(1 if fail else 0)
EOF
if [ $? -ne 0 ]; then FAIL=$((FAIL + 1)); else PASS=$((PASS + 1)); fi

# ─────────────────────────────────────────────
# [12] 中文与相对路径检查
# ─────────────────────────────────────────────
section "[12] Chinese-first and relative-path checks"
python3 - <<'EOF'
import pathlib, sys

root = pathlib.Path(".")
files = [
    root / "SKILL.md",
    root / "README.md",
    root / ".abtest/with_skill/questions.json",
]

skill = (root / "SKILL.md").read_text()
checks = {
    "SKILL.md 含语言要求节": "## 语言要求" in skill and "## 文档可读性要求" in skill,
    "SKILL.md 强调必须中文": "必须中文" in skill and "只有当用户明确要求其他语言时" in skill,
    "SKILL.md 强调文档正文必须中文": "文档内容本身也必须使用中文" in skill and "proposal.md" in skill and "design.md" in skill,
    "SKILL.md 含可读性要求": "人类易读语义" in skill and "术语首次出现需解释" in skill,
}

fail = False
for desc, result in checks.items():
    if result:
        print(f"  PASS: {desc}")
    else:
        print(f"  FAIL: {desc}")
        fail = True

needle = str(pathlib.Path(".").resolve())
for path in files:
    content = path.read_text()
    if needle in content:
        print(f"  FAIL: [{path}] 含项目绝对路径")
        fail = True
    else:
        print(f"  PASS: [{path}] 无项目绝对路径")

sys.exit(1 if fail else 0)
EOF
if [ $? -ne 0 ]; then FAIL=$((FAIL + 1)); else PASS=$((PASS + 1)); fi

# ─────────────────────────────────────────────
# [13] 文档可读性跨文件一致性检查
# ─────────────────────────────────────────────
section "[13] Readability guidance cross-file check"
python3 - <<'EOF'
import sys

checks = {
    "SKILL.md 含文档可读性要求": "## 文档可读性要求" in open("SKILL.md").read(),
    "spec-template.md 含可读性原则": "文档可读性原则" in open("references/spec-template.md").read(),
    "spec-checklist.md 含可读性检查": "## 可读性检查" in open("references/spec-checklist.md").read(),
    "planning-workflow.md 含可读性要求": "可读性要求" in open("references/planning-workflow.md").read(),
    "intent-to-openspec-mapping.md 含可读性要求": "## 文档可读性要求" in open("references/intent-to-openspec-mapping.md").read(),
    "output-example.md 含可读性说明": "人类易读语义" in open("references/output-example.md").read(),
    "README.md 含可读性门禁": "## 文档可读性门禁" in open("README.md").read(),
}

fail = False
for desc, result in checks.items():
    if result:
        print(f"  PASS: {desc}")
    else:
        print(f"  FAIL: {desc}")
        fail = True

sys.exit(1 if fail else 0)
EOF
if [ $? -ne 0 ]; then FAIL=$((FAIL + 1)); else PASS=$((PASS + 1)); fi

# ─────────────────────────────────────────────
# [14] A/B benchmark config checks
# ─────────────────────────────────────────────
section "[14] A/B benchmark config checks"
if python3 scripts/abtest_regression.py check; then
  PASS=$((PASS + 1))
else
  FAIL=$((FAIL + 1))
fi

# ─────────────────────────────────────────────
# [14] Python unit tests
# ─────────────────────────────────────────────
section "[15] Reproducible A/B score smoke"
if python3 scripts/abtest_regression.py score --abtest-dir tests/fixtures/abtest --mode both --only q1,q6 --require-complete; then
  PASS=$((PASS + 1))
else
  FAIL=$((FAIL + 1))
fi

# ─────────────────────────────────────────────
# [15] Python unit tests
# ─────────────────────────────────────────────
section "[16] Python unit tests"
if python3 -m unittest discover -s tests -v; then
  PASS=$((PASS + 1))
else
  FAIL=$((FAIL + 1))
fi

# ─────────────────────────────────────────────
# [17] .abtest questions.json 新模型关键词检查
# ─────────────────────────────────────────────
section "[17] .abtest questions.json alignment"
if [ -f ".abtest/with_skill/questions.json" ]; then
  python3 - <<'EOF'
import json, sys

keywords = ["/opsx:explore", "/opsx:propose", "/opsx:ff", "/opsx:verify", "/opsx:sync", "openspec/changes/", "Mermaid", "ASCII", "待确认", "验收", "方案", "计划", "规范"]
fail = False

for path in [".abtest/with_skill/questions.json", ".abtest/without_skill/questions.json"]:
    with open(path) as f:
        content = f.read()
    stale = []
    for pat in ["输出中文 OpenSpec 草案", "spec/review", "三图", "architecture.mermaid"]:
        if pat in content:
            stale.append(pat)
    if stale:
        print(f"  FAIL: [{path}] 含旧模型残留: {stale}")
        fail = True
    else:
        print(f"  PASS: [{path}] 无旧模型残留")

# with_skill questions 应含新模型关键词
with open(".abtest/with_skill/questions.json") as f:
    wc = f.read()
hits = [kw for kw in keywords if kw in wc]
if len(hits) >= 7:
    print(f"  PASS: with_skill/questions.json 含新模型关键词 {hits}")
else:
    print("  FAIL: with_skill/questions.json 缺少新模型关键词")
    fail = True

sys.exit(1 if fail else 0)
EOF
  if [ $? -ne 0 ]; then FAIL=$((FAIL + 1)); else PASS=$((PASS + 1)); fi
else
  echo "  SKIP: .abtest/ 不存在（本地可选目录）"
fi

# ─────────────────────────────────────────────
# 汇总
# ─────────────────────────────────────────────
echo
echo "════════════════════════════════════════"
TOTAL=$((PASS + FAIL))
echo "QA 结果: ${PASS} PASS / ${FAIL} FAIL（共 ${TOTAL} 项）"
echo "════════════════════════════════════════"

if [ $FAIL -gt 0 ]; then
  echo "FAIL: 存在 ${FAIL} 项未通过，请修复后重新运行。"
  exit 1
else
  echo "PASS: 全部通过。"
  exit 0
fi
