#!/usr/bin/env python3
"""
Stripe Integration - Main Controller (v1.0)
Unified entry point for managing payments and subscriptions.
"""

import os
import stripe
import sys
import json
from dotenv import load_dotenv
from pathlib import Path

# Config
load_dotenv(dotenv_path="/Users/mauroociappina/.gemini/.env")
stripe.api_key = os.getenv("STRIPE_API_KEY")

class StripeController:
    def __init__(self):
        self.api_key = stripe.api_key
        if not self.api_key or "sk_test" not in self.api_key:
            print("⚠️ WARN: STRIPE_API_KEY is missing or invalid (Placeholder detected).")

    def validate_connection(self):
        """Verifica si la API Key es válida"""
        try:
            stripe.Balance.retrieve()
            return True, "Conexión con Stripe exitosa."
        except Exception as e:
            return False, f"Error de conexión: {str(e)}"

    def create_payment_link(self, package, lead_id, email):
        """Genera un link de pago dinámico"""
        from create_stripe_checkout import create_checkout_session
        return create_checkout_session(package, lead_id, email)

    def list_recent_payments(self, limit=5):
        """Muestra los últimos pagos recibidos"""
        try:
            payments = stripe.PaymentIntent.list(limit=limit)
            return True, payments.data
        except Exception as e:
            return False, str(e)

if __name__ == "__main__":
    controller = StripeController()
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "validate":
            ok, msg = controller.validate_connection()
            print(json.dumps({"success": ok, "message": msg}))
            
        elif cmd == "recent":
            ok, data = controller.list_recent_payments()
            if ok:
                print(f"✅ Últimos {len(data)} intentos de pago encontrados.")
            else:
                print(f"❌ Error: {data}")
    else:
        print("Stripe Controller Active. Use 'validate' or 'recent'.")
