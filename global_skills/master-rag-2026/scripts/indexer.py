#!/usr/bin/env python3
"""
RAG Document Indexer - master-rag-2026
Indexes documents from a directory into Redis Vectors using Ollama embeddings.

Usage:
    python indexer.py /path/to/docs
    python indexer.py /path/to/docs --extensions md txt py
"""

import argparse
import hashlib
import json
import logging
import os
import sys
from pathlib import Path
from typing import List, Tuple

import requests

# Add shared and current dir to path
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT_DIR))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from shared.resilience import setup_logging, retry_with_backoff
    logger = setup_logging("rag-indexer")
except ImportError:
    logger = logging.getLogger(__name__)
    def retry_with_backoff(*args, **kwargs): return lambda f: f

OLLAMA_URL = "http://127.0.0.1:11434/api/embeddings"
EMBED_MODEL = "nomic-embed-text"
REDIS_VSET = "rag_knowledge"
CHUNK_MAX_CHARS = 1000
DEFAULT_EXTENSIONS = {".md", ".txt", ".py", ".yaml", ".yml", ".json"}


@retry_with_backoff(max_retries=3)
def get_embedding(text: str) -> list:
    """Get embedding from local Ollama with retry."""
    prompt = text[:1000] # Safe limit
    try:
        res = requests.post(
            OLLAMA_URL,
            json={"model": EMBED_MODEL, "prompt": prompt},
            timeout=30,
        )
        if res.status_code == 200:
            return res.json().get("embedding", [])
        logger.warning(f"Embedding failed with status {res.status_code}")
    except Exception as e:
        logger.error(f"Embedding error: {e}")
    return []


def chunk_text(text: str, source: str) -> List[Tuple[str, dict]]:
    """
    Split text into chunks by paragraphs, respecting CHUNK_MAX_CHARS.
    Returns list of (chunk_text, metadata) tuples.
    """
    paragraphs = text.split("\n\n")
    chunks = []
    current = ""
    chunk_idx = 0

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        if len(current) + len(para) + 2 > CHUNK_MAX_CHARS and current:
            chunks.append((
                current.strip(),
                {"source": source, "chunk": chunk_idx}
            ))
            chunk_idx += 1
            current = para
        else:
            current = f"{current}\n\n{para}" if current else para

    if current.strip():
        chunks.append((
            current.strip(),
            {"source": source, "chunk": chunk_idx}
        ))

    return chunks


def collect_files(directory: str, extensions: set) -> List[Path]:
    """Collect all indexable files from directory."""
    root = Path(directory)
    if not root.is_dir():
        logger.error(f"Not a directory: {directory}")
        return []

    files = []
    for ext in extensions:
        files.extend(root.rglob(f"*{ext}"))

    # Filter out hidden dirs and __pycache__
    files = [
        f for f in files
        if not any(part.startswith(".") or part == "__pycache__"
                   for part in f.parts)
    ]
    return sorted(files)


def index_directory(
    directory: str,
    extensions: set = None,
    redis_url: str = None,
    dry_run: bool = False,
) -> dict:
    """
    Index all documents from a directory into Redis Vectors.

    Args:
        directory: Path to directory with documents.
        extensions: File extensions to include.
        redis_url: Redis connection URL.
        dry_run: If True, only count chunks without indexing.

    Returns:
        Dict with indexed/skipped/errors counts.
    """
    import redis as redis_sync

    if extensions is None:
        extensions = DEFAULT_EXTENSIONS

    files = collect_files(directory, extensions)
    if not files:
        return {"indexed": 0, "skipped": 0, "errors": [], "files": 0}

    result = {"indexed": 0, "skipped": 0, "errors": [], "files": len(files)}

    # Connect to Redis (sync for simplicity in CLI)
    r = None
    if not dry_run:
        url = redis_url or os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")
        try:
            r = redis_sync.from_url(url, decode_responses=True)
            r.ping()
        except Exception as e:
            return {"indexed": 0, "skipped": 0,
                    "errors": [f"Redis connection failed: {e}"], "files": 0}

    for filepath in files:
        try:
            text = filepath.read_text(encoding="utf-8", errors="ignore")
            if len(text.strip()) < 50:
                result["skipped"] += 1
                continue

            rel_path = str(filepath.relative_to(directory))
            chunks = chunk_text(text, rel_path)

            for chunk_text_str, meta in chunks:
                if dry_run:
                    result["indexed"] += 1
                    continue

                # Generate embedding
                embedding = get_embedding(chunk_text_str)
                if not embedding:
                    result["errors"].append(
                        f"Embedding failed: {rel_path}#chunk{meta['chunk']}"
                    )
                    continue

                # Create unique ID
                doc_id = hashlib.md5(
                    f"{rel_path}:{meta['chunk']}".encode()
                ).hexdigest()

                # Store vector in Redis VectorSet
                # VADD key VALUES <dim> <v1>...<vn> <element_id>
                try:
                    r.execute_command(
                        "VADD", REDIS_VSET, "VALUES",
                        len(embedding), *embedding, doc_id
                    )
                except Exception:
                    # Fallback: try FP32 format
                    try:
                        r.execute_command(
                            "VADD", REDIS_VSET, "FP32",
                            *embedding, doc_id
                        )
                    except Exception as ve:
                        result["errors"].append(f"VADD failed: {ve}")
                        continue

                # Store the text in a hash for retrieval
                r.hset(f"rag_doc:{doc_id}", mapping={
                    "text": chunk_text_str,
                    "source": rel_path,
                    "chunk": str(meta["chunk"]),
                })

                result["indexed"] += 1

        except Exception as e:
            result["errors"].append(f"{filepath}: {e}")

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Index documents into Redis Vectors for RAG"
    )
    parser.add_argument("directory", help="Directory to index")
    parser.add_argument(
        "--extensions", nargs="+", default=None,
        help="File extensions to include (without dot)"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Only count chunks, don't actually index"
    )
    parser.add_argument(
        "--redis-url", default=None,
        help="Redis connection URL"
    )
    args = parser.parse_args()

    extensions = None
    if args.extensions:
        extensions = {f".{e.lstrip('.')}" for e in args.extensions}

    result = index_directory(
        args.directory,
        extensions=extensions,
        redis_url=args.redis_url,
        dry_run=args.dry_run,
    )

    print(json.dumps(result, indent=2))
    return 0 if not result["errors"] else 1


if __name__ == "__main__":
    sys.exit(main())
