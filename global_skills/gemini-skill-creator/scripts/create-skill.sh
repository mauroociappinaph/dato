#!/bin/bash

SKILL_NAME=$1
SKILLS_DIR="/Users/mauroociappina/.gemini/anti_gravity/skills"

if [ -z "$SKILL_NAME" ]; then
  echo "Error: Debes proporcionar un nombre para la habilidad."
  exit 1
fi

TARGET_DIR="$SKILLS_DIR/$SKILL_NAME"

if [ -d "$TARGET_DIR" ]; then
  echo "Error: La habilidad '$SKILL_NAME' ya existe."
  exit 1
fi

mkdir -p "$TARGET_DIR/scripts"
mkdir -p "$TARGET_DIR/examples"
mkdir -p "$TARGET_DIR/resources"

cat <<EOF > "$TARGET_DIR/SKILL.md"
---
name: $SKILL_NAME
description: Descripción de la habilidad $SKILL_NAME
---

# $SKILL_NAME

## Objetivo
[Describe aquí el propósito de la habilidad]

## Instrucciones
[Define las reglas y comportamientos]

## Flujo de Trabajo
1. [Paso 1]
2. [Paso 2]
EOF

echo "Habilidad '$SKILL_NAME' creada exitosamente en $TARGET_DIR"
