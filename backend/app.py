#!/usr/bin/env python3
"""
Aplicação principal Flask - Agente Qualificador
"""

import os
import logging
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

def create_app():
    """Factory para criar aplicação Flask"""
    app = Flask(__name__)
    
    # Configurações básicas
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key')
    app.config['DEBUG'] = os.getenv('FLASK_ENV') == 'development'
    
    # Configurações do Supabase
    app.config['SUPABASE_URL'] = os.getenv('SUPABASE_URL')
    app.config['SUPABASE_KEY'] = os.getenv('SUPABASE_ANON_KEY')
    app.config['SUPABASE_SERVICE_KEY'] = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
    
    # Configurar CORS
    CORS(app, origins=os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(','))
    
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Rota de health check principal
    @app.route('/api/health', methods=['GET'])
    def health():
        return jsonify({
            "status": "healthy",
            "service": "Agente Qualificador API",
            "version": "1.0.0",
            "environment": os.getenv('FLASK_ENV', 'development'),
            "features": {
                "supabase": bool(os.getenv('SUPABASE_URL')),
                "openai": bool(os.getenv('OPENAI_API_KEY')),
                "n8n": bool(os.getenv('N8N_WEBHOOK_URL_INTAKE')),
                "whatsapp_simulator": os.getenv('USE_WHATSAPP_SIMULATOR', 'true') == 'true',
                "twilio": bool(os.getenv('TWILIO_ACCOUNT_SID')) and os.getenv('TWILIO_ACCOUNT_SID') != 'ACyour-twilio-account-sid',
                "authentication": "supabase_ready"
            }
        })
    
    # Rota de login simples (para desenvolvimento)
    @app.route('/api/auth/login', methods=['POST'])
    def simple_login():
        """Login simples para desenvolvimento"""
        try:
            data = request.json
            email = data.get('email')
            password = data.get('password')
            
            # Login de desenvolvimento simples
            if email == 'admin@demo.com' and password == 'demo123':
                # Simular token JWT
                user_data = {
                    "id": "admin-user-001",
                    "email": "admin@demo.com",
                    "name": "Administrador Demo",
                    "role": "admin",
                    "tenant_id": "60675861-e22a-4990-bab8-65ed07632a63"
                }
                
                # Token simples (em produção usar JWT real)
                token = f"demo_token_{datetime.now().strftime('%Y%m%d%H%M%S')}"
                
                return jsonify({
                    "success": True,
                    "user": user_data,
                    "access_token": token,
                    "message": "Login realizado com sucesso"
                })
            else:
                return jsonify({
                    "success": False,
                    "error": "Credenciais inválidas"
                }), 401
                
        except Exception as e:
            app.logger.error(f"Erro no login: {e}")
            return jsonify({
                "success": False,
                "error": "Erro interno do servidor"
            }), 500
    
    # Rota de verificação de usuário
    @app.route('/api/auth/me', methods=['GET'])
    def get_current_user():
        """Obter dados do usuário atual"""
        auth_header = request.headers.get('Authorization', '')
        
        if 'demo_token_' in auth_header:
            # Usuário demo autenticado
            return jsonify({
                "id": "admin-user-001",
                "email": "admin@demo.com",
                "name": "Administrador Demo",
                "role": "admin",
                "tenant_id": "60675861-e22a-4990-bab8-65ed07632a63"
            })
        else:
            return jsonify({"error": "Não autenticado"}), 401
    
    # Rota de teste do simulador WhatsApp
    @app.route('/api/simulator/status', methods=['GET'])
    def simulator_status():
        return jsonify({
            "simulator_active": os.getenv('USE_WHATSAPP_SIMULATOR', 'true') == 'true',
            "message": "Simulador WhatsApp ativo - perfeito para testes!",
            "endpoints": [
                "/api/simulator/messages - Ver todas as mensagens simuladas",
                "/api/simulator/test - Enviar mensagem de teste",
                "/api/simulator/clear - Limpar simulações"
            ]
        })
    
    # Rota de teste N8N
    @app.route('/api/test/n8n', methods=['POST'])
    def test_n8n():
        import requests
        
        webhook_url = os.getenv('N8N_WEBHOOK_URL_INTAKE')
        if not webhook_url:
            return jsonify({"error": "N8N webhook não configurado"}), 400
        
        test_data = {
            "name": "Teste Flask",
            "phone": "+5511999887766",
            "email": "teste@flask.com",
            "tenant_id": "flask-test",
            "origem": "flask_api_test"
        }
        
        try:
            response = requests.post(webhook_url, json=test_data, timeout=10)
            return jsonify({
                "success": True,
                "n8n_response": response.text,
                "status_code": response.status_code,
                "test_data": test_data
            })
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    # Rota de teste WhatsApp Simulator
    @app.route('/api/test/whatsapp', methods=['POST'])
    def test_whatsapp():
        try:
            from datetime import datetime
            
            phone = "+5511999888777"
            message = "Olá! Esta é uma mensagem de teste do simulador WhatsApp. O sistema está funcionando perfeitamente! 🎉"
            
            message_data = {
                "id": f"TEST_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "to": phone,
                "message": message,
                "timestamp": datetime.now().isoformat(),
                "status": "sent",
                "simulator": True
            }
            
            app.logger.info(f"📱 TESTE WHATSAPP SIMULADO: {message_data}")
            
            return jsonify({
                "success": True,
                "message": "Mensagem WhatsApp simulada com sucesso!",
                "data": message_data,
                "note": "Esta é uma simulação - nenhuma mensagem real foi enviada"
            })
            
        except Exception as e:
            app.logger.error(f"Erro no teste WhatsApp: {e}")
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    # Rota simples para criar leads (sem autenticação para teste)
    @app.route('/api/leads', methods=['POST'])
    def create_lead_simple():
        """Criar lead simples para testes"""
        try:
            data = request.json
            
            # Validação básica
            if not data.get('name') or not data.get('phone'):
                return jsonify({'error': 'Nome e telefone são obrigatórios'}), 400
            
            # Simular criação (sem banco real por enquanto)
            lead_data = {
                'id': f"LEAD_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                'name': data['name'],
                'phone': data['phone'],
                'email': data.get('email'),
                'origem': data.get('origem', 'api_test'),
                'status': 'novo',
                'score': 0,
                'created_at': datetime.now().isoformat()
            }
            
            app.logger.info(f"📋 Lead criado (simulado): {lead_data}")
            
            return jsonify({
                "message": "Lead criado com sucesso (simulado)",
                "lead": lead_data
            }), 201
            
        except Exception as e:
            app.logger.error(f"Erro ao criar lead: {e}")
            return jsonify({'error': 'Erro interno do servidor'}), 500
    
    # Rota para listar leads (com dados reais do Supabase)
    @app.route('/api/leads', methods=['GET'])
    def list_leads_real():
        """Listar leads do Supabase"""
        try:
            from supabase import create_client
            
            # Conectar ao Supabase
            supabase_url = app.config['SUPABASE_URL']
            supabase_key = app.config['SUPABASE_SERVICE_KEY']
            supabase = create_client(supabase_url, supabase_key)
            
            # Buscar leads do tenant padrão
            tenant_id = '60675861-e22a-4990-bab8-65ed07632a63'
            
            result = supabase.table('leads').select('*').eq('tenant_id', tenant_id).execute()
            
            return jsonify({
                "data": result.data,
                "count": len(result.data),
                "total": len(result.data),
                "message": "Leads carregados do Supabase com sucesso!"
            })
            
        except Exception as e:
            app.logger.error(f"Erro ao buscar leads do Supabase: {e}")
            return jsonify({
                "data": [],
                "count": 0,
                "error": str(e),
                "message": "Erro ao conectar com Supabase - usando modo simulado"
            }), 500
    
    # Rota para sessões de chat (simulada)
    @app.route('/api/chat/sessions', methods=['GET'])
    def list_chat_sessions():
        """Listar sessões de chat para o frontend"""
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        
        # Dados simulados de sessões de chat
        mock_sessions = [
            {
                "id": f"SESSION_{datetime.now().strftime('%Y%m%d%H%M%S')}_1",
                "lead_name": "Maria Silva Teste",
                "phone": "+5511888777666",
                "status": "ativa",
                "last_message": "Sim, quero falar com um especialista",
                "score": 75,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            },
            {
                "id": f"SESSION_{datetime.now().strftime('%Y%m%d%H%M%S')}_2",
                "lead_name": "João Silva",
                "phone": "+5511999887766",
                "status": "finalizada",
                "last_message": "Obrigado pelas informações",
                "score": 45,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
        ]
        
        return jsonify({
            "data": mock_sessions,
            "count": len(mock_sessions),
            "page": page,
            "limit": limit,
            "total": len(mock_sessions),
            "total_pages": 1
        })
    
    # Rota para mensagens de uma sessão específica
    @app.route('/api/chat/sessions/<session_id>/messages', methods=['GET'])
    def get_session_messages(session_id):
        """Obter mensagens de uma sessão específica"""
        mock_messages = [
            {
                "id": f"MSG_1_{session_id}",
                "session_id": session_id,
                "direction": "inbound",
                "content": "Olá, vi sobre investimentos no YouTube",
                "created_at": datetime.now().isoformat()
            },
            {
                "id": f"MSG_2_{session_id}",
                "session_id": session_id,
                "direction": "outbound", 
                "content": "Olá! Que bom que você se interessou por investimentos. Você já investe hoje?",
                "created_at": datetime.now().isoformat()
            },
            {
                "id": f"MSG_3_{session_id}",
                "session_id": session_id,
                "direction": "inbound",
                "content": "Sim, já invisto na poupança",
                "created_at": datetime.now().isoformat()
            },
            {
                "id": f"MSG_4_{session_id}",
                "session_id": session_id,
                "direction": "outbound",
                "content": "Entendi! A poupança é um bom começo. Qual o valor aproximado que você tem disponível para investir?",
                "created_at": datetime.now().isoformat()
            }
        ]
        
        return jsonify({
            "data": mock_messages,
            "session_id": session_id
        })
    
    # Rota para dashboard/estatísticas
    @app.route('/api/dashboard', methods=['GET'])
    def dashboard_stats():
        """Estatísticas do dashboard"""
        # Buscar estatísticas reais do Supabase
        try:
            from supabase import create_client
            
            supabase_url = app.config['SUPABASE_URL']
            supabase_key = app.config['SUPABASE_SERVICE_KEY']
            supabase = create_client(supabase_url, supabase_key)
            
            tenant_id = '60675861-e22a-4990-bab8-65ed07632a63'
            
            # Contar leads por status
            leads_result = supabase.table('leads').select('status').eq('tenant_id', tenant_id).execute()
            leads_data = leads_result.data
            
            total_leads = len(leads_data)
            status_counts = {}
            for lead in leads_data:
                status = lead['status']
                status_counts[status] = status_counts.get(status, 0) + 1
            
            qualified_leads = status_counts.get('qualificado', 0)
            conversion_rate = (qualified_leads / total_leads * 100) if total_leads > 0 else 0
            
            return jsonify({
                "total_leads": total_leads,
                "qualified_leads": qualified_leads,
                "active_conversations": status_counts.get('em_conversa', 0),
                "conversion_rate": round(conversion_rate, 1),
                "timeline_leads": [
                    {"date": "2025-08-20", "count": 2},
                    {"date": "2025-08-21", "count": total_leads}
                ],
                "leads_by_status": status_counts
            })
            
        except Exception as e:
            app.logger.error(f"Erro no dashboard: {e}")
            # Fallback para dados simulados
            return jsonify({
                "total_leads": 15,
                "qualified_leads": 8,
                "active_conversations": 3,
                "conversion_rate": 53.3,
                "timeline_leads": [
                    {"date": "2025-08-20", "count": 5},
                    {"date": "2025-08-21", "count": 10}
                ],
                "leads_by_status": {
                    "novo": 3,
                    "em_conversa": 3,
                    "qualificado": 8,
                    "desqualificado": 1
                }
            })
    
    # Rota para webhook Twilio (simulada)
    @app.route('/api/webhooks/twilio', methods=['POST'])
    def webhook_twilio_simple():
        """Webhook Twilio simplificado para testes"""
        try:
            data = request.json or request.form.to_dict()
            
            app.logger.info(f"📱 Webhook Twilio recebido: {data}")
            
            # Simular processamento da IA
            from_number = data.get('From', '').replace('whatsapp:', '')
            message_body = data.get('Body', '')
            
            # Resposta simulada da IA
            ai_response = f"Olá! Recebi sua mensagem: '{message_body}'. Como posso ajudá-lo com investimentos?"
            
            response_data = {
                "success": True,
                "message": "Mensagem processada com sucesso",
                "from": from_number,
                "received_message": message_body,
                "ai_response": ai_response,
                "score": 25,  # Score simulado
                "next_step": "aguardando_resposta"
            }
            
            app.logger.info(f"🤖 IA respondeu: {ai_response}")
            
            return jsonify(response_data)
            
        except Exception as e:
            app.logger.error(f"Erro no webhook: {e}")
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    # Rotas faltantes que o frontend está tentando acessar
    @app.route('/api/chat/sessions/<session_id>', methods=['GET'])
    def get_session_details(session_id):
        """Obter detalhes de uma sessão específica"""
        try:
            from supabase import create_client
            
            supabase_url = app.config['SUPABASE_URL']
            supabase_key = app.config['SUPABASE_SERVICE_KEY']
            supabase = create_client(supabase_url, supabase_key)
            
            # Buscar sessão (simulada por enquanto)
            session_data = {
                "id": session_id,
                "lead_name": "Maria Silva",
                "phone": "+5511888777666",
                "status": "ativa",
                "current_step": "qualificacao_patrimonio",
                "context": {"score": 75},
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            
            return jsonify(session_data)
            
        except Exception as e:
            app.logger.error(f"Erro ao buscar sessão: {e}")
            return jsonify({"error": "Sessão não encontrada"}), 404
    
    # Rotas para páginas que não existem mas o frontend está tentando acessar
    @app.route('/api/upload', methods=['GET', 'POST'])
    def upload_page():
        """Página de upload (placeholder)"""
        return jsonify({
            "message": "Página de upload em desenvolvimento",
            "available_features": ["CSV upload", "Bulk import", "File validation"]
        })
    
    @app.route('/api/reports', methods=['GET'])
    def reports_page():
        """Página de relatórios (placeholder)"""
        return jsonify({
            "message": "Página de relatórios em desenvolvimento",
            "available_reports": ["Conversion funnel", "Lead sources", "Agent performance"]
        })
    
    # Middleware para CORS adicional
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
    
    return app

if __name__ == '__main__':
    from datetime import datetime
    
    app = create_app()
    
    print("🚀 Iniciando Agente Qualificador API...")
    print("=" * 50)
    print(f"🌐 URL: http://localhost:{os.getenv('PORT', 5000)}")
    print(f"🔧 Ambiente: {os.getenv('FLASK_ENV', 'development')}")
    print(f"🎭 Simulador WhatsApp: {os.getenv('USE_WHATSAPP_SIMULATOR', 'true') == 'true'}")
    print(f"🔗 N8N Webhook: {bool(os.getenv('N8N_WEBHOOK_URL_INTAKE'))}")
    print("=" * 50)
    print("📋 Endpoints disponíveis:")
    print("  • GET  /api/health - Status da API")
    print("  • GET  /api/simulator/status - Status do simulador")
    print("  • POST /api/test/n8n - Testar N8N")
    print("  • POST /api/test/whatsapp - Testar WhatsApp")
    print("  • POST /api/leads - Criar lead (teste)")
    print("  • GET  /api/leads - Listar leads (teste)")
    print("  • POST /api/webhooks/twilio - Webhook WhatsApp (teste)")
    print("=" * 50)
    
    app.run(
        host=os.getenv('HOST', '0.0.0.0'),
        port=int(os.getenv('PORT', 5000)),
        debug=os.getenv('FLASK_ENV') == 'development'
    )