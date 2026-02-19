# Mejores Prácticas y Checklists Rápidos

## Checklist de Depuración Rápida
Antes de rendirte, revisa:
- [ ] ¿Hay typos en los nombres de variables?
- [ ] ¿Es un problema de Case Sensitivity?
- [ ] ¿Hay valores null o undefined no manejados?
- [ ] ¿Errores de índice (off-by-one) en arrays?
- [ ] ¿Variables de entorno faltantes o incorrectas?
- [ ] ¿Caché desactualizada o persistente?
- [ ] ¿Paths relativos vs absolutos?

## Trampas Comunes
- **Cambios Múltiples**: Cambiar varias cosas a la vez impide saber qué arregló el problema. Cambia UNA sola cosa cada vez.
- **No leer el Stack Trace**: Leer solo la primera línea no basta; el error real suele estar más abajo.
- **Ignorar errores async**: Olvidar el manejo de promesas rechazadas (`unhandledRejection`).
- **Resolver el síntoma, no la causa**: Si un valor es nulo, no solo pongas un chequeo trivial; descubre POR QUÉ es nulo.

## Regla de Oro
**Corrige la causa raíz**, no solo el síntoma visible. Documenta tus hallazgos para ayudar a tu "yo del futuro".
