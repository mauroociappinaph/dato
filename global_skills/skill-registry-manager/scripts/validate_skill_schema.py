#!/usr/bin/env python3
"""
Validador de esquema para skill_registry.json con soporte para campos extendidos.
"""

import json
import sys
from typing import Dict, Any, List

def load_skill_registry() -> List[Dict[str, Any]]:
    """Carga el registro de skills desde el archivo JSON."""
    try:
        with open('/Users/mauroociappina/Desktop/TheDude/global_skills/skill_registry.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("ERROR: No se encontró skill_registry.json")
        return []
    except json.JSONDecodeError as e:
        print(f"ERROR: JSON inválido en skill_registry.json: {e}")
        return []

def validate_skill_schema(skill: Dict[str, Any]) -> List[str]:
    """Valida un skill contra el esquema extendido."""
    errors = []

    # Campos requeridos
    required_fields = ['name', 'description', 'path', 'id', 'version', 'status', 'cluster']
    for field in required_fields:
        if field not in skill:
            errors.append(f"Campo requerido faltante: {field}")

    # Validación de tipos básicos
    if 'name' in skill and not isinstance(skill['name'], str):
        errors.append("El campo 'name' debe ser string")

    if 'version' in skill and not isinstance(skill['version'], str):
        errors.append("El campo 'version' debe ser string")

    if 'status' in skill and skill['status'] not in ['active', 'deprecated']:
        errors.append("El campo 'status' debe ser 'active' o 'deprecated'")

    # Validación de campos extendidos
    if 'inputs' in skill:
        if not isinstance(skill['inputs'], dict):
            errors.append("El campo 'inputs' debe ser un objeto")
        else:
            for key, value in skill['inputs'].items():
                if not isinstance(key, str) or not isinstance(value, str):
                    errors.append(f"Los campos de 'inputs' deben tener claves y valores string")

    if 'outputs' in skill:
        if not isinstance(skill['outputs'], dict):
            errors.append("El campo 'outputs' debe ser un objeto")
        else:
            for key, value in skill['outputs'].items():
                if not isinstance(key, str) or not isinstance(value, str):
                    errors.append(f"Los campos de 'outputs' deben tener claves y valores string")

    if 'cost_estimate' in skill:
        if not isinstance(skill['cost_estimate'], dict):
            errors.append("El campo 'cost_estimate' debe ser un objeto")
        else:
            cost = skill['cost_estimate']
            if 'per_execution' in cost and not isinstance(cost['per_execution'], (int, float)):
                errors.append("El campo 'per_execution' debe ser numérico")
            if 'currency' in cost and cost['currency'] not in ['USD', 'EUR', 'ARS']:
                errors.append("El campo 'currency' debe ser USD, EUR o ARS")
            if 'complexity_factor' in cost and cost['complexity_factor'] not in ['low', 'medium', 'high']:
                errors.append("El campo 'complexity_factor' debe ser low, medium o high")

    if 'preferred_agent' in skill and not isinstance(skill['preferred_agent'], str):
        errors.append("El campo 'preferred_agent' debe ser string")

    return errors

def main():
    """Función principal de validación."""
    print("🔍 Validando esquema de skill_registry.json...")

    skills = load_skill_registry()
    if not skills:
        sys.exit(1)

    total_errors = 0
    skills_with_errors = 0

    for skill in skills:
        errors = validate_skill_schema(skill)
        if errors:
            skills_with_errors += 1
            total_errors += len(errors)
            print(f"\n❌ {skill.get('name', 'Skill sin nombre')}:")
            for error in errors:
                print(f"   - {error}")

    print(f"\n📊 Resultados de validación:")
    print(f"   - Total de skills: {len(skills)}")
    print(f"   - Skills con errores: {skills_with_errors}")
    print(f"   - Errores totales: {total_errors}")

    if skills_with_errors == 0:
        print("✅ Todas las skills pasaron la validación!")
        sys.exit(0)
    else:
        print("❌ Algunas skills tienen errores de esquema")
        sys.exit(1)

if __name__ == "__main__":
    main()
