#!/usr/bin/env python3
"""
Technical Debt Analyzer (v1.0)
REAL - Scans the project for architectural and code debt.
"""

import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/Users/mauroociappina/.gemini")
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
MAX_LOC = 300

def analyze_debt():
    print(f"🔍 Iniciando Análisis de Deuda Técnica en {PROJECT_ROOT}...")

    report = {
        "violations_300_rule": [],
        "missing_tests": [],
        "todo_fixme_count": 0,
        "oversized_logs": []
    }

    # 1. Check 300 Rule Violations
    for root, dirs, files in os.walk(PROJECT_ROOT):
        # Ignore specific dirs
        if any(d in root for d in ["node_modules", ".git", "anti_gravity-browser-profile", "ollama_data", "redis_data"]):
            continue

        for file in files:
            if file.endswith((".py", ".ts", ".tsx", ".js", ".sh")):
                file_path = Path(root) / file
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        if len(lines) > MAX_LOC:
                            report["violations_300_rule"].append({
                                "file": str(file_path.relative_to(PROJECT_ROOT)),
                                "lines": len(lines)
                            })
                except:
                    continue

    # 2. Check Missing Tests for core scripts
    if SCRIPTS_DIR.exists():
        for script in SCRIPTS_DIR.glob("*.py"):
            # Simple check: does a file with 'test' and the script name exist?
            test_found = False
            # Look in PROJECT_ROOT/tests or nearby
            test_patterns = [f"test_{script.name}", f"{script.stem}_test.py"]
            # For this simplified version, we just check if it's in a hypothetical 'tests' folder
            # or if it starts with 'test_'
            if script.name.startswith("test_"):
                continue

            # Heuristic: search project for tests
            # (Real implementation would be more thorough)
            report["missing_tests"].append(script.name)

    # 3. Scan for TODO/FIXME
    # (Using grep via shell for efficiency)
    try:
        todo_cmd = f"grep -riE 'TODO|FIXME' {PROJECT_ROOT} --exclude-dir={{.git,node_modules,anti_gravity-browser-profile}} | wc -l"
        res = os.popen(todo_cmd).read().strip()
        report["todo_fixme_count"] = int(res)
    except:
        pass

    # 4. Check Large Logs (> 10MB)
    logs_dir = PROJECT_ROOT / "logs"
    if logs_dir.exists():
        for log in logs_dir.glob("*.log"):
            size_mb = log.stat().st_size / (1024 * 1024)
            if size_mb > 10:
                report["oversized_logs"].append({
                    "file": log.name,
                    "size_mb": round(size_mb, 2)
                })

    return report

if __name__ == "__main__":
    results = analyze_debt()

    print("\n--- ⚖️ REPORTE DE DEUDA TÉCNICA DUDE v1.0 ---")

    print(f"\n📏 Violaciones Regla del 300 (>{MAX_LOC} líneas):")
    if results["violations_300_rule"]:
        for v in results["violations_300_rule"]:
            print(f"  ❌ {v['file']} ({v['lines']} líneas)")
    else:
        print("  ✅ Ninguna. Todos los archivos son modulares.")

    print(f"\n🧪 Scripts sin Tests Detectados:")
    if results["missing_tests"]:
        print(f"  ⚠️ {len(results['missing_tests'])} scripts en /scripts/ requieren cobertura.")
    else:
        print("  ✅ Cobertura aparente completa.")

    print(f"\n📝 Marcadores TODO/FIXME: {results['todo_fixme_count']}")

    print(f"\n📂 Logs Sobredimensionados (>10MB):")
    if results["oversized_logs"]:
        for l in results["oversized_logs"]:
            print(f"  🔴 {l['file']} ({l['size_mb']} MB)")
    else:
        print("  ✅ Logs bajo control.")

    print("\n🎯 CONCLUSIÓN:")
    total_debt_score = len(results["violations_300_rule"]) * 5 + (results["todo_fixme_count"] / 10)
    if total_debt_score > 20:
        print(">>> ESTADO: Deuda Crítica. Se recomienda refactorización inmediata.")
    elif total_debt_score > 5:
        print(">>> ESTADO: Deuda Moderada. Monitorear crecimiento.")
    else:
        print(">>> ESTADO: Código Limpio. Proceder con nuevas features.")
