# Mejores Prácticas y Estrategias

## 1. Versionado con Changesets
Gestionar versiones de múltiples paquetes manualmente es imposible. Usa **Changesets** para automatizar el changelog y las versiones.
- `pnpm changeset`: Abre un CLI para documentar qué ha cambiado y qué paquetes afecta.
- `pnpm changeset version`: Bump de versiones automático.
- `pnpm changeset publish`: Publicación automática a NPM o registros internos.

## 2. Evitar Dependencias Circulares
Un error común es que el Paquete A importe del Paquete B, y el Paquete B importe del Paquete A. Esto rompe la compilación y el árbol de dependencias.
**Regla**: Si dos paquetes se necesitan mutuamente, extrae la parte común a un tercer paquete (ej: `@repo/shared`).

## 3. Dependencias Fantasma
Usa siempre `pnpm` con su estructura de `node_modules` no plana. Esto evita que uses paquetes que no has declarado explícitamente en tu `package.json`, eliminando errores aleatorios en producción.

## 4. Commits Atómicos
Aprovecha el monorepo para hacer commits que tengan sentido completo:
*"feat(api): add user endpoint and @repo/types update"*
Esto hace que revertir cambios sea trivial y que el historial sea una joya de claridad.

## Checklist de Salud del Monorepo
- [ ] ¿Hay builds que fallan en cascada sin motivo? (Revisa entradas/salidas de caché).
- [ ] ¿Los tiempos de CI están aumentando linealmente? (Activa Remote Caching).
- [ ] ¿Es fácil para un nuevo dev levantar el proyecto? (Documenta el `pnpm install` y `pnpm dev`).
