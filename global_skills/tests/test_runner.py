"""
Test Runner Module - Core testing utilities for Global Skills.

This module provides:
- SkillValidator: Validates skills against the registry
- Test discovery utilities
- Report generation
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set


class SkillValidator:
    """Validates skills against the registry and filesystem."""

    REQUIRED_FIELDS = ["name", "id", "version", "status", "path"]
    VALID_STATUSES = {"active", "deprecated", "draft"}

    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or Path(__file__).parent.parent
        self.registry_path = self.project_root / "skill_registry.json"
        self.errors: List[Dict[str, Any]] = []
        self.warnings: List[Dict[str, Any]] = []

    def load_registry(self) -> List[Dict[str, Any]]:
        """Load the skill registry from JSON file."""
        if not self.registry_path.exists():
            self.errors.append({
                "type": "registry_not_found",
                "message": f"Registry file not found: {self.registry_path}",
            })
            return []

        try:
            with open(self.registry_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            self.errors.append({
                "type": "invalid_json",
                "message": f"Invalid JSON in registry: {e}",
            })
            return []
        except Exception as e:
            self.errors.append({
                "type": "read_error",
                "message": f"Error reading registry: {e}",
            })
            return []

    def validate_skill_structure(self, skill: Dict[str, Any]) -> List[str]:
        """Validate the structure of a skill definition."""
        errors = []

        # Check required fields
        for field in self.REQUIRED_FIELDS:
            if field not in skill:
                errors.append(f"Missing required field: {field}")

        # Check status is valid
        if "status" in skill and skill["status"] not in self.VALID_STATUSES:
            errors.append(f"Invalid status: {skill['status']}")

        # Check types
        if "name" in skill and not isinstance(skill["name"], str):
            errors.append("Field 'name' must be a string")

        if "id" in skill and not isinstance(skill["id"], str):
            errors.append("Field 'id' must be a string")

        return errors

    def validate_skill_files(self, skill: Dict[str, Any]) -> List[str]:
        """Validate that skill files exist on disk."""
        errors = []

        if "path" not in skill:
            return errors

        skill_path = Path(skill["path"])

        # If relative path, make it absolute
        if not skill_path.is_absolute():
            # Try to resolve relative to project root
            skill_path = self.project_root / skill_path

        if not skill_path.exists():
            errors.append(f"Skill file not found: {skill_path}")
        elif not skill_path.is_file():
            errors.append(f"Skill path is not a file: {skill_path}")

        # Check if skill directory exists (for skills with scripts)
        skill_id = skill.get("id", "")
        if skill_id:
            skill_dir = self.project_root / skill_id
            if skill_dir.exists() and skill_dir.is_dir():
                # Check for SKILL.md in directory
                skill_md = skill_dir / "SKILL.md"
                if not skill_md.exists():
                    self.warnings.append({
                        "skill": skill_id,
                        "message": f"SKILL.md not found in {skill_dir}",
                    })

        return errors

    def validate_skill(self, skill: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a single skill comprehensively."""
        skill_id = skill.get("id", "unknown")
        result = {
            "skill": skill_id,
            "valid": True,
            "errors": [],
            "warnings": [],
        }

        # Validate structure
        structure_errors = self.validate_skill_structure(skill)
        if structure_errors:
            result["valid"] = False
            result["errors"].extend(structure_errors)

        # Validate files
        file_errors = self.validate_skill_files(skill)
        if file_errors:
            result["valid"] = False
            result["errors"].extend(file_errors)

        return result

    def validate_all_skills(self) -> Dict[str, Any]:
        """Validate all skills in the registry."""
        self.errors = []
        self.warnings = []

        registry = self.load_registry()
        if not registry:
            return {
                "total": 0,
                "valid": 0,
                "invalid": 0,
                "errors": len(self.errors),
                "details": [],
                "validation_errors": self.errors,
            }

        results = []
        valid_count = 0
        invalid_count = 0

        for skill in registry:
            result = self.validate_skill(skill)
            results.append(result)

            if result["valid"]:
                valid_count += 1
            else:
                invalid_count += 1

        return {
            "total": len(registry),
            "valid": valid_count,
            "invalid": invalid_count,
            "errors": len(self.errors),
            "warnings": len(self.warnings),
            "details": results,
            "validation_errors": self.errors,
            "validation_warnings": self.warnings,
        }

    def get_active_skills(self) -> List[Dict[str, Any]]:
        """Get all active skills from the registry."""
        registry = self.load_registry()
        return [s for s in registry if s.get("status") == "active"]

    def get_skills_by_cluster(self, cluster: str) -> List[Dict[str, Any]]:
        """Get skills filtered by cluster."""
        registry = self.load_registry()
        return [s for s in registry if s.get("cluster") == cluster]

    def find_duplicate_ids(self) -> List[Dict[str, Any]]:
        """Find duplicate skill IDs in the registry."""
        registry = self.load_registry()
        seen_ids: Dict[str, int] = {}
        duplicates = []

        for skill in registry:
            skill_id = skill.get("id", "")
            if skill_id in seen_ids:
                duplicates.append({
                    "id": skill_id,
                    "occurrences": seen_ids[skill_id] + 1,
                })
                seen_ids[skill_id] += 1
            else:
                seen_ids[skill_id] = 1

        return duplicates


