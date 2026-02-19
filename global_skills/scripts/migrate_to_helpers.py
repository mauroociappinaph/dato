#!/usr/bin/env python3
"""
Script de migración para centralizar imports comunes en src/helpers/

Convierte archivos que usan os/sys/requests a usar los helpers centralizados.
"""

import os
import sys
import re
from pathlib import Path
from typing import List, Tuple

# Añadir src al path para importar helpers
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from helpers import get_project_root, list_python_files, get_relative_path


class ImportMigrator:
    """Migrates common imports to use centralized helpers."""

    def __init__(self):
        self.project_root = get_project_root()
        self.helpers_path = self.project_root / "src" / "helpers"

    def analyze_file(self, filepath: Path) -> dict:
        """Analyze a file to detect patterns that can be migrated."""
        content = filepath.read_text(encoding="utf-8", errors="ignore")

        patterns = {
            "has_os": "import os" in content,
            "has_sys": "import sys" in content,
            "has_requests": "import requests" in content,
            "has_os_path_join": "os.path.join" in content,
            "has_os_path_exists": "os.path.exists" in content,
            "has_os_makedirs": "os.makedirs" in content,
            "has_os_environ": "os.environ" in content or "os.getenv" in content,
            "has_sys_path_append": "sys.path.append" in content,
            "has_os_path_dirname": "os.path.dirname" in content,
            "has_os_path_abspath": "os.path.abspath" in content,
        }

        return patterns

    def should_migrate(self, filepath: Path) -> bool:
        """Check if file should be migrated."""
        # Skip helpers themselves, scripts, and core
        rel_path = get_relative_path(str(filepath), str(self.project_root))

        skip_patterns = [
            "src/helpers/",
            "src/core/",
            "src/types/",
            "scripts/",
            "__pycache__",
            "_archive/",
            "test_",
        ]

        for pattern in skip_patterns:
            if pattern in rel_path:
                return False

        return True

    def generate_import_statement(self, filepath: Path) -> str:
        """Generate the import statement for helpers."""
        # Calculate relative import path
        rel_path = get_relative_path(str(filepath), str(self.project_root))
        depth = len(Path(rel_path).parts) - 1

        if depth == 0:
            return "from src.helpers import get_env_var, ensure_dir, join_paths, path_exists"
        elif depth == 1:
            return "from ..src.helpers import get_env_var, ensure_dir, join_paths, path_exists"
        elif depth == 2:
            return "from ...src.helpers import get_env_var, ensure_dir, join_paths, path_exists"
        else:
            return "from src.helpers import get_env_var, ensure_dir, join_paths, path_exists"

    def migrate_file(self, filepath: Path, dry_run: bool = True) -> dict:
        """Migrate a single file."""
        content = filepath.read_text(encoding="utf-8", errors="ignore")
        original_content = content
        changes = []

        # Check if already imports from helpers
        if "from src.helpers" in content or "from ..src.helpers" in content:
            return {"migrated": False, "reason": "Already uses helpers", "changes": []}

        # Determine which helpers are needed
        needed_helpers = []

        if "os.environ.get" in content or "os.getenv" in content:
            needed_helpers.append("get_env_var")

        if "os.makedirs" in content:
            needed_helpers.append("ensure_dir")

        if "os.path.join" in content:
            needed_helpers.append("join_paths")

        if "os.path.exists" in content:
            needed_helpers.append("path_exists")

        if "os.path.dirname" in content and "os.path.abspath" in content:
            needed_helpers.append("get_script_dir")

        if not needed_helpers:
            return {"migrated": False, "reason": "No migratable patterns", "changes": []}

        # Generate import statement
        helper_import = self._generate_import_line(filepath, needed_helpers)

        # Find where to insert import (after existing imports)
        lines = content.split("\n")
        import_idx = 0
        for i, line in enumerate(lines):
            if line.startswith("import ") or line.startswith("from "):
                import_idx = i + 1

        # Insert helper import
        lines.insert(import_idx, helper_import)
        changes.append(f"Added import: {helper_import}")

        new_content = "\n".join(lines)

        if not dry_run:
            filepath.write_text(new_content, encoding="utf-8")

        return {
            "migrated": True,
            "reason": "Success",
            "changes": changes,
            "helpers": needed_helpers,
        }

    def _generate_import_line(self, filepath: Path, helpers: List[str]) -> str:
        """Generate import line with correct relative path."""
        rel_path = get_relative_path(str(filepath), str(self.project_root))
        depth = len(Path(rel_path).parts) - 1

        helpers_str = ", ".join(sorted(helpers))

        if depth == 0:
            prefix = "from src.helpers"
        elif depth == 1:
            prefix = "from ..src.helpers"
        elif depth == 2:
            prefix = "from ...src.helpers"
        elif depth == 3:
            prefix = "from ....src.helpers"
        else:
            prefix = "from src.helpers"

        return f"{prefix} import {helpers_str}"

    def run_migration(self, dry_run: bool = True) -> dict:
        """Run migration on all eligible files."""
        results = {
            "total_analyzed": 0,
            "migrated": 0,
            "skipped": 0,
            "errors": [],
            "migrations": [],
        }

        # Get all Python files
        python_files = list_python_files(str(self.project_root))

        for filepath in python_files:
            if not self.should_migrate(filepath):
                continue

            results["total_analyzed"] += 1

            try:
                result = self.migrate_file(filepath, dry_run=dry_run)

                if result["migrated"]:
                    results["migrated"] += 1
                    results["migrations"].append({
                        "file": str(filepath.relative_to(self.project_root)),
                        "helpers": result.get("helpers", []),
                    })
                else:
                    results["skipped"] += 1

            except Exception as e:
                results["errors"].append({
                    "file": str(filepath),
                    "error": str(e),
                })

        return results


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Migrate files to use centralized helpers")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=True,
        help="Show what would be changed without making changes",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually apply the migrations",
    )
    args = parser.parse_args()

    dry_run = not args.apply

    print("=" * 80)
    print("🚀 MIGRACIÓN A HELPERS CENTRALIZADOS")
    print("=" * 80)
    print(f"\nModo: {'DRY RUN (sin cambios)' if dry_run else 'APLICAR CAMBIOS'}")
    print()

    migrator = ImportMigrator()
    results = migrator.run_migration(dry_run=dry_run)

    print(f"📊 RESULTADOS:")
    print(f"   Archivos analizados: {results['total_analyzed']}")
    print(f"   Archivos migrados: {results['migrated']}")
    print(f"   Archivos omitidos: {results['skipped']}")

    if results["migrations"]:
        print(f"\n📁 ARCHIVOS MIGRADOS:")
        for migration in results["migrations"]:
            print(f"   ✓ {migration['file']}")
            print(f"     Helpers: {', '.join(migration['helpers'])}")

    if results["errors"]:
        print(f"\n❌ ERRORES ({len(results['errors'])}):")
        for error in results["errors"]:
            print(f"   - {error['file']}: {error['error']}")

    print("\n" + "=" * 80)

    if dry_run and results["migrated"] > 0:
        print("\n💡 Para aplicar los cambios, ejecuta:")
        print("   python scripts/migrate_to_helpers.py --apply")


if __name__ == "__main__":
    main()
