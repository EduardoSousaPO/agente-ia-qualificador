#!/usr/bin/env python3
"""
Serviço de Notificações - Substituindo N8N
Gerencia todas as notificações do sistema (email, Slack, CRM, etc.)
"""

import os
from typing import Dict, List, Optional
import structlog
from services.email_service import email_service
from services.crm_adapter import crm_adapter
from services.simple_supabase import simple_supabase

logger = structlog.get_logger()

class NotificationService:
    def __init__(self):
        """Inicializar serviço de notificações"""
        self.default_consultant_email = 'consultor@exemplo.com'
    
    def notify_qualified_lead(self, lead_data: Dict, score: int, context: Dict = None) -> Dict:
        """
        Notificar sobre lead qualificado
        Substitui completamente o workflow N8N de notificação
        """
        try:
            tenant_id = lead_data.get('tenant_id', '05dc8c52-c0a0-44ae-aa2a-eeaa01090a27')
            
            # Buscar configurações do tenant
            tenant_settings = self._get_tenant_settings(tenant_id)
            
            # Preparar dados da notificação
            notification_data = self._prepare_notification_data(lead_data, score, context)
            
            results = {}
            
            # 1. Notificação por Email
            if tenant_settings.get('notification_config', {}).get('qualified_lead_email', True):
                email_result = self._send_email_notification(notification_data, tenant_settings)
                results['email'] = email_result
            
            # 2. Notificação Slack (se configurado)
            if tenant_settings.get('notification_config', {}).get('qualified_lead_slack', False):
                slack_result = self._send_slack_notification(notification_data, tenant_settings)
                results['slack'] = slack_result
            
            # 3. Integração CRM
            crm_result = self._send_crm_notification(notification_data, tenant_id)
            results['crm'] = crm_result
            
            # 4. Atualizar lead no banco
            update_result = self._update_lead_status(lead_data['id'], score, notification_data['qualified_at'])
            results['database'] = update_result
            
            # 5. Salvar evento de auditoria
            self._save_audit_event(tenant_id, lead_data['id'], 'lead_qualified', {
                'score': score,
                'notification_results': results,
                'context': context
            })
            
            # Determinar sucesso geral
            email_success = results.get('email', {}).get('success', False)
            crm_success = results.get('crm', {}).get('success', False) or results.get('crm', {}).get('skipped', False)
            db_success = results.get('database', {}).get('success', False)
            
            overall_success = email_success and crm_success and db_success
            
            logger.info("Lead qualificado notificado (DIRETO - sem N8N)", 
                       lead_id=lead_data['id'],
                       tenant_id=tenant_id,
                       score=score,
                       email_success=email_success,
                       crm_success=crm_success,
                       db_success=db_success,
                       overall_success=overall_success)
            
            return {
                'success': overall_success,
                'message': 'Notificações processadas',
                'results': results,
                'lead_id': lead_data['id'],
                'score': score
            }
            
        except Exception as e:
            logger.error("Erro no serviço de notificações", 
                        lead_id=lead_data.get('id'), 
                        error=str(e))
            return {
                'success': False,
                'error': str(e),
                'results': {}
            }
    
    def notify_new_lead(self, lead_data: Dict) -> Dict:
        """
        Notificar sobre novo lead (intake)
        Substitui o workflow N8N de intake
        """
        try:
            tenant_id = lead_data.get('tenant_id', '05dc8c52-c0a0-44ae-aa2a-eeaa01090a27')
            
            # Buscar configurações do tenant
            tenant_settings = self._get_tenant_settings(tenant_id)
            
            results = {}
            
            # 1. Salvar no CRM (se configurado)
            if tenant_settings.get('crm_config', {}).get('auto_intake', True):
                crm_result = crm_adapter.send_lead(tenant_id, lead_data)
                results['crm'] = crm_result
            
            # 2. Notificação de intake (se configurado)
            if tenant_settings.get('notification_config', {}).get('new_lead_notification', False):
                email_result = self._send_intake_email(lead_data, tenant_settings)
                results['email'] = email_result
            
            # 3. Salvar evento de auditoria
            self._save_audit_event(tenant_id, lead_data.get('id'), 'lead_intake', {
                'origem': lead_data.get('origem'),
                'notification_results': results
            })
            
            logger.info("Novo lead notificado (intake direto)", 
                       lead_id=lead_data.get('id'),
                       tenant_id=tenant_id,
                       origem=lead_data.get('origem'))
            
            return {
                'success': True,
                'message': 'Lead intake processado',
                'results': results
            }
            
        except Exception as e:
            logger.error("Erro no intake de lead", 
                        lead_id=lead_data.get('id'), 
                        error=str(e))
            return {
                'success': False,
                'error': str(e)
            }
    
    def send_daily_summary(self, tenant_id: str) -> Dict:
        """
        Enviar resumo diário de atividades
        Substitui workflow N8N de relatórios
        """
        try:
            # Buscar estatísticas do dia
            stats = self._get_daily_stats(tenant_id)
            
            # Buscar configurações do tenant
            tenant_settings = self._get_tenant_settings(tenant_id)
            
            if not tenant_settings.get('notification_config', {}).get('daily_summary', False):
                return {
                    'success': True,
                    'message': 'Resumo diário desabilitado',
                    'skipped': True
                }
            
            # Enviar email com resumo
            consultant_email = tenant_settings.get('default_consultant_email', self.default_consultant_email)
            
            email_result = email_service.send_daily_summary_email(
                stats=stats,
                consultant_email=consultant_email,
                tenant_id=tenant_id
            )
            
            logger.info("Resumo diário enviado", 
                       tenant_id=tenant_id,
                       email_success=email_result.get('success', False))
            
            return email_result
            
        except Exception as e:
            logger.error("Erro ao enviar resumo diário", 
                        tenant_id=tenant_id, 
                        error=str(e))
            return {
                'success': False,
                'error': str(e)
            }
    
    def _get_tenant_settings(self, tenant_id: str) -> Dict:
        """Buscar configurações do tenant"""
        try:
            result = simple_supabase.client.table('tenants') \
                .select('settings') \
                .eq('id', tenant_id) \
                .single() \
                .execute()
            
            if result.data:
                return result.data.get('settings', {})
            
            return {}
            
        except Exception as e:
            logger.error("Erro ao buscar configurações do tenant", 
                        tenant_id=tenant_id, 
                        error=str(e))
            return {}
    
    def _prepare_notification_data(self, lead_data: Dict, score: int, context: Dict = None) -> Dict:
        """Preparar dados para notificação"""
        return {
            'lead_id': lead_data['id'],
            'name': lead_data['name'],
            'email': lead_data.get('email', 'Não informado'),
            'phone': lead_data['phone'],
            'score': score,
            'status': 'qualificado',
            'origem': lead_data.get('origem', 'WhatsApp'),
            'created_at': lead_data.get('created_at'),
            'qualified_at': __import__('datetime').datetime.now().isoformat(),
            'answers': context.get('answers', {}) if context else {},
            'conversation_summary': self._generate_conversation_summary(context) if context else ''
        }
    
    def _generate_conversation_summary(self, context: Dict) -> str:
        """Gerar resumo da conversa"""
        try:
            answers = context.get('answers', {})
            
            # Mapear respostas para texto legível
            patrimonio_map = {
                'A': 'Até R$ 50 mil',
                'B': 'R$ 50 mil a R$ 200 mil',
                'C': 'R$ 200 mil a R$ 500 mil',
                'D': 'Mais de R$ 500 mil'
            }
            
            objetivo_map = {
                'A': 'Aposentadoria',
                'B': 'Crescimento',
                'C': 'Reserva',
                'D': 'Especulação'
            }
            
            urgencia_map = {
                'A': 'Esta semana',
                'B': 'Este mês',
                'C': 'Em 3 meses',
                'D': 'Sem pressa'
            }
            
            interesse_map = {
                'A': 'Sim, urgente',
                'B': 'Sim, quando possível',
                'C': 'Talvez',
                'D': 'Não'
            }
            
            summary_parts = []
            
            if answers.get('patrimonio'):
                summary_parts.append(f"Patrimônio: {patrimonio_map.get(answers['patrimonio'], answers['patrimonio'])}")
            
            if answers.get('objetivo'):
                summary_parts.append(f"Objetivo: {objetivo_map.get(answers['objetivo'], answers['objetivo'])}")
            
            if answers.get('urgencia'):
                summary_parts.append(f"Urgência: {urgencia_map.get(answers['urgencia'], answers['urgencia'])}")
            
            if answers.get('interesse'):
                summary_parts.append(f"Interesse: {interesse_map.get(answers['interesse'], answers['interesse'])}")
            
            return " | ".join(summary_parts)
            
        except Exception as e:
            logger.error("Erro ao gerar resumo da conversa", error=str(e))
            return "Resumo não disponível"
    
    def _send_email_notification(self, notification_data: Dict, tenant_settings: Dict) -> Dict:
        """Enviar notificação por email"""
        try:
            consultant_email = tenant_settings.get('default_consultant_email', self.default_consultant_email)
            
            return email_service.send_qualified_lead_email(
                lead_data=notification_data,
                consultant_email=consultant_email
            )
            
        except Exception as e:
            logger.error("Erro ao enviar email de notificação", error=str(e))
            return {
                'success': False,
                'error': str(e)
            }
    
    def _send_slack_notification(self, notification_data: Dict, tenant_settings: Dict) -> Dict:
        """Enviar notificação Slack (placeholder)"""
        try:
            slack_webhook = tenant_settings.get('slack_config', {}).get('webhook_url')
            
            if not slack_webhook:
                return {
                    'success': True,
                    'message': 'Slack não configurado',
                    'skipped': True
                }
            
            # TODO: Implementar integração Slack real
            logger.info("Slack notification (simulado)", 
                       lead_id=notification_data['lead_id'])
            
            return {
                'success': True,
                'message': 'Notificação Slack simulada',
            }
            
        except Exception as e:
            logger.error("Erro ao enviar notificação Slack", error=str(e))
            return {
                'success': False,
                'error': str(e)
            }
    
    def _send_crm_notification(self, notification_data: Dict, tenant_id: str) -> Dict:
        """Enviar para CRM"""
        try:
            return crm_adapter.send_lead(tenant_id, notification_data)
            
        except Exception as e:
            logger.error("Erro ao enviar para CRM", error=str(e))
            return {
                'success': False,
                'error': str(e)
            }
    
    def _send_intake_email(self, lead_data: Dict, tenant_settings: Dict) -> Dict:
        """Enviar email de intake"""
        try:
            consultant_email = tenant_settings.get('default_consultant_email', self.default_consultant_email)
            
            return email_service.send_new_lead_email(
                lead_data=lead_data,
                consultant_email=consultant_email
            )
            
        except Exception as e:
            logger.error("Erro ao enviar email de intake", error=str(e))
            return {
                'success': False,
                'error': str(e)
            }
    
    def _update_lead_status(self, lead_id: str, score: int, qualified_at: str) -> Dict:
        """Atualizar status do lead no banco"""
        try:
            simple_supabase.client.table('leads') \
                .update({
                    'status': 'qualificado',
                    'score': score,
                    'qualified_at': qualified_at
                }) \
                .eq('id', lead_id) \
                .execute()
            
            return {
                'success': True,
                'message': 'Lead atualizado no banco'
            }
            
        except Exception as e:
            logger.error("Erro ao atualizar lead", lead_id=lead_id, error=str(e))
            return {
                'success': False,
                'error': str(e)
            }
    
    def _save_audit_event(self, tenant_id: str, lead_id: str, event_type: str, event_data: Dict):
        """Salvar evento de auditoria"""
        try:
            audit_data = {
                'tenant_id': tenant_id,
                'lead_id': lead_id,
                'event_type': event_type,
                'event_data': event_data,
                'created_at': __import__('datetime').datetime.now().isoformat(),
                'source': 'notification_service'
            }
            
            simple_supabase.client.table('audit_events') \
                .insert(audit_data) \
                .execute()
            
            logger.debug("Evento de auditoria salvo", 
                        tenant_id=tenant_id,
                        lead_id=lead_id,
                        event_type=event_type)
            
        except Exception as e:
            logger.error("Erro ao salvar evento de auditoria", 
                        tenant_id=tenant_id,
                        lead_id=lead_id,
                        error=str(e))
    
    def _get_daily_stats(self, tenant_id: str) -> Dict:
        """Buscar estatísticas do dia"""
        try:
            from datetime import datetime, timedelta
            
            today = datetime.now().date()
            yesterday = today - timedelta(days=1)
            
            # Buscar leads de hoje
            today_leads_result = simple_supabase.client.table('leads') \
                .select('*') \
                .eq('tenant_id', tenant_id) \
                .gte('created_at', today.isoformat()) \
                .execute()
            
            today_leads = today_leads_result.data or []
            
            # Calcular estatísticas
            total_leads = len(today_leads)
            qualified_leads = [lead for lead in today_leads if lead.get('score', 0) >= 70]
            qualified_count = len(qualified_leads)
            
            # Score médio
            avg_score = sum(lead.get('score', 0) for lead in today_leads) / total_leads if total_leads > 0 else 0
            
            return {
                'date': today.isoformat(),
                'total_leads': total_leads,
                'qualified_leads': qualified_count,
                'qualification_rate': (qualified_count / total_leads * 100) if total_leads > 0 else 0,
                'avg_score': round(avg_score, 1),
                'top_sources': self._get_top_sources(today_leads),
                'recent_qualified': qualified_leads[:5]
            }
            
        except Exception as e:
            logger.error("Erro ao buscar estatísticas diárias", 
                        tenant_id=tenant_id, 
                        error=str(e))
            return {
                'date': datetime.now().date().isoformat(),
                'total_leads': 0,
                'qualified_leads': 0,
                'qualification_rate': 0,
                'avg_score': 0,
                'top_sources': [],
                'recent_qualified': []
            }
    
    def _get_top_sources(self, leads: List[Dict]) -> List[Dict]:
        """Obter principais fontes de leads"""
        try:
            sources = {}
            for lead in leads:
                origem = lead.get('origem', 'Desconhecido')
                sources[origem] = sources.get(origem, 0) + 1
            
            # Ordenar por quantidade
            sorted_sources = sorted(sources.items(), key=lambda x: x[1], reverse=True)
            
            return [
                {'source': source, 'count': count}
                for source, count in sorted_sources[:5]
            ]
            
        except Exception as e:
            logger.error("Erro ao calcular top sources", error=str(e))
            return []

# Instância global
notification_service = NotificationService()
