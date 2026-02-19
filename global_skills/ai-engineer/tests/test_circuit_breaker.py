#!/usr/bin/env python3
"""
Tests for Circuit Breaker implementation

This module contains comprehensive tests for the Circuit Breaker pattern
implementation used to protect NVIDIA NIM API calls.

Run tests:
    python -m pytest test_circuit_breaker.py -v
    python -m pytest test_circuit_breaker.py::TestCircuitBreaker::test_closed_to_open_transition -v
"""

import asyncio
import pytest
import time
from datetime import datetime
from typing import Optional

import sys
import os

# Add parent directories to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerConfig,
    CircuitState,
    CircuitBreakerMetrics,
    CircuitBreakerOpenException,
    CircuitBreakerRegistry,
    create_nvidia_circuit_breaker
)


class TestCircuitBreakerBasics:
    """Test basic Circuit Breaker functionality"""

    def test_initialization(self):
        """Test that Circuit Breaker initializes correctly"""
        config = CircuitBreakerConfig(
            failure_threshold=3,
            recovery_timeout=10.0
        )
        circuit = CircuitBreaker(name="test", config=config)

        assert circuit.get_state() == CircuitState.CLOSED
        assert circuit.name == "test"
        assert circuit.config.failure_threshold == 3
        assert circuit.config.recovery_timeout == 10.0

    def test_default_configuration(self):
        """Test default Circuit Breaker configuration"""
        circuit = CircuitBreaker(name="test")

        assert circuit.config.failure_threshold == 5
        assert circuit.config.recovery_timeout == 30.0
        assert circuit.config.half_open_max_calls == 1
        assert circuit.config.success_threshold == 2

    @pytest.mark.asyncio
    async def test_successful_call(self):
        """Test that successful calls work normally"""
        circuit = CircuitBreaker(name="test")

        async def success_func():
            return "success"

        result = await circuit.call(success_func)
        assert result == "success"
        assert circuit.get_state() == CircuitState.CLOSED

    @pytest.mark.asyncio
    async def test_failed_call(self):
        """Test that failed calls are handled correctly"""
        config = CircuitBreakerConfig(expected_exceptions=[ValueError])
        circuit = CircuitBreaker(name="test", config=config)

        async def fail_func():
            raise ValueError("Test error")

        with pytest.raises(ValueError):
            await circuit.call(fail_func)

        metrics = circuit.get_metrics()
        assert metrics.failure_count == 1


class TestCircuitBreakerStateTransitions:
    """Test Circuit Breaker state transitions"""

    @pytest.mark.asyncio
    async def test_closed_to_open_transition(self):
        """Test transition from CLOSED to OPEN after failures"""
        config = CircuitBreakerConfig(
            failure_threshold=3,
            expected_exceptions=[Exception]
        )
        circuit = CircuitBreaker(name="test", config=config)

        async def fail_func():
            raise Exception("Test error")

        # Trigger 3 failures
        for i in range(3):
            with pytest.raises(Exception):
                await circuit.call(fail_func)

        # Circuit should be OPEN
        assert circuit.get_state() == CircuitState.OPEN

        metrics = circuit.get_metrics()
        assert metrics.failure_count == 3
        assert len(metrics.state_transitions) == 1
        assert metrics.state_transitions[0]["from"] == "closed"
        assert metrics.state_transitions[0]["to"] == "open"

    @pytest.mark.asyncio
    async def test_open_to_half_open_transition(self):
        """Test transition from OPEN to HALF_OPEN after timeout"""
        config = CircuitBreakerConfig(
            failure_threshold=1,
            recovery_timeout=0.1,  # 100ms for fast test
            expected_exceptions=[Exception]
        )
        circuit = CircuitBreaker(name="test", config=config)

        async def fail_func():
            raise Exception("Test error")

        # Trigger failure to open circuit
        with pytest.raises(Exception):
            await circuit.call(fail_func)

        assert circuit.get_state() == CircuitState.OPEN

        # Wait for recovery timeout
        await asyncio.sleep(0.15)

        # Next call should transition to HALF_OPEN
        # But since _can_execute is checked inside call, we need to check
        # if we can execute
        can_execute = await circuit._can_execute()
        assert can_execute  # Should be allowed in HALF_OPEN
        assert circuit.get_state() == CircuitState.HALF_OPEN

    @pytest.mark.asyncio
    async def test_half_open_to_closed_transition(self):
        """Test transition from HALF_OPEN to CLOSED after success"""
        config = CircuitBreakerConfig(
            failure_threshold=1,
            recovery_timeout=0.1,
            success_threshold=1,  # Only 1 success needed
            expected_exceptions=[Exception]
        )
        circuit = CircuitBreaker(name="test", config=config)

        async def fail_func():
            raise Exception("Test error")

        async def success_func():
            return "success"

        # Open the circuit
        with pytest.raises(Exception):
            await circuit.call(fail_func)

        assert circuit.get_state() == CircuitState.OPEN

        # Wait for recovery
        await asyncio.sleep(0.15)

        # Success should close the circuit
        result = await circuit.call(success_func)
        assert result == "success"
        assert circuit.get_state() == CircuitState.CLOSED

    @pytest.mark.asyncio
    async def test_half_open_to_open_transition(self):
        """Test transition from HALF_OPEN back to OPEN after failure"""
        config = CircuitBreakerConfig(
            failure_threshold=1,
            recovery_timeout=0.1,
            expected_exceptions=[Exception]
        )
        circuit = CircuitBreaker(name="test", config=config)

        async def fail_func():
            raise Exception("Test error")

        # Open the circuit
        with pytest.raises(Exception):
            await circuit.call(fail_func)

        assert circuit.get_state() == CircuitState.OPEN

        # Wait for recovery
        await asyncio.sleep(0.15)

        # Failure in HALF_OPEN should go back to OPEN
        with pytest.raises(Exception):
            await circuit.call(fail_func)

        assert circuit.get_state() == CircuitState.OPEN


