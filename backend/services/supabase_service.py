from supabase import create_client, Client
from typing import Dict, List, Optional, Any
import structlog
from flask import current_app

logger = structlog.get_logger()

class SupabaseService:
    """Serviço para interação com Supabase"""
    
    def __init__(self):
        self._client: Optional[Client] = None
        self._service_client: Optional[Client] = None
    
    @property
    def client(self) -> Client:
        """Cliente Supabase com chave anônima"""
        if self._client is None:
            url = current_app.config['SUPABASE_URL']
            key = current_app.config['SUPABASE_KEY']
            self._client = create_client(url, key)
            logger.info("Cliente Supabase inicializado")
        return self._client
    
    @property
    def service_client(self) -> Client:
        """Cliente Supabase com service role (para operações admin)"""
        if self._service_client is None:
            url = current_app.config['SUPABASE_URL']
            key = current_app.config['SUPABASE_SERVICE_KEY']
            self._service_client = create_client(url, key)
            logger.info("Service client Supabase inicializado")
        return self._service_client
    
    # CRUD Operations for Leads
    async def create_lead(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Criar um novo lead"""
        try:
            result = self.client.table('leads').insert(lead_data).execute()
            logger.info("Lead criado", lead_id=result.data[0]['id'])
            return result.data[0]
        except Exception as e:
            logger.error("Erro ao criar lead", error=str(e))
            raise
    
    async def get_lead(self, lead_id: str, tenant_id: str) -> Optional[Dict[str, Any]]:
        """Buscar lead por ID (com filtro de tenant)"""
        try:
            result = self.client.table('leads')\
                .select('*')\
                .eq('id', lead_id)\
                .eq('tenant_id', tenant_id)\
                .execute()
            
            if result.data:
                return result.data[0]
            return None
        except Exception as e:
            logger.error("Erro ao buscar lead", lead_id=lead_id, error=str(e))
            raise
    
    async def list_leads(self, tenant_id: str, filters: Optional[Dict] = None, 
                        page: int = 1, limit: int = 50) -> Dict[str, Any]:
        """Listar leads com filtros e paginação"""
        try:
            query = self.client.table('leads')\
                .select('*')\
                .eq('tenant_id', tenant_id)
            
            # Aplicar filtros
            if filters:
                if filters.get('status'):
                    query = query.eq('status', filters['status'])
                if filters.get('origem'):
                    query = query.eq('origem', filters['origem'])
                if filters.get('inserido_manual') is not None:
                    query = query.eq('inserido_manual', filters['inserido_manual'])
            
            # Paginação
            offset = (page - 1) * limit
            query = query.range(offset, offset + limit - 1)
            
            # Ordenação
            query = query.order('created_at', desc=True)
            
            result = query.execute()
            
            # Contar total (para paginação)
            count_result = self.client.table('leads')\
                .select('id', count='exact')\
                .eq('tenant_id', tenant_id)\
                .execute()
            
            return {
                'data': result.data,
                'count': count_result.count,
                'page': page,
                'limit': limit,
                'total_pages': (count_result.count + limit - 1) // limit
            }
        except Exception as e:
            logger.error("Erro ao listar leads", error=str(e))
            raise
    
    async def update_lead(self, lead_id: str, tenant_id: str, 
                         update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualizar lead"""
        try:
            result = self.client.table('leads')\
                .update(update_data)\
                .eq('id', lead_id)\
                .eq('tenant_id', tenant_id)\
                .execute()
            
            if result.data:
                logger.info("Lead atualizado", lead_id=lead_id)
                return result.data[0]
            else:
                raise ValueError("Lead não encontrado")
        except Exception as e:
            logger.error("Erro ao atualizar lead", lead_id=lead_id, error=str(e))
            raise
    
    # Session Operations
    async def create_session(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Criar nova sessão de conversa"""
        try:
            result = self.client.table('sessions').insert(session_data).execute()
            logger.info("Sessão criada", session_id=result.data[0]['id'])
            return result.data[0]
        except Exception as e:
            logger.error("Erro ao criar sessão", error=str(e))
            raise
    
    async def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Buscar sessão por ID"""
        try:
            result = self.client.table('sessions')\
                .select('*, leads(*)')\
                .eq('id', session_id)\
                .execute()
            
            if result.data:
                return result.data[0]
            return None
        except Exception as e:
            logger.error("Erro ao buscar sessão", session_id=session_id, error=str(e))
            raise
    
    async def update_session(self, session_id: str, 
                           update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualizar sessão"""
        try:
            result = self.client.table('sessions')\
                .update(update_data)\
                .eq('id', session_id)\
                .execute()
            
            if result.data:
                return result.data[0]
            else:
                raise ValueError("Sessão não encontrada")
        except Exception as e:
            logger.error("Erro ao atualizar sessão", session_id=session_id, error=str(e))
            raise
    
    # Message Operations
    async def create_message(self, message_data: Dict[str, Any]) -> Dict[str, Any]:
        """Criar nova mensagem"""
        try:
            result = self.client.table('messages').insert(message_data).execute()
            return result.data[0]
        except Exception as e:
            logger.error("Erro ao criar mensagem", error=str(e))
            raise
    
    async def get_messages(self, session_id: str) -> List[Dict[str, Any]]:
        """Buscar mensagens de uma sessão"""
        try:
            result = self.client.table('messages')\
                .select('*')\
                .eq('session_id', session_id)\
                .order('created_at', desc=False)\
                .execute()
            
            return result.data
        except Exception as e:
            logger.error("Erro ao buscar mensagens", session_id=session_id, error=str(e))
            raise
    
    # Qualification Operations
    async def create_qualification(self, qualification_data: Dict[str, Any]) -> Dict[str, Any]:
        """Criar qualificação de lead"""
        try:
            result = self.client.table('qualificacoes').insert(qualification_data).execute()
            logger.info("Qualificação criada", lead_id=qualification_data['lead_id'])
            return result.data[0]
        except Exception as e:
            logger.error("Erro ao criar qualificação", error=str(e))
            raise
    
    # Meeting Operations
    async def create_meeting(self, meeting_data: Dict[str, Any]) -> Dict[str, Any]:
        """Criar agendamento"""
        try:
            result = self.client.table('meetings').insert(meeting_data).execute()
            logger.info("Reunião criada", lead_id=meeting_data['lead_id'])
            return result.data[0]
        except Exception as e:
            logger.error("Erro ao criar reunião", error=str(e))
            raise
    
    # Audit Operations
    async def log_audit_event(self, tenant_id: str, user_id: Optional[str], 
                            action: str, resource_type: str, 
                            resource_id: Optional[str], details: Dict[str, Any]) -> None:
        """Registrar evento de auditoria"""
        try:
            audit_data = {
                'tenant_id': tenant_id,
                'user_id': user_id,
                'action': action,
                'resource_type': resource_type,
                'resource_id': resource_id,
                'details': details
            }
            
            self.service_client.table('audit_events').insert(audit_data).execute()
            logger.info("Evento de auditoria registrado", action=action, resource_type=resource_type)
        except Exception as e:
            logger.error("Erro ao registrar auditoria", error=str(e))
            # Não levanta exceção para não interromper o fluxo principal

# Instância global do serviço
supabase_service = SupabaseService()

