---
name: langgraph-director
description: Multi-agent orchestration and graph state persistence. 2026 Edition.
---

# LangGraph Director (Compressed)

## Purpose
Orchestrate task flow between specialized agents using state machines.

## Logic & Sync
- **State**: Use LangGraph for transitions (e.g., Security -> Backend).
- **Blackboard**: Use **Redis** for immediate shared memory.
- **Historical Sync**: MANDATORILY sync significant decision nodes with **Central Vector Memory (dude-central-brain)**.
- **Parallelism**: Manage simultaneous workflows across departments.

## Trigger
Multi-step, cross-departmental requests.