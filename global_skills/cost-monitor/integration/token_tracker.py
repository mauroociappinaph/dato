#!/usr/bin/env python3
"""
NIM Token Tracker - Captura de tokens de NVIDIA NIM

Este módulo proporciona un wrapper para el cliente NVIDIA NIM que captura
tokens usados en cada llamada para tracking de costos.
"""

from typing import Optional, Tuple, Dict, Any
from dataclasses import dataclass
import time


@dataclass
class TokenUsage:
    """Registro de uso de tokens para una ejecución"""
    tokens_input: int
    tokens_output: int
    tokens_total: int
    model_used: str
    latency_ms: float
    timestamp: float


class NIMTokenTracker:
    """
    Wrapper para NVIDIANIMClient que captura tokens usados.

    Intercepta llamadas al cliente NIM y extrae información de tokens
    para su uso en tracking de costos.

    Usage:
        from ai_engineer.scripts.nvidia_nim_client import NVIDIANIMClient
        from token_tracker import NIMTokenTracker

        nim_client = NVIDIANIMClient()
        tracker = NIMTokenTracker(nim_client)

        response = tracker.generate("prompt", model="meta/llama-3.1-8b")
        usage = tracker.get_last_usage()
        print(f"Tokens: {usage.tokens_total}")
    """

    def __init__(self, nim_client=None):
        """
        Inicializa el tracker.

        Args:
            nim_client: Instancia de NVIDIANIMClient (opcional)
        """
        self.nim_client = nim_client
        self._last_usage: Optional[TokenUsage] = None
        self._history: list = []
        self._max_history = 1000

    def set_client(self, nim_client):
        """Establece el cliente NIM después de la inicialización"""
        self.nim_client = nim_client

    def _estimate_input_tokens(self, text: str) -> int:
        """
        Estima tokens de entrada (aproximación simple).

        En producción, se debería usar el tokenizer real del modelo.
        Esta es una estimación conservadora: ~4 caracteres por token.

        Args:
            text: Texto de entrada

        Returns:
            Número estimado de tokens
        """
        if not text:
            return 0
        # Estimación conservadora: promedio de 4 caracteres por token
        return max(1, len(text) // 4)

    def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        max_tokens: int = 1024,
        **kwargs
    ) -> Any:
        """
        Genera texto y captura tokens usados.

        Args:
            prompt: Prompt de entrada
            model: Modelo a usar
            max_tokens: Máximo de tokens a generar
            **kwargs: Argumentos adicionales para el cliente NIM

        Returns:
            Respuesta del modelo (NIMResponse o similar)
        """
        if self.nim_client is None:
            raise RuntimeError("NIM client not set. Call set_client() first.")

        start_time = time.time()

        # Estimar tokens de entrada
        tokens_input = self._estimate_input_tokens(prompt)

        # Llamar al cliente NIM
        # Manejar tanto llamadas síncronas como asíncronas
        import asyncio
        import inspect

        if inspect.iscoroutinefunction(self.nim_client.generate):
            # Cliente asíncrono - no podemos await aquí, delegamos
            raise NotImplementedError(
                "Async NIM client not supported in sync generate(). "
                "Use generate_async() instead."
            )
        else:
            response = self.nim_client.generate(
                prompt=prompt,
                model=model,
                max_tokens=max_tokens,
                **kwargs
            )

        latency_ms = (time.time() - start_time) * 1000

        # Extraer tokens de salida de la respuesta
        tokens_output = getattr(response, 'tokens_used', 0)

        # Si no hay tokens en la respuesta, estimar basado en longitud
        if tokens_output == 0:
            output_text = getattr(response, 'text', '')
            tokens_output = self._estimate_input_tokens(output_text)

        # Guardar uso
        self._last_usage = TokenUsage(
            tokens_input=tokens_input,
            tokens_output=tokens_output,
            tokens_total=tokens_input + tokens_output,
            model_used=model or getattr(response, 'model', 'unknown'),
            latency_ms=latency_ms,
            timestamp=time.time()
        )

        # Guardar en historial
        self._history.append(self._last_usage)
        if len(self._history) > self._max_history:
            self._history.pop(0)

        return response

    async def generate_async(
        self,
        prompt: str,
        model: Optional[str] = None,
        max_tokens: int = 1024,
        **kwargs
    ) -> Any:
        """
        Versión asíncrona de generate().

        Args:
            prompt: Prompt de entrada
            model: Modelo a usar
            max_tokens: Máximo de tokens a generar
            **kwargs: Argumentos adicionales

        Returns:
            Respuesta del modelo
        """
        if self.nim_client is None:
            raise RuntimeError("NIM client not set. Call set_client() first.")

        start_time = time.time()

        # Estimar tokens de entrada
        tokens_input = self._estimate_input_tokens(prompt)

        # Llamar al cliente NIM (asíncrono)
        response = await self.nim_client.generate(
            prompt=prompt,
            model=model,
            max_tokens=max_tokens,
            **kwargs
        )

        latency_ms = (time.time() - start_time) * 1000

        # Extraer tokens de salida
        tokens_output = getattr(response, 'tokens_used', 0)

        # Si no hay tokens, estimar
        if tokens_output == 0:
            output_text = getattr(response, 'text', '')
            tokens_output = self._estimate_input_tokens(output_text)

        # Guardar uso
        self._last_usage = TokenUsage(
            tokens_input=tokens_input,
            tokens_output=tokens_output,
            tokens_total=tokens_input + tokens_output,
            model_used=model or getattr(response, 'model', 'unknown'),
            latency_ms=latency_ms,
            timestamp=time.time()
        )

        # Guardar en historial
        self._history.append(self._last_usage)
        if len(self._history) > self._max_history:
            self._history.pop(0)

        return response

    def get_last_usage(self) -> Optional[TokenUsage]:
        """
        Obtiene el último registro de uso de tokens.

        Returns:
            TokenUsage o None si no hay registros
        """
        return self._last_usage

    def get_usage_summary(self) -> Dict[str, Any]:
        """
        Obtiene un resumen del uso de tokens.

        Returns:
            Diccionario con estadísticas de uso
        """
        if not self._history:
            return {
                "total_calls": 0,
                "total_tokens": 0,
                "avg_tokens_per_call": 0,
                "avg_latency_ms": 0
            }

        total_tokens = sum(u.tokens_total for u in self._history)
        total_latency = sum(u.latency_ms for u in self._history)

        return {
            "total_calls": len(self._history),
            "total_tokens": total_tokens,
            "avg_tokens_per_call": total_tokens / len(self._history),
            "avg_latency_ms": total_latency / len(self._history),
            "last_model_used": self._history[-1].model_used if self._history else None
        }

    def reset_history(self):
        """Limpia el historial de uso"""
        self._history = []
        self._last_usage = None

    def get_history(self) -> list:
        """
        Obtiene todo el historial de uso.

        Returns:
            Lista de TokenUsage
        """
        return self._history.copy()


# Instancia global para uso conveniente
_default_tracker: Optional[NIMTokenTracker] = None


def get_token_tracker(nim_client=None) -> NIMTokenTracker:
    """
    Obtiene o crea el token tracker global.

    Args:
        nim_client: Cliente NIM (opcional)

    Returns:
        Instancia de NIMTokenTracker
    """
    global _default_tracker
    if _default_tracker is None:
        _default_tracker = NIMTokenTracker(nim_client)
    elif nim_client is not None:
        _default_tracker.set_client(nim_client)
    return _default_tracker