class TestCircuitBreakerFallback:
    """Test Circuit Breaker fallback behavior"""

    @pytest.mark.asyncio
    async def test_rejection_when_open(self):
        """Test that calls are rejected when circuit is OPEN"""
        config = CircuitBreakerConfig(
            failure_threshold=1,
            expected_exceptions=[Exception]
        )
        circuit = CircuitBreaker(name="test", config=config)

        async def fail_func():
            raise Exception("Test error")

        # Open the circuit
        with pytest.raises(Exception):
            await circuit.call(fail_func)

        assert circuit.get_state() == CircuitState.OPEN

        # Next call should be rejected
        async def any_func():
            return "should not execute"

        with pytest.raises(CircuitBreakerOpenException) as exc_info:
            await circuit.call(any_func)

        assert "test" in str(exc_info.value)
        assert exc_info.value.circuit_name == "test"

        metrics = circuit.get_metrics()
        assert metrics.rejected_calls == 1

    @pytest.mark.asyncio
    async def test_no_rejection_for_unexpected_exceptions(self):
        """Test that unexpected exceptions don't affect the circuit"""
        config = CircuitBreakerConfig(
            failure_threshold=3,
            expected_exceptions=[ValueError]  # Only ValueError counts
        )
        circuit = CircuitBreaker(name="test", config=config)

        async def type_error_func():
            raise TypeError("Unexpected error")

        # TypeError should not affect the circuit
        with pytest.raises(TypeError):
            await circuit.call(type_error_func)

        assert circuit.get_state() == CircuitState.CLOSED
        metrics = circuit.get_metrics()
        assert metrics.failure_count == 0  # Should not count


class TestCircuitBreakerMetrics:
    """Test Circuit Breaker metrics collection"""

    @pytest.mark.asyncio
    async def test_metrics_tracking(self):
        """Test that metrics are properly tracked"""
        circuit = CircuitBreaker(name="test")

        async def success_func():
            return "success"

        async def fail_func():
            raise ValueError("Test error")

        # Mix of success and failures
        await circuit.call(success_func)

        with pytest.raises(ValueError):
            await circuit.call(fail_func)

        await circuit.call(success_func)

        metrics = circuit.get_metrics()
        assert metrics.total_calls == 3
        assert metrics.success_count >= 1
        assert metrics.failure_count == 0  # Reset after success

    @pytest.mark.asyncio
    async def test_metrics_timestamps(self):
        """Test that timestamps are recorded"""
        config = CircuitBreakerConfig(expected_exceptions=[Exception])
        circuit = CircuitBreaker(name="test", config=config)

        before = datetime.now()

        async def fail_func():
            raise Exception("Test error")

        with pytest.raises(Exception):
            await circuit.call(fail_func)

        metrics = circuit.get_metrics()
        assert metrics.last_failure_time is not None
        assert metrics.last_failure_time >= before

    def test_metrics_to_dict(self):
        """Test metrics serialization"""
        circuit = CircuitBreaker(name="test")
        metrics = circuit.get_metrics()

        data = metrics.to_dict()
        assert "state" in data
        assert "failure_count" in data
        assert "total_calls" in data
        assert isinstance(data["state"], str)


