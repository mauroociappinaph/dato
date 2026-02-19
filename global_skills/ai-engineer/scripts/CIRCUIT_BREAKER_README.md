# 🛡️ Circuit Breaker Pattern

Implementación del patrón **Circuit Breaker** para protección de APIs contra rate limits y fallos en cascada.

## 📋 Overview

El Circuit Breaker es un patrón de diseño que previene fallos en cascada cuando un servicio externo (como NVIDIA NIM) experimenta problemas. En lugar de seguir intentando requests fallidos, el circuit breaker "abre" el circuito y redirige el tráfico a un fallback (Ollama local).

### Estados del Circuito

```
┌─────────┐     5 fallos     ┌─────────┐
│ CLOSED  │ ───────────────→ │  OPEN   │
│ (normal)│                  │(fallando│
└────┬────┘                  └────┬────┘
     │                            │
     │     30s timeout            │
     │ ←──────────────────────────┘
     │
     │ 1 éxito
     ↓
┌───────────┐
│ HALF_OPEN │
│  (prueba) │
└───────────┘
```

## 🚀 Uso Rápido

### Integrado con NVIDIA NIM Client

```python
from ai_engineer.scripts.nvidia_nim_client import NVIDIANIMClient

# Circuit Breaker está habilitado por defecto
client = NVIDIANIMClient()

# Generar texto - el circuit breaker protege automáticamente
response = client.generate("Explain quantum computing")
print(response.text)
print(f"Source: {response.source}")  # nvidia u ollama
print(f"Circuit: {response.circuit_state}")
```

### Uso Independiente

```python
from ai_engineer.scripts.circuit_breaker import (
    CircuitBreaker, CircuitBreakerConfig, CircuitState
)

# Crear circuit breaker con configuración personalizada
config = CircuitBreakerConfig(
    failure_threshold=5,          # Fallos antes de abrir
    recovery_timeout=30.0,        # Segundos antes de recuperación
    half_open_max_calls=1,        # Calls en estado half-open
    success_threshold=2,          # Éxitos para cerrar
    expected_exceptions=[Exception]  # Excepciones que cuentan
)

circuit = CircuitBreaker(name="my_api", config=config)

# Ejecutar función protegida
async def my_api_call():
    return await external_api.request()

result = await circuit.call(my_api_call)
```

### Como Decorador

```python
from circuit_breaker import CircuitBreaker

circuit = CircuitBreaker("api_calls")

@circuit.protect
async def fetch_user_data(user_id):
    return await api.get_user(user_id)

# La función está automáticamente protegida
user = await fetch_user_data(123)
```

## ⚙️ Configuración

### Configuración Básica

```python
config = CircuitBreakerConfig(
    failure_threshold=5,       # Número de fallos consecutivos antes de abrir
    recovery_timeout=30.0,     # Tiempo en segundos antes de intentar recuperación
    half_open_max_calls=1,     # Máximo de calls permitidos en half-open
    success_threshold=2,       # Éxitos consecutivos para cerrar desde half-open
    expected_exceptions=[      # Lista de excepciones que cuentan como fallo
        requests.exceptions.HTTPError,
        requests.exceptions.Timeout,
        requests.exceptions.ConnectionError
    ]
)
```

### Configuración por Tier de Skill

**Ultra/High (Skills críticos):**
```python
CircuitBreakerConfig(
    failure_threshold=3,      # Más sensible para proteger skills caros
    recovery_timeout=60.0     # Recuperación más conservadora
)
```

**Medium/Low (Skills operacionales):**
```python
CircuitBreakerConfig(
    failure_threshold=5,      # Más tolerante
    recovery_timeout=30.0     # Recuperación estándar
)
```

## 📊 Monitoreo

### Obtener Estado del Circuito

```python
# Usando NVIDIA Client
client = NVIDIANIMClient()
status = client.get_circuit_breaker_status()

print(f"Estado: {status['state']}")  # closed, open, half_open
print(f"Tiempo en estado: {status['time_in_state_seconds']}s")
print(f"Total llamadas: {status['metrics']['total_calls']}")
print(f"Rechazadas: {status['metrics']['rejected_calls']}")
print(f"Fallbacks: {status['metrics']['fallback_count']}")
```

### Estadísticas de Uso

```python
stats = client.get_usage_stats()

print(f"Total requests: {stats['total_requests']}")
print(f"Total tokens: {stats['total_tokens']}")
print(f"Circuit state: {stats['circuit_state']}")
print(f"Circuit failures: {stats['circuit_failure_count']}")
```

### Métricas del Circuit Breaker

```python
metrics = circuit.get_metrics()

print(f"State: {metrics.state.value}")
print(f"Failures: {metrics.failure_count}")
print(f"Successes: {metrics.success_count}")
print(f"Total calls: {metrics.total_calls}")
print(f"Rejected: {metrics.rejected_calls}")
print(f"Fallbacks: {metrics.fallback_count}")
print(f"Last failure: {metrics.last_failure_time}")
```

## 🎮 Control Manual

### Reset del Circuito

```python
# Reset manual a estado CLOSED
client.reset_circuit_breaker()
# Output: 🔄 Circuit Breaker manually reset to CLOSED
```

### Habilitar/Deshabilitar

```python
# Deshabilitar Circuit Breaker
client.disable_circuit_breaker()

# Habilitar Circuit Breaker
client.enable_circuit_breaker()
```

