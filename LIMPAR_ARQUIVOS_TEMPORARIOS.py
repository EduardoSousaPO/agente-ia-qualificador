#!/usr/bin/env python3
"""
LIMPAR ARQUIVOS TEMPORÁRIOS E DE TESTE
Remove arquivos criados durante correções que não são mais necessários
"""

import os
from pathlib import Path

def limpar_arquivos_temporarios():
    """Remove arquivos temporários e de teste desnecessários"""
    print("🧹 LIMPANDO ARQUIVOS TEMPORÁRIOS E DE TESTE")
    print("=" * 60)
    
    # Lista de arquivos temporários para remover
    arquivos_para_remover = [
        # Scripts de correção temporários
        "CORRECOES_MVP_100.py",
        "REMOVER_FALLBACKS_SIMULADOS.py",
        "VALIDACAO_MVP_100_FINAL.py", 
        "TESTE_MVP_SIMPLES.py",
        "LIMPAR_ARQUIVOS_TEMPORARIOS.py",  # Este próprio arquivo
        
        # Scripts de refatoração (já executados)
        "REFATORACAO_FASE1.py",
        "REFATORACAO_FASE2.py", 
        "REFATORACAO_FASE3.py",
        "REFATORACAO_FASE3_FIXED.py",
        
        # Arquivos de auditoria temporários
        "AUDITORIA_COMPLETA_PROJETO.py",
        
        # Auto-start para testes (não necessário em produção)
        "backend/auto_start_for_tests.py",
        
        # Scripts de diagnóstico temporários
        "backend/diagnostico_e_correcao_completa.py",
        
        # Testes temporários na raiz
        "tests/test_mvp_100_percent.py",
        "tests/TESTAR_SISTEMA.py",
        
        # Relatórios temporários de validação
        "RESULTADO_MVP_100.md",
        "PLANO_MVP_100_PORCENTO.md",
    ]
    
    removidos = []
    nao_encontrados = []
    
    for arquivo in arquivos_para_remover:
        caminho = Path(arquivo)
        if caminho.exists():
            try:
                caminho.unlink()
                removidos.append(arquivo)
                print(f"✅ Removido: {arquivo}")
            except Exception as e:
                print(f"❌ Erro ao remover {arquivo}: {str(e)}")
        else:
            nao_encontrados.append(arquivo)
            print(f"⚠️ Não encontrado: {arquivo}")
    
    print(f"\n📊 RESUMO DA LIMPEZA:")
    print(f"   ✅ Arquivos removidos: {len(removidos)}")
    print(f"   ⚠️ Não encontrados: {len(nao_encontrados)}")
    
    if removidos:
        print(f"\n🗑️ ARQUIVOS REMOVIDOS:")
        for arquivo in removidos:
            print(f"   - {arquivo}")
    
    # Verificar se há outros arquivos de teste esquecidos
    print(f"\n🔍 VERIFICANDO OUTROS ARQUIVOS DE TESTE...")
    
    # Buscar arquivos com padrões de teste
    padroes_teste = ["test_", "debug_", "temp_", "tmp_", "_test", "_temp"]
    arquivos_suspeitos = []
    
    for root, dirs, files in os.walk("."):
        # Ignorar node_modules e __pycache__
        dirs[:] = [d for d in dirs if d not in ['node_modules', '__pycache__', '.git']]
        
        for file in files:
            if any(padrao in file.lower() for padrao in padroes_teste):
                caminho_completo = os.path.join(root, file)
                # Ignorar arquivos legítimos de teste
                if not any(legitimo in caminho_completo for legitimo in [
                    'backend/tests/', 'frontend/src/', 'tests/test_auth_integration.py',
                    'tests/test_billing_', 'tests/test_endpoints.py', 'tests/test_knowledge_base_',
                    'tests/test_multi_tenant_', 'tests/test_production_ready.py', 'tests/test_qualification_fix.py'
                ]):
                    arquivos_suspeitos.append(caminho_completo)
    
    if arquivos_suspeitos:
        print(f"⚠️ Arquivos suspeitos encontrados (verifique manualmente):")
        for arquivo in arquivos_suspeitos:
            print(f"   - {arquivo}")
    else:
        print(f"✅ Nenhum arquivo suspeito encontrado")
    
    print(f"\n🎯 LIMPEZA CONCLUÍDA!")
    print(f"✅ Sistema limpo de arquivos temporários")
    print(f"✅ Apenas arquivos de produção mantidos")

if __name__ == "__main__":
    limpar_arquivos_temporarios()

