#!/usr/bin/env python3
import os
import subprocess
import datetime
import requests
from pathlib import Path

# --- CONFIGURACIÓN ---
PROJECT_ROOT = Path("/Users/mauroociappina/.gemini")
LOG_FILE = PROJECT_ROOT / "CORPORATE_LOG.md"
AGENTS_DIR = PROJECT_ROOT / "agents"

# Cargar variables de entorno
def load_env():
    env_vars = {}
    env_file = PROJECT_ROOT / ".env"
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    k, v = line.strip().split('=', 1)
                    env_vars[k] = v
    return env_vars

ENV = load_env()
TELEGRAM_TOKEN = ENV.get('TELEGRAM_BOT_TOKEN')
CHAT_ID = ENV.get('TELEGRAM_CHAT_ID')

def log_entry(status, message):
    timestamp = datetime.datetime.now().isoformat()
    icon = "🟢" if status == "OK" else ("🟡" if status == "WARN" else "🔴")
    entry = f"| {timestamp} | {icon} | {message} |\n"
    
    if not LOG_FILE.exists():
        with open(LOG_FILE, 'w') as f:
            f.write("# 📋 Bitácora Corporativa DUDE CORP\n\n| Fecha | Estado | Mensaje |\n|---|---|---|")
    
    with open(LOG_FILE, 'a') as f:
        f.write(entry)
    
    print(f"{icon} {message}")
    return f"{icon} {message}"

def send_telegram(text):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("⚠️ Telegram not configured.")
        return
    
    message = f"🏢 *THE DUDE - AUDIT REPORT*\n\n{text}"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(url, json={
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }, timeout=10)
    except Exception as e:
        print(f"❌ Error sending Telegram: {e}")

def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=PROJECT_ROOT)
        return result.stdout.strip()
    except Exception:
        return ""

def run_audit():
    report = []
    print("🕵️ Iniciando Auditoría Corporativa v3.1 (Redis 8 Optimized)...")

    # 1. Redis Check (Advanced)
    redis_info_raw = run_cmd("redis-cli info")
    if "redis_version" in redis_info_raw:
        # Extract specific metrics
        version = next((l for l in redis_info_raw.splitlines() if "redis_version:" in l), "redis_version:unknown").split(":")[1]
        frag_ratio = next((l for l in redis_info_raw.splitlines() if "mem_fragmentation_ratio:" in l), "mem_fragmentation_ratio:0").split(":")[1]
        evicted = next((l for l in redis_info_raw.splitlines() if "evicted_keys:" in l), "evicted_keys:0").split(":")[1]
        
        status = "OK"
        if float(frag_ratio) > 1.5: status = "WARN"
        
        report.append(log_entry(status, f"Redis v{version}: FRAG={frag_ratio}, EVICTED={evicted}"))
    else:
        report.append(log_entry("CRITICAL", "Redis: CAÍDO o No Respondiente."))

    # 2. Disk Check
    disk_usage = run_cmd("du -sh . | cut -f1")
    report.append(log_entry("OK", f"Espacio: Proyecto ocupa {disk_usage}"))

    # 3. Agents Check (Cluster-Aware)
    agents_to_check = {
        'AGENT_INTEL': 'CLUSTER_CEO/AGENT_INTEL',
        'AGENT_OPS': 'CLUSTER_EXECUTION/AGENT_OPS',
        'AGENT_SENTINEL': 'CLUSTER_GUARD/AGENT_TRUST_SAFETY',
        'AGENT_SECURITY': 'CLUSTER_GUARD/AGENT_SECURITY',
        'AGENT_FINANCE': 'CLUSTER_CEO/AGENT_FINANCE',
        'AGENT_BRAIN': 'CLUSTER_BRAIN/AGENT_BRAIN',
        'AGENT_GROWTH': 'CLUSTER_EXECUTION/AGENT_GROWTH',
        'CLUSTER_CEO': 'CLUSTER_CEO',
        'CLUSTER_EXECUTION': 'CLUSTER_EXECUTION',
        'CLUSTER_GUARD': 'CLUSTER_GUARD',
        'CLUSTER_BRAIN': 'CLUSTER_BRAIN'
    }
    found = []
    for name, subpath in agents_to_check.items():
        if (AGENTS_DIR / subpath).exists():
            found.append(name)
    
    status = "OK" if len(found) == len(agents_to_check) else "WARN"
    report.append(log_entry(status, f"Agentes: {len(found)}/{len(agents_to_check)} activos en sus CLUSTERS."))

    # 4. Git Check
    git_status = run_cmd("git status --short")
    if git_status:
        report.append(log_entry("WARN", f"Git: Cambios sin commit detectados.\n```\n{git_status[:200]}\n```"))
    else:
        report.append(log_entry("OK", "Git: Repositorio limpio."))

    # Enviar reporte
    send_telegram("\n".join(report))
    print("🏁 Auditoría completada.")

if __name__ == "__main__":
    run_audit()
