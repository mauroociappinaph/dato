#!/usr/bin/env python3
"""
agent-evaluation — LLMOps Eval Runner CLI
Statistical evaluation of LLM prompts with certification.

Usage:
    python main.py run eval_suite.yaml
    python main.py run eval_suite.yaml --runs 10 -o results.json
    python main.py report results.json
    python main.py report results.json -o report.md
"""

import argparse
import json
import sys
from pathlib import Path


def cmd_run(args):
    """Run an eval suite."""
    from eval_runner import run_eval_suite

    results = run_eval_suite(args.suite, runs_override=args.runs)
    output = json.dumps(results, indent=2, ensure_ascii=False)
    print(output)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"\n✅ Results saved to {args.output}", file=sys.stderr)

    return 0 if results["overall_pass_rate"] >= 0.8 else 1


def cmd_report(args):
    """Generate report from results."""
    from report import generate_report

    data = json.loads(Path(args.results).read_text(encoding="utf-8"))
    report = generate_report(data)
    print(report)

    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
        print(f"\n✅ Report saved to {args.output}", file=sys.stderr)

    return 0


def main():
    parser = argparse.ArgumentParser(
        prog="agent-evaluation",
        description="LLMOps Eval Runner — Statistical LLM Testing"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # Run subcommand
    p_run = sub.add_parser("run", help="Run an eval suite")
    p_run.add_argument("suite", help="Path to YAML eval suite")
    p_run.add_argument("--runs", type=int, default=None,
                       help="Override runs per test")
    p_run.add_argument("--output", "-o", default=None,
                       help="Save results to JSON file")

    # Report subcommand
    p_report = sub.add_parser("report", help="Generate report from results")
    p_report.add_argument("results", help="Path to JSON results")
    p_report.add_argument("--output", "-o", default=None,
                          help="Save report to file")

    args = parser.parse_args()
    commands = {"run": cmd_run, "report": cmd_report}
    return commands[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
