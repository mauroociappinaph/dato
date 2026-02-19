#!/bin/bash
# 🚀 Supabase Status Checker

echo "🔍 Verificando estado de Supabase..."
supabase status

if [ $? -eq 0 ]; then
  echo "✅ Sistema operativo."
else
  echo "❌ Error: No se pudo conectar con el proyecto local de Supabase. ¿Está el Docker encendido?"
fi
