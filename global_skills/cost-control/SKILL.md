---
name: cost-control
description: Rate limiting, quota tracking, and fallback policies for premium MCP servers to optimize costs.
---

# Cost Control

## Purpose
Manages usage quotas and implements intelligent fallback policies for premium MCP servers to prevent cost overruns while maintaining service quality.

## Capabilities
- **Rate Limiting**: Per-agent, per-server quotas
- **Usage Tracking**: Real-time cost monitoring
- **Fallback Policies**: Automatic switching to cost-effective alternatives
- **Reporting**: Daily/weekly usage reports

## Usage

```python
from cost_control.mcp_cost_controller import MCPCostController

controller = MCPCostController()

# Check if agent can use a premium server
if await controller.check_quota('exa', 'AGENT_SALES'):
    # Proceed with exa
    result = await use_exa(query)
    await controller.record_usage('exa', 'AGENT_SALES', cost=0.01)
else:
    # Use fallback
    result = await use_duckduckgo(query)
```

## Files
- `scripts/mcp_cost_controller.py`: Main controller
- `fallback_policies.json`: Fallback configuration
