#!/usr/bin/env python3
"""
Script para eliminar archivos __init__.py vacíos en subdirectorios que no necesitan ser paquetes Python.

Elimina __init__.py vacíos o casi vacíos (≤2 líneas) de subdirectorios como:
- scripts/
- resources/
- examples/
- assets/
- references/
- templates/
- docs/
"""

import os
import sys
from pathlib import Path

# Subdirectorios donde los __init__.py vacíos se pueden eliminar
TARGET_SUBDIRS = {'scripts', 'resources', 'examples', 'assets', 'references', 'templates', 'docs'}

def is_empty_or_trivial(filepath: Path) -> bool:
    """Verifica si el archivo está vacío o tiene ≤2 líneas (probablemente trivial)"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            return len(lines) <= 2
    except Exception:
        return False

def should_remove(filepath: Path) -> bool:
    """Determina si el archivo debe eliminarse"""
    # Verificar si está en uno de los subdirectorios objetivo
    parts = filepath.parts
    for part in parts:
        if part in TARGET_SUBDIRS:
            return is_empty_or_trivial(filepath)
    return False

def find_empty_init_files(base_path: str) -> list[Path]:
    """Encuentra todos los __init__.py vacíos en subdirectorios objetivo"""
    base = Path(base_path)
    empty_files = []

    for init_file in base.rglob('__init__.py'):
        if should_remove(init_file):
            empty_files.append(init_file)

    return sorted(empty_files)

def main():
    base_path = '/Users/mauroociappina/Desktop/TheDude/global_skills'
    dry_run = '--dry-run' in sys.argv

    print("=" * 70)
    print("🧹 CLEANUP: Eliminando __init__.py vacíos en subdirectorios")
    print("=" * 70)
    print(f"Directorio base: {base_path}")
    print(f"Subdirectorios objetivo: {', '.join(TARGET_SUBDIRS)}")
    print(f"Modo: {'DRY-RUN (simulación)' if dry_run else 'REAL (eliminando)'}")
    print()

    # Encontrar archivos a eliminar
    files_to_remove = find_empty_init_files(base_path)

    if not files_to_remove:
        print("✅ No se encontraron archivos __init__.py vacíos en subdirectorios.")
        return

    print(f"📁 Archivos a eliminar: {len(files_to_remove)}")
    print()

    # Agrupar por tipo de subdirectorio
    by_category = {}
    for f in files_to_remove:
        for part in f.parts:
            if part in TARGET_SUBDIRS:
                by_category.setdefault(part, []).append(f)
                break

    # Mostrar resumen por categoría
    print("📊 Resumen por categoría:")
    for category in sorted(by_category.keys()):
        count = len(by_category[category])
        print(f"   {category}/: {count} archivos")

    print()

    # Mostrar primeros 20 archivos como ejemplo
    if len(files_to_remove) > 20:
        print("📝 Primeros 20 archivos:")
        for f in files_to_remove[:20]:
            print(f"   - {f.relative_to(base_path)}")
        print(f"   ... y {len(files_to_remove) - 20} más")
    else:
        print("📝 Archivos a eliminar:")
        for f in files_to_remove:
            print(f"   - {f.relative_to(base_path)}")

    print()

    if dry_run:
        print("🏃 Modo dry-run: No se eliminó ningún archivo.")
        print(f"   Para eliminar realmente, ejecuta sin --dry-run")
        return

    # Confirmar antes de eliminar
    confirm = input(f"⚠️  ¿Eliminar {len(files_to_remove)} archivos? [y/N]: ").strip().lower()
    if confirm not in ('y', 'yes'):
        print("❌ Cancelado por el usuario.")
        return

    # Eliminar archivos
    removed = 0
    errors = 0

    for f in files_to_remove:
        try:
            f.unlink()
            removed += 1
        except Exception as e:
            print(f"   ❌ Error eliminando {f}: {e}")
            errors += 1

    print()
    print("=" * 70)
    print("✅ LIMPIEZA COMPLETADA")
    print("=" * 70)
    print(f"   Archivos eliminados: {removed}")
    if errors:
        print(f"   Errores: {errors}")

    # Contar archivos restantes
    remaining = list(Path(base_path).rglob('__init__.py'))
    remaining_empty = [f for f in remaining if is_empty_or_trivial(f)]

    print(f"   Total __init__.py restantes: {len(remaining)}")
    print(f"   __init__.py vacíos restantes: {len(remaining_empty)}")

if __name__ == "__main__":
    main()
