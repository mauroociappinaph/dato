# Arquitectura de Motores - Separación de Responsabilidades

## Visión General

Esta arquitectura implementa una clara separación de responsabilidades entre el **Playbook Engine** y el **Skill Engine**, asegurando que cada motor tenga un propósito bien definido y evitando duplicación de funcionalidades.

## Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENTES EXTERNOS                        │
│  (CLI, API REST, Web UI, Otros Sistemas)                       │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      │ 1. Solicitud de Playbook
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PLAYBOOK ENGINE                              │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │              ORQUESTACIÓN Y FLUJO                           │ │
│  │  ┌─────────────────┐  ┌─────────────────┐                  │ │
│  │  │   Validación    │  │   Planificación   │                  │ │
│  │  │   de Playbooks  │  │   de Ejecución   │                  │ │
│  │  └─────────────────┘  └─────────────────┘                  │ │
│  │           │                   │                            │ │
│  │           ▼                   ▼                            │ │
│  │  ┌─────────────────┐  ┌─────────────────┐                  │ │
│  │  │   Gestión de    │  │   Coordinación  │                  │ │
│  │  │   Dependencias  │  │   de Etapas     │                  │ │
│  │  └─────────────────┘  └─────────────────┘                  │ │
│  │           │                   │                            │ │
│  │           ▼                   ▼                            │ │
│  │  ┌─────────────────────────────────────────────────────────┐ │ │
│  │  │              INTERFAZ DE COMUNICACIÓN                   │ │ │
│  │  │          (SkillEngineInterface)                         │ │ │
│  │  └─────────────────────────────────────────────────────────┘ │ │
│  └─────────────────────────────────────────────────────────────┘ │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      │ 2. Llamadas a API
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SKILL ENGINE                                 │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │              EJECUCIÓN Y RECURSOS                          │ │
│  │  ┌─────────────────┐  ┌─────────────────┐                  │ │
│  │  │   Validación    │  │   Gestión de    │                  │ │
│  │  │   de Skills     │  │   Agents        │                  │ │
│  │  └─────────────────┘  └─────────────────┘                  │ │
│  │           │                   │                            │ │
│  │           ▼                   ▼                            │ │
│  │  ┌─────────────────┐  ┌─────────────────┐                  │ │
│  │  │   Ejecución     │  │   Monitoreo     │                  │ │
│  │  │   de Skills     │  │   de Recursos   │                  │ │
│  │  └─────────────────┘  └─────────────────┘                  │ │
│  │           │                   │                            │ │
│  │           ▼                   ▼                            │ │
│  │  ┌─────────────────┐  ┌─────────────────┐                  │ │
│  │  │   Estimación    │  │   Control de    │                  │ │
│  │  │   de Costos     │  │   Errores       │                  │ │
│  │  └─────────────────┘  └─────────────────┘                  │ │
│  └─────────────────────────────────────────────────────────────┘ │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      │ 3. Resultados
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ALMACENAMIENTO                               │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Registros de  │  │   Métricas de   │  │   Resultados    │ │
│  │   Ejecución     │  │   Performance   │  │   de Skills     │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Responsabilidades Claramente Definidas

### Playbook Engine

**Propósito:** Orquestación de workflows y gestión de playbooks

**Responsabilidades Principales:**
- ✅ **Validación de Playbooks**: Verificar estructura y dependencias
- ✅ **Planificación de Ejecución**: Determinar orden y paralelismo
- ✅ **Gestión de Dependencias**: Resolver dependencias entre etapas
- ✅ **Coordinación de Etapas**: Orquestar la ejecución de múltiples etapas
- ✅ **Gestión de Estado**: Seguimiento del progreso de ejecuciones
- ✅ **Políticas de Costos**: Validar límites y requerir aprobaciones
- ✅ **Manejo de Errores**: Estrategias de reintentos y fallbacks

**NO HACE:**
- ❌ Validación de skills individuales
- ❌ Ejecución directa de skills
- ❌ Gestión de agents
- ❌ Estimación de costos de skills
- ❌ Monitoreo de recursos

### Skill Engine

**Propósito:** Ejecución de skills y gestión de recursos

**Responsabilidades Principales:**
- ✅ **Validación de Skills**: Verificar disponibilidad y requisitos
- ✅ **Ejecución de Skills**: Lógica de ejecución individual
- ✅ **Gestión de Agents**: Asignación y monitoreo de recursos
- ✅ **Estimación de Costos**: Cálculo de costos por skill
- ✅ **Control de Errores**: Manejo de fallos y reintentos
- ✅ **Monitoreo de Recursos**: Uso de CPU, memoria, tokens
- ✅ **Optimización**: Caching, paralelismo, balanceo

**NO HACE:**
- ❌ Orquestación de workflows
- ❌ Gestión de dependencias entre etapas
- ❌ Validación de playbooks completos
- ❌ Coordinación de múltiples etapas

## Interfaz de Comunicación

### SkillEngineInterface

