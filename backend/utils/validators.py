"""
Utilitários de validação
"""
import re
from typing import Dict, List, Optional, Any
import uuid

def validate_phone_number(phone: str) -> bool:
    """Validar número de telefone brasileiro"""
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
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

class LeadSchema(Schema):
    """Schema de validação para leads"""
    name = fields.Str(required=True, validate=validate.Length(min=2, max=255))
    email = fields.Email(required=False, allow_none=True)
    phone = fields.Str(required=True, validate=validate.Length(min=10, max=20))
    origem = fields.Str(required=False, validate=validate.OneOf([
        'youtube', 'newsletter', 'manual', 'inbound_whatsapp', 'upload_csv', 'external'
    ]))
    tags = fields.List(fields.Str(), required=False, missing=[])

class MessageSchema(Schema):
    """Schema de validação para mensagens"""
    message = fields.Str(required=True, validate=validate.Length(min=1, max=4096))
    session_id = fields.UUID(required=True)

class SettingsSchema(Schema):
    """Schema de validação para configurações"""
    ai_config = fields.Dict(required=False)
    whatsapp_config = fields.Dict(required=False)
    notification_config = fields.Dict(required=False)
    scoring_config = fields.Dict(required=False)

def validate_lead_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validar dados de lead"""
    schema = LeadSchema()
    
    try:
        validated_data = schema.load(data)
        
        # Validação adicional do telefone
        if not validate_phone_number(validated_data['phone']):
            raise ValidationError("Número de telefone inválido")
        
        # Validação adicional do email se fornecido
        if validated_data.get('email') and not validate_email(validated_data['email']):
            raise ValidationError("Email inválido")
        
        return validated_data
        
    except ValidationError as e:
        raise ValidationError(f"Dados inválidos: {e.messages}")

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
    uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    return bool(re.match(uuid_pattern, tenant_id, re.IGNORECASE))

class WebhookPayloadSchema(Schema):
    """Schema para validação de payloads de webhook"""
    name = fields.Str(required=True)
    phone = fields.Str(required=True)
    email = fields.Email(required=False, allow_none=True)
    tenant_id = fields.UUID(required=True)
    origem = fields.Str(required=False, missing='external')
    tags = fields.List(fields.Str(), required=False, missing=[])

def validate_webhook_payload(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validar payload de webhook de intake"""
    schema = WebhookPayloadSchema()
    
    try:
        validated_data = schema.load(data)
        
        # Validações adicionais
        if not validate_phone_number(validated_data['phone']):
            raise ValidationError("Número de telefone inválido")
        
        if not validate_tenant_id(str(validated_data['tenant_id'])):
            raise ValidationError("Tenant ID inválido")
        
        return validated_data
        
    except ValidationError as e:
        raise ValidationError(f"Payload inválido: {e.messages}")

# Constantes de validação
VALID_LEAD_STATUSES = ['novo', 'em_conversa', 'qualificado', 'desqualificado']
VALID_SESSION_STATUSES = ['ativa', 'pausada', 'finalizada']
VALID_USER_ROLES = ['admin', 'closer', 'operator']
VALID_MESSAGE_DIRECTIONS = ['inbound', 'outbound']

def validate_enum_value(value: str, valid_values: List[str], field_name: str) -> str:
    """Validar valor enum"""
    if value not in valid_values:
        raise ValidationError(f"{field_name} deve ser um dos valores: {', '.join(valid_values)}")
    return value




