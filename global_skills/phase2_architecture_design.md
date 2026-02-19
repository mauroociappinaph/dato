# FASE 2: DISEÑO ARQUITECTÓNICO
## Skill: ai-solutions-architect

---

## 📊 HALLAZGOS DE FASE 1 (Resumen)

| Métrica | Valor |
|---------|-------|
| Total archivos analizados | 540 |
| Archivos Python (.py) | 367 |
| Archivos Markdown (.md) | 161 |
| Archivos JSON (.json) | 12 |
| **Archivos __init__.py duplicados** | **248** |
| **Archivos > 300 líneas** | **24** |

---

## 🏗️ PROPUESTA DE ARQUITECTURA REFACTORIZADA

### Estructura de Directorios Propuesta

```
global_skills/
├── src/                          # NUEVO: Código fuente centralizado
│   ├── __init__.py              # Barrel file principal
│   ├── core/                     # Lógica compartida entre skills
│   │   ├── __init__.py
│   │   ├── base_skill.py        # Clase base para todos los skills
│   │   ├── interfaces.py        # Interfaces ABC (SkillEngineInterface, etc.)
│   │   └── exceptions.py        # Excepciones personalizadas
│   ├── helpers/                  # Funciones utilitarias reutilizables
│   │   ├── __init__.py
│   │   ├── file_utils.py        # Operaciones de archivo comunes
│   │   ├── validation_utils.py  # Validaciones recurrentes
│   │   └── http_utils.py        # Requests/HTTP comunes
│   └── types/                    # Tipos compartidos
│       ├── __init__.py
│       └── common_types.py      # Dataclasses/Type hints compartidos
│
├── skills/                       # RENOMBRADO: Skills individuales
│   ├── __init__.py              # Barrel file con exports de todos los skills
│   ├── code-modularity-architect/
│   │   ├── __init__.py          # Exporta: CodeModularityArchitect
│   │   ├── SKILL.md
│   │   └── scripts/
│   ├── detect-duplicate-files/
│   ├── technical-debt-analysis/
│   ├── ai-solutions-architect/
│   └── ... (resto de skills)
│
├── tests/                        # NUEVO: Tests centralizados
│   ├── __init__.py
│   ├── unit/
│   ├── integration/
│   └── conftest.py
│
├── docs/                         # NUEVO: Documentación centralizada
│   ├── ARCHITECTURE.md
│   └── CONTRIBUTING.md
│
└── scripts/                      # Scripts de automatización
    ├── generate_barrel_files.py
    └── validate_architecture.py
```

---

## 🎯 PRINCIPIOS APLICADOS

### 1. DRY (Don't Repeat Yourself)
- **Problema**: 248 archivos `__init__.py` idénticos
- **Solución**: Crear template base en `src/core/` y generar barrel files dinámicamente

### 2. SRP (Single Responsibility Principle)
- **Problema**: Archivos > 300 líneas con múltiples responsabilidades
- **Solución**: Splitting quirúrgico - extraer funciones a `src/helpers/`

### 3. The 300 Rule
- **Regla**: Ningún archivo excede 300 líneas de código efectivo
- **Excepción**: Archivos de configuración y tests

### 4. Barrel Files
- Todo módulo debe exponer su API pública mediante `__init__.py`
- Ejemplo:
```python
# src/helpers/__init__.py
from .file_utils import read_skill_file, write_skill_file
from .validation_utils import validate_skill_name

__all__ = ['read_skill_file', 'write_skill_file', 'validate_skill_name']
```

---

## 📋 PLAN DE REFACTORIZACIÓN (FASE 3)

### Paso 1: Crear Infraestructura Base (src/)
- Crear directorios `src/core/`, `src/helpers/`, `src/types/`
- Implementar `base_skill.py` con clase base Skill
- Mover lógica común de `__init__.py` a `src/core/`

### Paso 2: Consolidar __init__.py
- Crear script `scripts/generate_barrel_files.py`
- Generar barrel files con exports dinámicos
- Eliminar 248 archivos `__init__.py` duplicados

### Paso 3: Aplicar The 300 Rule
- Identificar los 24 archivos grandes del análisis
- Extraer funciones a módulos en `src/helpers/`
- Crear tests de caracterización antes de refactorizar

### Paso 4: Migrar Skills a Nueva Estructura
- Mover cada skill a `skills/{skill-name}/`
- Actualizar imports en todos los archivos
- Validar que todo funciona correctamente

---

## 🔗 INTERFACES Y CONTRATOS

### SkillBase (Clase Base)
```python
# src/core/base_skill.py
from abc import ABC, abstractmethod
from typing import Dict, Any

class SkillBase(ABC):
    """Clase base para todos los Global Skills"""

    @property
    @abstractmethod
    def name(self) -> str:
        """Nombre único del skill"""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Descripción del skill"""
        pass

    @abstractmethod
    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Ejecuta el skill con los inputs proporcionados"""
        pass
```

### SkillEngineInterface
```python
# src/core/interfaces.py
from abc import ABC, abstractmethod

class SkillEngineInterface(ABC):
    @abstractmethod
    async def execute_skill(self, request: 'SkillRequest') -> 'SkillResult':
        pass

    @abstractmethod
    async def validate_skills(self, skills: list) -> dict:
        pass
```

---

## ✅ CRITERIOS DE ACEPTACIÓN

1. **Zero Breaking Changes**: Todos los skills deben seguir funcionando
2. **Tests Pass**: Todos los tests existentes deben pasar
3. **No Duplicación**: Eliminados los 248 `__init__.py` duplicados
4. **The 300 Rule**: Ningún archivo excede 300 líneas
5. **100% Barrel Files**: Todos los módulos tienen `__init__.py` con exports

---

## 📈 BENEFICIOS ESPERADOS

| Beneficio | Antes | Después |
|-----------|-------|---------|
| Archivos `__init__.py` | 248 duplicados | ~50 barrel files únicos |
| Líneas de código duplicadas | ~500+ | 0 |
| Tiempo de import | Lento | Optimizado |
| Mantenibilidad | Baja | Alta |
| Escalabilidad | Limitada | Modular |

---

## 🚀 DECISIÓN

**¿Proceder a Fase 3: Implementación?**

- [ ] Sí, aprobar diseño y comenzar implementación
- [ ] No, requiere modificaciones

**Nota**: Este diseño fue generado por `ai-solutions-architect` basándose en los hallazgos de `detect-duplicate-files` + `technical-debt-analysis`.
