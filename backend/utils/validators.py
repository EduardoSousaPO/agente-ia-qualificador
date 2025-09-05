"""
Utilitários de validação - Versão simplificada sem marshmallow
"""
import re
import uuid
from typing import Dict, List, Optional, Any

class ValidationError(Exception):
    """Exceção customizada para erros de validação"""
    def __init__(self, message: str, field: str = None):
        self.message = message
        self.field = field
        super().__init__(message)

def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> Optional[str]:
    """
    Validar se todos os campos obrigatórios estão presentes
    Retorna None se válido, ou string com erro se inválido
    """
    if not isinstance(data, dict):
        return "Dados devem ser um objeto JSON"
    
    missing_fields = []
    for field in required_fields:
        if field not in data or data[field] is None or data[field] == "":
            missing_fields.append(field)
    
    if missing_fields:
        return f"Campos obrigatórios ausentes: {', '.join(missing_fields)}"
    
    return None

def validate_uuid(uuid_string: str) -> bool:
    """Validar se a string é um UUID válido"""
    if not isinstance(uuid_string, str):
        return False
    
    try:
        uuid.UUID(uuid_string)
        return True
    except (ValueError, TypeError):
        return False

def validate_phone_number(phone: str) -> bool:
    """Validar número de telefone brasileiro"""
    if not isinstance(phone, str):
        return False
    
    # Remove todos os caracteres não numéricos
    clean_phone = re.sub(r'\D', '', phone)
    
    # Padrões aceitos:
    # 11 dígitos: 11987654321
    # 13 dígitos: 5511987654321
    patterns = [
        r'^11\d{8,9}$',      # SP com 8 ou 9 dígitos
        r'^\d{2}9\d{8}$',    # Qualquer estado com 9 dígitos
        r'^55\d{2}9\d{8}$',  # Com código do país
    ]
    
    return any(re.match(pattern, clean_phone) for pattern in patterns)

def validate_email(email: str) -> bool:
    """Validar email"""
    if not isinstance(email, str):
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_string_length(value: str, min_length: int = 0, max_length: int = None) -> bool:
    """Validar comprimento de string"""
    if not isinstance(value, str):
        return False
    
    if len(value) < min_length:
        return False
    
    if max_length and len(value) > max_length:
        return False
    
    return True

def validate_lead_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validar dados de lead"""
    # Validar campos obrigatórios
    required_fields = ['name', 'phone']
    validation_error = validate_required_fields(data, required_fields)
    if validation_error:
        raise ValidationError(validation_error)
    
    # Validar nome
    name = data.get('name', '').strip()
    if not validate_string_length(name, min_length=2, max_length=255):
        raise ValidationError("Nome deve ter entre 2 e 255 caracteres", 'name')
    
    # Validar telefone
    phone = data.get('phone', '').strip()
    if not validate_phone_number(phone):
        raise ValidationError("Número de telefone inválido", 'phone')
    
    # Validar email se fornecido
    email = data.get('email')
    if email and email.strip():
        if not validate_email(email.strip()):
            raise ValidationError("Email inválido", 'email')
    
    # Validar origem se fornecida
    valid_origins = ['youtube', 'newsletter', 'manual', 'inbound_whatsapp', 'upload_csv', 'external']
    origem = data.get('origem')
    if origem and origem not in valid_origins:
        raise ValidationError(f"Origem deve ser uma das opções: {', '.join(valid_origins)}", 'origem')
    
    # Retornar dados limpos
    validated_data = {
        'name': name,
        'phone': phone,
        'email': email.strip() if email else None,
        'origem': origem or 'manual',
        'tags': data.get('tags', []) if isinstance(data.get('tags'), list) else []
    }
    
    return validated_data

def validate_message_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validar dados de mensagem"""
    # Validar campos obrigatórios
    required_fields = ['message', 'session_id']
    validation_error = validate_required_fields(data, required_fields)
    if validation_error:
        raise ValidationError(validation_error)
    
    # Validar mensagem
    message = data.get('message', '').strip()
    if not validate_string_length(message, min_length=1, max_length=4096):
        raise ValidationError("Mensagem deve ter entre 1 e 4096 caracteres", 'message')
    
    # Validar session_id
    session_id = data.get('session_id')
    if not validate_uuid(session_id):
        raise ValidationError("session_id deve ser um UUID válido", 'session_id')
    
    return {
        'message': message,
        'session_id': session_id
    }

