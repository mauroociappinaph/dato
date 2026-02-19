# Estrategias y Mejores Prácticas de Git

## Rebase vs Merge
- **Rebase**: Úsalo para mantener un **historial lineal**. Es ideal para actualizar tu feature branch con los últimos cambios de `main`.
- **Merge**: Úsalo para integrar features completas en `main` o cuando colaboras en ramas públicas para **preservar el contexto** de las fusiones.

## Commits Atómicos
Cada commit debe representar una sola unidad lógica de cambio (ej: "feat: add validation" y "docs: update readme" deben ser commits separados). Esto facilita enormemente el uso de `cherry-pick` y `bisect`.

## Safe Force Push
Nunca uses `git push --force`. Usa siempre:
```bash
git push --force-with-lease
```
Esto evita sobrescribir commits de otros colaboradores que no hayas integrado todavía en tu local.

## Selección de Cerezas (Cherry-Pick)
Aplica cambios específicos de una rama a otra sin fusionar todo:
```bash
git cherry-pick <hash-del-commit>
```
Útil para aplicar un hotfix de `main` en una rama de release antigua.

## Dividir un Commit Grande
Si un commit tiene demasiadas cosas:
1. `git rebase -i <hash-anterior>^`
2. Marca el commit como `edit`.
3. `git reset HEAD^` (mantiene los cambios pero borra el commit).
4. `git add` y `git commit` en partes lógicas.
5. `git rebase --continue`.
