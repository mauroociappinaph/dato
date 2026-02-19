# CI/CD para Monorepos

El objetivo en un monorepo es ejecutar solo lo necesario para ahorrar tiempo y créditos de CI.

## 1. Detección de Cambios (Affected)
No compiles todo el repo en cada commit. Usa los mecanismos de Turbo o Nx para filtrar:

```yaml
# GitHub Action con Turborepo
- name: Build Affected
  run: npx turbo run build --filter=...[origin/main]
```

## 2. Caché de CI
Asegúrate de cachear el directorio de `node_modules` y la caché de las herramientas de build.

```yaml
- uses: actions/setup-node@v3
  with:
    node-version: 18
    cache: 'pnpm'

- name: Restore Turbo Cache
  uses: actions/cache@v3
  with:
    path: .turbo
    key: ${{ runner.os }}-turbo-${{ github.sha }}
    restore-keys: |
      ${{ runner.os }}-turbo-
```

## 3. Despliegue Selectivo
En el final de tu pipeline, utiliza scripts para determinar si una aplicación debe ser desplegada basándote en si fue "afectada".
```bash
if npx turbo run build --filter=web --dry=json | grep -q "\"task\": \"build\""; then
  echo "Deploying WEB app..."
  ./scripts/deploy-web.sh
fi
```