class TestDiscoverer:
    """Discovers and categorizes tests."""

    def __init__(self, tests_dir: Optional[Path] = None):
        self.tests_dir = tests_dir or Path(__file__).parent

    def discover_pytest_tests(self) -> List[Dict[str, Any]]:
        """Discover all pytest tests."""
        tests = []

        for test_file in self.tests_dir.rglob("test_*.py"):
            # Parse test file to find test functions
            test_info = {
                "file": str(test_file.relative_to(self.tests_dir)),
                "tests": [],
            }

            try:
                with open(test_file, "r", encoding="utf-8") as f:
                    content = f.read()

                # Simple regex-like parsing for test functions
                for line in content.split("\n"):
                    line = line.strip()
                    if line.startswith("def test_"):
                        func_name = line.split("(")[0].replace("def ", "")
                        test_info["tests"].append(func_name)

            except Exception as e:
                test_info["error"] = str(e)

            if test_info["tests"]:
                tests.append(test_info)

        return tests

    def count_tests_by_category(self) -> Dict[str, int]:
        """Count tests by category."""
        categories = {
            "unit": 0,
            "integration": 0,
            "e2e": 0,
            "skill": 0,
            "total": 0,
        }

        for test_file in self.tests_dir.rglob("test_*.py"):
            rel_path = str(test_file.relative_to(self.tests_dir))

            try:
                with open(test_file, "r", encoding="utf-8") as f:
                    content = f.read()

                count = content.count("\ndef test_")
                categories["total"] += count

                if "unit" in rel_path:
                    categories["unit"] += count
                elif "integration" in rel_path:
                    categories["integration"] += count
                elif "e2e" in rel_path:
                    categories["e2e"] += count
                elif "skills" in rel_path:
                    categories["skill"] += count

            except Exception:
                pass

        return categories

    def list_skill_tests(self) -> List[str]:
        """List all skill-specific tests."""
        skill_tests = []
        skills_dir = self.tests_dir / "unit" / "skills"

        if skills_dir.exists():
            for test_file in skills_dir.glob("test_*.py"):
                skill_name = test_file.stem.replace("test_", "")
                skill_tests.append(skill_name)

        return skill_tests


