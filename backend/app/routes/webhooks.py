from flask import Blueprint, request, jsonify
import structlog
from services.supabase_service import supabase_service
from services.twilio_service import twilio_service
from services.ai_service import ai_service

logger = structlog.get_logger()

webhooks_bp = Blueprint('webhooks', __name__)

@webhooks_bp.route('/twilio', methods=['POST'])
async def handle_twilio_webhook():
    """Webhook para receber mensagens do Twilio WhatsApp"""
    try:
        # Validar webhook (opcional, mas recomendado em produção)
        # signature = request.headers.get('X-Twilio-Signature')
        # if not await twilio_service.validate_webhook_signature(
        #     request.get_data(), signature, request.url
        # ):
        #     logger.warning("Webhook signature inválida")
        #     return jsonify({"error": "Signature inválida"}), 401
        
        # Processar payload
        payload = request.form.to_dict()
        message_data = twilio_service.parse_webhook_payload(payload)
        
        logger.info("Webhook Twilio recebido", 
                   from_number=message_data['from_number'],
                   message_sid=message_data['message_sid'])
        
        # Buscar ou criar lead baseado no número
        lead = await find_or_create_lead_from_phone(message_data['from_number'], payload)
        
        # Buscar ou criar sessão ativa
        session = await find_or_create_session(lead['id'])
        
        # Salvar mensagem recebida
        await save_inbound_message(session['id'], message_data)
        
        # Processar com IA apenas se não for mensagem de mídia
        if message_data['num_media'] == 0 and message_data['body'].strip():
            ai_response = await process_message_with_ai(
                message_data['body'], 
                session, 
                lead
            )
            
            # Enviar resposta via WhatsApp
            if ai_response['response']:
                send_result = await twilio_service.send_message(
                    message_data['from_number'],
                    ai_response['response']
                )
                
                if send_result['success']:
                    # Salvar mensagem enviada
                    await save_outbound_message(
                        session['id'], 
                        ai_response['response'],
                        send_result['message_sid']
                    )
                    
                    # Atualizar contexto da sessão
                    await update_session_context(session['id'], ai_response, lead['id'])
                    
                    # Verificar se está pronto para handoff
                    if ai_response.get('handoff_ready'):
                        await handle_qualified_lead(lead, session, ai_response)
        
        return jsonify({"status": "success", "message": "Webhook processado"})
        
    except Exception as e:
        logger.error("Erro no webhook Twilio", error=str(e))
        return jsonify({"error": "Erro interno"}), 500

async def find_or_create_lead_from_phone(phone_number: str, payload: dict) -> dict:
    """Encontrar ou criar lead baseado no número de telefone"""
    try:
        # Buscar lead existente em todos os tenants (inbound WhatsApp)
        existing_lead = supabase_service.client.table('leads')\
            .select('*')\
            .eq('phone', phone_number)\
            .execute()
        
        if existing_lead.data:
            return existing_lead.data[0]
        
        # Criar novo lead (inbound)
        # Por enquanto, vamos usar um tenant padrão para leads inbound
        # Em produção, você pode implementar lógica para determinar o tenant
        default_tenant = supabase_service.client.table('tenants')\
            .select('id')\
            .limit(1)\
            .execute()
        
        if not default_tenant.data:
            raise Exception("Nenhum tenant encontrado para lead inbound")
        
        lead_data = {
            'tenant_id': default_tenant.data[0]['id'],
            'name': payload.get('ProfileName', f'Lead {phone_number[-4:]}'),
            'phone': phone_number,
            'origem': 'inbound_whatsapp',
            'inserido_manual': False,
            'status': 'novo',
            'score': 0
        }
        
        new_lead = await supabase_service.create_lead(lead_data)
        
        logger.info("Novo lead criado via inbound", 
                   lead_id=new_lead['id'],
                   phone=phone_number)
        
        return new_lead
        
    except Exception as e:
        logger.error("Erro ao encontrar/criar lead", phone=phone_number, error=str(e))
        raise

async def find_or_create_session(lead_id: str) -> dict:
    """Encontrar ou criar sessão ativa para o lead"""
    try:
        # Buscar sessão ativa
        active_session = supabase_service.client.table('sessions')\
            .select('*')\
            .eq('lead_id', lead_id)\
            .eq('status', 'ativa')\
            .order('created_at', desc=True)\
            .limit(1)\
            .execute()
        
        if active_session.data:
            return active_session.data[0]
        
        # Criar nova sessão
        session_data = {
            'lead_id': lead_id,
            'status': 'ativa',
            'current_step': 'apresentacao',
            'context': {
                'score': 0,
                'message_history': []
            }
        }
        
        new_session = await supabase_service.create_session(session_data)
        
        logger.info("Nova sessão criada", session_id=new_session['id'], lead_id=lead_id)
        
        return new_session
        
    except Exception as e:
        logger.error("Erro ao encontrar/criar sessão", lead_id=lead_id, error=str(e))
        raise

async def save_inbound_message(session_id: str, message_data: dict) -> dict:
    """Salvar mensagem recebida no banco"""
    try:
        message_record = {
            'session_id': session_id,
            'direction': 'inbound',
            'content': message_data['body'],
            'message_type': 'media' if message_data['num_media'] > 0 else 'text',
            'twilio_sid': message_data['message_sid']
        }
        
        return await supabase_service.create_message(message_record)
        
    except Exception as e:
        logger.error("Erro ao salvar mensagem inbound", error=str(e))
        raise

async def save_outbound_message(session_id: str, content: str, twilio_sid: str) -> dict:
    """Salvar mensagem enviada no banco"""
    try:
        message_record = {
            'session_id': session_id,
            'direction': 'outbound',
            'content': content,
            'message_type': 'text',
            'twilio_sid': twilio_sid
        }
        
        return await supabase_service.create_message(message_record)
        
    except Exception as e:
        logger.error("Erro ao salvar mensagem outbound", error=str(e))
        raise