def validate_webhook_payload(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validar payload de webhook de intake"""
    # Validar campos obrigatórios
    required_fields = ['name', 'phone', 'tenant_id']
    validation_error = validate_required_fields(data, required_fields)
    if validation_error:
        raise ValidationError(validation_error)
    
    # Validar nome
    name = data.get('name', '').strip()
    if not validate_string_length(name, min_length=2, max_length=255):
        raise ValidationError("Nome deve ter entre 2 e 255 caracteres", 'name')
    
    # Validar telefone
    phone = data.get('phone', '').strip()
    if not validate_phone_number(phone):
        raise ValidationError("Número de telefone inválido", 'phone')
    
    # Validar tenant_id
    tenant_id = data.get('tenant_id')
    if not validate_uuid(tenant_id):
        raise ValidationError("tenant_id deve ser um UUID válido", 'tenant_id')
    
    # Validar email se fornecido
    email = data.get('email')
    if email and email.strip():
        if not validate_email(email.strip()):
            raise ValidationError("Email inválido", 'email')
    
    return {
        'name': name,
        'phone': phone,
        'email': email.strip() if email else None,
        'tenant_id': tenant_id,
        'origem': data.get('origem', 'external'),
        'tags': data.get('tags', []) if isinstance(data.get('tags'), list) else []
    }

def validate_csv_headers(headers: List[str]) -> List[str]:
    """Validar cabeçalhos do CSV de upload"""
    required_headers = ['name', 'phone']
    optional_headers = ['email', 'origem', 'tags']
    valid_headers = required_headers + optional_headers
    
    # Verificar se todos os cabeçalhos obrigatórios estão presentes
    missing_headers = [h for h in required_headers if h not in headers]
    if missing_headers:
        raise ValidationError(f"Cabeçalhos obrigatórios ausentes: {', '.join(missing_headers)}")
    
    # Verificar se há cabeçalhos inválidos
    invalid_headers = [h for h in headers if h not in valid_headers]
    if invalid_headers:
        raise ValidationError(f"Cabeçalhos inválidos: {', '.join(invalid_headers)}")
    
    return headers

def sanitize_string(text: str) -> str:
    """Sanitizar string removendo caracteres perigosos"""
    if not isinstance(text, str):
        return str(text)
    
    # Remove caracteres de controle e normaliza espaços
    sanitized = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
    sanitized = re.sub(r'\s+', ' ', sanitized).strip()
    
    return sanitized

def validate_tenant_id(tenant_id: str) -> bool:
    """Validar formato UUID do tenant"""
    return validate_uuid(tenant_id)

# Constantes de validação
VALID_LEAD_STATUSES = ['novo', 'em_conversa', 'qualificado', 'desqualificado']
VALID_SESSION_STATUSES = ['ativa', 'pausada', 'finalizada']
VALID_USER_ROLES = ['admin', 'operator', 'viewer']
VALID_MESSAGE_DIRECTIONS = ['inbound', 'outbound']

def validate_enum_value(value: str, valid_values: List[str], field_name: str) -> str:
    """Validar valor enum"""
    if value not in valid_values:
        raise ValidationError(f"{field_name} deve ser um dos valores: {', '.join(valid_values)}")
    return value

def validate_settings_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validar dados de configurações"""
    validated_data = {}
    
    # Validar configurações de IA (opcional)
    if 'ai_config' in data:
        ai_config = data['ai_config']
        if not isinstance(ai_config, dict):
            raise ValidationError("ai_config deve ser um objeto", 'ai_config')
        validated_data['ai_config'] = ai_config
    
    # Validar configurações do WhatsApp (opcional)
    if 'whatsapp_config' in data:
        whatsapp_config = data['whatsapp_config']
        if not isinstance(whatsapp_config, dict):
            raise ValidationError("whatsapp_config deve ser um objeto", 'whatsapp_config')
        validated_data['whatsapp_config'] = whatsapp_config
    
    # Validar configurações de notificação (opcional)
    if 'notification_config' in data:
        notification_config = data['notification_config']
        if not isinstance(notification_config, dict):
            raise ValidationError("notification_config deve ser um objeto", 'notification_config')
        validated_data['notification_config'] = notification_config
    
    # Validar configurações de scoring (opcional)
    if 'scoring_config' in data:
        scoring_config = data['scoring_config']
        if not isinstance(scoring_config, dict):
            raise ValidationError("scoring_config deve ser um objeto", 'scoring_config')
        validated_data['scoring_config'] = scoring_config
    
    return validated_data

# Funções auxiliares para facilitar importação
def validate_json_data(data: Any) -> bool:
    """Validar se os dados são JSON válidos"""
    return isinstance(data, (dict, list))

def validate_positive_integer(value: Any) -> bool:
    """Validar se o valor é um inteiro positivo"""
    try:
        return isinstance(value, int) and value > 0
    except:
        return False

def validate_score(score: Any) -> bool:
    """Validar score de qualificação (0-100)"""
    try:
        return isinstance(score, (int, float)) and 0 <= score <= 100
    except:
        return False