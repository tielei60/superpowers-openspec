import json
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
            self.assertEqual(payload["summary"]["cases"], 32)
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
            self.assertEqual(payload["summary"]["cases"], 32)

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


if __name__ == "__main__":
    unittest.main()
