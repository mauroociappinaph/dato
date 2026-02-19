#!/usr/bin/env python3
"""
Alert Manager Notifier - Delivery channels.
"""

import json
import logging
from .models import AlertRecord

logger = logging.getLogger(__name__)

class AlertNotifier:
    """Gestor de canales de envío para alertas"""

    def send_by_channel(self, channel: str, alert: AlertRecord):
        """Envía una alerta por el canal especificado"""
        if channel == "telegram":
            self._send_telegram(alert)
        elif channel == "email":
            self._send_email(alert)
        elif channel == "dashboard":
            self._send_dashboard(alert)
        elif channel == "log":
            self._send_log(alert)

    def _send_telegram(self, alert: AlertRecord):
        """Envía alerta por Telegram"""
        emoji_map = {
            "warning": "🟡",
            "caution": "🟠",
            "critical": "🔴",
            "daily_summary": "📊",
            "anomaly": "🚨"
        }
        emoji = emoji_map.get(alert.alert_type, "📢")
        percentage = (alert.cost_at_alert / alert.budget_limit) * 100
        message = f"""
{emoji} *ALERTA DE PRESUPUESTO - THE DUDE*

*{alert.message}*

💰 *Estado:*
• Gastado: ${alert.cost_at_alert:.2f} / ${alert.budget_limit:.2f}
• Porcentaje: {percentage:.1f}%
• Umbral: {alert.threshold_percent}%

⏰ *Fecha:* {alert.timestamp.strftime("%Y-%m-%d %H:%M")}
"""
        print(f"📤 [Telegram] {message}")

    def _send_email(self, alert: AlertRecord):
        """Envía alerta por email"""
        print(f"📧 [Email] {alert.alert_type}: {alert.message}")

    def _send_dashboard(self, alert: AlertRecord):
        """Envía alerta al dashboard"""
        print(f"📊 [Dashboard] {alert.alert_type}: {alert.message}")

    def _send_log(self, alert: AlertRecord):
        """Registra alerta en logs"""
        emoji_map = {
            "warning": "🟡",
            "caution": "🟠",
            "critical": "🔴",
            "daily_summary": "📊",
            "anomaly": "🚨"
        }
        emoji = emoji_map.get(alert.alert_type, "📢")
        print(f"{emoji} [{alert.timestamp}] {alert.alert_type.upper()}: {alert.message}")
