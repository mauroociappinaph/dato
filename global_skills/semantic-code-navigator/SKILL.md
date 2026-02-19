---
name: semantic-code-navigator
description: A high-efficiency replacement for 'read_file'. It understands code structure (classes, functions) and reads only what is necessary, saving tokens and time.
---

# Semantic Code Navigator

## Role
The "Code Cartographer" that provides surgical context instead of dumping raw file content. It is designed to replace sequential file reading with structural analysis.

## Core Directives
1. **Never read the whole file first:** Always start by listing the structure (functions/classes).
2. **Surgical Reading:** Use line numbers to extract only the relevant function body.
3. **Dependency Mapping:** Understand imports and exports to follow the logic flow across files.

## How to use
1. **Map Phase:** Call `scripts/code_nav.py --map [file/dir]` to see the table of contents.
2. **Extract Phase:** Call `scripts/code_nav.py --extract [symbol] [file]` to read only that part.
3. **Search Phase:** Use structural search to find where a logic pattern is implemented.

## Benefits
- **Token Economy:** Up to 80% reduction in tokens per task.
- **Speed:** Instant structure overview without parsing multi-megabyte files.
- **Precision:** Focus on logic, not boilerplate.
