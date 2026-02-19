# Git Worktrees: Multi-contexto sin fricciones

Los worktrees permiten tener múltiples directorios de trabajo para el mismo repositorio, eliminando la necesidad de hacer `stash` o cambiar constantemente de rama.

## Ventajas
- Corregir un bug crítico en `main` mientras desarrollas una feature pesada sin mover nada.
- Ejecutar tests en una rama mientras editas en otra.
- Comparar visualmente (con tu IDE) dos ramas abriendo dos carpetas.

## Operaciones Comunes
```bash
# Listar worktrees actuales
git worktree list

# Añadir un worktree para un hotfix urgente en una carpeta vecina
git worktree add -b hotfix/bug-urgente ../hotelcrm-hotfix main

# Añadir un worktree de una rama existente
git worktree add ../hotelcrm-feature feature/nueva-funcionalidad

# Eliminar un worktree cuando termines
git worktree remove ../hotelcrm-hotfix
git worktree prune  # Para limpiar referencias huérfanas
```

## Buenas Prácticas
- Crea los worktrees en directorios fuera de tu repositorio principal (un nivel arriba).
- Úsalos para tareas de corta duración o revisiones comparativas.
