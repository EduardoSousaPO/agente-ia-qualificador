#!/usr/bin/env python3
"""
Serviço de Qualificação de Leads - HUMANIZADO
Agora com conversação natural e fluida
"""

import json
from typing import Dict, Optional
import structlog
from services.openai_service import get_openai_service
from services.simple_supabase import simple_supabase
from services.simple_twilio import simple_twilio
from services.humanized_conversation_service import humanized_conversation_service
# from services.n8n_service import n8n_service  # REMOVIDO - N8N substituído por backend direto

logger = structlog.get_logger()

class QualificationService:
    def __init__(self):
        """Inicializar serviço de qualificação"""
        self.qualification_threshold = 70  # Score mínimo para qualificação
        self.use_humanized_conversation = True  # Flag para ativar conversação humanizada
    
    def _get_knowledge_base_context(self, tenant_id: str) -> str:
        """Buscar base de conhecimento do tenant"""
        try:
            # Garantir que o cliente está inicializado
            simple_supabase._ensure_client()
            
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
            
            # Buscar base de conhecimento do tenant
            tenant_id = '05dc8c52-c0a0-44ae-aa2a-eeaa01090a27'  # Default para demo
            knowledge_context = self._get_knowledge_base_context(tenant_id)
            
            # Mensagem inicial personalizada com base de conhecimento
            base_initial_message = """Olá! 👋 

Vi que você tem interesse em investimentos. Para te conectar com o melhor especialista, preciso fazer algumas perguntas rápidas. Tudo bem?

Primeira pergunta: Quanto você tem disponível para investir hoje?

A) Até R$ 50 mil
B) R$ 50 mil a R$ 200 mil  
C) R$ 200 mil a R$ 500 mil
D) Mais de R$ 500 mil"""
            
            initial_message = self._inject_knowledge_in_prompt(base_initial_message, knowledge_context)

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
        """
        Processar resposta do lead - VERSÃO HUMANIZADA
        Usa conversação natural em vez de perguntas robóticas
        """
        try:
            # Verificar se deve usar conversação humanizada
            if self.use_humanized_conversation:
                logger.info("Processando com conversação humanizada", 
                           session_id=session_id,
                           user_message=user_message[:50])
                
                # Buscar tenant_id da sessão
                session_result = simple_supabase.client.table('sessions') \
                    .select('*, leads(tenant_id)') \
                    .eq('id', session_id) \
                    .execute()
                
                tenant_id = None
                if session_result.data and session_result.data[0]['leads']:
                    tenant_id = session_result.data[0]['leads']['tenant_id']
                
                # Usar serviço de conversação humanizada
                return humanized_conversation_service.process_natural_conversation(
                    session_id, user_message, tenant_id
                )
            
            return self._process_robotic_conversation(session_id, user_message)
            
        except Exception as e:
            logger.error("Erro no processamento de resposta", 
                        session_id=session_id, error=str(e))
            return {
                "success": False,
                "error": "Erro interno do servidor",
                "message": "Desculpe, houve um problema. Pode repetir sua mensagem?"
            }
    
    def _process_robotic_conversation(self, session_id: str, user_message: str) -> Dict:
        try:
            # Buscar sessão
            session = simple_supabase.get_session(session_id)
            if not session:
                return {
                    'success': False,
                    'error': 'Sessão não encontrada'
                }
            
            # Buscar base de conhecimento do tenant
            lead = session.get('leads', {})
            tenant_id = lead.get('tenant_id', '05dc8c52-c0a0-44ae-aa2a-eeaa01090a27')  # Default para demo
            knowledge_context = self._get_knowledge_base_context(tenant_id)
            
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
            simple_supabase.create_message({
                'session_id': session_id,
                'direction': 'inbound',
                'content': user_message,
                'message_type': 'text'
            })
            simple_supabase.create_message({
                'session_id': session_id,
                'direction': 'outbound',
                'content': ai_message,
                'message_type': 'text'
            })

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

                # Notificar consultor se qualificado (DIRETO - sem N8N)
                if qualified:
                    from services.notification_service import notification_service
                    lead_data = simple_supabase.get_lead(lead_id)
                    notification_service.notify_qualified_lead(lead_data, final_score, updated_context)

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
        """Notificar consultor sobre lead qualificado (DIRETO - sem N8N)"""
        try:
            from services.email_service import email_service
            from services.crm_adapter import crm_adapter
            
            tenant_id = lead_data.get('tenant_id', '05dc8c52-c0a0-44ae-aa2a-eeaa01090a27')
            
            # Buscar configurações do tenant
            tenant_result = simple_supabase.client.table('tenants') \
                .select('settings') \
                .eq('id', tenant_id) \
                .single() \
                .execute()
            
            tenant_settings = tenant_result.data.get('settings', {}) if tenant_result.data else {}
            consultant_email = tenant_settings.get('default_consultant_email', 'consultor@exemplo.com')
            
            # Preparar dados para notificação
            notification_payload = {
                'lead_id': lead_data['id'],
                'name': lead_data['name'],
                'email': lead_data.get('email', 'Não informado'),
                'phone': lead_data['phone'],
                'score': score,
                'status': 'qualificado',
                'origem': 'WhatsApp',
                'created_at': lead_data.get('created_at'),
                'qualified_at': __import__('datetime').datetime.now().isoformat()
            }
            
            # 1. Enviar email para consultor (DIRETO)
            email_result = email_service.send_qualified_lead_email(
                lead_data=notification_payload,
                consultant_email=consultant_email
            )
            
            # 2. Enviar para CRM (DIRETO)
            crm_result = crm_adapter.send_lead(
                tenant_id=tenant_id,
                lead_payload=notification_payload
            )
            
            # 3. Atualizar lead no banco
            simple_supabase.client.table('leads') \
                .update({
                    'status': 'qualificado',
                    'score': score,
                    'qualified_at': notification_payload['qualified_at']
                }) \
                .eq('id', lead_data['id']) \
                .execute()
            
            email_success = email_result.get('success', False)
            crm_success = crm_result.get('success', False) or crm_result.get('skipped', False)
            
            logger.info("Consultor notificado DIRETAMENTE (sem N8N)", 
                       lead_id=lead_data['id'], 
                       score=score,
                       email_success=email_success,
                       crm_success=crm_success)
            
            return email_success and crm_success

        except Exception as e:
            logger.error("Erro ao notificar consultor", 
                        lead_id=lead_data.get('id'), 
                        error=str(e))
            return False

# Instância global
qualification_service = QualificationService()
