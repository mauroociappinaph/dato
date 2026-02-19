"""
Tests for agent-evaluation skill.
Tests YAML parsing, invariant checking, stats, and report generation without Ollama.
"""

import json
import sys
import tempfile
from pathlib import Path

import pytest

# Add scripts to path
SCRIPTS_DIR = Path(__file__).parent.parent.parent.parent / "agent-evaluation" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))


class TestInvariantChecker:
    """Test individual invariant checks."""

    def test_contains_pass(self):
        from eval_runner import check_invariant

        passed, reason = check_invariant("The score is 85", {"contains": "score"})
        assert passed is True

    def test_contains_fail(self):
        from eval_runner import check_invariant

        passed, reason = check_invariant("No result here", {"contains": "score"})
        assert passed is False

    def test_contains_case_insensitive(self):
        from eval_runner import check_invariant

        passed, _ = check_invariant("The SCORE is 85", {"contains": "score"})
        assert passed is True

    def test_not_contains_pass(self):
        from eval_runner import check_invariant

        passed, _ = check_invariant("Good result", {"not_contains": "error"})
        assert passed is True

    def test_not_contains_fail(self):
        from eval_runner import check_invariant

        passed, _ = check_invariant("This has error in it", {"not_contains": "error"})
        assert passed is False

    def test_max_length_pass(self):
        from eval_runner import check_invariant

        passed, _ = check_invariant("short", {"max_length": 100})
        assert passed is True

    def test_max_length_fail(self):
        from eval_runner import check_invariant

        passed, _ = check_invariant("x" * 200, {"max_length": 100})
        assert passed is False

    def test_min_length_pass(self):
        from eval_runner import check_invariant

        passed, _ = check_invariant("enough text here", {"min_length": 5})
        assert passed is True

    def test_min_length_fail(self):
        from eval_runner import check_invariant

        passed, _ = check_invariant("hi", {"min_length": 10})
        assert passed is False

    def test_matches_regex_pass(self):
        from eval_runner import check_invariant

        passed, _ = check_invariant("Score: 85", {"matches_regex": r"\d+"})
        assert passed is True

    def test_matches_regex_fail(self):
        from eval_runner import check_invariant

        passed, _ = check_invariant("No numbers", {"matches_regex": r"\d+"})
        assert passed is False

    def test_is_json_pass(self):
        from eval_runner import check_invariant

        passed, _ = check_invariant('{"score": 85}', {"is_json": True})
        assert passed is True

    def test_is_json_fail(self):
        from eval_runner import check_invariant

        passed, _ = check_invariant("not json at all", {"is_json": True})
        assert passed is False


class TestInvariantBatch:
    """Test checking multiple invariants at once."""

    def test_all_pass(self):
        from eval_runner import check_all_invariants

        result = check_all_invariants(
            '{"score": 85, "reasoning": "good"}',
            [
                {"contains": "score"},
                {"max_length": 500},
                {"is_json": True},
            ]
        )
        assert result["passed"] is True
        assert len(result["checks"]) == 3

    def test_one_fails(self):
        from eval_runner import check_all_invariants

        result = check_all_invariants(
            "no json here",
            [
                {"contains": "no"},
                {"is_json": True},
            ]
        )
        assert result["passed"] is False


class TestYAMLParsing:
    """Test eval suite YAML loading."""

    def test_load_valid_suite(self):
        from eval_runner import load_eval_suite

        with tempfile.NamedTemporaryFile(suffix=".yaml", mode="w", delete=False) as f:
            f.write("""
name: "test-suite"
model: "llama3.1:8b"
runs: 3
tests:
  - name: "basic_test"
    prompt: "Hello"
    invariants:
      - contains: "hello"
""")
            f.flush()

            suite = load_eval_suite(f.name)
            assert suite["name"] == "test-suite"
            assert len(suite["tests"]) == 1
            assert suite["tests"][0]["name"] == "basic_test"

            Path(f.name).unlink()

    def test_load_invalid_suite(self):
        from eval_runner import load_eval_suite

        with tempfile.NamedTemporaryFile(suffix=".yaml", mode="w", delete=False) as f:
            f.write("invalid: true\n")
            f.flush()

            with pytest.raises(ValueError):
                load_eval_suite(f.name)

            Path(f.name).unlink()


class TestReportGeneration:
    """Test Markdown report output."""

    def test_generate_report_basic(self):
        from report import generate_report

        results = {
            "suite": "test",
            "model": "test-model",
            "runs_per_test": 3,
            "total_tests": 1,
            "overall_pass_rate": 1.0,
            "avg_latency_ms": 100.0,
            "tests": [{
                "name": "basic",
                "pass_rate": 1.0,
                "passes": 3,
                "runs": 3,
                "latency_avg_ms": 100.0,
                "latency_p95_ms": 120.0,
                "details": [
                    {"run": 1, "passed": True, "latency_ms": 95.0,
                     "response_length": 50, "checks": []},
                    {"run": 2, "passed": True, "latency_ms": 100.0,
                     "response_length": 48, "checks": []},
                    {"run": 3, "passed": True, "latency_ms": 105.0,
                     "response_length": 52, "checks": []},
                ],
            }],
        }

        report = generate_report(results)
        assert "test" in report
        assert "100.0%" in report
        assert "✅" in report

    def test_report_shows_failures(self):
        from report import generate_report

        results = {
            "suite": "failing",
            "model": "test",
            "runs_per_test": 2,
            "total_tests": 1,
            "overall_pass_rate": 0.0,
            "avg_latency_ms": 50.0,
            "tests": [{
                "name": "bad_test",
                "pass_rate": 0.0,
                "passes": 0,
                "runs": 2,
                "latency_avg_ms": 50.0,
                "latency_p95_ms": 55.0,
                "details": [
                    {"run": 1, "passed": False, "latency_ms": 50.0,
                     "response_length": 10,
                     "checks": [{"invariant": {}, "passed": False,
                                 "reason": "Missing 'score'"}]},
                    {"run": 2, "passed": False, "latency_ms": 50.0,
                     "response_length": 10,
                     "checks": [{"invariant": {}, "passed": False,
                                 "reason": "Missing 'score'"}]},
                ],
            }],
        }

        report = generate_report(results)
        assert "❌" in report
        assert "Failure Details" in report
