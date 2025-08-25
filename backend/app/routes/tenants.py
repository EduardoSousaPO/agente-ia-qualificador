#!/usr/bin/env python3
"""
Rotas para gerenciamento de Tenants (Empresas) e Membros
"""

from flask import Blueprint, request, jsonify, g
from services.auth_service import require_auth, auth_service
from services.simple_supabase import simple_supabase
from utils.validators import validate_required_fields, validate_uuid, validate_email
import structlog

logger = structlog.get_logger()

tenants_bp = Blueprint('tenants', __name__)

# ========== AUTENTICAÇÃO ==========

@tenants_bp.route('/api/auth/login', methods=['POST'])
def login():
    """Login de usuário"""
    try:
        data = request.get_json()
        
        # Validar campos obrigatórios
        required_fields = ['email', 'password']
        validation_error = validate_required_fields(data, required_fields)
        if validation_error:
            return jsonify({'error': validation_error}), 400
        
        # Validar formato do email
        if not validate_email(data['email']):
            return jsonify({'error': 'Email inválido'}), 400
        
        # Fazer login
        result = auth_service.login(data['email'], data['password'])
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 401
            
    except Exception as e:
        logger.error("Erro no endpoint de login", error=str(e))
        return jsonify({'error': 'Erro interno do servidor'}), 500

@tenants_bp.route('/api/auth/me', methods=['GET'])
@require_auth()
def get_current_user():
    """Obter informações do usuário logado"""
    try:
        return jsonify({
            'success': True,
            'user': {
                'id': g.user_id,
                'tenant_id': g.tenant_id,
                'email': g.user_email,
                'role': g.user_role
            }
        }), 200
        
    except Exception as e:
        logger.error("Erro ao obter usuário atual", error=str(e))
        return jsonify({'error': 'Erro interno do servidor'}), 500

# ========== GESTÃO DE TENANTS ==========

@tenants_bp.route('/api/tenants', methods=['POST'])
@require_auth(roles=['admin'])  # Apenas admin global pode criar tenants
def create_tenant():
    """Criar nova empresa (tenant)"""
    try:
        data = request.get_json()
        
        # Validar campos obrigatórios
        required_fields = ['name']
        validation_error = validate_required_fields(data, required_fields)
        if validation_error:
            return jsonify({'error': validation_error}), 400
        
        # Dados do novo tenant
        tenant_data = {
            'name': data['name'],
            'domain': data.get('domain'),  # Opcional
            'settings': data.get('settings', {})
        }
        
        # Criar tenant no Supabase
        result = simple_supabase.client.table('tenants') \
            .insert(tenant_data) \
            .execute()
        
        if result.data:
            tenant = result.data[0]
            logger.info("Tenant criado", 
                       tenant_id=tenant['id'],
                       name=tenant['name'],
                       created_by=g.user_id)
            
            return jsonify({
                'success': True,
                'tenant': tenant,
                'message': 'Empresa criada com sucesso'
            }), 201
        else:
            return jsonify({'error': 'Falha ao criar empresa'}), 500
            
    except Exception as e:
        logger.error("Erro ao criar tenant", error=str(e))
        return jsonify({'error': 'Erro interno do servidor'}), 500

@tenants_bp.route('/api/tenants/me', methods=['GET'])
@require_auth()
def get_my_tenant():
    """Obter informações do tenant do usuário logado + membros"""
    try:
        # Buscar dados do tenant
        tenant_result = simple_supabase.client.table('tenants') \
            .select('*') \
            .eq('id', g.tenant_id) \
            .single() \
            .execute()
        
        if not tenant_result.data:
            return jsonify({'error': 'Tenant não encontrado'}), 404
        
        tenant = tenant_result.data
        
        # Buscar membros do tenant
        members_result = simple_supabase.client.table('users') \
            .select('id, email, role, name, created_at') \
            .eq('tenant_id', g.tenant_id) \
            .execute()
        
        members = members_result.data or []
        
        return jsonify({
            'success': True,
            'tenant': tenant,
            'members': members,
            'total_members': len(members)
        }), 200
        
    except Exception as e:
        logger.error("Erro ao obter dados do tenant", 
                    tenant_id=g.tenant_id, 
                    error=str(e))
        return jsonify({'error': 'Erro interno do servidor'}), 500

# ========== GESTÃO DE MEMBROS ==========

@tenants_bp.route('/api/tenants/<tenant_id>/members', methods=['POST'])
@require_auth(roles=['admin'])  # Apenas admin do tenant pode adicionar membros
def create_member(tenant_id):
    """Criar/convidar novo membro para o tenant"""
    try:
        # Verificar se o usuário pode gerenciar este tenant
        if g.tenant_id != tenant_id:
            return jsonify({'error': 'Acesso negado - tenant diferente'}), 403
        
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
        valid_roles = ['admin', 'operator', 'viewer']
        if data['role'] not in valid_roles:
            return jsonify({'error': f'Role deve ser um de: {valid_roles}'}), 400
        
        # Verificar se o email já existe
        existing_user = simple_supabase.client.table('users') \
            .select('id') \
            .eq('email', data['email']) \
            .execute()
        
        if existing_user.data:
            return jsonify({'error': 'Email já cadastrado'}), 409
        
        # Dados do novo usuário
        user_data = {
            'tenant_id': tenant_id,
            'email': data['email'],
            'role': data['role'],
            'name': data.get('name', data['email'].split('@')[0])
            # NOTA: password_hash seria definido em um fluxo de convite real
        }
        
        # Criar usuário no Supabase
        result = simple_supabase.client.table('users') \
            .insert(user_data) \
            .execute()
        
        if result.data:
            user = result.data[0]
            logger.info("Membro criado", 
                       user_id=user['id'],
                       tenant_id=tenant_id,
                       email=user['email'],
                       role=user['role'],
                       created_by=g.user_id)
            
            return jsonify({
                'success': True,
                'user': user,
                'message': 'Membro adicionado com sucesso'
            }), 201
        else:
            return jsonify({'error': 'Falha ao criar membro'}), 500
            
    except Exception as e:
        logger.error("Erro ao criar membro", 
                    tenant_id=tenant_id, 
                    error=str(e))
        return jsonify({'error': 'Erro interno do servidor'}), 500

@tenants_bp.route('/api/tenants/<tenant_id>/members', methods=['GET'])
@require_auth()
def list_members(tenant_id):
    """Listar membros do tenant"""
    try:
        # Verificar se o usuário pode ver este tenant
        if g.tenant_id != tenant_id:
            return jsonify({'error': 'Acesso negado - tenant diferente'}), 403
        
        # Buscar membros
        result = simple_supabase.client.table('users') \
            .select('id, email, role, name, created_at') \
            .eq('tenant_id', tenant_id) \
            .execute()
        
        members = result.data or []
        
        return jsonify({
            'success': True,
            'members': members,
            'total': len(members)
        }), 200
        
    except Exception as e:
        logger.error("Erro ao listar membros", 
                    tenant_id=tenant_id, 
                    error=str(e))
        return jsonify({'error': 'Erro interno do servidor'}), 500

