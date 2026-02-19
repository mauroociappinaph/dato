#!/usr/bin/env python3
"""
Script para enriquecer skills existentes con los nuevos campos.
"""

import json
import sys
from pathlib import Path

def load_skill_registry():
    """Carga el registro de skills."""
    try:
        with open('/Users/mauroociappina/.gemini/anti_gravity/global_skills/skill_registry.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error cargando registry: {e}")
        return []

def save_skill_registry(skills):
    """Guarda el registro de skills."""
    try:
        with open('/Users/mauroociappina/.gemini/anti_gravity/global_skills/skill_registry.json', 'w') as f:
            json.dump(skills, f, indent=2)
        print("✅ Registry actualizado exitosamente")
    except Exception as e:
        print(f"Error guardando registry: {e}")

def enrich_skills_with_new_fields():
    """Enriquece skills con los nuevos campos."""

    skills = load_skill_registry()
    if not skills:
        return

    # Definir costos y preferencias por cluster
    cluster_costs = {
        'DATA_AI': {'base_cost': 0.05, 'preferred_agent': 'AGENT_Schmidhuber'},
        'SECURITY': {'base_cost': 0.03, 'preferred_agent': 'AGENT_SECURITY'},
        'DEVELOPMENT': {'base_cost': 0.02, 'preferred_agent': 'AGENT_ORCHESTRATOR'},
        'BUSINESS': {'base_cost': 0.04, 'preferred_agent': 'AGENT_BUSINESS'},
        'OPERATIONS': {'base_cost': 0.02, 'preferred_agent': 'AGENT_ORCHESTRATOR'},
        'QUALITY_ASSURANCE': {'base_cost': 0.03, 'preferred_agent': 'AGENT_QA'},
        'INFRASTRUCTURE': {'base_cost': 0.03, 'preferred_agent': 'AGENT_INFRA'},
        'GOVERNANCE': {'base_cost': 0.02, 'preferred_agent': 'AGENT_GOVERNANCE'},
        'INTERFACE': {'base_cost': 0.02, 'preferred_agent': 'AGENT_ORCHESTRATOR'},
        'WEB3': {'base_cost': 0.06, 'preferred_agent': 'AGENT_WEB3'},
        'KNOWLEDGE': {'base_cost': 0.02, 'preferred_agent': 'AGENT_KNOWLEDGE'},
        'UNCATEGORIZED': {'base_cost': 0.02, 'preferred_agent': 'AGENT_ORCHESTRATOR'}
    }

    enriched_count = 0

    for skill in skills:
        # Solo enriquecer skills activos
        if skill.get('status') != 'active':
            continue

        # Si ya tiene los campos, saltar
        if 'inputs' in skill and 'outputs' in skill and 'cost_estimate' in skill:
            continue

        cluster = skill.get('cluster', 'UNCATEGORIZED')
        cost_config = cluster_costs.get(cluster, cluster_costs['UNCATEGORIZED'])

        # Definir inputs/outputs según el tipo de skill
        if 'ai' in skill['name'].lower() or 'llm' in skill['name'].lower():
            inputs = {"task_description": "string", "requirements": "object"}
            outputs = {"implementation": "string", "results": "object"}
        elif 'security' in skill['name'].lower() or 'audit' in skill['name'].lower():
            inputs = {"target": "string", "scope": "object"}
            outputs = {"vulnerabilities": "array", "report": "string"}
        elif 'deploy' in skill['name'].lower() or 'infra' in skill['name'].lower():
            inputs = {"environment": "string", "config": "object"}
            outputs = {"status": "string", "url": "string"}
        elif 'code' in skill['name'].lower() or 'review' in skill['name'].lower():
            inputs = {"code": "string", "context": "object"}
            outputs = {"analysis": "string", "suggestions": "array"}
        else:
            inputs = {"parameters": "object"}
            outputs = {"result": "string"}

        # Añadir los nuevos campos
        skill['inputs'] = inputs
        skill['outputs'] = outputs
        skill['cost_estimate'] = {
            "per_execution": cost_config['base_cost'],
            "currency": "USD",
            "complexity_factor": "medium"
        }
        skill['preferred_agent'] = cost_config['preferred_agent']

        enriched_count += 1
        print(f"✅ Enriquecido: {skill['name']}")

    if enriched_count > 0:
        save_skill_registry(skills)
        print(f"\n📊 Total de skills enriquecidos: {enriched_count}")
    else:
        print("ℹ️  No se encontraron skills que necesiten enriquecimiento")

if __name__ == "__main__":
    enrich_skills_with_new_fields()
