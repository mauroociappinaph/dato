#!/usr/bin/env python3
"""
FASE 1: ANÁLISIS Y DESCUBRIMIENTO
Skills: detect-duplicate-files + technical-debt-analysis
"""

import os
import hashlib
from pathlib import Path
from collections import defaultdict
import json
from src.helpers import join_paths

def get_file_hash(filepath):
    """Calcula hash SHA256 de un archivo"""
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        return None

def scan_directory(base_path):
    """Escanea directorio buscando archivos Python y MD"""
    files_by_hash = defaultdict(list)
    file_stats = {
        'total_files': 0,
        'python_files': 0,
        'md_files': 0,
        'json_files': 0,
        'large_files': [],  # > 300 líneas
        'empty_init_files': [],
        'files_with_duplicated_logic': []
    }

    for root, dirs, files in os.walk(base_path):
        # Ignorar __pycache__, .git, node_modules
        dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', 'node_modules', '_archive']]

        for file in files:
            if file.endswith(('.py', '.md', '.json')):
                filepath = os.path.join(root, file)
                rel_path = os.path.relpath(filepath, base_path)

                # Contar tipos de archivos
                file_stats['total_files'] += 1
                if file.endswith('.py'):
                    file_stats['python_files'] += 1
                elif file.endswith('.md'):
                    file_stats['md_files'] += 1
                elif file.endswith('.json'):
                    file_stats['json_files'] += 1

                # Verificar tamaño (The 300 Rule)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        if len(lines) > 300:
                            file_stats['large_files'].append({
                                'path': rel_path,
                                'lines': len(lines)
                            })

                        # Detectar __init__.py vacíos o casi vacíos
                        if file == '__init__.py' and len(lines) <= 2:
                            file_stats['empty_init_files'].append(rel_path)

                except Exception as e:
                    pass

                # Calcular hash para detectar duplicados exactos
                file_hash = get_file_hash(filepath)
                if file_hash:
                    files_by_hash[file_hash].append(rel_path)

    return files_by_hash, file_stats

