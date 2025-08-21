from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
import structlog
from services.supabase_service import supabase_service
from services.twilio_service import twilio_service

logger = structlog.get_logger()

chat_bp = Blueprint('chat', __name__)

def get_current_user_info():
    """Extrair informações do usuário atual do JWT"""
    claims = get_jwt()
    return {
        'user_id': claims.get('user_id'),
        'tenant_id': claims.get('tenant_id'),
        'role': claims.get('role'),
        'email': claims.get('email')
    }

@chat_bp.route('/<session_id>', methods=['GET'])
@jwt_required()
async def get_chat_history(session_id):
    """Obter histórico de mensagens de uma sessão"""
    try:
        user_info = get_current_user_info()
        tenant_id = user_info['tenant_id']
        
        # Buscar sessão e verificar se pertence ao tenant
        session = await supabase_service.get_session(session_id)
        
        if not session:
            return jsonify({"error": "Sessão não encontrada"}), 404
        
        # Verificar se a sessão pertence a um lead do tenant
        if session['leads']['tenant_id'] != tenant_id:
            return jsonify({"error": "Acesso negado"}), 403
        
        # Buscar mensagens
        messages = await supabase_service.get_messages(session_id)
        
        # Buscar dados do lead
        lead = session['leads']
        
        chat_data = {
            "session": {
                "id": session['id'],
                "status": session['status'],
                "current_step": session['current_step'],
                "context": session['context'],
                "created_at": session['created_at'],
                "updated_at": session['updated_at']
            },
            "lead": {
                "id": lead['id'],
                "name": lead['name'],
                "email": lead['email'],
                "phone": lead['phone'],
                "status": lead['status'],
                "score": lead['score'],
                "origem": lead['origem']
            },
            "messages": messages
        }
        
        return jsonify(chat_data)
        
    except Exception as e:
        logger.error("Erro ao buscar histórico do chat", session_id=session_id, error=str(e))
        return jsonify({"error": "Erro interno do servidor"}), 500

@chat_bp.route('/<session_id>/send', methods=['POST'])
@jwt_required()
async def send_message(session_id):
    """Enviar mensagem manual (takeover humano)"""
    try:
        user_info = get_current_user_info()
        tenant_id = user_info['tenant_id']
        user_id = user_info['user_id']
        
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({"error": "Mensagem é obrigatória"}), 400
        
        # Buscar sessão
        session = await supabase_service.get_session(session_id)
        
        if not session:
            return jsonify({"error": "Sessão não encontrada"}), 404
        
        if session['leads']['tenant_id'] != tenant_id:
            return jsonify({"error": "Acesso negado"}), 403
        
        # Enviar mensagem via WhatsApp
        send_result = await twilio_service.send_message(
            session['leads']['phone'],
            message
        )
        
        if not send_result['success']:
            return jsonify({
                "error": "Falha ao enviar mensagem",
                "details": send_result.get('error')
            }), 500
        
        # Salvar mensagem no banco
        message_data = {
            'session_id': session_id,
            'direction': 'outbound',
            'content': message,
            'message_type': 'text',
            'twilio_sid': send_result['message_sid']
        }
        
        saved_message = await supabase_service.create_message(message_data)
        
        # Marcar sessão como takeover humano
        context = session.get('context', {})
        context['human_takeover'] = True
        context['takeover_user_id'] = user_id
        context['takeover_at'] = saved_message['created_at']
        
        await supabase_service.update_session(session_id, {
            'context': context,
            'current_step': 'human_takeover'
        })
        
        # Log de auditoria
        await supabase_service.log_audit_event(
            tenant_id=tenant_id,
            user_id=user_id,
            action="human_takeover_message",
            resource_type="session",
            resource_id=session_id,
            details={
                "lead_id": session['lead_id'],
                "message_length": len(message),
                "twilio_sid": send_result['message_sid']
            }
        )
        
        logger.info("Mensagem manual enviada", 
                   session_id=session_id,
                   user_id=user_id,
                   message_sid=send_result['message_sid'])
        
        return jsonify({
            "success": True,
            "message": saved_message,
            "whatsapp_status": send_result['status']
        })
        
    except Exception as e:
        logger.error("Erro ao enviar mensagem manual", session_id=session_id, error=str(e))
        return jsonify({"error": "Erro interno do servidor"}), 500

