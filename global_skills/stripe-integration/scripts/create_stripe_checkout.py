#!/usr/bin/env python3
"""
Stripe Checkout Session Creator - Fase 1 Activation
Crea sesiones de pago para los paquetes de landing pages
"""

import os
import stripe
from dotenv import load_dotenv
import sys

# Path setup for Master Control
sys.path.append("/Users/mauroociappina/.gemini/master_control")
from orchestrator import MasterOrchestrator

load_dotenv(dotenv_path="/Users/mauroociappina/.gemini/.env")

# Configurar Stripe API
stripe.api_key = os.getenv("STRIPE_API_KEY")

# Precios configurados (en centavos)
PACKAGES = {
    "starter": {
        "name": "Starter Landing Page",
        "price": 49900,  # $499 USD
        "description": "Landing page responsive con copy optimizado por IA"
    },
    "pro": {
        "name": "Pro Landing Page", 
        "price": 99900,  # $999 USD
        "description": "Todo Starter + blog integrado, SEO optimizado, analytics"
    },
    "enterprise": {
        "name": "Enterprise Landing",
        "price": 199900,  # $1,999 USD
        "description": "Todo Pro + dominio custom, CRM integration, soporte prioritario"
    }
}

def create_checkout_session(package_type, lead_id, customer_email=None):
    """Crea una sesión de checkout Stripe"""
    boss = MasterOrchestrator()
    
    if package_type not in PACKAGES:
        raise ValueError(f"Package '{package_type}' no válido. Opciones: {list(PACKAGES.keys())}")
    
    package = PACKAGES[package_type]
    
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': package['name'],
                        'description': package['description'],
                        'metadata': {
                            'package_type': package_type,
                            'lead_id': str(lead_id)
                        }
                    },
                    'unit_amount': package['price'],
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=f'https://dude-agency.com/success?session_id={{CHECKOUT_SESSION_ID}}',
            cancel_url=f'https://dude-agency.com/cancel?lead_id={lead_id}',
            customer_email=customer_email,
            metadata={
                'lead_id': str(lead_id),
                'package_type': package_type,
                'source': 'dude_sales_pipeline'
            }
        )
        
        boss.register_activity("AGENT_BILLING", f"Created checkout for {customer_email}", "SUCCESS", revenue=package['price']/100)
        
        return {
            'success': True,
            'session_url': session.url,
            'session_id': session.id,
            'package': package_type,
            'price': package['price'] / 100,  # Convertir a dólares
            'lead_id': lead_id
        }
        
    except stripe.error.StripeError as e:
        boss.register_activity("AGENT_BILLING", f"Failed checkout for {customer_email}", "ERROR")
        return {
            'success': False,
            'error': str(e)
        }

def create_test_sessions():
    """Crea sesiones de prueba para todos los paquetes"""
    print("🚀 Creando sesiones de checkout de prueba...")
    
    test_lead_id = "test_lead_001"
    test_email = "test@thedude.agency"
    
    for package_type in PACKAGES.keys():
        result = create_checkout_session(package_type, test_lead_id, test_email)
        
        if result['success']:
            print(f"✅ {package_type.upper()}: ${result['price']}")
            print(f"   🔗 {result['session_url']}")
            print(f"   🆔 Session: {result['session_id']}")
            print()
        else:
            print(f"❌ Error en {package_type}: {result['error']}")
    
    print("🎯 Para probar: visita los links arriba y completa un pago de prueba")
    print("💡 El webhook en puerto 4242 recibirá el evento automáticamente")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        create_test_sessions()
    else:
        print("📋 Uso:")
        print("  python create_stripe_checkout.py test     # Crear sesiones de prueba")
        print("  python create_stripe_checkout.py <package> <lead_id> <email>  # Crear sesión específica")
        print()
        print("📦 Paquetes disponibles:", list(PACKAGES.keys()))