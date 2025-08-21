from twilio.rest import Client
from twilio.base.exceptions import TwilioException
from typing import Dict, Optional
import structlog
from flask import current_app

logger = structlog.get_logger()

class TwilioWhatsAppService:
    """Serviço para integração com Twilio WhatsApp Business API"""
    
    def __init__(self):
        self._client: Optional[Client] = None
    
    @property
    def client(self) -> Client:
        """Cliente Twilio"""
        if self._client is None:
            account_sid = current_app.config['TWILIO_ACCOUNT_SID']
            auth_token = current_app.config['TWILIO_AUTH_TOKEN']
            self._client = Client(account_sid, auth_token)
            logger.info("Cliente Twilio inicializado")
        return self._client
    
    async def send_message(self, to_number: str, message: str) -> Dict[str, str]:
        """Enviar mensagem de texto via WhatsApp"""
        try:
            # Formatar número para WhatsApp
            formatted_number = self._format_whatsapp_number(to_number)
            from_number = current_app.config['TWILIO_WHATSAPP_NUMBER']
            
            message_obj = self.client.messages.create(
                body=message,
                from_=f'whatsapp:{from_number}',
                to=f'whatsapp:{formatted_number}'
            )
            
            logger.info("Mensagem WhatsApp enviada", 
                       to=formatted_number, 
                       message_sid=message_obj.sid)
            
            return {
                "success": True,
                "message_sid": message_obj.sid,
                "status": message_obj.status,
                "to": formatted_number
            }
            
        except TwilioException as e:
            logger.error("Erro Twilio ao enviar mensagem", 
                        to=to_number, 
                        error=str(e),
                        error_code=e.code)
            return {
                "success": False,
                "error": str(e),
                "error_code": e.code
            }
        except Exception as e:
            logger.error("Erro geral ao enviar mensagem", to=to_number, error=str(e))
            return {
                "success": False,
                "error": str(e)
            }
    
    async def send_template_message(self, to_number: str, template_name: str, 
                                  parameters: Optional[Dict] = None) -> Dict[str, str]:
        """Enviar mensagem template aprovada"""
        try:
            formatted_number = self._format_whatsapp_number(to_number)
            from_number = current_app.config['TWILIO_WHATSAPP_NUMBER']
            
            # Templates pré-aprovados
            templates = {
                "welcome": "Olá! 👋 Sou assistente do escritório de investimentos. Posso te ajudar a descobrir as melhores oportunidades para fazer seu dinheiro render. Você já investe em alguma coisa?",
                "reengagement_24h": "Oi! 😊 Vi que você demonstrou interesse em investimentos ontem. Tem alguns minutos para conversarmos sobre suas metas financeiras?",
                "reengagement_72h": "Olá! Ainda está interessado em descobrir como fazer seu dinheiro render mais? Posso te mostrar algumas oportunidades interessantes! 💰",
                "qualified_handoff": "Perfeito! 🎉 Com base no nosso papo, acredito que posso te ajudar muito. Vou conectar você com um especialista. Que tal conversarmos amanhã às 14h ou quinta às 10h?"
            }
            
            message_body = templates.get(template_name, parameters.get('custom_message', ''))
            
            if parameters:
                # Substituir placeholders
                for key, value in parameters.items():
                    message_body = message_body.replace(f'{{{key}}}', str(value))
            
            message_obj = self.client.messages.create(
                body=message_body,
                from_=f'whatsapp:{from_number}',
                to=f'whatsapp:{formatted_number}'
            )
            
            logger.info("Template WhatsApp enviado", 
                       to=formatted_number,
                       template=template_name,
                       message_sid=message_obj.sid)
            
            return {
                "success": True,
                "message_sid": message_obj.sid,
                "status": message_obj.status,
                "template": template_name,
                "to": formatted_number
            }
            
        except Exception as e:
            logger.error("Erro ao enviar template", 
                        to=to_number, 
                        template=template_name, 
                        error=str(e))
            return {
                "success": False,
                "error": str(e)
            }
    
    def parse_webhook_payload(self, payload: Dict) -> Dict:
        """Processar payload do webhook Twilio"""
        try:
            # Extrair informações da mensagem recebida
            message_data = {
                "message_sid": payload.get("MessageSid"),
                "from_number": self._clean_whatsapp_number(payload.get("From", "")),
                "to_number": self._clean_whatsapp_number(payload.get("To", "")),
                "body": payload.get("Body", ""),
                "media_url": payload.get("MediaUrl0"),
                "media_content_type": payload.get("MediaContentType0"),
                "num_media": int(payload.get("NumMedia", 0)),
                "timestamp": payload.get("Timestamp"),
                "status": payload.get("SmsStatus", "received")
            }
            
            # Informações do perfil (se disponível)
            profile_data = {
                "profile_name": payload.get("ProfileName"),
                "wa_id": payload.get("WaId")
            }
            
            message_data.update(profile_data)
            
            logger.info("Webhook Twilio processado", 
                       from_number=message_data["from_number"],
                       message_sid=message_data["message_sid"])
            
            return message_data
            
        except Exception as e:
            logger.error("Erro ao processar webhook Twilio", error=str(e))
            raise
    
    def _format_whatsapp_number(self, number: str) -> str:
        """Formatar número para padrão WhatsApp"""
        # Remove todos os caracteres não numéricos
        clean_number = ''.join(filter(str.isdigit, number))
        
        # Se não tem código do país, assume Brasil (+55)
        if len(clean_number) == 11 and clean_number.startswith('0'):
            clean_number = clean_number[1:]  # Remove 0 inicial
        
        if len(clean_number) == 10 or len(clean_number) == 11:
            if not clean_number.startswith('55'):
                clean_number = '55' + clean_number
        
        # Adiciona 9 se for celular sem o 9
        if len(clean_number) == 12 and clean_number[4] != '9':
            clean_number = clean_number[:4] + '9' + clean_number[4:]
        
        return '+' + clean_number
    
    def _clean_whatsapp_number(self, whatsapp_number: str) -> str:
        """Limpar número do formato whatsapp:+5511999999999"""
        if whatsapp_number.startswith('whatsapp:'):
            return whatsapp_number.replace('whatsapp:', '')
        return whatsapp_number
    
    async def get_message_status(self, message_sid: str) -> Dict[str, str]:
        """Verificar status de uma mensagem"""
        try:
            message = self.client.messages(message_sid).fetch()
            
            return {
                "message_sid": message.sid,
                "status": message.status,
                "error_code": message.error_code,
                "error_message": message.error_message,
                "date_sent": message.date_sent.isoformat() if message.date_sent else None,
                "date_updated": message.date_updated.isoformat() if message.date_updated else None
            }
            
        except TwilioException as e:
            logger.error("Erro ao buscar status da mensagem", 
                        message_sid=message_sid, 
                        error=str(e))
            return {
                "message_sid": message_sid,
                "status": "error",
                "error": str(e)
            }
    
    async def validate_webhook_signature(self, request_data: bytes, 
                                       signature: str, url: str) -> bool:
        """Validar assinatura do webhook Twilio"""
        try:
            from twilio.request_validator import RequestValidator
            
            auth_token = current_app.config['TWILIO_AUTH_TOKEN']
            validator = RequestValidator(auth_token)
            
            return validator.validate(url, request_data, signature)
            
        except Exception as e:
            logger.error("Erro ao validar webhook signature", error=str(e))
            return False

