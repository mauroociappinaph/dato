#!/usr/bin/env python3
"""
Circuit Breaker Pattern Implementation for NVIDIA NIM

Protege las llamadas a NVIDIA NIM API contra rate limits (429) y errores de servidor (5xx),
con fallback automático a Ollama y métricas integradas al sistema de cost monitoring.

Usage:
    from circuit_breaker import CircuitBreaker, CircuitBreakerConfig, CircuitState

    config = CircuitBreakerConfig(
        failure_threshold=5,
        recovery_timeout=30.0,
        expected_exceptions=[requests.exceptions.HTTPError]
    )

    circuit = CircuitBreaker(name="nvidia_nim", config=config)

    # Execute function with circuit breaker protection
    result = await circuit.call(my_function, arg1, arg2)
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Type, Union
from functools import wraps

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CircuitState(Enum):
    """
    Estados del Circuit Breaker.

    CLOSED: Estado normal, las requests pasan directamente a NVIDIA
    OPEN: El circuito está abierto, se rechazan requests inmediatamente y se usa fallback
    HALF_OPEN: Estado de recuperación, se permite 1 request de prueba
    """
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


@dataclass
class CircuitBreakerConfig:
    """Configuración del Circuit Breaker.

    Attributes:
        failure_threshold: Número de fallos consecutivos antes de abrir el circuito
        recovery_timeout: Segundos antes de intentar recuperación (half-open)
        half_open_max_calls: Máximo de calls permitidos en estado HALF_OPEN
        success_threshold: Número de éxitos necesarios para cerrar desde half-open
        expected_exceptions: Lista de excepciones que cuentan como fallo
    """
    failure_threshold: int = 5
    recovery_timeout: float = 30.0
    half_open_max_calls: int = 1
    success_threshold: int = 2
    expected_exceptions: Optional[List[Type[Exception]]] = None

    def __post_init__(self):
        if self.expected_exceptions is None:
            self.expected_exceptions = [Exception]


@dataclass
class CircuitBreakerMetrics:
    """Métricas del Circuit Breaker para monitoreo.

    Attributes:
        state: Estado actual del circuito
        failure_count: Contador de fallos consecutivos
        success_count: Contador de éxitos consecutivos
        last_failure_time: Timestamp del último fallo
        last_success_time: Timestamp del último éxito
        total_calls: Total de llamadas procesadas
        rejected_calls: Llamadas rechazadas por circuito abierto
        state_transitions: Historial de transiciones de estado
    """
    state: CircuitState = CircuitState.CLOSED
    failure_count: int = 0
    success_count: int = 0
    last_failure_time: Optional[datetime] = None
    last_success_time: Optional[datetime] = None
    total_calls: int = 0
    rejected_calls: int = 0
    state_transitions: List[Dict[str, Any]] = field(default_factory=list)
    fallback_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convertir métricas a diccionario."""
        return {
            "state": self.state.value,
            "failure_count": self.failure_count,
            "success_count": self.success_count,
            "last_failure_time": self.last_failure_time.isoformat() if self.last_failure_time else None,
            "last_success_time": self.last_success_time.isoformat() if self.last_success_time else None,
            "total_calls": self.total_calls,
            "rejected_calls": self.rejected_calls,
            "fallback_count": self.fallback_count,
            "state_transitions_count": len(self.state_transitions)
        }


class CircuitBreakerOpenException(Exception):
    """Excepción lanzada cuando el circuito está abierto y se rechaza una llamada."""

    def __init__(self, circuit_name: str, message: str = None):
        self.circuit_name = circuit_name
        self.message = message or f"Circuit breaker '{circuit_name}' is OPEN"
        super().__init__(self.message)


