#!/usr/bin/env python3
"""
NVIDIA NIM Client - Backward Compatibility Layer

⚠️ DEPRECATED: Este archivo se mantiene solo para compatibilidad.
Por favor usa el nuevo módulo modular:

    from nvidia import NVIDIANIMClient, get_nim_client, ModelType

El nuevo paquete modular proporciona:
- Mejor organización del código
- Testabilidad mejorada
- Separación de responsabilidades
- Mantenimiento simplificado

Este archivo será removido en la versión 2.0.
"""

import warnings

# Emitir advertencia de deprecación
warnings.warn(
    "nvidia_nim_client.py is deprecated. "
    "Use 'from nvidia import NVIDIANIMClient' instead. "
    "This module will be removed in version 2.0.",
    DeprecationWarning,
    stacklevel=2
)

# Re-exportar todo desde el nuevo módulo modular
from .nvidia import (
    # Models
    ModelType,
    NIMResponse,
    UsageStats,
    ModelConfig,
    DEFAULT_CONFIG,
    get_model_tier,
    calculate_cost,
    # Fallback
    OllamaFallback,
    map_model_to_ollama,
    # Circuit Breaker
    CircuitBreakerWrapper,
    NIMCIRCUITConfig,
    create_nvidia_circuit,
    with_circuit_breaker,
    NIMCircuitBreakerManager,
    get_circuit_manager,
    CircuitBreaker,
    CircuitBreakerOpenException,
    CircuitState,
    # Client
    NVIDIANIMClient,
    get_nim_client,
    generate,
    generate_async,
)

# Mantener compatibilidad con imports antiguos
__all__ = [
    "ModelType",
    "NIMResponse",
    "NVIDIANIMClient",
    "get_nim_client",
    "generate",
    "generate_async",
    "CircuitBreaker",
    "CircuitBreakerOpenException",
    "CircuitState",
    "OllamaFallback",
]
