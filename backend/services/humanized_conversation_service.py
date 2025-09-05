#!/usr/bin/env python3
"""
Serviço de Conversação Humanizada
Transforma o agente robótico em um consultor humano e natural
"""

import json
import re
from typing import Dict, List, Optional, Tuple
import structlog
from services.openai_service import get_openai_service
from services.simple_supabase import simple_supabase

logger = structlog.get_logger()

class HumanizedConversationService:
    def __init__(self):
        """Inicializar serviço de conversação humanizada"""
        self.openai_service = get_openai_service()
        
        # Personalidade do agente
        self.agent_personality = {
            "name": "Ana",
            "role": "Consultora de Investimentos",
            "style": "amigável, profissional, empática",
            "approach": "conversacional, não robótica"
        }
        
        # Estados da conversa mais naturais
        self.conversation_states = {
            "inicio": "Iniciando conversa",
            "conhecendo_cliente": "Conhecendo o cliente",
            "explorando_patrimonio": "Explorando situação financeira",
            "entendendo_objetivos": "Entendendo objetivos",
            "avaliando_urgencia": "Avaliando timing",
            "medindo_interesse": "Medindo interesse real",
            "finalizando": "Finalizando qualificação",
            "pos_qualificacao": "Pós-qualificação"
        }
    
    def get_company_context(self, tenant_id: str) -> str:
        """Buscar contexto da empresa da base de conhecimento"""
        try:
            simple_supabase._ensure_client()
            
            result = simple_supabase.client.table('knowledge_base') \
                .select('content') \
                .eq('tenant_id', tenant_id) \
                .execute()
            
            if result.data and result.data[0]['content']:
                return result.data[0]['content']
            
            # Contexto padrão se não houver base de conhecimento
            return """
            Somos uma consultoria especializada em investimentos que ajuda pessoas a 
            multiplicar seu patrimônio de forma segura e inteligente. Nossa equipe tem 
            mais de 10 anos de experiência no mercado financeiro e já ajudou centenas 
            de clientes a alcançar seus objetivos financeiros.
            """
            
        except Exception as e:
            logger.error("Erro ao buscar contexto da empresa", error=str(e))
            return "Somos uma consultoria de investimentos especializada."
    
    def create_humanized_prompt(self, company_context: str, conversation_history: List[Dict], 
                              current_state: str, user_message: str) -> str:
        """Criar prompt humanizado para a IA"""
        
        # Informações coletadas até agora
        collected_info = self._extract_collected_info(conversation_history)
        
        prompt = f"""
Você é a Ana, uma consultora de investimentos experiente e empática. Você trabalha para uma empresa com o seguinte contexto:

CONTEXTO DA EMPRESA:
{company_context}

SUA PERSONALIDADE:
- Nome: Ana
- Profissão: Consultora de Investimentos Sênior
- Estilo: Amigável, profissional, empática e genuinamente interessada em ajudar
- Abordagem: Conversacional e natural, NUNCA robótica ou com perguntas de múltipla escolha
- Objetivo: Conhecer o cliente de forma natural para conectá-lo com o especialista certo

ESTADO ATUAL DA CONVERSA: {current_state}

INFORMAÇÕES JÁ COLETADAS:
{json.dumps(collected_info, indent=2, ensure_ascii=False)}

HISTÓRICO DA CONVERSA:
{self._format_conversation_history(conversation_history)}

ÚLTIMA MENSAGEM DO CLIENTE: "{user_message}"

INSTRUÇÕES PARA SUA RESPOSTA:

1. SEJA HUMANA E NATURAL:
   - Responda como uma pessoa real responderia
   - Use expressões naturais, emojis ocasionais
   - Faça perguntas abertas, não múltipla escolha
   - Demonstre interesse genuíno

2. COLETE INFORMAÇÕES NATURALMENTE:
   Você precisa descobrir sutilmente:
   - Patrimônio disponível para investir (sem ser direta)
   - Objetivos com os investimentos
   - Urgência/timing
   - Nível de interesse real

3. BASEIE-SE NO CONTEXTO DA EMPRESA:
   - Use as informações da empresa nas suas respostas
   - Mencione diferenciais e experiência quando relevante
   - Seja específica sobre como podem ajudar

4. FLUXO NATURAL:
   - Se é o início, seja acolhedora e apresente-se
   - Se já está no meio, continue a conversa naturalmente
   - Faça transições suaves entre tópicos
   - Não force informações, deixe fluir

5. QUANDO TIVER INFORMAÇÕES SUFICIENTES:
   - Faça um resumo natural do que entendeu
   - Explique próximos passos de forma humana
   - Seja transparente sobre o processo

RESPONDA COMO A ANA RESPONDERIA, DE FORMA NATURAL E HUMANA:
"""
        
        return prompt
    
    def _extract_collected_info(self, conversation_history: List[Dict]) -> Dict:
        """Extrair informações já coletadas da conversa"""
        info = {
            "patrimonio": None,
            "objetivo": None,
            "urgencia": None,
            "interesse": None,
            "outras_informacoes": []
        }
        
        # Analisar mensagens do usuário para extrair informações
        for msg in conversation_history:
            if msg.get('role') == 'user':
                content = msg.get('content', '').lower()
                
                # Detectar menções de valores/patrimônio
                if any(word in content for word in ['mil', 'milhão', 'reais', 'r$', 'dinheiro', 'valor']):
                    info["outras_informacoes"].append(f"Mencionou valores: {msg.get('content')}")
                
                # Detectar objetivos
                if any(word in content for word in ['aposentadoria', 'crescer', 'multiplicar', 'reserva']):
                    info["outras_informacoes"].append(f"Objetivo mencionado: {msg.get('content')}")
                
                # Detectar urgência
                if any(word in content for word in ['urgente', 'rápido', 'logo', 'semana', 'mês']):
                    info["outras_informacoes"].append(f"Timing mencionado: {msg.get('content')}")
        
        return info
    
    def _format_conversation_history(self, conversation_history: List[Dict]) -> str:
        """Formatar histórico da conversa para o prompt"""
        formatted = []
        
        for msg in conversation_history[-6:]:  # Últimas 6 mensagens
            role = "Ana" if msg.get('role') == 'assistant' else "Cliente"
            content = msg.get('content', '')
            formatted.append(f"{role}: {content}")
        
        return "\n".join(formatted) if formatted else "Primeira interação"
    
    def process_natural_conversation(self, session_id: str, user_message: str, 
                                   tenant_id: str = None) -> Dict:
        """Processar conversa de forma natural e humanizada"""
        try:
            # Buscar sessão e contexto
            session_result = simple_supabase.client.table('sessions') \
                .select('*, leads(*, tenants(*))') \
                .eq('id', session_id) \
                .execute()
            
            if not session_result.data:
                return {"success": False, "error": "Sessão não encontrada"}
            
            session = session_result.data[0]
            lead = session['leads']
            tenant = lead['tenants'] if lead else None
            
            # Usar tenant_id da sessão se não fornecido
            if not tenant_id and tenant:
                tenant_id = tenant['id']
            elif not tenant_id:
                tenant_id = "05dc8c52-c0a0-44ae-aa2a-eeaa01090a27"  # Default
            
            # Buscar contexto da empresa
            company_context = self.get_company_context(tenant_id)
            
            # Obter histórico da conversa
            context = session.get('context', {})
            conversation_history = context.get('conversation_history', [])
            current_state = context.get('current_state', 'inicio')
            
            # Adicionar mensagem do usuário ao histórico
            conversation_history.append({
                'role': 'user',
                'content': user_message
            })
            
            # Criar prompt humanizado
            humanized_prompt = self.create_humanized_prompt(
                company_context, conversation_history, current_state, user_message
            )
            
            # Gerar resposta humanizada
            messages = [
                {"role": "system", "content": humanized_prompt},
                {"role": "user", "content": user_message}
            ]
            
            ai_response = self.openai_service.chat_completion(messages)
            
            # Adicionar resposta da IA ao histórico
            conversation_history.append({
                'role': 'assistant',
                'content': ai_response
            })
            
            # Analisar se coletou informações suficientes
            qualification_analysis = self._analyze_qualification_readiness(conversation_history)
            
            # Atualizar contexto da sessão
            updated_context = {
                **context,
                'conversation_history': conversation_history,
                'current_state': qualification_analysis.get('next_state', current_state),
                'collected_info': qualification_analysis.get('collected_info', {}),
                'qualification_ready': qualification_analysis.get('ready', False)
            }
            
            # Salvar contexto atualizado
            simple_supabase.client.table('sessions') \
                .update({'context': updated_context}) \
                .eq('id', session_id) \
                .execute()
            
            # Se qualificação está pronta, calcular score
            final_result = {}
            if qualification_analysis.get('ready'):
                final_result = self._calculate_final_qualification(
                    qualification_analysis['collected_info'], session_id
                )
            
            return {
                "success": True,
                "message": ai_response,
                "context": updated_context,
                "qualification_ready": qualification_analysis.get('ready', False),
                "completed": final_result.get('completed', False),
                "qualified": final_result.get('qualified', False),
                "score": final_result.get('score', 0)
            }
            
        except Exception as e:
            logger.error("Erro no processamento de conversa humanizada", 
                        session_id=session_id, error=str(e))
            return {
                "success": False,
                "error": "Erro no processamento da conversa",
                "message": "Desculpe, houve um problema. Pode repetir sua mensagem?"
            }
    
    def _analyze_qualification_readiness(self, conversation_history: List[Dict]) -> Dict:
        """Analisar se a conversa coletou informações suficientes para qualificação"""
        
        # Prompt para analisar se temos informações suficientes
        analysis_prompt = f"""
Analise esta conversa e determine se temos informações suficientes para qualificar o lead.

CONVERSA:
{self._format_conversation_history(conversation_history)}

Você precisa identificar se conseguimos descobrir:
1. PATRIMÔNIO: Quanto tem disponível para investir (aproximadamente)
2. OBJETIVO: O que quer alcançar com investimentos
3. URGÊNCIA: Quando pretende começar/investir
4. INTERESSE: Nível de interesse real em prosseguir

Responda APENAS em JSON:
{{
    "ready": true/false,
    "collected_info": {{
        "patrimonio": "descrição ou null",
        "objetivo": "descrição ou null", 
        "urgencia": "descrição ou null",
        "interesse": "descrição ou null"
    }},
    "next_state": "estado_sugerido",
    "confidence": 0-100
}}
"""
        
        try:
            messages = [{"role": "system", "content": analysis_prompt}]
            response = self.openai_service.chat_completion(messages)
            
            # Tentar extrair JSON da resposta
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                analysis = json.loads(json_match.group())
                return analysis
            
        except Exception as e:
            logger.error("Erro na análise de prontidão", error=str(e))
        
        return {
            "ready": len(conversation_history) >= 8,  # Pelo menos 4 trocas
            "collected_info": {},
            "next_state": "conhecendo_cliente",
            "confidence": 50
        }
    
    def _calculate_final_qualification(self, collected_info: Dict, session_id: str) -> Dict:
        """Calcular qualificação final baseada nas informações coletadas"""
        
        # Prompt para converter informações naturais em score
        scoring_prompt = f"""
Baseado nas informações coletadas naturalmente, calcule um score de qualificação de 0-100.

INFORMAÇÕES COLETADAS:
{json.dumps(collected_info, indent=2, ensure_ascii=False)}

CRITÉRIOS DE PONTUAÇÃO:
- PATRIMÔNIO (0-40 pontos):
  * Mais de R$ 500 mil = 40 pontos
  * R$ 200-500 mil = 30 pontos  
  * R$ 50-200 mil = 20 pontos
  * Até R$ 50 mil = 10 pontos

- OBJETIVO (0-25 pontos):
  * Crescimento/Multiplicar = 25 pontos
  * Aposentadoria = 20 pontos
  * Reserva/Proteção = 15 pontos
  * Especulação = 10 pontos

- URGÊNCIA (0-20 pontos):
  * Esta semana/Urgente = 20 pontos
  * Este mês = 15 pontos
  * Próximos 3 meses = 10 pontos
  * Sem pressa = 5 pontos

- INTERESSE (0-15 pontos):
  * Muito interessado/Urgente = 15 pontos
  * Interessado = 10 pontos
  * Talvez/Pensando = 5 pontos
  * Pouco interesse = 0 pontos

Responda APENAS em JSON:
{{
    "score": 0-100,
    "qualified": true/false,
    "breakdown": {{
        "patrimonio": "pontos e justificativa",
        "objetivo": "pontos e justificativa",
        "urgencia": "pontos e justificativa", 
        "interesse": "pontos e justificativa"
    }},
    "summary": "resumo da qualificação"
}}
"""
        
        try:
            messages = [{"role": "system", "content": scoring_prompt}]
            response = self.openai_service.chat_completion(messages)
            
            # Extrair JSON
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                scoring = json.loads(json_match.group())
                
                # Atualizar lead com score
                lead_result = simple_supabase.client.table('sessions') \
                    .select('lead_id') \
                    .eq('id', session_id) \
                    .execute()
                
                if lead_result.data:
                    lead_id = lead_result.data[0]['lead_id']
                    
                    simple_supabase.client.table('leads') \
                        .update({
                            'score': scoring['score'],
                            'status': 'qualificado' if scoring['qualified'] else 'desqualificado'
                        }) \
                        .eq('id', lead_id) \
                        .execute()
                
                return {
                    "completed": True,
                    "qualified": scoring['qualified'],
                    "score": scoring['score'],
                    "breakdown": scoring.get('breakdown', {}),
                    "summary": scoring.get('summary', '')
                }
                
        except Exception as e:
            logger.error("Erro no cálculo de qualificação", error=str(e))
        
        return {
            "completed": True,
            "qualified": False,
            "score": 0,
            "breakdown": {},
            "summary": "Erro no cálculo"
        }

# Instância global
humanized_conversation_service = HumanizedConversationService()


