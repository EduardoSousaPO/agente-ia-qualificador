"""
Rotas para Join Requests - Sistema de Solicitações de Acesso à Empresa
Implementa fluxo completo de registro corporativo B2B
"""

from flask import Blueprint, request, jsonify, g
from services.auth_service import require_auth
from services.simple_supabase import simple_supabase
from utils.validators import validate_required_fields, validate_email
import structlog

logger = structlog.get_logger()
join_requests_bp = Blueprint('join_requests', __name__)

@join_requests_bp.route('/api/join-requests', methods=['POST'])
def create_join_request():
    """Criar solicitação de acesso à empresa"""
    try:
        data = request.get_json()
        required_fields = ['user_id', 'company_code', 'company_name']
        validation_error = validate_required_fields(data, required_fields)
        if validation_error:
            return jsonify({'error': validation_error}), 400

        # Garantir que o cliente Supabase está inicializado
        simple_supabase._ensure_client()

        # Verificar se empresa existe pelo código
        tenant_result = simple_supabase.client.table('tenants') \
            .select('id, name, code') \
            .eq('code', data['company_code']) \
            .single() \
            .execute()
        
        if not tenant_result.data:
            return jsonify({'error': 'Código da empresa não encontrado'}), 404
        
        tenant = tenant_result.data
        
        # Verificar se já existe solicitação
        existing_request = simple_supabase.client.table('join_requests') \
            .select('id, status') \
            .eq('tenant_id', tenant['id']) \
            .eq('user_id', data['user_id']) \
            .execute()
        
        if existing_request.data:
            status = existing_request.data[0]['status']
            if status == 'pending':
                return jsonify({'error': 'Já existe uma solicitação pendente para esta empresa'}), 409
            elif status == 'approved':
                return jsonify({'error': 'Usuário já foi aprovado para esta empresa'}), 409
        
        # Verificar se já é membro
        existing_membership = simple_supabase.client.table('memberships') \
            .select('id') \
            .eq('tenant_id', tenant['id']) \
            .eq('user_id', data['user_id']) \
            .execute()
        
        if existing_membership.data:
            return jsonify({'error': 'Usuário já é membro desta empresa'}), 409
        
        # Criar solicitação
        join_request_data = {
            'tenant_id': tenant['id'],
            'user_id': data['user_id'],
            'company_name': data['company_name'],
            'company_code': data['company_code'],
            'status': 'pending'
        }
        
        result = simple_supabase.client.table('join_requests') \
            .insert(join_request_data) \
            .execute()
        
        if result.data:
            # TODO: Enviar notificação para admins da empresa
            logger.info("Join request criado", 
                       request_id=result.data[0]['id'],
                       tenant_id=tenant['id'],
                       user_id=data['user_id'])
            
            return jsonify({
                'success': True,
                'message': 'Solicitação enviada com sucesso. Aguarde aprovação do administrador.',
                'request': result.data[0]
            }), 201
        
        return jsonify({'error': 'Falha ao criar solicitação'}), 500
        
    except Exception as e:
        logger.error("Erro ao criar join request", error=str(e))
        return jsonify({'error': 'Erro interno do servidor'}), 500

@join_requests_bp.route('/api/tenants/<tenant_id>/join-requests', methods=['GET'])
@require_auth(roles=['admin', 'owner'])
def get_tenant_join_requests(tenant_id):
    """Listar solicitações pendentes do tenant (apenas admins)"""
    try:
        # Garantir que o cliente Supabase está inicializado
        simple_supabase._ensure_client()

        # Verificar se usuário é admin do tenant
        membership_result = simple_supabase.client.table('memberships') \
            .select('role') \
            .eq('tenant_id', tenant_id) \
            .eq('user_id', g.user_id) \
            .execute()
        
        if not membership_result.data or membership_result.data[0]['role'] not in ['admin', 'owner']:
            return jsonify({'error': 'Acesso negado - permissão insuficiente'}), 403
        
        # Buscar solicitações com dados do usuário
        requests_result = simple_supabase.client.table('join_requests') \
            .select('''
                id,
                user_id,
                company_name,
                company_code,
                status,
                created_at,
                approved_at
            ''') \
            .eq('tenant_id', tenant_id) \
            .order('created_at', desc=True) \
            .execute()
        
        # Buscar dados dos usuários para cada solicitação
        for request in requests_result.data:
            # Buscar dados do usuário no auth.users (via profiles)
            user_result = simple_supabase.client.table('profiles') \
                .select('user_id') \
                .eq('user_id', request['user_id']) \
                .single() \
                .execute()
            
            if user_result.data:
                # Por enquanto usar dados placeholder - implementar busca real depois
                request['user_email'] = f"user-{request['user_id'][:8]}@example.com"
                request['user_name'] = f"Usuário {request['user_id'][:8]}"
            else:
                request['user_email'] = 'Email não encontrado'
                request['user_name'] = 'Nome não encontrado'
        
        return jsonify({
            'success': True,
            'requests': requests_result.data or []
        }), 200
        
    except Exception as e:
        logger.error("Erro ao buscar join requests", 
                    tenant_id=tenant_id, error=str(e))
        return jsonify({'error': 'Erro interno do servidor'}), 500

