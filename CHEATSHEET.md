# DATO - Cheatsheet de Ejecución

> **Regla simple:** Si no está en este archivo, no lo tenés que ejecutar.
>
> **Principio YAGNI:** Algunas tareas se movieron a "Tareas Diferidas" (ver TASK.md al final).

---

## FASE 0 (reducida)

| Sección | Subtasks | Qué hace |
|---------|----------|----------|
| 0.1 Git | 5 | Crear repo + ramas |
| 0.2 Config | **5** (era 7) | package.json, tsconfig, lint, husky, errors |
| 0.3 Directorios | 4 | Crear estructura |
| 0.4 CI/CD | **2** (era 4) | GitHub Actions, Secrets |
| 0.5 Supabase | 3 | Tablas + Auth |

**Total: ~20 subtasks** (antes ~25)

---

## Checkpoints de Validación

| CP | Cuándo | Qué validar | Con quién |
|----|--------|-------------|-----------|
| **CP0** | Post FASE 0 (día 7) | Setup técnico funciona | Vos (automatizado) |
| **CP1** | Día 14 (post FASE 1) | Badges, simplificación, flujo | 3-5 amigos |
| **CP2** | Día 60 (post FASE 2) | Búsqueda, notificaciones, retención | 5-10 usuarios reales |

**Regla:** No pasar a la siguiente fase hasta pasar el checkpoint.

### CP0 - Checklist rápido

```bash
pnpm install     # Sin errores
pnpm lint        # Sin errores
pnpm typecheck   # Sin errores
```

Si algo falla → fix antes de FASE 1.

---

## Se ejecuta SOLO (no hagas nada)

| Qué | Cuándo | Dónde |
|-----|--------|-------|
| Validación de código (lint, prettier, typecheck) | Cada `git commit` | Husky pre-commit |
| Secret scanning (gitleaks) | Cada `git commit` | Husky pre-commit |
| Dependency vulnerabilities (quick) | Cada `git commit` | Husky pre-commit |
| Build + tests | Cada `git push` | Husky pre-push |
| Dependency vulnerabilities (full) | Cada PR | GitHub Actions |
| OWASP security audit | Cada push a main + cron semanal | GitHub Actions |
| Auto-label issues/triage | Diario 00:00 UTC | GitHub Actions |
| Detección de código duplicado | Cada domingo 00:00 UTC | GitHub Actions |
| Performance (Lighthouse) | Cada PR | GitHub Actions |
| Smoke tests post-deploy | Después de deploy | GitHub Actions |

---

## Tenés que ejecutar YO (manual)

| Comando | Para qué | Cuándo usar |
|---------|----------|-------------|
| `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py [SUBTASK]` | Generar prompt de ejecución | Antes de empezar una subtask |
| `/jules "[tarea]"` | Delegar tarea pesada a background | Refactors grandes, bulk docs |
| `pnpm duplicates:check` | Verificar duplicados manualmente | Cuando lo necesites (no en FASE 0) |
| `pnpm modularity:check` | Verificar archivos >300 líneas | Cuando lo necesites (no en FASE 0) |

> **Nota:** `pnpm docs:generate` se agregará en FASE 1 cuando haya código que documentar.

---

## Flujo de trabajo típico

```
1. Elegís subtask (ej: 0.2.1)
   ↓
2. python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 0.2.1
   ↓
3. Leés el prompt generado y ejecutás la tarea
   ↓
4. git add . && git commit -m "feat(config): add package.json"
   ↓ (Husky valida automáticamente: lint, prettier, typecheck, gitleaks)
   ↓
5. git push
   ↓ (Husky valida: build, tests)
   ↓
6. Creás PR → GitHub Actions corre CI
```

---

## Skills que YA están planeadas

| Skill | Dónde se usa | Ejecución |
|-------|--------------|-----------|
| `api-endpoint-tester` | Task 1.11 (Smoke tests) | Automática post-deploy |
| `asynchronous-jules-helper` | Refactors grandes | Manual con `/jules` |

---

## Comandos útiles

```bash
# Ver estructura de tareas
cat TASK.md

# Ver progreso
grep -E "^\- \[x\]" TASK.md | wc -l  # Completadas
grep -E "^\- \[ \]" TASK.md | wc -l  # Pendientes

# Formatear código si falló pre-commit
pnpm format

# Correr tests manualmente
pnpm test
```

---

## Si algo falla

| Error | Solución |
|-------|----------|
| `pre-commit failed` | `pnpm format` + revisar errores |
| `pre-push failed` | `pnpm build && pnpm test` localmente |
| `CI failed` | Revisar logs en GitHub Actions |
| `No entiendo la task` | `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py [SUBTASK]` |

---

## Templates de Workflows (configurar cuando se necesiten)

### Stress Testing Semanal (Agent 3)

```yaml
# .github/workflows/stress-test.yml
name: Weekly RAG Stress Test
on:
  schedule:
    - cron: '0 6 * * 1'  # Lunes 6:00 UTC
  workflow_dispatch:  # Manual trigger

jobs:
  stress-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Run agentic-stress-tester
        run: |
          # Generar queries adversarias y testear Agent 3
          # Usa @global_skills/agentic-stress-tester/
          
      - name: Create issue if failures
        if: failure()
        uses: actions/create-issue@v1
        with:
          title: "🔴 RAG Stress Test Failed"
          labels: bug,agent-3
```

**Cuándo configurar:** Post-implementación Agent 3 (FASE 1).