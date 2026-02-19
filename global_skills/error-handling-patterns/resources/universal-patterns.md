# Universal Error Handling Patterns

## Circuit Breaker
Evita fallos en cascada en sistemas distribuidos dejando de llamar a un servicio que está fallando.

```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.state = "CLOSED"
        self.failure_count = 0
        self.last_failure_time = None

    def call(self, func):
        if self.state == "OPEN":
            # Verificar si el timeout ha pasado para pasar a HALF_OPEN
            ...
        try:
            result = func()
            self.on_success()
            return result
        except Exception:
            self.on_failure()
            raise
```

## Error Aggregation
Colecciona múltiples errores (ej. validación de formularios) antes de fallar, en lugar de detenerse en el primero.

```typescript
class ErrorCollector {
    private errors: Error[] = [];
    add(error: Error) { this.errors.push(error); }
    throw() {
        if (this.errors.length > 0) throw new AggregateError(this.errors);
    }
}
```

## Graceful Degradation
Proporciona funcionalidad de respaldo cuando ocurren errores.

```python
def get_exchange_rate(currency: str) -> float:
    return (
        try_function(lambda: api_provider_1.get_rate(currency))
        or try_function(lambda: api_provider_2.get_rate(currency))
        or try_function(lambda: cache.get_rate(currency))
        or DEFAULT_RATE # Último recurso
    )
```
