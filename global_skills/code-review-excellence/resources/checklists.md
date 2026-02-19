# Checklists de Revisión

## Security Review
- [ ] Input validado y sanitizado.
- [ ] Consultas SQL parametrizadas.
- [ ] Validaciones de AuthZ en cada acción.
- [ ] Sin secretos/API keys hardcodeados.

## Performance Review
- [ ] Sin consultas N+1.
- [ ] Operaciones costosas cacheadas.
- [ ] Listas grandes paginadas.
- [ ] Sin I/O bloqueante en rutas críticas.

## Testing Quality
- [ ] Tests prueban comportamiento, no detalles de implementación.
- [ ] Nombres de tests descriptivos.
- [ ] Casos borde y de error cubiertos.
- [ ] Tests independientes (sin estado compartido).

## Python Specifics
- **Mutable defaults**: Cuidado con `def add_item(i, items=[])`.
- **Catch broad**: Evita `except: pass`. Captura excepciones específicas.
- **Mutable class attributes**: Inicializa en `__init__`.

## TypeScript Specifics
- **Any usage**: Evita `any`, usa interfaces/tipos.
- **Async errors**: Verifica que cada `await` esté manejado o dentro de try-catch.
- **Prop mutation**: No mutar props directamente en componentes.
