#!/usr/bin/env python3
"""
Rotas para Base de Conhecimento e Feedback do Agente
"""

from flask import Blueprint, request, jsonify
from services.simple_supabase import simple_supabase
from utils.validators import validate_required_fields, validate_uuid
import structlog

logger = structlog.get_logger()

knowledge_bp = Blueprint('knowledge', __name__)

@knowledge_bp.route('/api/knowledge-base', methods=['POST'])
def save_knowledge_base():
    """Salvar/atualizar base de conhecimento do tenant"""
    try:
        data = request.get_json()
        
        # Validar campos obrigatórios
        required_fields = ['tenant_id', 'user_id', 'content']
        validation_error = validate_required_fields(data, required_fields)
        if validation_error:
            return jsonify({'error': validation_error}), 400
        
        # Validar UUIDs
        if not validate_uuid(data['tenant_id']) or not validate_uuid(data['user_id']):
            return jsonify({'error': 'tenant_id e user_id devem ser UUIDs válidos'}), 400
        
        # Verificar se já existe conhecimento para este tenant
        existing = simple_supabase.client.table('knowledge_base') \
            .select('id') \
            .eq('tenant_id', data['tenant_id']) \
            .execute()
        
        if existing.data:
            # Atualizar existente
            result = simple_supabase.client.table('knowledge_base') \
                .update({
                    'content': data['content'],
                    'user_id': data['user_id'],
                    'updated_at': 'now()'
                }) \
                .eq('tenant_id', data['tenant_id']) \
                .execute()
            
            logger.info("Base de conhecimento atualizada", 
                       tenant_id=data['tenant_id'])
        else:
            # Criar novo
            result = simple_supabase.client.table('knowledge_base') \
                .insert({
                    'tenant_id': data['tenant_id'],
                    'user_id': data['user_id'],
                    'content': data['content']
                }) \
                .execute()
            
            logger.info("Base de conhecimento criada", 
                       tenant_id=data['tenant_id'])
        
        return jsonify({
            'success': True,
            'message': 'Base de conhecimento salva com sucesso',
            'data': result.data[0] if result.data else None
        })
        
    except Exception as e:
        logger.error("Erro ao salvar base de conhecimento", error=str(e))
        return jsonify({'error': 'Erro interno do servidor'}), 500

@knowledge_bp.route('/api/knowledge-base/<tenant_id>', methods=['GET'])
def get_knowledge_base(tenant_id):
    """Buscar base de conhecimento do tenant"""
    try:
        # Validar UUID
        if not validate_uuid(tenant_id):
            return jsonify({'error': 'tenant_id deve ser um UUID válido'}), 400
        
        # Buscar conhecimento
        result = simple_supabase.client.table('knowledge_base') \
            .select('*') \
            .eq('tenant_id', tenant_id) \
            .execute()
        
        if result.data:
            return jsonify({
                'success': True,
                'data': result.data[0]
            })
        else:
            return jsonify({
                'success': True,
                'data': None,
                'message': 'Nenhuma base de conhecimento encontrada'
            })
        
    except Exception as e:
        logger.error("Erro ao buscar base de conhecimento", error=str(e))
        return jsonify({'error': 'Erro interno do servidor'}), 500

@knowledge_bp.route('/api/agent-feedback', methods=['POST'])
def save_agent_feedback():
    """Registrar feedback sobre mensagem do agente"""
    try:
        data = request.get_json()
        
        # Validar campos obrigatórios
        required_fields = ['tenant_id', 'user_id', 'session_id', 'agent_message', 'status']
        validation_error = validate_required_fields(data, required_fields)
        if validation_error:
            return jsonify({'error': validation_error}), 400
        
        # Validar UUIDs
        if not all(validate_uuid(data[field]) for field in ['tenant_id', 'user_id', 'session_id']):
            return jsonify({'error': 'tenant_id, user_id e session_id devem ser UUIDs válidos'}), 400
        
        # Validar status
        if data['status'] not in ['approved', 'rejected']:
            return jsonify({'error': 'status deve ser "approved" ou "rejected"'}), 400
        
        # Verificar se session existe
        session_check = simple_supabase.client.table('sessions') \
            .select('id') \
            .eq('id', data['session_id']) \
            .execute()
        
        if not session_check.data:
            return jsonify({'error': 'Sessão não encontrada'}), 404
        
        # Criar feedback
        result = simple_supabase.client.table('agent_feedback') \
            .insert({
                'tenant_id': data['tenant_id'],
                'user_id': data['user_id'],
                'session_id': data['session_id'],
                'agent_message': data['agent_message'],
                'status': data['status'],
                'notes': data.get('notes')
            }) \
            .execute()
        
        logger.info("Feedback do agente registrado", 
                   session_id=data['session_id'],
                   status=data['status'])
        
        return jsonify({
            'success': True,
            'message': 'Feedback registrado com sucesso',
            'data': result.data[0] if result.data else None
        })
        
    except Exception as e:
        logger.error("Erro ao registrar feedback", error=str(e))
        return jsonify({'error': 'Erro interno do servidor'}), 500

