#!/usr/bin/env python3
"""
NVIDIA NIM Configuration
Central configuration for NVIDIA API integration.
"""

import os
from pathlib import Path

# Load .env file if it exists (for development)
def _load_env_file():
    """Load environment variables from .env file"""
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ.setdefault(key, value)

_load_env_file()

# NVIDIA API Configuration
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
if not NVIDIA_API_KEY:
    raise ValueError(
        "NVIDIA_API_KEY environment variable is not set. "
        "Please set it before running: export NVIDIA_API_KEY='your-api-key' "
        "Or create a .env file in the scripts directory"
    )

NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"

# Model Pricing (per 1K tokens) - For cost estimation
MODEL_PRICING = {
    "meta/llama-3.1-8b-instruct": {"input": 0.0001, "output": 0.0002},
    "meta/llama-3.1-70b-instruct": {"input": 0.0006, "output": 0.0012},
    "nvidia/nemotron-4-340b-instruct": {"input": 0.0020, "output": 0.0040},
    "mistralai/mistral-7b-instruct-v0.3": {"input": 0.0001, "output": 0.0002},
    "mistralai/mixtral-8x7b-instruct-v0.1": {"input": 0.0003, "output": 0.0006},
}

# Default settings
DEFAULT_MODEL = "meta/llama-3.1-8b-instruct"
DEFAULT_MAX_TOKENS = 1024
DEFAULT_TEMPERATURE = 0.7


def calculate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """Calculate cost for a request"""
    pricing = MODEL_PRICING.get(model, MODEL_PRICING[DEFAULT_MODEL])
    input_cost = (input_tokens / 1000) * pricing["input"]
    output_cost = (output_tokens / 1000) * pricing["output"]
    return input_cost + output_cost
