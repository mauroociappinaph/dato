#!/usr/bin/env python3
"""
NVIDIA NIM Models - Definiciones de modelos y tipos de datos.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional, List


class ModelType(Enum):
    """Available NVIDIA NIM models ordered by capability."""
    # Ultra-Capacity (Complex reasoning, critical tasks)
    LLAMA_405B = "meta/llama-3.1-405b-instruct"
    NEMOTRON_340B = "nvidia/nemotron-4-340b-instruct"

    # High-Capacity (Deep analysis, architecture)
    LLAMA_70B = "meta/llama-3.1-70b-instruct"
    LLAMA_3_3_70B = "meta/llama-3.3-70b-instruct"
    MIXTRAL_8X22B = "mistralai/mixtral-8x22b-instruct-v0.1"

    # Medium-Capacity (Balance quality/speed)
    LLAMA_8B = "meta/llama-3.1-8b-instruct"  # Default
    MISTRAL_7B = "mistralai/mistral-7b-instruct-v0.3"
    GEMMA_27B = "google/gemma-2-27b-it"

    # Code-Specialized
    CODELLAMA_70B = "meta/codellama-70b"
    DEEPSEEK_CODER = "deepseek-ai/deepseek-coder-6.7b-instruct"

    # Fast/Low-Latency (Simple tasks, operations)
    LLAMA_3B = "meta/llama-3.2-3b-instruct"
    LLAMA_1B = "meta/llama-3.2-1b-instruct"
    PHI_3_MINI = "microsoft/phi-3-mini-4k-instruct"

    # Embeddings
    NV_EMBED = "nvidia/nv-embed-v1"
    NV_EMBED_QA = "nvidia/nv-embedqa-mistral-7b-v2"


@dataclass
class NIMResponse:
    """Structured response from NVIDIA NIM."""
    text: str
    model: str
    tokens_used: int
    finish_reason: str
    latency_ms: float
    source: str = "nvidia"  # "nvidia" or "ollama"
    circuit_state: str = "closed"  # Circuit breaker state


@dataclass
class UsageStats:
    """Usage statistics for cost monitoring."""
    total_requests: int
    total_tokens: int
    fallback_count: int
    nvidia_available: bool
    circuit_breaker_enabled: bool
    circuit_state: Optional[str] = None
    circuit_failure_count: int = 0
    circuit_rejected_count: int = 0
    circuit_fallback_count: int = 0
    circuit_total_calls: int = 0


@dataclass
class ModelConfig:
    """Configuration for a specific model."""
    model: ModelType
    max_tokens: int
    temperature: float
    top_p: float
    timeout: int


# Default configurations
DEFAULT_CONFIG = ModelConfig(
    model=ModelType.LLAMA_8B,
    max_tokens=1024,
    temperature=0.7,
    top_p=0.9,
    timeout=60
)

# Cost per 1K tokens for each model tier
MODEL_PRICING = {
    "ultra": 0.004,    # NEMOTRON_340B, LLAMA_405B
    "high": 0.001,     # LLAMA_70B, CODELLAMA_70B
    "medium": 0.0002,  # LLAMA_8B, MISTRAL_7B
    "low": 0.0001,     # LLAMA_3B, LLAMA_1B
}


def get_model_tier(model: ModelType) -> str:
    """Get the cost tier for a model."""
    tier_map = {
        ModelType.NEMOTRON_340B: "ultra",
        ModelType.LLAMA_405B: "ultra",
        ModelType.LLAMA_70B: "high",
        ModelType.LLAMA_3_3_70B: "high",
        ModelType.CODELLAMA_70B: "high",
        ModelType.MIXTRAL_8X22B: "high",
        ModelType.LLAMA_8B: "medium",
        ModelType.MISTRAL_7B: "medium",
        ModelType.GEMMA_27B: "medium",
        ModelType.DEEPSEEK_CODER: "medium",
        ModelType.LLAMA_3B: "low",
        ModelType.LLAMA_1B: "low",
        ModelType.PHI_3_MINI: "low",
    }
    return tier_map.get(model, "medium")


def calculate_cost(model: ModelType, tokens: int) -> float:
    """Calculate cost for a model and token count."""
    tier = get_model_tier(model)
    cost_per_1k = MODEL_PRICING.get(tier, 0.0002)
    return (tokens / 1000) * cost_per_1k
