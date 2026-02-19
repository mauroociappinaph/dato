# Conceptos y Fundamentos de Monorepos

## ¿Por qué un Monorepositorio?
### Ventajas
- **Código Compartido**: Reutilización inmediata de componentes UI, utilidades y tipos.
- **Cambios Atómicos**: Una sola PR puede actualizar una API y el Frontend que la consume simultáneamente.
- **Estandarización**: Un solo set de reglas de ESLint, Prettier y TS para todo el equipo.
- **Visibilidad**: Todo el código es fácilmente analizable y refactorizable.

### Desafíos
- **Rendimiento**: Sin herramientas de caché (como Turbo o Nx), las compilaciones pueden volverse eternas.
- **CI/CD Complejo**: Se requiere lógica para detectar qué ha cambiado y qué necesita ser testeado.
- **Tamaño del Repo**: El historial de Git puede crecer rápidamente si no se gestiona bien.

## Herramientas Clave
- **Gestores de Paquetes**: **pnpm** (Altamente recomendado por su eficiencia con hardlinks), npm o Yarn.
- **Sistemas de Build**:
  - **Turborepo**: Ligero, basado en Go, ideal para proyectos basados en Next.js.
  - **Nx**: Muy potente, rico en plugins, excelente para grafos complejos.
  - **Lerna**: El pionero, ahora bajo mantenimiento de Nrwl (Nx).

## Estructura Sugerida
```text
apps/          # Aplicaciones finales (web, docs, mobile)
packages/      # Paquetes compartidos (ui, utils, config, database)
tools/         # Scripts y herramientas internas de build
turbo.json     # Orquestación de tareas
pnpm-workspace.yaml # Definición de paquetes
```
