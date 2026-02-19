# Gestión de Incidentes y Resiliencia

## 1. Protocolo de Respuesta (On-call)
1. **Identificación**: Detección mediante alertas o reporte de usuario.
2. **Triaje**: ¿Cuál es el impacto? (Severidad 1, 2, 3).
3. **Mitigación**: El objetivo es restaurar el servicio (ej: rollback, escalado, purga de caché). **No es el momento de arreglar el bug**, es el momento de que el sistema funcione.
4. **Resolución**: Arreglo definitivo de la causa raíz.

## 2. Autopsias sin Culpa (Blameless Post-mortems)
El fallo es una oportunidad de aprendizaje, no de castigo.
- **¿Qué pasó?** (Cronología).
- **¿Por qué pasó?** (Los 5 porqués).
- **Acciones Preventivas**: Tareas concretas con responsables y fechas para evitar que vuelva a ocurrir.

## 3. Despliegues Seguros
- **Canary Deployments**: Desplegar solo a un 5% de usuarios y monitorear.
- **Blue-Green**: Cambiar el tráfico de una versión vieja a una nueva instantáneamente.
- **GitOps (ArgoCD/Flux)**: El estado deseado está en Git. Cualquier desviación se corrige automáticamente.

## 4. Ingeniería del Caos (Chaos Engineering)
- Romper cosas intencionalmente en entornos controlados para validar la resiliencia.
- **Chaos Mesh**, **Gremlin**.
- Probar: ¿Qué pasa si la DB cae? ¿Qué pasa si hay 500ms de latencia extra?

## 5. Gestión de Secretos
- Nunca en Git. Nunca en variables de entorno planas si es posible.
- **Vault**, **AWS Secrets Manager**, **SOPS** para encriptación de archivos en el repo.