class TestCircuitBreakerRegistry:
    """Test Circuit Breaker Registry"""

    def test_registry_singleton(self):
        """Test that registry is a singleton"""
        registry1 = CircuitBreakerRegistry()
        registry2 = CircuitBreakerRegistry()

        assert registry1 is registry2

    def test_register_and_get(self):
        """Test registering and retrieving circuit breakers"""
        registry = CircuitBreakerRegistry()
        circuit = CircuitBreaker(name="test_circuit")

        registry.register("test_circuit", circuit)

        retrieved = registry.get("test_circuit")
        assert retrieved is circuit

    def test_get_all(self):
        """Test getting all registered circuit breakers"""
        registry = CircuitBreakerRegistry()
        circuit1 = CircuitBreaker(name="circuit1")
        circuit2 = CircuitBreaker(name="circuit2")

        registry.register("circuit1", circuit1)
        registry.register("circuit2", circuit2)

        all_circuits = registry.get_all()
        assert "circuit1" in all_circuits
        assert "circuit2" in all_circuits

    @pytest.mark.asyncio
    async def test_get_all_status(self):
        """Test getting status of all circuits"""
        registry = CircuitBreakerRegistry()
        circuit = CircuitBreaker(name="test")
        registry.register("test", circuit)

        status = await registry.get_all_status()
        assert "test" in status
        assert status["test"]["state"] == "closed"


class TestCircuitBreakerDecorator:
    """Test Circuit Breaker as decorator"""

    @pytest.mark.asyncio
    async def test_decorator_success(self):
        """Test decorator with successful function"""
        circuit = CircuitBreaker(name="test")

        @circuit.protect
        async def protected_func():
            return "success"

        result = await protected_func()
        assert result == "success"

    @pytest.mark.asyncio
    async def test_decorator_failure(self):
        """Test decorator with failing function"""
        config = CircuitBreakerConfig(
            failure_threshold=1,
            expected_exceptions=[Exception]
        )
        circuit = CircuitBreaker(name="test", config=config)

        @circuit.protect
        async def protected_fail():
            raise Exception("Test error")

        with pytest.raises(Exception):
            await protected_fail()

        assert circuit.get_state() == CircuitState.OPEN


class TestCircuitBreakerReset:
    """Test Circuit Breaker reset functionality"""

    @pytest.mark.asyncio
    async def test_manual_reset(self):
        """Test manual reset of circuit breaker"""
        config = CircuitBreakerConfig(
            failure_threshold=1,
            expected_exceptions=[Exception]
        )
        circuit = CircuitBreaker(name="test", config=config)

        async def fail_func():
            raise Exception("Test error")

        # Open the circuit
        with pytest.raises(Exception):
            await circuit.call(fail_func)

        assert circuit.get_state() == CircuitState.OPEN

        # Reset the circuit
        circuit.reset()

        # Wait for reset to complete
        await asyncio.sleep(0.1)

        assert circuit.get_state() == CircuitState.CLOSED
        metrics = circuit.get_metrics()
        assert metrics.failure_count == 0


class TestCircuitBreakerStatus:
    """Test Circuit Breaker status reporting"""

    @pytest.mark.asyncio
    async def test_get_status(self):
        """Test getting complete circuit status"""
        circuit = CircuitBreaker(name="test")

        status = await circuit.get_status()

        assert status["name"] == "test"
        assert status["state"] == "closed"
        assert "metrics" in status
        assert "config" in status
        assert "time_in_state_seconds" in status

    @pytest.mark.asyncio
    async def test_status_updates_after_transition(self):
        """Test that status reflects state changes"""
        config = CircuitBreakerConfig(
            failure_threshold=1,
            expected_exceptions=[Exception]
        )
        circuit = CircuitBreaker(name="test", config=config)

        async def fail_func():
            raise Exception("Test error")

        # Initial status
        status1 = await circuit.get_status()
        assert status1["state"] == "closed"

        # Open circuit
        with pytest.raises(Exception):
            await circuit.call(fail_func)

        status2 = await circuit.get_status()
        assert status2["state"] == "open"
        assert status2["metrics"]["failure_count"] == 1


