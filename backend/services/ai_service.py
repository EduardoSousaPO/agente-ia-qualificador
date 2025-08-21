import openai
from typing import Dict, List, Optional, Tuple
import json
import structlog
from flask import current_app

logger = structlog.get_logger()

class AIQualificationService:
    """Serviço de IA para qualificação de leads"""
    
    def __init__(self):
        self.client = None
        self.system_prompt = """Você é o assistente de qualificação de um escritório de investimentos brasileiro.

PERSONALIDADE:
- Linguagem humana, consultiva e acolhedora
- Uma pergunta por vez, nunca bombardeie o lead
- Tom profissional mas descontraído
- Sempre demonstre expertise em investimentos

CRITÉRIOS DE QUALIFICAÇÃO:
1. PATRIMÔNIO: Faixa de valores disponíveis para investir
2. OBJETIVO: Metas de investimento (aposentadoria, renda extra, reserva, etc.)
3. URGÊNCIA: Prazo para começar a investir
4. INTERESSE: Disposição em falar com um especialista

ETAPAS DA CONVERSA:
1. APRESENTAÇÃO: Saudação calorosa + apresentação do escritório
2. INVESTIGAÇÃO: Se já investe e onde investe atualmente
3. PATRIMÔNIO: Descobrir faixa de patrimônio (R$ 10k-50k, R$ 50k-200k, R$ 200k-500k, R$ 500k+)
4. OBJETIVO: Entender objetivos de investimento
5. URGÊNCIA: Descobrir prazo para começar
6. OBJEÇÕES: Tratar dúvidas e objeções naturais
7. DECISÃO: Interesse em conversar com especialista

REGRAS IMPORTANTES:
- Se lead demonstrar interesse e atingir critérios mínimos, sinalize: HANDOFF_READY
- Se lead recusar ou não se qualificar, agradeça cordialmente e ofereça conteúdo gratuito
- Nunca seja insistente ou agressivo
- Mantenha o foco na qualificação, não tente vender diretamente
- Use linguagem brasileira natural (você, não senhor/senhora)

CRITÉRIO MÍNIMO QUALIFICAÇÃO:
- Patrimônio: Mínimo R$ 50.000 disponíveis
- Interesse: Demonstrar curiosidade sobre investimentos
- Urgência: Disposição para conversar nos próximos 30 dias"""

        self.conversation_steps = {
            "apresentacao": {
                "description": "Saudação e apresentação do escritório",
                "next_steps": ["investigacao"],
                "score_weight": 5
            },
            "investigacao": {
                "description": "Descobrir se já investe e onde",
                "next_steps": ["patrimonio"],
                "score_weight": 10
            },
            "patrimonio": {
                "description": "Identificar faixa de patrimônio",
                "next_steps": ["objetivo"],
                "score_weight": 40
            },
            "objetivo": {
                "description": "Entender objetivos de investimento",
                "next_steps": ["urgencia"],
                "score_weight": 20
            },
            "urgencia": {
                "description": "Descobrir prazo para começar",
                "next_steps": ["objecoes", "decisao"],
                "score_weight": 15
            },
            "objecoes": {
                "description": "Tratar objeções e dúvidas",
                "next_steps": ["decisao"],
                "score_weight": 5
            },
            "decisao": {
                "description": "Interesse em falar com especialista",
                "next_steps": ["handoff"],
                "score_weight": 5
            }
        }
    
    def _get_client(self):
        """Inicializar cliente OpenAI"""
        if self.client is None:
            openai.api_key = current_app.config['OPENAI_API_KEY']
            self.client = openai.OpenAI(api_key=current_app.config['OPENAI_API_KEY'])
        return self.client
    
    async def process_message(self, message: str, context: Dict) -> Dict:
        """Processar mensagem do lead e gerar resposta"""
        try:
            client = self._get_client()
            
            # Construir histórico da conversa
            messages = self._build_conversation_history(context, message)
            
            # Chamar OpenAI
            response = client.chat.completions.create(
                model=current_app.config['OPENAI_MODEL'],
                messages=messages,
                max_tokens=current_app.config['OPENAI_MAX_TOKENS'],
                temperature=0.7,
                functions=[{
                    "name": "update_qualification_context",
                    "description": "Atualizar contexto de qualificação do lead",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "current_step": {
                                "type": "string",
                                "enum": list(self.conversation_steps.keys()) + ["handoff"]
                            },
                            "patrimonio_faixa": {
                                "type": "string",
                                "enum": ["0-10k", "10k-50k", "50k-200k", "200k-500k", "500k+", "não_informado"]
                            },
                            "objetivo": {"type": "string"},
                            "urgencia": {
                                "type": "string", 
                                "enum": ["imediato", "30_dias", "3_meses", "6_meses", "1_ano", "sem_pressa", "não_informado"]
                            },
                            "interesse_especialista": {"type": "boolean"},
                            "handoff_ready": {"type": "boolean"},
                            "desqualificado": {"type": "boolean"},
                            "observacoes": {"type": "string"}
                        },
                        "required": ["current_step"]
                    }
                }],
                function_call="auto"
            )
            
            # Processar resposta
            ai_message = response.choices[0].message
            
            result = {
                "response": ai_message.content,
                "context_update": {},
                "handoff_ready": False,
                "desqualificado": False
            }
            
            # Se houve function call, processar contexto
            if ai_message.function_call:
                try:
                    function_args = json.loads(ai_message.function_call.arguments)
                    result["context_update"] = function_args
                    result["handoff_ready"] = function_args.get("handoff_ready", False)
                    result["desqualificado"] = function_args.get("desqualificado", False)
                except json.JSONDecodeError as e:
                    logger.error("Erro ao parsear function call", error=str(e))
            
            # Calcular score
            score = self._calculate_score(context, result["context_update"])
            result["score"] = score
            
            logger.info("Mensagem processada pela IA", 
                       current_step=result["context_update"].get("current_step"),
                       score=score,
                       handoff_ready=result["handoff_ready"])
            
            return result
            
        except Exception as e:
            logger.error("Erro ao processar mensagem com IA", error=str(e))
            # Fallback response
            return {
                "response": "Desculpe, tive um problema técnico. Pode repetir sua mensagem?",
                "context_update": {},
                "handoff_ready": False,
                "desqualificado": False,
                "score": context.get("score", 0)
            }
    
    def _build_conversation_history(self, context: Dict, new_message: str) -> List[Dict]:
        """Construir histórico da conversa para enviar à IA"""
        messages = [{"role": "system", "content": self.system_prompt}]
        
        # Adicionar contexto atual
        if context.get("current_step"):
            step_info = self.conversation_steps.get(context["current_step"], {})
            context_msg = f"CONTEXTO ATUAL: Etapa '{context['current_step']}' - {step_info.get('description', '')}"
            
            if context.get("patrimonio_faixa"):
                context_msg += f"\nPatrimônio: {context['patrimonio_faixa']}"
            if context.get("objetivo"):
                context_msg += f"\nObjetivo: {context['objetivo']}"
            if context.get("urgencia"):
                context_msg += f"\nUrgência: {context['urgencia']}"
            
            messages.append({"role": "system", "content": context_msg})
        
        # Adicionar histórico de mensagens (últimas 10)
        message_history = context.get("message_history", [])
        for msg in message_history[-10:]:  # Últimas 10 mensagens
            messages.append({
                "role": "user" if msg["direction"] == "inbound" else "assistant",
                "content": msg["content"]
            })
        
        # Adicionar nova mensagem
        messages.append({"role": "user", "content": new_message})
        
        return messages
    
    def _calculate_score(self, current_context: Dict, context_update: Dict) -> int:
        """Calcular score de qualificação do lead"""
        score = current_context.get("score", 0)
        
        # Pontuação por patrimônio
        patrimonio = context_update.get("patrimonio_faixa", current_context.get("patrimonio_faixa"))
        if patrimonio:
            patrimonio_scores = {
                "0-10k": 5,
                "10k-50k": 15,
                "50k-200k": 30,
                "200k-500k": 35,
                "500k+": 40
            }
            score = max(score, patrimonio_scores.get(patrimonio, 0))
        
        # Pontuação por objetivo (se bem definido)
        objetivo = context_update.get("objetivo", current_context.get("objetivo"))
        if objetivo and len(objetivo.strip()) > 10:  # Objetivo bem elaborado
            score += 15
        
        # Pontuação por urgência
        urgencia = context_update.get("urgencia", current_context.get("urgencia"))
        if urgencia:
            urgencia_scores = {
                "imediato": 20,
                "30_dias": 15,
                "3_meses": 10,
                "6_meses": 5,
                "1_ano": 2,
                "sem_pressa": 0
            }
            score += urgencia_scores.get(urgencia, 0)
        
        # Pontuação por interesse
        interesse = context_update.get("interesse_especialista", current_context.get("interesse_especialista"))
        if interesse:
            score += 15
        
        # Pontuação por engajamento (número de mensagens)
        message_count = len(current_context.get("message_history", []))
        if message_count >= 3:  # Pelo menos 3 trocas de mensagem
            score += 5
        if message_count >= 5:  # Conversa mais longa
            score += 5
        
        return min(score, 100)  # Máximo 100 pontos
    
    def get_qualification_summary(self, context: Dict) -> Dict:
        """Gerar resumo da qualificação"""
        return {
            "patrimonio_faixa": context.get("patrimonio_faixa", "não_informado"),
            "objetivo": context.get("objetivo", ""),
            "urgencia": context.get("urgencia", "não_informado"),
            "interesse_especialista": context.get("interesse_especialista", False),
            "score_final": context.get("score", 0),
            "current_step": context.get("current_step", "apresentacao"),
            "observacoes": context.get("observacoes", ""),
            "qualificado": context.get("score", 0) >= 70,  # Threshold de qualificação
            "handoff_ready": context.get("handoff_ready", False)
        }

# Instância global do serviço
ai_service = AIQualificationService()

