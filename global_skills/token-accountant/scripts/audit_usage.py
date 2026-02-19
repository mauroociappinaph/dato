#!/usr/bin/env python3
"""
Token Accountant - Usage Auditor
Calculates real-world cost of agent interactions.
"""

import json
import os
import sys
from pathlib import Path

def calculate_cost(model_name, input_tokens, output_tokens):
    matrix_path = Path(__file__).parent.parent / "resources" / "pricing_matrix.json"
    
    with open(matrix_path, 'r') as f:
        data = json.load(f)
    
    matrix = data.get("models", {})
    model = matrix.get(model_name.lower())
    
    if not model:
        return {"error": f"Model {model_name} not found in pricing matrix"}
    
    input_cost = (input_tokens / 1_000_000) * model.get("input_per_1m", 0)
    output_cost = (output_tokens / 1_000_000) * model.get("output_per_1m", 0)
    total_cost = input_cost + output_cost
    
    return {
        "model": model_name,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_cost_usd": round(total_cost, 6),
        "sovereign_savings_ratio": 1.0 if model.get("input_per_1m") == 0 else 0.0
    }

if __name__ == "__main__":
    if len(sys.argv) == 4:
        # Usage: python3 audit_usage.py gpt-4o 1500 500
        res = calculate_cost(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
        print(json.dumps(res, indent=2))
    else:
        print("Usage: audit_usage.py <model_name> <input_tokens> <output_tokens>")