class TestCircuitBreakerConcurrency:
    """Test Circuit Breaker thread safety"""

    @pytest.mark.asyncio
    async def test_concurrent_calls(self):
        """Test concurrent calls don't corrupt state"""
        circuit = CircuitBreaker(name="test")

        async def success_func():
            await asyncio.sleep(0.01)  # Small delay
            return "success"

        # Launch 10 concurrent calls
        tasks = [circuit.call(success_func) for _ in range(10)]
        results = await asyncio.gather(*tasks)

        assert all(r == "success" for r in results)
        assert circuit.get_state() == CircuitState.CLOSED

    @pytest.mark.asyncio
    async def test_concurrent_failures(self):
        """Test concurrent failures are handled correctly"""
        config = CircuitBreakerConfig(
            failure_threshold=5,
            expected_exceptions=[Exception]
        )
        circuit = CircuitBreaker(name="test", config=config)

        async def fail_func():
            raise Exception("Test error")

        # Launch 10 concurrent failing calls
        tasks = [circuit.call(fail_func) for _ in range(10)]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Circuit should be open
        assert circuit.get_state() == CircuitState.OPEN

        # Count exceptions
        exceptions = [r for r in results if isinstance(r, Exception)]
        assert len(exceptions) == 10


class TestNVIDIASpecific:
    """Test NVIDIA-specific circuit breaker configuration"""

    def test_create_nvidia_circuit_breaker(self):
        """Test factory function for NVIDIA circuit breaker"""
        circuit = create_nvidia_circuit_breaker(
            name="nvidia_test",
            failure_threshold=3,
            recovery_timeout=60.0
        )

        assert circuit.name == "nvidia_test"
        assert circuit.config.failure_threshold == 3
        assert circuit.config.recovery_timeout == 60.0

        # Should have requests exceptions registered
        import requests
        assert requests.exceptions.HTTPError in circuit.config.expected_exceptions

    def test_nvidia_circuit_breaker_registry(self):
        """Test that NVIDIA circuit breaker is registered"""
        circuit = create_nvidia_circuit_breaker(name="nvidia_test_2")

        registry = CircuitBreakerRegistry()
        assert registry.get("nvidia_test_2") is circuit


class TestCircuitBreakerIntegration:
    """Integration tests with simulated API calls"""

    @pytest.mark.asyncio
    async def test_simulated_api_rate_limit(self):
        """Test behavior with simulated rate limit errors"""
        config = CircuitBreakerConfig(
            failure_threshold=2,
            expected_exceptions=[Exception]
        )
        circuit = CircuitBreaker(name="api_test", config=config)

        call_count = 0

        async def simulated_api():
            nonlocal call_count
            call_count += 1
            raise Exception("429 Too Many Requests")

        # First 2 calls should fail but be attempted
        for i in range(2):
            with pytest.raises(Exception):
                await circuit.call(simulated_api)

        assert call_count == 2
        assert circuit.get_state() == CircuitState.OPEN

        # Next call should be rejected immediately
        with pytest.raises(CircuitBreakerOpenException):
            await circuit.call(simulated_api)

        # Call count should still be 2 (no new attempts)
        assert call_count == 2

    @pytest.mark.asyncio
    async def test_recovery_after_rate_limit(self):
        """Test recovery after rate limit period"""
        config = CircuitBreakerConfig(
            failure_threshold=1,
            recovery_timeout=0.1,  # Fast recovery for testing
            success_threshold=1,
            expected_exceptions=[Exception]
        )
        circuit = CircuitBreaker(name="api_test", config=config)

        call_count = 0
        should_succeed = False

        async def simulated_api():
            nonlocal call_count
            call_count += 1
            if not should_succeed:
                raise Exception("429 Too Many Requests")
            return "success"

        # Trigger circuit open
        with pytest.raises(Exception):
            await circuit.call(simulated_api)

        assert circuit.get_state() == CircuitState.OPEN

        # Wait for recovery timeout
        await asyncio.sleep(0.15)

        # Now API should work
        should_succeed = True
        result = await circuit.call(simulated_api)

        assert result == "success"
        assert circuit.get_state() == CircuitState.CLOSED


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
