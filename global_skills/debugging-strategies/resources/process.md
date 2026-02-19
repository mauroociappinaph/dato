# Proceso de Depuración Sistemática

## Fase 1: Reproducir
Asegúrate de tener un caso de prueba mínimo que falle consistentemente.
- ¿Se reproduce siempre o aleatoriamente?
- ¿Qué condiciones específicas (datos, usuario, navegador) lo disparan?
- Simplifica hasta el código mínimo necesario.

## Fase 2: Recopilar Información
- **Errores**: Stack traces completos, códigos de error, logs de consola.
- **Entorno**: Versiones de OS, lenguaje, dependencias y variables de entorno.
- **Cambios Recientes**: Revisa el historial de Git y los despliegues recientes.
- **Alcance**: ¿Afecta a todos o a un grupo específico? ¿Solo producción o también local?

## Fase 3: Formular Hipótesis
Hazte las preguntas clave:
- ¿Qué cambió recientemente?
- ¿Qué es diferente entre el entorno que funciona y el que no?
- ¿En qué capa es más probable que falle? (Validación, Lógica, Datos, Red).

## Fase 4: Prueba y Verificación
- **Búsqueda Binaria**: Comenta la mitad del código para ver si el error persiste. Divide y vencerás.
- **Logging Estratégico**: Traza el flujo de las variables en puntos críticos.
- **Aislamiento**: Mockea dependencias para probar componentes por separado.
- **Comparación**: Compara diffs de configuración y datos entre entornos.
