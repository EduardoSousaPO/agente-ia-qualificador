#!/usr/bin/env python3
"""
Script de inicialização do Agente Qualificador
Para produção
"""

import os
import sys
import subprocess
import time
from dotenv import load_dotenv

def iniciar_backend():
    """Iniciar servidor Flask"""
    print("🚀 Iniciando Backend Flask...")
    
    # Carregar variáveis de ambiente
    load_dotenv()
    
    # Verificar se todas as variáveis estão definidas
    vars_obrigatorias = [
        'SUPABASE_URL', 'SUPABASE_SERVICE_ROLE_KEY',
        'OPENAI_API_KEY', 'TWILIO_ACCOUNT_SID', 'TWILIO_AUTH_TOKEN'
    ]
    
    for var in vars_obrigatorias:
        if not os.getenv(var):
            print(f"❌ Variável {var} não definida!")
            return False
    
    # Iniciar Flask
    try:
        from main import app
        print("✅ Aplicação Flask carregada")
        
        # Configurações de produção
        app.config['DEBUG'] = False
        app.config['TESTING'] = False
        
        print("🌐 Servidor rodando em http://localhost:5000")
        print("🤖 Agente Qualificador pronto!")
        print("📱 Webhook WhatsApp: http://localhost:5000/api/whatsapp/webhook")
        
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,
            threaded=True
        )
        
    except Exception as e:
        print(f"❌ Erro ao iniciar Flask: {str(e)}")
        return False

if __name__ == "__main__":
    iniciar_backend()
