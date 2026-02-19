#!/usr/bin/env python3
"""
Eval Runner - agent-evaluation
Runs statistical evaluations of LLM prompts with multiple iterations.

Usage:
    python eval_runner.py eval_suite.yaml
    python eval_runner.py eval_suite.yaml --runs 10
"""

import argparse
import json
import logging
import re
import sys
import time
from pathlib import Path
from typing import Any

import requests
import yaml
import os

# Add shared and current dir to path
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT_DIR))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from shared.resilience import setup_logging, retry_with_backoff, safe_ollama_call
    logger = setup_logging("agent-eval")
except ImportError:
    logger = logging.getLogger(__name__)
    def retry_with_backoff(*args, **kwargs): return lambda f: f
    def safe_ollama_call(url, prompt, model, timeout=60):
        res = requests.post(url, json={"model": model, "prompt": prompt, "stream": False}, timeout=timeout)
        return res.json() if res.status_code == 200 else {"error": "http error"}

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
DEFAULT_MODEL = "llama3.1:8b"
DEFAULT_RUNS = 5


@retry_with_backoff(max_retries=3)
def call_ollama(prompt: str, model: str = DEFAULT_MODEL) -> tuple[str, float]:
    """
    Call local Ollama and return (response, latency_ms).
    """
    start = time.time()
    result = safe_ollama_call(OLLAMA_URL, prompt, model)
    latency = (time.time() - start) * 1000

    if "error" in result:
        return f"ERROR: {result['error']}", latency

    return result.get("response", "").strip(), latency


def check_invariant(response: str, invariant: dict) -> tuple[bool, str]:
    """
    Check if a response satisfies a single invariant.
    Returns (passed, reason).
    """
    if "contains" in invariant:
        target = invariant["contains"].lower()
        if target in response.lower():
            return True, f"Contains '{target}'"
        return False, f"Missing '{target}'"

    if "not_contains" in invariant:
        target = invariant["not_contains"].lower()
        if target not in response.lower():
            return True, f"Does not contain '{target}'"
        return False, f"Unexpectedly contains '{target}'"

    if "max_length" in invariant:
        limit = int(invariant["max_length"])
        if len(response) <= limit:
            return True, f"Length {len(response)} <= {limit}"
        return False, f"Length {len(response)} > {limit}"

    if "min_length" in invariant:
        limit = int(invariant["min_length"])
        if len(response) >= limit:
            return True, f"Length {len(response)} >= {limit}"
        return False, f"Length {len(response)} < {limit}"

    if "matches_regex" in invariant:
        pattern = invariant["matches_regex"]
        if re.search(pattern, response, re.IGNORECASE):
            return True, f"Matches regex '{pattern}'"
        return False, f"Does not match regex '{pattern}'"

    if "is_json" in invariant:
        try:
            json.loads(response)
            return True, "Valid JSON"
        except (json.JSONDecodeError, TypeError):
            return False, "Invalid JSON"

    return True, "Unknown invariant (skipped)"


def check_all_invariants(response: str, invariants: list[dict]) -> dict:
    """Check all invariants and return results."""
    results = []
    all_passed = True

    for inv in invariants:
        passed, reason = check_invariant(response, inv)
        results.append({"invariant": inv, "passed": passed, "reason": reason})
        if not passed:
            all_passed = False

    return {"passed": all_passed, "checks": results}


def run_test(test: dict, model: str, runs: int) -> dict:
    """Run a single test case N times and aggregate results."""
    name = test.get("name", "unnamed")
    prompt = test["prompt"]
    invariants = test.get("invariants", [])

    run_results = []
    latencies = []
    passes = 0

    for i in range(runs):
        response, latency_ms = call_ollama(prompt, model)
        latencies.append(latency_ms)

        inv_result = check_all_invariants(response, invariants)
        if inv_result["passed"]:
            passes += 1

        run_results.append({
            "run": i + 1,
            "passed": inv_result["passed"],
            "latency_ms": round(latency_ms, 1),
            "response_length": len(response),
            "checks": inv_result["checks"],
        })

    # Calculate statistics
    latencies_sorted = sorted(latencies)
    p95_idx = max(0, int(len(latencies_sorted) * 0.95) - 1)

    return {
        "name": name,
        "runs": runs,
        "pass_rate": round(passes / runs, 3),
        "passes": passes,
        "failures": runs - passes,
        "latency_avg_ms": round(sum(latencies) / len(latencies), 1),
        "latency_p95_ms": round(latencies_sorted[p95_idx], 1),
        "latency_min_ms": round(min(latencies), 1),
        "latency_max_ms": round(max(latencies), 1),
        "details": run_results,
    }


def load_eval_suite(path: str) -> dict:
    """Load eval suite from YAML file."""
    with open(path, "r", encoding="utf-8") as f:
        suite = yaml.safe_load(f)

    if not suite or "tests" not in suite:
        raise ValueError(f"Invalid eval suite: missing 'tests' key in {path}")

    return suite


def run_eval_suite(
    suite_path: str,
    runs_override: int = None,
) -> dict:
    """
    Run a complete eval suite.

    Args:
        suite_path: Path to YAML eval suite.
        runs_override: Override number of runs per test.

    Returns:
        Complete evaluation results.
    """
    suite = load_eval_suite(suite_path)
    suite_name = suite.get("name", Path(suite_path).stem)
    model = suite.get("model", DEFAULT_MODEL)
    runs = runs_override or suite.get("runs", DEFAULT_RUNS)

    results = {
        "suite": suite_name,
        "model": model,
        "runs_per_test": runs,
        "total_tests": len(suite["tests"]),
        "tests": [],
    }

    total_passes = 0
    all_latencies = []

    for test in suite["tests"]:
        test_result = run_test(test, model, runs)
        results["tests"].append(test_result)
        total_passes += test_result["passes"]
        all_latencies.append(test_result["latency_avg_ms"])

    total_runs = results["total_tests"] * runs
    results["overall_pass_rate"] = round(total_passes / total_runs, 3) if total_runs > 0 else 0
    results["avg_latency_ms"] = round(sum(all_latencies) / len(all_latencies), 1) if all_latencies else 0

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Run LLM evaluation suite"
    )
    parser.add_argument("suite", help="Path to YAML eval suite")
    parser.add_argument("--runs", type=int, default=None,
                        help="Override runs per test")
    parser.add_argument("--output", "-o", default=None,
                        help="Save results to JSON file")
    args = parser.parse_args()

    results = run_eval_suite(args.suite, runs_override=args.runs)

    output = json.dumps(results, indent=2, ensure_ascii=False)
    print(output)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"\n✅ Results saved to {args.output}", file=sys.stderr)

    # Exit code: 0 if >80% pass rate, 1 otherwise
    return 0 if results["overall_pass_rate"] >= 0.8 else 1


if __name__ == "__main__":
    sys.exit(main())
