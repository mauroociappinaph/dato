"""
System utilities for Global Skills.

Common system operations (os, sys, path) used across multiple skills.
"""

import os
import sys
from pathlib import Path
from typing import List, Optional, Tuple, Dict, Any


def get_env_var(key: str, default: Optional[str] = None, required: bool = False) -> Optional[str]:
    """
    Get an environment variable with optional default and required check.

    Args:
        key: Environment variable name
        default: Default value if not set
        required: If True, raises ValueError when not set

    Returns:
        The environment variable value or default

    Raises:
        ValueError: If required=True and variable is not set
    """
    value = os.environ.get(key, default)
    if required and value is None:
        raise ValueError(f"Required environment variable '{key}' is not set")
    return value


def get_env_int(key: str, default: Optional[int] = None, required: bool = False) -> Optional[int]:
    """Get an environment variable as integer."""
    value = get_env_var(key, None, required)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        raise ValueError(f"Environment variable '{key}' must be an integer, got: {value}")


def get_env_bool(key: str, default: bool = False) -> bool:
    """Get an environment variable as boolean."""
    value = os.environ.get(key, "").lower()
    if value in ("true", "1", "yes", "on"):
        return True
    if value in ("false", "0", "no", "off", ""):
        return default
    return default


def ensure_dir(path: str) -> Path:
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


def get_project_root() -> Path:
    """
    Get the project root directory.

    Returns:
        Path to project root
    """
    # Start from current file and go up to find project root
    current = Path(__file__).resolve()
    # Go up: system_utils.py -> helpers -> src -> global_skills
    return current.parent.parent.parent


def get_skill_dir(skill_name: str) -> Path:
    """
    Get the directory path for a specific skill.

    Args:
        skill_name: Name of the skill

    Returns:
        Path to skill directory
    """
    return get_project_root() / skill_name


def list_python_files(directory: str, exclude_dirs: Optional[List[str]] = None) -> List[Path]:
    """
    List all Python files in a directory recursively.

    Args:
        directory: Base directory to search
        exclude_dirs: List of directory names to exclude

    Returns:
        List of Path objects for Python files
    """
    if exclude_dirs is None:
        exclude_dirs = ['__pycache__', '.git', 'node_modules', '_archive', '.venv', 'venv']

    base_path = Path(directory)
    if not base_path.exists():
        return []

    python_files = []
    for path in base_path.rglob("*.py"):
        # Check if any part of the path is in exclude_dirs
        if not any(part in exclude_dirs for part in path.parts):
            python_files.append(path)

    return python_files


def read_file_lines(filepath: str) -> List[str]:
    """
    Read all lines from a file.

    Args:
        filepath: Path to file

    Returns:
        List of lines
    """
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return f.readlines()
    except Exception as e:
        return []


def get_file_line_count(filepath: str) -> int:
    """Get number of lines in a file."""
    return len(read_file_lines(filepath))


def get_relative_path(filepath: str, base_path: str) -> str:
    """
    Get relative path from base path.

    Args:
        filepath: Full file path
        base_path: Base directory path

    Returns:
        Relative path string
    """
    return os.path.relpath(filepath, base_path)


def walk_directory(base_path: str, exclude_dirs: Optional[List[str]] = None):
    """
    Walk directory tree yielding (root, dirs, files).

    Args:
        base_path: Base directory to walk
        exclude_dirs: List of directory names to exclude

    Yields:
        Tuples of (root, dirs, files)
    """
    if exclude_dirs is None:
        exclude_dirs = ['__pycache__', '.git', 'node_modules', '_archive']

    for root, dirs, files in os.walk(base_path):
        # Filter out excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        yield root, dirs, files


def add_to_python_path(directory: str) -> None:
    """
    Add a directory to Python path if not already there.

    Args:
        directory: Directory to add
    """
    abs_path = os.path.abspath(directory)
    if abs_path not in sys.path:
        sys.path.insert(0, abs_path)


def get_script_dir() -> Path:
    """Get the directory of the current script."""
    return Path(os.path.dirname(os.path.abspath(__file__)))


def join_paths(*paths: str) -> str:
    """Join multiple path components."""
    return os.path.join(*paths)


def path_exists(path: str) -> bool:
    """Check if a path exists."""
    return os.path.exists(path)


def is_file(path: str) -> bool:
    """Check if path is a file."""
    return os.path.isfile(path)


def is_dir(path: str) -> bool:
    """Check if path is a directory."""
    return os.path.isdir(path)


def get_file_size_bytes(filepath: str) -> int:
    """Get file size in bytes."""
    try:
        return os.path.getsize(filepath)
    except OSError:
        return 0
