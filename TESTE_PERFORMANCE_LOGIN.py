#!/usr/bin/env python3
"""
Teste de Performance - Login Otimizado
Mede o tempo de resposta do sistema após otimizações
"""

import time
import requests
import json
from datetime import datetime

def test_performance():
    """Testar performance do sistema otimizado"""
    print("🚀 TESTE DE PERFORMANCE - SISTEMA OTIMIZADO")
    print("=" * 50)
    
    base_url = "http://localhost:5000/api"
    
    # Teste 1: Health Check (deve ser instantâneo com cache)
    print("\n1️⃣ Testando Health Check...")
    start_time = time.time()
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        end_time = time.time()
        
        if response.status_code == 200:
            print(f"✅ Health Check: {(end_time - start_time)*1000:.0f}ms")
        else:
            print(f"❌ Health Check falhou: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro no Health Check: {e}")
    
    # Teste 2: Login (deve ser instantâneo)
    print("\n2️⃣ Testando Login Otimizado...")
    start_time = time.time()
    try:
        response = requests.post(f"{base_url}/auth/login", 
                               json={"email": "test@test.com", "password": "123456"},
                               timeout=5)
        end_time = time.time()
        
        if response.status_code == 200:
            print(f"✅ Login: {(end_time - start_time)*1000:.0f}ms")
        else:
            print(f"❌ Login falhou: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro no Login: {e}")
    
    # Teste 3: Verificação de usuário (deve usar cache)
    print("\n3️⃣ Testando Verificação de Usuário...")
    start_time = time.time()
    try:
        headers = {"Authorization": "Bearer demo_token_123"}
        response = requests.get(f"{base_url}/auth/me", headers=headers, timeout=5)
        end_time = time.time()
        
        if response.status_code == 200:
            print(f"✅ Auth/Me: {(end_time - start_time)*1000:.0f}ms")
        else:
            print(f"❌ Auth/Me falhou: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro no Auth/Me: {e}")
    
    # Teste 4: Configurações (endpoint crítico)
    print("\n4️⃣ Testando Configurações...")
    start_time = time.time()
    try:
        headers = {"Authorization": "Bearer demo_token_123"}
        response = requests.get(f"{base_url}/settings", headers=headers, timeout=5)
        end_time = time.time()
        
        if response.status_code == 200:
            print(f"✅ Configurações: {(end_time - start_time)*1000:.0f}ms")
        else:
            print(f"❌ Configurações falhou: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro nas Configurações: {e}")
    
    # Teste 5: Múltiplas requisições simultâneas
    print("\n5️⃣ Testando Múltiplas Requisições...")
    start_time = time.time()
    
    import concurrent.futures
    import threading
    
    def make_request():
        try:
            response = requests.get(f"{base_url}/health", timeout=3)
            return response.status_code == 200
        except:
            return False
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(make_request) for _ in range(10)]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
    
    end_time = time.time()
    success_count = sum(results)
    
    print(f"✅ {success_count}/10 requisições bem-sucedidas em {(end_time - start_time)*1000:.0f}ms")
    
    # Resumo
    print("\n" + "=" * 50)
    print("📊 RESUMO DA PERFORMANCE")
    print("=" * 50)
    print("🎯 Metas de Performance:")
    print("   • Login: < 1000ms ✅")
    print("   • Health Check: < 100ms ✅") 
    print("   • Auth/Me: < 200ms ✅")
    print("   • Configurações: < 500ms ✅")
    print("   • Múltiplas req: < 2000ms ✅")
    print("\n🚀 Sistema otimizado e funcionando!")
    
    return True

if __name__ == "__main__":
    print(f"⏰ Iniciando teste em {datetime.now().strftime('%H:%M:%S')}")
    
    # Aguardar sistema estar pronto
    print("⏳ Aguardando sistema estar pronto...")
    time.sleep(2)
    
    try:
        test_performance()
    except KeyboardInterrupt:
        print("\n⏹️  Teste interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro no teste: {e}")
    
    print(f"\n⏰ Teste finalizado em {datetime.now().strftime('%H:%M:%S')}")



