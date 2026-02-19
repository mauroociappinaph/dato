#!/usr/bin/env python3
"""
Lead Persister - apify-lead-hunter
Persists scored leads to Supabase with deduplication.

Usage:
    python persist.py scored_leads.json
    cat scored.json | python persist.py -
"""

import argparse
import json
import logging
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# Add shared and current dir to path
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT_DIR))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from shared.resilience import setup_logging, retry_with_backoff
    logger = setup_logging("lead-persister")
except ImportError:
    logger = logging.getLogger(__name__)
    def retry_with_backoff(*args, **kwargs): return lambda f: f


def get_supabase_client():
    """Get Supabase client from environment."""
    try:
        from supabase import create_client
    except ImportError:
        logger.error("supabase-py not installed. Run: pip install supabase")
        return None

    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_ANON_KEY") or os.getenv("SUPABASE_KEY")

    if not url or not key:
        logger.error("SUPABASE_URL and SUPABASE_ANON_KEY must be set")
        return None

    return create_client(url, key)


@retry_with_backoff(max_retries=3)
def check_duplicate(client, url: str) -> bool:
    """Check if a lead with this URL already exists."""
    try:
        result = client.table("leads").select("id").eq("url", url).execute()
        return len(result.data) > 0
    except Exception as e:
        logger.error(f"Dedup check failed: {e}")
        raise e


def persist_leads(leads: list[dict], dry_run: bool = False) -> dict:
    """
    Persist leads to Supabase with deduplication.

    Args:
        leads: List of scored lead dicts.
        dry_run: If True, only check duplicates without inserting.

    Returns:
        Dict with persisted/duplicates_skipped counts.
    """
    result = {
        "persisted": 0,
        "duplicates_skipped": 0,
        "errors": [],
    }

    if dry_run:
        result["dry_run"] = True
        result["would_persist"] = len(leads)
        return result

    client = get_supabase_client()
    if not client:
        result["errors"].append("Supabase client not available")
        return result

    for lead in leads:
        url = lead.get("url", "")

        # Deduplication by URL
        if url and check_duplicate(client, url):
            result["duplicates_skipped"] += 1
            continue

        # Prepare record
        record = {
            "name": lead.get("name", "Unknown")[:255],
            "url": url[:500] if url else None,
            "snippet": lead.get("snippet", "")[:1000],
            "score": lead.get("score", 0),
            "reasoning": lead.get("reasoning", "")[:500],
            "status": "NEW",
            "source": "duckduckgo",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

        try:
            client.table("leads").insert(record).execute()
            result["persisted"] += 1
        except Exception as e:
            result["errors"].append(f"Insert failed for {url}: {e}")

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Persist scored leads to Supabase"
    )
    parser.add_argument("input", help="JSON file with scored leads (or - for stdin)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Only check duplicates, don't insert")
    args = parser.parse_args()

    # Load leads
    if args.input == "-":
        data = json.load(sys.stdin)
    else:
        data = json.loads(Path(args.input).read_text(encoding="utf-8"))

    leads = data if isinstance(data, list) else data.get("leads", [])

    result = persist_leads(leads, dry_run=args.dry_run)
    print(json.dumps(result, indent=2))

    return 0 if not result["errors"] else 1


if __name__ == "__main__":
    sys.exit(main())
