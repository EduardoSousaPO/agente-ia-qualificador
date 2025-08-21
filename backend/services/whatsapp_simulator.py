"""
Simulador de WhatsApp para testes sem Twilio
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from flask import current_app

class WhatsAppSimulator:
    def __init__(self):
        self.messages = []  # Armazena mensagens simuladas
        self.conversations = {}  # Armazena conversas por telefone
        
    def send_message(self, to: str, message: str, media_url: List[str] = None) -> str:
        """Simula envio de mensagem WhatsApp"""
        
        # Gerar ID simulado
        message_id = f"SIM{datetime.now().strftime('%Y%m%d%H%M%S')}{len(self.messages)}"
        
        # Criar registro da mensagem
        sim_message = {
            "id": message_id,
            "to": to,
            "message": message,
            "media_url": media_url or [],
            "timestamp": datetime.now().isoformat(),
            "status": "sent",
            "type": "outbound"
        }
        
        # Armazenar mensagem
        self.messages.append(sim_message)
        
        # Armazenar na conversa
        if to not in self.conversations:
            self.conversations[to] = []
        self.conversations[to].append(sim_message)
        
        # Log detalhado
        current_app.logger.info(f"""
📱 SIMULAÇÃO WHATSAPP - MENSAGEM ENVIADA
═══════════════════════════════════════
📞 Para: {to}
💬 Mensagem: {message}
🎯 ID: {message_id}
⏰ Horário: {sim_message['timestamp']}
📎 Mídia: {len(media_url or [])} arquivos
═══════════════════════════════════════
""")
        
        # Simular resposta automática (opcional)
        if current_app.config.get('WHATSAPP_SIMULATE_RESPONSES', True):
            self._simulate_user_response(to, message)
        
        return message_id
    
    def _simulate_user_response(self, phone: str, sent_message: str):
        """Simula resposta do usuário baseada na mensagem enviada"""
        
        # Respostas simuladas baseadas no conteúdo
        responses = {
            "olá": "Oi! Tudo bem?",
            "investimento": "Sim, tenho interesse em investir",
            "patrimônio": "Tenho cerca de R$ 100.000",
            "objetivo": "Quero fazer minha aposentadoria",
            "urgência": "Não tenho pressa, posso esperar",
            "reunião": "Sim, aceito uma reunião",
            "default": "Entendi, pode continuar"
        }
        
        # Escolher resposta baseada na mensagem enviada
        response = responses["default"]
        for key, value in responses.items():
            if key.lower() in sent_message.lower():
                response = value
                break
        
        # Criar mensagem de resposta simulada
        response_id = f"SIM_RESP_{datetime.now().strftime('%H%M%S')}"
        sim_response = {
            "id": response_id,
            "from": phone,
            "message": response,
            "timestamp": datetime.now().isoformat(),
            "status": "received",
            "type": "inbound"
        }
        
        # Armazenar resposta
        self.messages.append(sim_response)
        self.conversations[phone].append(sim_response)
        
        current_app.logger.info(f"""
📱 SIMULAÇÃO WHATSAPP - RESPOSTA RECEBIDA
═══════════════════════════════════════
📞 De: {phone}
💬 Resposta: {response}
🎯 ID: {response_id}
═══════════════════════════════════════
""")
    
    def get_conversation(self, phone: str) -> List[Dict]:
        """Retorna conversa simulada de um telefone"""
        return self.conversations.get(phone, [])
    
    def get_all_messages(self) -> List[Dict]:
        """Retorna todas as mensagens simuladas"""
        return self.messages
    
    def clear_conversations(self):
        """Limpa todas as conversas simuladas"""
        self.messages = []
        self.conversations = {}
        current_app.logger.info("🧹 Conversas simuladas limpas")
    
    def send_template_message(self, to: str, template_name: str, components: List[Dict] = None) -> str:
        """Simula envio de mensagem template"""
        
        # Templates simulados
        templates = {
            "boas_vindas": "Olá! Bem-vindo ao nosso serviço de consultoria em investimentos. Como posso ajudá-lo?",
            "qualificacao_inicio": "Para oferecermos a melhor consultoria, preciso fazer algumas perguntas. Você investe atualmente?",
            "reuniao_agendada": "Perfeito! Sua reunião foi agendada. Em breve entraremos em contato.",
            "default": f"Template: {template_name}"
        }
        
        message = templates.get(template_name, templates["default"])
        
        # Se tem componentes, adicionar ao template
        if components:
            message += f" [Componentes: {json.dumps(components)}]"
        
        return self.send_message(to, message)

# Instância global do simulador
whatsapp_simulator = WhatsAppSimulator()
