#!/usr/bin/env python3
"""
Code Modularity Architect - Modularizer (v1.0)
REAL - Suggests splitting patterns for oversized files.
"""

import os
import sys
import re
from pathlib import Path

def suggest_split(file_path):
    print(f"✂️ Code Modularity Architect: Analizando costuras en {file_path}")
    
    if not os.path.exists(file_path):
        print(f"❌ Error: Archivo {file_path} no encontrado.")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.splitlines()

    suggestions = []

    # Heuristic 1: React Component with large return
    if "return (" in content or "return <" in content:
        if len(lines) > 200:
            suggestions.append(">>> PATRÓN DETECTADO: Componente React Gigante.")
            suggestions.append(">>> ACCIÓN: Extraer sub-componentes UI a archivos separados.")
            suggestions.append(">>> ACCIÓN: Mover lógica de estado a un Custom Hook (useModule.ts).")

    # Heuristic 2: Large Logic Classes/Functions
    if len(re.findall(r'def\s+', content)) > 5 or len(re.findall(r'class\s+', content)) > 1:
        suggestions.append(">>> PATRÓN DETECTADO: Exceso de responsabilidades (God Object).")
        suggestions.append(">>> ACCIÓN: Aplicar SRP. Dividir en clases/funciones utilitarias.")

    print("\n--- 🛠️ PLAN DE MODULARIZACIÓN SUGERIDO ---")
    for s in suggestions:
        print(s)
    
    if not suggestions:
        print("✅ El archivo parece estar bien estructurado o no se detectaron patrones de división automáticos.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        suggest_split(sys.argv[1])
    else:
        print("Usage: python3 main.py <file_path>")
