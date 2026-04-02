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

fail = False
for fname in normative:
    with open(fname) as f:
        lines = f.readlines()
    for i, line in enumerate(lines, 1):
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
    "/opsx:apply", "/opsx:archive",
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
# [7] description frontmatter 三段结构完整性
# ─────────────────────────────────────────────
section "[7] Description frontmatter completeness"
python3 - <<'EOF'
import sys

with open("SKILL.md") as f:
    content = f.read()

checks = {
    "正向触发词（先分析/先写 spec）": "先分析" in content and "先写 spec" in content,
    "正向触发词（新功能/规则变更）":   "新功能" in content and "规则变更" in content,
    "职责说明（桥接/映射）":           "桥接" in content and "映射" in content,
    "阻止过早实现门禁":                "阻止" in content and "实现" in content,
    "排除条件（bug 修复）":            "bug" in content.lower() and "不适用" in content,
    "排除条件（纯文案/样式）":         "文案" in content and "样式" in content,
    "停止条件节存在":                  "## 停止条件" in content,
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
# [8] .abtest questions.json 新模型关键词检查
# ─────────────────────────────────────────────
section "[8] .abtest questions.json alignment"
if [ -f ".abtest/with_skill/questions.json" ]; then
  python3 - <<'EOF'
import json, sys

keywords = ["/opsx:explore", "/opsx:propose", "/opsx:ff", "openspec/changes/"]
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
if hits:
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
