#!/usr/bin/env python3
"""
NVIDIA NIM Package - Módulo modular para integración con NVIDIA AI Foundation Models.

Este paquete proporciona acceso a modelos como Llama 3, Nemotron, Mistral, etc.
con protección de Circuit Breaker y fallback automático a Ollama.

Usage:
    # Importación completa
    from nvidia import NVIDIANIMClient, get_nim_client, ModelType

    # Uso rápido
    client = get_nim_client()
    response = client.generate("Explain quantum computing")
    print(response.text)

    # Con modelo específico
    response = client.generate(
        "Write Python code",
        model=ModelType.CODELLAMA_70B
    )

Submodules:
    - models: Definiciones de modelos (ModelType, NIMResponse, etc.)
    - fallback: Lógica de fallback a Ollama
    - circuit_breaker_integration: Protección de circuit breaker
    - client: Cliente principal NVIDIANIMClient
"""

# Version
__version__ = "1.0.0"

# Core imports
from .models import (
    ModelType,
    NIMResponse,
    UsageStats,
    ModelConfig,
    DEFAULT_CONFIG,
    get_model_tier,
    calculate_cost,
)

from .fallback import (
    OllamaFallback,
    map_model_to_ollama,
)

from .circuit_breaker_integration import (
    CircuitBreakerWrapper,
    NIMCIRCUITConfig,
    create_nvidia_circuit,
    with_circuit_breaker,
    NIMCircuitBreakerManager,
    get_circuit_manager,
    CircuitBreaker,
    CircuitBreakerOpenException,
    CircuitState,
)

from .client import (
    NVIDIANIMClient,
    get_nim_client,
    generate,
    generate_async,
)

# Public API
__all__ = [
    # Models
    "ModelType",
    "NIMResponse",
    "UsageStats",
    "ModelConfig",
    "DEFAULT_CONFIG",
    "get_model_tier",
    "calculate_cost",
    # Fallback
    "OllamaFallback",
    "map_model_to_ollama",
    # Circuit Breaker
    "CircuitBreakerWrapper",
    "NIMCIRCUITConfig",
    "create_nvidia_circuit",
    "with_circuit_breaker",
    "NIMCircuitBreakerManager",
    "get_circuit_manager",
    "CircuitBreaker",
    "CircuitBreakerOpenException",
    "CircuitState",
    # Client
    "NVIDIANIMClient",
    "get_nim_client",
    "generate",
    "generate_async",
]
