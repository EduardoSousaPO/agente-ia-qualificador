#!/usr/bin/env python3
"""
SCRIPT DE INICIALIZAÇÃO PARA PRODUÇÃO
Agente Qualificador IA - Sistema Humanizado
"""

import os
import sys
import time
import subprocess
from dotenv import load_dotenv

def verificar_sistema():
    """Verificação rápida do sistema"""
    print("🔍 Verificação rápida do sistema...")
    
    # Carregar variáveis
    load_dotenv()
    
    # Verificar variáveis críticas
    vars_criticas = ['SUPABASE_URL', 'OPENAI_API_KEY', 'TWILIO_ACCOUNT_SID']
    for var in vars_criticas:
        if not os.getenv(var):
            print(f"❌ ERRO: {var} não configurada!")
            return False
    
    print("✅ Variáveis de ambiente OK")
    
    # Testar imports críticos
    try:
        from services.simple_supabase import simple_supabase
        from services.openai_service import get_openai_service
        from services.humanized_conversation_service import humanized_conversation_service
        print("✅ Serviços importados OK")
    except Exception as e:
        print(f"❌ ERRO ao importar serviços: {str(e)}")
        return False
    
    # Testar Supabase
    try:
        simple_supabase.client.table('leads').select('id').limit(1).execute()
        print("✅ Supabase conectado OK")
    except Exception as e:
        print(f"❌ ERRO Supabase: {str(e)}")
        return False
    
    return True

def iniciar_servidor():
    """Iniciar servidor Flask em modo produção"""
    print("\n🚀 INICIANDO AGENTE QUALIFICADOR IA")
    print("=" * 60)
    
    if not verificar_sistema():
        print("❌ Sistema não está pronto. Execute o diagnóstico primeiro.")
        return False
    
    try:
        from main import app
        
        # Configurações de produção
        app.config.update({
            'DEBUG': False,
            'TESTING': False,
            'ENV': 'production'
        })
        
        host = os.getenv('HOST', '0.0.0.0')
        port = int(os.getenv('PORT', 5000))
        
        print(f"🌐 Servidor: http://{host}:{port}")
        print(f"🤖 Agente: Ana (Consultora Humanizada)")
        print(f"📱 Webhook WhatsApp: http://{host}:{port}/api/whatsapp/webhook")
        print(f"💼 Base de conhecimento: InvestCorp integrada")
        print("=" * 60)
        print("🎯 SISTEMA PRONTO PARA PRODUÇÃO!")
        print("📱 Conecte seu WhatsApp e teste o agente humanizado")
        print("=" * 60)
        
        # Iniciar servidor
        app.run(
            host=host,
            port=port,
            debug=False,
            threaded=True,
            use_reloader=False
        )
        
    except KeyboardInterrupt:
        print("\n🛑 Servidor interrompido pelo usuário")
        return True
    except Exception as e:
        print(f"❌ ERRO ao iniciar servidor: {str(e)}")
        return False

def mostrar_status():
    """Mostrar status do sistema"""
    print("\n📊 STATUS DO SISTEMA")
    print("=" * 40)
    
    # Verificar se está rodando
    try:
        import requests
        response = requests.get('http://localhost:5000/api/health', timeout=3)
        if response.status_code == 200:
            print("✅ Backend: ONLINE")
            data = response.json()
            print(f"   Status: {data.get('status', 'OK')}")
            print(f"   Timestamp: {data.get('timestamp', 'N/A')}")
        else:
            print("❌ Backend: OFFLINE")
    except:
        print("❌ Backend: OFFLINE")
    
    print("\n🤖 AGENTE HUMANIZADO:")
    print("   Nome: Ana (Consultora Sênior)")
    print("   Empresa: InvestCorp")
    print("   Modo: Conversação Natural")
    print("   Qualificação: Invisível ao cliente")
    
    print("\n📱 PARA TESTAR:")
    print("   1. Configure Twilio Sandbox")
    print("   2. Conecte WhatsApp: +1 415 523 8886")
    print("   3. Envie: join to-southern")
    print("   4. Teste: 'Oi, tenho interesse em investimentos'")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'status':
        mostrar_status()
    else:
        iniciar_servidor()