async def process_message_with_ai(message: str, session: dict, lead: dict) -> dict:
    """Processar mensagem com IA"""
    try:
        # Buscar histórico de mensagens
        messages = await supabase_service.get_messages(session['id'])
        
        # Preparar contexto
        context = session.get('context', {})
        context['message_history'] = [
            {
                'direction': msg['direction'],
                'content': msg['content'],
                'created_at': msg['created_at']
            }
            for msg in messages
        ]
        
        # Processar com IA
        ai_response = await ai_service.process_message(message, context)
        
        return ai_response
        
    except Exception as e:
        logger.error("Erro ao processar com IA", error=str(e))
        # Fallback response
        return {
            'response': 'Desculpe, tive um problema técnico. Pode repetir sua mensagem?',
            'context_update': {},
            'handoff_ready': False,
            'score': context.get('score', 0)
        }

async def update_session_context(session_id: str, ai_response: dict, lead_id: str):
    """Atualizar contexto da sessão e score do lead"""
    try:
        # Buscar contexto atual
        session = await supabase_service.get_session(session_id)
        current_context = session.get('context', {})
        
        # Aplicar updates do contexto
        current_context.update(ai_response['context_update'])
        current_context['score'] = ai_response['score']
        
        # Atualizar sessão
        await supabase_service.update_session(session_id, {
            'context': current_context,
            'current_step': ai_response['context_update'].get('current_step', session.get('current_step'))
        })
        
        # Atualizar score do lead
        await supabase_service.update_lead(lead_id, session['leads']['tenant_id'], {
            'score': ai_response['score']
        })
        
    except Exception as e:
        logger.error("Erro ao atualizar contexto", session_id=session_id, error=str(e))

async def handle_qualified_lead(lead: dict, session: dict, ai_response: dict):
    """Processar lead qualificado"""
    try:
        # Criar registro de qualificação
        qualification_summary = ai_service.get_qualification_summary(session['context'])
        
        qualification_data = {
            'lead_id': lead['id'],
            'patrimonio_faixa': qualification_summary['patrimonio_faixa'],
            'objetivo': qualification_summary['objetivo'],
            'urgencia': qualification_summary['urgencia'],
            'interesse_especialista': qualification_summary['interesse_especialista'],
            'score_final': qualification_summary['score_final'],
            'observacoes': qualification_summary['observacoes']
        }
        
        await supabase_service.create_qualification(qualification_data)
        
        # Atualizar status do lead
        await supabase_service.update_lead(lead['id'], lead['tenant_id'], {
            'status': 'qualificado'
        })
        
        # Finalizar sessão
        await supabase_service.update_session(session['id'], {
            'status': 'finalizada'
        })
        
        # TODO: Disparar notificação para closers via n8n
        
        logger.info("Lead qualificado via IA", 
                   lead_id=lead['id'],
                   score=qualification_summary['score_final'])
        
    except Exception as e:
        logger.error("Erro ao processar lead qualificado", lead_id=lead['id'], error=str(e))

@webhooks_bp.route('/intake/lead', methods=['POST'])
async def intake_lead():
    """Endpoint para receber leads de fontes externas (n8n, formulários)"""
    try:
        data = request.get_json()
        
        # Validar dados obrigatórios
        required_fields = ['name', 'phone', 'tenant_id']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"Campo '{field}' é obrigatório"}), 400
        
        # Verificar se tenant existe
        tenant = supabase_service.client.table('tenants')\
            .select('id')\
            .eq('id', data['tenant_id'])\
            .execute()
        
        if not tenant.data:
            return jsonify({"error": "Tenant não encontrado"}), 404
        
        # Verificar duplicata
        existing_lead = supabase_service.client.table('leads')\
            .select('id')\
            .eq('tenant_id', data['tenant_id'])\
            .eq('phone', data['phone'])\
            .execute()
        
        if existing_lead.data:
            return jsonify({"error": "Lead já existe", "lead_id": existing_lead.data[0]['id']}), 409
        
        # Criar lead
        lead_data = {
            'tenant_id': data['tenant_id'],
            'name': data['name'],
            'email': data.get('email'),
            'phone': data['phone'],
            'origem': data.get('origem', 'external'),
            'inserido_manual': False,
            'tags': data.get('tags', []),
            'status': 'novo',
            'score': 0
        }
        
        new_lead = await supabase_service.create_lead(lead_data)
        
        # Criar sessão inicial
        session_data = {
            'lead_id': new_lead['id'],
            'status': 'ativa',
            'current_step': 'apresentacao',
            'context': {'score': 0, 'message_history': []}
        }
        
        new_session = await supabase_service.create_session(session_data)
        
        # Enviar primeira mensagem via WhatsApp
        welcome_result = await twilio_service.send_template_message(
            data['phone'],
            'welcome_first_time',
            {'name': data['name']}
        )
        
        if welcome_result['success']:
            # Salvar mensagem enviada
            await save_outbound_message(
                new_session['id'],
                welcome_result.get('message_body', 'Mensagem de boas-vindas'),
                welcome_result['message_sid']
            )
        
        logger.info("Lead intake processado", 
                   lead_id=new_lead['id'],
                   origem=data.get('origem'))
        
        return jsonify({
            "success": True,
            "lead": new_lead,
            "session": new_session,
            "whatsapp_sent": welcome_result['success']
        }), 201
        
    except Exception as e:
        logger.error("Erro no intake de lead", error=str(e))
        return jsonify({"error": "Erro interno do servidor"}), 500




