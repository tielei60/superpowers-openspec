#!/usr/bin/env python3
"""Local A/B regression helpers for superpowers-openspec.

This script keeps the tracked benchmark definition under evals/ authoritative,
and treats .abtest/ as a local workspace for prompt bundles and generated
outputs.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EVALS_PATH = ROOT / "evals" / "evals.json"
DEFAULT_ABTEST_CASES_PATH = ROOT / "evals" / "abtest_cases.json"
DEFAULT_ABTEST_DIR = ROOT / ".abtest"


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def dump_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def ok(message: str) -> None:
    print(f"PASS: {message}")


def fail(message: str) -> None:
    print(f"FAIL: {message}")


def write_report(report_path: str | None, payload: dict[str, Any]) -> None:
    if not report_path:
        return
    dump_json(Path(report_path), payload)
    ok(f"已写入报告: {report_path}")


def compile_pattern(pattern: str) -> re.Pattern[str]:
    return re.compile(pattern, re.IGNORECASE | re.MULTILINE | re.DOTALL)


def resolve_evals_path(args: argparse.Namespace) -> Path:
    return Path(getattr(args, "evals_path", DEFAULT_EVALS_PATH))


def resolve_cases_path(args: argparse.Namespace) -> Path:
    return Path(getattr(args, "cases_path", DEFAULT_ABTEST_CASES_PATH))


def resolve_abtest_dir(args: argparse.Namespace) -> Path:
    return Path(getattr(args, "abtest_dir", DEFAULT_ABTEST_DIR))


def resolve_with_skill_path(args: argparse.Namespace) -> Path:
    return resolve_abtest_dir(args) / "with_skill" / "questions.json"


def resolve_without_skill_path(args: argparse.Namespace) -> Path:
    return resolve_abtest_dir(args) / "without_skill" / "questions.json"


def resolve_generated_dir(args: argparse.Namespace) -> Path:
    return resolve_abtest_dir(args) / "generated"


def load_eval_index(evals_path: Path) -> dict[int, dict[str, Any]]:
    evals = load_json(evals_path)["evals"]
    index: dict[int, dict[str, Any]] = {}
    for item in evals:
        index[item["id"]] = item
    return index


def load_abtest_cases(cases_path: Path) -> list[dict[str, Any]]:
    payload = load_json(cases_path)
    return payload["cases"]


def render_local_prompt_bundles(cases: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    with_skill_prompts = []
    without_skill_prompts = []

    for case in cases:
        with_skill_prompts.append(
            {
                "id": case["id"],
                "tags": case["tags"],
                "prompt": case["prompt"],
                "expected": case["with_skill"]["expected"],
                "not_expected": case["with_skill"]["not_expected"],
            }
        )
        without_skill_prompts.append(
            {
                "id": case["id"],
                "tags": case["tags"],
                "prompt": case["prompt"],
                "expected": case["without_skill"]["expected"],
            }
        )

    return (
        {
            "mode": "with_skill",
            "skill_path": "SKILL.md",
            "prompts": with_skill_prompts,
        },
        {
            "mode": "without_skill",
            "prompts": without_skill_prompts,
        },
    )


def command_check(args: argparse.Namespace) -> int:
    failures = 0
    evals_path = resolve_evals_path(args)
    cases_path = resolve_cases_path(args)
    with_skill_path = resolve_with_skill_path(args)
    without_skill_path = resolve_without_skill_path(args)
    eval_index = load_eval_index(evals_path)
    cases = load_abtest_cases(cases_path)
    seen_case_ids: set[str] = set()
    seen_eval_ids: set[int] = set()
    results: list[dict[str, Any]] = []

    for case in cases:
        case_id = case["id"]
        eval_id = case["eval_id"]

        if case_id in seen_case_ids:
            message = f"重复 case id: {case_id}"
            fail(message)
            results.append({"status": "failed", "scope": "case_id", "case_id": case_id, "errors": [message]})
            failures += 1
        else:
            seen_case_ids.add(case_id)

        if eval_id in seen_eval_ids:
            message = f"重复 eval_id: {eval_id}"
            fail(message)
            results.append({"status": "failed", "scope": "eval_id", "eval_id": eval_id, "errors": [message]})
            failures += 1
        else:
            seen_eval_ids.add(eval_id)

        if eval_id not in eval_index:
            message = f"{case_id} 引用了不存在的 eval #{eval_id}"
            fail(message)
            results.append(
                {
                    "status": "failed",
                    "scope": "case",
                    "case_id": case_id,
                    "eval_id": eval_id,
                    "errors": [message],
                }
            )
            failures += 1
            continue

        case_errors: list[str] = []
        eval_item = eval_index[eval_id]
        if case["prompt"] != eval_item["prompt"]:
            message = f"{case_id} 的 prompt 与 eval #{eval_id} 不一致"
            fail(message)
            case_errors.append(message)
            failures += 1
        else:
            ok(f"{case_id} 对齐 eval #{eval_id}")

        for mode in ("with_skill", "without_skill"):
            payload = case[mode]
            if "expected" not in payload or not payload["expected"]:
                message = f"{case_id}/{mode} 缺少 expected"
                fail(message)
                case_errors.append(message)
                failures += 1
            must_include = payload.get("must_include", [])
            must_exclude = payload.get("must_exclude", [])
            list_fields = {
                "must_include": must_include,
                "must_exclude": must_exclude,
                "required_commands": payload.get("required_commands", []),
                "forbidden_commands": payload.get("forbidden_commands", []),
                "required_artifacts": payload.get("required_artifacts", []),
                "forbidden_artifacts": payload.get("forbidden_artifacts", []),
                "required_mentions": payload.get("required_mentions", []),
                "forbidden_mentions": payload.get("forbidden_mentions", []),
            }
            for field_name, field_value in list_fields.items():
                if not isinstance(field_value, list):
                    message = f"{case_id}/{mode} 的 {field_name} 必须是数组"
                    fail(message)
                    case_errors.append(message)
                    failures += 1

        results.append(
            {
                "status": "failed" if case_errors else "passed",
                "scope": "case",
                "case_id": case_id,
                "eval_id": eval_id,
                "errors": case_errors,
            }
        )

    missing_eval_ids = sorted(set(eval_index) - seen_eval_ids)
    if missing_eval_ids:
        message = f"A/B case 未覆盖全部 eval，缺少: {missing_eval_ids}"
        fail(message)
        results.append(
            {
                "status": "failed",
                "scope": "coverage",
                "errors": [message],
                "missing_eval_ids": missing_eval_ids,
            }
        )
        failures += 1
    else:
        ok("A/B case 已覆盖全部 eval")
        results.append({"status": "passed", "scope": "coverage", "errors": []})

    expected_with_skill, expected_without_skill = render_local_prompt_bundles(cases)
    if with_skill_path.exists():
        local_with_skill = load_json(with_skill_path)
        if local_with_skill != expected_with_skill:
            message = f"{with_skill_path} 与跟踪配置不一致，请运行 sync"
            fail(message)
            results.append(
                {
                    "status": "failed",
                    "scope": "local_bundle",
                    "mode": "with_skill",
                    "errors": [message],
                }
            )
            failures += 1
        else:
            ok(f"{with_skill_path} 已与跟踪配置同步")
            results.append(
                {
                    "status": "passed",
                    "scope": "local_bundle",
                    "mode": "with_skill",
                    "errors": [],
                }
            )

    if without_skill_path.exists():
        local_without_skill = load_json(without_skill_path)
        if local_without_skill != expected_without_skill:
            message = f"{without_skill_path} 与跟踪配置不一致，请运行 sync"
            fail(message)
            results.append(
                {
                    "status": "failed",
                    "scope": "local_bundle",
                    "mode": "without_skill",
                    "errors": [message],
                }
            )
            failures += 1
        else:
            ok(f"{without_skill_path} 已与跟踪配置同步")
            results.append(
                {
                    "status": "passed",
                    "scope": "local_bundle",
                    "mode": "without_skill",
                    "errors": [],
                }
            )

    write_report(
        args.report,
        {
            "command": "check",
            "summary": {
                "cases": len(cases),
                "failures": failures,
                "covered_eval_ids": sorted(seen_eval_ids),
                "evals_path": str(evals_path),
                "cases_path": str(cases_path),
                "abtest_dir": str(resolve_abtest_dir(args)),
            },
            "results": results,
        },
    )

    return 1 if failures else 0


def command_sync(args: argparse.Namespace) -> int:
    cases_path = resolve_cases_path(args)
    abtest_dir = resolve_abtest_dir(args)
    with_skill_path = resolve_with_skill_path(args)
    without_skill_path = resolve_without_skill_path(args)
    cases = load_abtest_cases(cases_path)
    with_skill, without_skill = render_local_prompt_bundles(cases)
    dump_json(with_skill_path, with_skill)
    dump_json(without_skill_path, without_skill)
    ok(f"已同步 {with_skill_path}")
    ok(f"已同步 {without_skill_path}")
    write_report(
        args.report,
        {
            "command": "sync",
            "summary": {
                "cases": len(cases),
                "bundles_written": 2,
                "abtest_dir": str(abtest_dir),
                "cases_path": str(cases_path),
            },
            "results": [
                {"status": "passed", "scope": "bundle", "mode": "with_skill", "path": str(with_skill_path)},
                {"status": "passed", "scope": "bundle", "mode": "without_skill", "path": str(without_skill_path)},
            ],
        },
    )
    return 0


def score_mode(case: dict[str, Any], mode: str, content: str) -> list[str]:
    errors: list[str] = []
    rules = case[mode]
    for token in rules.get("required_commands", []):
        if token not in content:
            errors.append(f"缺少必须命中的命令: {token}")
    for token in rules.get("forbidden_commands", []):
        if token in content:
            errors.append(f"命中了禁止命令: {token}")
    for token in rules.get("required_artifacts", []):
        if token not in content:
            errors.append(f"缺少必须命中的产物: {token}")
    for token in rules.get("forbidden_artifacts", []):
        if token in content:
            errors.append(f"命中了禁止产物: {token}")
    for pattern in rules.get("required_mentions", []):
        if not compile_pattern(pattern).search(content):
            errors.append(f"缺少必须命中的说明: {pattern}")
    for pattern in rules.get("forbidden_mentions", []):
        if compile_pattern(pattern).search(content):
            errors.append(f"命中了禁止说明: {pattern}")
    for pattern in rules.get("must_include", []):
        if not compile_pattern(pattern).search(content):
            errors.append(f"缺少必须命中模式: {pattern}")
    for pattern in rules.get("must_exclude", []):
        if compile_pattern(pattern).search(content):
            errors.append(f"命中了禁止模式: {pattern}")
    return errors


def command_score(args: argparse.Namespace) -> int:
    requested_modes = [args.mode] if args.mode != "both" else ["with_skill", "without_skill"]
    selected_case_ids = set(args.only.split(",")) if args.only else None
    cases_path = resolve_cases_path(args)
    generated_dir = resolve_generated_dir(args)
    cases = load_abtest_cases(cases_path)

    failures = 0
    scored = 0
    missing = 0
    results: list[dict[str, Any]] = []

    for case in cases:
        if selected_case_ids and case["id"] not in selected_case_ids:
            continue

        for mode in requested_modes:
            output_path = generated_dir / mode / f"{case['id']}.md"
            if not output_path.exists():
                missing += 1
                message = f"{mode}/{case['id']} 缺少输出文件: {output_path}"
                result = {
                    "case_id": case["id"],
                    "eval_id": case["eval_id"],
                    "mode": mode,
                    "output_path": str(output_path),
                    "status": "missing",
                    "errors": [message],
                }
                results.append(result)
                if args.require_complete:
                    fail(message)
                    failures += 1
                else:
                    print(f"SKIP: {message}")
                continue

            content = output_path.read_text(encoding="utf-8")
            errors = score_mode(case, mode, content)
            scored += 1
            if errors:
                results.append(
                    {
                        "case_id": case["id"],
                        "eval_id": case["eval_id"],
                        "mode": mode,
                        "output_path": str(output_path),
                        "status": "failed",
                        "errors": errors,
                    }
                )
                fail(f"{mode}/{case['id']} -> {'; '.join(errors)}")
                failures += 1
            else:
                results.append(
                    {
                        "case_id": case["id"],
                        "eval_id": case["eval_id"],
                        "mode": mode,
                        "output_path": str(output_path),
                        "status": "passed",
                        "errors": [],
                    }
                )
                ok(f"{mode}/{case['id']}")

    summary = {
        "scored": scored,
        "failures": failures,
        "missing": missing,
        "mode": args.mode,
        "selected_case_ids": sorted(selected_case_ids) if selected_case_ids else "all",
        "require_complete": args.require_complete,
        "cases_path": str(cases_path),
        "generated_dir": str(generated_dir),
    }
    print(f"SUMMARY: scored={scored} failures={failures} missing={missing} mode={args.mode}")
    write_report(
        args.report,
        {
            "command": "score",
            "summary": summary,
            "results": results,
        },
    )
    return 1 if failures else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Local A/B regression helpers")
    subparsers = parser.add_subparsers(dest="command", required=True)

    check_parser = subparsers.add_parser("check", help="Validate tracked A/B config")
    check_parser.add_argument(
        "--evals-path",
        default=str(DEFAULT_EVALS_PATH),
        help="Path to evals.json",
    )
    check_parser.add_argument(
        "--cases-path",
        default=str(DEFAULT_ABTEST_CASES_PATH),
        help="Path to abtest_cases.json",
    )
    check_parser.add_argument(
        "--abtest-dir",
        default=str(DEFAULT_ABTEST_DIR),
        help="Directory containing local with_skill/ and without_skill/ prompt bundles",
    )
    check_parser.add_argument(
        "--report",
        help="Write a JSON report to the given path",
    )
    check_parser.set_defaults(func=command_check)

    sync_parser = subparsers.add_parser("sync", help="Sync local .abtest prompt bundles")
    sync_parser.add_argument(
        "--cases-path",
        default=str(DEFAULT_ABTEST_CASES_PATH),
        help="Path to abtest_cases.json",
    )
    sync_parser.add_argument(
        "--abtest-dir",
        default=str(DEFAULT_ABTEST_DIR),
        help="Target directory for generated with_skill/ and without_skill/ prompt bundles",
    )
    sync_parser.add_argument(
        "--report",
        help="Write a JSON report to the given path",
    )
    sync_parser.set_defaults(func=command_sync)

    score_parser = subparsers.add_parser("score", help="Score local generated outputs")
    score_parser.add_argument(
        "--evals-path",
        default=str(DEFAULT_EVALS_PATH),
        help="Path to evals.json",
    )
    score_parser.add_argument(
        "--cases-path",
        default=str(DEFAULT_ABTEST_CASES_PATH),
        help="Path to abtest_cases.json",
    )
    score_parser.add_argument(
        "--abtest-dir",
        default=str(DEFAULT_ABTEST_DIR),
        help="Directory containing generated/ benchmark outputs",
    )
    score_parser.add_argument(
        "--mode",
        choices=("with_skill", "without_skill", "both"),
        default="with_skill",
        help="Which output mode to score",
    )
    score_parser.add_argument(
        "--only",
        help="Comma-separated case ids to score, e.g. q1,q2,q17",
    )
    score_parser.add_argument(
        "--require-complete",
        action="store_true",
        help="Fail when any selected output file is missing",
    )
    score_parser.add_argument(
        "--report",
        help="Write a JSON report to the given path",
    )
    score_parser.set_defaults(func=command_score)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
