#!/usr/bin/env python3
"""
Basic Test - Prueba básica de los motores

Prueba simple para verificar que la arquitectura funciona correctamente.
"""

import sys
import os

# Añadir el path del proyecto
sys.path.insert(0, '/Users/mauroociappina/.gemini')

def test_basic_functionality():
    """Prueba básica de funcionalidad"""
    print("=== BASIC FUNCTIONALITY TEST ===")

    try:
        # Probar import de la API
        print("1. Testing API imports...")
        from anti_gravity.global_skills.playbook_engine_api import (
            SkillRequest, StageRequest, CostEstimation, ExecutionStatus
        )
        print("   ✓ API imports successful")

        # Probar creación de objetos
        print("2. Testing object creation...")
        skill_request = SkillRequest(
            skill_name='test_skill',
            agent_name='default',
            timeout=30
        )
        print(f"   ✓ SkillRequest created: {skill_request.skill_name}")

        stage_request = StageRequest(
            stage_name='test_stage',
            skills=[skill_request],
            parallel=True
        )
        print(f"   ✓ StageRequest created: {stage_request.stage_name}")

        # Probar import del Playbook Engine
        print("3. Testing Playbook Engine import...")
        from anti_gravity.global_skills.playbook_engine.playbook_engine_refactored import PlaybookEngine
        print("   ✓ Playbook Engine import successful")

        # Probar import del Skill Engine
        print("4. Testing Skill Engine import...")
        from anti_gravity.scripts.skill_engine_master_enhanced import enhanced_skill_engine
        print("   ✓ Skill Engine import successful")

        # Probar instanciación del Playbook Engine
        print("5. Testing Playbook Engine instantiation...")
        playbook_engine = PlaybookEngine(enhanced_skill_engine)
        print("   ✓ Playbook Engine instantiated")

        # Probar métodos básicos
        print("6. Testing basic methods...")
        playbooks = playbook_engine.list_playbooks()
        print(f"   ✓ Found {len(playbooks)} playbooks")

        # Probar métodos del Skill Engine
        print("7. Testing Skill Engine methods...")
        agent_status = enhanced_skill_engine.get_agent_status()
        print(f"   ✓ Agent status: {list(agent_status.keys())}")

        registry_status = enhanced_skill_engine.get_skill_registry_status()
        print(f"   ✓ Registry status: {registry_status['total_skills']} skills")

        metrics = enhanced_skill_engine.get_execution_metrics()
        print(f"   ✓ Execution metrics: {metrics}")

        print("\n🎉 ALL BASIC TESTS PASSED!")
        print("The separation of responsibilities is working correctly.")
        return True

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_basic_functionality()
    exit(0 if success else 1)
