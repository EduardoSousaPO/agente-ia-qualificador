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
        self.url = None
        self.service_key = None
        self.client = None
    
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

# Instância global
simple_supabase = SimpleSupabaseService()
