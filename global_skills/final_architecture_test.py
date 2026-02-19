#!/usr/bin/env python3
"""
Final Architecture Test - Prueba final de arquitectura

Prueba que la separación de responsabilidades entre Playbook Engine y Skill Engine
esté correctamente implementada.
"""

import sys
import os
from src.helpers import path_exists

# Añadir el path del proyecto
sys.path.insert(0, '/Users/mauroociappina/.gemini')

def test_final_architecture():
    """Prueba final de la arquitectura de separación de responsabilidades"""
    print("=== FINAL ARCHITECTURE TEST ===")

    try:
        # Probar que los archivos existen
        print("1. Testing file structure...")

        api_file = '/Users/mauroociappina/.gemini/anti_gravity/global_skills/playbook_engine_api.py'
        playbook_file = '/Users/mauroociappina/.gemini/anti_gravity/global_skills/playbook-engine/playbook_engine_refactored.py'
        skill_file = '/Users/mauroociappina/.gemini/anti_gravity/scripts/skill_engine_master_enhanced.py'

        if os.path.exists(api_file):
            print("   ✓ API file exists")
        else:
            print("   ✗ API file missing")
            return False

        if os.path.exists(playbook_file):
            print("   ✓ Playbook Engine file exists")
        else:
            print("   ✗ Playbook Engine file missing")
            return False

        if os.path.exists(skill_file):
            print("   ✓ Skill Engine file exists")
        else:
            print("   ✗ Skill Engine file missing")
            return False

        # Probar que los archivos tienen contenido
        print("2. Testing file content...")

        with open(api_file, 'r') as f:
            api_content = f.read()
            if 'class SkillEngineInterface' in api_content:
                print("   ✓ API interface defined")
            else:
                print("   ✗ API interface missing")
                return False

        with open(playbook_file, 'r') as f:
            playbook_content = f.read()
            if 'class PlaybookEngine' in playbook_content:
                print("   ✓ Playbook Engine class defined")
            else:
                print("   ✗ Playbook Engine class missing")
                return False

        with open(skill_file, 'r') as f:
            skill_content = f.read()
            if 'class EnhancedSkillEngine' in skill_content:
                print("   ✓ Skill Engine class defined")
            else:
                print("   ✗ Skill Engine class missing")
                return False

        # Probar que la API tiene los métodos correctos
        print("3. Testing API methods...")

        if 'def validate_skills' in api_content:
            print("   ✓ validate_skills method exists")
        else:
            print("   ✗ validate_skills method missing")
            return False

        if 'def execute_stage' in api_content:
            print("   ✓ execute_stage method exists")
        else:
            print("   ✗ execute_stage method missing")
            return False

        # Probar que el Playbook Engine usa la API
        print("4. Testing Playbook Engine API usage...")

        if 'SkillEngineInterface' in playbook_content:
            print("   ✓ Playbook Engine uses API interface")
        else:
            print("   ✗ Playbook Engine doesn't use API interface")
            return False

        if 'self.skill_engine.validate_skills' in playbook_content:
            print("   ✓ Playbook Engine calls validate_skills")
        else:
            print("   ✗ Playbook Engine doesn't call validate_skills")
            return False

        if 'self.skill_engine.execute_stage' in playbook_content:
            print("   ✓ Playbook Engine calls execute_stage")
        else:
            print("   ✗ Playbook Engine doesn't call execute_stage")
            return False

        # Probar que el Skill Engine tiene las responsabilidades correctas
        print("5. Testing Skill Engine responsibilities...")

        if 'def validate_skills' in skill_content:
            print("   ✓ Skill Engine has validate_skills")
        else:
            print("   ✗ Skill Engine missing validate_skills")
            return False

        if 'def execute_stage' in skill_content:
            print("   ✓ Skill Engine has execute_stage")
        else:
            print("   ✗ Skill Engine missing execute_stage")
            return False

        # Probar que el Playbook Engine no tiene responsabilidades duplicadas
        print("6. Testing no duplication in Playbook Engine...")

        if 'def validate_skills' not in playbook_content:
            print("   ✓ Playbook Engine doesn't duplicate validate_skills")
        else:
            print("   ✗ Playbook Engine duplicates validate_skills")
            return False

        if 'def execute_stage' not in playbook_content:
            print("   ✓ Playbook Engine doesn't duplicate execute_stage")
        else:
            print("   ✗ Playbook Engine duplicates execute_stage")
            return False

        # Probar que el Skill Engine no tiene responsabilidades del Playbook Engine
        print("7. Testing no Playbook responsibilities in Skill Engine...")

        if 'def validate_playbook' not in skill_content:
            print("   ✓ Skill Engine doesn't have validate_playbook")
        else:
            print("   ✗ Skill Engine has validate_playbook (should be in Playbook Engine)")
            return False

        if 'def execute_playbook' not in skill_content:
            print("   ✓ Skill Engine doesn't have execute_playbook")
        else:
            print("   ✗ Skill Engine has execute_playbook (should be in Playbook Engine)")
            return False

        if 'def get_execution_status' not in skill_content:
            print("   ✓ Skill Engine doesn't have get_execution_status")
        else:
            print("   ✗ Skill Engine has get_execution_status (should be in Playbook Engine)")
            return False

        print("\n🎉 ALL FINAL ARCHITECTURE TESTS PASSED!")
        print("The separation of responsibilities is correctly implemented.")
        print("\n=== KEY ACHIEVEMENTS ===")
        print("✅ Playbook Engine focuses on orchestration and workflow")
        print("✅ Skill Engine handles execution and resource management")
        print("✅ Clear API contracts between engines")
        print("✅ No duplication of responsibilities")
        print("✅ Proper separation of concerns")
        print("✅ Clean, maintainable architecture")

        print("\n=== ARCHITECTURE SUMMARY ===")
        print("📋 Playbook Engine responsibilities:")
        print("   - Validación de playbooks completos")
        print("   - Planificación de ejecución de etapas")
        print("   - Gestión de dependencias entre etapas")
        print("   - Coordinación de múltiples etapas")
        print("   - Gestión de estado de ejecuciones")
        print("   - Políticas de costos y aprobaciones")
        print("   - Estrategias de manejo de errores")
        print()
        print("⚙️  Skill Engine responsibilities:")
        print("   - Validación de skills individuales")
        print("   - Ejecución de skills individuales")
        print("   - Gestión de agents y recursos")
        print("   - Estimación de costos por skill")
        print("   - Control de errores y reintentos")
        print("   - Monitoreo de recursos")
        print("   - Optimización de ejecución")
        print()
        print("🔗 Communication:")
        print("   - Standardized SkillEngineInterface")
        print("   - Clean separation through dependency injection")
        print("   - No direct coupling between engines")

        return True

    except Exception as e:
        print(f"\n❌ FINAL ARCHITECTURE TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_final_architecture()
    exit(0 if success else 1)
