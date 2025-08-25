#!/usr/bin/env python3
"""
Serviço OpenAI para processamento de mensagens com IA
"""

import os
import json
from typing import Dict, Tuple, Optional
import structlog
from openai import OpenAI

logger = structlog.get_logger()

class OpenAIService:
    def __init__(self):
        """Inicializar serviço OpenAI"""
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
        self.max_tokens = int(os.getenv('OPENAI_MAX_TOKENS', '1000'))
        self.temperature = float(os.getenv('OPENAI_TEMPERATURE', '0.7'))
        
    def process_message(self, context: Dict, user_message: str, knowledge_context: str = "") -> Tuple[str, Dict]:
        """Processar mensagem do usuário com IA"""
        try:
            # Construir prompt baseado no contexto e conhecimento
            system_prompt = self._build_system_prompt(context, knowledge_context)
            
            # Histórico de conversa
            conversation_history = context.get('conversation_history', [])
            
            # Preparar mensagens para OpenAI
            messages = [
                {"role": "system", "content": system_prompt}
            ]
            
            # Adicionar histórico
            messages.extend(conversation_history)
            
            # Adicionar mensagem atual do usuário
            messages.append({
                "role": "user", 
                "content": user_message
            })
            
            # Chamar OpenAI
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            # Atualizar contexto
            updated_context = self._update_context(context, user_message, ai_response)
            
            logger.info("Mensagem processada com IA", 
                       user_message_length=len(user_message),
                       ai_response_length=len(ai_response),
                       current_step=updated_context.get('current_step'),
                       tokens_used=response.usage.total_tokens if response.usage else 0)
            
            return ai_response, updated_context
            
        except Exception as e:
            logger.error("Erro ao processar mensagem com IA", error=str(e))
            # Fallback para resposta padrão
            fallback_response = "Desculpe, houve um problema técnico. Pode repetir sua resposta?"
            return fallback_response, context
    
    def _build_system_prompt(self, context: Dict, knowledge_context: str = "") -> str:
        """Construir prompt do sistema com base no contexto e conhecimento"""
        
        # Prompt base de qualificação
        base_prompt = """Você é um assistente especializado em qualificação de leads para consultoria de investimentos.

OBJETIVO: Qualificar o lead fazendo EXATAMENTE 4 perguntas essenciais.

REGRAS IMPORTANTES:
1. Seja cordial, profissional e consultivo
2. Faça UMA pergunta por vez
3. Aguarde a resposta antes da próxima pergunta
4. Mantenha o tom natural, como um consultor experiente
5. Após as 4 perguntas, calcule o score e finalize

SEQUÊNCIA OBRIGATÓRIA:
1. PATRIMÔNIO: "Quanto você tem disponível para investir hoje?"
2. OBJETIVO: "Qual seu principal objetivo com os investimentos?"
3. URGÊNCIA: "Quando pretende começar a investir?"
4. INTERESSE: "Gostaria de falar com um de nossos especialistas?"

SCORING (0-100 pontos):
- PATRIMÔNIO: Até R$ 50k=10pts, R$ 50-200k=20pts, R$ 200-500k=25pts, R$ 500k+=30pts
- OBJETIVO: Aposentadoria=25pts, Crescimento=20pts, Reserva=15pts, Especulação=10pts
- URGÊNCIA: Esta semana=25pts, Este mês=20pts, 3 meses=15pts, Sem pressa=5pts
- INTERESSE: Sim urgente=20pts, Sim possível=15pts, Talvez=10pts, Não=0pts

IMPORTANTE: Quando o lead responder a 4ª pergunta, responda com:
"QUALIFICACAO_COMPLETA: [score calculado]"
"""
        
        # Se há conhecimento da empresa, injetar no prompt
        if knowledge_context.strip():
            return f"""
CONTEXTO DA EMPRESA:
{knowledge_context}

FLUXO OBRIGATÓRIO:
{base_prompt}

IMPORTANTE: Use o contexto da empresa para responder dúvidas específicas, mas SEMPRE mantenha o fluxo de 4 perguntas obrigatórias.
"""
        
        return base_prompt
    
    def _update_context(self, context: Dict, user_message: str, ai_response: str) -> Dict:
        """Atualizar contexto da sessão"""
        updated_context = context.copy()
        
        # Adicionar ao histórico de conversa
        if 'conversation_history' not in updated_context:
            updated_context['conversation_history'] = []
        
        updated_context['conversation_history'].extend([
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": ai_response}
        ])
        
        # Analisar progresso da qualificação
        current_step = updated_context.get('current_step', 'inicio')
        answers = updated_context.get('answers', {})
        
        # Detectar respostas e avançar etapas
        if current_step == 'inicio' or current_step == 'patrimonio':
            # Tentar extrair resposta sobre patrimônio
            patrimonio = self._extract_patrimonio_answer(user_message)
            if patrimonio:
                answers['patrimonio'] = patrimonio
                updated_context['current_step'] = 'objetivo'
        
        elif current_step == 'objetivo':
            # Tentar extrair resposta sobre objetivo
            objetivo = self._extract_objetivo_answer(user_message)
            if objetivo:
                answers['objetivo'] = objetivo
                updated_context['current_step'] = 'urgencia'
        
        elif current_step == 'urgencia':
            # Tentar extrair resposta sobre urgência
            urgencia = self._extract_urgencia_answer(user_message)
            if urgencia:
                answers['urgencia'] = urgencia
                updated_context['current_step'] = 'interesse'
        
        elif current_step == 'interesse':
            # Tentar extrair resposta sobre interesse
            interesse = self._extract_interesse_answer(user_message)
            if interesse:
                answers['interesse'] = interesse
                updated_context['current_step'] = 'qualificacao_completa'
        
        updated_context['answers'] = answers
        
        return updated_context
    
    def _extract_patrimonio_answer(self, message: str) -> Optional[str]:
        """Extrair resposta sobre patrimônio"""
        message_lower = message.lower()
        
        # Detectar opções múltipla escolha
        if 'a' in message_lower or 'até' in message_lower or '50' in message:
            return 'ate_50k'
        elif 'b' in message_lower or ('50' in message and '200' in message):
            return '50k_200k'
        elif 'c' in message_lower or ('200' in message and '500' in message):
            return '200k_500k'
        elif 'd' in message_lower or 'mais' in message_lower or '500' in message:
            return 'acima_500k'
        
        # Detectar valores monetários
        if any(term in message_lower for term in ['mil', 'k', 'milhão', 'milhões']):
            if any(num in message for num in ['500', '1000', '1.000']):
                return 'acima_500k'
            elif any(num in message for num in ['200', '300', '400']):
                return '200k_500k'
            elif any(num in message for num in ['50', '100', '150']):
                return '50k_200k'
            else:
                return 'ate_50k'
        
        return None
    
    def _extract_objetivo_answer(self, message: str) -> Optional[str]:
        """Extrair resposta sobre objetivo"""
        message_lower = message.lower()
        
        if 'a' in message_lower or 'aposentadoria' in message_lower:
            return 'aposentadoria'
        elif 'b' in message_lower or 'crescimento' in message_lower:
            return 'crescimento'
        elif 'c' in message_lower or 'reserva' in message_lower or 'emergência' in message_lower:
            return 'reserva'
        elif 'd' in message_lower or 'especulação' in message_lower or 'day trade' in message_lower:
            return 'especulacao'
        
        return None
    
    def _extract_urgencia_answer(self, message: str) -> Optional[str]:
        """Extrair resposta sobre urgência"""
        message_lower = message.lower()
        
        if 'a' in message_lower or 'esta semana' in message_lower or 'semana' in message_lower:
            return 'esta_semana'
        elif 'b' in message_lower or 'este mês' in message_lower or 'mês' in message_lower:
            return 'este_mes'
        elif 'c' in message_lower or '3 meses' in message_lower or 'três meses' in message_lower:
            return 'tres_meses'
        elif 'd' in message_lower or 'não tenho pressa' in message_lower or 'sem pressa' in message_lower:
            return 'sem_pressa'
        
        return None
    
    def _extract_interesse_answer(self, message: str) -> Optional[str]:
        """Extrair resposta sobre interesse"""
        message_lower = message.lower()
        
        if 'a' in message_lower or ('sim' in message_lower and 'urgente' in message_lower):
            return 'sim_urgente'
        elif 'b' in message_lower or ('sim' in message_lower and 'possível' in message_lower):
            return 'sim_possivel'
        elif 'c' in message_lower or 'talvez' in message_lower:
            return 'talvez'
        elif 'd' in message_lower or 'não' in message_lower or 'nao' in message_lower:
            return 'nao'
        
        return None
    
    def get_qualification_status(self, context: Dict) -> Dict:
        """Verificar status da qualificação"""
        answers = context.get('answers', {})
        current_step = context.get('current_step', 'inicio')
        
        # Verificar se todas as 4 perguntas foram respondidas
        required_answers = ['patrimonio', 'objetivo', 'urgencia', 'interesse']
        completed = all(answer in answers for answer in required_answers)
        
        if not completed:
            return {
                'completed': False,
                'qualified': False,
                'score': 0,
                'answers_count': len(answers),
                'current_step': current_step
            }
        
        # Calcular score
        score = self._calculate_score(answers)
        qualified = score >= 70
        
        return {
            'completed': True,
            'qualified': qualified,
            'score': score,
            'answers': answers,
            'current_step': 'qualificacao_completa'
        }
    
    def _calculate_score(self, answers: Dict) -> int:
        """Calcular score baseado nas respostas"""
        score = 0
        
        # PATRIMÔNIO (0-30 pontos)
        patrimonio_scores = {
            'ate_50k': 10,
            '50k_200k': 20,
            '200k_500k': 25,
            'acima_500k': 30
        }
        score += patrimonio_scores.get(answers.get('patrimonio'), 0)
        
        # OBJETIVO (0-25 pontos)
        objetivo_scores = {
            'aposentadoria': 25,
            'crescimento': 20,
            'reserva': 15,
            'especulacao': 10
        }
        score += objetivo_scores.get(answers.get('objetivo'), 0)
        
        # URGÊNCIA (0-25 pontos)
        urgencia_scores = {
            'esta_semana': 25,
            'este_mes': 20,
            'tres_meses': 15,
            'sem_pressa': 5
        }
        score += urgencia_scores.get(answers.get('urgencia'), 0)
        
        # INTERESSE (0-20 pontos)
        interesse_scores = {
            'sim_urgente': 20,
            'sim_possivel': 15,
            'talvez': 10,
            'nao': 0
        }
        score += interesse_scores.get(answers.get('interesse'), 0)
        
        return min(score, 100)  # Máximo 100 pontos

# Instância global do serviço
openai_service = OpenAIService()
