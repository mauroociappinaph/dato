---
name: asynchronous-jules-helper
description: Background assistant for heavy refactoring via Jules. 2026 Edition.
---

# Asynchronous Jules Helper (Compressed)

## Purpose
Delegate long-running or repetitive tasks to Jules in isolated containers, maintaining main thread productivity.

## Capabilities
- **Background Execution**: Use `/jules` for multi-file refactoring or documentation generation.
- **State Sync**: MANDATORILY synchronize context via **Central Vector Memory** before delegation.
- **Async Notification**: Alert Owner upon job completion.

## Protocols
1. **Handshake**: Define clear task entry/exit points.
2. **Review**: Present changes for human approval before final merge.

## Usage
1. `/jules [large-scale instruction]` -> 2. Work on other tasks -> 3. Review and merge.