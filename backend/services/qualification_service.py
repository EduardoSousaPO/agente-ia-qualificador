#!/usr/bin/env python3
"""
Serviço de Qualificação de Leads - UNIFICADO (OpenAI-only)
"""

import json
from typing import Dict, Optional
import structlog
from services.openai_service import get_openai_service
from services.simple_supabase import simple_supabase
from services.simple_twilio import simple_twilio
from services.n8n_service import n8n_service

logger = structlog.get_logger()

class QualificationService:
    def __init__(self):
        """Inicializar serviço de qualificação"""
        self.qualification_threshold = 70  # Score mínimo para qualificação
    
    def _get_knowledge_base_context(self, tenant_id: str) -> str:
        """Buscar base de conhecimento do tenant"""
        try:
            result = simple_supabase.client.table('knowledge_base') \
                .select('content') \
                .eq('tenant_id', tenant_id) \
                .execute()
            
            if result.data:
                return result.data[0]['content']
            return ""
            
        except Exception as e:
            logger.error("Erro ao buscar base de conhecimento", 
                        tenant_id=tenant_id, error=str(e))
            return ""
    
    def _inject_knowledge_in_prompt(self, base_prompt: str, knowledge: str) -> str:
        """Injetar conhecimento no prompt da IA"""
        if not knowledge.strip():
            return base_prompt
        
        return f"""
CONTEXTO DA EMPRESA:
{knowledge}

FLUXO OBRIGATÓRIO:
{base_prompt}

IMPORTANTE: Use o contexto da empresa para responder dúvidas específicas, mas SEMPRE mantenha o fluxo de 4 perguntas obrigatórias.
"""
    
    def _save_agent_message_for_feedback(self, session_id: str, agent_message: str, tenant_id: str):
        """Salvar mensagem do agente para feedback posterior"""
        try:
            logger.info("Mensagem do agente salva para feedback", 
                       session_id=session_id, 
                       message_length=len(agent_message))
        except Exception as e:
            logger.error("Erro ao salvar mensagem para feedback", error=str(e))
    
    def start_qualification(self, lead_id: str, phone: str) -> Dict:
        """Iniciar processo de qualificação para um lead"""
        try:
            # Criar nova sessão
            session_data = {
                'lead_id': lead_id,
                'status': 'ativa',
                'current_step': 'inicio',
                'context': {
                    'qualification_started': True,
                    'answers': {},
                    'conversation_history': [],
                    'phone': phone
                }
            }
            
            session = simple_supabase.create_session(session_data)
            session_id = session['id']
            
            # Mensagem inicial padronizada
            initial_message = """Olá! 👋 

Vi que você tem interesse em investimentos. Para te conectar com o melhor especialista, preciso fazer algumas perguntas rápidas. Tudo bem?

Primeira pergunta: Quanto você tem disponível para investir hoje?

A) Até R$ 50 mil
B) R$ 50 mil a R$ 200 mil  
C) R$ 200 mil a R$ 500 mil
D) Mais de R$ 500 mil"""

            # Enviar mensagem inicial
            send_result = simple_twilio.send_message(phone, initial_message)
            
            if send_result['success']:
                # Salvar mensagem no banco
                message_data = {
                    'session_id': session_id,
                    'direction': 'outbound',
                    'content': initial_message,
                    'message_type': 'text',
                    'twilio_sid': send_result.get('message_sid')
                }
                
                simple_supabase.create_message(message_data)
                
                # Atualizar contexto da sessão
                initial_context = session_data['context']
                initial_context['conversation_history'].append({
                    "role": "assistant",
                    "content": initial_message
                })
                initial_context['current_step'] = 'patrimonio'
                
                simple_supabase.update_session(session_id, {
                    'context': initial_context
                })
                
                logger.info("Qualificação iniciada", 
                           lead_id=lead_id, 
                           session_id=session_id)
                
                return {
                    'success': True,
                    'session_id': session_id,
                    'message': 'Qualificação iniciada com sucesso'
                }
            else:
                logger.error("Falha ao enviar mensagem inicial", 
                           lead_id=lead_id, 
                           error=send_result.get('error'))
                return {
                    'success': False,
                    'error': 'Falha ao enviar mensagem inicial'
                }
                
        except Exception as e:
            logger.error("Erro ao iniciar qualificação", 
                        lead_id=lead_id, 
                        error=str(e))
            return {
                'success': False,
                'error': 'Erro interno do servidor'
            }

    def process_lead_response(self, session_id: str, user_message: str) -> Dict:
        """Processar resposta do lead usando APENAS OpenAI (UNIFICADO)"""
        try:
            # Buscar sessão
            session = simple_supabase.get_session(session_id)
            if not session:
                return {
                    'success': False,
                    'error': 'Sessão não encontrada'
                }
            
            # Obter contexto da sessão
            context = session.get('context', {})
            current_step = context.get('current_step', 'patrimonio')
            answers = context.get('answers', {})
            
            logger.info("Processando resposta com OpenAI unificado", 
                       session_id=session_id,
                       current_step=current_step,
                       user_message=user_message[:50])
            
            # Extrair resposta usando OpenAI
            openai_service = get_openai_service()
            extracted_answer = openai_service.extract_qualification_answer(user_message)
            option = extracted_answer.get('option', '')
            
            # Processar baseado no step atual
            ai_message = ""
            next_step = current_step
            completed = False
            final_score = 0
            qualified = False

            if current_step == 'patrimonio':
                if option in ['A', 'B', 'C', 'D']:
                    answers['patrimonio'] = option
                    next_step = 'objetivo'
                    ai_message = "Ótimo, obrigado pela resposta! \n\nAgora, vamos para a segunda pergunta: Qual seu principal objetivo com os investimentos? \n\nA) Aposentadoria \nB) Crescimento \nC) Reserva \nD) Especulação"
                else:
                    ai_message = "Não entendi sua resposta sobre patrimônio. Por favor, escolha uma das opções (A, B, C ou D) ou descreva o valor. \n\nQuanto você tem disponível para investir hoje? \n\nA) Até R$ 50 mil\nB) R$ 50 mil a R$ 200 mil  \nC) R$ 200 mil a R$ 500 mil\nD) Mais de R$ 500 mil"

            elif current_step == 'objetivo':
                if option in ['A', 'B', 'C', 'D']:
                    answers['objetivo'] = option
                    next_step = 'urgencia'
                    ai_message = "Perfeito! Agora, a terceira pergunta: Quando pretende começar a investir? \n\nA) Esta semana \nB) Este mês \nC) Em 3 meses \nD) Sem pressa"
                else:
                    ai_message = "Não entendi seu objetivo. Por favor, escolha uma das opções (A, B, C ou D). \n\nQual seu principal objetivo com os investimentos? \n\nA) Aposentadoria \nB) Crescimento \nC) Reserva \nD) Especulação"

            elif current_step == 'urgencia':
                if option in ['A', 'B', 'C', 'D']:
                    answers['urgencia'] = option
                    next_step = 'interesse'
                    ai_message = "Excelente! Por último, gostaria de saber: você gostaria de falar com um de nossos especialistas? \n\nA) Sim, urgente \nB) Sim, quando possível \nC) Talvez \nD) Não"
                else:
                    ai_message = "Não entendi sua urgência. Por favor, escolha uma das opções (A, B, C ou D). \n\nQuando pretende começar a investir? \n\nA) Esta semana \nB) Este mês \nC) Em 3 meses \nD) Sem pressa"

            elif current_step == 'interesse':
                if option in ['A', 'B', 'C', 'D']:
                    answers['interesse'] = option
                    
                    # Calcular score final usando OpenAI (ÚNICA FONTE DA VERDADE)
                    final_score = openai_service.calculate_lead_score(answers)
                    qualified = openai_service.is_qualified(final_score)
                    
                    completed = True
                    next_step = 'qualificacao_completa'
                    
                    if qualified:
                        ai_message = f"QUALIFICACAO_COMPLETA: {final_score}. Parabéns! Você está qualificado para falar com um de nossos especialistas. Em breve entraremos em contato para agendar sua reunião."
                    else:
                        ai_message = f"QUALIFICACAO_COMPLETA: {final_score}. Agradecemos suas respostas. No momento, nossos serviços são mais adequados para outro perfil de investidor. Mas fique à vontade para nos procurar no futuro!"
                else:
                    ai_message = "Não entendi seu interesse. Por favor, escolha uma das opções (A, B, C ou D). \n\nGostaria de falar com um de nossos especialistas? \n\nA) Sim, urgente \nB) Sim, quando possível \nC) Talvez \nD) Não"

            elif current_step == 'inicio':  # Primeiro contato
                next_step = 'patrimonio'
                ai_message = """Olá! 👋 

Vi que você tem interesse em investimentos. Para te conectar com o melhor especialista, preciso fazer algumas perguntas rápidas. Tudo bem?

Primeira pergunta: Quanto você tem disponível para investir hoje?

A) Até R$ 50 mil
B) R$ 50 mil a R$ 200 mil  
C) R$ 200 mil a R$ 500 mil
D) Mais de R$ 500 mil"""
                context['qualification_started'] = True

            # Atualizar histórico de conversa
            conversation_history = context.get('conversation_history', [])
            conversation_history.append({"role": "user", "content": user_message})
            conversation_history.append({"role": "assistant", "content": ai_message})

            # Salvar mensagens no banco
            simple_supabase.create_message(session_id, 'inbound', user_message)
            simple_supabase.create_message(session_id, 'outbound', ai_message)

            # Atualizar contexto da sessão
            updated_context = {
                'answers': answers,
                'current_step': next_step,
                'conversation_history': conversation_history,
                'qualification_started': context.get('qualification_started', False),
                'phone': context.get('phone')
            }

            simple_supabase.update_session(session_id, {
                'context': updated_context,
                'current_step': next_step
            })

            # Enviar mensagem via WhatsApp
            send_result = simple_twilio.send_message(context.get('phone'), ai_message)

            # Se qualificação foi completada
            if completed:
                lead_id = session['lead_id']
                
                # Atualizar score do lead
                simple_supabase.update_lead(lead_id, {
                    'score': final_score,
                    'status': 'qualificado' if qualified else 'desqualificado'
                })

                # Notificar consultor se qualificado
                if qualified:
                    lead_data = simple_supabase.get_lead(lead_id)
                    self._notify_consultant(lead_data, final_score)

                logger.info("Qualificação completada (OpenAI-only)", 
                           session_id=session_id,
                           lead_id=lead_id,
                           final_score=final_score,
                           qualified=qualified)

            return {
                'success': True,
                'message': ai_message,
                'context': updated_context,
                'completed': completed,
                'score': final_score,
                'qualified': qualified,
                'send_success': send_result.get('success', False)
            }

        except Exception as e:
            logger.error("Erro ao processar resposta do lead", 
                        session_id=session_id, 
                        error=str(e))
            return {
                'success': False,
                'error': 'Erro interno do servidor'
            }

    def _notify_consultant(self, lead_data: Dict, score: int) -> bool:
        """Notificar consultor sobre lead qualificado via webhook local"""
        try:
            # Preparar payload para webhook local (que dispara email + CRM)
            payload = {
                'tenant_id': lead_data.get('tenant_id', '60675861-e22a-4990-bab8-65ed07632a63'),  # Tenant demo
                'lead': {
                    'id': lead_data['id'],
                    'name': lead_data['name'],
                    'email': lead_data.get('email', 'Não informado'),
                    'phone': lead_data['phone'],
                    'score': score,
                    'origem': lead_data.get('origem', 'WhatsApp'),
                    'created_at': lead_data.get('created_at')
                }
            }

            # Chamar webhook local diretamente (mais confiável que N8N externo)
            import requests
            
            webhook_url = 'http://localhost:5000/api/hooks/qualified-lead'
            
            response = requests.post(
                webhook_url,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            if response.status_code == 200:
                result_data = response.json()
                logger.info("Consultor notificado via webhook local", 
                           lead_id=lead_data['id'], 
                           score=score,
                           email_success=result_data.get('results', {}).get('email', {}).get('success', False),
                           crm_success=result_data.get('results', {}).get('crm', {}).get('success', False))
                return True
            else:
                logger.error("Falha no webhook de notificação", 
                           lead_id=lead_data['id'], 
                           status_code=response.status_code,
                           response=response.text[:200])
                return False

        except Exception as e:
            logger.error("Erro ao notificar consultor", 
                        lead_id=lead_data.get('id'), 
                        error=str(e))
            return False

# Instância global
qualification_service = QualificationService()
