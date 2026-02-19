#!/usr/bin/env python3
"""
Approval Gateway - Sistema de aprobaciones para playbooks.

Este archivo contiene la clase principal ApprovalGateway que gestiona
solicitudes de aprobación, decisiones y notificaciones.
"""

import asyncio
import json
import logging
import uuid
from dataclasses import asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

# Importaciones locales
from .models import (
    ApprovalRequest,
    ApprovalStatus,
    ApprovalType,
    ApprovalPolicy,
    ApprovalDecision
)
from .notifications import NotificationManager
from .policies import PolicyEngine

logger = logging.getLogger(__name__)


class ApprovalGateway:
    """Sistema de aprobaciones para playbooks"""

    def __init__(self, skill_engine=None):
        self.skill_engine = skill_engine
        self.approvals_dir = Path("approvals")
        self.approvals_dir.mkdir(exist_ok=True)

        # Estado de solicitudes activas
        self.active_requests: Dict[str, ApprovalRequest] = {}

        # Sub-módulos especializados
        self.policy_engine = PolicyEngine()
        self.notification_manager = NotificationManager(self)

    async def check_approval_required(
        self,
        playbook_data: Dict[str, Any],
        context: Dict[str, Any] = None
    ) -> bool:
        """Verifica si se requiere aprobación según políticas"""
        return self.policy_engine.check_approval_required(playbook_data, context)

    async def create_approval_request(
        self,
        playbook_name: str,
        stage_name: Optional[str],
        request_type: ApprovalType,
        reason: str,
        metadata: Dict[str, Any],
        approvers: List[str],
        expires_in_minutes: int = 60
    ) -> ApprovalRequest:
        """Crea una solicitud de aprobación"""
        request_id = str(uuid.uuid4())
        expires_at = datetime.now() + timedelta(minutes=expires_in_minutes)

        approval_request = ApprovalRequest(
            request_id=request_id,
            playbook_name=playbook_name,
            stage_name=stage_name,
            request_type=request_type,
            reason=reason,
            metadata=metadata,
            created_at=datetime.now(),
            expires_at=expires_at,
            status=ApprovalStatus.PENDING,
            approvers=approvers,
            decision=None,
            notifications_sent=[]
        )

        self.active_requests[request_id] = approval_request

        # Enviar notificaciones
        await self.notification_manager.send_notifications(approval_request)

        # Iniciar temporizador de expiración
        if expires_at:
            asyncio.create_task(self._handle_expiration(approval_request))

        logger.info(f"Solicitud de aprobación creada: {request_id} para {playbook_name}")
        return approval_request

    async def _handle_expiration(self, request: ApprovalRequest):
        """Maneja la expiración de solicitudes"""
        if not request.expires_at:
            return

        await asyncio.sleep((request.expires_at - datetime.now()).total_seconds())

        if request.status == ApprovalStatus.PENDING:
            request.status = ApprovalStatus.EXPIRED
            logger.warning(f"Solicitud de aprobación expirada: {request.request_id}")

    async def approve_request(self, request_id: str, approver: str, comment: str = "") -> bool:
        """Aprueba una solicitud de aprobación"""
        request = self.active_requests.get(request_id)
        if not request:
            logger.error(f"Solicitud no encontrada: {request_id}")
            return False

        if request.status != ApprovalStatus.PENDING:
            logger.error(f"Solicitud no está pendiente: {request_id}")
            return False

        # Registrar decisión
        if request.decision is None:
            request.decision = {
                "approvals": [],
                "rejections": [],
                "final_decision": None,
                "finalized_at": None
            }

        request.decision["approvals"].append({
            "approver": approver,
            "comment": comment,
            "timestamp": datetime.now().isoformat()
        })

        # Verificar si se alcanza el quórum
        await self._check_quorum(request)

        logger.info(f"Solicitud aprobada por {approver}: {request_id}")
        return True

    async def reject_request(self, request_id: str, approver: str, reason: str = "") -> bool:
        """Rechaza una solicitud de aprobación"""
        request = self.active_requests.get(request_id)
        if not request:
            logger.error(f"Solicitud no encontrada: {request_id}")
            return False

        if request.status != ApprovalStatus.PENDING:
            logger.error(f"Solicitud no está pendiente: {request_id}")
            return False

        # Rechazo inmediato (política de veto)
        request.status = ApprovalStatus.REJECTED
        request.decision = {
            "approvals": [],
            "rejections": [{
                "approver": approver,
                "reason": reason,
                "timestamp": datetime.now().isoformat()
            }],
            "final_decision": "rejected",
            "finalized_at": datetime.now().isoformat()
        }

        logger.info(f"Solicitud rechazada por {approver}: {request_id}")
        return True

    async def _check_quorum(self, request: ApprovalRequest):
        """Verifica si se alcanza el quórum de aprobaciones"""
        if request.decision is None:
            return

        approvals = len(request.decision["approvals"])
        rejections = len(request.decision["rejections"])

        # Si hay rechazos, se rechaza inmediatamente
        if rejections > 0:
            request.status = ApprovalStatus.REJECTED
            request.decision["final_decision"] = "rejected"
            request.decision["finalized_at"] = datetime.now().isoformat()
            return

        # Verificar quórum requerido
        required_quorum = request.metadata.get("quorum", len(request.approvers))

        if approvals >= required_quorum:
            request.status = ApprovalStatus.APPROVED
            request.decision["final_decision"] = "approved"
            request.decision["finalized_at"] = datetime.now().isoformat()

    async def get_request_status(self, request_id: str) -> Optional[ApprovalRequest]:
        """Obtiene el estado de una solicitud"""
        return self.active_requests.get(request_id)

    def list_pending_requests(self) -> List[ApprovalRequest]:
        """Lista solicitudes pendientes"""
        return [
            req for req in self.active_requests.values()
            if req.status == ApprovalStatus.PENDING
        ]

    async def get_approval_history(
        self,
        playbook_name: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Obtiene el historial de aprobaciones"""
        history = []

        for request in self.active_requests.values():
            if playbook_name and request.playbook_name != playbook_name:
                continue

            history.append({
                'request_id': request.request_id,
                'playbook_name': request.playbook_name,
                'stage_name': request.stage_name,
                'status': request.status.value,
                'created_at': request.created_at.isoformat(),
                'decision': request.decision
            })

        return history

    async def cancel_request(self, request_id: str, reason: str = "") -> bool:
        """Cancela una solicitud de aprobación"""
        request = self.active_requests.get(request_id)
        if not request:
            return False

        request.status = ApprovalStatus.CANCELLED
        logger.info(f"Solicitud cancelada: {request_id} - {reason}")
        return True

    def export_approvals_to_json(self, output_path: str):
        """Exporta el estado actual de aprobaciones a JSON"""
        data = {
            'active_requests': [
                asdict(req) for req in self.active_requests.values()
            ],
            'policies': [
                asdict(policy) for policy in self.policy_engine.policies
            ],
            'exported_at': datetime.now().isoformat()
        }

        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)

        logger.info(f"Exportación de aprobaciones guardada en: {output_path}")

    async def cleanup_expired_requests(self):
        """Limpia solicitudes expiradas"""
        now = datetime.now()
        expired_requests = []

        for request_id, request in self.active_requests.items():
            if (request.expires_at and
                request.expires_at < now and
                request.status == ApprovalStatus.PENDING):
                request.status = ApprovalStatus.EXPIRED
                expired_requests.append(request_id)

        for request_id in expired_requests:
            del self.active_requests[request_id]

        if expired_requests:
            logger.info(f"Limpieza de {len(expired_requests)} solicitudes expiradas")

    async def batch_approve(
        self,
        request_ids: List[str],
        approver: str,
        comment: str = ""
    ) -> Dict[str, bool]:
        """Aprueba múltiples solicitudes en lote"""
        results = {}

        for request_id in request_ids:
            success = await self.approve_request(request_id, approver, comment)
            results[request_id] = success

        return results

    async def batch_reject(
        self,
        request_ids: List[str],
        approver: str,
        reason: str = ""
    ) -> Dict[str, bool]:
        """Rechaza múltiples solicitudes en lote"""
        results = {}

        for request_id in request_ids:
            success = await self.reject_request(request_id, approver, reason)
            results[request_id] = success

        return results

    # Delegación a PolicyEngine
    @property
    def policies(self) -> List[ApprovalPolicy]:
        """Acceso a políticas del motor de políticas"""
        return self.policy_engine.policies

    async def evaluate_policies(
        self,
        playbook_data: Dict[str, Any],
        context: Dict[str, Any]
    ) -> List[ApprovalPolicy]:
        """Delegación a PolicyEngine"""
        return await self.policy_engine.evaluate_policies(playbook_data, context)

    async def create_approval_policy(
        self,
        name: str,
        description: str,
        conditions: Dict[str, Any],
        actions: Dict[str, Any],
        priority: int = 1
    ) -> ApprovalPolicy:
        """Delegación a PolicyEngine"""
        return await self.policy_engine.create_policy(
            name, description, conditions, actions, priority
        )

    def list_approval_policies(self) -> List[ApprovalPolicy]:
        """Delegación a PolicyEngine"""
        return self.policy_engine.list_policies()
