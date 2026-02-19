---
name: context7-docs-engine
description: External API documentation synthesis via MCP. 2026 Edition.
---

# Documentation Engine (Compressed)

## Purpose
Ensure agents use current, best-practice API versions. Prevent obsolescence.

## Responsibilities
1. **Search (MCP-First)**: Use servers like Open-Aware to find official docs.
2. **Version Check**: Cross-reference with `package.json` / `requirements.txt`.
3. **Synthesis**: Reduce thousands of pages to executable 1-2 page summaries.
4. **Snippets**: Extract "best-practice" code for implementations.

## Trigger
Contextualization phase of the Dude Pipeline.