def analyze_technical_debt(base_path, files_by_hash, file_stats):
    """Analiza deuda técnica en el codebase"""

    print("=" * 80)
    print("🔍 FASE 1: ANÁLISIS Y DESCUBRIMIENTO - REPORTE")
    print("=" * 80)

    # 1. ARCHIVOS DUPLICADOS EXACTOS
    print("\n📁 1. ARCHIVOS DUPLICADOS EXACTOS (SHA256)")
    print("-" * 80)
    duplicates = {k: v for k, v in files_by_hash.items() if len(v) > 1}
    if duplicates:
        for file_hash, paths in duplicates.items():
            print(f"\n⚠️  Duplicados encontrados ({len(paths)} archivos):")
            for path in paths:
                print(f"   - {path}")
    else:
        print("   ✅ No se encontraron archivos duplicados exactos")

    # 2. ARCHIVOS GRANDES (> 300 líneas - The 300 Rule)
    print("\n\n📏 2. ARCHIVOS QUE VIOLAN 'THE 300 RULE'")
    print("-" * 80)
    if file_stats['large_files']:
        print(f"   ⚠️  {len(file_stats['large_files'])} archivos exceden 300 líneas:")
        for file in sorted(file_stats['large_files'], key=lambda x: x['lines'], reverse=True):
            print(f"   - {file['path']}: {file['lines']} líneas")
    else:
        print("   ✅ Todos los archivos cumplen con The 300 Rule")

    # 3. ARCHIVOS __init__.py VACÍOS
    print("\n\n📦 3. ARCHIVOS __init__.py VACÍOS O CASI VACÍOS")
    print("-" * 80)
    if file_stats['empty_init_files']:
        print(f"   ⚠️  {len(file_stats['empty_init_files'])} archivos __init__.py vacíos:")
        for path in file_stats['empty_init_files']:
            print(f"   - {path}")
    else:
        print("   ✅ Todos los __init__.py tienen contenido relevante")

    # 4. ESTADÍSTICAS GENERALES
    print("\n\n📊 4. ESTADÍSTICAS GENERALES")
    print("-" * 80)
    print(f"   Total de archivos analizados: {file_stats['total_files']}")
    print(f"   Archivos Python (.py): {file_stats['python_files']}")
    print(f"   Archivos Markdown (.md): {file_stats['md_files']}")
    print(f"   Archivos JSON (.json): {file_stats['json_files']}")
    print(f"   Archivos > 300 líneas: {len(file_stats['large_files'])}")
    print(f"   Duplicados exactos: {len(duplicates)}")

    # 5. RECOMENDACIONES DE REFACTORIZACIÓN
    print("\n\n💡 5. RECOMENDACIONES DE REFACTORIZACIÓN (PRIORIZADAS)")
    print("-" * 80)

    recommendations = []

    if file_stats['large_files']:
        recommendations.append({
            'priority': 'ALTA',
            'type': 'Split de archivos grandes',
            'files': [f["path"] for f in file_stats['large_files'][:5]],
            'action': 'Aplicar splitting quirúrgico - extraer funciones a módulos separados'
        })

    if duplicates:
        recommendations.append({
            'priority': 'ALTA',
            'type': 'Eliminar duplicación',
            'count': len(duplicates),
            'action': 'Consolidar archivos duplicados en un único módulo reusable'
        })

    if file_stats['empty_init_files']:
        recommendations.append({
            'priority': 'MEDIA',
            'type': 'Barrel files',
            'files': file_stats['empty_init_files'][:5],
            'action': 'Convertir __init__.py vacíos en barrel files con exports públicos'
        })

    # Analizar patrones de duplicación lógica (funciones similares)
    similar_patterns = detect_similar_patterns(base_path)
    if similar_patterns:
        recommendations.append({
            'priority': 'ALTA',
            'type': 'Código duplicado lógico',
            'patterns': similar_patterns,
            'action': 'Extraer lógica común a funciones utilitarias en src/helpers/'
        })

    for i, rec in enumerate(recommendations, 1):
        print(f"\n   {i}. [{rec['priority']}] {rec['type']}")
        print(f"      Acción: {rec['action']}")
        if 'files' in rec:
            print(f"      Archivos afectados: {len(rec['files'])}")
        if 'count' in rec:
            print(f"      Grupos de duplicados: {rec['count']}")

    # Guardar reporte JSON
    report = {
        'phase': 'Phase 1: Analysis & Discovery',
        'duplicates': duplicates,
        'large_files': file_stats['large_files'],
        'empty_init_files': file_stats['empty_init_files'],
        'statistics': {
            'total_files': file_stats['total_files'],
            'python_files': file_stats['python_files'],
            'md_files': file_stats['md_files'],
            'json_files': file_stats['json_files']
        },
        'recommendations': recommendations
    }

    report_path = os.path.join(base_path, 'phase1_report.json')
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)

    print(f"\n\n📄 Reporte completo guardado en: {report_path}")
    print("=" * 80)

def detect_similar_patterns(base_path):
    """Detecta patrones similares de código entre archivos"""
    patterns = []

    # Buscar imports comunes repetidos
    import_patterns = defaultdict(list)

    for root, dirs, files in os.walk(base_path):
        dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', 'node_modules', '_archive']]

        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        # Buscar imports estándar comunes
                        if 'import os' in content and 'import sys' in content:
                            rel_path = os.path.relpath(filepath, base_path)
                            import_patterns['os+sys'].append(rel_path)
                        if 'requests.get' in content:
                            rel_path = os.path.relpath(filepath, base_path)
                            import_patterns['requests'].append(rel_path)
                except:
                    pass

    # Reportar patrones que aparecen en múltiples archivos
    for pattern, files in import_patterns.items():
        if len(files) > 3:  # Si aparece en más de 3 archivos
            patterns.append({
                'pattern': pattern,
                'occurrences': len(files),
                'example_files': files[:3]
            })

    return patterns

if __name__ == "__main__":
    base_path = "/Users/mauroociappina/Desktop/TheDude/global_skills"
    print("🚀 Iniciando Fase 1: Análisis y Descubrimiento...")
    print(f"📂 Directorio objetivo: {base_path}")
    print("⏳ Escaneando archivos...\n")

    files_by_hash, file_stats = scan_directory(base_path)
    analyze_technical_debt(base_path, files_by_hash, file_stats)
