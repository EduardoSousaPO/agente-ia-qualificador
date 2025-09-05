#!/usr/bin/env python3
"""
AUDITORIA COMPLETA - OPERAÇÃO REAL
Identifica todos os problemas que impedem operação com leads reais
"""

import requests
import json
import time
from datetime import datetime

class AuditoriaOperacaoReal:
    def __init__(self):
        self.base_url = "http://localhost:5000"
        self.problemas = []
        self.sucessos = []
        
    def log_resultado(self, teste, sucesso, detalhes=""):
        timestamp = datetime.now().strftime("%H:%M:%S")
        status = "✅" if sucesso else "❌"
        print(f"{status} [{timestamp}] {teste}")
        if detalhes:
            print(f"    💡 {detalhes}")
        
        if sucesso:
            self.sucessos.append(teste)
        else:
            self.problemas.append(f"{teste}: {detalhes}")
    
    def teste_1_backend_health(self):
        """Teste 1: Verificar se backend está saudável"""
        print("\n🏥 TESTE 1: SAÚDE DO BACKEND")
        try:
            response = requests.get(f"{self.base_url}/api/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                features = data.get('features', {})
                
                self.log_resultado("Backend Online", True)
                self.log_resultado("Supabase Configurado", features.get('supabase', False))
                self.log_resultado("OpenAI Configurado", features.get('openai', False))
                self.log_resultado("Twilio Configurado", features.get('twilio', False))
                
                return True
            else:
                self.log_resultado("Backend Health Check", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_resultado("Backend Health Check", False, str(e))
            return False
    
    def teste_2_criacao_leads(self):
        """Teste 2: Criar lead via API"""
        print("\n📋 TESTE 2: CRIAÇÃO DE LEADS")
        try:
            lead_data = {
                "name": f"Lead Teste {int(time.time())}",
                "phone": f"119999{int(time.time()) % 10000:04d}",
                "email": f"teste{int(time.time())}@example.com",
                "origem": "teste_auditoria"
            }
            
            response = requests.post(
                f"{self.base_url}/api/leads",
                json=lead_data,
                timeout=10
            )
            
            if response.status_code == 201:
                data = response.json()
                lead_id = data.get('lead', {}).get('id')
                self.log_resultado("Criação de Lead", True, f"ID: {lead_id}")
                return lead_id
            else:
                self.log_resultado("Criação de Lead", False, f"Status: {response.status_code}")
                return None
        except Exception as e:
            self.log_resultado("Criação de Lead", False, str(e))
            return None
    
    def teste_3_listagem_leads(self):
        """Teste 3: Listar leads"""
        print("\n📊 TESTE 3: LISTAGEM DE LEADS")
        try:
            response = requests.get(f"{self.base_url}/api/leads", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                count = data.get('count', 0)
                self.log_resultado("Listagem de Leads", True, f"Total: {count} leads")
                return count > 0
            else:
                self.log_resultado("Listagem de Leads", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_resultado("Listagem de Leads", False, str(e))
            return False
    
    def teste_4_webhook_whatsapp(self):
        """Teste 4: Webhook WhatsApp"""
        print("\n📱 TESTE 4: WEBHOOK WHATSAPP")
        try:
            # Simular webhook do Twilio
            webhook_data = {
                "Body": "Olá, tenho interesse em investimentos",
                "From": "whatsapp:+5511999887766",
                "To": "whatsapp:+14155238886",
                "MessageSid": f"TEST_{int(time.time())}",
                "AccountSid": "TEST_ACCOUNT"
            }
            
            response = requests.post(
                f"{self.base_url}/api/whatsapp/webhook",
                data=webhook_data,  # Twilio envia como form data
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                self.log_resultado("Webhook WhatsApp", True, "Processou mensagem")
                return True
            else:
                self.log_resultado("Webhook WhatsApp", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_resultado("Webhook WhatsApp", False, str(e))
            return False
    
    def teste_5_configuracoes(self):
        """Teste 5: API de Configurações"""
        print("\n⚙️ TESTE 5: CONFIGURAÇÕES")
        try:
            headers = {"Authorization": "Bearer demo_token_123"}
            response = requests.get(
                f"{self.base_url}/api/settings",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                settings = data.get('settings', {})
                ai_config = settings.get('ai_config', {})
                
                self.log_resultado("API Configurações", True)
                self.log_resultado("Configurações IA", bool(ai_config))
                return True
            else:
                self.log_resultado("API Configurações", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_resultado("API Configurações", False, str(e))
            return False
    
    def teste_6_base_conhecimento(self):
        """Teste 6: Base de Conhecimento"""
        print("\n📚 TESTE 6: BASE DE CONHECIMENTO")
        try:
            tenant_id = "05dc8c52-c0a0-44ae-aa2a-eeaa01090a27"
            response = requests.get(
                f"{self.base_url}/api/knowledge-base/{tenant_id}",
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                content = data.get('data', {}).get('content', '')
                
                self.log_resultado("Base de Conhecimento", True)
                self.log_resultado("Conteúdo Carregado", len(content) > 0, f"Tamanho: {len(content)} chars")
                return True
            else:
                self.log_resultado("Base de Conhecimento", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_resultado("Base de Conhecimento", False, str(e))
            return False
    
    def teste_7_fluxo_qualificacao(self):
        """Teste 7: Fluxo completo de qualificação"""
        print("\n🎯 TESTE 7: FLUXO DE QUALIFICAÇÃO")
        try:
            # Simular sequência de mensagens de qualificação
            mensagens = [
                "Olá, tenho interesse em investimentos",
                "Tenho 500 mil reais para investir",
                "Quero investir nos próximos 30 dias",
                "Já invisto em renda fixa"
            ]
            
            phone = f"5511999{int(time.time()) % 100000:05d}"
            
            for i, mensagem in enumerate(mensagens):
                webhook_data = {
                    "Body": mensagem,
                    "From": f"whatsapp:+{phone}",
                    "To": "whatsapp:+14155238886",
                    "MessageSid": f"TEST_FLOW_{int(time.time())}_{i}",
                    "AccountSid": "TEST_ACCOUNT"
                }
                
                response = requests.post(
                    f"{self.base_url}/api/whatsapp/webhook",
                    data=webhook_data,
                    timeout=15
                )
                
                if response.status_code != 200:
                    self.log_resultado(f"Qualificação Passo {i+1}", False, f"Status: {response.status_code}")
                    return False
                
                time.sleep(1)  # Aguardar processamento
            
            self.log_resultado("Fluxo de Qualificação", True, "4 mensagens processadas")
            return True
            
        except Exception as e:
            self.log_resultado("Fluxo de Qualificação", False, str(e))
            return False
    
    def executar_auditoria_completa(self):
        """Executar auditoria completa do sistema"""
        print("🔍 AUDITORIA COMPLETA - OPERAÇÃO REAL")
        print("=" * 60)
        
        # Executar todos os testes
        testes = [
            self.teste_1_backend_health,
            self.teste_2_criacao_leads,
            self.teste_3_listagem_leads,
            self.teste_4_webhook_whatsapp,
            self.teste_5_configuracoes,
            self.teste_6_base_conhecimento,
            self.teste_7_fluxo_qualificacao
        ]
        
        resultados = []
        for teste in testes:
            resultado = teste()
            resultados.append(resultado)
        
        # Calcular score
        sucessos = sum(1 for r in resultados if r)
        total = len(resultados)
        score = (sucessos / total * 100) if total > 0 else 0
        
        print(f"\n📊 RESULTADO FINAL:")
        print(f"   ✅ Testes aprovados: {len(self.sucessos)}")
        print(f"   ❌ Problemas encontrados: {len(self.problemas)}")
        print(f"   📈 Score de Operação Real: {score:.1f}%")
        
        if score >= 90:
            print(f"\n🎉 SISTEMA PRONTO PARA OPERAÇÃO REAL!")
            print(f"   ✅ Apenas configuração Twilio/WhatsApp Business necessária")
        elif score >= 70:
            print(f"\n⚠️ SISTEMA QUASE PRONTO - Pequenos ajustes necessários")
        else:
            print(f"\n🔧 SISTEMA PRECISA DE CORREÇÕES IMPORTANTES")
        
        # Mostrar problemas
        if self.problemas:
            print(f"\n🚨 PROBLEMAS ENCONTRADOS:")
            for i, problema in enumerate(self.problemas, 1):
                print(f"   {i}. {problema}")
        
        return score >= 90
    
    def gerar_relatorio_final(self):
        """Gerar relatório final da auditoria"""
        score = (len(self.sucessos) / (len(self.sucessos) + len(self.problemas)) * 100) if (len(self.sucessos) + len(self.problemas)) > 0 else 0
        
        relatorio = f"""# 🔍 AUDITORIA OPERAÇÃO REAL - RELATÓRIO FINAL

**Data**: {datetime.now().strftime("%d/%m/%Y %H:%M")}  
**Score**: {score:.1f}%  
**Status**: {'✅ PRONTO PARA OPERAÇÃO REAL' if score >= 90 else '🔧 PRECISA CORREÇÕES'}

## 📊 RESULTADOS:
- ✅ Sucessos: {len(self.sucessos)}
- ❌ Problemas: {len(self.problemas)}

## ✅ FUNCIONALIDADES VALIDADAS:
{chr(10).join([f'- {s}' for s in self.sucessos])}

## ❌ PROBLEMAS ENCONTRADOS:
{chr(10).join([f'- {p}' for p in self.problemas]) if self.problemas else '✅ Nenhum problema crítico encontrado'}

## 🚀 PRÓXIMOS PASSOS:
{'- Configurar Twilio/WhatsApp Business para operação real' if score >= 90 else '- Corrigir problemas listados acima'}
{'- Testar com número real do WhatsApp' if score >= 90 else '- Re-executar auditoria após correções'}

---
*Auditoria gerada automaticamente*"""
        
        with open("RELATORIO_AUDITORIA_OPERACAO_REAL.md", 'w', encoding='utf-8') as f:
            f.write(relatorio)
        
        print(f"\n📄 Relatório salvo em: RELATORIO_AUDITORIA_OPERACAO_REAL.md")

if __name__ == "__main__":
    auditor = AuditoriaOperacaoReal()
    
    # Executar auditoria
    sistema_pronto = auditor.executar_auditoria_completa()
    
    # Gerar relatório
    auditor.gerar_relatorio_final()
    
    # Status final
    if sistema_pronto:
        print(f"\n🎉 SISTEMA 100% PRONTO PARA OPERAÇÃO REAL!")
        print(f"   📱 Apenas configure Twilio/WhatsApp Business")
    else:
        print(f"\n🔧 Corrija os problemas para operação real")

