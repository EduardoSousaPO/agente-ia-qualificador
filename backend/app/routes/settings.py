from flask import Blueprint, request, jsonify, g, current_app
from services.auth_service import require_auth
import structlog
from services.simple_supabase import simple_supabase
from datetime import datetime

logger = structlog.get_logger()

settings_bp = Blueprint('settings', __name__)

# Função removida - usando g.* diretamente

@settings_bp.route('/api/settings', methods=['GET'])
@require_auth()
def get_tenant_settings():
    """Obter configurações do tenant"""
    try:
        tenant_id = g.tenant_id
        
        # Buscar tenant e configurações
        logger.info("Buscando configurações do tenant", tenant_id=tenant_id)
        
        tenant_data = simple_supabase.client.table('tenants')\
            .select('*')\
            .eq('id', tenant_id)\
            .execute()
        
        logger.debug("Resultado da busca do tenant", 
                    data_count=len(tenant_data.data) if tenant_data.data else 0,
                    tenant_id=tenant_id)
        
        if not tenant_data.data:
            logger.warning("Tenant não encontrado", tenant_id=tenant_id)
            return jsonify({"error": "Tenant não encontrado"}), 404
        
        tenant = tenant_data.data[0]
        settings = tenant.get('settings', {})
        
        # Configurações padrão
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
        
        # Merge configurações padrão com personalizadas
        merged_settings = {**default_settings, **settings}
        
        return jsonify({
            "tenant": {
                "id": tenant['id'],
                "name": tenant['name'],
                "domain": tenant['domain'],
                "created_at": tenant['created_at']
            },
            "settings": merged_settings
        })
        
    except Exception as e:
        logger.error("Erro ao buscar configurações", 
                    error=str(e), 
                    tenant_id=g.get('tenant_id'), 
                    user_id=g.get('user_id'),
                    traceback=str(e.__class__.__name__))
        return jsonify({"error": "Erro interno do servidor", "details": str(e) if current_app.debug else None}), 500

@settings_bp.route('/api/settings', methods=['PUT'])
@require_auth()
def update_tenant_settings():
    """Atualizar configurações do tenant"""
    try:
        tenant_id = g.tenant_id
        user_id = g.user_id
        
        # Verificar permissão (apenas admin pode alterar configurações)
        if g.user_role not in ['admin']:
            return jsonify({"error": "Acesso negado. Apenas administradores podem alterar configurações"}), 403
        
        data = request.get_json()
        new_settings = data.get('settings', {})
        
        # Buscar configurações atuais
        tenant_data = simple_supabase.client.table('tenants')\
            .select('settings')\
            .eq('id', tenant_id)\
            .execute()
        
        if not tenant_data.data:
            return jsonify({"error": "Tenant não encontrado"}), 404
        
        current_settings = tenant_data.data[0].get('settings', {})
        
        # Merge configurações
        updated_settings = {**current_settings, **new_settings}
        
        # Atualizar no banco
        simple_supabase.client.table('tenants')\
            .update({'settings': updated_settings})\
            .eq('id', tenant_id)\
            .execute()
        
        # Log de auditoria (comentado por enquanto)
        # await simple_supabase.log_audit_event(
        #     tenant_id=tenant_id,
        #     user_id=user_id,
        #     action="update_settings",
        #     resource_type="tenant",
        #     resource_id=tenant_id,
        #     details={
        #         "updated_keys": list(new_settings.keys()),
        #         "settings_diff": new_settings
        #     }
        # )
        
        logger.info("Configurações atualizadas", 
                   tenant_id=tenant_id,
                   user_id=user_id,
                   updated_keys=list(new_settings.keys()))
        
        return jsonify({
            "success": True,
            "message": "Configurações atualizadas com sucesso",
            "settings": updated_settings
        })
        
    except Exception as e:
        logger.error("Erro ao atualizar configurações", error=str(e))
        return jsonify({"error": "Erro interno do servidor"}), 500

