"""
Rotas para Gerenciamento de Empresas - Interface Admin
Permite criar, editar e gerenciar empresas via frontend
"""

from flask import Blueprint, request, jsonify, g
from services.auth_service import require_auth
from services.simple_supabase import simple_supabase
from utils.validators import validate_required_fields
import structlog
import re

logger = structlog.get_logger()
companies_bp = Blueprint('companies', __name__)

def validate_company_code(code):
    """Validar formato do código da empresa"""
    if not code or len(code) < 4 or len(code) > 20:
        return False
    # Apenas letras e números, sem espaços
    return bool(re.match(r'^[A-Z0-9]+$', code))

def generate_slug(name):
    """Gerar slug a partir do nome da empresa"""
    slug = name.lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)  # Remove caracteres especiais
    slug = re.sub(r'\s+', '-', slug)  # Substitui espaços por hífens
    slug = re.sub(r'-+', '-', slug)   # Remove hífens duplos
    return slug.strip('-')

@companies_bp.route('/api/companies', methods=['GET'])
@require_auth(roles=['admin', 'super_admin'])
def list_companies():
    """Listar todas as empresas (apenas super-admin ou admin global)"""
    try:
        simple_supabase._ensure_client()
        
        # Buscar todas as empresas
        result = simple_supabase.client.table('tenants') \
            .select('id, name, slug, code, created_at, settings') \
            .order('name') \
            .execute()
        
        companies = result.data or []
        
        # Para cada empresa, buscar quantidade de membros
        for company in companies:
            try:
                members_result = simple_supabase.client.table('memberships') \
                    .select('*', count='exact') \
                    .eq('tenant_id', company['id']) \
                    .execute()
                
                company['member_count'] = members_result.count or 0
                
                # Buscar quantidade de solicitações pendentes
                requests_result = simple_supabase.client.table('join_requests') \
                    .select('id', count='exact') \
                    .eq('tenant_id', company['id']) \
                    .eq('status', 'pending') \
                    .execute()
                
                company['pending_requests'] = requests_result.count or 0
                
            except Exception as e:
                logger.warning("Erro ao buscar estatísticas da empresa", 
                             company_id=company['id'], error=str(e))
                company['member_count'] = 0
                company['pending_requests'] = 0
        
        return jsonify({
            'success': True,
            'companies': companies,
            'total': len(companies)
        }), 200
        
    except Exception as e:
        logger.error("Erro ao listar empresas", error=str(e))
        return jsonify({'error': 'Erro interno do servidor'}), 500

@companies_bp.route('/api/companies', methods=['POST'])
@require_auth(roles=['admin', 'super_admin'])
def create_company():
    """Criar nova empresa"""
    try:
        data = request.get_json()
        required_fields = ['name', 'code']
        validation_error = validate_required_fields(data, required_fields)
        if validation_error:
            return jsonify({'error': validation_error}), 400
        
        # Validar código da empresa
        code = data['code'].upper().strip()
        if not validate_company_code(code):
            return jsonify({'error': 'Código deve ter 4-20 caracteres, apenas letras e números'}), 400
        
        # Gerar slug automaticamente se não fornecido
        slug = data.get('slug', '').strip()
        if not slug:
            slug = generate_slug(data['name'])
        
        # Validar se código já existe
        simple_supabase._ensure_client()
        existing_code = simple_supabase.client.table('tenants') \
            .select('id') \
            .eq('code', code) \
            .execute()
        
        if existing_code.data:
            return jsonify({'error': f'Código "{code}" já está em uso'}), 409
        
        # Validar se slug já existe
        existing_slug = simple_supabase.client.table('tenants') \
            .select('id') \
            .eq('slug', slug) \
            .execute()
        
        if existing_slug.data:
            return jsonify({'error': f'Slug "{slug}" já está em uso'}), 409
        
        # Preparar dados da empresa
        company_data = {
            'name': data['name'].strip(),
            'slug': slug,
            'code': code,
            'settings': {
                'company_type': data.get('company_type', 'investment_advisory'),
                'max_members': int(data.get('max_members', 50)),
                'description': data.get('description', ''),
                'created_by': g.user_id
            }
        }
        
        # Criar empresa
        result = simple_supabase.client.table('tenants') \
            .insert(company_data) \
            .execute()
        
        if result.data:
            company = result.data[0]
            company['member_count'] = 0
            company['pending_requests'] = 0
            
            logger.info("Nova empresa criada", 
                       company_id=company['id'],
                       name=company['name'],
                       code=company['code'],
                       created_by=g.user_id)
            
            return jsonify({
                'success': True,
                'message': f'Empresa "{data["name"]}" criada com sucesso!',
                'company': company
            }), 201
        
        return jsonify({'error': 'Falha ao criar empresa'}), 500
        
    except Exception as e:
        logger.error("Erro ao criar empresa", error=str(e))
        return jsonify({'error': 'Erro interno do servidor'}), 500