### Registro Global de Circuitos

```python
from circuit_breaker import CircuitBreakerRegistry

registry = CircuitBreakerRegistry()

# Crear múltiples circuitos
circuit1 = CircuitBreaker("api1")
circuit2 = CircuitBreaker("api2")

# Registrar
registry.register("service1", circuit1)
registry.register("service2", circuit2)

# Obtener todos los estados
all_status = await registry.get_all_status()

# Resetear todos
registry.reset_all()
```

## 🧪 Testing

### Ejecutar Tests

```bash
# Tests completos
python -m pytest global_skills/ai-engineer/tests/test_circuit_breaker.py -v

# Tests específicos
python -m pytest test_circuit_breaker.py::TestCircuitBreakerStateTransitions -v

# Demo interactivo
python global_skills/ai-engineer/scripts/circuit_breaker.py
```

### Demo del Circuit Breaker

```bash
python global_skills/ai-engineer/scripts/circuit_breaker.py
```

Output esperado:
```
🧪 Circuit Breaker Demo
==================================================

1. Probando fallos consecutivos...
   Call 1: Simulated API failure
   State: closed
   Call 2: Simulated API failure
   State: closed
   Call 3: Simulated API failure
   State: open

2. Esperando recuperación (5s)...

3. Intentando llamada en half-open...
   Result: Simulated API failure
   State: open

4. Esperando otra recuperación (5s)...

5. Intentando con función exitosa...
   Result: Success!
   State: closed

6. Métricas finales:
   Total calls: 5
   Rejected calls: 1
   State transitions: 3

✅ Demo completado!
```

## 🔧 Integración con Sistema de Costos

El Circuit Breaker se integra automáticamente con el sistema de cost monitoring:

```python
# Las métricas incluyen información del circuit breaker
from cost_monitor.integration import MonitoredSkillEngineAdapter

adapter = MonitoredSkillEngineAdapter(skill_engine)
adapter.execute_skill(request)

# Las métricas del circuit breaker se registran automáticamente
```

## 📈 Casos de Uso

### Rate Limiting (429)

```python
# Cuando NVIDIA retorna 429 Too Many Requests
# El circuit breaker detecta y abre el circuito
# Los siguientes requests usan Ollama inmediatamente

response = client.generate("Large prompt")
if response.source == "ollama":
    print("🔴 Usando fallback - Circuito probablemente abierto")
```

### Errores de Servidor (5xx)

```python
# Errores 500, 502, 503, 504 también activan el circuit breaker
# El sistema se recupera automáticamente después del timeout
```

### Timeouts

```python
# Requests que exceden el timeout (60s) cuentan como fallo
# El circuit breaker protege contra APIs lentas
```

## 🏗️ Arquitectura

### Componentes

1. **CircuitBreaker**: Clase principal con lógica de estados
2. **CircuitState**: Enum con los 3 estados (CLOSED, OPEN, HALF_OPEN)
3. **CircuitBreakerConfig**: Configuración personalizable
4. **CircuitBreakerMetrics**: Métricas y estadísticas
5. **CircuitBreakerRegistry**: Registro global de circuitos

### Thread Safety

El Circuit Breaker es thread-safe usando `asyncio.Lock`:

```python
# Múltiples coroutines pueden usar el circuito simultáneamente
async def concurrent_calls():
    tasks = [
        circuit.call(api_call)
        for _ in range(10)
    ]
    results = await asyncio.gather(*tasks)
```

## 🚨 Troubleshooting

### El circuito no abre

Verificar que las excepciones estén configuradas correctamente:

```python
config = CircuitBreakerConfig(
    expected_exceptions=[
        requests.exceptions.HTTPError,  # Para 429, 5xx
        requests.exceptions.Timeout,
        Exception  # Cualquier excepción
    ]
)
```

### No se usa fallback

Verificar que el fallback esté habilitado:

```python
response = client.generate(
    "prompt",
    fallback=True  # Asegurar que fallback esté activado
)
```

### El circuito no se recupera

Verificar el `recovery_timeout`:

```python
# Para pruebas, usar timeout corto
config = CircuitBreakerConfig(recovery_timeout=5.0)

# En producción, usar timeout más conservador
config = CircuitBreakerConfig(recovery_timeout=60.0)
```

## 📚 Referencia API

### CircuitBreaker

```python
class CircuitBreaker:
    def __init__(self, name: str, config: CircuitBreakerConfig)
    async def call(self, func, *args, **kwargs) -> Any
    def protect(self, func) -> Callable
    def get_state(self) -> CircuitState
    def get_metrics(self) -> CircuitBreakerMetrics
    def reset(self)
    async def get_status(self) -> Dict[str, Any]
```

### CircuitBreakerConfig

```python
@dataclass
class CircuitBreakerConfig:
    failure_threshold: int = 5
    recovery_timeout: float = 30.0
    half_open_max_calls: int = 1
    success_threshold: int = 2
    expected_exceptions: List[Type[Exception]] = [Exception]
```

## 🔗 Referencias

- [Microsoft: Circuit Breaker Pattern](https://docs.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker)
- [Martin Fowler: Circuit Breaker](https://martinfowler.com/bliki/CircuitBreaker.html)
- [NVIDIA NIM Documentation](https://docs.nvidia.com/nim/)

---

**Versión**: 1.0.0
**Última actualización**: 11 de Febrero de 2026
**Estado**: ✅ Producción
