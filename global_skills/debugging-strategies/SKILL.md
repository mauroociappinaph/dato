---
name: debugging-strategies
description: Systematic root cause analysis and profiling. 2026 Edition.
---

# Debugging Strategies (Compressed)

## Purpose
Transform guesswork into systematic problem-solving. Focus on **Root Cause Analysis (RCA)** and autonomous fixing via the **Self-Correction Pilot**.

## Scientific Loop (Actionable)
1. **Observe**: Capture exact error/logs (stderr).
2. **Isolate**: Create minimal reproduction or binary search (`git bisect`).
3. **Hypothesize**: Use `sequentialthinking` to map the failure point.
4. **Fix & Verify**: Apply patch and re-test immediately.

## Language Matrix (Tools)
| Language | Tool / Method | Strategy |
| :--- | :--- | :--- |
| **JS/TS** | `debugger`, `console.table`, `clinic.js` | Profiling & Heap Snapshots. |
| **Python** | `pdb`, `breakpoint()`, `cProfile` | Post-mortem debugging. |
| **Go** | `delve (dlv)`, `pprof` | Memory/CPU profiling. |
| **Shell** | `set -x`, `strace` | Execution tracing. |

## Advanced Patterns
- **Binary Search**: Comment out code halves to find the culprit.
- **Differential Debugging**: Compare working vs broken environments/versions.
- **Race Condition Detection**: Stress test with variable timing.

## Rules (Mandatory)
1. **No Supposition**: Verify every assumption with a log or test.
2. **Data-First**: Always capture stack traces before proposing a fix.
3. **Immunity**: MANDATORILY index the fix in **Central Vector Memory** via **post-mortem-memory**.