class TestReport:
    """Generates test reports."""

    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or Path(__file__).parent.parent
        self.report_data: Dict[str, Any] = {
            "timestamp": datetime.now().isoformat(),
            "results": {},
            "summary": {},
        }

    def add_result(self, name: str, exit_code: int, output: str = "") -> None:
        """Add a test result."""
        self.report_data["results"][name] = {
            "exit_code": exit_code,
            "passed": exit_code == 0,
            "output": output,
        }

    def set_summary(self, passed: int, total: int, elapsed: float) -> None:
        """Set the summary statistics."""
        self.report_data["summary"] = {
            "passed": passed,
            "total": total,
            "failed": total - passed,
            "elapsed_seconds": elapsed,
            "success_rate": (passed / total * 100) if total > 0 else 0,
        }

    def save(self, filename: str = "test_report.json") -> Path:
        """Save the report to a JSON file."""
        report_path = self.project_root / filename
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(self.report_data, f, indent=2)
        return report_path

    def generate_html(self, filename: str = "test_report.html") -> Path:
        """Generate an HTML report."""
        html_path = self.project_root / filename

        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Global Skills Test Report</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        h1 {{
            color: #333;
            border-bottom: 3px solid #4CAF50;
            padding-bottom: 10px;
        }}
        .summary {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .result {{
            background: white;
            padding: 15px;
            margin: 10px 0;
            border-radius: 4px;
            border-left: 4px solid #ddd;
        }}
        .passed {{
            border-left-color: #4CAF50;
            background: #e8f5e9;
        }}
        .failed {{
            border-left-color: #f44336;
            background: #ffebee;
        }}
        .metric {{
            display: inline-block;
            margin: 10px 20px 10px 0;
            font-size: 18px;
        }}
        .metric-value {{
            font-weight: bold;
            color: #333;
        }}
        .timestamp {{
            color: #666;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <h1>🧪 Global Skills Test Report</h1>
    <p class="timestamp">Generated: {self.report_data['timestamp']}</p>

    <div class="summary">
        <h2>Summary</h2>
        <div class="metric">
            Total: <span class="metric-value">{self.report_data['summary'].get('total', 0)}</span>
        </div>
        <div class="metric">
            Passed: <span class="metric-value" style="color: #4CAF50;">{self.report_data['summary'].get('passed', 0)}</span>
        </div>
        <div class="metric">
            Failed: <span class="metric-value" style="color: #f44336;">{self.report_data['summary'].get('failed', 0)}</span>
        </div>
        <div class="metric">
            Success Rate: <span class="metric-value">{self.report_data['summary'].get('success_rate', 0):.1f}%</span>
        </div>
        <div class="metric">
            Duration: <span class="metric-value">{self.report_data['summary'].get('elapsed_seconds', 0):.2f}s</span>
        </div>
    </div>

    <h2>Test Results</h2>
"""

        for name, result in self.report_data["results"].items():
            status_class = "passed" if result["passed"] else "failed"
            status_icon = "✓" if result["passed"] else "✗"
            html_content += f"""
    <div class="result {status_class}">
        <strong>{status_icon} {name}</strong>
        <span style="float: right; color: {'#4CAF50' if result['passed'] else '#f44336'};">
            {'PASSED' if result['passed'] else 'FAILED'}
        </span>
    </div>
"""

        html_content += """
</body>
</html>
"""

        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        return html_path


def generate_skill_test_template(skill_name: str) -> str:
    """Generate a test file template for a skill."""
    return f'''"""
Tests for {skill_name} skill.

Auto-generated test template. Customize as needed.
"""

import pytest
from pathlib import Path


# Mark all tests in this file as skill tests
pytestmark = pytest.mark.skill


class Test{skill_name.replace("-", "_").title()}Skill:
    """Test suite for {skill_name} skill."""

    def test_skill_exists_in_registry(self, skill_registry):
        """Verify skill is registered."""
        skill_ids = [s["id"] for s in skill_registry]
        assert "{skill_name}" in skill_ids, f"Skill {skill_name} not found in registry"

    def test_skill_is_active(self, skill_registry):
        """Verify skill is active."""
        skill = next((s for s in skill_registry if s["id"] == "{skill_name}"), None)
        assert skill is not None
        assert skill["status"] == "active"

    def test_skill_has_required_fields(self, skill_registry, skill_assertions):
        """Verify skill has all required fields."""
        skill = next((s for s in skill_registry if s["id"] == "{skill_name}"), None)
        assert skill is not None
        skill_assertions.assert_valid_skill(skill)

    def test_skill_files_exist(self, skill_registry, project_root):
        """Verify skill files exist on disk."""
        skill = next((s for s in skill_registry if s["id"] == "{skill_name}"), None)
        if skill:
            skill_path = Path(skill["path"])
            if not skill_path.is_absolute():
                skill_path = project_root / skill_path
            assert skill_path.exists(), f"Skill file not found: {{skill_path}}"

    def test_skill_has_documentation(self, skill_registry, project_root):
        """Verify skill has SKILL.md documentation."""
        skill_dir = project_root / "{skill_name}"
        if skill_dir.exists():
            skill_md = skill_dir / "SKILL.md"
            assert skill_md.exists(), f"SKILL.md not found in {{skill_dir}}"
'''


if __name__ == "__main__":
    # Run validation if executed directly
    validator = SkillValidator()
    report = validator.validate_all_skills()

    print("\n" + "="*60)
    print("SKILL VALIDATION REPORT")
    print("="*60 + "\n")

    print(f"Total Skills: {report['total']}")
    print(f"Valid: {report['valid']}")
    print(f"Invalid: {report['invalid']}")
    print(f"Errors: {report['errors']}")

    if report['details']:
        print("\nDetails:")
        for detail in report['details']:
            status = "✓" if detail['valid'] else "✗"
            print(f"  {status} {detail['skill']}")
            if detail['errors']:
                for error in detail['errors']:
                    print(f"    - {error}")

    sys.exit(0 if report['invalid'] == 0 else 1)
