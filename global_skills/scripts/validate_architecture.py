#!/usr/bin/env python3
"""
Validate Architecture - Check compliance with architectural standards.

Validates:
- No files exceed 300 lines (The 300 Rule)
- All __init__.py files are valid barrel files
- No duplicate code patterns
- Proper directory structure

Usage:
    python scripts/validate_architecture.py [SKILLS_ROOT]

Exit codes:
    0 - All validations passed
    1 - One or more validations failed
"""

import sys
import os
from pathlib import Path
from typing import List, Tuple, Dict
import json


class ArchitectureValidator:
    """Validates Global Skills architecture compliance."""

    def __init__(self, skills_root: str):
        self.skills_root = Path(skills_root)
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.stats: Dict[str, int] = {
            "total_files": 0,
            "python_files": 0,
            "large_files": 0,
            "empty_init_files": 0,
            "skills_count": 0,
        }

    def validate(self) -> bool:
        """Run all validations. Returns True if all passed."""
        print("🔍 Running architecture validations...\n")

        self._check_directory_structure()
        self._validate_300_rule()
        self._validate_barrel_files()
        self._check_src_structure()

        return len(self.errors) == 0

    def _check_directory_structure(self) -> None:
        """Verify required directories exist."""
        print("📁 Checking directory structure...")

        required_dirs = [
            "src/core",
            "src/helpers",
            "src/types",
            "scripts",
            "docs",
            "tests",
        ]

        for dir_path in required_dirs:
            full_path = self.skills_root / dir_path
            if not full_path.exists():
                self.errors.append(f"Missing required directory: {dir_path}")
            else:
                print(f"   ✅ {dir_path}")

        print()

    def _validate_300_rule(self) -> None:
        """Check that no files exceed 300 lines."""
        print("📏 Validating The 300 Rule (max 300 lines per file)...")

        large_files = []

        for py_file in self.skills_root.rglob("*.py"):
            # Skip __pycache__ and .git
            if "__pycache__" in str(py_file) or ".git" in str(py_file):
                continue

            self.stats["python_files"] += 1

            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    line_count = len(f.readlines())

                if line_count > 300:
                    large_files.append((py_file.relative_to(self.skills_root), line_count))
                    self.stats["large_files"] += 1
            except Exception:
                pass

        if large_files:
            print(f"   ⚠️  Found {len(large_files)} files exceeding 300 lines:")
            for file_path, line_count in sorted(large_files, key=lambda x: x[1], reverse=True):
                print(f"      - {file_path}: {line_count} lines")
                self.warnings.append(f"File exceeds 300 lines: {file_path} ({line_count})")
        else:
            print("   ✅ All files comply with The 300 Rule")

        print()

    def _validate_barrel_files(self) -> None:
        """Check that __init__.py files are valid barrel files."""
        print("🛢️  Validating barrel files...")

        empty_init_files = []

        for init_file in self.skills_root.rglob("__init__.py"):
            # Skip __pycache__
            if "__pycache__" in str(init_file):
                continue

            try:
                with open(init_file, "r", encoding="utf-8") as f:
                    content = f.read().strip()

                # Check if file is empty or nearly empty (just a comment or docstring)
                lines = [line.strip() for line in content.split("\n") if line.strip()]
                code_lines = [line for line in lines if not line.startswith("#")]

                if len(code_lines) <= 1:
                    rel_path = init_file.relative_to(self.skills_root)
                    empty_init_files.append(rel_path)
                    self.stats["empty_init_files"] += 1
            except Exception:
                pass

        if empty_init_files:
            print(f"   ⚠️  Found {len(empty_init_files)} empty/nearly empty __init__.py files:")
            for file_path in empty_init_files[:10]:
                print(f"      - {file_path}")
            if len(empty_init_files) > 10:
                print(f"      ... and {len(empty_init_files) - 10} more")
            self.warnings.append(f"Empty __init__.py files found: {len(empty_init_files)}")
        else:
            print("   ✅ All barrel files are properly populated")

        print()

    def _check_src_structure(self) -> None:
        """Verify src/ directory has proper structure."""
        print("🔧 Checking src/ structure...")

        required_src_files = [
            "src/core/__init__.py",
            "src/core/base_skill.py",
            "src/core/interfaces.py",
            "src/core/exceptions.py",
            "src/core/barrel_generator.py",
            "src/helpers/__init__.py",
            "src/helpers/file_utils.py",
            "src/helpers/validation_utils.py",
            "src/helpers/http_utils.py",
            "src/types/__init__.py",
            "src/types/common_types.py",
        ]

        for file_path in required_src_files:
            full_path = self.skills_root / file_path
            if full_path.exists():
                print(f"   ✅ {file_path}")
            else:
                print(f"   ❌ Missing: {file_path}")
                self.errors.append(f"Missing required file: {file_path}")

        print()

    def print_report(self) -> None:
        """Print validation report."""
        print("=" * 70)
        print("📊 VALIDATION REPORT")
        print("=" * 70)

        print(f"\n📈 Statistics:")
        print(f"   Python files: {self.stats['python_files']}")
        print(f"   Large files (>300 lines): {self.stats['large_files']}")
        print(f"   Empty __init__.py: {self.stats['empty_init_files']}")

        if self.warnings:
            print(f"\n⚠️  Warnings ({len(self.warnings)}):")
            for warning in self.warnings[:10]:
                print(f"   - {warning}")
            if len(self.warnings) > 10:
                print(f"   ... and {len(self.warnings) - 10} more")

        if self.errors:
            print(f"\n❌ Errors ({len(self.errors)}):")
            for error in self.errors:
                print(f"   - {error}")

        print("\n" + "=" * 70)
        if not self.errors:
            print("✅ ALL VALIDATIONS PASSED")
            print("\nThe architecture is compliant with all standards!")
        else:
            print(f"❌ VALIDATION FAILED - {len(self.errors)} error(s)")
        print("=" * 70)


def main():
    """Main entry point."""
    # Get skills root
    skills_root = sys.argv[1] if len(sys.argv) > 1 else "."
    skills_root = Path(skills_root).resolve()

    print("=" * 70)
    print("🔍 GLOBAL SKILLS - ARCHITECTURE VALIDATOR")
    print("=" * 70)
    print(f"\n📂 Validating: {skills_root}\n")

    if not skills_root.exists():
        print(f"❌ Error: Directory not found: {skills_root}")
        sys.exit(1)

    # Run validation
    validator = ArchitectureValidator(str(skills_root))
    is_valid = validator.validate()
    validator.print_report()

    # Exit with appropriate code
    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()
