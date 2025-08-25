#!/usr/bin/env python3
"""
🔧 CONFIGURAÇÃO AUTOMÁTICA N8N - SISTEMA COMPLETO
Configura todos os workflows e integrações necessárias
"""

import os
import json
import requests
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv(dotenv_path='backend/.env')

def print_header(title):
    print(f"\n{'='*60}")
    print(f"🔧 {title}")
    print(f"{'='*60}")

def print_step(emoji, step, details=""):
    print(f"\n{emoji} {step}")
    if details:
        print(f"   {details}")

def check_credentials():
    """Verificar se todas as credenciais estão configuradas"""
    print_step("🔍", "Verificando credenciais necessárias...")
    
    required_vars = {
        'SUPABASE_URL': os.getenv('SUPABASE_URL'),
        'SUPABASE_SERVICE_ROLE_KEY': os.getenv('SUPABASE_SERVICE_ROLE_KEY'),
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
        'N8N_WEBHOOK_URL_INTAKE': os.getenv('N8N_WEBHOOK_URL_INTAKE')
    }
    
    missing = []
    for var, value in required_vars.items():
        if not value or 'your-' in value:
            missing.append(var)
        else:
            print(f"   ✅ {var}: {'*' * 20}{value[-10:]}")
    
    if missing:
        print(f"   ❌ Faltando: {', '.join(missing)}")
        return False
    
    print("   ✅ Todas as credenciais estão configuradas!")
    return True

def get_n8n_info():
    """Obter informações do N8N"""
    print_step("🔗", "Configuração N8N...")
    
    n8n_url = os.getenv('N8N_WEBHOOK_URL_INTAKE', '')
    if not n8n_url:
        print("   ❌ N8N_WEBHOOK_URL_INTAKE não configurado")
        return None
    
    # Extrair base URL
    base_url = n8n_url.replace('/webhook/intake-lead', '')
    workspace = base_url.split('//')[1].split('.')[0]
    
    print(f"   🌐 Workspace: {workspace}")
    print(f"   📥 Intake URL: {n8n_url}")
    print(f"   📱 WhatsApp URL: {base_url}/webhook/whatsapp-webhook")
    
    return {
        'base_url': base_url,
        'workspace': workspace,
        'intake_url': n8n_url,
        'whatsapp_url': f"{base_url}/webhook/whatsapp-webhook"
    }

def test_n8n_connection(n8n_info):
    """Testar conexão com N8N"""
    print_step("🧪", "Testando conexão N8N...")
    
    test_data = {
        "name": "Teste Automático",
        "phone": "+5511999888777",
        "email": "teste@automatico.com",
        "origem": "setup_script"
    }
    
    try:
        response = requests.post(n8n_info['intake_url'], json=test_data, timeout=10)
        if response.status_code == 200:
            print("   ✅ N8N Intake webhook respondeu com sucesso!")
            return True
        else:
            print(f"   ❌ N8N retornou status {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Erro ao conectar N8N: {e}")
        return False

def generate_twilio_config(n8n_info):
    """Gerar configuração para Twilio"""
    print_step("📱", "Configuração Twilio...")
    
    webhook_url = f"{n8n_info['base_url']}/webhook/whatsapp-webhook"
    
    print("   📋 Configure no Twilio Console:")
    print("   1. Acesse: Console → Phone Numbers → WhatsApp Sandbox")
    print(f"   2. Webhook URL: {webhook_url}")
    print("   3. HTTP Method: POST")
    print("   4. Events: Incoming Messages")
    
    return webhook_url

def generate_env_updates():
    """Gerar atualizações para .env"""
    print_step("⚙️", "Atualizações necessárias no .env...")
    
    n8n_base = os.getenv('N8N_WEBHOOK_URL_INTAKE', '').replace('/webhook/intake-lead', '')
    
    env_updates = f"""
# N8N Webhooks Completos
N8N_WEBHOOK_URL_INTAKE={os.getenv('N8N_WEBHOOK_URL_INTAKE')}
N8N_WEBHOOK_URL_WHATSAPP={n8n_base}/webhook/whatsapp-webhook
N8N_WEBHOOK_URL_QUALIFIED={n8n_base}/webhook/qualified-lead
N8N_WEBHOOK_URL_REENGAGEMENT={n8n_base}/webhook/reengagement

# Twilio para N8N (adicionar ao Twilio Console)
TWILIO_WEBHOOK_URL={n8n_base}/webhook/whatsapp-webhook
"""
    
    print(f"   📝 Adicione ao backend/.env:")
    print(env_updates)
    
    return env_updates

