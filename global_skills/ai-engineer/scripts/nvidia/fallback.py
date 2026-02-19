#!/usr/bin/env python3
"""
NVIDIA NIM Fallback - Lógica de fallback a Ollama.
"""

import time
import requests
from typing import Optional, List

from .models import NIMResponse, ModelType


class OllamaFallback:
    """Fallback handler for Ollama local inference."""

    def __init__(self, base_url: str = "http://127.0.0.1:11434"):
        self.base_url = base_url
        self.generate_url = f"{base_url}/api/generate"
        self.embed_url = f"{base_url}/api/embeddings"

    def is_available(self) -> bool:
        """Check if Ollama is available."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            return response.status_code == 200
        except Exception:
            return False

    def generate(
        self,
        prompt: str,
        model: str = "llama3.1",
        circuit_breaker=None
    ) -> NIMResponse:
        """Generate text using Ollama."""
        start_time = time.time()

        response = requests.post(
            self.generate_url,
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=120
        )

        response.raise_for_status()
        data = response.json()

        latency = (time.time() - start_time) * 1000

        # Record fallback in circuit breaker
        if circuit_breaker:
            circuit_breaker.record_fallback()

        # Estimate tokens (rough approximation)
        estimated_tokens = len(prompt.split()) + len(data["response"].split())

        return NIMResponse(
            text=data["response"],
            model=f"ollama/{model}",
            tokens_used=estimated_tokens,
            finish_reason="stop",
            latency_ms=latency,
            source="ollama",
            circuit_state=circuit_breaker.get_state().value if circuit_breaker else "disabled"
        )

    def generate_embedding(
        self,
        text: str,
        model: str = "nomic-embed-text"
    ) -> List[float]:
        """Generate embeddings using Ollama."""
        response = requests.post(
            self.embed_url,
            json={"model": model, "prompt": text},
            timeout=30
        )
        response.raise_for_status()
        return response.json()["embedding"]


def map_model_to_ollama(model: ModelType) -> str:
    """Map NVIDIA model to Ollama equivalent."""
    mapping = {
        ModelType.LLAMA_8B: "llama3.1",
        ModelType.LLAMA_70B: "llama3.1:70b",
        ModelType.LLAMA_3B: "llama3.2",
        ModelType.LLAMA_1B: "llama3.2:1b",
        ModelType.CODELLAMA_70B: "codellama:70b",
        ModelType.MISTRAL_7B: "mistral",
        ModelType.NV_EMBED: "nomic-embed-text",
    }
    return mapping.get(model, "llama3.1")
