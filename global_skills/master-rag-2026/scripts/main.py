#!/usr/bin/env python3
"""
master-rag-2026 — Solution-RAG CLI
Index documents and query semantically via Redis Vectors + Ollama.

Usage:
    python main.py index /path/to/docs
    python main.py index /path/to/docs --extensions md txt --dry-run
    python main.py query "¿Cuál es la propuesta de valor?"
    python main.py query "lead generation" --top-k 5
    python main.py stats
"""

import argparse
import json
import os
import sys


def cmd_index(args):
    """Index documents from a directory."""
    from indexer import index_directory

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
    return 0 if not result.get("errors") else 1


def cmd_query(args):
    """Query indexed documents semantically."""
    from query import semantic_query

    result = semantic_query(
        args.query_text,
        top_k=args.top_k,
        redis_url=args.redis_url,
        use_cache=not args.no_cache,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if "error" not in result else 1


def cmd_stats(args):
    """Show index statistics."""
    import redis as redis_sync

    url = args.redis_url or os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")
    try:
        r = redis_sync.from_url(url, decode_responses=True)
        r.ping()
    except Exception as e:
        print(json.dumps({"error": f"Redis connection failed: {e}"}))
        return 1

    # Count documents in hash namespace
    doc_keys = list(r.scan_iter(match="rag_doc:*", count=100))
    cache_keys = list(r.scan_iter(match="rag_cache:*", count=100))

    # Check if VectorSet exists
    vset_exists = False
    try:
        r.execute_command("VCARD", "rag_knowledge")
        vset_exists = True
    except Exception:
        pass

    stats = {
        "vectorset_exists": vset_exists,
        "indexed_chunks": len(doc_keys),
        "cached_queries": len(cache_keys),
    }
    print(json.dumps(stats, indent=2))
    return 0


def main():
    parser = argparse.ArgumentParser(
        prog="master-rag-2026",
        description="Solution-RAG: Index and query documents semantically"
    )
    parser.add_argument(
        "--redis-url", default=None,
        help="Redis connection URL"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # Index subcommand
    p_index = sub.add_parser("index", help="Index documents from a directory")
    p_index.add_argument("directory", help="Directory to index")
    p_index.add_argument("--extensions", nargs="+", default=None,
                         help="File extensions (without dot)")
    p_index.add_argument("--dry-run", action="store_true",
                         help="Count chunks without indexing")

    # Query subcommand
    p_query = sub.add_parser("query", help="Semantic search")
    p_query.add_argument("query_text", help="Natural language query")
    p_query.add_argument("--top-k", type=int, default=3,
                         help="Number of results")
    p_query.add_argument("--no-cache", action="store_true",
                         help="Skip cache")

    # Stats subcommand
    sub.add_parser("stats", help="Show index statistics")

    args = parser.parse_args()

    commands = {"index": cmd_index, "query": cmd_query, "stats": cmd_stats}
    return commands[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
