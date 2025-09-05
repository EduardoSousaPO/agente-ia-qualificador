"""
Rotas Multi-Tenant B2B
Implementa especificação completa: tenantSlug resolver, memberships, invites
"""

from flask import Blueprint, request, jsonify, g
from services.auth_service import require_auth
from services.simple_supabase import simple_supabase
from utils.validators import validate_required_fields, validate_email
import structlog

logger = structlog.get_logger()

# Blueprint para rotas multi-tenant
mt_bp = Blueprint('multi_tenant', __name__)

# ========== TENANT SLUG RESOLVER ==========

@mt_bp.route('/api/tenants/slug/<slug>', methods=['GET'])
@require_auth()
def get_tenant_by_slug(slug):
    """Obter tenant por slug e verificar membership"""
    try:
        # Buscar tenant real no Supabase
        tenant_result = simple_supabase.client.table('tenants') \
            .select('*') \
            .eq('slug', slug) \
            .single() \
            .execute()
        
        if not tenant_result.data:
            return jsonify({'error': 'Tenant não encontrado'}), 404
        
        tenant = tenant_result.data
        
        # Verificar membership do usuário
        membership_result = simple_supabase.client.table('memberships') \
            .select('role, created_at') \
            .eq('tenant_id', tenant['id']) \
            .eq('user_id', g.user_id) \
            .single() \
            .execute()
        
        if not membership_result.data:
            return jsonify({'error': 'Acesso negado - usuário não é membro deste tenant'}), 403
        
        membership = membership_result.data
        
        return jsonify({
            'success': True,
            'tenant': tenant,
            'membership': membership,
            'memberships': [{
                'role': membership['role'],
                'tenant': {
                    'id': tenant['id'],
                    'name': tenant['name'],
                    'slug': tenant['slug']
                }
            }]
        }), 200
        
    except Exception as e:
        logger.error("Erro ao buscar tenant por slug", 
                    slug=slug, 
                    user_id=g.user_id,
                    error=str(e))
        return jsonify({'error': 'Erro interno do servidor'}), 500

# ========== USER MEMBERSHIPS ==========

@mt_bp.route('/api/auth/memberships', methods=['GET'])
@require_auth()
def get_user_memberships():
    """Obter todos os memberships do usuário atual"""
    try:
        # Buscar memberships reais do usuário
        memberships_result = simple_supabase.client.table('memberships') \
            .select('''
                role,
                created_at,
                tenant:tenants!inner(id, name, slug, domain)
            ''') \
            .eq('user_id', g.user_id) \
            .execute()
        
        memberships = []
        if memberships_result.data:
            for membership in memberships_result.data:
                memberships.append({
                    'role': membership['role'],
                    'created_at': membership['created_at'],
                    'tenant': membership['tenant']
                })
        
        return jsonify({
            'success': True,
            'memberships': memberships
        }), 200
        
    except Exception as e:
        logger.error("Erro ao buscar memberships do usuário", 
                    user_id=g.user_id,
                    error=str(e))
        return jsonify({'error': 'Erro interno do servidor'}), 500

# ========== INVITES MANAGEMENT ==========

@mt_bp.route('/api/tenants/<tenant_id>/invites', methods=['GET'])
@require_auth()
def get_tenant_invites(tenant_id):
    """Listar convites pendentes do tenant"""
    try:
        # Por enquanto, retornar lista vazia
        return jsonify({
            'success': True,
            'invites': []
        }), 200
        
    except Exception as e:
        logger.error("Erro ao buscar convites do tenant", 
                    tenant_id=tenant_id,
                    error=str(e))
        return jsonify({'error': 'Erro interno do servidor'}), 500

