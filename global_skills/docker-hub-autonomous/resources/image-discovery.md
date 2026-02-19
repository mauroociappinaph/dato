# Descubrimiento Inteligente de Imágenes

Este recurso guía al agente en la selección de la base tecnológica más robusta y eficiente disponible en Docker Hub.

## Criterios de Selección (Jerarquía)
1. **Official Images**: Siempre priorizar las imágenes marcadas como "Docker Official Image".
2. **Verified Publishers**: Imágenes de organizaciones reconocidas (p. ej., Bitnami, Redis, Microsoft).
3. **Reputación Comunitaria**: Validar por número de estrellas, descargas y frecuencia de actualizaciones (frescura).

## Variantes de Imágenes
- **Alpine**: Ultra-ligera basada en musl libc. Ideal para microservicios donde el tamaño es crítico.
- **Slim**: Basada en Debian pero reducida al mínimo necesario para el runtime.
- **Distroless**: Sin gestor de paquetes ni shell. Máxima seguridad para producción.
- **Full/Standard**: Solo permitida en entornos de desarrollo o build stages.

## Flujo de Descubrimiento
1. Definir el runtime requerido (Node.js, Python, Go).
2. Buscar la versión LTS (Long Term Support) más reciente.
3. Evaluar variantes de seguridad (Alpine vs Slim).
4. Verificar soporte de arquitectura (multi-arch: amd64/arm64).

---
*Docker Hub Autonomous - Discovery Module*
