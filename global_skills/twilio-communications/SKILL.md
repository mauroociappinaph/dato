---
name: twilio-communications
description: SMS, Voice, WhatsApp, and 2FA via Twilio. 2026 Edition.
---

# Twilio Communications (Compressed)

## Purpose
Build secure and reliable multi-channel communication systems. Focus on compliance, rate limits, and automated verification.

## Capabilities
- **Messaging**: SMS (E.164 format), WhatsApp Business API, A2P 10DLC compliance.
- **Voice**: IVR systems (TwiML), Call recording, Redirects, Real-time status callbacks.
- **Identity**: Twilio Verify (2FA/OTP), Fraud prevention, Automatic code expiration.

## Patterns
- **SMS**: Validate E.164 -> Handle segments (160 chars) -> Implement status callbacks.
- **Verify**: Use Twilio managed OTP -> Never store codes locally -> Handle rate limits.
- **IVR**: Stateless webhooks -> Return TwiML XML -> Validate `X-Twilio-Signature`.

## Rules (Mandatory)
1. **Signature Validation**: ALWAYS verify webhook signatures to prevent spoofing.
2. **No Hardcoding**: Credentials must be injected via **secrets-vault-orchestrator**.
3. **Opt-out Tracking**: MANDATORILY track user opt-out status in the database.
4. **Intelligent Filtering (2026)**: Use LLM-based spam/relevance filtering before sending messages.
