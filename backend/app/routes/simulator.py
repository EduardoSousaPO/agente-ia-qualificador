"""
Rotas para visualizar simulações WhatsApp
"""

from flask import Blueprint, jsonify, request
from services.whatsapp_simulator import whatsapp_simulator
from services.twilio_service_updated import twilio_service
from utils.auth_middleware import token_required

simulator_bp = Blueprint('simulator', __name__)

@simulator_bp.route('/messages', methods=['GET'])
@token_required
def get_all_messages():
    """Obter todas as mensagens simuladas"""
    try:
        messages = twilio_service.get_all_simulated_messages()
        return jsonify({
            "success": True,
            "messages": messages,
            "total": len(messages)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@simulator_bp.route('/conversation/<phone>', methods=['GET'])
@token_required
def get_conversation(phone):
    """Obter conversa de um telefone específico"""
    try:
        conversation = twilio_service.get_conversation_history(phone)
        return jsonify({
            "success": True,
            "phone": phone,
            "conversation": conversation,
            "total_messages": len(conversation)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@simulator_bp.route('/clear', methods=['POST'])
@token_required
def clear_simulation():
    """Limpar todas as simulações"""
    try:
        twilio_service.clear_simulation_data()
        return jsonify({
            "success": True,
            "message": "Simulações limpas com sucesso"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@simulator_bp.route('/test-message', methods=['POST'])
@token_required
def test_message():
    """Enviar mensagem de teste"""
    try:
        data = request.json
        phone = data.get('phone', '+5511999999999')
        message = data.get('message', 'Mensagem de teste do simulador')
        
        # Simular envio sem await (função síncrona)
        from services.whatsapp_simulator import whatsapp_simulator
        result = whatsapp_simulator.send_message(phone, message)
        
        return jsonify({
            "success": True,
            "result": {"message_id": result, "status": "sent", "simulator": True},
            "message": "Mensagem de teste enviada"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@simulator_bp.route('/status', methods=['GET'])
def get_simulator_status():
    """Status do simulador"""
    return jsonify({
        "simulator_active": True,
        "total_messages": len(whatsapp_simulator.get_all_messages()),
        "total_conversations": len(whatsapp_simulator.conversations),
        "message": "Simulador WhatsApp ativo - ideal para testes!"
    })
