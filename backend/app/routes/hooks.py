#!/usr/bin/env python3
"""
Rotas de Webhooks para integração com N8N
"""

from flask import Blueprint, request, jsonify
from services.email_service import email_service
from services.crm_adapter import crm_adapter
from services.simple_supabase import simple_supabase
from utils.validators import validate_required_fields, validate_uuid
import structlog

logger = structlog.get_logger()

hooks_bp = Blueprint('hooks', __name__)

@hooks_bp.route('/api/hooks/qualified-lead', methods=['POST'])
def handle_qualified_lead():
    """
    Webhook para processar leads qualificados vindos do N8N
    
    Payload esperado:
    {
        "tenant_id": "uuid",
        "lead": {
            "name": "string",
            "email": "string", 
            "phone": "string",
            "score": number,
            "answers": object,
            "origem": "string"
        }
    }
    """
    try:
        data = request.get_json()
        
        # Validar campos obrigatórios
        required_fields = ['tenant_id', 'lead']
        validation_error = validate_required_fields(data, required_fields)
        if validation_error:
            return jsonify({'error': validation_error}), 400
        
        tenant_id = data['tenant_id']
        lead_data = data['lead']
        
        # Validar tenant_id
        if not validate_uuid(tenant_id):
            return jsonify({'error': 'tenant_id deve ser um UUID válido'}), 400
        
        # Validar campos do lead
        lead_required_fields = ['name', 'phone', 'score']
        lead_validation_error = validate_required_fields(lead_data, lead_required_fields)
        if lead_validation_error:
            return jsonify({'error': f'Lead: {lead_validation_error}'}), 400
        
        logger.info("Webhook qualified-lead recebido", 
                   tenant_id=tenant_id,
                   lead_name=lead_data.get('name'),
                   score=lead_data.get('score'))
        
        # Buscar configurações do tenant
        tenant_result = simple_supabase.client.table('tenants') \
            .select('settings') \
            .eq('id', tenant_id) \
            .single() \
            .execute()
        
        if not tenant_result.data:
            return jsonify({'error': 'Tenant não encontrado'}), 404
        
        tenant_settings = tenant_result.data.get('settings', {})
        
        # Obter email do consultor (configuração do tenant ou padrão)
        consultant_email = tenant_settings.get('default_consultant_email')
        
        if not consultant_email:
            logger.warning("Email do consultor não configurado", tenant_id=tenant_id)
            consultant_email = 'consultor@exemplo.com'  # Fallback para demo
        
        # Preparar payload completo
        full_payload = {
            'lead_id': lead_data.get('id', 'webhook-lead'),
            'name': lead_data['name'],
            'email': lead_data.get('email', 'Não informado'),
            'phone': lead_data['phone'],
            'score': lead_data['score'],
            'status': 'qualificado',
            'origem': lead_data.get('origem', 'WhatsApp'),
            'answers': lead_data.get('answers', {}),
            'created_at': lead_data.get('created_at')
        }
        
        results = {}
        
        # 1. Enviar email para consultor
        email_result = email_service.send_qualified_lead_email(
            lead_data=full_payload,
            consultant_email=consultant_email
        )
        results['email'] = email_result
        
        # 2. Enviar para CRM configurado
        crm_result = crm_adapter.send_lead(
            tenant_id=tenant_id,
            lead_payload=full_payload
        )
        results['crm'] = crm_result
        
        # Determinar status geral
        email_success = email_result.get('success', False)
        crm_success = crm_result.get('success', False) or crm_result.get('skipped', False)
        
        overall_success = email_success and crm_success
        
        logger.info("Webhook qualified-lead processado", 
                   tenant_id=tenant_id,
                   lead_name=lead_data.get('name'),
                   email_success=email_success,
                   crm_success=crm_success,
                   overall_success=overall_success)
        
        return jsonify({
            'success': overall_success,
            'message': 'Lead qualificado processado',
            'results': results,
            'tenant_id': tenant_id,
            'lead_name': lead_data.get('name'),
            'consultant_email': consultant_email
        }), 200
        
    except Exception as e:
        logger.error("Erro no webhook qualified-lead", error=str(e))
        return jsonify({
            'success': False,
            'error': 'Erro interno do servidor',
            'details': str(e)
        }), 500

@hooks_bp.route('/api/hooks/test-email', methods=['POST'])
def test_email():
    """Endpoint para testar envio de email"""
    try:
        data = request.get_json()
        
        to_email = data.get('to_email')
        if not to_email:
            return jsonify({'error': 'to_email é obrigatório'}), 400
        
        result = email_service.send_test_email(to_email)
        
        return jsonify(result), 200 if result['success'] else 500
        
    except Exception as e:
        logger.error("Erro no teste de email", error=str(e))
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@hooks_bp.route('/api/hooks/test-crm', methods=['POST'])
def test_crm():
    """Endpoint para testar conexão com CRM"""
    try:
        data = request.get_json()
        
        tenant_id = data.get('tenant_id')
        if not tenant_id:
            return jsonify({'error': 'tenant_id é obrigatório'}), 400
        
        if not validate_uuid(tenant_id):
            return jsonify({'error': 'tenant_id deve ser um UUID válido'}), 400
        
        result = crm_adapter.test_crm_connection(tenant_id)
        
        return jsonify(result), 200 if result['success'] else 500
        
    except Exception as e:
        logger.error("Erro no teste de CRM", error=str(e))
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@hooks_bp.route('/api/hooks/health', methods=['GET'])
def hooks_health():
    """Health check para webhooks"""
    return jsonify({
        'status': 'healthy',
        'service': 'webhooks',
        'endpoints': [
            'POST /api/hooks/qualified-lead',
            'POST /api/hooks/test-email',
            'POST /api/hooks/test-crm',
            'GET /api/hooks/health'
        ]
    }), 200