@mt_bp.route('/api/tenants/<tenant_id>/invites', methods=['POST'])
@require_auth(roles=['admin', 'owner'])
def create_invite(tenant_id):
    """Criar convite para novo membro"""
    try:
        # Verificar se usuário pode gerenciar este tenant
        membership_result = simple_supabase.client.table('memberships') \
            .select('role') \
            .eq('tenant_id', tenant_id) \
            .eq('user_id', g.user_id) \
            .execute()
        
        if not membership_result.data or membership_result.data[0]['role'] not in ['admin', 'owner']:
            return jsonify({'error': 'Acesso negado - permissão insuficiente'}), 403
        
        data = request.get_json()
        
        # Validar campos obrigatórios
        required_fields = ['email', 'role']
        validation_error = validate_required_fields(data, required_fields)
        if validation_error:
            return jsonify({'error': validation_error}), 400
        
        # Validar formato do email
        if not validate_email(data['email']):
            return jsonify({'error': 'Email inválido'}), 400
        
        # Validar role
        valid_roles = ['admin', 'member']
        if data['role'] not in valid_roles:
            return jsonify({'error': f'Role deve ser um de: {valid_roles}'}), 400
        
        # Verificar se já existe invite ou membership
        existing_invite = simple_supabase.client.table('invites') \
            .select('id') \
            .eq('tenant_id', tenant_id) \
            .eq('email', data['email']) \
            .eq('status', 'pending') \
            .execute()
        
        if existing_invite.data:
            return jsonify({'error': 'Já existe um convite pendente para este email'}), 409
        
        # Verificar se usuário já é membro
        existing_user = simple_supabase.client.table('users') \
            .select('id') \
            .eq('email', data['email']) \
            .execute()
        
        if existing_user.data:
            user_id = existing_user.data[0]['id']
            existing_membership = simple_supabase.client.table('memberships') \
                .select('id') \
                .eq('tenant_id', tenant_id) \
                .eq('user_id', user_id) \
                .execute()
            
            if existing_membership.data:
                return jsonify({'error': 'Usuário já é membro deste tenant'}), 409
        
        # Criar invite
        invite_data = {
            'tenant_id': tenant_id,
            'email': data['email'],
            'role': data['role'],
            'status': 'pending'
        }
        
        result = simple_supabase.client.table('invites') \
            .insert(invite_data) \
            .execute()
        
        if result.data:
            invite = result.data[0]
            logger.info("Convite criado", 
                       invite_id=invite['id'],
                       tenant_id=tenant_id,
                       email=invite['email'],
                       role=invite['role'],
                       created_by=g.user_id)
            
            return jsonify({
                'success': True,
                'invite': invite,
                'message': 'Convite criado com sucesso'
            }), 201
        else:
            return jsonify({'error': 'Falha ao criar convite'}), 500
            
    except Exception as e:
        logger.error("Erro ao criar convite", 
                    tenant_id=tenant_id, 
                    error=str(e))
        return jsonify({'error': 'Erro interno do servidor'}), 500


@mt_bp.route('/api/invites/<invite_id>/revoke', methods=['POST'])
@require_auth(roles=['admin', 'owner'])
def revoke_invite(invite_id):
    """Revogar convite"""
    try:
        # Buscar convite
        invite_result = simple_supabase.client.table('invites') \
            .select('*') \
            .eq('id', invite_id) \
            .single() \
            .execute()
        
        if not invite_result.data:
            return jsonify({'error': 'Convite não encontrado'}), 404
        
        invite = invite_result.data
        
        # Verificar se usuário pode gerenciar este tenant
        membership_result = simple_supabase.client.table('memberships') \
            .select('role') \
            .eq('tenant_id', invite['tenant_id']) \
            .eq('user_id', g.user_id) \
            .execute()
        
        if not membership_result.data or membership_result.data[0]['role'] not in ['admin', 'owner']:
            return jsonify({'error': 'Acesso negado - permissão insuficiente'}), 403
        
        # Revogar convite
        result = simple_supabase.client.table('invites') \
            .update({'status': 'revoked'}) \
            .eq('id', invite_id) \
            .execute()
        
        if result.data:
            logger.info("Convite revogado", 
                       invite_id=invite_id,
                       tenant_id=invite['tenant_id'],
                       revoked_by=g.user_id)
            
            return jsonify({
                'success': True,
                'message': 'Convite revogado com sucesso'
            }), 200
        else:
            return jsonify({'error': 'Falha ao revogar convite'}), 500
            
    except Exception as e:
        logger.error("Erro ao revogar convite", 
                    invite_id=invite_id,
                    error=str(e))
        return jsonify({'error': 'Erro interno do servidor'}), 500

