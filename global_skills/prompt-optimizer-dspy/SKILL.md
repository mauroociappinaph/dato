---
name: prompt-optimizer-dspy
description: Mathematical optimization of agent prompts using DSPy and MIPROv2. Replaces manual prompt engineering with data-driven compilation.
---

# Prompt Optimizer (DSPy Edition)

## Purpose
Transform "Prompt Engineering" (Guesswork) into "Prompt Programming" (Optimization). 
This skill uses the **DSPy** framework to mathematically optimize the instructions of other agents based on their success/failure metrics.

## Core Capabilities
- **Compiler**: Uses `dspy.MIPROv2` (Multi-prompt Instruction Proposal Optimizer) to find the optimal prompt for a given task.
- **Metric-Driven**: Optimizes against a defined metric (e.g., "Lead Replied = True", "Code Passed Tests = True").
- **Sovereign Execution**: Connects to local Ollama models (`llama3.1`, `deepseek-coder`) to perform the optimization loop without leaking data to the cloud.

## Workflow
1. **Define Task**: Identify the Agent/Module to optimize (e.g., `AGENT_SALES`).
2. **Gather Data**: Retrieve a dataset of inputs (prompts) and outcomes (success/fail) from Redis or the Success Vault.
3. **Compile**: Run `scripts/compile_agent.py` to search the prompt space.
4. **Deploy**: Update the agent's `MISSION_PROFILE.md` with the compiled, high-performance instruction.

## Rules
- **No Magic**: Optimization requires at least 5-10 examples of Input->Expected Output.
- **Local First**: Prioritize local inference for the optimization loop to save costs.
