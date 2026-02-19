# Observabilidad y Monitoreo Moderno

## 1. Logs: Del Texto al Conocimiento
No busques líneas, busca patrones.
- **Plataformas**: ELK Stack (Logstash/Kibana), Grafana Loki (altamente eficiente en almacenamiento), Fluentd.
- **Estrategia**:
  - Centralización inmediata.
  - Correlación mediante ID de transacción o `trace-id`.
  - Estructuración (JSON) en origen para consultas rápidas.

## 2. Métricas y Alertas
- **Prometheus & Grafana**: El estándar de facto.
- **Golden Signals**:
  1. **Latencia**: Tiempo que tarda una petición.
  2. **Tráfico**: Demanda del sistema (Req/sec).
  3. **Errores**: Tasa de fallos (explícitos, implícitos o por timeout).
  4. **Saturación**: Qué tan "lleno" está el servicio (limitaciones de CPU/Mem).

## 3. Rastreo Distribuido (Tracing)
Esencial para microservicios donde el fallo puede estar 5 saltos más adelante.
- **Herramientas**: Jaeger, Zipkin, OpenTelemetry (OTel), AWS X-Ray.
- **Implementación**:
  - Propagación de contexto en cabeceras HTTP/gRPC.
  - Instrumentación automática con OTel para lenguajes populares.
  - Spans personalizados para lógica de negocio crítica.

## 4. Monitoreo Sintético
- **Simulación de Usuario**: Pingdom, Datadog Synthetics.
- **Checks de Salud**: No solo "está vivo", sino "¿puede escribir en la DB?".

> [!TIP]
> **Cardinalidad**: Ten cuidado con la alta cardinalidad en las métricas (ej: usar ID de usuario como etiqueta). Puede hacer explotar tu sistema de monitoreo.
