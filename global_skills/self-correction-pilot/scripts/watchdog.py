#!/usr/bin/env python3
"""
Self-Correction Watchdog (v1.0)
Monitors logs for failures and triggers the Meta-Learning Optimizer.
"""

import os
import re
import sys
import subprocess
from pathlib import Path

# Config
LOGS_DIR = Path("/Users/mauroociappina/.gemini/logs")
OPTIMIZER_SCRIPT = Path("/Users/mauroociappina/.gemini/anti_gravity/global_skills/meta-learning-engine/scripts/optimizer.py")
FAILURE_KEYWORDS = ["ERROR", "FAILURE", "FAILED", "StatusCode.UNAVAILABLE", "EXCEPTION"]

def run_watchdog():
    print("🛡️ Watchdog: Iniciando monitoreo de logs para autocuración...")
    
    if not LOGS_DIR.exists():
        print(f"❌ Error: Directorio de logs {LOGS_DIR} no encontrado.")
        return

    # Scan all .log files
    for log_file in LOGS_DIR.glob("*.log"):
        process_log(log_file)

def process_log(log_path):
    # Read the last 100 lines to find recent errors
    try:
        with open(log_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()[-100:]
    except Exception as e:
        print(f"⚠️ No se pudo leer {log_path.name}: {e}")
        return

    content = "".join(lines)
    
    # 1. Detect if there's a failure
    if any(keyword in content.upper() for keyword in FAILURE_KEYWORDS):
        print(f"⚠️ Fallo detectado en {log_path.name}")
        
        # 2. Identify the Agent (heuristic: look for AGENT_NAME: patterns)
        agent_match = re.search(r'(AGENT_[A-Z_]+)', content)
        agent_name = agent_match.group(1) if agent_match else "UNKNOWN_AGENT"
        
        if agent_name == "UNKNOWN_AGENT":
            # Heuristic 2: Try to derive agent from log name (e.g., agent_sales.log -> AGENT_SALES)
            name_part = log_path.stem.replace("agent_", "").upper()
            agent_name = f"AGENT_{name_part}"

        print(f"🧠 Disparando optimización para {agent_name}...")
        
        # 3. Extract relevant error snippet (last 5 lines of error)
        error_snippet = ""
        for i, line in enumerate(lines):
            if any(k in line.upper() for k in FAILURE_KEYWORDS):
                # Take context around the error
                start = max(0, i - 2)
                end = min(len(lines), i + 5)
                error_snippet = "".join(lines[start:end])
                break
        
        # 4. Call the Optimizer
        try:
            cmd = [sys.executable, str(OPTIMIZER_SCRIPT), agent_name, error_snippet]
            subprocess.run(cmd, check=True)
            print(f"✅ Protocolo de autocuración enviado para {agent_name}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error al ejecutar el optimizador: {e}")

if __name__ == "__main__":
    run_watchdog()