@settings_bp.route('/api/settings/ai-prompts', methods=['GET'])
@require_auth()
def get_ai_prompts():
    """Obter prompts de IA personalizados"""
    try:
        tenant_id = g.tenant_id
        
        # Buscar configurações
        tenant_data = simple_supabase.client.table('tenants')\
            .select('settings')\
            .eq('id', tenant_id)\
            .execute()
        
        settings = tenant_data.data[0].get('settings', {}) if tenant_data.data else {}
        ai_config = settings.get('ai_config', {})
        
        # Prompts padrão
        default_prompts = {
            "system_prompt": """Você é o assistente de qualificação de um escritório de investimentos brasileiro.

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
3. PATRIMÔNIO: Descobrir faixa de patrimônio
4. OBJETIVO: Entender objetivos de investimento
5. URGÊNCIA: Descobrir prazo para começar
6. OBJEÇÕES: Tratar dúvidas e objeções naturais
7. DECISÃO: Interesse em conversar com especialista

REGRAS IMPORTANTES:
- Se lead demonstrar interesse e atingir critérios mínimos, sinalize: HANDOFF_READY
- Se lead recusar ou não se qualificar, agradeça cordialmente
- Nunca seja insistente ou agressivo
- Use linguagem brasileira natural""",
            
            "welcome_message": "Olá! 👋 Sou assistente do escritório de investimentos. Posso te ajudar a descobrir as melhores oportunidades para fazer seu dinheiro render. Você já investe em alguma coisa?",
            
            "reengagement_24h": "Oi! 😊 Vi que você demonstrou interesse em investimentos ontem. Tem alguns minutos para conversarmos sobre suas metas financeiras?",
            
            "reengagement_72h": "Olá! Ainda está interessado em descobrir como fazer seu dinheiro render mais? Posso te mostrar algumas oportunidades interessantes! 💰",
            
            "handoff_message": "Perfeito! 🎉 Com base no nosso papo, acredito que posso te ajudar muito. Vou conectar você com um especialista. Que tal conversarmos {horario1} ou {horario2}?"
        }
        
        # Merge com prompts personalizados
        custom_prompts = ai_config.get('prompts', {})
        prompts = {**default_prompts, **custom_prompts}
        
        return jsonify({
            "prompts": prompts,
            "is_customized": bool(custom_prompts)
        })
        
    except Exception as e:
        logger.error("Erro ao buscar prompts de IA", error=str(e))
        return jsonify({"error": "Erro interno do servidor"}), 500

@settings_bp.route('/api/settings/ai-prompts', methods=['PUT'])
@require_auth()
def update_ai_prompts():
    """Atualizar prompts de IA personalizados"""
    try:
        tenant_id = g.tenant_id
        user_id = g.user_id
        
        # Verificar permissão
        if g.user_role not in ['admin']:
            return jsonify({"error": "Acesso negado"}), 403
        
        data = request.get_json()
        new_prompts = data.get('prompts', {})
        
        # Buscar configurações atuais
        tenant_data = simple_supabase.client.table('tenants')\
            .select('settings')\
            .eq('id', tenant_id)\
            .execute()
        
        current_settings = tenant_data.data[0].get('settings', {}) if tenant_data.data else {}
        ai_config = current_settings.get('ai_config', {})
        
        # Atualizar prompts
        ai_config['prompts'] = new_prompts
        current_settings['ai_config'] = ai_config
        
        # Salvar no banco
        simple_supabase.client.table('tenants')\
            .update({'settings': current_settings})\
            .eq('id', tenant_id)\
            .execute()
        
        # Log de auditoria (comentado por enquanto)
        # await simple_supabase.log_audit_event(
        #     tenant_id=tenant_id,
        #     user_id=user_id,
        #     action="update_ai_prompts",
        #     resource_type="tenant",
        #     resource_id=tenant_id,
        #     details={"prompt_keys": list(new_prompts.keys())}
        # )
        
        logger.info("Prompts de IA atualizados", tenant_id=tenant_id)
        
        return jsonify({
            "success": True,
            "message": "Prompts atualizados com sucesso"
        })
        
    except Exception as e:
        logger.error("Erro ao atualizar prompts", error=str(e))
        return jsonify({"error": "Erro interno do servidor"}), 500