```python
class SkillEngineInterface(ABC):
    @abstractmethod
    async def execute_skill(self, request: SkillRequest) -> SkillResult:
        """Ejecuta un skill individual"""

    @abstractmethod
    async def execute_stage(self, request: StageRequest) -> StageResult:
        """Ejecuta una etapa con múltiples skills"""

    @abstractmethod
    async def estimate_cost(self, skills: List[str]) -> CostEstimation:
        """Estima el costo de ejecutar skills"""

    @abstractmethod
    async def validate_skills(self, skills: List[str]) -> Dict[str, bool]:
        """Valida skills individuales"""

    @abstractmethod
    async def get_skill_info(self, skill_name: str) -> Dict[str, Any]:
        """Obtiene información de skills"""
```

### Beneficios de la Interfaz

1. **Desacoplamiento**: Cada motor puede evolucionar independientemente
2. **Testeabilidad**: Fácil de mockear para pruebas unitarias
3. **Extensibilidad**: Nuevos métodos pueden añadirse sin romper compatibilidad
4. **Claridad**: Define claramente qué espera cada motor del otro

## Flujos de Trabajo

### 1. Ejecución de Playbook

```
1. Cliente → Playbook Engine: "Ejecutar playbook X"
2. Playbook Engine: Validar estructura del playbook
3. Playbook Engine: Planificar ejecución de etapas
4. Playbook Engine → Skill Engine: "Validar skills de etapa 1"
5. Skill Engine: Validar skills individuales
6. Skill Engine → Playbook Engine: Resultado de validación
7. Playbook Engine: Coordinar ejecución de etapa 1
8. Playbook Engine → Skill Engine: "Ejecutar etapa 1"
9. Skill Engine: Ejecutar skills en paralelo/serie
10. Skill Engine → Playbook Engine: Resultados de la etapa
11. Playbook Engine: Continuar con siguientes etapas
12. Playbook Engine → Cliente: Resultado final
```

### 2. Estimación de Costos

```
1. Playbook Engine: Analizar skills requeridos
2. Playbook Engine → Skill Engine: "Estimar costo de skills [A, B, C]"
3. Skill Engine: Calcular costos individuales
4. Skill Engine: Sumar costos y aplicar descuentos
5. Skill Engine → Playbook Engine: "Costo estimado: $10.50"
6. Playbook Engine: Validar contra límites de presupuesto
7. Playbook Engine: Decidir si requiere aprobación
```

### 3. Gestión de Errores

```
1. Skill Engine: Detecta error en skill "X"
2. Skill Engine: Intenta reintentos configurados
3. Skill Engine: Si falla, reporta error al Playbook Engine
4. Playbook Engine: Aplica estrategia de fallback
5. Playbook Engine: Decide si continuar o abortar
6. Playbook Engine: Actualiza estado de ejecución
7. Playbook Engine: Reporta estado al cliente
```

## Ventajas de la Arquitectura

### 1. Mantenibilidad
- **Código más limpio**: Cada motor tiene un propósito claro
- **Fácil de entender**: Separación lógica de responsabilidades
- **Modificaciones aisladas**: Cambios en un motor no afectan al otro

### 2. Escalabilidad
- **Escalado independiente**: Cada motor puede escalar según su carga
- **Optimización específica**: Cada motor puede optimizarse para su propósito
- **Recursos especializados**: Agents pueden especializarse en tipos de skills

### 3. Testeabilidad
- **Pruebas unitarias claras**: Cada motor puede probarse independientemente
- **Mocks fáciles**: Interfaz bien definida facilita mocking
- **Integración controlada**: Pruebas de integración más simples

### 4. Flexibilidad
- **Implementaciones alternativas**: Distintas implementaciones del Skill Engine
- **Estrategias de ejecución**: Diferentes políticas en el Playbook Engine
- **Extensiones futuras**: Fácil añadir nuevas funcionalidades

## Mejoras Implementadas

### Antes (Problemas)
- ❌ Duplicación de validación de skills
- ❌ Playbook Engine ejecutaba skills directamente
- ❌ Skill Engine manejaba dependencias de playbooks
- ❌ Falta de interfaces claras
- ❌ Difícil de testear y mantener

### Después (Soluciones)
- ✅ **Separación clara**: Cada motor con responsabilidades definidas
- ✅ **Interfaz estandarizada**: Comunicación mediante interfaces bien definidas
- ✅ **Sin duplicación**: Cada funcionalidad en un solo lugar
- ✅ **Fácil de testear**: Componentes desacoplados y mockeables
- ✅ **Escalable**: Cada motor puede optimizarse independientemente

## Conclusión

Esta arquitectura de separación de responsabilidades proporciona una base sólida para el desarrollo futuro, asegurando que el sistema sea mantenible, escalable y fácil de entender. La clara delimitación de responsabilidades entre el Playbook Engine y el Skill Engine elimina la duplicación de código y mejora significativamente la calidad del software.
