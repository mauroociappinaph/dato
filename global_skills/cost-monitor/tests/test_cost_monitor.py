#!/usr/bin/env python3
"""
Test Suite para Cost Monitor

Tests de integración para verificar el funcionamiento completo del sistema.
"""

import sys
import os
import unittest
import tempfile
import shutil
from datetime import datetime, timedelta

# Añadir path del proyecto
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cost_monitor.core.cost_tracker import CostTracker
from cost_monitor.core.alert_manager import AlertManager, AlertType
from cost_monitor.config import calculate_cost, get_tier_for_skill


class TestCostTracker(unittest.TestCase):
    """Tests para CostTracker"""

    def setUp(self):
        """Setup antes de cada test"""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_costs.db")
        self.tracker = CostTracker(db_path=self.db_path)

    def tearDown(self):
        """Cleanup después de cada test"""
        shutil.rmtree(self.temp_dir)

    def test_track_execution(self):
        """Test: Registrar una ejecución"""
        record = self.tracker.track_execution(
            skill_name="security-auditor",
            model_used="nvidia/nemotron-4-340b-instruct",
            tokens_input=1000,
            tokens_output=500
        )

        self.assertIsNotNone(record.id)
        self.assertEqual(record.skill_name, "security-auditor")
        self.assertEqual(record.tokens_input, 1000)
        self.assertEqual(record.tokens_output, 500)
        self.assertEqual(record.total_tokens, 1500)
        self.assertGreater(record.cost_usd, 0)
        print(f"✅ Track execution: ${record.cost_usd:.6f}")

    def test_cost_calculation(self):
        """Test: Cálculo de costos"""
        # Ultra tier: $0.004 por 1K tokens
        cost = calculate_cost(
            "nvidia/nemotron-4-340b-instruct",
            tokens_input=1000,
            tokens_output=1000
        )
        expected = 2000 * (0.004 / 1000)  # $0.008
        self.assertAlmostEqual(cost, expected, places=6)
        print(f"✅ Cost calculation: ${cost:.6f}")

    def test_cost_summary(self):
        """Test: Resumen de costos"""
        # Crear algunos registros
        for i in range(5):
            self.tracker.track_execution(
                skill_name=f"skill-{i}",
                model_used="meta/llama-3.1-8b-instruct",
                tokens_input=100,
                tokens_output=100
            )

        summary = self.tracker.get_cost_summary(period="today")

        self.assertEqual(summary.total_executions, 5)
        self.assertGreater(summary.total_cost, 0)
        self.assertEqual(len(summary.skill_breakdown), 5)
        print(f"✅ Cost summary: {summary.total_executions} executions, ${summary.total_cost:.6f}")

    def test_top_skills(self):
        """Test: Top skills por costo"""
        # Crear registros con diferentes costos
        self.tracker.track_execution(
            skill_name="expensive-skill",
            model_used="nvidia/nemotron-4-340b-instruct",
            tokens_input=10000,
            tokens_output=5000
        )

        for i in range(3):
            self.tracker.track_execution(
                skill_name=f"cheap-skill-{i}",
                model_used="meta/llama-3.2-3b-instruct",
                tokens_input=100,
                tokens_output=50
            )

        top_skills = self.tracker.get_top_skills(limit=2)

        self.assertEqual(len(top_skills), 2)
        self.assertEqual(top_skills[0][0], "expensive-skill")
        print(f"✅ Top skills: {top_skills[0][0]} (${top_skills[0][1]:.6f})")

    def test_cost_trends(self):
        """Test: Tendencias de costos"""
        # Crear registros
        for i in range(3):
            self.tracker.track_execution(
                skill_name="test-skill",
                model_used="meta/llama-3.1-8b-instruct",
                tokens_input=100,
                tokens_output=100
            )

        trends = self.tracker.get_cost_trends(days=7)

        self.assertGreaterEqual(len(trends), 1)
        self.assertIn("date", trends[0])
        self.assertIn("cost", trends[0])
        print(f"✅ Cost trends: {len(trends)} days")


