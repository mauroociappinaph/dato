#!/usr/bin/env python3
"""
Ejemplo de uso del sistema de control de costos con skills.
"""

import asyncio
import sys
from pathlib import Path

# Añadir el path para importar el controlador
sys.path.append(str(Path(__file__).parent.parent.parent.parent / 'cost-control' / 'scripts'))

from mcp_cost_controller import MCPCostController

async def main():
    """Ejemplo de uso del controlador de costos con skills."""

    controller = MCPCostController()

    print("💰 Sistema de Control de Costos para Skills")
    print("=" * 50)

    # Ejemplo 1: Verificar costo de un skill
    print("\n1. Verificando costo de skills:")
    skills_to_check = ['web-command-center', 'ai-engineer', 'code-reviewer']

    for skill_id in skills_to_check:
        cost = await controller.get_skill_cost_estimate(skill_id)
        print(f"   {skill_id}: ${cost:.4f}")

    # Ejemplo 2: Verificar cuota para un agente
    print("\n2. Verificando cuota para AGENT_SALES:")
    agent_id = "AGENT_SALES"

    for skill_id in skills_to_check:
        can_use = await controller.check_skill_cost_quota(agent_id, skill_id)
        status = "✅ Permitido" if can_use else "❌ Denegado"
        print(f"   {skill_id}: {status}")

    # Ejemplo 3: Simular uso de skills
    print("\n3. Simulando uso de skills:")

    for skill_id in skills_to_check:
        cost = await controller.get_skill_cost_estimate(skill_id)
        if cost > 0:
            await controller.record_usage('skill', agent_id, cost)
            print(f"   ✅ Usado {skill_id} - Costo: ${cost:.4f}")

    # Ejemplo 4: Ver estadísticas
    print("\n4. Estadísticas de uso:")
    stats = await controller.get_usage_stats(agent_id)
    print(f"   Llamadas totales: {stats.get('total_calls', 0)}")
    print(f"   Costo total: ${stats.get('total_cost', 0):.2f}")

    print("\n✅ Ejemplo completado exitosamente!")

if __name__ == "__main__":
    asyncio.run(main())
