#!/usr/bin/env python3
"""
Serviço Twilio Simplificado (Síncrono)
"""

import os
from typing import Dict
import structlog

logger = structlog.get_logger()

class SimpleTwilioService:
    def __init__(self):
        self.use_simulator = os.getenv('USE_WHATSAPP_SIMULATOR', 'true').lower() == 'true'
        
    def send_message(self, to_phone: str, message: str) -> Dict:
        """Enviar mensagem WhatsApp"""
        try:
            if self.use_simulator:
                # Simular envio
                logger.info("📱 Simulando envio WhatsApp", 
                           to=to_phone, 
                           message=message[:50] + "...")
                
                return {
                    'success': True,
                    'message_sid': f'SIM_{int(__import__("time").time())}',
                    'status': 'sent'
                }
            else:
                # Twilio real
                from twilio.rest import Client
                
                account_sid = os.getenv('TWILIO_ACCOUNT_SID')
                auth_token = os.getenv('TWILIO_AUTH_TOKEN')
                from_number = os.getenv('TWILIO_WHATSAPP_NUMBER')
                
                if not account_sid or not auth_token or not from_number:
                    logger.error("Credenciais Twilio não configuradas")
                    return {
                        'success': False,
                        'error': 'Credenciais Twilio não configuradas'
                    }
                
                client = Client(account_sid, auth_token)
                
                # Garantir formato correto do número
                if not to_phone.startswith('+'):
                    to_phone = '+' + to_phone.replace('+', '')
                
                message_obj = client.messages.create(
                    body=message,
                    from_=f'whatsapp:{from_number}',
                    to=f'whatsapp:{to_phone}'
                )
                
                logger.info("📱 WhatsApp enviado via Twilio", 
                           to=to_phone,
                           message_sid=message_obj.sid,
                           status=message_obj.status)
                
                return {
                    'success': True,
                    'message_sid': message_obj.sid,
                    'status': message_obj.status
                }
                
        except Exception as e:
            logger.error("Erro ao enviar mensagem", error=str(e))
            return {
                'success': False,
                'error': str(e)
            }

# Instância global
simple_twilio = SimpleTwilioService()
