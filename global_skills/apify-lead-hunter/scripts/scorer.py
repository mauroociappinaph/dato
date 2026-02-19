#!/usr/bin/env python3
"""
Lead Scorer - apify-lead-hunter
Scores leads using local Ollama LLM (sovereign, $0).

Usage:
    python scorer.py leads.json
    python scorer.py leads.json --model llama3.1:8b --output scored.json
    cat leads.json | python scorer.py -
"""

import argparse
import json
import logging
import os
import sys
from pathlib import Path

import requests

# Add shared and current dir to path
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT_DIR))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from shared.resilience import setup_logging, retry_with_backoff, safe_ollama_call
    logger = setup_logging("lead-scorer")
except ImportError:
    logger = logging.getLogger(__name__)
    def retry_with_backoff(*args, **kwargs): return lambda f: f
    def safe_ollama_call(url, prompt, model, timeout=60):
        res = requests.post(url, json={"model": model, "prompt": prompt, "stream": False}, timeout=timeout)
        return res.json() if res.status_code == 200 else {"error": "http error"}

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
DEFAULT_MODEL = "llama3.1:8b"


@retry_with_backoff(max_retries=3)
def score_lead(lead: dict, model: str = DEFAULT_MODEL) -> dict:
    """
    Score a single lead using Ollama.
    Returns the lead dict with added 'score' and 'reasoning' fields.
    """
    name = lead.get("name", "Unknown")
    url = lead.get("url", "")
    snippet = lead.get("snippet", "")

    prompt = f"""You are a B2B lead scoring agent for an AI services company.
Score this lead from 0 to 100 based on:
- Relevance to B2B services (technology, marketing, consulting, real estate)
- Likely company size and budget
- Digital presence signals
- Potential need for AI/automation

Output ONLY a JSON object: {{"score": <0-100>, "reasoning": "<one sentence>"}}

Lead:
- Name: {name}
- URL: {url}
- Description: {snippet}

JSON:"""

    result = safe_ollama_call(OLLAMA_URL, prompt, model)

    if "error" in result:
        lead["score"] = 0
        lead["reasoning"] = f"Error: {result['error']}"
        return lead

    response = result.get("response", "").strip()

    try:
        # Handle cases where LLM wraps in markdown
        clean = response
        if "```" in clean:
            clean = clean.split("```")[1]
            if clean.startswith("json"):
                clean = clean[4:]
        # Find JSON object
        start = clean.find("{")
        end = clean.rfind("}") + 1
        if start >= 0 and end > start:
            parsed = json.loads(clean[start:end])
            lead["score"] = min(100, max(0, int(parsed.get("score", 0))))
            lead["reasoning"] = parsed.get("reasoning", "No reasoning provided")
            return lead
    except (json.JSONDecodeError, ValueError):
        pass

    # Fallback: score 50 if parsing fails
    lead["score"] = 50
    lead["reasoning"] = "Scoring failed — default score assigned"
    return lead


def score_leads(leads: list[dict], model: str = DEFAULT_MODEL) -> dict:
    """
    Score a batch of leads.

    Returns:
        Dict with scored count and leads list.
    """
    scored = []
    for lead in leads:
        scored_lead = score_lead(lead, model)
        scored.append(scored_lead)

    # Sort by score descending
    scored.sort(key=lambda x: x.get("score", 0), reverse=True)

    return {
        "scored": len(scored),
        "model": model,
        "leads": scored,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Score leads using local Ollama LLM"
    )
    parser.add_argument("input", help="JSON file with leads (or - for stdin)")
    parser.add_argument("--model", default=DEFAULT_MODEL,
                        help=f"Ollama model (default: {DEFAULT_MODEL})")
    parser.add_argument("--output", "-o", default=None,
                        help="Save to JSON file")
    args = parser.parse_args()

    # Load leads
    if args.input == "-":
        data = json.load(sys.stdin)
    else:
        # Allow reading from scored_test.json or leads_test.json
        try:
            data = json.loads(Path(args.input).read_text(encoding="utf-8"))
        except Exception as e:
            logger.error(f"Failed to read input file: {e}")
            return 1

    # Accept both raw list and {"leads": [...]} format
    leads = data if isinstance(data, list) else data.get("leads", [])

    result = score_leads(leads, model=args.model)
    output = json.dumps(result, indent=2, ensure_ascii=False)
    print(output)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")

    return 0


if __name__ == "__main__":
    sys.exit(main())
