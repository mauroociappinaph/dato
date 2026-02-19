#!/usr/bin/env python3
"""
Demo - Sistema de Monitoreo de Costos The Dude

Este script demuestra el uso completo del sistema de monitoreo de costos.
"""

import sys
import os
from datetime import datetime

# Añadir path del proyecto
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.cost_tracker import CostTracker
from core.alert_manager import AlertManager, AlertType
from config import calculate_cost
from ..src.helpers import get_script_dir


def print_header(title):
    """Imprime un header formateado"""
    print("\n" + "=" * 60)
    print(f"🚀 {title}")
    print("=" * 60)


def demo_cost_tracking():
    """Demo: Tracking de costos"""
    print_header("DEMO 1: TRACKING DE COSTOS")

    # Inicializar tracker
    tracker = CostTracker()

    # Simular ejecuciones de diferentes skills
    print("\n📊 Registrando ejecuciones de skills...")

    executions = [
        {
            "skill": "security-auditor",
            "model": "nvidia/nemotron-4-340b-instruct",  # Ultra tier
            "input": 2000,
            "output": 1500
        },
        {
            "skill": "code-review-excellence",
            "model": "meta/codellama-70b",  # High tier
            "input": 3000,
            "output": 2000
        },
        {
            "skill": "ai-engineer",
            "model": "meta/llama-3.1-70b-instruct",  # High tier
            "input": 2500,
            "output": 1800
        },
        {
            "skill": "domain-strategy-router",
            "model": "meta/llama-3.2-3b-instruct",  # Low tier
            "input": 500,
            "output": 300
        },
    ]

    for exec_data in executions:
        record = tracker.track_execution(
            skill_name=exec_data["skill"],
            model_used=exec_data["model"],
            tokens_input=exec_data["input"],
            tokens_output=exec_data["output"]
        )

        print(f"  ✅ {exec_data['skill']}")
        print(f"     Modelo: {exec_data['model'].split('/')[-1]}")
        print(f"     Tokens: {record.total_tokens} | Costo: ${record.cost_usd:.6f}")

    # Mostrar resumen
    print("\n📈 Resumen de costos (hoy):")
    summary = tracker.get_cost_summary(period="today")
    print(f"  • Ejecuciones: {summary.total_executions}")
    print(f"  • Costo total: ${summary.total_cost:.6f}")
    print(f"  • Tokens totales: {summary.total_tokens}")
    print(f"  • Costo promedio: ${summary.avg_cost_per_execution:.6f}")

    # Top skills
    print("\n🏆 Top skills por costo:")
    top_skills = tracker.get_top_skills(limit=3)
    for i, (skill, cost, count) in enumerate(top_skills, 1):
        print(f"  {i}. {skill}: ${cost:.6f} ({count} ejecuciones)")


def demo_budget_alerts():
    """Demo: Alertas de presupuesto"""
    print_header("DEMO 2: ALERTAS DE PRESUPUESTO")

    # Inicializar managers
    tracker = CostTracker()
    alert_manager = AlertManager()

    # Configurar presupuesto mensual bajo para demo
    print("\n💰 Configurando presupuesto...")
    budget = alert_manager.set_budget_limit(
        amount=0.05,  # $0.05 para demo
        period="monthly",
        alert_thresholds=[50, 75, 90, 100]
    )
    print(f"  ✅ Presupuesto: ${budget.amount_usd} ({budget.period})")
    print(f"  📊 Umbrales: {budget.alert_thresholds}%")

    # Generar ejecuciones costosas para activar alertas
    print("\n⚡ Generando ejecuciones costosas...")

    expensive_executions = [
        ("security-auditor", "nvidia/nemotron-4-340b-instruct", 5000, 3000),
        ("meta-learning-engine", "nvidia/nemotron-4-340b-instruct", 4000, 2500),
        ("hardening-auditor", "meta/llama-3.1-405b-instruct", 6000, 3500),
    ]

    for skill, model, input_toks, output_toks in expensive_executions:
        record = tracker.track_execution(
            skill_name=skill,
            model_used=model,
            tokens_input=input_toks,
            tokens_output=output_toks
        )

        print(f"  💸 {skill}: ${record.cost_usd:.6f}")

        # Verificar presupuesto después de cada ejecución
        current_cost = tracker.get_current_month_cost()
        status = alert_manager.check_budget_status(current_cost, "monthly")

        if status["alert_needed"]:
            print(f"  ⚠️  ALERTA: {status['alert_type'].upper()}!")
            print(f"      Presupuesto: {status['percentage']:.1f}% usado")
            print(f"      Gastado: ${status['current_cost']:.4f} / ${status['budget_limit']:.4f}")

            # Enviar alerta
            alert = alert_manager.check_and_alert(
                current_cost=current_cost,
                period="monthly",
                channels=["log"]
            )

            if alert:
                print(f"      Mensaje: {alert.message}")


