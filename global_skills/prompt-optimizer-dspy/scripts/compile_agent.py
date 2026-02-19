#!/usr/bin/env python3
"""
DSPy Agent Compiler (Sovereign Edition)
Optimizes agent instructions using mathematical backpropagation via MIPROv2.
"""

import dspy
import os
import sys
import json
from dspy import MIPROv2

# --- CONFIGURATION ---
OLLAMA_MODEL = "llama3.1:8b"
OLLAMA_URL = "http://localhost:11434"

# 1. Setup Language Model (Sovereign)
lm = dspy.LM(f"ollama_chat/{OLLAMA_MODEL}", api_base=OLLAMA_URL, max_tokens=2000)
dspy.settings.configure(lm=lm)

class AgentModule(dspy.Module):
    """Generic DSPy Module for any Agent Task"""
    def __init__(self, role_description):
        super().__init__()
        self.role = role_description
        # The 'signature' defines Input -> Output fields
        self.prog = dspy.ChainOfThought("user_intent -> agent_action")

    def forward(self, user_intent):
        return self.prog(user_intent=user_intent)

def load_dataset(agent_name):
    """
    Mock Data Loader - In production, this pulls from Redis/Pinecone Success Vault.
    Returns: List of dspy.Example(user_intent="...", agent_action="...")
    """
    # Example for AGENT_SALES
    if "SALES" in agent_name:
        return [
            dspy.Example(user_intent="Find leads for SaaS", agent_action="Search LinkedIn for SaaS founders, filter by headcount > 50, and enrich email.").with_inputs("user_intent"),
            dspy.Example(user_intent="Reply to objection: too expensive", agent_action="Acknowledge concern, pivot to ROI calculation, and offer a pilot.").with_inputs("user_intent"),
            dspy.Example(user_intent="Follow up on no reply", agent_action="Send a 'break-up' email or a value-add article. Do not just ask 'did you see this'.").with_inputs("user_intent")
        ]
    return []

def metric_exact_match(example, pred, trace=None):
    """
    Simple metric: Does the predicted action contain keywords from the ground truth?
    In production, this would be an LLM-as-a-Judge metric.
    """
    ground_truth = example.agent_action.lower()
    prediction = pred.agent_action.lower()
    
    # Simple semantic overlap check
    score = 0
    if len(prediction) > 10: score += 0.2
    if any(word in prediction for word in ground_truth.split() if len(word) > 4):
        score += 0.8
        
    return score >= 0.8

def optimize_agent(agent_name, role_description):
    print(f"🚀 [DSPy] Compiling Agent: {agent_name}...")
    
    # 1. Load Training Data
    trainset = load_dataset(agent_name)
    if not trainset:
        print("❌ No training data found. Cannot optimize.")
        return

    # 2. Define Program
    program = AgentModule(role_description)

    # 3. Optimize with MIPROv2 (Multi-prompt Instruction Proposal Optimizer)
    # This searches for the best instructions/prompts
    teleprompter = MIPROv2(metric=metric_exact_match, auto="light", prompt_model=lm, task_model=lm)
    
    print("   ... Optimizing instructions (this may take a minute) ...")
    try:
        optimized_program = teleprompter.compile(program, trainset=trainset, requires_permission_to_run=False)
        
        # 4. Save the Optimized Instruction
        # DSPy saves the 'state' which includes the optimized signature/instructions
        save_path = f"{agent_name}_optimized.json"
        optimized_program.save(save_path)
        
        print(f"✅ Optimization Complete! Saved to {save_path}")
        print("   (You can now load this JSON to inspect the improved prompts)")
        
    except Exception as e:
        print(f"❌ Optimization failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 2:
        optimize_agent(sys.argv[1], sys.argv[2])
    else:
        # Test Run
        optimize_agent("AGENT_SALES", "You are an autonomous sales hunter.")
