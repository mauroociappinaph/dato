#!/usr/bin/env python3
"""
Generate Barrel Files - CLI tool for auto-generating __init__.py files.

Usage:
    python scripts/generate_barrel_files.py [SKILLS_ROOT] [--dry-run]

Examples:
    # Generate all barrel files
    python scripts/generate_barrel_files.py

    # Preview changes without writing
    python scripts/generate_barrel_files.py --dry-run

    # Specify custom skills directory
    python scripts/generate_barrel_files.py /path/to/global_skills
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.barrel_generator import BarrelGenerator, generate_barrel_files


def main():
    """Main entry point for CLI."""
    # Parse arguments
    args = sys.argv[1:]
    dry_run = "--dry-run" in args

    # Get skills root (default to parent directory)
    skills_root = "."
    for arg in args:
        if not arg.startswith("--"):
            skills_root = arg
            break

    # Resolve to absolute path
    skills_root = Path(skills_root).resolve()

    print("=" * 70)
    print("🛢️  GLOBAL SKILLS - BARREL FILE GENERATOR")
    print("=" * 70)
    print(f"\n📂 Skills root: {skills_root}")
    print(f"🧪 Dry run: {dry_run}")
    print()

    # Check if directory exists
    if not skills_root.exists():
        print(f"❌ Error: Directory not found: {skills_root}")
        sys.exit(1)

    # Check for skill_registry.json
    registry_path = skills_root / "skill_registry.json"
    if not registry_path.exists():
        print(f"⚠️  Warning: skill_registry.json not found at {registry_path}")
        print("   Will scan filesystem instead...")

    # Generate barrel files
    try:
        results = generate_barrel_files(str(skills_root), dry_run=dry_run)

        if dry_run:
            print("\n✅ Dry run complete. No files were modified.")
        else:
            success_count = sum(1 for v in results.values() if v)
            total_count = len(results)

            print("\n" + "=" * 70)
            print("📊 GENERATION SUMMARY")
            print("=" * 70)
            print(f"\n✅ Successfully generated: {success_count}/{total_count}")

            if success_count < total_count:
                print("\n❌ Failed generations:")
                for path, success in results.items():
                    if not success:
                        print(f"   - {path}")

            print("\n🎉 Barrel file generation complete!")
            print(f"\nNext steps:")
            print(f"   1. Review generated files")
            print(f"   2. Run: python scripts/validate_architecture.py")

    except Exception as e:
        print(f"\n❌ Error during generation: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