@companies_bp.route('/api/companies/<company_id>', methods=['PUT'])
@require_auth(roles=['admin', 'super_admin'])
def update_company(company_id):
    """Atualizar empresa existente"""
    try:
        data = request.get_json()
        
        # Buscar empresa existente
        simple_supabase._ensure_client()
        existing_result = simple_supabase.client.table('tenants') \
            .select('*') \
            .eq('id', company_id) \
            .single() \
            .execute()
        
        if not existing_result.data:
            return jsonify({'error': 'Empresa não encontrada'}), 404
        
        existing_company = existing_result.data
        
        # Preparar dados para atualização
        update_data = {}
        
        if 'name' in data and data['name'].strip():
            update_data['name'] = data['name'].strip()
        
        if 'code' in data and data['code'].strip():
            new_code = data['code'].upper().strip()
            if not validate_company_code(new_code):
                return jsonify({'error': 'Código deve ter 4-20 caracteres, apenas letras e números'}), 400
            
            # Verificar se código já existe (exceto na empresa atual)
            if new_code != existing_company['code']:
                existing_code = simple_supabase.client.table('tenants') \
                    .select('id') \
                    .eq('code', new_code) \
                    .neq('id', company_id) \
                    .execute()
                
                if existing_code.data:
                    return jsonify({'error': f'Código "{new_code}" já está em uso'}), 409
            
            update_data['code'] = new_code
        
        if 'slug' in data and data['slug'].strip():
            new_slug = data['slug'].strip()
            # Verificar se slug já existe (exceto na empresa atual)
            if new_slug != existing_company['slug']:
                existing_slug = simple_supabase.client.table('tenants') \
                    .select('id') \
                    .eq('slug', new_slug) \
                    .neq('id', company_id) \
                    .execute()
                
                if existing_slug.data:
                    return jsonify({'error': f'Slug "{new_slug}" já está em uso'}), 409
            
            update_data['slug'] = new_slug
        
        # Atualizar settings se fornecido
        if any(key in data for key in ['company_type', 'max_members', 'description']):
            current_settings = existing_company.get('settings', {})
            
            if 'company_type' in data:
                current_settings['company_type'] = data['company_type']
            if 'max_members' in data:
                current_settings['max_members'] = int(data['max_members'])
            if 'description' in data:
                current_settings['description'] = data['description']
            
            current_settings['updated_by'] = g.user_id
            update_data['settings'] = current_settings
        
        if not update_data:
            return jsonify({'error': 'Nenhum dado para atualizar'}), 400
        
        # Atualizar empresa
        result = simple_supabase.client.table('tenants') \
            .update(update_data) \
            .eq('id', company_id) \
            .execute()
        
        if result.data:
            company = result.data[0]
            
            logger.info("Empresa atualizada", 
                       company_id=company_id,
                       updated_fields=list(update_data.keys()),
                       updated_by=g.user_id)
            
            return jsonify({
                'success': True,
                'message': 'Empresa atualizada com sucesso!',
                'company': company
            }), 200
        
        return jsonify({'error': 'Falha ao atualizar empresa'}), 500
        
    except Exception as e:
        logger.error("Erro ao atualizar empresa", company_id=company_id, error=str(e))
        return jsonify({'error': 'Erro interno do servidor'}), 500

@companies_bp.route('/api/companies/<company_id>/stats', methods=['GET'])
@require_auth(roles=['admin', 'super_admin'])
def get_company_stats(company_id):
    """Obter estatísticas detalhadas da empresa"""
    try:
        simple_supabase._ensure_client()
        
        # Buscar empresa
        company_result = simple_supabase.client.table('tenants') \
            .select('*') \
            .eq('id', company_id) \
            .single() \
            .execute()
        
        if not company_result.data:
            return jsonify({'error': 'Empresa não encontrada'}), 404
        
        company = company_result.data
        
        # Estatísticas de membros
        members_result = simple_supabase.client.table('memberships') \
            .select('role') \
            .eq('tenant_id', company_id) \
            .execute()
        
        members = members_result.data or []
        member_stats = {
            'total': len(members),
            'admins': len([m for m in members if m['role'] in ['admin', 'owner']]),
            'members': len([m for m in members if m['role'] == 'member'])
        }
        
        # Estatísticas de solicitações
        requests_result = simple_supabase.client.table('join_requests') \
            .select('status') \
            .eq('tenant_id', company_id) \
            .execute()
        
        requests = requests_result.data or []
        request_stats = {
            'total': len(requests),
            'pending': len([r for r in requests if r['status'] == 'pending']),
            'approved': len([r for r in requests if r['status'] == 'approved']),
            'rejected': len([r for r in requests if r['status'] == 'rejected'])
        }
        
        return jsonify({
            'success': True,
            'company': company,
            'member_stats': member_stats,
            'request_stats': request_stats
        }), 200
        
    except Exception as e:
        logger.error("Erro ao buscar estatísticas da empresa", 
                    company_id=company_id, error=str(e))
        return jsonify({'error': 'Erro interno do servidor'}), 500

@companies_bp.route('/api/companies/validate-code/<code>', methods=['GET'])
def validate_company_code_endpoint(code):
    """Validar se código da empresa está disponível (público para signup)"""
    try:
        simple_supabase._ensure_client()
        
        # Buscar empresa pelo código
        result = simple_supabase.client.table('tenants') \
            .select('id, name, code') \
            .eq('code', code.upper()) \
            .single() \
            .execute()
        
        if result.data:
            return jsonify({
                'valid': True,
                'available': False,
                'company_name': result.data['name'],
                'message': 'Código encontrado'
            }), 200
        else:
            return jsonify({
                'valid': False,
                'available': True,
                'message': 'Código disponível para uso'
            }), 200
        
    except Exception as e:
        logger.error("Erro ao validar código da empresa", code=code, error=str(e))
        return jsonify({'error': 'Erro interno do servidor'}), 500
