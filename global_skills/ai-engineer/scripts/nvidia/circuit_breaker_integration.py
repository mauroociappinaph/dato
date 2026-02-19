#!/usr/bin/env python3
"""
NVIDIA NIM Circuit Breaker Integration

Integración del Circuit Breaker con NVIDIA NIM Client.
Proporciona wrappers y utilidades específicas para manejo de fallos
y fallback automático a Ollama.

Usage:
    from circuit_breaker_integration import (
        NIMCIRCUITConfig,
        with_circuit_breaker,
        create_nvidia_circuit
    )

    @with_circuit_breaker(fallback_enabled=True)
    async def generate_with_protection(client, prompt):
        return await client.generate(prompt)
"""

import asyncio
import logging
from dataclasses import dataclass
from functools import wraps
from typing import Any, Callable, Optional, TypeVar, Union

# Import Circuit Breaker from parent directory
try:
    from ..circuit_breaker import (
        CircuitBreaker,
        CircuitBreakerConfig,
        CircuitBreakerOpenException,
        CircuitState,
        create_nvidia_circuit_breaker,
        registry
    )
except ImportError:
    # Fallback for direct execution
    import sys
    import os
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    from circuit_breaker import (
        CircuitBreaker,
        CircuitBreakerConfig,
        CircuitBreakerOpenException,
        CircuitState,
        create_nvidia_circuit_breaker,
        registry
    )

from .models import NIMResponse, UsageStats
from .fallback import OllamaFallback, map_model_to_ollama

# Logging
logger = logging.getLogger(__name__)

T = TypeVar('T')


@dataclass
class NIMCIRCUITConfig:
    """Configuración específica para Circuit Breaker de NVIDIA NIM.

    Attributes:
        failure_threshold: Fallos antes de abrir el circuito
        recovery_timeout: Segundos antes de intentar recuperación
        fallback_enabled: Si se usa Ollama como fallback
        fallback_on_reject: Si se usa fallback cuando el circuito rechaza
        track_metrics: Si se registran métricas detalladas
    """
    failure_threshold: int = 5
    recovery_timeout: float = 30.0
    fallback_enabled: bool = True
    fallback_on_reject: bool = True
    track_metrics: bool = True


def create_nvidia_circuit(
    name: str = "nvidia_nim",
    config: Optional[NIMCIRCUITConfig] = None
) -> CircuitBreaker:
    """Crear circuit breaker configurado para NVIDIA NIM.

    Args:
        name: Nombre identificador del circuito
        config: Configuración específica de NIM

    Returns:
        CircuitBreaker configurado
    """
    cfg = config or NIMCIRCUITConfig()

    circuit = create_nvidia_circuit_breaker(
        name=name,
        failure_threshold=cfg.failure_threshold,
        recovery_timeout=cfg.recovery_timeout
    )

    logger.info(f"Created NVIDIA circuit breaker: {name}")
    return circuit


class CircuitBreakerWrapper:
    """Wrapper que integra Circuit Breaker + Fallback para NVIDIA NIM.

    Esta clase envuelve las llamadas a NVIDIA NIM con:
    - Protección de Circuit Breaker
    - Fallback automático a Ollama
    - Métricas integradas
    - Logging detallado

    Example:
        >>> wrapper = CircuitBreakerWrapper()
        >>> result = await wrapper.call(
        ...     nvidia_client.generate,
        ...     prompt="Hello",
        ...     model=ModelType.LLAMA_8B
        ... )
    """

    def __init__(
        self,
        circuit: Optional[CircuitBreaker] = None,
        fallback: Optional[OllamaFallback] = None,
        config: Optional[NIMCIRCUITConfig] = None
    ):
        self.config = config or NIMCIRCUITConfig()
        self.circuit = circuit or create_nvidia_circuit(config=self.config)
        self.fallback = fallback or OllamaFallback()

        # Stats
        self._fallback_count = 0
        self._success_count = 0
        self._failure_count = 0

    async def call(
        self,
        func: Callable[..., T],
        *args,
        fallback_func: Optional[Callable[..., T]] = None,
        **kwargs
    ) -> T:
        """Ejecutar función con protección de circuit breaker.

        Args:
            func: Función principal (llamada a NVIDIA)
            *args: Argumentos para la función
            fallback_func: Función alternativa si falla
            **kwargs: Keyword arguments

        Returns:
            Resultado de la función (NVIDIA o fallback)

        Raises:
            Exception: Si ambas funciones fallan
        """
        try:
            # Intentar con circuit breaker
            result = await self.circuit.call(func, *args, **kwargs)
            self._success_count += 1
            return result

        except CircuitBreakerOpenException:
            logger.warning("Circuit breaker OPEN - using fallback")
            self._fallback_count += 1

            if self.config.fallback_enabled and fallback_func:
                return await fallback_func(*args, **kwargs)
            raise

        except Exception as e:
            logger.error(f"NVIDIA call failed: {e}")
            self._failure_count += 1

            if self.config.fallback_enabled and fallback_func:
                logger.info("Attempting fallback...")
                self._fallback_count += 1
                return await fallback_func(*args, **kwargs)
            raise

    async def generate_with_fallback(
        self,
        nvidia_func: Callable,
        prompt: str,
        model: Any,
        **kwargs
    ) -> NIMResponse:
        """Generar texto con fallback automático a Ollama.

        Args:
            nvidia_func: Función de generación de NVIDIA
            prompt: Prompt para el modelo
            model: Modelo a usar
            **kwargs: Argumentos adicionales

        Returns:
            NIMResponse con el resultado
        """
        async def fallback_generate():
            """Función de fallback a Ollama."""
            ollama_model = map_model_to_ollama(model)
            return self.fallback.generate(
                prompt=prompt,
                model=ollama_model,
                circuit_breaker=self.circuit
            )

        return await self.call(
            nvidia_func,
            prompt,
            model,
            fallback_func=fallback_generate,
            **kwargs
        )

    def get_stats(self) -> dict:
        """Obtener estadísticas del wrapper.

        Returns:
            Diccionario con estadísticas
        """
        return {
            "success_count": self._success_count,
            "failure_count": self._failure_count,
            "fallback_count": self._fallback_count,
            "circuit_state": self.circuit.get_state().value,
            "circuit_metrics": self.circuit.get_metrics().to_dict()
        }


