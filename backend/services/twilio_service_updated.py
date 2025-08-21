from twilio.rest import Client
from twilio.base.exceptions import TwilioException
from typing import Dict, Optional
import structlog
from flask import current_app
from .whatsapp_simulator import whatsapp_simulator

logger = structlog.get_logger()

class TwilioWhatsAppService:
    """Serviço para integração com Twilio WhatsApp Business API com simulação"""
    
    def __init__(self):
        self._client: Optional[Client] = None
        self._use_simulator = True  # Padrão: usar simulação
    
    def init_app(self, app):
        """Inicializar serviço com configurações da app"""
        with app.app_context():
            # Verificar se deve usar simulação
            self._use_simulator = current_app.config.get('USE_WHATSAPP_SIMULATOR', True)
            
            if not self._use_simulator:
                # Configuração real do Twilio
                account_sid = current_app.config.get('TWILIO_ACCOUNT_SID')
                auth_token = current_app.config.get('TWILIO_AUTH_TOKEN')
                
                if account_sid and auth_token and account_sid != 'ACyour-twilio-account-sid':
                    self._client = Client(account_sid, auth_token)
                    logger.info("Cliente Twilio REAL inicializado")
                else:
                    logger.info("🎭 Credenciais Twilio não configuradas, usando simulador")
                    self._use_simulator = True
            
            if self._use_simulator:
                logger.info("🎭 Usando simulador WhatsApp para testes")
    
    @property
    def client(self) -> Client:
        """Cliente Twilio"""
        if self._client is None and not self._use_simulator:
            account_sid = current_app.config['TWILIO_ACCOUNT_SID']
            auth_token = current_app.config['TWILIO_AUTH_TOKEN']
            self._client = Client(account_sid, auth_token)
            logger.info("Cliente Twilio inicializado")
        return self._client
    
    async def send_message(self, to_number: str, message: str) -> Dict[str, str]:
        """Enviar mensagem de texto via WhatsApp"""
        
        if self._use_simulator:
            # Usar simulador
            message_id = whatsapp_simulator.send_message(to_number, message)
            return {
                "success": True,
                "message_sid": message_id,
                "status": "sent",
                "to": to_number,
                "simulator": True
            }
        
        # Código real do Twilio
        try:
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
                "to": formatted_number,
                "simulator": False
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
        
        if self._use_simulator:
            # Usar simulador
            message_id = whatsapp_simulator.send_template_message(to_number, template_name, parameters)
            return {
                "success": True,
                "message_sid": message_id,
                "status": "sent",
                "template": template_name,
                "to": to_number,
                "simulator": True
            }
        
        # Código real do Twilio
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
                "to": formatted_number,
                "simulator": False
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
    
    def get_conversation_history(self, phone: str) -> list:
        """Obter histórico de conversa (simulador)"""
        if self._use_simulator:
            return whatsapp_simulator.get_conversation(phone)
        return []
    
    def get_all_simulated_messages(self) -> list:
        """Obter todas as mensagens simuladas"""
        if self._use_simulator:
            return whatsapp_simulator.get_all_messages()
        return []
    
    def clear_simulation_data(self):
        """Limpar dados de simulação"""
        if self._use_simulator:
            whatsapp_simulator.clear_conversations()
    
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

# Instância global do serviço
twilio_service = TwilioWhatsAppService()
