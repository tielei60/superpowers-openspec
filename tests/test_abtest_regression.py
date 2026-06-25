import json
import re
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "abtest_regression.py"
FIXTURE_ABTEST_DIR = ROOT / "tests" / "fixtures" / "abtest"


def run_script(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python3", str(SCRIPT), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


class AbtestRegressionCliTests(unittest.TestCase):
    def test_check_report_writes_summary_for_tracked_config(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            report_path = Path(tmpdir) / "check-report.json"
            proc = run_script(
                "check",
                "--report",
                str(report_path),
            )

            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertTrue(report_path.exists(), proc.stdout + proc.stderr)

            payload = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["command"], "check")
            self.assertEqual(payload["summary"]["failures"], 0)
            self.assertEqual(payload["summary"]["cases"], 34)
            self.assertTrue(any(item["scope"] == "coverage" for item in payload["results"]))

    def test_check_report_detects_prompt_drift_from_custom_cases_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            evals_path = tmp / "evals.json"
            cases_path = tmp / "abtest_cases.json"
            report_path = tmp / "check-report.json"

            evals_path.write_text(
                json.dumps(
                    {
                        "evals": [
                            {
                                "id": 1,
                                "tags": ["触发类"],
                                "prompt": "原始 prompt",
                                "expected_output": "应触发规范阶段。",
                            }
                        ]
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            cases_path.write_text(
                json.dumps(
                    {
                        "version": 1,
                        "cases": [
                            {
                                "id": "q1",
                                "eval_id": 1,
                                "tags": ["触发类"],
                                "prompt": "被改坏的 prompt",
                                "with_skill": {
                                    "expected": "仍应触发",
                                    "not_expected": "不应悄悄通过。",
                                    "must_include": [],
                                    "must_exclude": [],
                                },
                                "without_skill": {"expected": "普通建议即可", "must_include": [], "must_exclude": []},
                            }
                        ],
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

            proc = run_script(
                "check",
                "--evals-path",
                str(evals_path),
                "--cases-path",
                str(cases_path),
                "--report",
                str(report_path),
            )

            self.assertNotEqual(proc.returncode, 0)
            self.assertTrue(report_path.exists(), proc.stdout + proc.stderr)

            payload = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["command"], "check")
            self.assertGreater(payload["summary"]["failures"], 0)
            self.assertTrue(
                any("不一致" in error for item in payload["results"] for error in item.get("errors", [])),
                payload,
            )

    def test_sync_report_writes_summary_and_bundles_to_custom_abtest_dir(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            abtest_dir = tmp / "abtest"
            report_path = tmp / "sync-report.json"

            proc = run_script(
                "sync",
                "--abtest-dir",
                str(abtest_dir),
                "--report",
                str(report_path),
            )

            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertTrue((abtest_dir / "with_skill" / "questions.json").exists(), proc.stdout + proc.stderr)
            self.assertTrue((abtest_dir / "without_skill" / "questions.json").exists(), proc.stdout + proc.stderr)
            self.assertTrue(report_path.exists(), proc.stdout + proc.stderr)

            payload = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["command"], "sync")
            self.assertEqual(payload["summary"]["bundles_written"], 2)
            self.assertEqual(payload["summary"]["cases"], 34)

    def test_score_report_writes_summary_for_tracked_fixture_dir(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            report_path = Path(tmpdir) / "score-report.json"
            proc = run_script(
                "score",
                "--abtest-dir",
                str(FIXTURE_ABTEST_DIR),
                "--mode",
                "both",
                "--only",
                "q1,q6",
                "--require-complete",
                "--report",
                str(report_path),
            )

            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertTrue(report_path.exists(), proc.stdout + proc.stderr)

            payload = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["command"], "score")
            self.assertEqual(payload["summary"]["failures"], 0)
            self.assertEqual(payload["summary"]["missing"], 0)
            self.assertEqual(payload["summary"]["scored"], 4)
            self.assertEqual(len(payload["results"]), 4)

    def test_score_report_captures_missing_output_failures(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            report_path = tmp / "score-report-missing.json"
            proc = run_script(
                "score",
                "--abtest-dir",
                str(tmp / "abtest"),
                "--mode",
                "with_skill",
                "--only",
                "q27",
                "--require-complete",
                "--report",
                str(report_path),
            )

            self.assertNotEqual(proc.returncode, 0)
            self.assertTrue(report_path.exists(), proc.stdout + proc.stderr)

            payload = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["command"], "score")
            self.assertEqual(payload["summary"]["failures"], 1)
            self.assertEqual(payload["summary"]["missing"], 1)
            self.assertEqual(payload["summary"]["scored"], 0)
            self.assertEqual(payload["results"][0]["status"], "missing")

    def test_score_report_enforces_structured_rule_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            evals_path = tmp / "evals.json"
            cases_path = tmp / "abtest_cases.json"
            abtest_dir = tmp / "abtest"
            report_path = tmp / "score-report.json"
            generated_path = abtest_dir / "generated" / "with_skill" / "q1.md"
            generated_path.parent.mkdir(parents=True, exist_ok=True)

            evals_path.write_text(
                json.dumps(
                    {
                        "evals": [
                            {
                                "id": 1,
                                "tags": ["命令映射类"],
                                "prompt": "直接给我规范入口。",
                                "expected_output": "应进入 propose。",
                            }
                        ]
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            cases_path.write_text(
                json.dumps(
                    {
                        "version": 1,
                        "cases": [
                            {
                                "id": "q1",
                                "eval_id": 1,
                                "tags": ["命令映射类"],
                                "prompt": "直接给我规范入口。",
                                "with_skill": {
                                    "expected": "应进入 propose。",
                                    "required_commands": ["/opsx:propose"],
                                    "required_artifacts": ["proposal.md"],
                                    "required_mentions": ["规范阶段"],
                                },
                                "without_skill": {"expected": "普通建议即可"},
                            }
                        ],
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            generated_path.write_text(
                "当前建议使用 /opsx:propose，并保持在规范阶段处理。\n",
                encoding="utf-8",
            )

            proc = run_script(
                "score",
                "--evals-path",
                str(evals_path),
                "--cases-path",
                str(cases_path),
                "--abtest-dir",
                str(abtest_dir),
                "--mode",
                "with_skill",
                "--only",
                "q1",
                "--require-complete",
                "--report",
                str(report_path),
            )

            self.assertNotEqual(proc.returncode, 0)
            self.assertTrue(report_path.exists(), proc.stdout + proc.stderr)

            payload = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["command"], "score")
            self.assertEqual(payload["summary"]["failures"], 1)
            self.assertTrue(
                any("proposal.md" in error for error in payload["results"][0]["errors"]),
                payload,
            )

    def test_q28_requires_each_readability_requirement(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            abtest_dir = tmp / "abtest"
            report_path = tmp / "score-report.json"
            generated_path = abtest_dir / "generated" / "with_skill" / "q28.md"
            generated_path.parent.mkdir(parents=True, exist_ok=True)
            generated_path.write_text(
                "文档需要更易阅读。\n",
                encoding="utf-8",
            )

            proc = run_script(
                "score",
                "--abtest-dir",
                str(abtest_dir),
                "--mode",
                "with_skill",
                "--only",
                "q28",
                "--require-complete",
                "--report",
                str(report_path),
            )

            self.assertNotEqual(proc.returncode, 0)
            self.assertTrue(report_path.exists(), proc.stdout + proc.stderr)

            payload = json.loads(report_path.read_text(encoding="utf-8"))
            errors = payload["results"][0]["errors"]
            self.assertTrue(any("术语解释" in error for error in errors), payload)
            self.assertTrue(any("先说结论" in error for error in errors), payload)
            self.assertTrue(any("表格" in error for error in errors), payload)

    def test_skill_restores_solution_document_priority_warning(self) -> None:
        content = (ROOT / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("跳过 `docs/solutions/*.md` 直接生成 OpenSpec change", content)
        self.assertIn("先写方案文档，确认后再进 OpenSpec", content)

    def test_skill_requires_business_style_expression(self) -> None:
        content = (
            (ROOT / "SKILL.md").read_text(encoding="utf-8")
            + "\n"
            + (ROOT / "references/spec-template.md").read_text(encoding="utf-8")
            + "\n"
            + (ROOT / "references/planning-workflow.md").read_text(encoding="utf-8")
        )

        required_phrases = [
            "先讲业务场景，再讲系统处理，最后讲技术支撑",
            "用户/业务人员",
            "解决什么业务问题",
            "系统怎么处理",
            "异常情况怎么处理",
            "业务价值是什么",
            "技术词可以出现，但必须放在业务解释之后",
        ]
        for phrase in required_phrases:
            self.assertIn(phrase, content)

    def test_skill_treats_ai_terms_as_examples_not_banned_words(self) -> None:
        content = (
            (ROOT / "SKILL.md").read_text(encoding="utf-8")
            + "\n"
            + (ROOT / "references/spec-template.md").read_text(encoding="utf-8")
            + "\n"
            + (ROOT / "references/planning-workflow.md").read_text(encoding="utf-8")
        )

        required_phrases = [
            "技术词不是禁用词",
            "不要逐词列禁用清单",
            "通过写法规则约束",
            "示例，不是穷举",
            "先解释业务含义和用户可见结果",
        ]
        for phrase in required_phrases:
            self.assertIn(phrase, content)

    def test_skill_description_is_chinese_trigger_only(self) -> None:
        content = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        frontmatter = content.split("---", 2)[1]
        match = re.search(r"description:\s*>\s*(.*?)\n\s*$", frontmatter, re.S)

        self.assertIsNotNone(match)
        description = " ".join(match.group(1).split())

        self.assertTrue(description.startswith("用于："), description)
        self.assertLessEqual(len(description), 500)
        self.assertNotIn("/opsx:", description)
        self.assertNotIn("docs/solutions", description)
        self.assertNotIn("确认后", description)
        self.assertNotIn("生成", description)
        self.assertIn("分析需求", description)
        self.assertIn("方案文档", description)
        self.assertIn("功能变更", description)
        self.assertIn("数据模型", description)
        self.assertIn("设计与实现混合", description)

    def test_skill_has_quick_execution_path(self) -> None:
        content = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        quick_path = content.split("## 权威来源", 1)[0]

        required_phrases = [
            "## 快速执行路径",
            "先写方案文档",
            "直接进入 OpenSpec",
            "已确认方案转 OpenSpec",
            "已完成规范进入实现",
            "当前阶段",
            "下一步只做",
        ]
        for phrase in required_phrases:
            self.assertIn(phrase, quick_path)

    def test_skill_main_file_stays_compact(self) -> None:
        content = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        sections = {
            line.strip()
            for line in content.splitlines()
            if line.startswith("## ")
        }

        self.assertLessEqual(len(content.splitlines()), 220)
        required_sections = {
            "## 快速执行路径",
            "## 触发边界",
            "## 阶段门禁",
            "## 产物质量要求",
            "## 常见错误",
            "## 停止条件",
        }
        self.assertTrue(required_sections.issubset(sections), sections)
        self.assertNotIn("## 整体流程", sections)
        self.assertNotIn("## 完整方案文档先行", sections)
        self.assertNotIn("## 方案文档优先级", sections)
        self.assertNotIn("## 确定性语言要求", sections)
        self.assertNotIn("## 行为描述写法（业务驱动）", sections)
        self.assertNotIn("## 文档可读性要求", sections)


if __name__ == "__main__":
    unittest.main()
