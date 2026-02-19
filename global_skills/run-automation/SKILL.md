---
name: run-automation
description: Safe bridge to execute internal automation scripts from the .gemini/scripts directory.
---

# run-automation

This tool allows AI Agents to execute pre-approved python scripts that reside in the `.gemini/scripts/` directory.
It uses a secure bridge (`bridge_executor.py`) to prevent arbitrary code execution, only allowing scripts explicitly defined in the allowlist.

## Usage

Use this tool when you need to trigger a background process, run a scraper, enrich leads, or perform any "Mechanical" task that has a corresponding script.

### Arguments

- `script_name` (Required): The alias of the script to run.
    - `intel_profiler`: Runs `agent_intel_profiler.py` (Enriches NEW leads)
    - `city_hunter`: Runs `agent_city_hunter.py` (Finds leads in target cities)
    - `contact_finder`: Runs `agent_contact_finder.py` (Finds emails for leads)
    - `sales_hunter`: Runs `agent_sales_hunter.py` (Autonomous Sales Cycle)
    - `dashboard_gen`: Runs `generate_sovereign_dashboard.py` (Rebuilds Streamlit dashboard)
    - `outreach_sentinel`: Runs `outreach_sentinel.py` (Deduplication check)
    - `test_dummy`: Runs `experiments/test_dummy.py` (For verification only)

- `args` (Optional): A string of arguments to pass to the script.
    - Example: `--verbose` or `--limit 10`

## Examples

**1. Trigger Intel Enrichment**
```python
run_automation(script_name="intel_profiler")
```

**2. Run City Hunter for a specific target (if supported by script)**
```python
run_automation(script_name="city_hunter", args="--city 'New York'")
```