def with_circuit_breaker(
    circuit_name: str = "nvidia_nim",
    config: Optional[NIMCIRCUITConfig] = None,
    fallback_enabled: bool = True
):
    """Decorador para proteger funciones con circuit breaker.

    Args:
        circuit_name: Nombre del circuit breaker
        config: Configuración opcional
        fallback_enabled: Si se habilita fallback

    Returns:
        Decorador configurado

    Example:
        >>> @with_circuit_breaker()
        ... async def generate_text(prompt: str):
        ...     return await nvidia_client.generate(prompt)
    """
    cfg = config or NIMCIRCUITConfig()
    cfg.fallback_enabled = fallback_enabled

    circuit = create_nvidia_circuit(circuit_name, cfg)
    wrapper = CircuitBreakerWrapper(circuit=circuit, config=cfg)

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            return await wrapper.call(func, *args, **kwargs)

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            return asyncio.run(wrapper.call(func, *args, **kwargs))

        # Detectar si la función es async
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper

    return decorator


class NIMCircuitBreakerManager:
    """Manager para múltiples circuit breakers de NVIDIA NIM.

    Permite gestionar circuitos separados para diferentes
    modelos o endpoints.
    """

    def __init__(self):
        self._circuits: dict[str, CircuitBreaker] = {}
        self._wrappers: dict[str, CircuitBreakerWrapper] = {}

    def get_or_create(
        self,
        name: str,
        config: Optional[NIMCIRCUITConfig] = None
    ) -> CircuitBreakerWrapper:
        """Obtener o crear un circuit breaker.

        Args:
            name: Nombre del circuito
            config: Configuración opcional

        Returns:
            CircuitBreakerWrapper configurado
        """
        if name not in self._wrappers:
            cfg = config or NIMCIRCUITConfig()
            circuit = create_nvidia_circuit(name, cfg)
            self._wrappers[name] = CircuitBreakerWrapper(
                circuit=circuit,
                config=cfg
            )
            self._circuits[name] = circuit

        return self._wrappers[name]

    def get_circuit(self, name: str) -> Optional[CircuitBreaker]:
        """Obtener circuit breaker por nombre.

        Args:
            name: Nombre del circuito

        Returns:
            CircuitBreaker o None
        """
        return self._circuits.get(name)

    def get_all_status(self) -> dict:
        """Obtener estado de todos los circuitos.

        Returns:
            Diccionario con estados
        """
        status = {}
        for name, circuit in self._circuits.items():
            status[name] = {
                "state": circuit.get_state().value,
                "metrics": circuit.get_metrics().to_dict()
            }
        return status

    def reset_all(self):
        """Resetear todos los circuit breakers."""
        for circuit in self._circuits.values():
            circuit.reset()
        logger.info("All circuit breakers reset")


# Singleton global
_circuit_manager: Optional[NIMCircuitBreakerManager] = None


def get_circuit_manager() -> NIMCircuitBreakerManager:
    """Obtener el manager global de circuit breakers.

    Returns:
        NIMCircuitBreakerManager singleton
    """
    global _circuit_manager
    if _circuit_manager is None:
        _circuit_manager = NIMCircuitBreakerManager()
    return _circuit_manager


# Exports públicos
__all__ = [
    "NIMCIRCUITConfig",
    "CircuitBreakerWrapper",
    "create_nvidia_circuit",
    "with_circuit_breaker",
    "NIMCircuitBreakerManager",
    "get_circuit_manager",
    "CircuitBreaker",
    "CircuitBreakerOpenException",
    "CircuitState",
]