@knowledge_bp.route('/api/agent-feedback/<tenant_id>', methods=['GET'])
def get_agent_feedback(tenant_id):
    """Buscar histórico de feedback do tenant"""
    try:
        # Validar UUID
        if not validate_uuid(tenant_id):
            return jsonify({'error': 'tenant_id deve ser um UUID válido'}), 400
        
        # Parâmetros de paginação
        page = int(request.args.get('page', 1))
        limit = min(int(request.args.get('limit', 20)), 100)  # Máximo 100
        offset = (page - 1) * limit
        
        # Filtros opcionais
        status_filter = request.args.get('status')
        
        # Query base
        query = simple_supabase.client.table('agent_feedback') \
            .select('''
                *,
                sessions!inner(
                    id,
                    current_step,
                    leads!inner(
                        name,
                        phone
                    )
                )
            ''') \
            .eq('tenant_id', tenant_id) \
            .order('created_at', desc=True)
        
        # Aplicar filtro de status se fornecido
        if status_filter and status_filter in ['approved', 'rejected']:
            query = query.eq('status', status_filter)
        
        # Executar query com paginação
        result = query.range(offset, offset + limit - 1).execute()
        
        # Contar total
        count_result = simple_supabase.client.table('agent_feedback') \
            .select('id', count='exact') \
            .eq('tenant_id', tenant_id)
        
        if status_filter:
            count_result = count_result.eq('status', status_filter)
        
        count_result = count_result.execute()
        total = count_result.count
        
        return jsonify({
            'success': True,
            'data': result.data,
            'pagination': {
                'page': page,
                'limit': limit,
                'total': total,
                'pages': (total + limit - 1) // limit
            }
        })
        
    except Exception as e:
        logger.error("Erro ao buscar feedback", error=str(e))
        return jsonify({'error': 'Erro interno do servidor'}), 500

@knowledge_bp.route('/api/agent-messages/<session_id>', methods=['GET'])
def get_agent_messages_for_feedback(session_id):
    """Buscar mensagens do agente de uma sessão para feedback"""
    try:
        # Validar UUID
        if not validate_uuid(session_id):
            return jsonify({'error': 'session_id deve ser um UUID válido'}), 400
        
        # Buscar mensagens do agente (outbound) desta sessão
        result = simple_supabase.client.table('messages') \
            .select('''
                *,
                sessions!inner(
                    id,
                    current_step,
                    leads!inner(
                        name,
                        phone,
                        tenant_id
                    )
                )
            ''') \
            .eq('session_id', session_id) \
            .eq('direction', 'outbound') \
            .order('created_at', desc=False) \
            .execute()
        
        # Verificar se já existe feedback para cada mensagem
        if result.data:
            message_ids = [msg['id'] for msg in result.data]
            feedback_result = simple_supabase.client.table('agent_feedback') \
                .select('agent_message, status') \
                .in_('session_id', [session_id]) \
                .execute()
            
            # Criar mapa de feedback existente
            feedback_map = {fb['agent_message']: fb['status'] for fb in feedback_result.data}
            
            # Adicionar status de feedback a cada mensagem
            for msg in result.data:
                msg['feedback_status'] = feedback_map.get(msg['content'])
        
        return jsonify({
            'success': True,
            'data': result.data
        })
        
    except Exception as e:
        logger.error("Erro ao buscar mensagens do agente", error=str(e))
        return jsonify({'error': 'Erro interno do servidor'}), 500
