# Best Practices & Pitfalls

## Best Practices
- **Fail Fast**: Valida la entrada temprano y falla rápido para evitar corromper el estado de la aplicación.
- **Preserve Context**: Incluye stack traces, metadatos, IDs de usuario y timestamps en los errores.
- **Meaningful Messages**: Explica qué pasó y, si es posible, cómo solucionarlo.
- **Handle at Right Level**: Captura el error solo donde puedas manejarlo de forma significativa.
- **Clean Up Resources**: Usa bloques `finally`, manejadores de contexto o `defer` para cerrar conexiones y archivos.
- **Don't Swallow Errors**: Nunca dejes bloques `catch` vacíos. Al menos loguea el error.

## Common Pitfalls
- **Catching Too Broadly**: Capturar `Exception` o `Error` genérico puede ocultar bugs reales de lógica.
- **Logging and Re-throwing**: Evita loguear un error y luego volver a lanzarlo (re-throw), ya que ensucia los logs con duplicados. Loguea en el nivel más alto que capture el error.
- **Poor Error Messages**: Mensajes como "Error occurred" no son útiles para el troubleshooting.
- **Ignoring Async Errors**: Olvidar manejar rechazos de promesas puede causar que la aplicación se cuelgue o muera sin rastro.

---
*Powered by Gemini Skill Creator*
