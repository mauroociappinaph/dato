# Kubernetes & Container Debugging

## 1. El Cinturón de Herramientas `kubectl`
- **Inspección Básica**:
  - `kubectl describe pod <pod>`: Errores de scheduling, montado de volúmenes o límites de recursos.
  - `kubectl logs -f <pod> -c <container>`: Logs en tiempo real.
  - `kubectl get events --sort-by='.lastTimestamp'`: Historial de eventos del clúster.

- **Depuración Avanzada**:
  - `kubectl exec -it <pod> -- /bin/bash`: Entrar al contenedor (si tiene shell).
  - `kubectl debug <pod> -it --image=busybox`: Crea un contenedor de depuración junto al pod con problemas (ideal para imágenes distroless/minimalistas).
  - `kubectl port-forward <pod> 8080:80`: Probar servicios internamente desde tu local.

## 2. Ciclos de Vida y Estados de Error
- **CrashLoopBackOff**: Casi siempre es un error de configuración, falta de archivos, variables de entorno o fallo de conexión a DB al iniciar.
- **ImagePullBackOff**: Credenciales del registro de imágenes (ImagePullSecrets) incorrectas o nombre de imagen inexistente.
- **OOMKilled**: El contenedor excedió el límite de memoria asignado (`limits.memory`).
- **Pending**: No hay recursos suficientes en los Nodos o problemas de selectores/afinidades.

## 3. Redes en K8s
- **CNI (Container Network Interface)**: Resolución de problemas de conectividad entre pods (Calico, Cilium, Flannel).
- **Services & Ingress**: Verificar que los selectores de los servicios coincidan con las etiquetas de los pods.
- **Service Mesh (Istio/Linkerd)**: Depuración de mTLS, inyección de sidecars y políticas de tráfico.

## 4. Almacenamiento (PVC/PV)
- Verificar el estado de los `PersistentVolumeClaims`.
- Errores de "Multi-Attach": Un PV siendo reclamado por dos pods en diferentes nodos (si el modo es `ReadWriteOnce`).