@settings_bp.route('/api/settings/users', methods=['GET'])
@require_auth()
def list_tenant_users():
    """Listar usuários do tenant"""
    try:
        tenant_id = g.tenant_id
        
        # Verificar permissão
        if g.user_role not in ['admin', 'closer']:
            return jsonify({"error": "Acesso negado"}), 403
        
        # Buscar usuários
        users_data = simple_supabase.client.table('users')\
            .select('id, email, name, role, created_at')\
            .eq('tenant_id', tenant_id)\
            .order('created_at', desc=True)\
            .execute()
        
        return jsonify({
            "users": users_data.data,
            "total": len(users_data.data)
        })
        
    except Exception as e:
        logger.error("Erro ao listar usuários", error=str(e))
        return jsonify({"error": "Erro interno do servidor"}), 500

@settings_bp.route('/api/settings/integrations', methods=['GET'])
@require_auth()
def get_integrations_status():
    """Verificar status das integrações"""
    try:
        # Usar g.* diretamente
        
        # Verificar permissão
        if g.user_role not in ['admin']:
            return jsonify({"error": "Acesso negado"}), 403
        
        from flask import current_app
        
        integrations_status = {
            "openai": {
                "configured": bool(current_app.config.get('OPENAI_API_KEY')),
                "model": current_app.config.get('OPENAI_MODEL', 'gpt-4o-mini')
            },
            "twilio": {
                "configured": bool(
                    current_app.config.get('TWILIO_ACCOUNT_SID') and 
                    current_app.config.get('TWILIO_AUTH_TOKEN')
                ),
                "whatsapp_number": current_app.config.get('TWILIO_WHATSAPP_NUMBER')
            },
            "supabase": {
                "configured": bool(
                    current_app.config.get('SUPABASE_URL') and 
                    current_app.config.get('SUPABASE_KEY')
                ),
                "url": current_app.config.get('SUPABASE_URL')
            },
            "n8n": {
                "configured": bool(current_app.config.get('N8N_WEBHOOK_URL')),
                "webhook_url": current_app.config.get('N8N_WEBHOOK_URL')
            }
        }
        
        return jsonify({
            "integrations": integrations_status,
            "all_configured": all(
                integration["configured"] 
                for integration in integrations_status.values()
            )
        })
        
    except Exception as e:
        logger.error("Erro ao verificar integrações", error=str(e))
        return jsonify({"error": "Erro interno do servidor"}), 500

@settings_bp.route('/api/settings/health', methods=['GET'])
@require_auth()
def settings_health_check():
    """Diagnóstico da funcionalidade de configurações"""
    try:
        tenant_id = g.tenant_id
        user_id = g.user_id
        user_role = g.user_role
        
        # Verificar conectividade com Supabase
        simple_supabase._ensure_client()
        
        # Testar busca do tenant
        tenant_data = simple_supabase.client.table('tenants')\
            .select('id, name, created_at')\
            .eq('id', tenant_id)\
            .execute()
        
        # Verificar se usuário existe
        user_data = simple_supabase.client.table('users')\
            .select('id, email, role')\
            .eq('id', user_id)\
            .execute()
        
        return jsonify({
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "auth_context": {
                "user_id": user_id,
                "tenant_id": tenant_id,
                "user_role": user_role
            },
            "database_checks": {
                "tenant_found": bool(tenant_data.data),
                "user_found": bool(user_data.data),
                "tenant_data": tenant_data.data[0] if tenant_data.data else None,
                "user_data": user_data.data[0] if user_data.data else None
            },
            "supabase_connection": "ok"
        })
        
    except Exception as e:
        logger.error("Erro no health check", error=str(e))
        return jsonify({
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500



