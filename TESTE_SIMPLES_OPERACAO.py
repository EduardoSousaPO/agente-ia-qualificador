#!/usr/bin/env python3
"""
TESTE SIMPLES - OPERAÇÃO REAL
Identifica problemas básicos que impedem operação real
"""

import os
import sys
from pathlib import Path

def verificar_arquivos_essenciais():
    """Verificar se arquivos essenciais existem"""
    print("🔍 VERIFICANDO ARQUIVOS ESSENCIAIS...")
    
    arquivos_essenciais = [
        "backend/main.py",
        "backend/.env",
        "backend/services/simple_supabase.py",
        "backend/services/qualification_service.py",
        "backend/app/routes/whatsapp.py",
        "frontend/package.json"
    ]
    
    problemas = []
    sucessos = []
    
    for arquivo in arquivos_essenciais:
        if Path(arquivo).exists():
            print(f"✅ {arquivo}")
            sucessos.append(arquivo)
        else:
            print(f"❌ {arquivo} - AUSENTE")
            problemas.append(arquivo)
    
    return len(problemas) == 0, problemas

def verificar_variaveis_ambiente():
    """Verificar variáveis de ambiente críticas"""
    print("\n🔧 VERIFICANDO VARIÁVEIS DE AMBIENTE...")
    
    # Carregar .env se existir
    env_file = Path("backend/.env")
    if env_file.exists():
        from dotenv import load_dotenv
        load_dotenv("backend/.env")
        print("✅ Arquivo .env carregado")
    else:
        print("❌ Arquivo .env não encontrado")
        return False, ["Arquivo .env ausente"]
    
    variaveis_criticas = [
        "SUPABASE_URL",
        "SUPABASE_SERVICE_ROLE_KEY",
        "OPENAI_API_KEY"
    ]
    
    problemas = []
    sucessos = []
    
    for var in variaveis_criticas:
        valor = os.getenv(var)
        if valor and valor != "your-value-here" and len(valor) > 10:
            print(f"✅ {var} - Configurada")
            sucessos.append(var)
        else:
            print(f"❌ {var} - Não configurada ou inválida")
            problemas.append(var)
    
    # Verificar Twilio (opcional)
    twilio_sid = os.getenv("TWILIO_ACCOUNT_SID")
    if twilio_sid and twilio_sid != "ACyour-twilio-account-sid":
        print(f"✅ TWILIO_ACCOUNT_SID - Configurada")
    else:
        print(f"⚠️ TWILIO_ACCOUNT_SID - Não configurada (opcional para testes)")
    
    return len(problemas) == 0, problemas

def verificar_dependencias():
    """Verificar dependências Python"""
    print("\n📦 VERIFICANDO DEPENDÊNCIAS...")
    
    dependencias_criticas = [
        "flask",
        "supabase",
        "openai",
        "requests",
        "python-dotenv"
    ]
    
    problemas = []
    sucessos = []
    
    for dep in dependencias_criticas:
        try:
            __import__(dep.replace("-", "_"))
            print(f"✅ {dep}")
            sucessos.append(dep)
        except ImportError:
            print(f"❌ {dep} - Não instalada")
            problemas.append(dep)
    
    return len(problemas) == 0, problemas

def verificar_estrutura_projeto():
    """Verificar estrutura básica do projeto"""
    print("\n📁 VERIFICANDO ESTRUTURA DO PROJETO...")
    
    diretorios_essenciais = [
        "backend",
        "backend/app",
        "backend/app/routes",
        "backend/services",
        "frontend",
        "frontend/src"
    ]
    
    problemas = []
    sucessos = []
    
    for diretorio in diretorios_essenciais:
        if Path(diretorio).is_dir():
            print(f"✅ {diretorio}/")
            sucessos.append(diretorio)
        else:
            print(f"❌ {diretorio}/ - AUSENTE")
            problemas.append(diretorio)
    
    return len(problemas) == 0, problemas