class TestAlertManager(unittest.TestCase):
    """Tests para AlertManager"""

    def setUp(self):
        """Setup antes de cada test"""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_alerts.db")
        self.alert_manager = AlertManager(db_path=self.db_path)

    def tearDown(self):
        """Cleanup después de cada test"""
        shutil.rmtree(self.temp_dir)

    def test_set_budget(self):
        """Test: Configurar presupuesto"""
        config = self.alert_manager.set_budget_limit(
            amount=100.0,
            period="monthly",
            alert_thresholds=[50, 75, 90, 100]
        )

        self.assertIsNotNone(config.id)
        self.assertEqual(config.amount_usd, 100.0)
        self.assertEqual(config.period, "monthly")
        self.assertEqual(len(config.alert_thresholds), 4)
        print(f"✅ Budget set: ${config.amount_usd} ({config.period})")

    def test_check_budget_status(self):
        """Test: Verificar estado del presupuesto"""
        # Configurar presupuesto
        self.alert_manager.set_budget_limit(
            amount=100.0,
            period="monthly"
        )

        # Verificar estado al 50%
        status = self.alert_manager.check_budget_status(50.0, "monthly")

        self.assertTrue(status["has_budget"])
        self.assertEqual(status["budget_limit"], 100.0)
        self.assertEqual(status["current_cost"], 50.0)
        self.assertEqual(status["percentage"], 50.0)
        print(f"✅ Budget status: {status['percentage']}%")

    def test_alert_triggering(self):
        """Test: Activación de alertas"""
        # Configurar presupuesto
        self.alert_manager.set_budget_limit(
            amount=100.0,
            period="monthly",
            alert_thresholds=[75, 100]
        )

        # Verificar a 75% (debe activar warning)
        status = self.alert_manager.check_budget_status(75.0, "monthly")

        self.assertTrue(status["alert_needed"])
        self.assertEqual(status["threshold_triggered"], 75)
        print(f"✅ Alert triggered at {status['threshold_triggered']}%")

    def test_alert_cooldown(self):
        """Test: Cooldown de alertas"""
        should_send = self.alert_manager.should_send_alert(
            AlertType.WARNING,
            threshold=75
        )
        self.assertTrue(should_send)

        # Inmediatamente después, no debería enviar
        should_send = self.alert_manager.should_send_alert(
            AlertType.WARNING,
            threshold=75
        )
        self.assertFalse(should_send)
        print(f"✅ Alert cooldown working")


class TestIntegration(unittest.TestCase):
    """Tests de integración"""

    def setUp(self):
        """Setup"""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_integration.db")
        self.tracker = CostTracker(db_path=self.db_path)
        self.alert_manager = AlertManager(db_path=self.db_path)

    def tearDown(self):
        """Cleanup"""
        shutil.rmtree(self.temp_dir)

    def test_full_workflow(self):
        """Test: Flujo completo de tracking + alertas"""
        print("\n🧪 Testing full workflow...")

        # 1. Configurar presupuesto mensual
        self.alert_manager.set_budget_limit(
            amount=1.0,  # $1.00 para que se active rápido
            period="monthly",
            alert_thresholds=[50, 100]
        )
        print("  ✓ Budget configured")

        # 2. Registrar algunas ejecuciones
        models = [
            "meta/llama-3.1-8b-instruct",  # Medium tier
            "meta/llama-3.1-70b-instruct",  # High tier
        ]

        for i in range(5):
            record = self.tracker.track_execution(
                skill_name=f"test-skill-{i}",
                model_used=models[i % len(models)],
                tokens_input=1000,
                tokens_output=500
            )
            print(f"  ✓ Tracked execution {i+1}: ${record.cost_usd:.6f}")

        # 3. Verificar resumen
        summary = self.tracker.get_cost_summary(period="today")
        print(f"  ✓ Summary: {summary.total_executions} executions, ${summary.total_cost:.6f}")

        # 4. Verificar alertas
        current_cost = self.tracker.get_current_month_cost()
        status = self.alert_manager.check_budget_status(current_cost, "monthly")
        print(f"  ✓ Budget check: {status['percentage']:.1f}% used")

        # 5. Si hay alerta, mostrarla
        if status["alert_needed"]:
            print(f"  ⚠️  ALERT: {status['alert_type']} at {status['threshold_triggered']}%")

        self.assertGreater(summary.total_executions, 0)
        self.assertGreater(summary.total_cost, 0)


def run_tests():
    """Ejecutar todos los tests"""
    print("=" * 60)
    print("🧪 COST MONITOR - TEST SUITE")
    print("=" * 60)

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Añadir tests
    suite.addTests(loader.loadTestsFromTestCase(TestCostTracker))
    suite.addTests(loader.loadTestsFromTestCase(TestAlertManager))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Resumen
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    if result.wasSuccessful():
        print("\n✅ ALL TESTS PASSED!")
        return 0
    else:
        print("\n❌ SOME TESTS FAILED")
        return 1


if __name__ == "__main__":
    exit(run_tests())
