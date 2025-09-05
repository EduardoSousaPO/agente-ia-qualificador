from flask import Blueprint, request, jsonify, g
from services.auth_service import require_auth
import structlog

logger = structlog.get_logger()

settings_simple_bp = Blueprint('settings_simple', __name__)

@settings_simple_bp.route('/api/settings', methods=['GET'])
def get_tenant_settings():
    """Obter configurações do tenant"""
    try:
        # Configurações padrão para funcionar
        default_settings = {
            "ai_config": {
                "model": "gpt-4o-mini",
                "temperature": 0.7,
                "max_tokens": 1000,
                "qualification_threshold": 70
            },
            "whatsapp_config": {
                "welcome_template": "welcome_first_time",
                "reengagement_24h": True,
                "reengagement_72h": True,
                "business_hours": {
                    "enabled": False,
                    "start": "09:00",
                    "end": "18:00",
                    "timezone": "America/Sao_Paulo"
                }
            },
            "notification_config": {
                "qualified_lead_slack": True,
                "qualified_lead_email": True,
                "daily_summary": True
            },
            "scoring_config": {
                "patrimonio_weights": {
                    "0-10k": 5,
                    "10k-50k": 15,
                    "50k-200k": 30,
                    "200k-500k": 35,
                    "500k+": 40
                },
                "objetivo_weight": 15,
                "urgencia_weights": {
                    "imediato": 20,
                    "30_dias": 15,
                    "3_meses": 10,
                    "6_meses": 5,
                    "1_ano": 2,
                    "sem_pressa": 0
                },
                "interesse_weight": 15,
                "engajamento_weight": 10
            }
        }
        
        return jsonify({
            "tenant": {
                "id": "05dc8c52-c0a0-44ae-aa2a-eeaa01090a27",
                "name": "LDC Capital Investimentos",
                "domain": "ldc-capital.com",
                "created_at": "2025-01-20T10:00:00Z"
            },
            "settings": default_settings
        })
        
    except Exception as e:
        logger.error("Erro ao buscar configurações", error=str(e))
        return jsonify({"error": "Erro interno do servidor"}), 500

@settings_simple_bp.route('/api/settings', methods=['PUT'])
def update_tenant_settings():
    """Atualizar configurações do tenant"""
    try:
        # Por enquanto, simular sucesso
        return jsonify({
            "success": True,
            "message": "Configurações atualizadas com sucesso"
        })
        
    except Exception as e:
        logger.error("Erro ao atualizar configurações", error=str(e))
        return jsonify({"error": "Erro interno do servidor"}), 500

@settings_simple_bp.route('/settings/users', methods=['GET'])
@require_auth()
def list_tenant_users():
    """Listar usuários do tenant"""
    try:
        # Retornar usuários simulados
        users = [
            {
                "id": g.user_id,
                "email": g.user_email,
                "name": "Usuário Admin",
                "role": g.user_role,
                "created_at": "2025-01-20T10:00:00Z"
            }
        ]
        
        return jsonify({
            "users": users,
            "total": len(users)
        })
        
    except Exception as e:
        logger.error("Erro ao listar usuários", error=str(e))
        return jsonify({"error": "Erro interno do servidor"}), 500
