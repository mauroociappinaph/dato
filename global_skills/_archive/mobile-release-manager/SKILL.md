---
name: mobile-release-manager
description: Mobile CI/CD automation and app store compliance. 2026 Edition.
---

# Mobile Release Manager (Compressed)

## Purpose
Automate the mobile app release lifecycle (signing, building, uploading).

## Capabilities
- **Fastlane**: Manage Lanes (`beta`/`prod`), signing (Match), and metadata.
- **Ops**: App Store Connect / Play Console API integration.
- **Finance**: Consult **Financial-Controller** to optimize expensive macOS runner minutes.
- **OTA**: CodePush/Expo updates for JS-only fixes.

## Release Rules
1. **Phased Rollout**: 1% -> 10% -> 100%.
2. **Secrets**: Encrypt Keystores and p12 certs in CI variables.
3. **SemVer**: Strictly follow semantic versioning.