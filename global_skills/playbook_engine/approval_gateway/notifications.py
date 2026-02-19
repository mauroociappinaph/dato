#!/usr/bin/env python3
"""
Approval Gateway Notifications - Sistema de notificaciones.

Este archivo contiene la lógica para enviar notificaciones
a través de múltiples canales (Telegram, Email, Webhook, Consola).
"""

import json
import logging
from datetime import datetime
from typing import TYPE_CHECKING

from .models import ApprovalRequest, NotificationChannel

if TYPE_CHECKING:
    from .gateway import ApprovalGateway

logger = logging.getLogger(__name__)


class NotificationManager:
    """Gestor de notificaciones para solicitudes de aprobación"""

    def __init__(self, gateway: "ApprovalGateway"):
        self.gateway = gateway
        self.notification_channels = {
            NotificationChannel.TELEGRAM: self._send_telegram,
            NotificationChannel.EMAIL: self._send_email,
            NotificationChannel.WEBHOOK: self._send_webhook,
            NotificationChannel.CONSOLE: self._send_console
        }

    async def send_notifications(self, request: ApprovalRequest):
        """Envía notificaciones a los aprobadores"""
        message = self._format_approval_message(request)

        for approver in request.approvers:
            # Intentar enviar por diferentes canales
            for channel in [
                NotificationChannel.TELEGRAM,
                NotificationChannel.EMAIL,
                NotificationChannel.CONSOLE
            ]:
                try:
                    await self.notification_channels[channel](approver, message, request)
                    request.notifications_sent.append(f"{channel.value}:{approver}")
                    logger.info(f"Notificación enviada a {approver} por {channel.value}")
                    break  # Si tiene éxito, no intentar otros canales
                except Exception as e:
                    logger.warning(
                        f"Error enviando notificación a {approver} por {channel.value}: {e}"
                    )
                    continue

    def _format_approval_message(self, request: ApprovalRequest) -> str:
        """Formatea el mensaje de aprobación"""
        stage_info = f" en la etapa '{request.stage_name}'" if request.stage_name else ""

        message = f"""
SOLICITUD DE APROBACIÓN - PLAYBOOK

Playbook: {request.playbook_name}{stage_info}
Tipo: {request.request_type.value}
Motivo: {request.reason}
ID: {request.request_id}
Creado: {request.created_at.strftime('%Y-%m-%d %H:%M:%S')}

Metadatos:
{json.dumps(request.metadata, indent=2)}

Acciones disponibles:
- Aprobar: /approve {request.request_id}
- Rechazar: /reject {request.request_id}
- Ver detalles: /details {request.request_id}
"""
        return message

    async def _send_telegram(self, recipient: str, message: str, request: ApprovalRequest):
        """Envía notificación por Telegram"""
        # En producción, aquí iría la integración con Telegram
        logger.info(f"Telegram notification to {recipient}: {message[:100]}...")

    async def _send_email(self, recipient: str, message: str, request: ApprovalRequest):
        """Envía notificación por email"""
        # En producción, aquí iría la integración con SMTP
        logger.info(f"Email notification to {recipient}: {message[:100]}...")

    async def _send_webhook(self, recipient: str, message: str, request: ApprovalRequest):
        """Envía notificación por webhook"""
        # En producción, aquí iría la integración con webhooks
        logger.info(f"Webhook notification to {recipient}: {message[:100]}...")

    async def _send_console(self, recipient: str, message: str, request: ApprovalRequest):
        """Envía notificación por consola"""
        print(f"\n{'='*60}")
        print(message)
        print(f"{'='*60}\n")
