"""
Unit tests for src/helpers module.
"""

import os
from pathlib import Path

import pytest

# Mark all tests in this file as unit tests
pytestmark = pytest.mark.unit


class TestSystemUtils:
    """Tests for system_utils helper functions."""

    def test_path_exists_with_existing_file(self, tmp_path):
        """Test path_exists returns True for existing file."""
        from src.helpers import path_exists

        test_file = tmp_path / "test.txt"
        test_file.write_text("test")

        assert path_exists(str(test_file)) is True

    def test_path_exists_with_nonexistent_file(self, tmp_path):
        """Test path_exists returns False for nonexistent file."""
        from src.helpers import path_exists

        nonexistent = tmp_path / "nonexistent.txt"

        assert path_exists(str(nonexistent)) is False

    def test_ensure_dir_creates_directory(self, tmp_path):
        """Test ensure_dir creates directory."""
        from src.helpers import ensure_dir

        new_dir = tmp_path / "new_directory"
        ensure_dir(str(new_dir))

        assert new_dir.exists()
        assert new_dir.is_dir()

    def test_join_paths(self):
        """Test join_paths joins paths correctly."""
        from src.helpers import join_paths

        result = join_paths("path", "to", "file")
        assert result == os.path.join("path", "to", "file")


class TestValidationUtils:
    """Tests for validation_utils helper functions."""

    def test_validate_skill_name_valid(self):
        """Test validate_skill_name with valid name."""
        from src.helpers import validate_skill_name

        # Should not raise
        validate_skill_name("valid-skill-name")
        validate_skill_name("another_valid_name")

    def test_validate_skill_name_invalid(self):
        """Test validate_skill_name with invalid name."""
        from src.helpers import validate_skill_name

        with pytest.raises(ValueError):
            validate_skill_name("")

        with pytest.raises(ValueError):
            validate_skill_name("   ")

    def test_validate_file_exists(self, tmp_path):
        """Test validate_file_exists."""
        from src.helpers import validate_file_exists

        test_file = tmp_path / "test.txt"
        test_file.write_text("test")

        # Should not raise
        validate_file_exists(str(test_file))

    def test_validate_file_exists_not_found(self, tmp_path):
        """Test validate_file_exists raises for missing file."""
        from src.helpers import validate_file_exists

        with pytest.raises(FileNotFoundError):
            validate_file_exists(str(tmp_path / "nonexistent.txt"))


class TestFileUtils:
    """Tests for file_utils helper functions."""

    def test_load_json_file(self, tmp_path):
        """Test load_json_file."""
        from src.helpers import load_json_file

        test_file = tmp_path / "test.json"
        test_file.write_text('{"key": "value"}')

        result = load_json_file(str(test_file))
        assert result == {"key": "value"}

    def test_save_json_file(self, tmp_path):
        """Test save_json_file."""
        from src.helpers import save_json_file

        test_file = tmp_path / "test.json"
        data = {"key": "value"}

        save_json_file(str(test_file), data)

        assert test_file.exists()
        content = test_file.read_text()
        assert '"key": "value"' in content

    def test_get_file_size(self, tmp_path):
        """Test get_file_size returns correct size."""
        from src.helpers import get_file_size

        test_file = tmp_path / "test.txt"
        test_file.write_text("Hello, World!")

        size = get_file_size(str(test_file))
        assert size > 0


class TestHttpUtils:
    """Tests for http_utils helper functions."""

    def test_validate_url_valid(self):
        """Test validate_url with valid URLs."""
        from src.helpers import validate_url

        # Should not raise
        validate_url("https://example.com")
        validate_url("http://localhost:8080")

    def test_validate_url_invalid(self):
        """Test validate_url with invalid URLs."""
        from src.helpers import validate_url

        with pytest.raises(ValueError):
            validate_url("not-a-url")

        with pytest.raises(ValueError):
            validate_url("")

    def test_parse_json_response_valid(self):
        """Test parse_json_response with valid JSON."""
        from src.helpers import parse_json_response

        result = parse_json_response('{"key": "value"}')
        assert result == {"key": "value"}

    def test_parse_json_response_invalid(self):
        """Test parse_json_response with invalid JSON."""
        from src.helpers import parse_json_response

        with pytest.raises(ValueError):
            parse_json_response("not valid json")
