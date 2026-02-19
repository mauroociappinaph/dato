"""
Validation utilities for Global Skills.

Common validation functions used across multiple skills.
"""

import re
from pathlib import Path
from typing import List, Dict, Any, Optional


def validate_skill_name(name: str) -> tuple[bool, Optional[str]]:
    """
    Validate a skill name.

    Skill names should be:
    - Lowercase
    - Use hyphens as separators
    - Start with a letter
    - Contain only alphanumeric characters and hyphens

    Args:
        name: Skill name to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not name:
        return False, "Skill name cannot be empty"

    if not re.match(r'^[a-z][a-z0-9-]*$', name):
        return False, (
            "Skill name must start with a letter, contain only lowercase "
            "letters, numbers, and hyphens"
        )

    if '--' in name:
        return False, "Skill name cannot contain consecutive hyphens"

    if name.endswith('-'):
        return False, "Skill name cannot end with a hyphen"

    if len(name) > 50:
        return False, "Skill name must be 50 characters or less"

    return True, None


def validate_skill_inputs(inputs: Dict[str, Any], schema: Dict[str, Any]) -> List[str]:
    """
    Validate skill inputs against a schema.

    Args:
        inputs: Input dictionary to validate
        schema: JSON schema for validation

    Returns:
        List of validation error messages
    """
    errors = []

    # Check required fields
    required = schema.get("required", [])
    for field in required:
        if field not in inputs:
            errors.append(f"Missing required field: {field}")

    # Check property types
    properties = schema.get("properties", {})
    for field, value in inputs.items():
        if field in properties:
            expected_type = properties[field].get("type")
            if expected_type and not _check_type(value, expected_type):
                errors.append(
                    f"Field '{field}' should be of type {expected_type}, "
                    f"got {type(value).__name__}"
                )

        # Check enum values
        if field in properties and "enum" in properties[field]:
            allowed = properties[field]["enum"]
            if value not in allowed:
                errors.append(
                    f"Field '{field}' must be one of {allowed}, got {value}"
                )

    return errors


def _check_type(value: Any, expected_type: str) -> bool:
    """Check if value matches expected type."""
    type_map = {
        "string": str,
        "integer": int,
        "number": (int, float),
        "boolean": bool,
        "array": list,
        "object": dict,
    }

    if expected_type not in type_map:
        return True  # Unknown type, assume valid

    return isinstance(value, type_map[expected_type])


def validate_file_exists(file_path: str, file_type: str = "file") -> tuple[bool, Optional[str]]:
    """
    Validate that a file exists.

    Args:
        file_path: Path to validate
        file_type: Type of file for error messages

    Returns:
        Tuple of (is_valid, error_message)
    """
    path = Path(file_path)

    if not path.exists():
        return False, f"{file_type.capitalize()} not found: {file_path}"

    if file_type == "file" and not path.is_file():
        return False, f"Path is not a file: {file_path}"

    if file_type == "directory" and not path.is_dir():
        return False, f"Path is not a directory: {file_path}"

    return True, None


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename for safe use.

    Args:
        filename: Original filename

    Returns:
        Sanitized filename
    """
    # Replace spaces with underscores
    sanitized = filename.replace(" ", "_")

    # Remove unsafe characters
    sanitized = re.sub(r'[<>:"/\\|?*]', "", sanitized)

    # Limit length
    if len(sanitized) > 100:
        name, ext = Path(sanitized).stem, Path(sanitized).suffix
        sanitized = name[:100 - len(ext)] + ext

    return sanitized


def validate_cost_limit(estimated_cost: float, limit: Optional[float]) -> tuple[bool, Optional[str]]:
    """
    Validate that estimated cost is within limit.

    Args:
        estimated_cost: Estimated cost of execution
        limit: Maximum allowed cost (None = no limit)

    Returns:
        Tuple of (is_valid, error_message)
    """
    if limit is None:
        return True, None

    if estimated_cost > limit:
        return False, (
            f"Estimated cost ${estimated_cost:.4f} exceeds limit ${limit:.4f}"
        )

    return True, None


def validate_version(version: str) -> tuple[bool, Optional[str]]:
    """
    Validate semantic version string.

    Args:
        version: Version string (e.g., "1.2.3")

    Returns:
        Tuple of (is_valid, error_message)
    """
    pattern = r'^\d+\.\d+\.\d+(-[a-zA-Z0-9.-]+)?(\+[a-zA-Z0-9.-]+)?$'

    if not re.match(pattern, version):
        return False, "Version must follow semantic versioning (e.g., 1.2.3)"

    return True, None
