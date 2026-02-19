# pnpm Workspaces & Nx

## pnpm Workspaces (Gestión de Dependencias)
pnpm es el motor de ejecución preferido para monorepos por su velocidad y manejo de dependencias "fantasma".

### pnpm-workspace.yaml
```yaml
packages:
  - 'apps/*'
  - 'packages/*'
```

### Gestión de Paquetes
```bash
# Añadir dependencia a un paquete específico
pnpm add axios --filter @repo/api

# Añadir un paquete local a otro
pnpm add @repo/ui --filter web

# Ejecutar un comando en todos los paquetes recursivamente
pnpm -r build
```

## Nx (Poder y Grafos)
Nx es ideal para monorepos que necesitan más que solo orquestación de tareas, ofreciendo generadores de código y un grafo de dependencias avanzado.

### Comandos de Poder
- **Grafo de Dependencias**: `nx graph` (visualiza cómo se conectan tus paquetes).
- **Proyectos Afectados**: `nx affected:build --base=main` (solo compila lo que cambió respecto a main).
- **Generadores**: `nx generate @nx/react:lib my-ui` (crea un paquete con todo el boilerplate necesario).

### nx.json (Caché y Metas)
Nx utiliza `targetDefaults` para definir el comportamiento de la caché y las dependencias de tareas, similar a Turborepo pero con más granularidad en los "inputs" (archivos que invalidan la caché).
