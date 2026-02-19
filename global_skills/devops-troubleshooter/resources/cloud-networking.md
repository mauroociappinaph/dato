# Cloud Networking & Connectivity

## 1. DNS: Siempre es el DNS
- **Herramientas**: `dig`, `nslookup`, `host`.
- **Problemas comunes**:
  - Tiempo de TTL largo retrasando cambios.
  - Recursión DNS fallida en el clúster.
  - Registros A/CNAME incorrectos.

## 2. Load Balancers & Proxies
- **AWS ALB/NLB**: Verificar reglas de Target Groups y Health Checks.
- **Nginx/HAProxy**: Revisar timeouts (`proxy_read_timeout`) y límites de tamaño de cuerpo (`client_max_body_size`).
- **502 Bad Gateway**: El balanceador no puede conectar con el backend (backend caído o puerto incorrecto).
- **504 Gateway Timeout**: El backend aceptó la conexión pero tardó demasiado en responder.

## 3. VPC & Security Groups
- **Tráfico bloqueado**: Verifica SGs de entrada/salida y Network ACLs.
- **Egress**: Problemas con NAT Gateways (saturación de puertos o falta de ancho de banda).
- **Peering**: Rutas faltantes en la tabla de ruteo para conectar dos VPCs.

## 4. Latencia de Red e eBPF
- **tcpdump / Wireshark**: Análisis profundo de paquetes.
- **eBPF (Cilium/Hubble)**: Visibilidad de red de alto rendimiento sin modificar la aplicación. Permite ver quién habla con quién y por dónde se pierden los paquetes en tiempo real.