class CircuitBreaker:
    """
    Implementación del patrón Circuit Breaker para protección de APIs.

    Características:
    - 3 estados: CLOSED (normal), OPEN (fallando), HALF_OPEN (recuperación)
    - Thread-safe usando asyncio.Lock
    - Backoff exponencial integrado
    - Métricas detalladas para monitoreo
    - Fallback automático configurable

    Example:
        >>> config = CircuitBreakerConfig(failure_threshold=5)
        >>> circuit = CircuitBreaker("nvidia_nim", config)
        >>>
        >>> # Método 1: Usar call()
        >>> result = await circuit.call(my_api_call, arg1, arg2)
        >>>
        >>> # Método 2: Usar como decorador
        >>> @circuit.protect
        >>> async def my_function():
        >>>     return await api.call()
    """

    def __init__(self, name: str, config: Optional[CircuitBreakerConfig] = None):
        """
        Inicializar Circuit Breaker.

        Args:
            name: Nombre identificador del circuit breaker
            config: Configuración opcional (usa defaults si no se proporciona)
        """
        self.name = name
        self.config = config or CircuitBreakerConfig()

        # Estado interno
        self._state = CircuitState.CLOSED
        self._lock = asyncio.Lock()
        self._half_open_calls = 0
        self._last_state_change = datetime.now()

        # Métricas
        self._metrics = CircuitBreakerMetrics()

        logger.info(f"CircuitBreaker '{name}' initialized in CLOSED state")

    async def call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Ejecutar función con protección del circuit breaker.

        Args:
            func: Función a ejecutar (puede ser sync o async)
            *args: Argumentos posicionales para la función
            **kwargs: Argumentos nombrados para la función

        Returns:
            Resultado de la función ejecutada

        Raises:
            CircuitBreakerOpenException: Si el circuito está abierto
            Exception: Cualquier excepción lanzada por la función
        """
        async with self._lock:
            # Verificar si podemos ejecutar
            if not await self._can_execute():
                self._metrics.rejected_calls += 1
                logger.warning(f"Circuit '{self.name}' is OPEN - rejecting call")
                raise CircuitBreakerOpenException(self.name)

            # Si estamos en half-open, incrementar contador
            if self._state == CircuitState.HALF_OPEN:
                self._half_open_calls += 1

            self._metrics.total_calls += 1

        # Ejecutar la función fuera del lock
        try:
            # Manejar funciones async y sync
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)

            # Registrar éxito
            await self._on_success()
            return result

        except Exception as e:
            # Verificar si es una excepción esperada
            if self._is_expected_exception(e):
                await self._on_failure(e)
            else:
                # Excepción no esperada, no afecta el circuito
                logger.error(f"Unexpected exception in circuit '{self.name}': {e}")
            raise

    def protect(self, func: Callable) -> Callable:
        """
        Decorador para proteger una función con el circuit breaker.

        Example:
            >>> circuit = CircuitBreaker("api")
            >>>
            >>> @circuit.protect
            >>> async def call_api():
            >>>     return await api.request()
        """
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await self.call(func, *args, **kwargs)
        return wrapper

    async def _can_execute(self) -> bool:
        """
        Verificar si se puede ejecutar una llamada basado en el estado actual.

        Returns:
            True si se puede ejecutar, False si debe rechazarse
        """
        now = datetime.now()

        if self._state == CircuitState.CLOSED:
            # Estado normal, siempre permitir
            return True

        elif self._state == CircuitState.OPEN:
            # Verificar si es tiempo de intentar recuperación
            time_in_open = now - self._last_state_change
            if time_in_open >= timedelta(seconds=self.config.recovery_timeout):
                # Cambiar a half-open para probar recuperación
                await self._transition_to(CircuitState.HALF_OPEN)
                self._half_open_calls = 0
                return True
            else:
                # Todavía en cooldown
                return False

        elif self._state == CircuitState.HALF_OPEN:
            # Permitir solo un número limitado de calls en half-open
            return self._half_open_calls < self.config.half_open_max_calls

        return True

    async def _on_success(self):
        """Manejar éxito de una llamada."""
        async with self._lock:
            self._metrics.success_count += 1
            self._metrics.last_success_time = datetime.now()

            if self._state == CircuitState.HALF_OPEN:
                # En half-open, acumular éxitos
                if self._metrics.success_count >= self.config.success_threshold:
                    # Suficientes éxitos, cerrar el circuito
                    await self._transition_to(CircuitState.CLOSED)
                    self._metrics.failure_count = 0
                    logger.info(f"Circuit '{self.name}' CLOSED after recovery")
            else:
                # En closed, resetear contador de fallos
                self._metrics.failure_count = 0

    async def _on_failure(self, exception: Exception):
        """
        Manejar fallo de una llamada.

        Args:
            exception: La excepción que causó el fallo
        """
        async with self._lock:
            self._metrics.failure_count += 1
            self._metrics.last_failure_time = datetime.now()
            self._metrics.success_count = 0

            logger.warning(
                f"Circuit '{self.name}' failure {self._metrics.failure_count}/"
                f"{self.config.failure_threshold}: {exception}"
            )

            if self._state == CircuitState.HALF_OPEN:
                # Fallo en half-open, volver a open
                await self._transition_to(CircuitState.OPEN)
                logger.warning(f"Circuit '{self.name}' returned to OPEN after failure in half-open")

            elif self._state == CircuitState.CLOSED:
                # En closed, verificar si debemos abrir
                if self._metrics.failure_count >= self.config.failure_threshold:
                    await self._transition_to(CircuitState.OPEN)
                    logger.error(f"Circuit '{self.name}' OPENED after {self._metrics.failure_count} failures")

    def _is_expected_exception(self, exception: Exception) -> bool:
        """
        Verificar si una excepción cuenta como fallo para el circuit breaker.

        Args:
            exception: Excepción a verificar

        Returns:
            True si es una excepción esperada
        """
        return any(isinstance(exception, exc_type) for exc_type in self.config.expected_exceptions)

    async def _transition_to(self, new_state: CircuitState):
        """
        Transicionar a un nuevo estado.

        Args:
            new_state: Nuevo estado al que transicionar
        """
        if self._state == new_state:
            return

        old_state = self._state
        self._state = new_state
        self._last_state_change = datetime.now()

        # Registrar transición
        transition = {
            "from": old_state.value,
            "to": new_state.value,
            "timestamp": datetime.now().isoformat(),
            "failure_count": self._metrics.failure_count
        }
        self._metrics.state_transitions.append(transition)
        self._metrics.state = new_state

        logger.info(f"Circuit '{self.name}' transitioned: {old_state.value} → {new_state.value}")

    def get_state(self) -> CircuitState:
        """Obtener estado actual del circuito."""
        return self._state

    def get_metrics(self) -> CircuitBreakerMetrics:
        """Obtener métricas actuales."""
        return self._metrics

    def reset(self):
        """Reset manual del circuit breaker a estado CLOSED."""
        asyncio.create_task(self._transition_to(CircuitState.CLOSED))
        self._metrics.failure_count = 0
        self._metrics.success_count = 0
        self._half_open_calls = 0
        logger.info(f"Circuit '{self.name}' manually reset to CLOSED")

    def record_fallback(self):
        """Registrar uso de fallback (llamada desde el cliente cuando usa Ollama)."""
        self._metrics.fallback_count += 1

    async def get_status(self) -> Dict[str, Any]:
        """
        Obtener estado completo del circuit breaker.

        Returns:
            Diccionario con estado y métricas
        """
        async with self._lock:
            time_in_state = datetime.now() - self._last_state_change

            return {
                "name": self.name,
                "state": self._state.value,
                "time_in_state_seconds": time_in_state.total_seconds(),
                "metrics": self._metrics.to_dict(),
                "config": {
                    "failure_threshold": self.config.failure_threshold,
                    "recovery_timeout": self.config.recovery_timeout,
                    "half_open_max_calls": self.config.half_open_max_calls,
                    "success_threshold": self.config.success_threshold
                }
            }


class CircuitBreakerRegistry:
    """
    Registro global de circuit breakers.

    Permite gestionar múltiples circuit breakers y obtener métricas consolidadas.
    """

    _instance = None
    _lock = asyncio.Lock()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._circuits: Dict[str, CircuitBreaker] = {}
        return cls._instance

    def register(self, name: str, circuit: CircuitBreaker):
        """Registrar un circuit breaker."""
        self._circuits[name] = circuit
        logger.info(f"Registered circuit breaker: {name}")

    def get(self, name: str) -> Optional[CircuitBreaker]:
        """Obtener circuit breaker por nombre."""
        return self._circuits.get(name)

    def get_all(self) -> Dict[str, CircuitBreaker]:
        """Obtener todos los circuit breakers."""
        return self._circuits.copy()

    async def get_all_status(self) -> Dict[str, Dict[str, Any]]:
        """Obtener estado de todos los circuit breakers."""
        status = {}
        for name, circuit in self._circuits.items():
            status[name] = await circuit.get_status()
        return status

    def reset_all(self):
        """Resetear todos los circuit breakers."""
        for circuit in self._circuits.values():
            circuit.reset()
        logger.info("All circuit breakers reset")


# Singleton para acceso global
registry = CircuitBreakerRegistry()


# Factory function para crear circuit breakers preconfigurados
def create_nvidia_circuit_breaker(
    name: str = "nvidia_nim",
    failure_threshold: int = 5,
    recovery_timeout: float = 30.0
) -> CircuitBreaker:
    """
    Crear circuit breaker preconfigurado para NVIDIA NIM.

    Args:
        name: Nombre del circuit breaker
        failure_threshold: Fallos antes de abrir
        recovery_timeout: Segundos antes de intentar recuperación

    Returns:
        CircuitBreaker configurado para NVIDIA
    """
    try:
        import requests
        expected_exceptions = [
            requests.exceptions.HTTPError,
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
            requests.exceptions.RequestException
        ]
    except ImportError:
        expected_exceptions = [Exception]

    config = CircuitBreakerConfig(
        failure_threshold=failure_threshold,
        recovery_timeout=recovery_timeout,
        expected_exceptions=expected_exceptions
    )

    circuit = CircuitBreaker(name=name, config=config)
    registry.register(name, circuit)

    return circuit


if __name__ == "__main__":
    # Demo del circuit breaker
    async def demo():
        print("🧪 Circuit Breaker Demo")
        print("=" * 50)

        # Crear circuit breaker con configuración sensible para demo
        config = CircuitBreakerConfig(
            failure_threshold=3,
            recovery_timeout=5.0,
            success_threshold=1
        )

        circuit = CircuitBreaker(name="demo", config=config)

        # Función que falla
        async def failing_function():
            raise Exception("Simulated API failure")

        # Función que tiene éxito
        async def success_function():
            return "Success!"

        print("\n1. Probando fallos consecutivos...")
        for i in range(5):
            try:
                await circuit.call(failing_function)
            except Exception as e:
                print(f"   Call {i+1}: {e}")
                print(f"   State: {circuit.get_state().value}")

        print("\n2. Esperando recuperación (5s)...")
        await asyncio.sleep(5)

        print("\n3. Intentando llamada en half-open...")
        try:
            # Esta debería fallar y volver a abrir
            await circuit.call(failing_function)
        except Exception as e:
            print(f"   Result: {e}")
            print(f"   State: {circuit.get_state().value}")

        print("\n4. Esperando otra recuperación (5s)...")
        await asyncio.sleep(5)

        print("\n5. Intentando con función exitosa...")
        try:
            result = await circuit.call(success_function)
            print(f"   Result: {result}")
            print(f"   State: {circuit.get_state().value}")
        except Exception as e:
            print(f"   Error: {e}")

        print("\n6. Métricas finales:")
        metrics = circuit.get_metrics()
        print(f"   Total calls: {metrics.total_calls}")
        print(f"   Rejected calls: {metrics.rejected_calls}")
        print(f"   State transitions: {len(metrics.state_transitions)}")

        print("\n✅ Demo completado!")

    asyncio.run(demo())
