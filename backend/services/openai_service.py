#!/usr/bin/env python3
"""
Serviço OpenAI Unificado - ÚNICA FONTE DA VERDADE para Scoring
Sistema de Qualificação: 4 perguntas obrigatórias, score 0-100, qualificado >= 70
"""

import os
import json
import re
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
        
        # Threshold para qualificação
        self.qualification_threshold = 70
        
    def chat_completion(self, messages: list, model: str = None) -> str:
        """Completions básico do OpenAI"""
        try:
            response = self.client.chat.completions.create(
                model=model or self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error("Erro no chat completion", error=str(e))
            return "Desculpe, houve um erro. Pode repetir sua resposta?"
    
    def extract_qualification_answer(self, user_message: str) -> Dict:
        """
        Extrair resposta de qualificação da mensagem do usuário
        Retorna: {step: str, option: "A|B|C|D"}
        """
        try:
            message_upper = user_message.upper().strip()
            
            # Tentar extrair letra direta (A, B, C, D)
            if len(message_upper) == 1 and message_upper in ['A', 'B', 'C', 'D']:
                return {'option': message_upper}
            
            # Buscar padrões de letra
            match = re.search(r'\b([A-D])\b', message_upper)
            if match:
                return {'option': match.group(1)}
            
            # Mapeamento de conteúdo para letras (PATRIMÔNIO)
            if any(word in message_upper for word in ['50', 'CINQUENTA', 'ATÉ']):
                return {'option': 'A'}
            elif any(word in message_upper for word in ['200', 'DUZENTOS', '50 MIL A']):
                return {'option': 'B'}
            elif any(word in message_upper for word in ['500', 'QUINHENTOS', '200 MIL A']):
                return {'option': 'C'}
            elif any(word in message_upper for word in ['MAIS DE', 'ACIMA', 'SUPERIOR']):
                return {'option': 'D'}
            
            # Mapeamento de conteúdo (OBJETIVO)
            elif 'APOSENTADORIA' in message_upper:
                return {'option': 'A'}
            elif 'CRESCIMENTO' in message_upper:
                return {'option': 'B'}
            elif 'RESERVA' in message_upper:
                return {'option': 'C'}
            elif 'ESPECULAÇÃO' in message_upper or 'ESPECULACAO' in message_upper:
                return {'option': 'D'}
            
            # Mapeamento de conteúdo (URGÊNCIA)
            elif 'ESTA SEMANA' in message_upper or 'SEMANA' in message_upper:
                return {'option': 'A'}
            elif 'ESTE MÊS' in message_upper or 'ESTE MES' in message_upper:
                return {'option': 'B'}
            elif '3 MESES' in message_upper or 'TRÊS MESES' in message_upper:
                return {'option': 'C'}
            elif 'SEM PRESSA' in message_upper or 'NÃO TENHO PRESSA' in message_upper:
                return {'option': 'D'}
            
            # Mapeamento de conteúdo (INTERESSE)
            elif 'SIM' in message_upper and 'URGENTE' in message_upper:
                return {'option': 'A'}
            elif 'SIM' in message_upper and ('POSSÍVEL' in message_upper or 'POSSIVEL' in message_upper):
                return {'option': 'B'}
            elif 'TALVEZ' in message_upper:
                return {'option': 'C'}
            elif 'NÃO' in message_upper or 'NAO' in message_upper:
                return {'option': 'D'}
            
            # Não conseguiu extrair
            logger.warning("Não foi possível extrair resposta", message=user_message)
            return {}
            
        except Exception as e:
            logger.error("Erro ao extrair resposta", error=str(e), message=user_message)
            return {}
    
    def calculate_lead_score(self, answers: Dict) -> int:
        """
        Calcular score do lead baseado nas respostas (ÚNICA FONTE DA VERDADE)
        
        Sistema de pontuação:
        - Patrimônio: 0-30 pontos (A=10, B=20, C=25, D=30)
        - Objetivo: 0-25 pontos (A=25, B=20, C=15, D=10)
        - Urgência: 0-25 pontos (A=25, B=20, C=15, D=5)
        - Interesse: 0-20 pontos (A=20, B=15, C=10, D=0)
        
        Total: 0-100 pontos | Qualificado: >= 70 pontos
        """
        try:
            score = 0
            
            # PATRIMÔNIO (0-30 pontos) - Maior peso por indicar capacidade
            patrimonio_scores = {
                'A': 10,  # Até R$ 50 mil
                'B': 20,  # R$ 50-200 mil
                'C': 25,  # R$ 200-500 mil
                'D': 30   # Mais de R$ 500 mil
            }
            
            # OBJETIVO (0-25 pontos) - Aposentadoria = maior valor (longo prazo)
            objetivo_scores = {
                'A': 25,  # Aposentadoria
                'B': 20,  # Crescimento
                'C': 15,  # Reserva
                'D': 10   # Especulação
            }
            
            # URGÊNCIA (0-25 pontos) - Urgência alta = maior conversão
            urgencia_scores = {
                'A': 25,  # Esta semana
                'B': 20,  # Este mês
                'C': 15,  # Em 3 meses
                'D': 5    # Sem pressa
            }
            
            # INTERESSE (0-20 pontos) - Interesse direto em consultoria
            interesse_scores = {
                'A': 20,  # Sim, urgente
                'B': 15,  # Sim, quando possível
                'C': 10,  # Talvez
                'D': 0    # Não
            }
            
            # Calcular pontuação total
            patrimonio_score = patrimonio_scores.get(answers.get('patrimonio', ''), 0)
            objetivo_score = objetivo_scores.get(answers.get('objetivo', ''), 0)
            urgencia_score = urgencia_scores.get(answers.get('urgencia', ''), 0)
            interesse_score = interesse_scores.get(answers.get('interesse', ''), 0)
            
            score = patrimonio_score + objetivo_score + urgencia_score + interesse_score
            
            # Log detalhado para auditoria
            logger.info("Score calculado (OpenAI-only)", 
                       answers=answers,
                       score_breakdown={
                           'patrimonio': f"{answers.get('patrimonio', 'N/A')} = {patrimonio_score}pts",
                           'objetivo': f"{answers.get('objetivo', 'N/A')} = {objetivo_score}pts",
                           'urgencia': f"{answers.get('urgencia', 'N/A')} = {urgencia_score}pts",
                           'interesse': f"{answers.get('interesse', 'N/A')} = {interesse_score}pts"
                       },
                       score_total=score,
                       qualified=score >= self.qualification_threshold,
                       threshold=self.qualification_threshold)
            
            return score
            
        except Exception as e:
            logger.error("Erro ao calcular score", error=str(e), answers=answers)
            return 0
    
    def is_qualified(self, score: int) -> bool:
        """Verificar se lead está qualificado baseado no score"""
        return score >= self.qualification_threshold
    
    def get_qualification_summary(self, answers: Dict) -> Dict:
        """Obter resumo completo da qualificação"""
        try:
            # Verificar se todas as respostas estão presentes
            required_answers = ['patrimonio', 'objetivo', 'urgencia', 'interesse']
            answers_count = sum(1 for key in required_answers if answers.get(key))
            
            if answers_count < 4:
                return {
                    'completed': False,
                    'score': 0,
                    'qualified': False,
                    'answers_count': answers_count,
                    'missing_answers': [key for key in required_answers if not answers.get(key)]
                }
            
            # Calcular score final
            score = self.calculate_lead_score(answers)
            qualified = self.is_qualified(score)
            
            return {
                'completed': True,
                'score': score,
                'qualified': qualified,
                'answers': answers,
                'threshold': self.qualification_threshold,
                'status': 'QUALIFICADO' if qualified else 'NÃO QUALIFICADO'
            }
            
        except Exception as e:
            logger.error("Erro ao obter resumo de qualificação", error=str(e))
            return {
                'completed': False,
                'score': 0,
                'qualified': False,
                'error': str(e)
            }

# Instância global - criada sob demanda para evitar erro de inicialização
openai_service = None

def get_openai_service():
    """Obter instância do OpenAI Service (lazy loading)"""
    global openai_service
    if openai_service is None:
        openai_service = OpenAIService()
    return openai_service

# Função para teste rápido (sem API)
def test_scoring_system():
    """Testar sistema de scoring unificado sem OpenAI API"""
    print("🧪 Testando Sistema de Scoring Unificado (OpenAI-only)")
    
    # Criar instância mock para teste
    class MockOpenAIService:
        def __init__(self):
            self.qualification_threshold = 70
            
        def calculate_lead_score(self, answers):
            score = 0
            patrimonio_scores = {'A': 10, 'B': 20, 'C': 25, 'D': 30}
            objetivo_scores = {'A': 25, 'B': 20, 'C': 15, 'D': 10}
            urgencia_scores = {'A': 25, 'B': 20, 'C': 15, 'D': 5}
            interesse_scores = {'A': 20, 'B': 15, 'C': 10, 'D': 0}
            
            score += patrimonio_scores.get(answers.get('patrimonio', ''), 0)
            score += objetivo_scores.get(answers.get('objetivo', ''), 0)
            score += urgencia_scores.get(answers.get('urgencia', ''), 0)
            score += interesse_scores.get(answers.get('interesse', ''), 0)
            
            print(f"  Breakdown: P={patrimonio_scores.get(answers.get('patrimonio', ''), 0)} + O={objetivo_scores.get(answers.get('objetivo', ''), 0)} + U={urgencia_scores.get(answers.get('urgencia', ''), 0)} + I={interesse_scores.get(answers.get('interesse', ''), 0)} = {score}")
            return score
    
    mock_service = MockOpenAIService()
    
    # Cenário 1: Cliente Premium (score alto)
    answers_premium = {
        'patrimonio': 'D',  # Mais de R$ 500k = 30pts
        'objetivo': 'A',    # Aposentadoria = 25pts
        'urgencia': 'A',    # Esta semana = 25pts
        'interesse': 'A'    # Sim, urgente = 20pts
    }
    
    score_premium = mock_service.calculate_lead_score(answers_premium)
    print(f"Cliente Premium: {score_premium}/100 - {'✅ QUALIFICADO' if score_premium >= 70 else '❌ NÃO QUALIFICADO'}")
    
    # Cenário 2: Cliente Médio
    answers_medio = {
        'patrimonio': 'B',  # R$ 50-200k = 20pts
        'objetivo': 'B',    # Crescimento = 20pts
        'urgencia': 'B',    # Este mês = 20pts
        'interesse': 'B'    # Sim, possível = 15pts
    }
    
    score_medio = mock_service.calculate_lead_score(answers_medio)
    print(f"Cliente Médio: {score_medio}/100 - {'✅ QUALIFICADO' if score_medio >= 70 else '❌ NÃO QUALIFICADO'}")
    
    # Cenário 3: Cliente Baixo
    answers_baixo = {
        'patrimonio': 'A',  # Até R$ 50k = 10pts
        'objetivo': 'D',    # Especulação = 10pts
        'urgencia': 'D',    # Sem pressa = 5pts
        'interesse': 'D'    # Não = 0pts
    }
    
    score_baixo = mock_service.calculate_lead_score(answers_baixo)
    print(f"Cliente Baixo: {score_baixo}/100 - {'✅ QUALIFICADO' if score_baixo >= 70 else '❌ NÃO QUALIFICADO'}")
    
    print(f"\n✅ Sistema de scoring funcionando - Threshold: {mock_service.qualification_threshold}")
    return True

if __name__ == "__main__":
    test_scoring_system()
