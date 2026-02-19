# Rebase Interactivo: Edición del Historial

La rebase interactiva es la herramienta principal para preparar un historial de commits profesional antes de un PR.

## Operaciones Comunes
- **pick**: Mantiene el commit.
- **reword**: Cambia solo el mensaje del commit.
- **edit**: Permite modificar los archivos del commit.
- **squash**: Combina el commit con el anterior y permite editar el mensaje final.
- **fixup**: Como squash, pero descarta automáticamente el mensaje del commit actual (ideal para correcciones rápidas).
- **drop**: Elimina el commit por completo.

## Comandos Clave
```bash
# Rebase de los últimos 5 commits
git rebase -i HEAD~5

# Rebase desde la base de la rama actual con main
git rebase -i $(git merge-base HEAD main)

# Autosquash automático (si usas --fixup)
git rebase -i --autosquash main
```

## Flujo de Trabajo: Limpieza Pre-PR
1. `git checkout feature/mi-rama`
2. `git rebase -i main`
3. En el editor, marca como `fixup` o `squash` los commits de "fix typo" o "debug".
4. Usa `reword` para asegurar que el commit cumple con el estándar de `commitlint`.
5. `git push --force-with-lease` (Siempre usa lease por seguridad).
