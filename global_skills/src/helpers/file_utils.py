"""
File utilities for Global Skills.

Common file operations used across multiple skills.
"""

import os
import shutil
from pathlib import Path
from typing import List, Optional, Dict, Any
import json
import yaml


def read_skill_file(skill_path: str, filename: str = "SKILL.md") -> Optional[str]:
    """
    Read a file from a skill directory.

    Args:
        skill_path: Path to the skill directory
        filename: Name of the file to read

    Returns:
        File content as string, or None if file doesn't exist
    """
    file_path = Path(skill_path) / filename
    if not file_path.exists():
        return None

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None


def write_skill_file(skill_path: str, filename: str, content: str) -> bool:
    """
    Write content to a file in a skill directory.

    Args:
        skill_path: Path to the skill directory
        filename: Name of the file to write
        content: Content to write

    Returns:
        True if successful, False otherwise
    """
    file_path = Path(skill_path) / filename

    try:
        ensure_directory(skill_path)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error writing {file_path}: {e}")
        return False


def list_skill_files(skill_path: str, pattern: str = "*") -> List[Path]:
    """
    List files in a skill directory matching a pattern.

    Args:
        skill_path: Path to the skill directory
        pattern: Glob pattern to match (default: "*")

    Returns:
        List of Path objects matching the pattern
    """
    skill_dir = Path(skill_path)
    if not skill_dir.exists():
        return []

    return list(skill_dir.glob(pattern))


def ensure_directory(path: str) -> Path:
    """
    Ensure a directory exists, creating it if necessary.

    Args:
        path: Directory path

    Returns:
        Path object
    """
    dir_path = Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def copy_skill_template(template_path: str, target_path: str, replacements: Dict[str, str] = None) -> bool:
    """
    Copy a skill template directory to a new location with optional replacements.

    Args:
        template_path: Path to the template directory
        target_path: Path to create the new skill
        replacements: Dictionary of string replacements for template files

    Returns:
        True if successful, False otherwise
    """
    try:
        template = Path(template_path)
        target = Path(target_path)

        if not template.exists():
            print(f"Template not found: {template}")
            return False

        if target.exists():
            print(f"Target already exists: {target}")
            return False

        # Copy template directory
        shutil.copytree(template, target)

        # Apply replacements if provided
        if replacements:
            for file_path in target.rglob("*"):
                if file_path.is_file():
                    try:
                        content = file_path.read_text(encoding="utf-8")
                        for old, new in replacements.items():
                            content = content.replace(old, new)
                        file_path.write_text(content, encoding="utf-8")
                    except Exception as e:
                        print(f"Warning: Could not process {file_path}: {e}")

        return True
    except Exception as e:
        print(f"Error copying template: {e}")
        return False


def load_json_file(file_path: str) -> Optional[Dict[str, Any]]:
    """Load a JSON file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON {file_path}: {e}")
        return None


def save_json_file(file_path: str, data: Dict[str, Any], indent: int = 2) -> bool:
    """Save data to a JSON file."""
    try:
        ensure_directory(Path(file_path).parent)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=indent, default=str)
        return True
    except Exception as e:
        print(f"Error saving JSON {file_path}: {e}")
        return False


def load_yaml_file(file_path: str) -> Optional[Dict[str, Any]]:
    """Load a YAML file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading YAML {file_path}: {e}")
        return None


def save_yaml_file(file_path: str, data: Dict[str, Any]) -> bool:
    """Save data to a YAML file."""
    try:
        ensure_directory(Path(file_path).parent)
        with open(file_path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)
        return True
    except Exception as e:
        print(f"Error saving YAML {file_path}: {e}")
        return False


def get_file_size(file_path: str) -> int:
    """Get file size in bytes."""
    try:
        return Path(file_path).stat().st_size
    except Exception:
        return 0


def get_line_count(file_path: str) -> int:
    """Get number of lines in a file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return len(f.readlines())
    except Exception:
        return 0
