#!/usr/bin/env python3
"""
Configuração simplificada do N8N usando apenas webhooks
"""

import os

def configure_n8n_simple():
    print("🔧 Configuração Simplificada N8N")
    print("=" * 40)
    
    print("📋 Vamos configurar apenas os webhooks (sem API Key)")
    print("💡 Isso é suficiente para o funcionamento básico!")
    
    # Obter URLs dos webhooks
    print("\n🔗 No seu N8N, clique no nó 'Webhook' e copie a URL:")
    
    base_url = "https://eduardopires25.app.n8n.cloud"
    
    webhook_intake = input(f"URL do webhook Intake (ex: {base_url}/webhook/intake-lead): ").strip()
    if not webhook_intake:
        webhook_intake = f"{base_url}/webhook/intake-lead"
    
    # Criar arquivo .env atualizado
    env_content = f"""# Flask Configuration
FLASK_ENV=development
FLASK_SECRET_KEY=your-secret-key-change-in-production
JWT_SECRET_KEY=your-jwt-secret-key
HOST=0.0.0.0
PORT=5000

# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-supabase-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-supabase-service-role-key

# Database URLs
DATABASE_URL=postgresql://postgres.wsoxukpeyzmpcngjugie:[YOUR-PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres?pgbouncer=true
DIRECT_URL=postgresql://postgres.wsoxukpeyzmpcngjugie:[YOUR-PASSWORD]@aws-0-us-east-1.pooler.supabase.com:5432/postgres

# OpenAI Configuration
OPENAI_API_KEY=sk-proj-your-openai-api-key-here
OPENAI_MODEL=gpt-4o-mini
OPENAI_MAX_TOKENS=1000

# Twilio Configuration
TWILIO_ACCOUNT_SID=ACyour-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_WHATSAPP_NUMBER=+14155238886

# n8n Configuration
N8N_WEBHOOK_URL_INTAKE={webhook_intake}
N8N_WEBHOOK_URL_QUALIFIED={base_url}/webhook/qualified-lead
N8N_WEBHOOK_URL_REENGAGEMENT={base_url}/webhook/reengagement

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,https://your-frontend-domain.com

# Logging
LOG_LEVEL=INFO

# Rate Limiting (optional)
REDIS_URL=redis://localhost:6379
"""
    
    # Salvar no backend
    with open('backend/.env', 'w') as f:
        f.write(env_content)
    
    print(f"\n✅ Arquivo backend/.env criado!")
    print(f"🔗 Webhook configurado: {webhook_intake}")
    
    # Mostrar próximos passos
    print("\n📋 Próximos passos:")
    print("1. ✅ N8N configurado (webhooks)")
    print("2. ⏳ Configurar Twilio (próximo)")
    print("3. ⏳ Testar integração completa")
    
    return webhook_intake

if __name__ == "__main__":
    configure_n8n_simple()
