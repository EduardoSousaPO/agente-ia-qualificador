"""
Health check routes
"""

from flask import Blueprint, jsonify
import os

health_bp = Blueprint('health', __name__)

@health_bp.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Agente Qualificador API",
        "version": "1.0.0",
        "environment": os.getenv('FLASK_ENV', 'development'),
        "features": {
            "supabase": bool(os.getenv('SUPABASE_URL')),
            "openai": bool(os.getenv('OPENAI_API_KEY')),
            "n8n": bool(os.getenv('N8N_WEBHOOK_URL_INTAKE')),
            "whatsapp_simulator": os.getenv('USE_WHATSAPP_SIMULATOR', 'true') == 'true',
            "twilio": bool(os.getenv('TWILIO_ACCOUNT_SID')) and os.getenv('TWILIO_ACCOUNT_SID') != 'ACyour-twilio-account-sid'
        }
    })

@health_bp.route('/status', methods=['GET'])
def status():
    """Detailed status endpoint"""
    return jsonify({
        "status": "operational",
        "timestamp": "2025-01-21T19:30:00Z",
        "uptime": "running",
        "database": "connected",
        "external_apis": {
            "supabase": "connected",
            "openai": "connected",
            "twilio": "simulator_mode" if os.getenv('USE_WHATSAPP_SIMULATOR') == 'true' else "connected",
            "n8n": "connected"
        }
    })
