#!/usr/bin/env python3
"""
Skill Test Generator - Genera tests automáticamente para todos los skills.

Uso:
    python scripts/generate_skill_tests.py --all
    python scripts/generate_skill_tests.py --skill security-auditor
    python scripts/generate_skill_tests.py --missing
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

# Template para tests de skills
SKILL_TEST_TEMPLATE = '''"""
Tests for {skill_name} skill.

Auto-generated test template. Customize as needed.
Generated: {timestamp}
"""

import pytest
from pathlib import Path


# Mark all tests in this file as skill tests
pytestmark = pytest.mark.skill


class Test{skill_class_name}Skill:
    """Test suite for {skill_name} skill."""

    def test_skill_exists_in_registry(self, skill_registry):
        """Verify skill is registered."""
        skill_ids = [s["id"] for s in skill_registry]
        assert "{skill_id}" in skill_ids, f"Skill {skill_name} not found in registry"

    def test_skill_is_active(self, skill_registry):
        """Verify skill is active."""
        skill = next((s for s in skill_registry if s["id"] == "{skill_id}"), None)
        assert skill is not None
        assert skill["status"] == "active"

    def test_skill_has_required_fields(self, skill_registry, skill_assertions):
        """Verify skill has all required fields."""
        skill = next((s for s in skill_registry if s["id"] == "{skill_id}"), None)
        assert skill is not None
        skill_assertions.assert_valid_skill(skill)

    def test_skill_has_name(self, skill_registry):
        """Verify skill has a name."""
        skill = next((s for s in skill_registry if s["id"] == "{skill_id}"), None)
        assert skill is not None
        assert skill.get("name")
        assert isinstance(skill["name"], str)

    def test_skill_has_description(self, skill_registry):
        """Verify skill has a description."""
        skill = next((s for s in skill_registry if s["id"] == "{skill_id}"), None)
        assert skill is not None
        assert skill.get("description")
        assert isinstance(skill["description"], str)

    def test_skill_has_cluster(self, skill_registry):
        """Verify skill has a cluster assigned."""
        skill = next((s for s in skill_registry if s["id"] == "{skill_id}"), None)
        assert skill is not None
        assert skill.get("cluster")
        assert isinstance(skill["cluster"], str)

    def test_skill_files_exist(self, skill_registry, project_root):
        """Verify skill files exist on disk."""
        skill = next((s for s in skill_registry if s["id"] == "{skill_id}"), None)
        if skill and skill.get("path"):
            skill_path = Path(skill["path"])
            if not skill_path.is_absolute():
                skill_path = project_root / skill_path
            assert skill_path.exists(), f"Skill file not found: {{skill_path}}"

    def test_skill_has_documentation(self, project_root):
        """Verify skill has SKILL.md documentation."""
        skill_dir = project_root / "{skill_dir_name}"
        if skill_dir.exists():
            skill_md = skill_dir / "SKILL.md"
            assert skill_md.exists(), f"SKILL.md not found in {{skill_dir}}"

    def test_skill_has_version(self, skill_registry):
        """Verify skill has a version."""
        skill = next((s for s in skill_registry if s["id"] == "{skill_id}"), None)
        assert skill is not None
        assert skill.get("version")
        # Version should follow semantic versioning (simplified check)
        version = skill["version"]
        assert "." in version, "Version should follow semantic versioning"

    def test_skill_has_cost_estimate(self, skill_registry):
        """Verify skill has cost estimate."""
        skill = next((s for s in skill_registry if s["id"] == "{skill_id}"), None)
        assert skill is not None
        cost = skill.get("cost_estimate", {{}})
        assert "per_execution" in cost
        assert "currency" in cost

    def test_skill_has_preferred_agent(self, skill_registry):
        """Verify skill has preferred agent assigned."""
        skill = next((s for s in skill_registry if s["id"] == "{skill_id}"), None)
        assert skill is not None
        assert skill.get("preferred_agent")
        assert skill["preferred_agent"].startswith("AGENT_")
'''


class SkillTestGenerator:
    """Generates test files for skills."""

    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or Path(__file__).parent.parent
        self.registry_path = self.project_root / "skill_registry.json"
        self.skills_test_dir = self.project_root / "tests" / "unit" / "skills"
        self.generated_files: List[Path] = []

    def load_registry(self) -> List[Dict[str, Any]]:
        """Load the skill registry."""
        if not self.registry_path.exists():
            print(f"❌ Registry not found: {self.registry_path}")
            return []

        with open(self.registry_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def generate_class_name(self, skill_id: str) -> str:
        """Generate a valid Python class name from skill ID."""
        # Convert kebab-case or snake_case to PascalCase
        parts = skill_id.replace("-", "_").split("_")
        return "".join(part.capitalize() for part in parts)

    def generate_test_file(self, skill: Dict[str, Any]) -> Path:
        """Generate a test file for a single skill."""
        skill_id = skill.get("id", "")
        skill_name = skill.get("name", skill_id)
        skill_dir_name = skill_id  # Directory name matches ID

        if not skill_id:
            raise ValueError("Skill ID is required")

        # Generate class name
        skill_class_name = self.generate_class_name(skill_id)

        # Generate test content
        from datetime import datetime

        test_content = SKILL_TEST_TEMPLATE.format(
            skill_name=skill_name,
            skill_id=skill_id,
            skill_class_name=skill_class_name,
            skill_dir_name=skill_dir_name,
            timestamp=datetime.now().isoformat(),
        )

        # Ensure directory exists
        self.skills_test_dir.mkdir(parents=True, exist_ok=True)

        # Write test file
        test_file = self.skills_test_dir / f"test_{skill_id}.py"
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(test_content)

        self.generated_files.append(test_file)
        return test_file

    def generate_all_tests(self, force: bool = False) -> List[Path]:
        """Generate tests for all skills in the registry."""
        registry = self.load_registry()
        if not registry:
            return []

        print(f"🔄 Generating tests for {len(registry)} skills...\n")

        for skill in registry:
            skill_id = skill.get("id", "")
            if not skill_id:
                continue

            test_file = self.skills_test_dir / f"test_{skill_id}.py"

            if test_file.exists() and not force:
                print(f"  ⏭️  Skipping {skill_id} (already exists)")
                continue

            try:
                self.generate_test_file(skill)
                print(f"  ✅ Generated tests for: {skill_id}")
            except Exception as e:
                print(f"  ❌ Error generating tests for {skill_id}: {e}")

        return self.generated_files

    def generate_missing_tests(self) -> List[Path]:
        """Generate tests only for skills that don't have them yet."""
        registry = self.load_registry()
        if not registry:
            return []

        # Find existing test files
        existing_tests: Set[str] = set()
        if self.skills_test_dir.exists():
            for test_file in self.skills_test_dir.glob("test_*.py"):
                skill_id = test_file.stem.replace("test_", "")
                existing_tests.add(skill_id)

        # Find skills without tests
        missing_skills = [
            s for s in registry if s.get("id") and s["id"] not in existing_tests
        ]

        if not missing_skills:
            print("✅ All skills already have tests!")
            return []

        print(f"🔄 Generating tests for {len(missing_skills)} missing skills...\n")

        for skill in missing_skills:
            skill_id = skill.get("id", "")
            try:
                self.generate_test_file(skill)
                print(f"  ✅ Generated: {skill_id}")
            except Exception as e:
                print(f"  ❌ Error: {skill_id}: {e}")

        return self.generated_files

    def list_existing_tests(self) -> List[str]:
        """List all skills that have tests."""
        if not self.skills_test_dir.exists():
            return []

        skills = []
        for test_file in self.skills_test_dir.glob("test_*.py"):
            skill_id = test_file.stem.replace("test_", "")
            skills.append(skill_id)

        return sorted(skills)

    def get_test_coverage(self) -> Dict[str, Any]:
        """Get test coverage statistics."""
        registry = self.load_registry()
        existing_tests = set(self.list_existing_tests())

        total = len(registry)
        tested = len([s for s in registry if s.get("id") in existing_tests])
        missing = total - tested

        missing_skills = [
            s["id"] for s in registry if s.get("id") not in existing_tests
        ]

        return {
            "total_skills": total,
            "tested": tested,
            "missing": missing,
            "coverage_percent": (tested / total * 100) if total > 0 else 0,
            "missing_skills": missing_skills,
        }


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate tests for Global Skills",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/generate_skill_tests.py --all          # Generate for all skills
  python scripts/generate_skill_tests.py --missing      # Generate only missing
  python scripts/generate_skill_tests.py --skill ai-engineer  # Generate for one skill
  python scripts/generate_skill_tests.py --list         # List existing tests
  python scripts/generate_skill_tests.py --coverage     # Show test coverage
        """,
    )

    parser.add_argument(
        "--all", "-a", action="store_true", help="Generate tests for all skills"
    )
    parser.add_argument(
        "--missing", "-m", action="store_true", help="Generate only missing tests"
    )
    parser.add_argument("--skill", "-s", help="Generate tests for specific skill")
    parser.add_argument(
        "--force", "-f", action="store_true", help="Overwrite existing tests"
    )
    parser.add_argument("--list", "-l", action="store_true", help="List existing tests")
    parser.add_argument(
        "--coverage", "-c", action="store_true", help="Show test coverage"
    )

    args = parser.parse_args()

    generator = SkillTestGenerator()

    if args.list:
        tests = generator.list_existing_tests()
        print(f"\n📋 Existing skill tests ({len(tests)}):\n")
        for test in tests:
            print(f"  • {test}")
        return 0

    if args.coverage:
        coverage = generator.get_test_coverage()
        print("\n📊 Test Coverage:\n")
        print(f"  Total Skills: {coverage['total_skills']}")
        print(f"  With Tests: {coverage['tested']}")
        print(f"  Missing: {coverage['missing']}")
        print(f"  Coverage: {coverage['coverage_percent']:.1f}%")

        if coverage["missing_skills"]:
            print("\n  Missing tests for:")
            for skill in coverage["missing_skills"]:
                print(f"    • {skill}")
        return 0

    if args.skill:
        # Generate for specific skill
        registry = generator.load_registry()
        skill = next((s for s in registry if s.get("id") == args.skill), None)

        if not skill:
            print(f"❌ Skill not found: {args.skill}")
            return 1

        test_file = generator.generate_test_file(skill)
        print(f"\n✅ Generated test file: {test_file}")
        return 0

    if args.missing:
        generator.generate_missing_tests()
        print(f"\n✅ Generated {len(generator.generated_files)} test files")
        return 0

    if args.all:
        generator.generate_all_tests(force=args.force)
        print(f"\n✅ Generated {len(generator.generated_files)} test files")
        return 0

    # Default: show help
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
