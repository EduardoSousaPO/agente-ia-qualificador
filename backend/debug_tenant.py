#!/usr/bin/env python3
"""
Debug - Testar endpoint de tenant
"""

import sys
import os
sys.path.append('.')

from services.simple_supabase import simple_supabase

def debug_tenant():
    """Debug do tenant"""
    print("🔍 DEBUG - TENANT ENDPOINT")
    print("=" * 40)
    
    try:
        # Testar conexão
        client = simple_supabase.client
        print("✅ Cliente Supabase conectado")
        
        # Buscar tenant por slug
        slug = "demo"
        print(f"\n📋 Buscando tenant com slug: {slug}")
        
        tenant_result = client.table('tenants') \
            .select('*') \
            .eq('slug', slug) \
            .execute()
        
        print(f"📊 Resultado tenant: {tenant_result.data}")
        
        if tenant_result.data:
            tenant = tenant_result.data[0]
            tenant_id = tenant['id']
            print(f"✅ Tenant encontrado: {tenant_id}")
            
            # Buscar membership
            user_id = '5f9c5ba8-0ad7-43a6-92df-c205cb6b5e23'
            print(f"\n👤 Buscando membership para user: {user_id}")
            
            membership_result = client.table('memberships') \
                .select('role, created_at') \
                .eq('tenant_id', tenant_id) \
                .eq('user_id', user_id) \
                .execute()
            
            print(f"📊 Resultado membership: {membership_result.data}")
            
            if membership_result.data:
                print("✅ Membership encontrado")
            else:
                print("❌ Membership não encontrado")
                
                # Criar membership se não existir
                print("🔧 Criando membership...")
                create_result = client.table('memberships').insert({
                    'tenant_id': tenant_id,
                    'user_id': user_id,
                    'role': 'admin'
                }).execute()
                
                print(f"📊 Membership criado: {create_result.data}")
        else:
            print("❌ Tenant não encontrado")
            
            # Criar tenant se não existir
            print("🔧 Criando tenant demo...")
            create_tenant = client.table('tenants').insert({
                'name': 'Empresa Demo',
                'slug': 'demo',
                'domain': 'demo.localhost',
                'settings': {}
            }).execute()
            
            print(f"📊 Tenant criado: {create_tenant.data}")
            
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_tenant()