# Templates de mensagem pré-definidos
MESSAGE_TEMPLATES = {
    "welcome_first_time": """Olá {name}! 👋 

Sou assistente do escritório de investimentos. Vi que você se interessou pelos nossos conteúdos.

Posso te ajudar a descobrir as melhores oportunidades para fazer seu dinheiro render mais! 💰

Você já investe em alguma coisa?""",

    "welcome_inbound": """Oi! 😊 

Que bom que você entrou em contato! Sou assistente especializado em investimentos.

Posso te ajudar a encontrar as melhores opções para seus objetivos financeiros.

Me conta, qual é seu principal objetivo com investimentos?""",

    "reengagement_24h": """Oi {name}! 😊 

Vi que você demonstrou interesse em investimentos ontem.

Tem alguns minutos para conversarmos sobre suas metas financeiras? Posso te mostrar algumas oportunidades bem interessantes!""",

    "qualified_notification": """🎉 Lead Qualificado!

Nome: {name}
Telefone: {phone}
Patrimônio: {patrimonio}
Objetivo: {objetivo}
Score: {score}/100

Sugestões de horário:
• {horario1}
• {horario2}""",

    "handoff_message": """Perfeito! 🎉 

Com base no nosso papo, acredito que posso te ajudar muito com seus investimentos.

Vou conectar você com um dos nossos especialistas para uma conversa mais detalhada.

Que tal conversarmos:
• {horario1}
• {horario2}

Qual horário funciona melhor para você?"""
}

# Instância global do serviço
twilio_service = TwilioWhatsAppService()

