"""
Helper utilities for Global Skills.

Reusable functions for common operations across all skills.
"""

from .file_utils import (
    read_skill_file,
    write_skill_file,
    list_skill_files,
    ensure_directory,
    copy_skill_template,
    load_json_file,
    save_json_file,
    load_yaml_file,
    save_yaml_file,
    get_file_size,
    get_line_count,
)

from .validation_utils import (
    validate_skill_name,
    validate_skill_inputs,
    validate_file_exists,
    sanitize_filename,
)

from .http_utils import (
    make_request,
    make_request_with_retry,
    validate_url,
    parse_json_response,
    fetch_with_auth,
)

from .system_utils import (
    get_env_var,
    get_env_int,
    get_env_bool,
    ensure_dir,
    get_project_root,
    get_skill_dir,
    list_python_files,
    read_file_lines,
    get_file_line_count,
    get_relative_path,
    walk_directory,
    add_to_python_path,
    get_script_dir,
    join_paths,
    path_exists,
    is_file,
    is_dir,
    get_file_size_bytes,
)

__all__ = [
    # File utilities
    "read_skill_file",
    "write_skill_file",
    "list_skill_files",
    "ensure_directory",
    "copy_skill_template",
    "load_json_file",
    "save_json_file",
    "load_yaml_file",
    "save_yaml_file",
    "get_file_size",
    "get_line_count",
    # Validation utilities
    "validate_skill_name",
    "validate_skill_inputs",
    "validate_file_exists",
    "sanitize_filename",
    # HTTP utilities
    "make_request",
    "make_request_with_retry",
    "validate_url",
    "parse_json_response",
    "fetch_with_auth",
    # System utilities
    "get_env_var",
    "get_env_int",
    "get_env_bool",
    "ensure_dir",
    "get_project_root",
    "get_skill_dir",
    "list_python_files",
    "read_file_lines",
    "get_file_line_count",
    "get_relative_path",
    "walk_directory",
    "add_to_python_path",
    "get_script_dir",
    "join_paths",
    "path_exists",
    "is_file",
    "is_dir",
    "get_file_size_bytes",
]
