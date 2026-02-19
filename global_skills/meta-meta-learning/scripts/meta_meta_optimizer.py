#!/usr/bin/env python3
"""
Meta-Meta Learning Engine - Recursive Optimizer (Phase 31)
100% REAL - NO SIMULATION.
Uses actual log evidence to improve system code.
"""

import os
import sys
import re
import requests
from pathlib import Path

# Config
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL = "llama3.1:8b"
LOG_FILE = Path("/Users/mauroociappina/.gemini/logs/massive_hunt.log")
META_OPTIMIZER_PATH = Path("/Users/mauroociappina/.gemini/anti_gravity/global_skills/meta-learning-engine/scripts/optimizer.py")

def get_real_log_evidence():
    """Reads actual logs to find recurring errors"""
    if not LOG_FILE.exists():
        return None
    
    with open(LOG_FILE, 'r') as f:
        lines = f.readlines()
    
    # Capture only the last 50 lines to detect recent failures
    recent_logs = "".join(lines[-50:])
    errors = re.findall(r"error|failed|unavailable", recent_logs, re.IGNORECASE)
    
    if len(errors) > 5:
        return recent_logs
    return None

def optimize_meta_optimizer():
    print("🧠 [META-META] Analizando evidencia real en logs...")
    
    evidence = get_real_log_evidence()
    
    if not evidence:
        print("✅ [META-META] No se detectan fallos críticos recurrentes en los logs. El sistema es estable.")
        return

    print("⚠️ [META-META] Fallos detectados. Iniciando Optimización de Segundo Orden basada en datos reales...")

    # 1. Read current optimizer code
    with open(META_OPTIMIZER_PATH, 'r') as f:
        code = f.read()

    # 2. Ask AI to improve the INTERNAL PROMPT of the optimizer using the REAL evidence
    current_prompt_match = re.search(r'prompt = f"""(.*?)"""', code, re.DOTALL)
    if not current_prompt_match:
        print("❌ [META-META] No se pudo localizar el prompt en el optimizador.")
        return

    current_prompt = current_prompt_match.group(1)
    
    refinement_task = f"""
    SYSTEM: You are a Meta-Meta-Learning Engine (Recursive Self-Improvement).
    TASK: The following prompt is used by a 'Meta-Learning Optimizer' to fix agents. 
    Logs show these REAL errors: 
    {evidence[:500]} 
    
    Improve the prompt to handle these specific failure patterns, focusing on 'StatusCode.UNAVAILABLE' and trace exports.
    
    CURRENT PROMPT:
    {current_prompt}
    
    OUTPUT: Provide ONLY the improved text for the prompt string.
    """

    try:
        res = requests.post(OLLAMA_URL, json={"model": MODEL, "prompt": refinement_task, "stream": False})
        new_prompt_text = res.json()['response'].strip()
        
        # 3. Apply the fix back to the optimizer file
        new_code = code.replace(current_prompt, new_prompt_text)
        
        with open(META_OPTIMIZER_PATH, 'w') as f:
            f.write(new_code)
            
        print("🎉 [META-META] ÉXITO: El sistema se ha auto-modificado basado en evidencia real de logs.")
        return True
    except Exception as e:
        print(f"❌ [META-META] Error en optimización: {e}")
        return False

if __name__ == "__main__":
    optimize_meta_optimizer()