#!/usr/bin/env python3
"""
apify-lead-hunter — Sovereign Lead Generation Pipeline
Hunt, score, and persist leads without paid APIs.

Usage:
    python main.py hunt "Agencias inmobiliarias Bilbao" --max 20
    python main.py score leads.json
    python main.py persist scored_leads.json
    python main.py pipeline "Agencias inmobiliarias Bilbao" --max 10
"""

import argparse
import json
import sys


def cmd_hunt(args):
    """Search for leads."""
    from hunter import hunt_leads

    result = hunt_leads(args.query, max_results=args.max)
    output = json.dumps(result, indent=2, ensure_ascii=False)
    print(output)

    if args.output:
        from pathlib import Path
        Path(args.output).write_text(output, encoding="utf-8")

    return 0


def cmd_score(args):
    """Score leads with Ollama."""
    from scorer import score_leads
    from pathlib import Path

    if args.input == "-":
        data = json.load(sys.stdin)
    else:
        data = json.loads(Path(args.input).read_text(encoding="utf-8"))

    leads = data if isinstance(data, list) else data.get("leads", [])
    result = score_leads(leads, model=args.model)
    output = json.dumps(result, indent=2, ensure_ascii=False)
    print(output)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")

    return 0


def cmd_persist(args):
    """Persist leads to Supabase."""
    from persist import persist_leads
    from pathlib import Path

    if args.input == "-":
        data = json.load(sys.stdin)
    else:
        data = json.loads(Path(args.input).read_text(encoding="utf-8"))

    leads = data if isinstance(data, list) else data.get("leads", [])
    result = persist_leads(leads, dry_run=args.dry_run)
    print(json.dumps(result, indent=2))

    return 0 if not result["errors"] else 1


def cmd_pipeline(args):
    """Full pipeline: Hunt → Score → Persist."""
    from hunter import hunt_leads
    from scorer import score_leads
    from persist import persist_leads

    print(f"🔍 Hunting: {args.query} (max {args.max})...", file=sys.stderr)
    hunt_result = hunt_leads(args.query, max_results=args.max)
    leads = hunt_result["leads"]
    print(f"   Found {len(leads)} leads", file=sys.stderr)

    if not leads:
        print(json.dumps({"status": "no_leads_found", "query": args.query}))
        return 0

    print(f"🧠 Scoring {len(leads)} leads with {args.model}...", file=sys.stderr)
    score_result = score_leads(leads, model=args.model)
    scored = score_result["leads"]

    # Filter by minimum score
    qualified = [l for l in scored if l.get("score", 0) >= args.min_score]
    print(f"   {len(qualified)}/{len(scored)} leads scored >= {args.min_score}",
          file=sys.stderr)

    if args.dry_run:
        result = {
            "status": "dry_run",
            "query": args.query,
            "total_found": len(leads),
            "qualified": len(qualified),
            "leads": qualified,
        }
    else:
        print(f"💾 Persisting {len(qualified)} leads...", file=sys.stderr)
        persist_result = persist_leads(qualified)
        result = {
            "status": "completed",
            "query": args.query,
            "total_found": len(leads),
            "qualified": len(qualified),
            "persisted": persist_result["persisted"],
            "duplicates_skipped": persist_result["duplicates_skipped"],
            "leads": qualified,
        }

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


def main():
    parser = argparse.ArgumentParser(
        prog="lead-hunter",
        description="Sovereign Lead Generation Pipeline"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # Hunt
    p_hunt = sub.add_parser("hunt", help="Search for leads")
    p_hunt.add_argument("query", help="Search query")
    p_hunt.add_argument("--max", type=int, default=20, help="Max results")
    p_hunt.add_argument("--output", "-o", default=None)

    # Score
    p_score = sub.add_parser("score", help="Score leads with LLM")
    p_score.add_argument("input", help="JSON file (or - for stdin)")
    p_score.add_argument("--model", default="llama3.1:8b")
    p_score.add_argument("--output", "-o", default=None)

    # Persist
    p_persist = sub.add_parser("persist", help="Save leads to Supabase")
    p_persist.add_argument("input", help="JSON file (or - for stdin)")
    p_persist.add_argument("--dry-run", action="store_true")

    # Pipeline (full)
    p_pipe = sub.add_parser("pipeline", help="Hunt → Score → Persist")
    p_pipe.add_argument("query", help="Search query")
    p_pipe.add_argument("--max", type=int, default=20, help="Max results")
    p_pipe.add_argument("--model", default="llama3.1:8b")
    p_pipe.add_argument("--min-score", type=int, default=50,
                        help="Minimum score to persist (default: 50)")
    p_pipe.add_argument("--dry-run", action="store_true",
                        help="Score but don't persist")

    args = parser.parse_args()
    commands = {
        "hunt": cmd_hunt, "score": cmd_score,
        "persist": cmd_persist, "pipeline": cmd_pipeline,
    }
    return commands[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
