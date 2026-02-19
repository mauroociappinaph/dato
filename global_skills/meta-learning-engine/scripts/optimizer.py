#!/usr/bin/env python3
"""
Meta-Learning Optimizer (System Backpropagation)
Reads failure logs, analyzes root cause with Llama 3, and REWRITES agent instructions.
"""

import os
import sys
import json
import requests
from pathlib import Path

# Add ai-engineer scripts to path for NVIDIA client
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "ai-engineer", "scripts"))

try:
    from nvidia_nim_client import NVIDIANIMClient, ModelType
    NIM_AVAILABLE = True
except ImportError:
    NIM_AVAILABLE = False

# Config
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL = "llama3.1:8b" # Fast reasoning model (fallback)

# Initialize NVIDIA client if available
_nim_client = None
if NIM_AVAILABLE:
    _nim_client = NVIDIANIMClient()
AGENTS_DIR = Path("/Users/mauroociappina/.gemini/agents")

def get_agent_instruction_path(agent_name):
    # Map agent names to their instruction files
    # Try generic search first
    for root, dirs, files in os.walk(AGENTS_DIR):
        if agent_name in root and "MISSION_PROFILE.md" in files:
            return Path(root) / "MISSION_PROFILE.md"
        if agent_name in root and ".clinerules" in files:
            return Path(root) / ".clinerules"
    return None

def analyze_failure(failure_log):
    """Ask AI to deduce a new rule from the failure (NVIDIA NIM preferred, Ollama fallback)"""
    prompt = f"""**IMPROVED PROMPT**

SYSTEM: You are a Meta-Meta-Learning Engine, tasked with debugging an autonomous agent's rule set.

TASK: Analyze this error log, identify the specific tool parameter responsible for the issue, and formulate a precise NEW RULE to rectify it by specifying the exact tool parameters and values required to prevent similar errors in the future.

ERROR LOG:
{failure_log}

OUTPUT FORMAT (JSON only):
{{
  "analysis": "Root cause explanation with specific tool parameter details",
  "new_rule": "Exact markdown line to add to the agent's instructions, including tool parameter values",
  "section": "Where to insert it (e.g., 'CORE MANDATES', 'PROTOCOL') and which tool parameters to adjust"
}}"""

    # Try NVIDIA NIM first
    if NIM_AVAILABLE and _nim_client and _nim_client.is_available():
        try:
            print("   🚀 Using NVIDIA NIM for analysis...")
            response = _nim_client.generate(prompt, model=ModelType.LLAMA_3_1_8B, max_tokens=2048)
            return json.loads(response.text)
        except Exception as e:
            print(f"   ⚠️  NVIDIA NIM failed: {e}. Falling back to Ollama...")

    # Fallback to Ollama
    try:
        print("   🦙 Using Ollama for analysis...")
        res = requests.post(OLLAMA_URL, json={"model": MODEL, "prompt": prompt, "stream": False, "format": "json"})
        return json.loads(res.json()['response'])
    except Exception as e:
        print(f"❌ AI Analysis Failed: {e}")
        return None

def apply_gradient(agent_name, failure_data):
    """The 'Backpropagation' step: Modifying the source code/instructions"""
    print(f"🧠 Optimizing {agent_name} based on failure data...")

    target_file = get_agent_instruction_path(agent_name)
    if not target_file:
        print(f"❌ Could not find instruction file for {agent_name}")
        return

    optimization = analyze_failure(failure_data)
    if not optimization:
        return

    print(f"   📉 Gradient calculated: {optimization['analysis']}")
    print(f"   📝 Injecting rule: '{optimization['new_rule']}' into {optimization['section']}")

    # Read, Modify, Write
    with open(target_file, 'r') as f:
        content = f.read()

    # Simple insertion logic (append to section)
    if optimization['section'] in content:
        # Find section and append rule
        parts = content.split(optimization['section'])
        # Insert after the section header
        new_content = parts[0] + optimization['section'] + "\n" + optimization['new_rule'] + parts[1]

        with open(target_file, 'w') as f:
            f.write(new_content)
        print("✅ Optimization Applied. System weights updated.")
    else:
        print(f"⚠️ Section '{optimization['section']}' not found. Appending to end.")
        with open(target_file, 'a') as f:
            f.write(f"\n\n## {optimization['section']}\n{optimization['new_rule']}")

if __name__ == "__main__":
    # Example usage: python optimizer.py AGENT_SALES "Email bounced due to rate limit"
    if len(sys.argv) > 2:
        apply_gradient(sys.argv[1], sys.argv[2])
    else:
        print("Usage: optimizer.py <AGENT_NAME> <FAILURE_LOG>")