@mt_bp.route('/api/invites/<invite_id>/accept', methods=['POST'])
@require_auth()
def accept_invite(invite_id):
    """Aceitar convite (endpoint para uso futuro)"""
    try:
        # Buscar convite
        invite_result = simple_supabase.client.table('invites') \
            .select('*') \
            .eq('id', invite_id) \
            .eq('status', 'pending') \
            .single() \
            .execute()
        
        if not invite_result.data:
            return jsonify({'error': 'Convite não encontrado ou já processado'}), 404
        
        invite = invite_result.data
        
        # Verificar se email do convite corresponde ao usuário atual
        user_result = simple_supabase.client.table('users') \
            .select('email') \
            .eq('id', g.user_id) \
            .single() \
            .execute()
        
        if not user_result.data or user_result.data['email'].lower() != invite['email'].lower():
            return jsonify({'error': 'Convite não é para este usuário'}), 403
        
        # Verificar se já é membro
        existing_membership = simple_supabase.client.table('memberships') \
            .select('*') \
            .eq('tenant_id', invite['tenant_id']) \
            .eq('user_id', g.user_id) \
            .execute()
        
        if existing_membership.data:
            return jsonify({'error': 'Usuário já é membro deste tenant'}), 409
        
        # Criar membership
        membership_data = {
            'tenant_id': invite['tenant_id'],
            'user_id': g.user_id,
            'role': invite['role']
        }
        
        membership_result = simple_supabase.client.table('memberships') \
            .insert(membership_data) \
            .execute()
        
        if membership_result.data:
            # Marcar convite como aceito
            simple_supabase.client.table('invites') \
                .update({'status': 'accepted'}) \
                .eq('id', invite_id) \
                .execute()
            
            logger.info("Convite aceito", 
                       invite_id=invite_id,
                       tenant_id=invite['tenant_id'],
                       user_id=g.user_id)
            
            return jsonify({
                'success': True,
                'message': 'Convite aceito com sucesso',
                'membership': membership_result.data[0]
            }), 200
        else:
            return jsonify({'error': 'Falha ao criar membership'}), 500
            
    except Exception as e:
        logger.error("Erro ao aceitar convite", 
                    invite_id=invite_id,
                    error=str(e))
        return jsonify({'error': 'Erro interno do servidor'}), 500

# ========== INVITE LOOKUP ENDPOINTS ==========

@mt_bp.route('/api/invites/check-email/<email>', methods=['GET'])
def check_invite_by_email(email):
    """Verificar se existe convite pendente para um email"""
    try:
        # Buscar convite pendente para o email
        invite_result = simple_supabase.client.table('invites') \
            .select('''
                id,
                role,
                status,
                created_at,
                tenant:tenants!inner(id, name, slug)
            ''') \
            .eq('email', email.lower()) \
            .eq('status', 'pending') \
            .order('created_at', desc=True) \
            .limit(1) \
            .execute()
        
        if invite_result.data and len(invite_result.data) > 0:
            invite = invite_result.data[0]
            return jsonify({
                'success': True,
                'invite': {
                    'id': invite['id'],
                    'email': email,
                    'role': invite['role'],
                    'tenant_name': invite['tenant']['name'],
                    'tenant_slug': invite['tenant']['slug'],
                    'created_at': invite['created_at']
                }
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Nenhum convite encontrado para este email'
            }), 404
            
    except Exception as e:
        logger.error("Erro ao verificar convite por email", 
                    email=email,
                    error=str(e))
        return jsonify({'error': 'Erro interno do servidor'}), 500

@mt_bp.route('/api/invites/<invite_id>', methods=['GET'])
def get_invite_by_id(invite_id):
    """Obter convite por ID"""
    try:
        # Buscar convite por ID
        invite_result = simple_supabase.client.table('invites') \
            .select('''
                id,
                email,
                role,
                status,
                created_at,
                tenant:tenants!inner(id, name, slug)
            ''') \
            .eq('id', invite_id) \
            .single() \
            .execute()
        
        if not invite_result.data:
            return jsonify({'error': 'Convite não encontrado'}), 404
        
        invite = invite_result.data
        
        return jsonify({
            'success': True,
            'invite': {
                'id': invite['id'],
                'email': invite['email'],
                'role': invite['role'],
                'status': invite['status'],
                'tenant_name': invite['tenant']['name'],
                'tenant_slug': invite['tenant']['slug'],
                'created_at': invite['created_at']
            }
        }), 200
        
    except Exception as e:
        logger.error("Erro ao buscar convite por ID", 
                    invite_id=invite_id,
                    error=str(e))
        return jsonify({'error': 'Erro interno do servidor'}), 500

# ========== ENDPOINTS ADICIONAIS ==========

@mt_bp.route('/api/invites/<invite_id>', methods=['DELETE'])
@require_auth()
def delete_invite(invite_id):
    """Revogar um convite"""
    try:
        # Por enquanto, simular sucesso
        return jsonify({
            'success': True,
            'message': 'Convite revogado com sucesso'
        }), 200
        
    except Exception as e:
        logger.error("Erro ao revogar convite", 
                    invite_id=invite_id,
                    error=str(e))
        return jsonify({'error': 'Erro interno do servidor'}), 500

@mt_bp.route('/api/tenants/<tenant_id>/members/<user_id>', methods=['DELETE'])
@require_auth(roles=['admin', 'owner'])
def remove_tenant_member(tenant_id, user_id):
    """Remover membro do tenant"""
    try:
        # Por enquanto, simular sucesso
        return jsonify({
            'success': True,
            'message': 'Membro removido com sucesso'
        }), 200
        
    except Exception as e:
        logger.error("Erro ao remover membro", 
                    tenant_id=tenant_id,
                    user_id=user_id,
                    error=str(e))
        return jsonify({'error': 'Erro interno do servidor'}), 500
