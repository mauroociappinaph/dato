# Debug & Trace Configuration (Expert Setup)

## 1. VS Code: El Centro de Mando
Configuración para conectar el debugger a procesos locales y remotos (Docker/K8s).

### Node.js Debugging
```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Attach to Docker",
      "type": "node",
      "request": "attach",
      "port": 9229,
      "address": "localhost",
      "localRoot": "${workspaceFolder}",
      "remoteRoot": "/usr/src/app",
      "skipFiles": ["<node_internals>/**"]
    }
  ]
}
```

## 2. Chrome DevTools (Frontend & Node)
- **Memory Tab**: Toma "Heap Snapshots" para encontrar por qué la memoria no baja. Compara dos capturas para ver qué objetos han crecido.
- **Performance Tab**: Analiza el "Main Thread" para ver qué funciones están bloqueando la UI o el event loop de Node.
- **Network Tab**: Filtra por tipo (XHR, JS, CSS) para ver latencias de red y tamaños de payload.

## 3. OpenTelemetry (OTel): Tracing de Producción
Configuración básica para empezar a emitir trazas.

```javascript
// otel-collector.yaml (ejemplo simplificado)
receivers:
  otlp:
    protocols:
      http:
      grpc:
exporters:
  jaeger:
    endpoint: "localhost:14250"
service:
  pipelines:
    traces:
      receivers: [otlp]
      exporters: [jaeger]
```

## 4. Depuración en Producción (Safe)
- **Log Levels Dinámicos**: Cambiar de `INFO` a `DEBUG` sin reiniciar el servicio (usando configuraciones dinámicas o feature flags).
- **Conditional Logging**: Loggear el cuerpo de la petición solo si falla, para ahorrar almacenamiento y proteger la privacidad.
- **Canary Tracing**: Habilitar el tracing detallado solo para un porcentaje pequeño de usuarios.

## 5. Source Map Management
Asegúrate de que los logs de producción apunten a líneas de código legibles, no a código minificado.
- Sube tus source maps a Sentry/Datadog de forma privada durante el pipeline de CI.