@join_requests_bp.route('/api/join-requests/<request_id>/approve', methods=['POST'])
@require_auth(roles=['admin', 'owner'])
def approve_join_request(request_id):
    """Aprovar solicitação de acesso"""
    try:
        # Garantir que o cliente Supabase está inicializado
        simple_supabase._ensure_client()

        # Buscar solicitação
        request_result = simple_supabase.client.table('join_requests') \
            .select('*') \
            .eq('id', request_id) \
            .eq('status', 'pending') \
            .single() \
            .execute()
        
        if not request_result.data:
            return jsonify({'error': 'Solicitação não encontrada ou já processada'}), 404
        
        join_request = request_result.data
        
        # Verificar se usuário pode aprovar (é admin do tenant)
        membership_result = simple_supabase.client.table('memberships') \
            .select('role') \
            .eq('tenant_id', join_request['tenant_id']) \
            .eq('user_id', g.user_id) \
            .execute()
        
        if not membership_result.data or membership_result.data[0]['role'] not in ['admin', 'owner']:
            return jsonify({'error': 'Acesso negado - permissão insuficiente'}), 403
        
        data = request.get_json()
        role = data.get('role', 'member') if data else 'member'  # Default role
        
        # Criar membership
        membership_data = {
            'tenant_id': join_request['tenant_id'],
            'user_id': join_request['user_id'],
            'role': role
        }
        
        membership_result = simple_supabase.client.table('memberships') \
            .insert(membership_data) \
            .execute()
        
        if membership_result.data:
            # Atualizar status da solicitação
            simple_supabase.client.table('join_requests') \
                .update({
                    'status': 'approved',
                    'approved_by': g.user_id,
                    'approved_at': 'now()'
                }) \
                .eq('id', request_id) \
                .execute()
            
            logger.info("Join request aprovado", 
                       request_id=request_id,
                       tenant_id=join_request['tenant_id'],
                       user_id=join_request['user_id'],
                       approved_by=g.user_id)
            
            return jsonify({
                'success': True,
                'message': 'Solicitação aprovada com sucesso',
                'membership': membership_result.data[0]
            }), 200
        
        return jsonify({'error': 'Falha ao criar membership'}), 500
        
    except Exception as e:
        logger.error("Erro ao aprovar join request", 
                    request_id=request_id, error=str(e))
        return jsonify({'error': 'Erro interno do servidor'}), 500

@join_requests_bp.route('/api/join-requests/<request_id>/reject', methods=['POST'])
@require_auth(roles=['admin', 'owner'])
def reject_join_request(request_id):
    """Rejeitar solicitação de acesso"""
    try:
        # Garantir que o cliente Supabase está inicializado
        simple_supabase._ensure_client()

        # Buscar solicitação
        request_result = simple_supabase.client.table('join_requests') \
            .select('*') \
            .eq('id', request_id) \
            .eq('status', 'pending') \
            .single() \
            .execute()
        
        if not request_result.data:
            return jsonify({'error': 'Solicitação não encontrada ou já processada'}), 404
        
        join_request = request_result.data
        
        # Verificar permissão
        membership_result = simple_supabase.client.table('memberships') \
            .select('role') \
            .eq('tenant_id', join_request['tenant_id']) \
            .eq('user_id', g.user_id) \
            .execute()
        
        if not membership_result.data or membership_result.data[0]['role'] not in ['admin', 'owner']:
            return jsonify({'error': 'Acesso negado - permissão insuficiente'}), 403
        
        # Atualizar status
        result = simple_supabase.client.table('join_requests') \
            .update({
                'status': 'rejected',
                'approved_by': g.user_id,
                'approved_at': 'now()'
            }) \
            .eq('id', request_id) \
            .execute()
        
        if result.data:
            logger.info("Join request rejeitado", 
                       request_id=request_id,
                       tenant_id=join_request['tenant_id'],
                       user_id=join_request['user_id'],
                       rejected_by=g.user_id)
            
            return jsonify({
                'success': True,
                'message': 'Solicitação rejeitada'
            }), 200
        
        return jsonify({'error': 'Falha ao rejeitar solicitação'}), 500
        
    except Exception as e:
        logger.error("Erro ao rejeitar join request", 
                    request_id=request_id, error=str(e))
        return jsonify({'error': 'Erro interno do servidor'}), 500

# Rota adicional para verificar se um company code existe (para validação no frontend)
@join_requests_bp.route('/api/company-code/<code>/validate', methods=['GET'])
def validate_company_code(code):
    """Validar se código da empresa existe"""
    try:
        # Garantir que o cliente Supabase está inicializado
        simple_supabase._ensure_client()

        # Buscar empresa pelo código
        tenant_result = simple_supabase.client.table('tenants') \
            .select('id, name, code') \
            .eq('code', code) \
            .single() \
            .execute()
        
        if tenant_result.data:
            return jsonify({
                'valid': True,
                'company_name': tenant_result.data['name']
            }), 200
        else:
            return jsonify({'valid': False}), 200
        
    except Exception as e:
        logger.error("Erro ao validar company code", code=code, error=str(e))
        return jsonify({'error': 'Erro interno do servidor'}), 500










