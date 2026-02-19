import os
import json
from flask import Flask, request, jsonify
from supabase import create_client
from dotenv import load_dotenv

load_dotenv(dotenv_path="/Users/mauroociappina/.gemini/.env")

app = Flask(__name__)

SUPABASE_URL = "https://fmcgnrjkyecppxquijvj.supabase.co"
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# NOTA: En producción, este script debe correr detrás de un tunnel (Cloudflare/Ngrok)
# y validar la firma de Stripe (stripe.Webhook.construct_event)

@app.route('/webhook/stripe', methods=['POST'])
def stripe_webhook():
    print("🚀 Webhook endpoint called!")
    
    payload = request.get_data()
    sig_header = request.headers.get('Stripe-Signature')

    try:
        event = json.loads(payload)
    except Exception as e:
        print(f"❌ Error parsing JSON: {e}")
        return jsonify(error=str(e)), 400

    print(f"📨 Event received: {event['type']}")
    
    # Manejar el evento checkout.session.completed
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_email = session.get('customer_details', {}).get('email')
        amount = session.get('amount_total', 0) / 100  # Convertir a dólares

        print(f"🎯 Checkout completado para: {customer_email}")
        print(f"💰 Monto: ${amount} USD")

        # Actualizar estado en Supabase
        lead_id = session.get('metadata', {}).get('lead_id')
        print(f"🆔 Lead ID from metadata: {lead_id}")

        if lead_id:
            print(f"🔍 Intentando actualizar lead ID: {lead_id}")
            try:
                # Intentar actualizar por UUID
                result = supabase.table("leads").update({
                    "status": "PAID",
                    "last_contact_at": session.get('created'),
                    "intel_report": f"STRIPE_PAYMENT_{session.get('id')}_COMPLETED"
                }).eq("id", lead_id).execute()
                
                print(f"✅ Lead ID {lead_id} actualizado a PAID")
                
            except Exception as e:
                # Si falla (UUID inválido), buscar por email
                print(f"⚠️ Error actualizando por ID: {e}")
                print(f"🔍 Buscando lead por email: {customer_email}")
                
                try:
                    result = supabase.table("leads").update({
                        "status": "PAID",
                        "last_contact_at": session.get('created'),
                        "intel_report": f"STRIPE_PAYMENT_{session.get('id')}_COMPLETED"
                    }).eq("contact_email", customer_email).execute()
                    
                    print(f"✅ Lead con email {customer_email} actualizado a PAID")
                    
                except Exception as e2:
                    print(f"❌ Error actualizando por email: {e2}")
                    return jsonify(error=f"Lead no encontrado: {lead_id}/{customer_email}"), 404

            # Notificar al administrador
            try:
                from notify_mauro import notify_mauro
                notify_mauro(f"✅ **PAGO RECIBIDO**\n📧 Email: {customer_email}\n🆔 Lead ID: {lead_id}\n💰 Monto: ${amount} USD")
            except ImportError:
                print(f"📧 Notification: ✅ PAGO RECIBIDO - Email: {customer_email} - Lead ID: {lead_id} - Monto: ${amount}")
            except Exception as e:
                print(f"⚠️ Error notificación: {e}")

            return jsonify(success=True, message="Payment processed successfully"), 200
    
    # Para otros tipos de eventos
    print(f"📝 Event type {event['type']} received but not processed")
    return jsonify(success=True, message="Event received"), 200

if __name__ == "__main__":
    app.run(port=4242, debug=True)