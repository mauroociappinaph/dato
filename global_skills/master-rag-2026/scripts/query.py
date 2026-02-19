#!/usr/bin/env python3
"""
RAG Semantic Query - master-rag-2026
Searches indexed documents using semantic similarity via Redis Vectors.

Usage:
    python query.py "How does the playbook engine work?"
    python query.py "propuesta de valor" --top-k 5
"""

import argparse
import hashlib
import json
import os
import sys
import logging
from pathlib import Path

import requests

# Add shared and current dir to path
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT_DIR))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from shared.resilience import setup_logging, retry_with_backoff
    logger = setup_logging("rag-query")
except ImportError:
    logger = logging.getLogger(__name__)
    def retry_with_backoff(*args, **kwargs): return lambda f: f

OLLAMA_URL = "http://127.0.0.1:11434/api/embeddings"
EMBED_MODEL = "nomic-embed-text"
REDIS_VSET = "rag_knowledge"


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
    except Exception as e:
        logger.warning(f"Embedding error: {e}")
    return []


def check_semantic_cache(r, query: str, threshold: float = 0.95) -> dict | None:
    """Check if a semantically similar query was already answered."""
    cache_key = f"rag_cache:{hashlib.md5(query.encode()).hexdigest()}"
    cached = r.get(cache_key)
    if cached:
        try:
            return json.loads(cached)
        except (json.JSONDecodeError, TypeError):
            pass
    return None


def set_semantic_cache(r, query: str, results: list, ttl: int = 86400):
    """Cache query results for 24h."""
    cache_key = f"rag_cache:{hashlib.md5(query.encode()).hexdigest()}"
    r.setex(cache_key, ttl, json.dumps(results, ensure_ascii=False))


def semantic_query(
    query: str,
    top_k: int = 3,
    redis_url: str = None,
    use_cache: bool = True,
) -> dict:
    """
    Perform semantic search against indexed documents.

    Args:
        query: Natural language query.
        top_k: Number of results to return.
        redis_url: Redis connection URL.
        use_cache: Whether to check/store cache.

    Returns:
        Dict with results and metadata.
    """
    import redis as redis_sync

    url = redis_url or os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")
    try:
        r = redis_sync.from_url(url, decode_responses=True)
        r.ping()
    except Exception as e:
        return {"results": [], "error": f"Redis connection failed: {e}",
                "from_cache": False}

    # Check cache first
    if use_cache:
        cached = check_semantic_cache(r, query)
        if cached:
            return {"results": cached, "from_cache": True, "query": query}

    # Generate query embedding
    embedding = get_embedding(query)
    if not embedding:
        return {"results": [], "error": "Failed to generate embedding",
                "from_cache": False}

    # Search Redis VectorSet
    try:
        raw = r.execute_command(
            "VSIM", REDIS_VSET, "VALUES",
            len(embedding), *embedding,
            "WITHSCORES", "COUNT", top_k
        )
    except Exception as e:
        return {"results": [], "error": f"VSIM failed: {e}",
                "from_cache": False}

    # Parse results — VSIM returns [id1, score1, id2, score2, ...]
    results = []
    if raw and isinstance(raw, list):
        i = 0
        while i < len(raw) - 1:
            doc_id = raw[i] if isinstance(raw[i], str) else raw[i].decode()
            score = float(raw[i + 1]) if not isinstance(raw[i + 1], float) else raw[i + 1]
            i += 2

            # Retrieve the document text
            doc_data = r.hgetall(f"rag_doc:{doc_id}")
            if doc_data:
                results.append({
                    "text": doc_data.get("text", ""),
                    "source": doc_data.get("source", "unknown"),
                    "chunk": int(doc_data.get("chunk", 0)),
                    "score": round(score, 4),
                })

    # Cache results
    if use_cache and results:
        set_semantic_cache(r, query, results)

    return {"results": results, "from_cache": False, "query": query}


def main():
    parser = argparse.ArgumentParser(
        description="Semantic search against indexed RAG documents"
    )
    parser.add_argument("query", help="Natural language query")
    parser.add_argument(
        "--top-k", type=int, default=3,
        help="Number of results (default: 3)"
    )
    parser.add_argument(
        "--no-cache", action="store_true",
        help="Skip cache lookup"
    )
    parser.add_argument(
        "--redis-url", default=None,
        help="Redis connection URL"
    )
    args = parser.parse_args()

    result = semantic_query(
        args.query,
        top_k=args.top_k,
        redis_url=args.redis_url,
        use_cache=not args.no_cache,
    )

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if "error" not in result else 1


if __name__ == "__main__":
    sys.exit(main())
