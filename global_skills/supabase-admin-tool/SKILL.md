---
name: supabase-admin-tool
description: Interfaz de administración para Supabase via CLI.
---

# Supabase Admin Tool

## Objetivo
Permitir al AGENT_OPS gestionar la infraestructura de base de datos y Edge Functions de forma autónoma.

## Instrucciones
1. Usar siempre `supabase status` antes de realizar cambios.
2. Las migraciones deben ser validadas en un entorno local o de desarrollo antes de aplicarse a producción.
3. Reportar cualquier error de conexión inmediatamente al CEO.

## Flujo de Trabajo
1. `check-status.sh`: Verifica salud del proyecto.
2. `list-tables.sh`: Inspecciona el esquema actual.
3. `db-diff.sh`: Detecta cambios entre local y remoto.