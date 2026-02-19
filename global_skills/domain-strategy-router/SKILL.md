# Domain Strategy Router (High-Speed Triage)

## Purpose
Reduce orchestration latency by implementing a 3-layer filtering system. Act as the "Load Balancer" of the Sovereign Agent Cloud.

## Triage Layers (2026)
1. **Layer 1: Departmental Filter**: Identify which of the 8 departments handles the task (Core, Engineering, Quality, Ops, Security, Data, Product, Comms).
2. **Layer 2: Semantic Pre-selection**: Query **Central Vector Memory (dude-central-brain)** to retrieve only the Top 3 specialists from the selected department.
3. **Layer 3: Hot-Path Cache**: Check **Redis** for previous identical task-to-agent mappings to achieve zero-latency routing.

## Responsibilities
- **Dynamic Routing**: Discard irrelevant agents immediately based on departmental scope.
- **Rule Injection**: Load specific quality gates only for the filtered Top 3 specialists.
- **Efficiency**: Report "Orchestration Latency" to the **Financial-Controller**.

## Trigger
Step 4.5 of the Dude Pipeline.