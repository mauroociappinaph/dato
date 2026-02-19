#!/usr/bin/env python3
"""
NVIDIA NIM Client - Cliente principal modular.

Utiliza los módulos separados:
- models: Definiciones de modelos y tipos
- fallback: Lógica de fallback a Ollama
- circuit_breaker_integration: Protección de circuit breaker

Usage:
    from client import NVIDIANIMClient, get_nim_client

    client = get_nim_client()
    response = client.generate("Explain quantum computing")
    print(response.text)
"""

import os
import time
import asyncio
import requests
from typing import Optional, Dict, Any, List

from .models import ModelType, NIMResponse, UsageStats, calculate_cost
from .fallback import OllamaFallback, map_model_to_ollama
from .circuit_breaker_integration import (
    CircuitBreakerWrapper, NIMCIRCUITConfig, CircuitBreakerOpenException,
    CircuitState, get_circuit_manager
)

try:
    from ..nvidia_config import NVIDIA_API_KEY, NVIDIA_BASE_URL
except ImportError:
    from nvidia_config import NVIDIA_API_KEY, NVIDIA_BASE_URL


class NVIDIANIMClient:
    """Cliente NVIDIA NIM con Circuit Breaker y fallback a Ollama."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        circuit_breaker_enabled: bool = True,
        circuit_config: Optional[Dict[str, Any]] = None
    ):
        self.api_key = api_key or NVIDIA_API_KEY or os.getenv("NVIDIA_API_KEY")
        self.base_url = NVIDIA_BASE_URL
        self.preferred_model = ModelType.LLAMA_8B

        # Tracking
        self.total_tokens = 0
        self.total_requests = 0
        self.fallback_count = 0

        # Circuit Breaker
        self.circuit_enabled = circuit_breaker_enabled
        self._wrapper: Optional[CircuitBreakerWrapper] = None

        if circuit_breaker_enabled:
            cfg = NIMCIRCUITConfig(
                failure_threshold=circuit_config.get("failure_threshold", 5) if circuit_config else 5,
                recovery_timeout=circuit_config.get("recovery_timeout", 30.0) if circuit_config else 30.0,
                fallback_enabled=True
            )
            self._wrapper = CircuitBreakerWrapper(config=cfg)

    def is_available(self) -> bool:
        """Check if NVIDIA NIM is available."""
        if not self.api_key:
            return False
        try:
            response = requests.get(
                f"{self.base_url}/models",
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=5
            )
            return response.status_code == 200
        except Exception:
            return False

    async def _call_nvidia(self, prompt: str, model: ModelType, max_tokens: int = 1024) -> NIMResponse:
        """Call NVIDIA NIM API."""
        start_time = time.time()

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": model.value,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": 0.7,
            "top_p": 0.9
        }

        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )
        )

        response.raise_for_status()
        data = response.json()

        latency = (time.time() - start_time) * 1000
        tokens = data.get("usage", {}).get("total_tokens", 0)
        self.total_tokens += tokens
        self.total_requests += 1

        circuit_state = "disabled"
        if self._wrapper:
            circuit_state = self._wrapper.circuit.get_state().value

        return NIMResponse(
            text=data["choices"][0]["message"]["content"],
            model=model.value,
            tokens_used=tokens,
            finish_reason=data["choices"][0].get("finish_reason", "unknown"),
            latency_ms=latency,
            source="nvidia",
            circuit_state=circuit_state
        )

    async def generate_async(
        self,
        prompt: str,
        model: Optional[ModelType] = None,
        max_tokens: int = 1024,
        fallback: bool = True
    ) -> NIMResponse:
        """Generate text with Circuit Breaker protection (async)."""
        model = model or self.preferred_model

        if not self.circuit_enabled or not self._wrapper:
            return await self._generate_legacy(prompt, model, max_tokens, fallback)

        circuit_state = self._wrapper.circuit.get_state()

        if circuit_state == CircuitState.OPEN:
            if fallback:
                print("🔴 Circuit OPEN - Using Ollama fallback")
                return self._wrapper.fallback.generate(
                    prompt, map_model_to_ollama(model), self._wrapper.circuit
                )
            raise CircuitBreakerOpenException("nvidia_nim", "Circuit OPEN and fallback disabled")

        try:
            return await self._wrapper.circuit.call(
                self._call_nvidia, prompt, model, max_tokens
            )
        except CircuitBreakerOpenException:
            if fallback:
                print("🔴 Circuit OPEN during call - Using Ollama fallback")
                return self._wrapper.fallback.generate(
                    prompt, map_model_to_ollama(model), self._wrapper.circuit
                )
            raise
        except Exception as e:
            if fallback:
                print(f"⚠️ NVIDIA NIM failed: {e}. Falling back to Ollama...")
                return self._wrapper.fallback.generate(
                    prompt, map_model_to_ollama(model), self._wrapper.circuit
                )
            raise

    def generate(
        self,
        prompt: str,
        model: Optional[ModelType] = None,
        max_tokens: int = 1024,
        fallback: bool = True
    ) -> NIMResponse:
        """Generate text (sync version)."""
        return asyncio.run(self.generate_async(prompt, model, max_tokens, fallback))

    async def _generate_legacy(
        self, prompt: str, model: ModelType, max_tokens: int, fallback: bool
    ) -> NIMResponse:
        """Legacy generate without Circuit Breaker."""
        if self.is_available():
            try:
                return await self._call_nvidia(prompt, model, max_tokens)
            except Exception as e:
                if not fallback:
                    raise
                print(f"⚠️ NVIDIA NIM failed: {e}. Falling back to Ollama...")

        if fallback:
            fallback_handler = OllamaFallback()
            return fallback_handler.generate(prompt, map_model_to_ollama(model))

        raise RuntimeError("NVIDIA NIM not available and fallback disabled")

    def generate_embedding(self, text: str) -> List[float]:
        """Generate embeddings with fallback to Ollama."""
        if self.is_available():
            if self._wrapper and self._wrapper.circuit.get_state() == CircuitState.OPEN:
                print("🔴 Circuit OPEN - Skipping NVIDIA for embeddings")
            else:
                try:
                    headers = {
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    }
                    response = requests.post(
                        f"{self.base_url}/embeddings",
                        headers=headers,
                        json={"input": text, "model": "nvidia/nv-embed-v1"},
                        timeout=30
                    )
                    if response.status_code == 200:
                        return response.json()["data"][0]["embedding"]
                except Exception:
                    pass

        try:
            fallback = OllamaFallback()
            return fallback.generate_embedding(text)
        except Exception as e:
            raise RuntimeError(f"Embedding generation failed: {e}")

    def get_usage_stats(self) -> Dict[str, Any]:
        """Get usage statistics."""
        stats = {
            "total_requests": self.total_requests,
            "total_tokens": self.total_tokens,
            "fallback_count": self.fallback_count,
            "nvidia_available": self.is_available(),
            "circuit_breaker_enabled": self.circuit_enabled
        }

        if self._wrapper:
            metrics = self._wrapper.circuit.get_metrics()
            stats.update({
                "circuit_state": metrics.state.value,
                "circuit_failure_count": metrics.failure_count,
                "circuit_rejected_count": metrics.rejected_calls,
                "circuit_fallback_count": metrics.fallback_count,
                "circuit_total_calls": metrics.total_calls
            })

        return stats

    def get_circuit_breaker_status(self) -> Optional[Dict[str, Any]]:
        """Get Circuit Breaker status."""
        if not self._wrapper:
            return None
        return asyncio.run(self._wrapper.circuit.get_status())

    def reset_circuit_breaker(self):
        """Reset Circuit Breaker to CLOSED."""
        if self._wrapper:
            self._wrapper.circuit.reset()
            print("🔄 Circuit Breaker reset to CLOSED")


# Singleton
_nim_client: Optional[NVIDIANIMClient] = None


def get_nim_client(circuit_breaker_enabled: bool = True) -> NVIDIANIMClient:
    """Get or create singleton NIM client."""
    global _nim_client
    if _nim_client is None:
        _nim_client = NVIDIANIMClient(circuit_breaker_enabled=circuit_breaker_enabled)
    return _nim_client


# Convenience functions
async def generate_async(prompt: str, **kwargs) -> str:
    """Quick async generate function."""
    client = get_nim_client()
    return (await client.generate_async(prompt, **kwargs)).text


def generate(prompt: str, **kwargs) -> str:
    """Quick generate function (sync)."""
    client = get_nim_client()
    return client.generate(prompt, **kwargs).text
