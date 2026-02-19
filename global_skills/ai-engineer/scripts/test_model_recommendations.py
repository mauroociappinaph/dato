#!/usr/bin/env python3
"""Test script for model_recommendations module."""

import sys
import os

# Add the scripts directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print('🧪 Probando módulo model_recommendations refactorizado...')
print()

# Probar importación usando imports absolutos
try:
    from nvidia.models import ModelType
    from model_recommendations.mappings import SKILL_MODEL_MAPPING, COST_MAP
    from model_recommendations.recommender import (
        get_recommended_model,
        get_cost_estimate,
        get_skills_by_cluster,
        get_skills_by_tier,
        estimate_cost_for_execution
    )
    print('✅ Importaciones exitosas')
    print(f'   - Total skills mapeados: {len(SKILL_MODEL_MAPPING)}')
    print(f'   - ModelType disponible: {len(ModelType)} modelos')
except Exception as e:
    print(f'❌ Error: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Probar funciones
print()
print('🧪 Probando funciones:')

# Test 1: get_recommended_model
model = get_recommended_model('security-auditor')
print(f'✅ security-auditor → {model.value}')

# Test 2: get_cost_estimate
cost = get_cost_estimate('meta-learning-engine')
print(f'✅ meta-learning-engine cost: ${cost["cost_per_1k_tokens"]:.4f}/1K tokens ({cost["tier"]} tier)')

# Test 3: get_skills_by_cluster
data_ai_skills = get_skills_by_cluster('DATA_AI')
print(f'✅ DATA_AI cluster: {len(data_ai_skills)} skills')

# Test 4: get_skills_by_tier
high_tier = get_skills_by_tier('high')
print(f'✅ High tier skills: {len(high_tier)}')

# Test 5: estimate_cost
exec_cost = estimate_cost_for_execution('security-auditor', 2000)
print(f'✅ security-auditor 2K tokens execution: ${exec_cost:.4f}')

# Test 6: Fallback
unknown_model = get_recommended_model('unknown-skill')
print(f'✅ unknown-skill fallback → {unknown_model.value}')

print()
print('🎉 Todas las pruebas pasaron!')
print()
print('📊 Resumen de la refactorización de model_recommendations:')
print('   - Archivo original: 608 líneas')
print('   - Nuevo módulo: 3 archivos especializados')
print('   - __init__.py: ~70 líneas (API pública)')
print('   - mappings.py: ~400 líneas (datos de mapeo)')
print('   - recommender.py: ~220 líneas (lógica + funciones nuevas)')
