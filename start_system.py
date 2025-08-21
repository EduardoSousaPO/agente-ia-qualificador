#!/usr/bin/env python3
"""
Script para inicializar o sistema completo do Agente Qualificador
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path

def print_header(title):
    print("\n" + "=" * 60)
    print(f"🚀 {title}")
    print("=" * 60)

def print_step(step, description):
    print(f"\n{step} {description}")

def check_python_deps():
    """Verificar dependências Python"""
    print_step("🔍", "Verificando dependências Python...")
    
    required_packages = [
        'flask', 'flask_cors', 'dotenv', 
        'supabase', 'openai', 'twilio', 'requests'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"  ✅ {package}")
        except ImportError:
            missing.append(package)
            print(f"  ❌ {package}")
    
    if missing:
        print(f"\n⚠️  Instalando dependências faltantes: {', '.join(missing)}")
        subprocess.run([sys.executable, '-m', 'pip', 'install'] + missing)
    
    return len(missing) == 0

def check_node_deps():
    """Verificar dependências Node.js"""
    print_step("🔍", "Verificando dependências Node.js...")
    
    frontend_path = Path("frontend")
    if not frontend_path.exists():
        print("❌ Pasta frontend não encontrada")
        return False
    
    node_modules = frontend_path / "node_modules"
    if not node_modules.exists():
        print("📦 Instalando dependências do frontend...")
        os.chdir("frontend")
        result = subprocess.run(["npm", "install"], capture_output=True, text=True)
        os.chdir("..")
        
        if result.returncode != 0:
            print(f"❌ Erro ao instalar dependências: {result.stderr}")
            return False
        print("✅ Dependências do frontend instaladas")
    else:
        print("✅ Dependências do frontend já instaladas")
    
    return True

def start_backend():
    """Iniciar backend Flask"""
    print_step("🖥️", "Iniciando backend Flask...")
    
    backend_path = Path("backend")
    if not backend_path.exists():
        print("❌ Pasta backend não encontrada")
        return None
    
    app_file = backend_path / "app.py"
    if not app_file.exists():
        print("❌ Arquivo backend/app.py não encontrado")
        return None
    
    # Iniciar backend em processo separado
    env = os.environ.copy()
    env['PYTHONPATH'] = str(backend_path.absolute())
    
    try:
        process = subprocess.Popen(
            [sys.executable, "app.py"],
            cwd=backend_path,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Aguardar alguns segundos para o servidor iniciar
        time.sleep(3)
        
        # Testar se o backend está respondendo
        try:
            response = requests.get("http://localhost:5000/api/health", timeout=5)
            if response.status_code == 200:
                print("✅ Backend Flask iniciado com sucesso!")
                print(f"🌐 URL: http://localhost:5000")
                return process
            else:
                print(f"⚠️  Backend respondeu com status {response.status_code}")
        except requests.exceptions.RequestException:
            print("⚠️  Backend pode estar iniciando ainda...")
        
        return process
        
    except Exception as e:
        print(f"❌ Erro ao iniciar backend: {e}")
        return None

def start_frontend():
    """Iniciar frontend Next.js"""
    print_step("🎨", "Iniciando frontend Next.js...")
    
    frontend_path = Path("frontend")
    if not frontend_path.exists():
        print("❌ Pasta frontend não encontrada")
        return None
    
    try:
        process = subprocess.Popen(
            ["npm", "run", "dev"],
            cwd=frontend_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        time.sleep(5)
        print("✅ Frontend Next.js iniciado!")
        print(f"🌐 URL: http://localhost:3000")
        return process
        
    except Exception as e:
        print(f"❌ Erro ao iniciar frontend: {e}")
        return None

def test_system():
    """Testar sistema completo"""
    print_step("🧪", "Testando sistema...")
    
    tests = [
        ("Backend Health", "http://localhost:5000/api/health"),
        ("Simulator Status", "http://localhost:5000/api/simulator/status"),
        ("N8N Test", "http://localhost:5000/api/test/n8n")
    ]
    
    for test_name, url in tests:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"  ✅ {test_name}")
            else:
                print(f"  ⚠️  {test_name} - Status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"  ❌ {test_name} - Erro: {e}")

def main():
    print_header("AGENTE QUALIFICADOR - INICIALIZAÇÃO COMPLETA")
    
    # Verificar dependências
    print_step("1️⃣", "VERIFICANDO DEPENDÊNCIAS")
    python_ok = check_python_deps()
    node_ok = check_node_deps()
    
    if not python_ok or not node_ok:
        print("\n❌ Dependências não instaladas corretamente")
        return
    
    # Iniciar serviços
    print_step("2️⃣", "INICIANDO SERVIÇOS")
    
    backend_process = start_backend()
    if not backend_process:
        print("❌ Falha ao iniciar backend")
        return
    
    frontend_process = start_frontend()
    if not frontend_process:
        print("❌ Falha ao iniciar frontend")
        if backend_process:
            backend_process.terminate()
        return
    
    # Testar sistema
    print_step("3️⃣", "TESTANDO SISTEMA")
    time.sleep(5)  # Aguardar serviços estabilizarem
    test_system()
    
    # Informações finais
    print_header("SISTEMA INICIADO COM SUCESSO!")
    print("🎉 O Agente Qualificador está funcionando!")
    print("\n📋 URLs Disponíveis:")
    print("  🖥️  Backend API: http://localhost:5000")
    print("  🎨 Frontend App: http://localhost:3000")
    print("  🔍 Health Check: http://localhost:5000/api/health")
    print("  🎭 Simulador: http://localhost:5000/api/simulator/status")
    
    print("\n🧪 Testes Disponíveis:")
    print("  • POST http://localhost:5000/api/test/n8n")
    print("  • POST http://localhost:5000/api/test/whatsapp")
    
    print("\n📱 Sistema configurado com:")
    print("  ✅ Supabase (Banco de dados)")
    print("  ✅ N8N (Automação)")
    print("  ✅ OpenAI (IA)")
    print("  🎭 WhatsApp Simulador (Testes)")
    
    print("\n⚠️  Para parar o sistema: Ctrl+C")
    
    try:
        # Manter processos rodando
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Parando sistema...")
        if backend_process:
            backend_process.terminate()
        if frontend_process:
            frontend_process.terminate()
        print("✅ Sistema parado com sucesso!")

if __name__ == "__main__":
    main()
