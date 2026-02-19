---
name: detect-duplicate-files
description: Redundancy detection via hashing and vector analysis. 2026 Edition.
---

# Detect Duplicate Files (Compressed)

## Purpose
Identify Content-identical files to reduce redundancy and architectural confusion.

## Logic
1. **Scan**: Recurse through workspace (respecting excludes).
2. **Hash**: Calculate SHA256 per file.
3. **Semantic Verification**: Consult **Central Vector Memory (dude-central-brain)** to distinguish between "Architectural Patterns" (e.g., Hexagonal boilerplate) and junk code.
4. **Action**: Flag non-pattern duplicates for removal.

## Inputs
- `--min-size`: Skip small files.
- `--exclude`: Ignore `node_modules`, `.git`.