def testar_importacoes_backend():
    """Testar se o backend pode ser importado"""
    print("\n🐍 TESTANDO IMPORTAÇÕES DO BACKEND...")
    
    try:
        sys.path.append("backend")
        
        # Testar importações críticas
        from services.simple_supabase import simple_supabase
        print("✅ SimpleSupabaseService importado")
        
        from services.qualification_service import qualification_service
        print("✅ QualificationService importado")
        
        from app.routes.whatsapp import whatsapp_bp
        print("✅ WhatsApp Blueprint importado")
        
        return True, []
        
    except Exception as e:
        print(f"❌ Erro na importação: {str(e)}")
        return False, [str(e)]

def executar_diagnostico_completo():
    """Executar diagnóstico completo"""
    print("🔍 DIAGNÓSTICO COMPLETO - OPERAÇÃO REAL")
    print("=" * 50)
    
    testes = [
        ("Arquivos Essenciais", verificar_arquivos_essenciais),
        ("Variáveis de Ambiente", verificar_variaveis_ambiente),
        ("Dependências Python", verificar_dependencias),
        ("Estrutura do Projeto", verificar_estrutura_projeto),
        ("Importações Backend", testar_importacoes_backend)
    ]
    
    total_sucessos = 0
    total_problemas = []
    
    for nome_teste, funcao_teste in testes:
        sucesso, problemas = funcao_teste()
        if sucesso:
            total_sucessos += 1
        else:
            total_problemas.extend([f"{nome_teste}: {p}" for p in problemas])
    
    # Calcular score
    score = (total_sucessos / len(testes) * 100)
    
    print(f"\n📊 RESULTADO DO DIAGNÓSTICO:")
    print(f"   ✅ Testes aprovados: {total_sucessos}/{len(testes)}")
    print(f"   ❌ Problemas encontrados: {len(total_problemas)}")
    print(f"   📈 Score de Preparação: {score:.1f}%")
    
    if score >= 80:
        print(f"\n🎉 SISTEMA PRONTO PARA TESTES!")
        print(f"   ✅ Estrutura básica está correta")
        print(f"   🚀 Próximo passo: Iniciar backend e testar APIs")
    else:
        print(f"\n🔧 SISTEMA PRECISA DE CORREÇÕES")
        print(f"\n🚨 PROBLEMAS ENCONTRADOS:")
        for i, problema in enumerate(total_problemas, 1):
            print(f"   {i}. {problema}")
    
    # Gerar relatório
    relatorio = f"""# 🔍 DIAGNÓSTICO OPERAÇÃO REAL

**Score**: {score:.1f}%  
**Status**: {'✅ PRONTO PARA TESTES' if score >= 80 else '🔧 PRECISA CORREÇÕES'}

## ❌ PROBLEMAS ENCONTRADOS:
{chr(10).join([f'- {p}' for p in total_problemas]) if total_problemas else '✅ Nenhum problema encontrado'}

## 🚀 PRÓXIMOS PASSOS:
{'- Iniciar backend: cd backend && python main.py' if score >= 80 else '- Corrigir problemas listados acima'}
{'- Testar APIs com Postman ou curl' if score >= 80 else '- Re-executar diagnóstico após correções'}
{'- Configurar Twilio para WhatsApp real' if score >= 80 else ''}

---
*Diagnóstico gerado automaticamente*"""
    
    with open("DIAGNOSTICO_OPERACAO_REAL.md", 'w', encoding='utf-8') as f:
        f.write(relatorio)
    
    print(f"\n📄 Relatório salvo em: DIAGNOSTICO_OPERACAO_REAL.md")
    
    return score >= 80

if __name__ == "__main__":
    sistema_ok = executar_diagnostico_completo()
    
    if sistema_ok:
        print(f"\n🎉 SISTEMA PRONTO!")
        print(f"   📱 Execute: cd backend && python main.py")
        print(f"   🌐 Teste: http://localhost:5000/api/health")
    else:
        print(f"\n🔧 Corrija os problemas primeiro")

