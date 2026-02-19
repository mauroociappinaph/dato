"""
Resilience and utility module for THE DUDE skills.
Provides standardized logging, retries, and safe LLM calls.
"""

import logging
import time
import functools
import sys
import os
from typing import Any, Callable

import requests

def setup_logging(name: str, verbose: bool = False) -> logging.Logger:
    """Standardized logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO

    # Check if we are in a container to adjust output
    is_container = os.path.exists('/.dockerenv')

    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    logging.basicConfig(
        level=level,
        format=log_format,
        stream=sys.stderr  # Skills should output JSON to stdout, logs to stderr
    )

    return logging.getLogger(name)

def retry_with_backoff(max_retries: int = 3, initial_delay: float = 1.0, backoff_factor: float = 2.0):
    """Decorator for retrying functions with exponential backoff."""
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            delay = initial_delay
            while retries <= max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if retries == max_retries:
                        logging.error(f"Failed {func.__name__} after {max_retries} retries: {e}")
                        raise

                    logging.warning(f"Error in {func.__name__}: {e}. Retrying in {delay:.1f}s... ({retries + 1}/{max_retries})")
                    time.sleep(delay)
                    retries += 1
                    delay *= backoff_factor
            return None
        return wrapper
    return decorator

def safe_ollama_call(url: str, prompt: str, model: str, timeout: int = 60) -> dict:
    """
    Standardized safe call to Ollama with error handling and retry placeholder.
    Returns response or empty dict on error.
    """
    try:
        res = requests.post(
            url,
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=timeout
        )
        if res.status_code == 200:
            return res.json()
        else:
            logging.error(f"Ollama returned HTTP {res.status_code}: {res.text}")
            return {"error": f"HTTP {res.status_code}"}
    except requests.exceptions.Timeout:
        logging.error(f"Ollama request timed out after {timeout}s")
        return {"error": "timeout"}
    except Exception as e:
        logging.error(f"Ollama connection error: {e}")
        return {"error": str(e)}

def print_json_stderr(data: Any):
    """Print results as JSON to stdout and logs to stderr to keep them separate."""
    import json
    print(json.dumps(data, indent=2, ensure_ascii=False))
