"""
Authentication routes
"""

from flask import Blueprint, request, jsonify, current_app
from services.simple_supabase import simple_supabase
import jwt
from functools import wraps

auth_bp = Blueprint('auth', __name__)

def token_required(f):
    """Decorator para verificar token JWT"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Token de acesso requerido'}), 401
        
        try:
            # Remove "Bearer " do token
            token = token.replace('Bearer ', '')
            
            # Verificar token com Supabase
            client = simple_supabase.client
            user = client.auth.get_user(token)
            
            if not user:
                return jsonify({'error': 'Token inválido'}), 401
                
            # Adicionar dados do usuário ao contexto da requisição
            request.current_user = user
            
        except Exception as e:
            current_app.logger.error(f"Erro na validação do token: {e}")
            return jsonify({'error': 'Token inválido'}), 401
            
        return f(*args, **kwargs)
    
    return decorated

@auth_bp.route('/me', methods=['GET'])
@token_required
def get_current_user():
    """Obter dados do usuário atual"""
    try:
        user = request.current_user
        
        # Buscar dados adicionais do usuário no banco
        client = simple_supabase.client
        result = client.table('users').select('*').eq('id', user.user.id).single().execute()
        
        if result.data:
            return jsonify(result.data)
        else:
            # Se não existe na tabela users, criar registro básico
            user_data = {
                'id': user.user.id,
                'email': user.user.email,
                'name': user.user.user_metadata.get('full_name', ''),
                'role': 'operator',
                'tenant_id': user.user.user_metadata.get('tenant_id', 'default')
            }
            
            result = client.table('users').insert(user_data).execute()
            return jsonify(result.data[0])
            
    except Exception as e:
        current_app.logger.error(f"Erro ao buscar usuário: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Endpoint de login (usando Supabase Auth no frontend)"""
    return jsonify({
        'message': 'Use Supabase Auth no frontend para fazer login',
        'login_url': '/auth/login'
    })

@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout():
    """Endpoint de logout"""
    try:
        # O logout é feito no frontend com Supabase
        return jsonify({'message': 'Logout realizado com sucesso'})
    except Exception as e:
        current_app.logger.error(f"Erro no logout: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500
