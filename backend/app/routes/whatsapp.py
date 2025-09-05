#!/usr/bin/env python3
"""
Webhook do Twilio WhatsApp - Substituindo N8N
Processa mensagens WhatsApp recebidas e executa qualificação de leads
"""

from flask import Blueprint, request, jsonify, g
from services.simple_supabase import simple_supabase
from services.qualification_service import qualification_service
from services.simple_twilio import simple_twilio
from services.openai_service import get_openai_service
from services.email_service import email_service
from services.crm_adapter import crm_adapter
from utils.validators import validate_required_fields
import structlog
import re

logger = structlog.get_logger()

whatsapp_bp = Blueprint('whatsapp', __name__)

@whatsapp_bp.route('/api/whatsapp/webhook', methods=['POST'])
def twilio_webhook():
    """
    Webhook principal do Twilio WhatsApp
    Recebe mensagens do WhatsApp e processa qualificação
    
    Payload esperado do Twilio:
    {
        "Body": "mensagem do usuário",
        "From": "whatsapp:+5511999888777",
        "To": "whatsapp:+14155238886",
        "AccountSid": "AC...",
        "MessageSid": "SM..."
    }
    """
    try:
        # Obter dados do webhook do Twilio
        data = request.form.to_dict() if request.form else request.get_json()
        
        if not data:
            logger.warning("Webhook recebido sem dados")
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        # Validar campos obrigatórios do Twilio
        required_fields = ['Body', 'From']
        validation_error = validate_required_fields(data, required_fields)
        if validation_error:
            logger.error("Webhook Twilio com dados inválidos", error=validation_error)
            return jsonify({'error': validation_error}), 400
        
        # Extrair dados da mensagem
        message_body = data.get('Body', '').strip()
        from_number = data.get('From', '')  # whatsapp:+5511999888777
        to_number = data.get('To', '')      # whatsapp:+14155238886
        message_sid = data.get('MessageSid', '')
        account_sid = data.get('AccountSid', '')
        
        # Limpar número de telefone (remover whatsapp: e +)
        clean_phone = from_number.replace('whatsapp:', '').replace('+', '')
        
        logger.info("Webhook Twilio recebido", 
                   from_number=from_number,
                   clean_phone=clean_phone,
                   message_body=message_body[:100],
                   message_sid=message_sid)
        
        # Filtrar mensagens vazias ou de sistema
        if not message_body or len(message_body.strip()) < 1:
            logger.info("Mensagem vazia ignorada")
            return jsonify({'status': 'ignored', 'reason': 'empty_message'}), 200
        
        # Buscar ou criar lead
        lead = _find_or_create_lead(clean_phone, from_number)
        if not lead:
            logger.error("Falha ao buscar/criar lead", phone=clean_phone)
            return jsonify({'error': 'Falha ao processar lead'}), 500
        
        lead_id = lead['id']
        tenant_id = lead.get('tenant_id', '05dc8c52-c0a0-44ae-aa2a-eeaa01090a27')
        
        # Buscar ou criar sessão ativa
        session = _find_or_create_session(lead_id, clean_phone)
        if not session:
            logger.error("Falha ao buscar/criar sessão", lead_id=lead_id)
            return jsonify({'error': 'Falha ao processar sessão'}), 500
        
        session_id = session['id']
        
        # Salvar mensagem recebida
        _save_incoming_message(session_id, message_body, message_sid)
        
        # Processar resposta com IA
        ai_response = qualification_service.process_lead_response(session_id, message_body)
        
        if not ai_response.get('success'):
            logger.error("Falha no processamento IA", 
                        session_id=session_id,
                        error=ai_response.get('error'))
            return jsonify({'error': 'Falha no processamento IA'}), 500
        
        # Verificar se qualificação foi completada
        if ai_response.get('completed') and ai_response.get('qualified'):
            score = ai_response.get('score', 0)
            logger.info("Lead qualificado via WhatsApp", 
                       lead_id=lead_id,
                       score=score,
                       session_id=session_id)
            
            # Notificar consultor diretamente (sem N8N)
            _notify_qualified_lead(lead, score, ai_response.get('context', {}))
        
        logger.info("Webhook Twilio processado com sucesso", 
                   lead_id=lead_id,
                   session_id=session_id,
                   completed=ai_response.get('completed', False),
                   qualified=ai_response.get('qualified', False),
                   score=ai_response.get('score', 0))
        
        # Retornar resposta com todos os dados da IA
        response_data = {
            'success': True,
            'message': 'Mensagem processada com sucesso',
            'lead_id': lead_id,
            'session_id': session_id,
            'completed': ai_response.get('completed', False),
            'qualified': ai_response.get('qualified', False),
            'score': ai_response.get('score', 0),
            'ai_message': ai_response.get('message', ''),
            'context': ai_response.get('context', {})
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        logger.error("Erro no webhook Twilio", error=str(e))
        return jsonify({
            'success': False,
            'error': 'Erro interno do servidor',
            'details': str(e)
        }), 500

def _find_or_create_lead(clean_phone: str, full_phone: str) -> dict:
    """Buscar lead existente ou criar novo"""
    try:
        # Buscar lead existente
        result = simple_supabase.client.table('leads') \
            .select('*') \
            .eq('phone', clean_phone) \
            .limit(1) \
            .execute()
        
        if result.data:
            lead = result.data[0]
            logger.info("Lead existente encontrado", 
                       lead_id=lead['id'], 
                       phone=clean_phone)
            return lead
        
        # Criar novo lead
        new_lead_data = {
            'name': f'Lead WhatsApp {clean_phone[-4:]}',  # Nome temporário
            'phone': clean_phone,
            'email': None,
            'origem': 'WhatsApp',
            'status': 'novo',
            'score': 0,
            'tenant_id': '05dc8c52-c0a0-44ae-aa2a-eeaa01090a27'  # Tenant demo
        }
        
        create_result = simple_supabase.client.table('leads') \
            .insert(new_lead_data) \
            .execute()
        
        if create_result.data:
            new_lead = create_result.data[0]
            logger.info("Novo lead criado via WhatsApp", 
                       lead_id=new_lead['id'], 
                       phone=clean_phone)
            return new_lead
        
        return None
        
    except Exception as e:
        logger.error("Erro ao buscar/criar lead", phone=clean_phone, error=str(e))
        return None

def _find_or_create_session(lead_id: str, phone: str) -> dict:
    """Buscar sessão ativa ou criar nova"""
    try:
        # Buscar sessão ativa
        result = simple_supabase.client.table('sessions') \
            .select('*') \
            .eq('lead_id', lead_id) \
            .eq('status', 'ativa') \
            .limit(1) \
            .execute()
        
        if result.data:
            session = result.data[0]
            logger.info("Sessão ativa encontrada", 
                       session_id=session['id'], 
                       lead_id=lead_id)
            return session
        
        # Criar nova sessão
        new_session_data = {
            'lead_id': lead_id,
            'status': 'ativa',
            'current_step': 'inicio',
            'context': {
                'phone': phone,
                'qualification_started': False,
                'answers': {},
                'conversation_history': [],
                'source': 'twilio_webhook'
            }
        }
        
        create_result = simple_supabase.client.table('sessions') \
            .insert(new_session_data) \
            .execute()
        
        if create_result.data:
            new_session = create_result.data[0]
            logger.info("Nova sessão criada via WhatsApp", 
                       session_id=new_session['id'], 
                       lead_id=lead_id)
            return new_session
        
        return None
        
    except Exception as e:
        logger.error("Erro ao buscar/criar sessão", lead_id=lead_id, error=str(e))
        return None

def _save_incoming_message(session_id: str, message_body: str, message_sid: str):
    """Salvar mensagem recebida no banco"""
    try:
        message_data = {
            'session_id': session_id,
            'direction': 'inbound',
            'content': message_body,
            'message_type': 'text',
            'twilio_sid': message_sid
        }
        
        simple_supabase.client.table('messages') \
            .insert(message_data) \
            .execute()
        
        logger.info("Mensagem recebida salva", 
                   session_id=session_id,
                   message_length=len(message_body))
        
    except Exception as e:
        logger.error("Erro ao salvar mensagem recebida", 
                    session_id=session_id, 
                    error=str(e))

def _notify_qualified_lead(lead_data: dict, score: int, context: dict):
    """Notificar consultor sobre lead qualificado (substituindo N8N)"""
    try:
        tenant_id = lead_data.get('tenant_id', '05dc8c52-c0a0-44ae-aa2a-eeaa01090a27')
        
        # Buscar configurações do tenant
        tenant_result = simple_supabase.client.table('tenants') \
            .select('settings') \
            .eq('id', tenant_id) \
            .single() \
            .execute()
        
        tenant_settings = tenant_result.data.get('settings', {}) if tenant_result.data else {}
        consultant_email = tenant_settings.get('default_consultant_email', 'consultor@exemplo.com')
        
        # Preparar dados para notificação
        notification_payload = {
            'lead_id': lead_data['id'],
            'name': lead_data['name'],
            'email': lead_data.get('email', 'Não informado'),
            'phone': lead_data['phone'],
            'score': score,
            'status': 'qualificado',
            'origem': 'WhatsApp',
            'answers': context.get('answers', {}),
            'created_at': lead_data.get('created_at'),
            'qualified_at': __import__('datetime').datetime.now().isoformat()
        }
        
        results = {}
        
        # 1. Enviar email para consultor
        email_result = email_service.send_qualified_lead_email(
            lead_data=notification_payload,
            consultant_email=consultant_email
        )
        results['email'] = email_result
        
        # 2. Enviar para CRM
        crm_result = crm_adapter.send_lead(
            tenant_id=tenant_id,
            lead_payload=notification_payload
        )
        results['crm'] = crm_result
        
        # 3. Atualizar lead no banco
        simple_supabase.client.table('leads') \
            .update({
                'status': 'qualificado',
                'score': score,
                'qualified_at': notification_payload['qualified_at']
            }) \
            .eq('id', lead_data['id']) \
            .execute()
        
        logger.info("Lead qualificado notificado (sem N8N)", 
                   lead_id=lead_data['id'],
                   score=score,
                   email_success=email_result.get('success', False),
                   crm_success=crm_result.get('success', False))
        
        return results
        
    except Exception as e:
        logger.error("Erro ao notificar lead qualificado", 
                    lead_id=lead_data.get('id'), 
                    error=str(e))
        return {'error': str(e)}

@whatsapp_bp.route('/api/whatsapp/test', methods=['POST'])
def test_whatsapp_webhook():
    """Endpoint para testar webhook do WhatsApp"""
    try:
        data = request.get_json()
        
        test_payload = {
            'Body': data.get('message', 'Tenho interesse em investir 500 mil reais'),
            'From': f"whatsapp:+{data.get('phone', '5511999888777')}",
            'To': 'whatsapp:+14155238886',
            'MessageSid': f'TEST_{int(__import__("time").time())}',
            'AccountSid': 'TEST_ACCOUNT'
        }
        
        # Simular webhook
        with whatsapp_bp.test_client() as client:
            response = client.post('/api/whatsapp/webhook', 
                                 data=test_payload,
                                 content_type='application/x-www-form-urlencoded')
        
        return jsonify({
            'success': True,
            'test_payload': test_payload,
            'webhook_response': response.get_json() if response.data else {},
            'status_code': response.status_code
        }), 200
        
    except Exception as e:
        logger.error("Erro no teste de webhook", error=str(e))
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@whatsapp_bp.route('/api/whatsapp/health', methods=['GET'])
def whatsapp_health():
    """Health check para webhook WhatsApp"""
    return jsonify({
        'status': 'healthy',
        'service': 'whatsapp_webhook',
        'endpoints': [
            'POST /api/whatsapp/webhook',
            'POST /api/whatsapp/test',
            'GET /api/whatsapp/health'
        ],
        'twilio_configured': simple_twilio.use_simulator == False,
        'simulator_mode': simple_twilio.use_simulator
    }), 200
