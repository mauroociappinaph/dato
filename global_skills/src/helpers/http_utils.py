"""
HTTP utilities for Global Skills.

Common HTTP operations with retry logic and error handling.
"""

import asyncio
import json
from typing import Dict, Any, Optional, Callable
from urllib.parse import urlparse
import aiohttp


async def make_request(
    url: str,
    method: str = "GET",
    headers: Optional[Dict[str, str]] = None,
    json_data: Optional[Dict] = None,
    timeout: int = 30,
) -> tuple[bool, Any]:
    """
    Make an HTTP request with proper error handling.

    Args:
        url: URL to request
        method: HTTP method (GET, POST, etc.)
        headers: Optional headers dict
        json_data: Optional JSON payload
        timeout: Request timeout in seconds

    Returns:
        Tuple of (success, response_data)
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method=method,
                url=url,
                headers=headers,
                json=json_data,
                timeout=aiohttp.ClientTimeout(total=timeout),
            ) as response:
                if response.status >= 200 and response.status < 300:
                    try:
                        data = await response.json()
                        return True, data
                    except:
                        text = await response.text()
                        return True, text
                else:
                    text = await response.text()
                    return False, f"HTTP {response.status}: {text}"
    except asyncio.TimeoutError:
        return False, "Request timeout"
    except Exception as e:
        return False, str(e)


async def make_request_with_retry(
    url: str,
    method: str = "GET",
    headers: Optional[Dict[str, str]] = None,
    json_data: Optional[Dict] = None,
    timeout: int = 30,
    max_retries: int = 3,
    retry_delay: float = 1.0,
) -> tuple[bool, Any]:
    """
    Make an HTTP request with automatic retry logic.

    Args:
        url: URL to request
        method: HTTP method
        headers: Optional headers
        json_data: Optional JSON payload
        timeout: Request timeout
        max_retries: Maximum number of retries
        retry_delay: Initial delay between retries (doubles each time)

    Returns:
        Tuple of (success, response_data)
    """
    last_error = None

    for attempt in range(max_retries):
        success, result = await make_request(
            url=url,
            method=method,
            headers=headers,
            json_data=json_data,
            timeout=timeout,
        )

        if success:
            return True, result

        last_error = result

        # Don't retry on client errors (4xx)
        if isinstance(result, str) and result.startswith("HTTP 4"):
            return False, result

        if attempt < max_retries - 1:
            await asyncio.sleep(retry_delay * (2 ** attempt))

    return False, f"Failed after {max_retries} attempts: {last_error}"


def validate_url(url: str) -> tuple[bool, Optional[str]]:
    """
    Validate a URL format.

    Args:
        url: URL to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        parsed = urlparse(url)

        if not parsed.scheme:
            return False, "URL must have a scheme (http:// or https://)"

        if parsed.scheme not in ("http", "https"):
            return False, f"Unsupported scheme: {parsed.scheme}"

        if not parsed.netloc:
            return False, "URL must have a domain"

        return True, None
    except Exception as e:
        return False, f"Invalid URL format: {e}"


def parse_json_response(response: Any) -> tuple[bool, Any]:
    """
    Safely parse a JSON response.

    Args:
        response: Response data (string or dict)

    Returns:
        Tuple of (success, parsed_data)
    """
    if isinstance(response, dict):
        return True, response

    if isinstance(response, str):
        try:
            return True, json.loads(response)
        except json.JSONDecodeError as e:
            return False, f"JSON parse error: {e}"

    return False, f"Unexpected response type: {type(response)}"


async def fetch_with_auth(
    url: str,
    auth_token: str,
    auth_header: str = "Authorization",
    auth_prefix: str = "Bearer",
    **kwargs
) -> tuple[bool, Any]:
    """
    Make an authenticated HTTP request.

    Args:
        url: URL to request
        auth_token: Authentication token
        auth_header: Header name for auth
        auth_prefix: Prefix for auth token
        **kwargs: Additional arguments for make_request

    Returns:
        Tuple of (success, response_data)
    """
    headers = kwargs.pop("headers", {})
    headers[auth_header] = f"{auth_prefix} {auth_token}"

    return await make_request(url, headers=headers, **kwargs)
