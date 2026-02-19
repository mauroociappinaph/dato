# Diagrama de Arquitectura - Sistema Enriquecido de Skill Registry

## Visión General del Sistema

```
┌─────────────────────────────────────────────────────────────────────┐
│                        AGENTES Y ORQUESTACIÓN                        │
├─────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐     │
│  │   AGENT_AI      │  │ AGENT_SECURITY  │  │ AGENT_BUSINESS  │     │
│  │                 │  │                 │  │                 │     │
│  │ - preferred_agent│  │ - preferred_agent│  │ - preferred_agent│     │
│  │ - cost_quota    │  │ - cost_quota    │  │ - cost_quota    │     │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘     │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    SISTEMA DE CONTROL DE COSTOS                      │
├─────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │              MCPCostController                                  │ │
│  │                                                                 │ │
│  │  ┌─────────────────────┐  ┌─────────────────────────────────┐   │ │
│  │  │ get_skill_cost_     │  │ check_skill_cost_quota()        │   │ │
│  │  │ estimate()          │  │ - Verifica límite diario        │   │ │
│  │  │ - Lee cost_estimate │  │ - Calcula costo acumulado       │   │ │
│  │  │   del registry      │  │ - Retorna True/False            │   │ │
│  │  └─────────────────────┘  └─────────────────────────────────┘   │ │
│  │                                                                 │ │
│  │  ┌─────────────────────┐  ┌─────────────────────────────────┐   │ │
│  │  │ check_quota_by_     │  │ record_usage()                  │   │ │
│  │  │ cost()              │  │ - Incrementa contador Redis     │   │ │
│  │  │ - Control presupuesto│  │ - Registra costos               │   │ │
│  │  │ - Límite $10/día    │  │ - Persistencia 7 días           │   │ │
│  │  └─────────────────────┘  └─────────────────────────────────┘   │ │
│  └─────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    REGISTRO DE SKILLS ENRIQUECIDO                    │
├─────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │                    skill_registry.json                          │ │
│  │                                                                 │ │
│  │  ┌─────────────────────────────────────────────────────────────┐ │ │
│  │  │ {                                                           │ │ │
│  │  │   "name": "ai-engineer",                                    │ │ │
│  │  │   "description": "...",                                     │ │ │
│  │  │   "cluster": "DATA_AI",                                     │ │ │
│  │  │   "inputs": {                                               │ │ │
│  │  │     "task_description": "string",                           │ │ │
│  │  │     "requirements": "object"                                │ │ │
│  │  │   },                                                        │ │ │
│  │  │   "outputs": {                                              │ │ │
│  │  │     "implementation": "string",                             │ │ │
│  │  │     "results": "object"                                     │ │ │
│  │  │   },                                                        │ │ │
│  │  │   "cost_estimate": {                                        │ │ │
│  │  │     "per_execution": 0.05,                                  │ │ │
│  │  │     "currency": "USD",                                      │ │ │
│  │  │     "complexity_factor": "medium"                           │ │ │
│  │  │   },                                                        │ │ │
│  │  │   "preferred_agent": "AGENT_Schmidhuber"                    │ │ │
│  │  │ }                                                           │ │ │
│  │  └─────────────────────────────────────────────────────────────┘ │ │
│  └─────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      INFRAESTRUCTURA COMÚN                          │
├─────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐     │
│  │     Redis       │  │   Supabase      │  │   Validación    │     │
│  │                 │  │                 │  │                 │     │
│  │ - Contadores    │  │ - Persistencia  │  │ - Esquema JSON  │     │
│  │ - Costos        │  │ - Consultas     │  │ - Tipos de datos│     │
│  │ - TTL 7 días    │  │ - Seguridad     │  │ - Rangos        │     │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘     │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        HERRAMIENTAS DE GESTIÓN                       │
├─────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐     │
│  │ enrich_skills   │  │ validate_skill_ │  │ example_skill_  │     │
│  │ .py             │  │ schema.py       │  │ cost_usage.py   │     │
│  │                 │  │                 │  │                 │     │
│  │ - Enriquecimiento│  │ - Validación    │  │ - Demostración  │     │
│  │   automático    │  │   automática    │  │   práctica      │     │
│  │ - Asignación    │  │ - Errores       │  │ - Integración   │     │
│  │   inteligente   │  │ - Reportes      │  │   real          │     │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘     │
└─────────────────────────────────────────────────────────────────────┘
```