def demo_cost_calculator():
    """Demo: Calculadora de costos"""
    print_header("DEMO 3: CALCULADORA DE COSTOS")

    print("\n🧮 Calculando costos estimados...\n")

    scenarios = [
        ("Nemotron 4 340B (Ultra)", "nvidia/nemotron-4-340b-instruct", 1000, 500),
        ("Llama 3.1 405B (Ultra)", "meta/llama-3.1-405b-instruct", 1000, 500),
        ("Llama 3.1 70B (High)", "meta/llama-3.1-70b-instruct", 1000, 500),
        ("CodeLlama 70B (High)", "meta/codellama-70b", 1000, 500),
        ("Llama 3.1 8B (Medium)", "meta/llama-3.1-8b-instruct", 1000, 500),
        ("Llama 3.2 3B (Low)", "meta/llama-3.2-3b-instruct", 1000, 500),
    ]

    print(f"{'Modelo':<25} {'Tier':<8} {'Input':<8} {'Output':<8} {'Costo':<12}")
    print("-" * 70)

    for name, model, input_toks, output_toks in scenarios:
        cost = calculate_cost(model, input_toks, output_toks)
        total = input_toks + output_toks

        # Determinar tier
        if "340b" in model.lower() or "405b" in model.lower():
            tier = "Ultra"
        elif "70b" in model.lower():
            tier = "High"
        elif "8b" in model.lower():
            tier = "Medium"
        else:
            tier = "Low"

        print(f"{name:<25} {tier:<8} {input_toks:<8} {output_toks:<8} ${cost:.6f}")

    print("\n💡 Nota: Los costos son por 1,500 tokens totales")


def demo_dashboard_api():
    """Demo: Endpoints de la API"""
    print_header("DEMO 4: API ENDPOINTS DISPONIBLES")

    endpoints = [
        ("GET", "/", "Información del servicio"),
        ("GET", "/health", "Verificación de salud"),
        ("GET", "/api/costs/summary", "Resumen de costos"),
        ("GET", "/api/costs/trends", "Tendencias de costos"),
        ("GET", "/api/costs/skills", "Top skills por costo"),
        ("GET", "/api/costs/clusters", "Costos por cluster"),
        ("GET", "/api/costs/models", "Costos por modelo"),
        ("POST", "/api/costs/track", "Registrar ejecución"),
        ("GET", "/api/budget/status", "Estado del presupuesto"),
        ("POST", "/api/budget/configure", "Configurar presupuesto"),
        ("GET", "/api/budget/history", "Historial de alertas"),
        ("GET", "/api/export/json", "Exportar a JSON"),
        ("GET", "/api/calculator", "Calcular costo estimado"),
        ("GET", "/api/stats/executions", "Estadísticas de ejecuciones"),
        ("GET", "/api/stats/efficiency", "Estadísticas de eficiencia"),
    ]

    print("\n🌐 Endpoints REST API:\n")
    print(f"{'Método':<8} {'Endpoint':<30} {'Descripción'}")
    print("-" * 70)

    for method, endpoint, description in endpoints:
        print(f"{method:<8} {endpoint:<30} {description}")

    print("\n🚀 Para iniciar el servidor:")
    print("   python -m api.dashboard_api")
    print("\n📱 El servidor estará disponible en:")
    print("   http://localhost:8080")


def demo_export():
    """Demo: Exportación de datos"""
    print_header("DEMO 5: EXPORTACIÓN DE DATOS")

    tracker = CostTracker()

    # Generar algunos datos para exportar
    print("\n📊 Generando datos de ejemplo...")
    for i in range(5):
        tracker.track_execution(
            skill_name=f"demo-skill-{i}",
            model_used="meta/llama-3.1-8b-instruct",
            tokens_input=500,
            tokens_output=300
        )

    # Exportar a JSON
    output_file = "/tmp/cost_monitor_demo_export.json"
    count = tracker.export_to_json(output_file)

    print(f"  ✅ Exportados {count} registros a:")
    print(f"     {output_file}")

    # Mostrar contenido
    import json
    with open(output_file, 'r') as f:
        data = json.load(f)

    print(f"\n📄 Contenido (primer registro):")
    if data:
        first_record = data[0]
        print(f"     ID: {first_record['id']}")
        print(f"     Skill: {first_record['skill_name']}")
        print(f"     Modelo: {first_record['model_used']}")
        print(f"     Costo: ${first_record['cost_usd']}")
        print(f"     Timestamp: {first_record['timestamp']}")


def main():
    """Función principal del demo"""
    print("\n" + "=" * 60)
    print("🎯 THE DUDE - COST MONITOR DEMO")
    print("=" * 60)
    print(f"\nFecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Sistema de Monitoreo de Costos en Tiempo Real")

    try:
        # Ejecutar demos
        demo_cost_tracking()
        demo_budget_alerts()
        demo_cost_calculator()
        demo_dashboard_api()
        demo_export()

        # Resumen final
        print_header("RESUMEN FINAL")
        print("\n✅ Sistema implementado:")
        print("  • Tracking de tokens por skill")
        print("  • Dashboard de costos acumulados")
        print("  • Alertas de presupuesto configurables")
        print("  • API REST completa")
        print("  • Exportación de datos")
        print("  • Tests de integración")

        print("\n🚀 Próximos pasos:")
        print("  1. Integrar con Skill Engine")
        print("  2. Configurar notificaciones Telegram")
        print("  3. Desplegar dashboard web")
        print("  4. Configurar monitoreo continuo")

        print("\n" + "=" * 60)
        print("🎉 DEMO COMPLETADO")
        print("=" * 60 + "\n")

    except Exception as e:
        print(f"\n❌ Error en demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
