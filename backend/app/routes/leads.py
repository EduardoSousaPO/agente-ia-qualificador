"""
Leads management routes
"""

from flask import Blueprint, request, jsonify, current_app
from services.supabase_service import supabase_service
from .auth import token_required
import pandas as pd
import io
from datetime import datetime
import uuid

leads_bp = Blueprint('leads', __name__)

@leads_bp.route('/', methods=['GET'])
@token_required
def get_leads():
    """Listar leads com filtros"""
    try:
        # Parâmetros de filtro
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        status = request.args.get('status')
        origem = request.args.get('origem')
        search = request.args.get('search')
        
        # Calcular offset
        offset = (page - 1) * limit
        
        # Construir query
        client = supabase_service.client
        query = client.table('leads').select('*', count='exact')
        
        # Aplicar filtros
        if status:
            query = query.eq('status', status)
        if origem:
            query = query.eq('origem', origem)
        if search:
            query = query.or_(f'name.ilike.%{search}%,email.ilike.%{search}%,phone.ilike.%{search}%')
        
        # Paginação e ordenação
        result = query.order('created_at', desc=True).range(offset, offset + limit - 1).execute()
        
        return jsonify({
            "data": result.data,
            "count": len(result.data),
            "total": result.count,
            "page": page,
            "limit": limit,
            "total_pages": (result.count + limit - 1) // limit
        })
        
    except Exception as e:
        current_app.logger.error(f"Erro ao buscar leads: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@leads_bp.route('/', methods=['POST'])
@token_required
def create_lead():
    """Criar novo lead"""
    try:
        data = request.json
        
        # Validação básica
        required_fields = ['name', 'phone']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400
        
        # Dados do lead
        lead_data = {
            'id': str(uuid.uuid4()),
            'tenant_id': request.current_user.user.user_metadata.get('tenant_id', 'default'),
            'name': data['name'],
            'email': data.get('email'),
            'phone': data['phone'],
            'origem': data.get('origem', 'manual'),
            'inserido_manual': True,
            'tags': data.get('tags', []),
            'status': 'novo',
            'score': 0,
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }
        
        # Inserir no banco
        client = supabase_service.client
        result = client.table('leads').insert(lead_data).execute()
        
        return jsonify({
            "message": "Lead criado com sucesso",
            "lead": result.data[0]
        }), 201
        
    except Exception as e:
        current_app.logger.error(f"Erro ao criar lead: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@leads_bp.route('/<lead_id>', methods=['GET'])
@token_required
def get_lead(lead_id):
    """Obter detalhes de um lead específico"""
    try:
        client = supabase_service.client
        result = client.table('leads').select('*').eq('id', lead_id).single().execute()
        
        if not result.data:
            return jsonify({'error': 'Lead não encontrado'}), 404
        
        return jsonify(result.data)
        
    except Exception as e:
        current_app.logger.error(f"Erro ao buscar lead: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@leads_bp.route('/<lead_id>', methods=['PUT'])
@token_required
def update_lead(lead_id):
    """Atualizar lead"""
    try:
        data = request.json
        
        # Dados para atualização
        update_data = {
            'updated_at': datetime.utcnow().isoformat()
        }
        
        # Campos permitidos para atualização
        allowed_fields = ['name', 'email', 'phone', 'origem', 'tags', 'status', 'score']
        for field in allowed_fields:
            if field in data:
                update_data[field] = data[field]
        
        # Atualizar no banco
        client = supabase_service.client
        result = client.table('leads').update(update_data).eq('id', lead_id).execute()
        
        if not result.data:
            return jsonify({'error': 'Lead não encontrado'}), 404
        
        return jsonify({
            "message": "Lead atualizado com sucesso",
            "lead": result.data[0]
        })
        
    except Exception as e:
        current_app.logger.error(f"Erro ao atualizar lead: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@leads_bp.route('/upload', methods=['POST'])
@token_required
def upload_leads_csv():
    """Upload de leads em lote via CSV"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
        if not file.filename.endswith('.csv'):
            return jsonify({'error': 'Arquivo deve ser CSV'}), 400
        
        # Ler CSV
        csv_data = file.read().decode('utf-8')
        df = pd.read_csv(io.StringIO(csv_data))
        
        # Validar colunas obrigatórias
        required_columns = ['name', 'phone']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return jsonify({
                'error': f'Colunas obrigatórias faltando: {", ".join(missing_columns)}'
            }), 400
        
        # Processar leads
        tenant_id = request.current_user.user.user_metadata.get('tenant_id', 'default')
        leads_data = []
        errors = []
        
        for index, row in df.iterrows():
            try:
                lead_data = {
                    'id': str(uuid.uuid4()),
                    'tenant_id': tenant_id,
                    'name': str(row['name']).strip(),
                    'phone': str(row['phone']).strip(),
                    'email': str(row.get('email', '')).strip() or None,
                    'origem': str(row.get('origem', 'csv_upload')).strip(),
                    'inserido_manual': True,
                    'tags': [],
                    'status': 'novo',
                    'score': 0,
                    'created_at': datetime.utcnow().isoformat(),
                    'updated_at': datetime.utcnow().isoformat()
                }
                leads_data.append(lead_data)
            except Exception as e:
                errors.append(f"Linha {index + 1}: {str(e)}")
        
        # Inserir leads no banco
        client = supabase_service.client
        created_count = 0
        
        for lead_data in leads_data:
            try:
                client.table('leads').insert(lead_data).execute()
                created_count += 1
            except Exception as e:
                errors.append(f"Erro ao criar lead {lead_data['name']}: {str(e)}")
        
        return jsonify({
            "message": "Upload processado",
            "created": created_count,
            "total": len(leads_data),
            "errors": errors
        })
        
    except Exception as e:
        current_app.logger.error(f"Erro no upload de CSV: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@leads_bp.route('/<lead_id>/manual-qualify', methods=['POST'])
@token_required
def manual_qualification(lead_id):
    """Qualificação manual de lead"""
    try:
        data = request.json
        
        # Criar registro de qualificação
        qualification_data = {
            'id': str(uuid.uuid4()),
            'lead_id': lead_id,
            'patrimonio_faixa': data.get('patrimonio_faixa'),
            'objetivo': data.get('objetivo'),
            'urgencia': data.get('urgencia'),
            'interesse_especialista': data.get('interesse_especialista', False),
            'score_final': data.get('score_final', 0),
            'observacoes': data.get('observacoes'),
            'created_at': datetime.utcnow().isoformat()
        }
        
        client = supabase_service.client
        
        # Inserir qualificação
        client.table('qualificacoes').insert(qualification_data).execute()
        
        # Atualizar status do lead
        status = 'qualificado' if qualification_data['score_final'] >= 70 else 'desqualificado'
        client.table('leads').update({
            'status': status,
            'score': qualification_data['score_final'],
            'updated_at': datetime.utcnow().isoformat()
        }).eq('id', lead_id).execute()
        
        return jsonify({
            "message": "Qualificação manual realizada com sucesso",
            "qualification": qualification_data
        })
        
    except Exception as e:
        current_app.logger.error(f"Erro na qualificação manual: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500
