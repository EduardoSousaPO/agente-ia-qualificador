#!/usr/bin/env python3
"""
Serviço N8N para Workflows
"""

import os
import requests
from typing import Dict
import structlog

logger = structlog.get_logger()

class N8NService:
    def __init__(self):
        self.base_url = os.getenv('N8N_WEBHOOK_URL_INTAKE', '').replace('/webhook/intake-lead', '')
        self.api_key = os.getenv('N8N_API_KEY', '')
        
    def notify_qualified_lead(self, lead_data: Dict, score: int, answers: Dict) -> Dict:
        """Notificar consultor sobre lead qualificado"""
        try:
            # Usar URL específica para qualified-lead
            webhook_url = os.getenv('N8N_WEBHOOK_URL_QUALIFIED')
            
            if not webhook_url:
                # Fallback para URL base + endpoint
                if self.base_url:
                    webhook_url = f"{self.base_url}/webhook/qualified-lead"
                else:
                    logger.info("🔔 Simulando notificação N8N (webhook não configurado)",
                               lead_name=lead_data.get('name'),
                               score=score)
                    
                    return {
                        'success': True,
                        'message': 'Notificação simulada - N8N não configurado',
                        'simulated': True
                    }
            
            # Preparar dados para N8N
            notification_data = {
                'event': 'lead_qualified',
                'lead': {
                    'id': lead_data.get('id'),
                    'name': lead_data.get('name'),
                    'phone': lead_data.get('phone'),
                    'email': lead_data.get('email', ''),
                    'origem': lead_data.get('origem', ''),
                    'score': score,
                    'qualified_at': __import__('datetime').datetime.now().isoformat()
                },
                'qualification': {
                    'patrimonio': answers.get('patrimonio', ''),
                    'objetivo': answers.get('objetivo', ''),
                    'urgencia': answers.get('urgencia', ''),
                    'interesse': answers.get('interesse', ''),
                    'score': score,
                    'threshold': 70
                },
                'next_actions': [
                    'Entrar em contato em até 2 horas',
                    'Agendar consultoria gratuita',
                    'Preparar proposta personalizada'
                ]
            }
            
            # Enviar para N8N
            headers = {'Content-Type': 'application/json'}
            if self.api_key:
                headers['Authorization'] = f'Bearer {self.api_key}'
            
            response = requests.post(
                webhook_url,
                json=notification_data,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info("🔔 Lead qualificado notificado via N8N",
                           lead_id=lead_data.get('id'),
                           score=score,
                           webhook_url=webhook_url)
                
                return {
                    'success': True,
                    'message': 'Consultor notificado via N8N',
                    'webhook_response': response.json() if response.text else {}
                }
            else:
                logger.error("Erro ao notificar N8N",
                           status_code=response.status_code,
                           response=response.text)
                
                return {
                    'success': False,
                    'error': f'N8N webhook retornou {response.status_code}'
                }
                
        except Exception as e:
            logger.error("Erro no serviço N8N", error=str(e))
            return {
                'success': False,
                'error': str(e)
            }
    
    def send_intake_notification(self, lead_data: Dict) -> Dict:
        """Notificar sobre novo lead (intake)"""
        try:
            webhook_url = os.getenv('N8N_WEBHOOK_URL_INTAKE')
            
            if not webhook_url:
                logger.info("🔔 Simulando intake N8N (webhook não configurado)",
                           lead_name=lead_data.get('name'))
                
                return {
                    'success': True,
                    'message': 'Intake simulado - N8N não configurado',
                    'simulated': True
                }
            
            # Preparar dados para N8N
            intake_data = {
                'event': 'new_lead',
                'lead': lead_data,
                'timestamp': __import__('datetime').datetime.now().isoformat()
            }
            
            # Enviar para N8N
            headers = {'Content-Type': 'application/json'}
            if self.api_key:
                headers['Authorization'] = f'Bearer {self.api_key}'
            
            response = requests.post(
                webhook_url,
                json=intake_data,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info("🔔 Novo lead notificado via N8N",
                           lead_id=lead_data.get('id'),
                           webhook_url=webhook_url)
                
                return {
                    'success': True,
                    'message': 'Lead intake processado via N8N',
                    'webhook_response': response.json() if response.text else {}
                }
            else:
                logger.error("Erro no intake N8N",
                           status_code=response.status_code,
                           response=response.text)
                
                return {
                    'success': False,
                    'error': f'N8N intake webhook retornou {response.status_code}'
                }
                
        except Exception as e:
            logger.error("Erro no intake N8N", error=str(e))
            return {
                'success': False,
                'error': str(e)
            }

# Instância global
n8n_service = N8NService()
