---
name: error-handling-patterns
description: Resilient architecture and troubleshooting. 2026 Edition.
---

# Error Handling Patterns (Compressed)

## Purpose
Build fault-tolerant applications and provide systematic troubleshooting.

## Capabilities
- **Patterns**: Custom Error classes, Result Types (TS/Rust/Go), Circuit Breakers, Exponential Backoff.
- **Strategy**: Exceptions for unexpected; Result Types for expected (validation).
- **Troubleshooting**: Scientific RCA (Observe -> Hypothesize -> Fix).

## Rules
1. **Fail Fast**: Validate at the edge.
2. **Sanitize**: Never leak stack traces or DB names to clients.
3. **Log RED**: Rate, Errors, Duration metrics integration.