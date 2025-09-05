#!/usr/bin/env python3
"""
Serviço Supabase Simplificado (Síncrono)
"""

import os
from supabase import create_client
from typing import Dict, Optional
import structlog

logger = structlog.get_logger()

class SimpleSupabaseService:
    def __init__(self):
        """Inicializar serviço Supabase com carregamento robusto"""
        # Garantir carregamento do .env
        self._load_environment()
        
        self.url = None
        self.service_key = None
        self.client = None
        self._ensure_client()
    
    def _load_environment(self):
        """Carregar variáveis de ambiente - APENAS .env real"""
        from dotenv import load_dotenv
        load_dotenv()  # Carrega apenas o .env do diretório atual
    def _ensure_client(self):
        """Garantir que o cliente está inicializado"""
        if self.client is None:
            self.url = os.getenv('SUPABASE_URL')
            self.service_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
            
            if not self.url or not self.service_key:
                raise Exception("SUPABASE_URL e SUPABASE_SERVICE_ROLE_KEY são obrigatórios")
                
            self.client = create_client(self.url, self.service_key)
    
    def create_session(self, session_data: Dict) -> Dict:
        """Criar nova sessão"""
        try:
            self._ensure_client()
            result = self.client.table('sessions').insert(session_data).execute()
            return result.data[0]
        except Exception as e:
            logger.error("Erro ao criar sessão", error=str(e))
            raise
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """Buscar sessão por ID"""
        try:
            self._ensure_client()
            result = self.client.table('sessions')\
                .select('*, leads(*)')\
                .eq('id', session_id)\
                .execute()
            
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error("Erro ao buscar sessão", error=str(e))
            return None
    
    def update_session(self, session_id: str, update_data: Dict) -> bool:
        """Atualizar sessão"""
        try:
            self._ensure_client()
            self.client.table('sessions')\
                .update(update_data)\
                .eq('id', session_id)\
                .execute()
            return True
        except Exception as e:
            logger.error("Erro ao atualizar sessão", error=str(e))
            return False
    
    def create_message(self, message_data: Dict) -> Dict:
        """Criar nova mensagem"""
        try:
            self._ensure_client()
            result = self.client.table('messages').insert(message_data).execute()
            return result.data[0]
        except Exception as e:
            logger.error("Erro ao criar mensagem", error=str(e))
            raise
    
    def get_messages(self, session_id: str) -> list:
        """Buscar mensagens de uma sessão"""
        try:
            self._ensure_client()
            result = self.client.table('messages')\
                .select('*')\
                .eq('session_id', session_id)\
                .order('created_at')\
                .execute()
            
            return result.data
        except Exception as e:
            logger.error("Erro ao buscar mensagens", error=str(e))
            return []
    
    def get_lead(self, lead_id: str) -> Optional[Dict]:
        """Buscar lead por ID"""
        try:
            self._ensure_client()
            result = self.client.table('leads')\
                .select('*')\
                .eq('id', lead_id)\
                .execute()
            
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error("Erro ao buscar lead", error=str(e))
            return None
    
    def update_lead(self, lead_id: str, update_data: Dict) -> bool:
        """Atualizar lead"""
        try:
            self._ensure_client()
            self.client.table('leads')\
                .update(update_data)\
                .eq('id', lead_id)\
                .execute()
            return True
        except Exception as e:
            logger.error("Erro ao atualizar lead", error=str(e))
            return False
    
    def get_sessions_by_tenant(self, tenant_id: str, limit: int = 20, offset: int = 0) -> Dict:
        """Buscar sessões por tenant com paginação"""
        try:
            self._ensure_client()
            
            response = self.client.table('sessions').select(
                'id, lead_id, status, current_step, context, created_at, updated_at, leads(phone, name)'
            ).eq('tenant_id', tenant_id).order('created_at', desc=True).limit(limit).offset(offset).execute()
            
            # Contar total
            count_response = self.client.table('sessions').select('id', count='exact').eq('tenant_id', tenant_id).execute()
            
            return {
                'data': response.data,
                'count': count_response.count if count_response.count else 0
            }
            
        except Exception as e:
            logger.error(f"Erro ao buscar sessões: {str(e)}")
            return {'data': [], 'count': 0}
    
    def get_messages_by_session(self, session_id: str) -> list:
        """Buscar mensagens de uma sessão específica"""
        try:
            self._ensure_client()
            
            response = self.client.table('messages').select(
                'id, session_id, direction, content, message_type, created_at'
            ).eq('session_id', session_id).order('created_at', desc=False).execute()
            
            return response.data
            
        except Exception as e:
            logger.error(f"Erro ao buscar mensagens da sessão {session_id}: {str(e)}")
            return []

# Instância global
simple_supabase = SimpleSupabaseService()
