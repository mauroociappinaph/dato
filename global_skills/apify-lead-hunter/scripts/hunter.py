#!/usr/bin/env python3
"""
Lead Hunter - apify-lead-hunter (Sovereign Edition)
Searches for business leads using DuckDuckGo LITE (no API key needed).

Usage:
    python hunter.py "Agencias inmobiliarias Bilbao" --max 20
"""

import argparse
import json
import logging
import sys
import time
import os
from urllib.parse import quote_plus
from pathlib import Path

import requests
from bs4 import BeautifulSoup

# Add shared and current dir to path
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT_DIR))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from shared.resilience import setup_logging, retry_with_backoff
    logger = setup_logging("lead-hunter")
except ImportError:
    logger = logging.getLogger(__name__)
    def retry_with_backoff(*args, **kwargs): return lambda f: f

DDG_URL = "https://lite.duckduckgo.com/lite/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
}


@retry_with_backoff(max_retries=3)
def search_duckduckgo(query: str, max_results: int = 20) -> list[dict]:
    """
    Search DuckDuckGo LITE and parse results.
    Returns list of {name, url, snippet}.
    """
    results = []

    try:
        res = requests.post(
            DDG_URL,
            data={"q": query, "kl": "es-es"},
            headers=HEADERS,
            timeout=15,
        )
        if res.status_code != 200:
            logger.error(f"DuckDuckGo returned {res.status_code}")
            raise Exception(f"HTTP {res.status_code}")

        soup = BeautifulSoup(res.text, "html.parser")

        # DuckDuckGo LITE uses a table layout
        # Results are in <a class="result-link"> or similar
        links = soup.find_all("a", class_="result-link")

        if not links:
            # Fallback: parse table rows
            rows = soup.find_all("tr")
            for row in rows:
                link = row.find("a")
                if link and link.get("href", "").startswith("http"):
                    url = link["href"]
                    name = link.get_text(strip=True)
                    # Find snippet in next sibling
                    snippet_td = row.find("td", class_="result-snippet")
                    snippet = snippet_td.get_text(strip=True) if snippet_td else ""

                    if name and url and "duckduckgo.com" not in url:
                        results.append({
                            "name": name,
                            "url": url,
                            "snippet": snippet,
                        })
                        if len(results) >= max_results:
                            break
        else:
            for link in links:
                url = link.get("href", "")
                name = link.get_text(strip=True)
                if name and url and "duckduckgo.com" not in url:
                    results.append({
                        "name": name,
                        "url": url,
                        "snippet": "",
                    })
                if len(results) >= max_results:
                    break

    except Exception as e:
        logger.error(f"Search failed: {e}")

    # Deduplicate by URL
    seen = set()
    unique = []
    for r in results:
        if r["url"] not in seen:
            seen.add(r["url"])
            unique.append(r)

    return unique[:max_results]


def hunt_leads(query: str, max_results: int = 20) -> dict:
    """
    Hunt for leads using DuckDuckGo.

    Args:
        query: Search query (e.g., "Agencias inmobiliarias Bilbao")
        max_results: Maximum number of leads to return.

    Returns:
        Dict with leads_found count and leads list.
    """
    leads = search_duckduckgo(query, max_results)

    return {
        "query": query,
        "leads_found": len(leads),
        "leads": leads,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Hunt for business leads using DuckDuckGo"
    )
    parser.add_argument("query", help="Search query")
    parser.add_argument("--max", type=int, default=20,
                        help="Max results (default: 20)")
    parser.add_argument("--output", "-o", default=None,
                        help="Save to JSON file")
    args = parser.parse_args()

    result = hunt_leads(args.query, max_results=args.max)
    output = json.dumps(result, indent=2, ensure_ascii=False)
    print(output)

    if args.output:
        from pathlib import Path
        Path(args.output).write_text(output, encoding="utf-8")

    return 0


if __name__ == "__main__":
    sys.exit(main())
