#!/usr/bin/env python3
"""
🧪 TESTE COMPLETO - AGENTE QUALIFICADOR IA
Validação final antes de usar em produção
"""

import requests
import json
import time
from datetime import datetime

# Configurações
BACKEND_URL = "http://localhost:5000"
FRONTEND_URL = "http://localhost:3000"
HEADERS = {"Content-Type": "application/json"}

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(title):
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}  {title}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.END}")

def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.END}")

def print_info(message):
    print(f"{Colors.YELLOW}ℹ️  {message}{Colors.END}")

def test_backend_health():
    """Teste 1: Backend funcionando"""
    print_header("TESTE 1: BACKEND HEALTH CHECK")
    
    try:
        response = requests.get(f"{BACKEND_URL}/api/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print_success("Backend online")
            print_info(f"OpenAI: {'✅' if data['features']['openai'] else '❌'}")
            print_info(f"Supabase: {'✅' if data['features']['supabase'] else '❌'}")
            print_info(f"WhatsApp: {'✅ Simulador' if data['features']['whatsapp_simulator'] else '✅ Real'}")
            return True
        else:
            print_error(f"Backend offline: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Erro na conexão: {e}")
        return False

def test_frontend_access():
    """Teste 2: Frontend acessível"""
    print_header("TESTE 2: FRONTEND ACESSÍVEL")
    
    try:
        response = requests.get(FRONTEND_URL, timeout=10)
        if response.status_code == 200:
            print_success("Frontend acessível")
            print_info("Interface web funcionando")
            return True
        else:
            print_error(f"Frontend não acessível: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Frontend offline: {e}")
        print_info("Execute: cd frontend && npm run dev")
        return False

def test_login_system():
    """Teste 3: Sistema de login"""
    print_header("TESTE 3: SISTEMA DE LOGIN")
    
    login_data = {
        "email": "admin@demo.com",
        "password": "demo123"
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/api/auth/login", headers=HEADERS, json=login_data)
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print_success("Login funcionando")
                print_info(f"Usuário: {data['user']['name']}")
                print_info(f"Role: {data['user']['role']}")
                return data['access_token']
            else:
                print_error("Login falhou")
                return None
        else:
            print_error(f"Login endpoint erro: {response.status_code}")
            return None
    except Exception as e:
        print_error(f"Erro no login: {e}")
        return None

def test_lead_creation(token):
    """Teste 4: Criação de lead"""
    print_header("TESTE 4: CRIAÇÃO DE LEAD")
    
    if not token:
        print_error("Token não disponível")
        return None
    
    lead_data = {
        "name": f"Lead Teste {datetime.now().strftime('%H%M%S')}",
        "phone": f"+5511999{datetime.now().strftime('%M%S')}",
        "email": "teste@exemplo.com",
        "origem": "teste_final"
    }
    
    headers = {**HEADERS, "Authorization": f"Bearer {token}"}
    
    try:
        response = requests.post(f"{BACKEND_URL}/api/leads", headers=headers, json=lead_data)
        if response.status_code in [200, 201]:
            data = response.json()
            if 'lead' in data:
                lead = data['lead']
                print_success("Lead criado")
                print_info(f"ID: {lead['id']}")
                print_info(f"Nome: {lead['name']}")
                return lead
            else:
                print_error("Resposta inválida")
                return None
        else:
            print_error(f"Falha na criação: {response.status_code}")
            return None
    except Exception as e:
        print_error(f"Erro: {e}")
        return None

def test_qualification_start(lead, token):
    """Teste 5: Iniciar qualificação"""
    print_header("TESTE 5: QUALIFICAÇÃO IA")
    
    if not lead or not token:
        print_error("Lead ou token não disponível")
        return False
    
    headers = {**HEADERS, "Authorization": f"Bearer {token}"}
    
    try:
        response = requests.post(f"{BACKEND_URL}/api/leads/{lead['id']}/start-qualification", headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print_success("Qualificação iniciada")
                print_info(f"Session ID: {data['session_id']}")
                print_info("Primeira mensagem enviada")
                return True
            else:
                print_error(f"Erro: {data.get('error')}")
                return False
        else:
            print_error(f"Falha: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Erro: {e}")
        return False

def generate_final_report(results):
    """Relatório final"""
    print_header("RELATÓRIO FINAL")
    
    total = len(results)
    passed = sum(1 for r in results.values() if r)
    success_rate = (passed / total) * 100
    
    print(f"{Colors.BOLD}📊 RESUMO:{Colors.END}")
    print(f"   Total de testes: {total}")
    print(f"   Testes aprovados: {passed}")
    print(f"   Taxa de sucesso: {success_rate:.1f}%")
    
    print(f"\n{Colors.BOLD}📋 DETALHES:{Colors.END}")
    for test_name, result in results.items():
        status = f"{Colors.GREEN}✅ PASSOU{Colors.END}" if result else f"{Colors.RED}❌ FALHOU{Colors.END}"
        print(f"   {test_name}: {status}")
    
    print(f"\n{Colors.BOLD}🎯 RESULTADO:{Colors.END}")
    if success_rate >= 90:
        print(f"{Colors.GREEN}{Colors.BOLD}🎉 SISTEMA PRONTO PARA USO!{Colors.END}")
        print(f"{Colors.GREEN}✅ Todos os componentes funcionando{Colors.END}")
        print(f"{Colors.GREEN}✅ Login: admin@demo.com / demo123{Colors.END}")
        print(f"{Colors.GREEN}✅ URLs: Frontend (3000) + Backend (5000){Colors.END}")
    elif success_rate >= 70:
        print(f"{Colors.YELLOW}{Colors.BOLD}⚠️  SISTEMA QUASE PRONTO{Colors.END}")
        print(f"{Colors.YELLOW}Alguns ajustes necessários{Colors.END}")
    else:
        print(f"{Colors.RED}{Colors.BOLD}❌ SISTEMA PRECISA DE CORREÇÕES{Colors.END}")
    
    print(f"\n{Colors.BOLD}📝 PRÓXIMOS PASSOS:{Colors.END}")
    if not results.get('Frontend'):
        print("   • Iniciar frontend: cd frontend && npm run dev")
    if not results.get('Backend'):
        print("   • Verificar backend: cd backend && python app.py")
    if not results.get('Login'):
        print("   • Verificar credenciais de login")
    
    print(f"\n⏰ Teste concluído: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def main():
    """Executar todos os testes"""
    print(f"{Colors.BOLD}{Colors.BLUE}")
    print("🧪" + "="*58 + "🧪")
    print("  TESTE FINAL - AGENTE QUALIFICADOR IA PRONTO")
    print("🧪" + "="*58 + "🧪")
    print(f"{Colors.END}")
    
    results = {}
    
    # Teste 1: Backend
    results['Backend'] = test_backend_health()
    
    # Teste 2: Frontend
    results['Frontend'] = test_frontend_access()
    
    # Teste 3: Login
    token = test_login_system()
    results['Login'] = token is not None
    
    # Teste 4: Lead
    lead = test_lead_creation(token)
    results['Criação Lead'] = lead is not None
    
    # Teste 5: Qualificação
    results['Qualificação IA'] = test_qualification_start(lead, token)
    
    # Relatório Final
    generate_final_report(results)

if __name__ == "__main__":
    main()


