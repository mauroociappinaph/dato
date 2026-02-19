# Técnicas Avanzadas de Depuración

## 1. Git Bisect
Ideal para encontrar qué commit exacto introdujo una regresión.
```bash
git bisect start
git bisect bad                    # El commit actual es malo
git bisect good v1.0.0            # El tag v1.0.0 era bueno
# Git hará checkout del commit intermedio automáticamente
# Pruébalo y dile a git:
git bisect good   # Si funciona
git bisect bad    # Si está roto
# Repite hasta que git identifique el culpable.
git bisect reset  # Para volver al estado original
```

## 2. Depuración Diferencial
Compara sistemáticamente los entornos. Haz una tabla con:
- Versiones de Node/Python
- Datos (BD vacía vs 1M registros)
- Permisos de usuario
- Horarios y Timezones

## 3. Depuración de Seguimiento (Tracing)
Usa decoradores o wrappers para ver exactamente qué entra y qué sale de las funciones sospechosas sin ensuciar el código base con logs permanentes.

## 4. Detección de Fugas de Memoria
- **Heap Snapshots**: En Chrome DevTools, compara snapshots antes y después de una acción.
- **V8 Snapshot**: En Node, usa `v8.writeHeapSnapshot()` para analizar el uso de memoria bajo sospecha.
- **Tests de Fuga**: Mide `process.memoryUsage().heapUsed` en `afterEach` si sospechas de una acumulación de memoria en tus tests.
