# SOP-003: CI/CD Troubleshooting - DATO

> **Ver también:** [SOP de Incidentes](incidents.md)

---

## FASE 0-1: Troubleshooting Simple

**Si el CI falla, el flujo es:**

```
1. gh run view --log  →  Leés el error
2. Arreglás el código localmente
3. git push           →  CI corre de nuevo
```

### Comandos Útiles

```bash
# Ver último run fallido
gh run list --status=failure --limit=1

# Ver logs de un run específico
gh run view <run-id> --log

# Re-run un workflow
gh run rerun <run-id>

# Ver diferencias con último exitoso
git diff origin/develop HEAD
```

### Errores Comunes

| Error | Causa | Fix |
|-------|-------|-----|
| Lint error | Código no formateado | `pnpm lint --fix` |
| Type error | Tipo incorrecto | Corregir tipo o agregar `@types/` |
| Test failed | Test roto | Fix del test o del código |
| Build failed | Error de compilación | Ver log, corregir import/tipo |

---

## FASE 2+: Troubleshooting Avanzado

> **Cuándo usar:** Producción activa, incidentes recurrentes, múltiples desarrolladores.

Ver **TASK.md sección 2.5** para implementación de:

| Skill | Función |
|-------|---------|
| `telegram-hq-commander` | Notificaciones automáticas de CI failed |
| `self-correction-pilot` | RCA automático, aplica fixes |
| `post-mortem-memory` | Extrae lecciones, sube a Vector Memory |

### Flujo FASE 2+

```
CI Falla → Telegram alert → self-correction-pilot (RCA + Fix) → post-mortem-memory (lecciones)
```

---

## Rollback (FASE 1+)

Si deploy falla:

```bash
# Vercel
vercel rollback

# Railway
railway rollback
```

---

*Para troubleshooting avanzado con Vector Memory, ver FASE 2 en TASK.md*