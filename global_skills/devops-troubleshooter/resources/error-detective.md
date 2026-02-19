# Error Detective: Patrones y Anomalías

## 1. Patrones de Registro (Regex)
La clave para parsear logs masivos es el uso efectivo de expresiones regulares.
- **Error básico**: `(?i)error|fail|critical|fatal` (ignora mayúsculas/minúsculas).
- **Timeout**: `timeout|exceeded|deadline`
- **Networking**: `connection reset|refused|econnrefused`
- **Autenticación**: `401|403|unauthorized|forbidden`

## 2. Análisis de Stack Traces
- **Bottom-Up**: La causa inmediata suele estar al inicio del rastro.
- **Top-Down**: El contexto de la petición está al final del rastro.
- **Anomalías**: Busca hilos bloqueados (`Blocked`), picos de excepciones del mismo tipo o cambios súbitos en el volumen de logs.

## 3. Correlación de Anomalías
- **Tiempo**: ¿Sucedió el error justo después de un despliegue (`git commit`)?
- **Espacio**: ¿Sucede solo en un nodo específico? ¿En una región de AWS en particular?
- **Carga**: ¿Correlaciona el aumento de errores con el aumento de peticiones de un cliente específico?

## 4. Estrategias de Investigación
1. **Diferencial**: Compara logs de un entorno que funciona con uno que no.
2. **Cronológica**: Sigue el flujo de un `trace-id` a través de todos los servicios involucrados.
3. **Estadística**: ¿Es un error del 0.1% o del 100%? Esto define la prioridad.

> [!IMPORTANT]
> **Cascading Failures**: Un error de timeout en un servicio puede causar que las colas de peticiones se llenen en otro, provocando una caída total del sistema.
