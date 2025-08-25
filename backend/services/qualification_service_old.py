#!/usr/bin/env python3
"""
Serviço de Qualificação de Leads - Versão Corrigida
"""

import json
from typing import Dict, Optional
import structlog
from services.openai_service import openai_service
from services.simple_supabase import simple_supabase
from services.simple_twilio import simple_twilio
from services.n8n_service import n8n_service
# Removido simple_qualification - usando apenas OpenAI

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
        """Salvar mensagem do agente para feedback posterior (opcional)"""
        try:
            # Implementação opcional - pode ser usado para coleta de feedback
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
            
            # Gerar mensagem inicial da IA
            initial_context = session_data['context']
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
        """Processar resposta do lead - VERSÃO CORRIGIDA COM SCORING SIMPLES"""
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
            
            logger.info("Processando resposta com sistema simples", 
                       session_id=session_id,
                       current_step=current_step,
                       user_message=user_message[:50])
            
            # Processar resposta com sistema simples
            result = simple_qualification.process_user_answer(
                current_step, user_message, context
            )
            
            if not result['success']:
                return result
            
            # Atualizar contexto da sessão
            updated_context = result['context']
            
            # Salvar mensagem do usuário
            simple_supabase.create_message(session_id, 'inbound', user_message)
            
            # Preparar resposta da IA
            ai_message = result['message']
            
            # Salvar mensagem da IA
            simple_supabase.create_message(session_id, 'outbound', ai_message)
            
            # Atualizar sessão
            simple_supabase.update_session(session_id, {
                'context': updated_context,
                'current_step': updated_context.get('current_step'),
                'updated_at': 'now()'
            })
            
            # Se qualificação foi completada
            if result.get('completed', False):
                lead_id = session['lead_id']
                score = result['score']
                qualified = result['qualified']
                
                # Atualizar lead com score
                simple_supabase.update_lead(lead_id, {
                    'score': score,
                    'status': 'qualificado' if qualified else 'desqualificado',
                    'updated_at': 'now()'
                })
                
                # Finalizar sessão
                simple_supabase.update_session(session_id, {
                    'status': 'finalizada',
                    'context': updated_context
                })
                
                # Se qualificado, notificar consultor
                if qualified:
                    lead = simple_supabase.get_lead(lead_id)
                    if lead:
                        self._notify_consultant_simple(lead, score, updated_context)
                
                logger.info("Qualificação completada com sistema simples",
                           lead_id=lead_id,
                           score=score,
                           qualified=qualified)
            
            # Enviar mensagem via WhatsApp
            if session.get('leads'):
                phone = session['leads'].get('phone')
                if phone:
                    twilio_result = simple_twilio.send_message(phone, ai_message)
                    if not twilio_result.get('success'):
                        logger.warning("Falha no envio WhatsApp", 
                                     phone=phone,
                                     error=twilio_result.get('error'))
            
            return {
                'success': True,
                'message': ai_message,
                'completed': result.get('completed', False),
                'score': result.get('score'),
                'qualified': result.get('qualified')
            }
            
        except Exception as e:
            logger.error("Erro ao processar resposta do lead", 
                        session_id=session_id, 
                        error=str(e))
            return {
                'success': False,
                'error': 'Erro interno do servidor'
            }

    def _notify_consultant_simple(self, lead: Dict, score: int, context: Dict):
        """Notificar consultor sobre lead qualificado - versão simples"""
        try:
            answers = context.get('answers', {})
            
            notification_message = f"""🎯 LEAD QUALIFICADO!

👤 **Nome**: {lead.get('name', 'N/A')}
📱 **Telefone**: {lead.get('phone', 'N/A')}
📧 **Email**: {lead.get('email', 'N/A')}
📊 **Score**: {score}/100

💰 **Patrimônio**: {answers.get('patrimonio', 'N/A')}
🎯 **Objetivo**: {answers.get('objetivo', 'N/A')}
⏰ **Urgência**: {answers.get('urgencia', 'N/A')}
🤝 **Interesse**: {answers.get('interesse', 'N/A')}

🚀 **Ação**: Entrar em contato em até 2 horas!
"""
            
            # Notificar via N8N (se disponível)
            try:
                n8n_service.notify_qualified_lead({
                    'lead': lead,
                    'score': score,
                    'answers': answers,
                    'message': notification_message
                })
            except Exception as e:
                logger.warning("Falha na notificação N8N", error=str(e))
            
            logger.info("Consultor notificado", lead_id=lead['id'], score=score)
            
        except Exception as e:
            logger.error("Erro ao notificar consultor", error=str(e))

    def process_lead_response_old(self, session_id: str, user_message: str) -> Dict:
        """Processar resposta do lead durante qualificação"""
        try:
            # Buscar sessão
            session = simple_supabase.get_session(session_id)
            if not session:
                return {
                    'success': False,
                    'error': 'Sessão não encontrada'
                }
            
            # Verificar se sessão está ativa
            if session['status'] != 'ativa':
                return {
                    'success': False,
                    'error': 'Sessão não está ativa'
                }
            
            # Verificar se há takeover humano
            context = session.get('context', {})
            if context.get('human_takeover', False):
                return {
                    'success': False,
                    'error': 'Sessão sob controle humano'
                }
            
            # Salvar mensagem do usuário
            user_message_data = {
                'session_id': session_id,
                'direction': 'inbound',
                'content': user_message,
                'message_type': 'text'
            }
            
            simple_supabase.create_message(user_message_data)
            
            # Buscar tenant_id do lead
            lead = simple_supabase.get_lead(session['lead_id'])
            tenant_id = lead.get('tenant_id') if lead else None
            
            # Buscar base de conhecimento
            knowledge_context = ""
            if tenant_id:
                knowledge_context = self._get_knowledge_base_context(tenant_id)
            
            # Processar com IA (incluindo conhecimento)
            ai_response, updated_context = openai_service.process_message(
                context, user_message, knowledge_context
            )
            
            # Verificar se qualificação foi completada
            qualification_status = openai_service.get_qualification_status(updated_context)
            
            if qualification_status['completed']:
                # Qualificação completa - processar resultado
                result = self._handle_qualification_complete(
                    session, updated_context, qualification_status
                )
                
                # Personalizar resposta final
                if qualification_status['qualified']:
                    ai_response = f"""🎯 **PERFEITO!** Você está qualificado! 

Score: {qualification_status['score']}/100

Nosso especialista entrará em contato em até 2 horas para agendar sua consultoria gratuita. 

Pode ser hoje às 14h ou 16h?"""
                else:
                    ai_response = f"""Obrigado pelas respostas! 

Com base no seu perfil (Score: {qualification_status['score']}/100), recomendo que explore nosso conteúdo gratuito primeiro.

Acesse: www.exemplo.com/materiais-gratuitos

Quando estiver pronto para investir mais, estaremos aqui! 😊"""
            
            # Enviar resposta da IA
            phone = session['leads']['phone']
            send_result = simple_twilio.send_message(phone, ai_response)
            
            if send_result['success']:
                # Salvar resposta da IA
                ai_message_data = {
                    'session_id': session_id,
                    'direction': 'outbound',
                    'content': ai_response,
                    'message_type': 'text',
                    'twilio_sid': send_result.get('message_sid')
                }
                
                simple_supabase.create_message(ai_message_data)
                
                # Salvar mensagem do agente para feedback (opcional)
                if tenant_id:
                    self._save_agent_message_for_feedback(session_id, ai_response, tenant_id)
                
                # Atualizar sessão
                simple_supabase.update_session(session_id, {
                    'context': updated_context,
                    'current_step': updated_context.get('current_step')
                })
                
                logger.info("Resposta processada", 
                           session_id=session_id,
                           step=updated_context.get('current_step'),
                           qualified=qualification_status.get('qualified'))
                
                return {
                    'success': True,
                    'ai_response': ai_response,
                    'qualification_status': qualification_status,
                    'session_updated': True
                }
            else:
                logger.error("Falha ao enviar resposta da IA", 
                           session_id=session_id,
                           error=send_result.get('error'))
                return {
                    'success': False,
                    'error': 'Falha ao enviar resposta'
                }
                
        except Exception as e:
            logger.error("Erro ao processar resposta do lead", 
                        session_id=session_id, 
                        error=str(e))
            return {
                'success': False,
                'error': 'Erro interno do servidor'
            }

    def _handle_qualification_complete(self, session: Dict, 
                                           context: Dict, 
                                           status: Dict) -> Dict:
        """Processar qualificação completa"""
        try:
            lead_id = session['lead_id']
            score = status['score']
            qualified = status['qualified']
            
            # Atualizar lead com score e status
            lead_update = {
                'score': score,
                'status': 'qualificado' if qualified else 'desqualificado',
                'qualification_completed_at': 'now()'
            }
            
            simple_supabase.update_lead(lead_id, lead_update)
            
            # Finalizar sessão
            simple_supabase.update_session(session['id'], {
                'status': 'finalizada',
                'context': context
            })
            
            # Se qualificado, notificar consultor
            if qualified:
                self._notify_consultant(session['leads'], score, context)
            
            logger.info("Qualificação finalizada", 
                       lead_id=lead_id,
                       score=score,
                       qualified=qualified)
            
            return {
                'success': True,
                'qualified': qualified,
                'score': score
            }
            
        except Exception as e:
            logger.error("Erro ao finalizar qualificação", error=str(e))
            return {
                'success': False,
                'error': 'Erro ao finalizar qualificação'
            }

    def _notify_consultant(self, lead: Dict, score: int, context: Dict):
        """Notificar consultor sobre lead qualificado"""
        try:
            answers = context.get('answers', {})
            
            # Notificar via N8N
            result = n8n_service.notify_qualified_lead(lead, score, answers)
            
            if result['success']:
                logger.info("🎯 CONSULTOR NOTIFICADO COM SUCESSO",
                           lead_name=lead['name'],
                           score=score,
                           via_n8n=not result.get('simulated', False))
            else:
                logger.error("Falha ao notificar consultor via N8N",
                           error=result.get('error'))
            
            # Log detalhado para acompanhamento
            notification_data = {
                'lead_name': lead['name'],
                'lead_phone': lead['phone'],
                'lead_email': lead.get('email', 'N/A'),
                'score': score,
                'patrimonio': answers.get('patrimonio', 'N/A'),
                'objetivo': answers.get('objetivo', 'N/A'),
                'urgencia': answers.get('urgencia', 'N/A'),
                'interesse': answers.get('interesse', 'N/A'),
                'notification_status': 'success' if result['success'] else 'failed'
            }
            
            logger.info("🎯 LEAD QUALIFICADO - Detalhes da Notificação", 
                       **notification_data)
            
        except Exception as e:
            logger.error("Erro ao notificar consultor", error=str(e))

    def get_qualification_criteria(self) -> Dict:
        """Obter critérios de qualificação"""
        return {
            'threshold': self.qualification_threshold,
            'scoring': {
                'patrimonio': {
                    'ate_50k': 10,
                    '50k_200k': 20,
                    '200k_500k': 25,
                    'acima_500k': 30
                },
                'objetivo': {
                    'aposentadoria': 25,
                    'crescimento': 20,
                    'reserva': 15,
                    'especulacao': 10
                },
                'urgencia': {
                    'esta_semana': 25,
                    'este_mes': 20,
                    'tres_meses': 15,
                    'sem_pressa': 5
                },
                'interesse': {
                    'sim_urgente': 20,
                    'sim_possivel': 15,
                    'talvez': 10,
                    'nao': 0
                }
            }
        }

# Instância global do serviço
qualification_service = QualificationService()
