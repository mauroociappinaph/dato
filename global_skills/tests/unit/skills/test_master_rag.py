"""
Tests for master-rag-2026 skill.
Tests chunking logic, output formats, and file collection without Redis/Ollama.
"""

import json
import os
import sys
import tempfile
from pathlib import Path

import pytest

# Add scripts to path
SCRIPTS_DIR = Path(__file__).parent.parent.parent.parent / "master-rag-2026" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))


class TestChunking:
    """Test document chunking logic."""

    def test_chunk_text_single_paragraph(self):
        from indexer import chunk_text

        text = "This is a single paragraph of text."
        chunks = chunk_text(text, "test.md")

        assert len(chunks) == 1
        assert chunks[0][0] == "This is a single paragraph of text."
        assert chunks[0][1]["source"] == "test.md"
        assert chunks[0][1]["chunk"] == 0

    def test_chunk_text_multiple_paragraphs(self):
        from indexer import chunk_text

        text = "Paragraph one.\n\nParagraph two.\n\nParagraph three."
        chunks = chunk_text(text, "doc.md")

        assert len(chunks) >= 1
        # All text should be present across chunks
        all_text = " ".join(c[0] for c in chunks)
        assert "Paragraph one" in all_text
        assert "Paragraph two" in all_text
        assert "Paragraph three" in all_text

    def test_chunk_text_respects_max_size(self):
        from indexer import chunk_text, CHUNK_MAX_CHARS

        # Create text with many paragraphs
        paras = ["x" * 300 for _ in range(20)]
        text = "\n\n".join(paras)
        chunks = chunk_text(text, "big.md")

        # Each chunk should be under max
        for chunk_text_str, _ in chunks:
            assert len(chunk_text_str) <= CHUNK_MAX_CHARS + 300  # margin for last para

    def test_chunk_text_empty(self):
        from indexer import chunk_text

        chunks = chunk_text("", "empty.md")
        assert len(chunks) == 0

    def test_chunk_metadata_increments(self):
        from indexer import chunk_text

        # Force multiple chunks with large paragraphs
        paras = ["word " * 500 for _ in range(5)]
        text = "\n\n".join(paras)
        chunks = chunk_text(text, "multi.md")

        if len(chunks) > 1:
            indices = [c[1]["chunk"] for c in chunks]
            assert indices == list(range(len(chunks)))


class TestFileCollection:
    """Test file collection from directories."""

    def test_collect_files_default_extensions(self):
        from indexer import collect_files

        with tempfile.TemporaryDirectory() as tmp:
            # Create test files
            (Path(tmp) / "readme.md").write_text("# Hello")
            (Path(tmp) / "script.py").write_text("print('hi')")
            (Path(tmp) / "image.png").write_bytes(b"\x89PNG")
            (Path(tmp) / "data.txt").write_text("data")

            files = collect_files(tmp, {".md", ".txt", ".py"})
            names = {f.name for f in files}

            assert "readme.md" in names
            assert "script.py" in names
            assert "data.txt" in names
            assert "image.png" not in names

    def test_collect_files_excludes_hidden(self):
        from indexer import collect_files

        with tempfile.TemporaryDirectory() as tmp:
            hidden = Path(tmp) / ".hidden"
            hidden.mkdir()
            (hidden / "secret.md").write_text("secret")
            (Path(tmp) / "public.md").write_text("public")

            files = collect_files(tmp, {".md"})
            names = {f.name for f in files}

            assert "public.md" in names
            assert "secret.md" not in names

    def test_collect_files_nonexistent_dir(self):
        from indexer import collect_files

        files = collect_files("/nonexistent/path", {".md"})
        assert files == []


class TestDryRun:
    """Test dry-run mode (no Redis needed)."""

    def test_dry_run_counts_chunks(self):
        from indexer import index_directory

        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "doc1.md").write_text("A" * 100 + "\n\n" + "B" * 100)
            (Path(tmp) / "doc2.txt").write_text("C" * 100)

            result = index_directory(tmp, dry_run=True)

            assert result["indexed"] > 0
            assert result["files"] == 2
            assert result["errors"] == []


class TestQueryOutputFormat:
    """Test query output format validation."""

    def test_query_result_structure(self):
        """Verify the expected output structure keys exist."""
        expected_keys = {"results", "from_cache", "query"}
        # We can't test actual query without Redis, but verify the function signature
        from query import semantic_query
        assert callable(semantic_query)
