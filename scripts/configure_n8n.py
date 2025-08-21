#!/usr/bin/env python3
"""
Script para configurar N8N automaticamente via API
"""

import requests
import json
import os
from typing import Dict, Any

class N8NConfigurator:
    def __init__(self, n8n_url: str, api_key: str = None):
        self.base_url = n8n_url.rstrip('/')
        self.api_key = api_key
        self.headers = {
            'Content-Type': 'application/json',
        }
        if api_key:
            self.headers['Authorization'] = f'Bearer {api_key}'
    
    def get_workflows(self) -> Dict[str, Any]:
        """Listar todos os workflows"""
        try:
            response = requests.get(f"{self.base_url}/api/v1/workflows", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Erro ao buscar workflows: {e}")
            return {}
    
    def get_webhook_urls(self) -> Dict[str, str]:
        """Extrair URLs dos webhooks dos workflows"""
        workflows = self.get_workflows()
        webhook_urls = {}
        
        if 'data' in workflows:
            for workflow in workflows['data']:
                if 'nodes' in workflow:
                    for node in workflow['nodes']:
                        if node.get('type') == 'n8n-nodes-base.webhook':
                            webhook_path = node.get('parameters', {}).get('path', '')
                            if webhook_path:
                                webhook_urls[workflow['name']] = f"{self.base_url}/webhook/{webhook_path}"
        
        return webhook_urls
    
    def create_credentials(self, name: str, type_name: str, data: Dict) -> bool:
        """Criar credenciais no N8N"""
        try:
            payload = {
                'name': name,
                'type': type_name,
                'data': data
            }
            response = requests.post(f"{self.base_url}/api/v1/credentials", 
                                   headers=self.headers, json=payload)
            response.raise_for_status()
            print(f"✅ Credencial '{name}' criada com sucesso")
            return True
        except Exception as e:
            print(f"❌ Erro ao criar credencial '{name}': {e}")
            return False
    
    def setup_supabase_credentials(self, supabase_url: str, service_key: str):
        """Configurar credenciais do Supabase"""
        return self.create_credentials(
            name="Supabase API",
            type_name="supabaseApi",
            data={
                "host": supabase_url,
                "serviceRole": service_key
            }
        )
    
    def setup_flask_credentials(self, flask_url: str):
        """Configurar credenciais do Flask API"""
        return self.create_credentials(
            name="Flask API Auth",
            type_name="httpHeaderAuth",
            data={
                "name": "Content-Type",
                "value": "application/json"
            }
        )

def main():
    print("🔧 Configurador Automático N8N")
    print("=" * 40)
    
    # Configurações (você pode alterar aqui)
    N8N_URL = input("Digite a URL do seu N8N (ex: https://workspace.app.n8n.cloud): ").strip()
    API_KEY = input("Digite sua API Key do N8N (opcional, Enter para pular): ").strip() or None
    
    # Configurações do projeto
    SUPABASE_URL = "https://wsoxukpeyzmpcngjugie.supabase.co"
    SUPABASE_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Indzb3h1a3BleXptcGNuZ2p1Z2llIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NTU0ODM0NSwiZXhwIjoyMDcxMTI0MzQ1fQ.BKoJd_3Z2djDtoWzPjfrrnI2jvrT19WEyw6QK-6CxpI"
    FLASK_URL = "http://localhost:5000/api"
    
    configurator = N8NConfigurator(N8N_URL, API_KEY)
    
    print("\n📋 Buscando workflows existentes...")
    webhook_urls = configurator.get_webhook_urls()
    
    if webhook_urls:
        print("\n🔗 URLs dos Webhooks encontradas:")
        for workflow_name, url in webhook_urls.items():
            print(f"  • {workflow_name}: {url}")
        
        print("\n📝 Adicione estas URLs ao seu .env:")
        for workflow_name, url in webhook_urls.items():
            if "intake" in workflow_name.lower():
                print(f"N8N_WEBHOOK_URL_INTAKE={url}")
            elif "qualified" in workflow_name.lower():
                print(f"N8N_WEBHOOK_URL_QUALIFIED={url}")
            elif "reengagement" in workflow_name.lower():
                print(f"N8N_WEBHOOK_URL_REENGAGEMENT={url}")
    else:
        print("❌ Nenhum webhook encontrado. Verifique se os workflows foram importados.")
    
    if API_KEY:
        print("\n🔐 Configurando credenciais...")
        configurator.setup_supabase_credentials(SUPABASE_URL, SUPABASE_SERVICE_KEY)
        configurator.setup_flask_credentials(FLASK_URL)
    else:
        print("\n⚠️  API Key não fornecida. Configure as credenciais manualmente no N8N.")
    
    print("\n✅ Configuração concluída!")

if __name__ == "__main__":
    main()
