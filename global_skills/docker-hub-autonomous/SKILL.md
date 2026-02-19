---
name: docker-hub-autonomous
description: Intelligent image discovery and CVE auditing. 2026 Edition.
---

# Docker Hub Autonomous (Compressed)

## Purpose
Manage image lifecycle with focus on security (distroless) and efficiency.

## Capabilities
- **Discovery**: Locate official Alpine/Slim/Distroless images.
- **Audit**: Proactive CVE scanning (Trivy/Snyk) before production.
- **Opt**: Dockerfile layer analysis to minimize attack surface and size.
- **Finance**: Report bandwidth/storage usage to **Financial-Controller**.

## Rules
1. **Safety First**: Never suggest an image without a vulnerability report.
2. **Immutability**: MANDATORILY reference images by **Digest (Hash)** in production.
