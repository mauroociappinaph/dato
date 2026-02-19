#!/usr/bin/env python3
"""
Acceptance Criteria Guardian - Validator Script
Parses Markdown files for Gherkin syntax and validates DoD compliance.
"""

import os
import sys
import re

def validate_gherkin(file_path):
    if not os.path.exists(file_path):
        return {"status": "ERROR", "msg": f"File not found: {file_path}"}

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Search for Gherkin keywords
    keywords = ["Given", "When", "Then", "Scenario", "Feature"]
    found = {k: len(re.findall(rf"\b{k}\b", content)) for k in keywords}
    
    scenarios = re.findall(r"(?:Scenario|Escenario):", content)
    
    score = 0
    if found["Given"] > 0: score += 2
    if found["When"] > 0: score += 2
    if found["Then"] > 0: score += 2
    if len(scenarios) > 0: score += 4

    status = "PASS" if score >= 8 else "WARN" if score > 0 else "FAIL"
    
    return {
        "file": file_path,
        "status": status,
        "score": score,
        "scenarios_found": len(scenarios),
        "details": found
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        result = validate_gherkin(sys.argv[1])
        import json
        print(json.dumps(result, indent=2))
    else:
        print("Usage: python3 validate_ac.py <path_to_markdown>")
