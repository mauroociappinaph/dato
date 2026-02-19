# Cherry-Picking: Aplicación Selectiva

El cherry-picking permite aplicar commits específicos de una rama a otra sin realizar una fusión completa.

## Comandos Esenciales
```bash
# Cherry-pick de un solo commit
git cherry-pick abc123

# Cherry-pick de un rango (el primero es exclusivo)
git cherry-pick abc123..def456

# Cherry-pick sin commitear (deja los cambios en staging)
git cherry-pick -n abc123

# Editar mensaje al cherry-pickear
git cherry-pick -e abc123
```

## Manejo de Conflictos
Si hay conflictos durante el proceso:
1. Resuelve los conflictos en los archivos.
2. `git add <archivos-resueltos>`
3. `git cherry-pick --continue`

Si decides cancelar:
`git cherry-pick --abort`

## Cherry-pick Parcial
Para aplicar solo archivos específicos de un commit:
```bash
git checkout <hash-del-commit> -- path/to/file.py
git commit -m "cherry-pick: apply specific files from <hash>"
```
