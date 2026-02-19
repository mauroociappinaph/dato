# Recuperación y Reflog: Tu Red de Seguridad

El **Reflog** registra cada movimiento que hace el HEAD, lo que permite recuperar casi cualquier cosa que haya sido commitada en los últimos 90 días.

## Ver el Historial de Movimientos
```bash
git reflog
# O para una rama específica
git reflog show feature/mi-rama
```

## Escenarios de Rescate

### 1. "He hecho un reset --hard por error"
Busca en el reflog el estado anterior al reset (marcado como `HEAD@{1}` usualmente).
```bash
git reset --hard HEAD@{1}
```

### 2. "He borrado una rama y necesito recuperarla"
Encuentra el hash del último commit de esa rama en el reflog.
```bash
git branch nombre-rama-recuperada <hash-del-reflog>
```

### 3. "He perdido un commit después de un rebase fallido"
Si abortaste el rebase o salió mal, puedes volver al estado previo al inicio del rebase buscando el ID en el reflog.

## Comandos de Emergencia (Abortar)
Si te sientes perdido en medio de una operación:
- `git rebase --abort`
- `git merge --abort`
- `git cherry-pick --abort`
- `git bisect reset`