@chat_bp.route('/<session_id>/takeover', methods=['POST'])
@jwt_required()
async def takeover_session(session_id):
    """Assumir controle da sessão (pausar IA)"""
    try:
        user_info = get_current_user_info()
        tenant_id = user_info['tenant_id']
        user_id = user_info['user_id']
        
        # Buscar sessão
        session = await supabase_service.get_session(session_id)
        
        if not session:
            return jsonify({"error": "Sessão não encontrada"}), 404
        
        if session['leads']['tenant_id'] != tenant_id:
            return jsonify({"error": "Acesso negado"}), 403
        
        # Atualizar sessão para takeover
        context = session.get('context', {})
        context['human_takeover'] = True
        context['takeover_user_id'] = user_id
        context['takeover_at'] = supabase_service.client.table('sessions')\
            .select('now() as timestamp')\
            .execute().data[0]['timestamp']
        
        await supabase_service.update_session(session_id, {
            'status': 'pausada',
            'context': context,
            'current_step': 'human_takeover'
        })
        
        # Log de auditoria
        await supabase_service.log_audit_event(
            tenant_id=tenant_id,
            user_id=user_id,
            action="session_takeover",
            resource_type="session",
            resource_id=session_id,
            details={"lead_id": session['lead_id']}
        )
        
        logger.info("Sessão assumida por humano", session_id=session_id, user_id=user_id)
        
        return jsonify({
            "success": True,
            "message": "Controle da sessão assumido",
            "session_status": "pausada"
        })
        
    except Exception as e:
        logger.error("Erro no takeover da sessão", session_id=session_id, error=str(e))
        return jsonify({"error": "Erro interno do servidor"}), 500

@chat_bp.route('/<session_id>/resume', methods=['POST'])
@jwt_required()
async def resume_ai_session(session_id):
    """Retomar controle da IA na sessão"""
    try:
        user_info = get_current_user_info()
        tenant_id = user_info['tenant_id']
        user_id = user_info['user_id']
        
        # Buscar sessão
        session = await supabase_service.get_session(session_id)
        
        if not session:
            return jsonify({"error": "Sessão não encontrada"}), 404
        
        if session['leads']['tenant_id'] != tenant_id:
            return jsonify({"error": "Acesso negado"}), 403
        
        # Atualizar sessão para retomar IA
        context = session.get('context', {})
        context['human_takeover'] = False
        context['resumed_by_user_id'] = user_id
        context['resumed_at'] = supabase_service.client.table('sessions')\
            .select('now() as timestamp')\
            .execute().data[0]['timestamp']
        
        await supabase_service.update_session(session_id, {
            'status': 'ativa',
            'context': context
            # current_step mantém o último step da IA
        })
        
        # Log de auditoria
        await supabase_service.log_audit_event(
            tenant_id=tenant_id,
            user_id=user_id,
            action="session_resume_ai",
            resource_type="session",
            resource_id=session_id,
            details={"lead_id": session['lead_id']}
        )
        
        logger.info("Sessão retomada pela IA", session_id=session_id, user_id=user_id)
        
        return jsonify({
            "success": True,
            "message": "Controle retomado pela IA",
            "session_status": "ativa"
        })
        
    except Exception as e:
        logger.error("Erro ao retomar sessão da IA", session_id=session_id, error=str(e))
        return jsonify({"error": "Erro interno do servidor"}), 500

@chat_bp.route('/<session_id>/close', methods=['POST'])
@jwt_required()
async def close_session(session_id):
    """Finalizar sessão"""
    try:
        user_info = get_current_user_info()
        tenant_id = user_info['tenant_id']
        user_id = user_info['user_id']
        
        data = request.get_json()
        reason = data.get('reason', 'Finalizada manualmente')
        
        # Buscar sessão
        session = await supabase_service.get_session(session_id)
        
        if not session:
            return jsonify({"error": "Sessão não encontrada"}), 404
        
        if session['leads']['tenant_id'] != tenant_id:
            return jsonify({"error": "Acesso negado"}), 403
        
        # Finalizar sessão
        context = session.get('context', {})
        context['closed_by_user_id'] = user_id
        context['close_reason'] = reason
        context['closed_at'] = supabase_service.client.table('sessions')\
            .select('now() as timestamp')\
            .execute().data[0]['timestamp']
        
        await supabase_service.update_session(session_id, {
            'status': 'finalizada',
            'context': context
        })
        
        # Log de auditoria
        await supabase_service.log_audit_event(
            tenant_id=tenant_id,
            user_id=user_id,
            action="session_closed",
            resource_type="session",
            resource_id=session_id,
            details={
                "lead_id": session['lead_id'],
                "reason": reason
            }
        )
        
        logger.info("Sessão finalizada", session_id=session_id, reason=reason)
        
        return jsonify({
            "success": True,
            "message": "Sessão finalizada com sucesso"
        })
        
    except Exception as e:
        logger.error("Erro ao finalizar sessão", session_id=session_id, error=str(e))
        return jsonify({"error": "Erro interno do servidor"}), 500




