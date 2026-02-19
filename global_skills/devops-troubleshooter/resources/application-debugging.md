# Application & Microservices Debugging

## 1. Comunicación entre Servicios
- **Retries & Backoff**: Evita el efecto "Thundering Herd" (muchos clientes reintentando a la vez).
- **Circuit Breaker**: Deja de enviar tráfico a un servicio que ya está fallando para darle tiempo a recuperarse.
- **Dead Letter Queues (DLQ)**: Mueve mensajes fallidos a una cola especial para análisis manual.

## 2. Depuración de APIs
- **REST**: Validar cabeceras `Content-Type`, `Authorization` y formatos JSON.
- **gRPC**: Problemas de compatibilidad de Protobuf o errores de serialización.
- **GraphQL**: Monitorear la profundidad de las consultas y el problema "N+1" en los resolvers.

## 3. Mensajería (Kafka / RabbitMQ)
- **Consumer Lag**: Los consumidores no procesan los mensajes tan rápido como llegan.
- **Rebalancing**: Problemas de estabilidad en el grupo de consumidores.
- **Poison Pills**: Mensajes con formato corrupto que hacen fallar a cualquier consumidor que intente leerlos.

## 4. Configuración y Entorno
- **Config Drift**: Diferencias no documentadas entre los entornos de Staging y Producción.
- **Secretos caducados**: Certificados TLS o API Keys que dejaron de funcionar.
- **Environment Overrides**: Variables que están siendo sobrescritas en tiempo de ejecución por scripts de CI/CD.

> [!TIP]
> **Idempotencia**: Asegúrate de que reintentar una petición fallida no cause efectos secundarios duplicados (ej: cobrar dos veces al usuario).
