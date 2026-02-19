# Git Bisect: Búsqueda Binaria de Errores

`bisect` es la herramienta definitiva para encontrar exactamente qué commit introdujo una regresión.

## Proceso Manual
1. **Iniciar**: `git bisect start`
2. **Marcar estado malo**: `git bisect bad` (normalmente el actual)
3. **Marcar estado bueno**: `git bisect good v1.0.0` (o un hash antiguo)
4. **Testeo**: Git hará checkout de commits intermedios. Pruébalos y dile:
   - `git bisect good` si funciona.
   - `git bisect bad` si falla.
5. **Fin**: Una vez identificado el commit culpable, sal con `git bisect reset`.

## Bisección Automatizada (Pro)
Si tienes un script de test (como `npm test` o similar) que sale con código 0 o 1, puedes automatizarlo:
```bash
git bisect start HEAD v1.0.0
git bisect run npm test
```
Git encontrará el culpable solo mientras te tomas un café.
