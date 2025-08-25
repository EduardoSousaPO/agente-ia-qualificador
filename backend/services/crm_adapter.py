#!/usr/bin/env python3
"""
Adaptador CRM Genérico - Suporte a Webhook, Google Sheets, Notion
"""

import os
import json
import requests
from typing import Dict, Optional, Any
from datetime import datetime
import structlog

logger = structlog.get_logger()

class CRMAdapter:
    """Adaptador genérico para integração com diferentes CRMs"""
    
    def __init__(self):
        """Inicializar adaptador CRM"""
        self.timeout = 30  # Timeout para requests HTTP
    
    def send_lead(self, tenant_id: str, lead_payload: Dict) -> Dict:
        """
        Enviar lead para CRM baseado na configuração do tenant
        
        Args:
            tenant_id: ID do tenant
            lead_payload: Dados do lead qualificado
            
        Returns:
            Dict com resultado da operação
        """
        try:
            # Buscar configuração do CRM para o tenant
            crm_config = self._get_tenant_crm_config(tenant_id)
            
            if not crm_config:
                logger.warning("CRM não configurado para tenant", tenant_id=tenant_id)
                return {
                    'success': True,
                    'message': 'CRM não configurado - lead não enviado',
                    'skipped': True
                }
            
            crm_type = crm_config.get('type', 'webhook')
            
            # Roteamento baseado no tipo de CRM
            if crm_type == 'webhook':
                return self._send_to_webhook(crm_config, lead_payload)
            elif crm_type == 'google_sheets_webhook':
                return self._send_to_google_sheets(crm_config, lead_payload)
            elif crm_type == 'notion':
                return self._send_to_notion(crm_config, lead_payload)
            else:
                logger.error("Tipo de CRM não suportado", crm_type=crm_type, tenant_id=tenant_id)
                return {
                    'success': False,
                    'error': f'Tipo de CRM não suportado: {crm_type}'
                }
                
        except Exception as e:
            logger.error("Erro no adaptador CRM", 
                        tenant_id=tenant_id, 
                        error=str(e))
            return {
                'success': False,
                'error': f'Erro no CRM adapter: {str(e)}'
            }
    
    def _get_tenant_crm_config(self, tenant_id: str) -> Optional[Dict]:
        """Buscar configuração do CRM para o tenant"""
        try:
            # Importar aqui para evitar circular import
            from services.simple_supabase import simple_supabase
            
            result = simple_supabase.client.table('tenants') \
                .select('settings') \
                .eq('id', tenant_id) \
                .single() \
                .execute()
            
            if result.data and result.data.get('settings'):
                settings = result.data['settings']
                return settings.get('crm')
            
            return None
            
        except Exception as e:
            logger.error("Erro ao buscar config CRM", tenant_id=tenant_id, error=str(e))
            return None
    
    def _send_to_webhook(self, crm_config: Dict, lead_payload: Dict) -> Dict:
        """Enviar lead para webhook genérico"""
        try:
            url = crm_config.get('url')
            auth_header = crm_config.get('authHeader')
            
            if not url:
                return {
                    'success': False,
                    'error': 'URL do webhook não configurada'
                }
            
            # Preparar headers
            headers = {
                'Content-Type': 'application/json',
                'User-Agent': 'Agente-Qualificador-IA/1.0'
            }
            
            if auth_header:
                if auth_header.startswith('Bearer '):
                    headers['Authorization'] = auth_header
                else:
                    headers['Authorization'] = f'Bearer {auth_header}'
            
            # Payload padronizado para webhook
            webhook_payload = {
                'event': 'qualified_lead',
                'timestamp': datetime.utcnow().isoformat(),
                'lead': {
                    'id': lead_payload.get('lead_id'),
                    'name': lead_payload.get('name'),
                    'email': lead_payload.get('email'),
                    'phone': lead_payload.get('phone'),
                    'score': lead_payload.get('score'),
                    'status': lead_payload.get('status'),
                    'origem': lead_payload.get('origem'),
                    'created_at': lead_payload.get('created_at')
                },
                'source': 'agente-qualificador-ia'
            }
            
            # Fazer request
            response = requests.post(
                url,
                json=webhook_payload,
                headers=headers,
                timeout=self.timeout
            )
            
            if response.status_code in [200, 201, 202]:
                logger.info("Lead enviado para webhook CRM", 
                           url=url[:50] + "...",
                           lead_id=lead_payload.get('lead_id'),
                           status_code=response.status_code)
                
                return {
                    'success': True,
                    'message': f'Lead enviado para CRM webhook (HTTP {response.status_code})',
                    'response_status': response.status_code
                }
            else:
                logger.error("Erro no webhook CRM", 
                           url=url[:50] + "...",
                           status_code=response.status_code,
                           response=response.text[:200])
                
                return {
                    'success': False,
                    'error': f'Webhook retornou HTTP {response.status_code}'
                }
                
        except requests.RequestException as e:
            logger.error("Erro de conexão com webhook CRM", error=str(e))
            return {
                'success': False,
                'error': f'Erro de conexão: {str(e)}'
            }
        except Exception as e:
            logger.error("Erro no envio para webhook", error=str(e))
            return {
                'success': False,
                'error': f'Erro no webhook: {str(e)}'
            }
    
    def _send_to_google_sheets(self, crm_config: Dict, lead_payload: Dict) -> Dict:
        """Enviar lead para Google Sheets via Apps Script webhook"""
        try:
            url = crm_config.get('url')  # URL do Apps Script
            
            if not url:
                return {
                    'success': False,
                    'error': 'URL do Google Sheets não configurada'
                }
            
            # Payload específico para Google Sheets
            sheets_payload = {
                'action': 'add_lead',
                'data': [
                    lead_payload.get('name', ''),
                    lead_payload.get('email', ''),
                    lead_payload.get('phone', ''),
                    lead_payload.get('score', 0),
                    lead_payload.get('status', ''),
                    lead_payload.get('origem', ''),
                    datetime.utcnow().strftime('%d/%m/%Y %H:%M:%S')
                ]
            }
            
            headers = {
                'Content-Type': 'application/json'
            }
            
            response = requests.post(
                url,
                json=sheets_payload,
                headers=headers,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                logger.info("Lead enviado para Google Sheets", 
                           lead_id=lead_payload.get('lead_id'))
                
                return {
                    'success': True,
                    'message': 'Lead adicionado ao Google Sheets'
                }
            else:
                return {
                    'success': False,
                    'error': f'Google Sheets retornou HTTP {response.status_code}'
                }
                
        except Exception as e:
            logger.error("Erro no envio para Google Sheets", error=str(e))
            return {
                'success': False,
                'error': f'Erro no Google Sheets: {str(e)}'
            }
    
    def _send_to_notion(self, crm_config: Dict, lead_payload: Dict) -> Dict:
        """Enviar lead para Notion Database"""
        try:
            token = crm_config.get('token')
            database_id = crm_config.get('database_id')
            
            if not token or not database_id:
                return {
                    'success': False,
                    'error': 'Token ou Database ID do Notion não configurados'
                }
            
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json',
                'Notion-Version': '2022-06-28'
            }
            
            # Payload para Notion Database
            notion_payload = {
                'parent': {'database_id': database_id},
                'properties': {
                    'Nome': {
                        'title': [{'text': {'content': lead_payload.get('name', '')}}]
                    },
                    'Email': {
                        'email': lead_payload.get('email', '')
                    },
                    'Telefone': {
                        'phone_number': lead_payload.get('phone', '')
                    },
                    'Score': {
                        'number': lead_payload.get('score', 0)
                    },
                    'Status': {
                        'select': {'name': lead_payload.get('status', 'qualificado')}
                    },
                    'Origem': {
                        'select': {'name': lead_payload.get('origem', 'WhatsApp')}
                    }
                }
            }
            
            response = requests.post(
                'https://api.notion.com/v1/pages',
                json=notion_payload,
                headers=headers,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                logger.info("Lead enviado para Notion", 
                           lead_id=lead_payload.get('lead_id'))
                
                return {
                    'success': True,
                    'message': 'Lead adicionado ao Notion'
                }
            else:
                return {
                    'success': False,
                    'error': f'Notion API retornou HTTP {response.status_code}'
                }
                
        except Exception as e:
            logger.error("Erro no envio para Notion", error=str(e))
            return {
                'success': False,
                'error': f'Erro no Notion: {str(e)}'
            }

    def test_crm_connection(self, tenant_id: str) -> Dict:
        """Testar conexão com CRM configurado"""
        try:
            crm_config = self._get_tenant_crm_config(tenant_id)
            
            if not crm_config:
                return {
                    'success': False,
                    'error': 'CRM não configurado para este tenant'
                }
            
            # Payload de teste
            test_payload = {
                'lead_id': 'test-lead-123',
                'name': 'Lead de Teste',
                'email': 'teste@exemplo.com',
                'phone': '+55 11 99999-9999',
                'score': 85,
                'status': 'teste',
                'origem': 'teste',
                'created_at': datetime.utcnow().isoformat()
            }
            
            result = self.send_lead(tenant_id, test_payload)
            
            if result['success']:
                return {
                    'success': True,
                    'message': 'Conexão com CRM testada com sucesso',
                    'crm_type': crm_config.get('type', 'webhook')
                }
            else:
                return result
                
        except Exception as e:
            logger.error("Erro no teste de CRM", tenant_id=tenant_id, error=str(e))
            return {
                'success': False,
                'error': f'Erro no teste: {str(e)}'
            }

# Instância global
crm_adapter = CRMAdapter()