def show_workflow_files():
    """Mostrar arquivos de workflow disponíveis"""
    print_step("📂", "Workflows N8N disponíveis para importação:")
    
    workflows = [
        {
            'file': 'n8n/intake_complete_workflow.json',
            'name': '📥 Lead Intake Completo',
            'description': 'Recebe leads → Cria no Supabase → Envia primeira mensagem WhatsApp'
        },
        {
            'file': 'n8n/complete_whatsapp_workflow.json', 
            'name': '🤖 WhatsApp AI Agent',
            'description': 'Processa mensagens → IA responde → Qualifica → Notifica closers'
        },
        {
            'file': 'n8n/intake_workflow_simple.json',
            'name': '📥 Intake Simples (atual)',
            'description': 'Apenas webhook → HTTP request (básico)'
        }
    ]
    
    for i, workflow in enumerate(workflows, 1):
        print(f"   {i}. {workflow['name']}")
        print(f"      Arquivo: {workflow['file']}")
        print(f"      Função: {workflow['description']}")
        print()

def show_credentials_setup():
    """Mostrar configuração de credenciais N8N"""
    print_step("🔑", "Credenciais necessárias no N8N:")
    
    credentials = [
        {
            'name': 'OpenAI API',
            'type': 'OpenAI',
            'fields': {
                'API Key': os.getenv('OPENAI_API_KEY', 'sk-proj-sua-chave-aqui')
            }
        },
        {
            'name': 'Twilio API',
            'type': 'HTTP Basic Auth',
            'fields': {
                'Username': os.getenv('TWILIO_ACCOUNT_SID', 'ACsua-account-sid'),
                'Password': os.getenv('TWILIO_AUTH_TOKEN', 'seu-auth-token')
            }
        }
    ]
    
    for cred in credentials:
        print(f"   🔐 {cred['name']} ({cred['type']}):")
        for field, value in cred['fields'].items():
            masked_value = f"{'*' * 15}{value[-8:]}" if len(value) > 20 else value
            print(f"      {field}: {masked_value}")
        print()

def show_integration_endpoints():
    """Mostrar endpoints de integração"""
    print_step("🔗", "Endpoints de integração configurados:")
    
    flask_url = os.getenv('NEXT_PUBLIC_API_URL', 'http://localhost:5000/api')
    n8n_base = os.getenv('N8N_WEBHOOK_URL_INTAKE', '').replace('/webhook/intake-lead', '')
    
    endpoints = [
        {
            'name': 'Flask → N8N (Lead Intake)',
            'url': f"{flask_url}/test/n8n",
            'method': 'POST',
            'description': 'Testar envio de leads para N8N'
        },
        {
            'name': 'Twilio → N8N (WhatsApp)',
            'url': f"{n8n_base}/webhook/whatsapp-webhook",
            'method': 'POST', 
            'description': 'Webhook para mensagens WhatsApp'
        },
        {
            'name': 'N8N → Flask (Backup)',
            'url': f"{flask_url}/webhooks/twilio-n8n",
            'method': 'POST',
            'description': 'Fallback se N8N não processar'
        },
        {
            'name': 'Frontend → N8N (Direto)',
            'url': f"{n8n_base}/webhook/intake-lead-complete",
            'method': 'POST',
            'description': 'Formulários web → N8N diretamente'
        }
    ]
    
    for endpoint in endpoints:
        print(f"   🌐 {endpoint['name']}")
        print(f"      URL: {endpoint['url']}")
        print(f"      Method: {endpoint['method']}")
        print(f"      Uso: {endpoint['description']}")
        print()

def main():
    """Executar configuração completa"""
    print_header("CONFIGURAÇÃO AUTOMÁTICA N8N - SISTEMA COMPLETO")
    print("🎯 Este script vai configurar todas as integrações N8N necessárias")
    
    # 1. Verificar credenciais
    if not check_credentials():
        print("\n❌ Configure as credenciais faltantes no backend/.env")
        return
    
    # 2. Obter informações N8N
    n8n_info = get_n8n_info()
    if not n8n_info:
        print("\n❌ Configure N8N_WEBHOOK_URL_INTAKE no backend/.env")
        return
    
    # 3. Testar conexão
    test_n8n_connection(n8n_info)
    
    # 4. Mostrar workflows
    show_workflow_files()
    
    # 5. Mostrar credenciais
    show_credentials_setup()
    
    # 6. Configuração Twilio
    generate_twilio_config(n8n_info)
    
    # 7. Atualizações .env
    generate_env_updates()
    
    # 8. Endpoints de integração
    show_integration_endpoints()
    
    print_header("PRÓXIMOS PASSOS")
    print("1. 📥 Importe os workflows JSON no N8N")
    print("2. 🔑 Configure as credenciais no N8N")
    print("3. 📱 Configure o webhook no Twilio Console")
    print("4. ⚙️ Adicione as variáveis ao backend/.env")
    print("5. 🧪 Teste os endpoints de integração")
    
    print(f"\n🎉 CONFIGURAÇÃO COMPLETA!")
    print(f"📋 Documentação: n8n/CONFIGURACAO_COMPLETA_N8N.md")
    print(f"🔗 N8N Workspace: {n8n_info['workspace']}.app.n8n.cloud")

if __name__ == "__main__":
    main()