## Flujos de Integración

### 1. Flujo de Control de Costos

```
Agente → MCPCostController → skill_registry.json → Redis
   │           │                    │               │
   │           │                    │               │
   │    check_skill_cost_quota()    │               │
   │           │                    │               │
   │    get_skill_cost_estimate()   │               │
   │           │                    │               │
   │           ▼                    ▼               ▼
   │    Verifica límite        Lee cost_estimate  Incrementa
   │    diario ($10)           del skill         contador
   │           │                    │               │
   │           ▼                    ▼               ▼
   └─────── Decisiones de cuota ←─────── Registro de costos
```

### 2. Flujo de Validación de Esquema

```
skill_registry.json → validate_skill_schema.py → Reporte
         │                    │                    │
         │                    │                    │
         │                    ▼                    │
         │             Validación de campos        │
         │                    │                    │
         │                    ▼                    │
         │             Tipos y rangos              │
         │                    │                    │
         │                    ▼                    │
         └───────────── Errores/Éxitos ←───────────┘
```

### 3. Flujo de Enriquecimiento Automático

```
skill_registry.json → enrich_skills.py → skill_registry.json
         │                    │                    │
         │                    │                    │
         │                    ▼                    │
         │             Análisis de cluster         │
         │                    │                    │
         │                    ▼                    │
         │             Asignación de costos        │
         │                    │                    │
         │                    ▼                    │
         └───────────── Skills enriquecidos ←──────┘
```

## Componentes Clave

### 1. **MCPCostController** (Cost Control System)
- **Funciones principales**:
  - `get_skill_cost_estimate()`: Obtiene costo desde el registry
  - `check_skill_cost_quota()`: Verifica cuota basada en costo
  - `check_quota_by_cost()`: Control de presupuesto diario
  - `record_usage()`: Registro de costos en Redis

### 2. **skill_registry.json** (Registro Enriquecido)
- **Campos nuevos**:
  - `inputs`: Esquema de entrada para interfaces
  - `outputs`: Esquema de salida para contratos
  - `cost_estimate`: Costo de ejecución y complejidad
  - `preferred_agent`: Agente óptimo para ejecución

### 3. **Sistema de Validación**
- **validate_skill_schema.py**: Validador automático
- **Tipos soportados**: String, Number, Object, Array
- **Validaciones**: Tipos, rangos, valores permitidos

### 4. **Infraestructura Común**
- **Redis**: Contadores de uso y costos
- **Supabase**: Persistencia y consultas
- **Validación**: Esquema JSON robusto

## Beneficios de la Arquitectura

### 1. **Gobernanza**
- Control total sobre costos y asignación de agentes
- Validación automática de interfaces
- Registro de auditoría completo

### 2. **Optimización**
- Selección inteligente basada en especialización
- Control de presupuesto en tiempo real
- Fallback automático por límites de costo

### 3. **Escalabilidad**
- Sistema preparado para crecimiento futuro
- Arquitectura modular y desacoplada
- Integración con infraestructura existente

### 4. **Monitoreo**
- Métricas de costo y performance por skill
- Estadísticas de uso en tiempo real
- Alertas por límites de presupuesto

## Integraciones Existentes

### Con Sistemas Existentes
- **Cost Control**: skill_registry → cost_estimate → mcp_cost_controller
- **Agent Orchestration**: skill_registry → preferred_agent → load_balancer
- **Validation**: skill_registry → inputs/outputs → schema_validator

### Con Infraestructura
- **Redis**: Persistencia de contadores y costos
- **Supabase**: Almacenamiento y consultas estructuradas
- **Redis Infra**: Operaciones de cache y contadores

## Estado Actual

**✅ IMPLEMENTACIÓN COMPLETA**

Todos los componentes están implementados, integrados y funcionando:
- 93 skills enriquecidos exitosamente
- 0 errores de validación
- Sistema de control de costos operativo
- Validación automática activa
- Documentación completa
