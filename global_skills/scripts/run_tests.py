#!/usr/bin/env python3
"""
Test Runner CLI - Script maestro para ejecutar todos los tests de Global Skills.

Uso:
    python scripts/run_tests.py --all
    python scripts/run_tests.py --unit
    python scripts/run_tests.py --integration
    python scripts/run_tests.py --skill security-auditor
    python scripts/run_tests.py --coverage
    python scripts/run_tests.py --list
"""

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Colors for terminal output
COLORS = {
    "green": "\033[92m",
    "red": "\033[91m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "cyan": "\033[96m",
    "reset": "\033[0m",
    "bold": "\033[1m",
}


def color(text: str, color_name: str) -> str:
    """Add color to text."""
    return f"{COLORS.get(color_name, '')}{text}{COLORS['reset']}"


class TestRunner:
    """Master test runner for Global Skills."""

    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or Path(__file__).parent.parent
        self.tests_dir = self.project_root / "tests"
        self.results: List[Dict] = []
        self.start_time: Optional[float] = None

    def run_command(
        self,
        cmd: List[str],
        description: str,
        capture_output: bool = True
    ) -> Tuple[int, str, str]:
        """Run a command and return exit code, stdout, stderr."""
        print(color(f"\n{'='*60}", "cyan"))
        print(color(f"Running: {description}", "bold"))
        print(color(f"Command: {' '.join(cmd)}", "blue"))
        print(color(f"{'='*60}\n", "cyan"))

        start = time.time()

        try:
            result = subprocess.run(
                cmd,
                capture_output=capture_output,
                text=True,
                cwd=self.project_root,
            )
            elapsed = time.time() - start

            # Print output
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(color(result.stderr, "yellow"))

            status = "✓ PASSED" if result.returncode == 0 else "✗ FAILED"
            status_color = "green" if result.returncode == 0 else "red"
            print(color(f"\n{status} in {elapsed:.2f}s", status_color))

            return result.returncode, result.stdout, result.stderr

        except Exception as e:
            elapsed = time.time() - start
            print(color(f"\n✗ ERROR: {e}", "red"))
            return 1, "", str(e)

    def run_pytest(
        self,
        test_path: Optional[str] = None,
        markers: Optional[List[str]] = None,
        coverage: bool = False,
        verbose: bool = True,
    ) -> int:
        """Run pytest with given options."""
        cmd = ["python3", "-m", "pytest"]

        if test_path:
            cmd.append(test_path)
        else:
            cmd.append("tests/")

        if verbose:
            cmd.append("-v")

        if markers:
            for marker in markers:
                cmd.extend(["-m", marker])

        if coverage:
            cmd.extend([
                "--cov=global_skills",
                "--cov=src",
                "--cov-report=term-missing",
                "--cov-report=html:htmlcov",
                "--cov-report=xml:coverage.xml",
            ])

        # Add common options
        cmd.extend([
            "--tb=short",
            "--strict-markers",
            "--color=yes",
        ])

        exit_code, stdout, stderr = self.run_command(
            cmd,
            f"pytest {test_path or 'all tests'}"
        )

        self.results.append({
            "test": test_path or "pytest",
            "exit_code": exit_code,
            "stdout": stdout,
            "stderr": stderr,
        })

        return exit_code

    def run_unit_tests(self, coverage: bool = False) -> int:
        """Run unit tests."""
        return self.run_pytest(
            test_path="tests/unit",
            markers=["unit"],
            coverage=coverage
        )

    def run_integration_tests(self, coverage: bool = False) -> int:
        """Run integration tests."""
        return self.run_pytest(
            test_path="tests/integration",
            markers=["integration"],
            coverage=coverage
        )

    def run_e2e_tests(self, coverage: bool = False) -> int:
        """Run end-to-end tests."""
        return self.run_pytest(
            test_path="tests/e2e",
            markers=["e2e"],
            coverage=coverage
        )

    def run_skill_tests(self, skill_name: Optional[str] = None, coverage: bool = False) -> int:
        """Run skill-specific tests."""
        if skill_name:
            # Test specific skill
            test_file = f"tests/unit/skills/test_{skill_name}.py"
            if not (self.project_root / test_file).exists():
                print(color(f"⚠ No tests found for skill: {skill_name}", "yellow"))
                return 0
            return self.run_pytest(test_path=test_file, coverage=coverage)
        else:
            # Test all skills
            return self.run_pytest(
                test_path="tests/unit/skills",
                markers=["skill"],
                coverage=coverage
            )

    def run_architecture_tests(self) -> int:
        """Run existing architecture tests."""
        tests = [
            ("basic_test.py", "Basic Functionality Test"),
            ("test_architecture.py", "Architecture Test"),
            ("final_architecture_test.py", "Final Architecture Test"),
        ]

        all_passed = True
        for test_file, description in tests:
            test_path = self.project_root / test_file
            if test_path.exists():
                exit_code, _, _ = self.run_command(
                    ["python", str(test_file)],
                    description
                )
                if exit_code != 0:
                    all_passed = False
            else:
                print(color(f"⚠ Test file not found: {test_file}", "yellow"))

        return 0 if all_passed else 1

    def run_integration_test_suite(self) -> int:
        """Run the integration test suite."""
        exit_code, _, _ = self.run_command(
            ["python", "-m", "global_skills.integration_tests"],
            "Integration Test Suite"
        )
        return exit_code

    def validate_skills(self) -> int:
        """Validate all skills in the registry."""
        print(color("\n" + "="*60, "cyan"))
        print(color("Validating All Skills", "bold"))
        print(color("="*60 + "\n", "cyan"))

        try:
            import sys
            sys.path.insert(0, str(self.project_root))
            from tests.test_runner import SkillValidator
            validator = SkillValidator(self.project_root)
            report = validator.validate_all_skills()

            print(color(f"\n{'='*60}", "cyan"))
            print(color("VALIDATION SUMMARY", "bold"))
            print(color(f"{'='*60}\n", "cyan"))
            print(f"Total Skills: {report['total']}")
            print(color(f"Valid: {report['valid']}", "green"))
            print(color(f"Invalid: {report['invalid']}", "red" if report['invalid'] > 0 else "green"))
            print(color(f"Errors: {report['errors']}", "red" if report['errors'] > 0 else "green"))

            if report.get('details'):
                print(color("\nDetails:", "bold"))
                for detail in report['details']:
                    status_color = "green" if detail['valid'] else "red"
                    print(color(f"  {'✓' if detail['valid'] else '✗'} {detail['skill']}", status_color))
                    if detail.get('errors'):
                        for error in detail['errors']:
                            print(color(f"    - {error}", "red"))

            return 0 if report['invalid'] == 0 and report['errors'] == 0 else 1

        except Exception as e:
            print(color(f"Error validating skills: {e}", "red"))
            return 1

    def list_tests(self) -> int:
        """List all available tests."""
        print(color("\n" + "="*60, "cyan"))
        print(color("Available Tests", "bold"))
        print(color("="*60 + "\n", "cyan"))

        # List pytest tests
        print(color("Pytest Tests:", "bold"))
        exit_code, stdout, _ = self.run_command(
            ["python", "-m", "pytest", "--collect-only", "-q"],
            "Collecting tests",
            capture_output=True
        )
        if stdout:
            lines = stdout.strip().split("\n")
            for line in lines:
                if line.strip() and not line.startswith("="):
                    print(f"  • {line.strip()}")

        # List architecture tests
        print(color("\nArchitecture Tests:", "bold"))
        arch_tests = [
            "basic_test.py",
            "test_architecture.py",
            "final_architecture_test.py",
        ]
        for test in arch_tests:
            exists = (self.project_root / test).exists()
            status = color("✓", "green") if exists else color("✗", "red")
            print(f"  {status} {test}")

        # List skills with tests
        print(color("\nSkills with Tests:", "bold"))
        skills_dir = self.tests_dir / "unit" / "skills"
        if skills_dir.exists():
            for test_file in sorted(skills_dir.glob("test_*.py")):
                skill_name = test_file.stem.replace("test_", "")
                print(f"  • {skill_name}")

        return 0

    def run_all_tests(self, coverage: bool = False) -> int:
        """Run all tests in sequence."""
        self.start_time = time.time()

        print(color("\n" + "="*70, "cyan"))
        print(color("GLOBAL SKILLS - COMPLETE TEST SUITE", "bold"))
        print(color("="*70 + "\n", "cyan"))

        results = {}

        # 1. Unit Tests
        print(color("\n[1/6] Running Unit Tests...", "bold"))
        results['unit'] = self.run_unit_tests(coverage=coverage)

        # 2. Integration Tests
        print(color("\n[2/6] Running Integration Tests...", "bold"))
        results['integration'] = self.run_integration_tests(coverage=coverage)

        # 3. E2E Tests
        print(color("\n[3/6] Running E2E Tests...", "bold"))
        results['e2e'] = self.run_e2e_tests(coverage=coverage)

        # 4. Skill Tests
        print(color("\n[4/6] Running Skill Tests...", "bold"))
        results['skills'] = self.run_skill_tests(coverage=coverage)

        # 5. Architecture Tests
        print(color("\n[5/6] Running Architecture Tests...", "bold"))
        results['architecture'] = self.run_architecture_tests()

        # 6. Skill Validation
        print(color("\n[6/6] Validating Skills...", "bold"))
        results['validation'] = self.validate_skills()

        # Summary
        elapsed = time.time() - self.start_time
        passed = sum(1 for v in results.values() if v == 0)
        total = len(results)

        print(color(f"\n{'='*70}", "cyan"))
        print(color("FINAL SUMMARY", "bold"))
        print(color(f"{'='*70}\n", "cyan"))

        for name, exit_code in results.items():
            status = color("✓ PASSED", "green") if exit_code == 0 else color("✗ FAILED", "red")
            print(f"{name.capitalize():20} {status}")

        print(f"\nTotal: {passed}/{total} test suites passed")
        print(f"Time: {elapsed:.2f}s")

        # Save report
        report = {
            "timestamp": datetime.now().isoformat(),
            "results": results,
            "summary": {
                "passed": passed,
                "total": total,
                "elapsed_seconds": elapsed,
            },
        }

        report_file = self.project_root / "test_report.json"
        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)
        print(f"\nReport saved to: {report_file}")

        return 0 if passed == total else 1


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Test Runner for Global Skills",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/run_tests.py --all                    # Run all tests
  python scripts/run_tests.py --unit                   # Run unit tests only
  python scripts/run_tests.py --integration            # Run integration tests
  python scripts/run_tests.py --skill security-auditor # Test specific skill
  python scripts/run_tests.py --coverage               # Run with coverage
  python scripts/run_tests.py --list                   # List all tests
  python scripts/run_tests.py --validate               # Validate skills
        """
    )

    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Run all tests"
    )
    parser.add_argument(
        "--unit", "-u",
        action="store_true",
        help="Run unit tests"
    )
    parser.add_argument(
        "--integration", "-i",
        action="store_true",
        help="Run integration tests"
    )
    parser.add_argument(
        "--e2e", "-e",
        action="store_true",
        help="Run end-to-end tests"
    )
    parser.add_argument(
        "--skill", "-s",
        metavar="NAME",
        help="Run tests for specific skill"
    )
    parser.add_argument(
        "--architecture",
        action="store_true",
        help="Run architecture tests"
    )
    parser.add_argument(
        "--validate", "-v",
        action="store_true",
        help="Validate all skills"
    )
    parser.add_argument(
        "--coverage", "-c",
        action="store_true",
        help="Run with coverage reporting"
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List all available tests"
    )
    parser.add_argument(
        "--pytest",
        nargs=argparse.REMAINDER,
        help="Pass remaining arguments to pytest"
    )

    args = parser.parse_args()

    # If no args provided, show help
    if len(sys.argv) == 1:
        parser.print_help()
        return 0

    runner = TestRunner()

    # Handle different commands
    if args.list:
        return runner.list_tests()

    if args.pytest:
        # Pass through to pytest
        cmd = ["python", "-m", "pytest"] + args.pytest
        exit_code, _, _ = runner.run_command(cmd, "pytest (passthrough)")
        return exit_code

    if args.all:
        return runner.run_all_tests(coverage=args.coverage)

    if args.unit:
        return runner.run_unit_tests(coverage=args.coverage)

    if args.integration:
        return runner.run_integration_tests(coverage=args.coverage)

    if args.e2e:
        return runner.run_e2e_tests(coverage=args.coverage)

    if args.skill:
        return runner.run_skill_tests(skill_name=args.skill, coverage=args.coverage)

    if args.architecture:
        return runner.run_architecture_tests()

    if args.validate:
        return runner.validate_skills()

    # Default: run all
    return runner.run_all_tests(coverage=args.coverage)


if __name__ == "__main__":
    sys.exit(main())
