# 🚀 **PROMPT COMPLETO E IDEAL PARA CURSOR AI**

## 📋 **CONTEXTO E PROBLEMA CRÍTICO**

O sistema "Agente Qualificador" precisa implementar um **fluxo completo de registro corporativo** onde novos usuários inserem um **código da empresa** e **nome da empresa**, e essas solicitações precisam ser **aprovadas por um usuário master/admin** da empresa. O sistema deve manter **isolamento completo por tenant** (empresa) e **integração perfeita com Supabase Auth**.

### **🔍 ANÁLISE TÉCNICA ATUAL (CRÍTICA)**

**✅ O QUE JÁ EXISTE:**
- Sistema multi-tenant básico com tabelas: `tenants`, `users`, `memberships`, `profiles`
- Autenticação Supabase configurada
- RLS (Row Level Security) implementado
- Frontend com páginas de login/signup

**❌ PROBLEMAS IDENTIFICADOS:**
- **Banco inconsistente**: Código assume tabela `invites` que não existe
- **Falta coluna `slug` em `tenants`**: Prisma schema vs. banco real desalinhados
- **Falta coluna `code` em `tenants`**: Necessária para company codes
- **Falta tabela `join_requests`**: Para solicitações pendentes sem convite
- **Migrations não aplicadas**: `001_multi_tenant_foundation.sql` não foi executado
- **Interface de signup**: Não tem campo para company code

## 🎯 **MISSÃO CRÍTICA COMPLETA**

Implementar um **sistema robusto de registro corporativo B2B** que permita:

### **FLUXO PRINCIPAL:**
1. **Usuário se registra** → Insere email, senha, nome, **código da empresa** e **nome da empresa**
2. **Sistema valida** → Verifica se empresa existe, se há convite pendente
3. **Cria solicitação** → Se não há convite, cria `join_request` pendente
4. **Notifica admin** → Admin da empresa recebe notificação de nova solicitação
5. **Admin aprova** → Interface para aprovar/rejeitar solicitações
6. **Acesso liberado** → Sistema cria `membership` e usuário acessa apenas dados da sua empresa

### **FUNCIONALIDADES OBRIGATÓRIAS:**
- ✅ **Registro com company code** - Campo obrigatório na tela de signup
- ✅ **Validação de empresa** - Verificar se código existe e está ativo
- ✅ **Sistema de aprovação** - Admins aprovam/rejeitam solicitações
- ✅ **Isolamento por tenant** - Usuário vê apenas dados da sua empresa
- ✅ **Interface admin** - Dashboard para gerenciar solicitações
- ✅ **Notificações** - Alertas para admins sobre novas solicitações
- ✅ **Auditoria completa** - Log de todas as ações de aprovação/rejeição

## 🏗️ **IMPLEMENTAÇÃO FASE A FASE**

### **FASE 1: CORREÇÃO DO BANCO DE DADOS** 🗄️

#### **1.1 Aplicar Migrations Pendentes**
```sql
-- Executar no Supabase SQL Editor:
-- 1. Adicionar coluna slug em tenants
ALTER TABLE public.tenants ADD COLUMN IF NOT EXISTS slug TEXT;
CREATE UNIQUE INDEX IF NOT EXISTS tenants_slug_unique ON public.tenants (slug) WHERE slug IS NOT NULL;

-- 2. Adicionar coluna code em tenants (para company codes)
ALTER TABLE public.tenants ADD COLUMN IF NOT EXISTS code TEXT;
CREATE UNIQUE INDEX IF NOT EXISTS tenants_code_unique ON public.tenants (code) WHERE code IS NOT NULL;

-- 3. Criar tabela invites (do arquivo 001_multi_tenant_foundation.sql)
CREATE TABLE IF NOT EXISTS public.invites (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES public.tenants(id) ON DELETE CASCADE,
  email TEXT NOT NULL,
  role TEXT NOT NULL CHECK (role IN ('admin','member')),
  status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending','accepted','revoked')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE (tenant_id, email)
);

-- 4. Criar tabela join_requests (nova funcionalidade)
CREATE TABLE IF NOT EXISTS public.join_requests (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES public.tenants(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  company_name TEXT NOT NULL,
  company_code TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending','approved','rejected')),
  approved_by UUID REFERENCES auth.users(id),
  approved_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE (tenant_id, user_id)
);
```

#### **1.2 Habilitar RLS e Criar Policies**
```sql
-- RLS para join_requests
ALTER TABLE public.join_requests ENABLE ROW LEVEL SECURITY;

-- Policy: Usuário vê apenas suas próprias solicitações
CREATE POLICY "join_requests_self" ON public.join_requests 
  FOR SELECT USING (user_id = auth.uid());

-- Policy: Admins veem solicitações do seu tenant
CREATE POLICY "join_requests_admin" ON public.join_requests 
  FOR ALL USING (
    EXISTS(
      SELECT 1 FROM public.memberships m 
      WHERE m.tenant_id = join_requests.tenant_id 
      AND m.user_id = auth.uid() 
      AND m.role IN ('admin', 'owner')
    )
  );
```

#### **1.3 Atualizar Schema Prisma**
```prisma
model Tenant {
  id        String   @id @default(dbgenerated("gen_random_uuid()")) @db.Uuid
  name      String   @db.VarChar(255)
  slug      String?  @unique @db.VarChar(255)
  code      String?  @unique @db.VarChar(255)  // NOVO: Company code
  domain    String?  @unique @db.VarChar(255)
  settings  Json     @default("{}")
  createdAt DateTime @default(now()) @map("created_at") @db.Timestamptz(6)
  updatedAt DateTime @default(now()) @updatedAt @map("updated_at") @db.Timestamptz(6)

  // Relations
  users                User[]
  leads                Lead[]
  auditEvents          AuditEvent[]
  memberships          Membership[]
  invites              Invite[]
  joinRequests         JoinRequest[]  // NOVO
  defaultProfiles      Profile[]      @relation("ProfileDefaultTenant")
  knowledgeBase        KnowledgeBase[]

  @@map("tenants")
}

// NOVA TABELA: Join Requests
model JoinRequest {
  id          String    @id @default(dbgenerated("gen_random_uuid()")) @db.Uuid
  tenantId    String    @map("tenant_id") @db.Uuid
  userId      String    @map("user_id") @db.Uuid
  companyName String    @map("company_name") @db.VarChar(255)
  companyCode String    @map("company_code") @db.VarChar(255)
  status      String    @default("pending") @db.VarChar(50) // pending, approved, rejected
  approvedBy  String?   @map("approved_by") @db.Uuid
  approvedAt  DateTime? @map("approved_at") @db.Timestamptz(6)
  createdAt   DateTime  @default(now()) @map("created_at") @db.Timestamptz(6)

  // Relations
  tenant    Tenant @relation(fields: [tenantId], references: [id], onDelete: Cascade)
  
  @@unique([tenantId, userId])
  @@map("join_requests")
}
```

### **FASE 2: BACKEND - APIs DE JOIN REQUESTS** 🔧

#### **2.1 Criar Rotas de Join Requests**
```python
# backend/app/routes/join_requests.py
from flask import Blueprint, request, jsonify, g
from services.auth_service import require_auth
from services.simple_supabase import simple_supabase
from utils.validators import validate_required_fields, validate_email
import structlog

logger = structlog.get_logger()
join_requests_bp = Blueprint('join_requests', __name__)

@join_requests_bp.route('/api/join-requests', methods=['POST'])
def create_join_request():
    """Criar solicitação de acesso à empresa"""
    try:
        data = request.get_json()
        required_fields = ['user_id', 'company_code', 'company_name']
        validation_error = validate_required_fields(data, required_fields)
        if validation_error:
            return jsonify({'error': validation_error}), 400

        # Verificar se empresa existe pelo código
        tenant_result = simple_supabase.client.table('tenants') \
            .select('id, name, code') \
            .eq('code', data['company_code']) \
            .single() \
            .execute()
        
        if not tenant_result.data:
            return jsonify({'error': 'Código da empresa não encontrado'}), 404
        
        tenant = tenant_result.data
        
        # Verificar se já existe solicitação
        existing_request = simple_supabase.client.table('join_requests') \
            .select('id, status') \
            .eq('tenant_id', tenant['id']) \
            .eq('user_id', data['user_id']) \
            .execute()
        
        if existing_request.data:
            status = existing_request.data[0]['status']
            if status == 'pending':
                return jsonify({'error': 'Já existe uma solicitação pendente para esta empresa'}), 409
            elif status == 'approved':
                return jsonify({'error': 'Usuário já foi aprovado para esta empresa'}), 409
        
        # Verificar se já é membro
        existing_membership = simple_supabase.client.table('memberships') \
            .select('id') \
            .eq('tenant_id', tenant['id']) \
            .eq('user_id', data['user_id']) \
            .execute()
        
        if existing_membership.data:
            return jsonify({'error': 'Usuário já é membro desta empresa'}), 409
        
        # Criar solicitação
        join_request_data = {
            'tenant_id': tenant['id'],
            'user_id': data['user_id'],
            'company_name': data['company_name'],
            'company_code': data['company_code'],
            'status': 'pending'
        }
        
        result = simple_supabase.client.table('join_requests') \
            .insert(join_request_data) \
            .execute()
        
        if result.data:
            # TODO: Enviar notificação para admins da empresa
            logger.info("Join request criado", 
                       request_id=result.data[0]['id'],
                       tenant_id=tenant['id'],
                       user_id=data['user_id'])
            
            return jsonify({
                'success': True,
                'message': 'Solicitação enviada com sucesso. Aguarde aprovação do administrador.',
                'request': result.data[0]
            }), 201
        
        return jsonify({'error': 'Falha ao criar solicitação'}), 500
        
    except Exception as e:
        logger.error("Erro ao criar join request", error=str(e))
        return jsonify({'error': 'Erro interno do servidor'}), 500

@join_requests_bp.route('/api/tenants/<tenant_id>/join-requests', methods=['GET'])
@require_auth(roles=['admin', 'owner'])
def get_tenant_join_requests(tenant_id):
    """Listar solicitações pendentes do tenant (apenas admins)"""
    try:
        # Verificar se usuário é admin do tenant
        membership_result = simple_supabase.client.table('memberships') \
            .select('role') \
            .eq('tenant_id', tenant_id) \
            .eq('user_id', g.user_id) \
            .execute()
        
        if not membership_result.data or membership_result.data[0]['role'] not in ['admin', 'owner']:
            return jsonify({'error': 'Acesso negado - permissão insuficiente'}), 403
        
        # Buscar solicitações com dados do usuário
        requests_result = simple_supabase.client.table('join_requests') \
            .select('''
                id,
                user_id,
                company_name,
                company_code,
                status,
                created_at,
                approved_at
            ''') \
            .eq('tenant_id', tenant_id) \
            .order('created_at', desc=True) \
            .execute()
        
        # Buscar dados dos usuários para cada solicitação
        for request in requests_result.data:
            user_result = simple_supabase.client.table('profiles') \
                .select('user_id') \
                .eq('user_id', request['user_id']) \
                .single() \
                .execute()
            
            if user_result.data:
                # Buscar dados do auth.users via RPC ou metadata
                request['user_email'] = 'user@example.com'  # Placeholder - implementar busca real
                request['user_name'] = 'Nome do Usuário'    # Placeholder
        
        return jsonify({
            'success': True,
            'requests': requests_result.data or []
        }), 200
        
    except Exception as e:
        logger.error("Erro ao buscar join requests", 
                    tenant_id=tenant_id, error=str(e))
        return jsonify({'error': 'Erro interno do servidor'}), 500

@join_requests_bp.route('/api/join-requests/<request_id>/approve', methods=['POST'])
@require_auth(roles=['admin', 'owner'])
def approve_join_request(request_id):
    """Aprovar solicitação de acesso"""
    try:
        # Buscar solicitação
        request_result = simple_supabase.client.table('join_requests') \
            .select('*') \
            .eq('id', request_id) \
            .eq('status', 'pending') \
            .single() \
            .execute()
        
        if not request_result.data:
            return jsonify({'error': 'Solicitação não encontrada ou já processada'}), 404
        
        join_request = request_result.data
        
        # Verificar se usuário pode aprovar (é admin do tenant)
        membership_result = simple_supabase.client.table('memberships') \
            .select('role') \
            .eq('tenant_id', join_request['tenant_id']) \
            .eq('user_id', g.user_id) \
            .execute()
        
        if not membership_result.data or membership_result.data[0]['role'] not in ['admin', 'owner']:
            return jsonify({'error': 'Acesso negado - permissão insuficiente'}), 403
        
        data = request.get_json()
        role = data.get('role', 'member')  # Default role
        
        # Criar membership
        membership_data = {
            'tenant_id': join_request['tenant_id'],
            'user_id': join_request['user_id'],
            'role': role
        }
        
        membership_result = simple_supabase.client.table('memberships') \
            .insert(membership_data) \
            .execute()
        
        if membership_result.data:
            # Atualizar status da solicitação
            simple_supabase.client.table('join_requests') \
                .update({
                    'status': 'approved',
                    'approved_by': g.user_id,
                    'approved_at': 'now()'
                }) \
                .eq('id', request_id) \
                .execute()
            
            logger.info("Join request aprovado", 
                       request_id=request_id,
                       tenant_id=join_request['tenant_id'],
                       user_id=join_request['user_id'],
                       approved_by=g.user_id)
            
            return jsonify({
                'success': True,
                'message': 'Solicitação aprovada com sucesso',
                'membership': membership_result.data[0]
            }), 200
        
        return jsonify({'error': 'Falha ao criar membership'}), 500
        
    except Exception as e:
        logger.error("Erro ao aprovar join request", 
                    request_id=request_id, error=str(e))
        return jsonify({'error': 'Erro interno do servidor'}), 500

@join_requests_bp.route('/api/join-requests/<request_id>/reject', methods=['POST'])
@require_auth(roles=['admin', 'owner'])
def reject_join_request(request_id):
    """Rejeitar solicitação de acesso"""
    try:
        # Buscar solicitação
        request_result = simple_supabase.client.table('join_requests') \
            .select('*') \
            .eq('id', request_id) \
            .eq('status', 'pending') \
            .single() \
            .execute()
        
        if not request_result.data:
            return jsonify({'error': 'Solicitação não encontrada ou já processada'}), 404
        
        join_request = request_result.data
        
        # Verificar permissão
        membership_result = simple_supabase.client.table('memberships') \
            .select('role') \
            .eq('tenant_id', join_request['tenant_id']) \
            .eq('user_id', g.user_id) \
            .execute()
        
        if not membership_result.data or membership_result.data[0]['role'] not in ['admin', 'owner']:
            return jsonify({'error': 'Acesso negado - permissão insuficiente'}), 403
        
        # Atualizar status
        result = simple_supabase.client.table('join_requests') \
            .update({
                'status': 'rejected',
                'approved_by': g.user_id,
                'approved_at': 'now()'
            }) \
            .eq('id', request_id) \
            .execute()
        
        if result.data:
            logger.info("Join request rejeitado", 
                       request_id=request_id,
                       tenant_id=join_request['tenant_id'],
                       user_id=join_request['user_id'],
                       rejected_by=g.user_id)
            
            return jsonify({
                'success': True,
                'message': 'Solicitação rejeitada'
            }), 200
        
        return jsonify({'error': 'Falha ao rejeitar solicitação'}), 500
        
    except Exception as e:
        logger.error("Erro ao rejeitar join request", 
                    request_id=request_id, error=str(e))
        return jsonify({'error': 'Erro interno do servidor'}), 500
```

#### **2.2 Registrar Blueprint no App Principal**
```python
# backend/app.py
from app.routes.join_requests import join_requests_bp

app.register_blueprint(join_requests_bp)
```

### **FASE 3: FRONTEND - INTERFACE DE REGISTRO** 💻

#### **3.1 Atualizar Página de Signup**
```typescript
// frontend/src/app/signup/page.tsx - Adicionar campos de empresa

// Adicionar ao schema de validação
const signupSchema = z.object({
  name: z.string().min(2, 'Nome deve ter pelo menos 2 caracteres'),
  email: z.string().email('Email inválido'),
  password: z.string().min(6, 'Senha deve ter pelo menos 6 caracteres'),
  confirmPassword: z.string(),
  companyCode: z.string().min(3, 'Código da empresa é obrigatório'),
  companyName: z.string().min(2, 'Nome da empresa é obrigatório'),
  acceptTerms: z.boolean().refine(val => val, 'Você deve aceitar os termos')
}).refine((data) => data.password === data.confirmPassword, {
  message: "Senhas não coincidem",
  path: ["confirmPassword"]
})

// Adicionar campos no formulário (após o campo email):
{/* Código da Empresa */}
<div>
  <label htmlFor="companyCode" className="block text-sm font-medium text-gray-700">
    Código da empresa *
  </label>
  <input
    {...register('companyCode')}
    type="text"
    className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
    placeholder="Ex: ACME-2024"
  />
  {errors.companyCode && (
    <p className="mt-1 text-sm text-red-600">{errors.companyCode.message}</p>
  )}
</div>

{/* Nome da Empresa */}
<div>
  <label htmlFor="companyName" className="block text-sm font-medium text-gray-700">
    Nome da empresa *
  </label>
  <input
    {...register('companyName')}
    type="text"
    className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
    placeholder="Ex: ACME Corporation"
  />
  {errors.companyName && (
    <p className="mt-1 text-sm text-red-600">{errors.companyName.message}</p>
  )}
</div>

// Atualizar função onSubmit:
const onSubmit = async (data: SignupFormData) => {
  setLoading(true)
  
  try {
    // 1. Criar conta no Supabase Auth
    const { data: authData, error: authError } = await supabase.auth.signUp({
      email: data.email,
      password: data.password,
      options: {
        data: {
          full_name: data.name
        }
      }
    })

    if (authError) throw new Error(authError.message)
    if (!authData.user) throw new Error('Erro ao criar usuário')

    // 2. Criar solicitação de acesso à empresa
    const joinRequestResponse = await fetch('http://localhost:5000/api/join-requests', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_id: authData.user.id,
        company_code: data.companyCode,
        company_name: data.companyName
      })
    })

    const joinRequestResult = await joinRequestResponse.json()

    if (joinRequestResponse.ok) {
      toast.success('Conta criada! Sua solicitação foi enviada para aprovação.')
      router.push('/login?message=pending-approval')
    } else {
      throw new Error(joinRequestResult.error || 'Erro ao enviar solicitação')
    }

  } catch (error: any) {
    console.error('Erro no signup:', error)
    toast.error(error.message || 'Erro ao criar conta')
  } finally {
    setLoading(false)
  }
}
```

#### **3.2 Atualizar Página de Login (Mensagem de Aprovação Pendente)**
```typescript
// frontend/src/app/login/page.tsx - Adicionar mensagem de aprovação pendente

useEffect(() => {
  const message = searchParams.get('message')
  if (message === 'pending-approval') {
    toast.info('Sua solicitação está pendente de aprovação. Você receberá um email quando for aprovado.', {
      duration: 8000
    })
  }
}, [searchParams])
```

### **FASE 4: FRONTEND - INTERFACE ADMIN** 👨‍💼

#### **4.1 Criar Página de Gerenciamento de Solicitações**
```typescript
// frontend/src/app/admin/join-requests/page.tsx
'use client'

import { useState, useEffect } from 'react'
import { DashboardLayout } from '@/components/layout/dashboard-layout'
import { useAuth } from '@/components/providers'
import toast from 'react-hot-toast'

interface JoinRequest {
  id: string
  user_id: string
  user_email: string
  user_name: string
  company_name: string
  company_code: string
  status: 'pending' | 'approved' | 'rejected'
  created_at: string
  approved_at?: string
}

export default function JoinRequestsPage() {
  const [requests, setRequests] = useState<JoinRequest[]>([])
  const [loading, setLoading] = useState(true)
  const [processing, setProcessing] = useState<string | null>(null)
  const { user } = useAuth()

  useEffect(() => {
    loadJoinRequests()
  }, [user])

  const loadJoinRequests = async () => {
    if (!user?.tenant?.id) return

    try {
      setLoading(true)
      const response = await fetch(`http://localhost:5000/api/tenants/${user.tenant.id}/join-requests`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json'
        }
      })

      if (response.ok) {
        const result = await response.json()
        setRequests(result.requests || [])
      } else {
        toast.error('Erro ao carregar solicitações')
      }
    } catch (error) {
      toast.error('Erro ao carregar solicitações')
    } finally {
      setLoading(false)
    }
  }

  const handleApprove = async (requestId: string, role: string = 'member') => {
    try {
      setProcessing(requestId)
      const response = await fetch(`http://localhost:5000/api/join-requests/${requestId}/approve`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ role })
      })

      if (response.ok) {
        toast.success('Solicitação aprovada com sucesso!')
        loadJoinRequests() // Recarregar lista
      } else {
        const result = await response.json()
        toast.error(result.error || 'Erro ao aprovar solicitação')
      }
    } catch (error) {
      toast.error('Erro ao aprovar solicitação')
    } finally {
      setProcessing(null)
    }
  }

  const handleReject = async (requestId: string) => {
    try {
      setProcessing(requestId)
      const response = await fetch(`http://localhost:5000/api/join-requests/${requestId}/reject`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json'
        }
      })

      if (response.ok) {
        toast.success('Solicitação rejeitada')
        loadJoinRequests() // Recarregar lista
      } else {
        const result = await response.json()
        toast.error(result.error || 'Erro ao rejeitar solicitação')
      }
    } catch (error) {
      toast.error('Erro ao rejeitar solicitação')
    } finally {
      setProcessing(null)
    }
  }

  if (loading) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        </div>
      </DashboardLayout>
    )
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Solicitações de Acesso</h1>
          <p className="text-gray-600">Gerencie solicitações de novos membros para sua empresa</p>
        </div>

        {/* Estatísticas */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white p-6 rounded-lg shadow-sm border">
            <div className="text-2xl font-bold text-yellow-600">
              {requests.filter(r => r.status === 'pending').length}
            </div>
            <div className="text-sm text-gray-600">Pendentes</div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-sm border">
            <div className="text-2xl font-bold text-green-600">
              {requests.filter(r => r.status === 'approved').length}
            </div>
            <div className="text-sm text-gray-600">Aprovadas</div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-sm border">
            <div className="text-2xl font-bold text-red-600">
              {requests.filter(r => r.status === 'rejected').length}
            </div>
            <div className="text-sm text-gray-600">Rejeitadas</div>
          </div>
        </div>

        {/* Lista de Solicitações */}
        <div className="bg-white shadow-sm rounded-lg border">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-lg font-medium text-gray-900">
              Solicitações ({requests.length})
            </h2>
          </div>
          
          {requests.length === 0 ? (
            <div className="p-12 text-center">
              <div className="text-gray-400 text-lg mb-2">📋</div>
              <p className="text-gray-500">Nenhuma solicitação encontrada</p>
            </div>
          ) : (
            <div className="divide-y divide-gray-200">
              {requests.map((request) => (
                <div key={request.id} className="p-6">
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3">
                        <div className="flex-shrink-0">
                          <div className="h-8 w-8 bg-gray-200 rounded-full flex items-center justify-center">
                            <span className="text-sm font-medium text-gray-600">
                              {request.user_name?.charAt(0) || request.user_email?.charAt(0) || '?'}
                            </span>
                          </div>
                        </div>
                        <div>
                          <p className="text-sm font-medium text-gray-900">
                            {request.user_name || 'Nome não informado'}
                          </p>
                          <p className="text-sm text-gray-500">{request.user_email}</p>
                        </div>
                      </div>
                      <div className="mt-2 text-sm text-gray-600">
                        <span className="font-medium">Empresa:</span> {request.company_name}
                        <span className="ml-4 font-medium">Código:</span> {request.company_code}
                      </div>
                      <div className="mt-1 text-xs text-gray-400">
                        Solicitado em {new Date(request.created_at).toLocaleString('pt-BR')}
                      </div>
                    </div>

                    <div className="flex items-center space-x-3">
                      {/* Status Badge */}
                      <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${
                        request.status === 'pending' 
                          ? 'bg-yellow-100 text-yellow-800'
                          : request.status === 'approved'
                          ? 'bg-green-100 text-green-800'
                          : 'bg-red-100 text-red-800'
                      }`}>
                        {request.status === 'pending' ? 'Pendente' : 
                         request.status === 'approved' ? 'Aprovado' : 'Rejeitado'}
                      </span>

                      {/* Actions */}
                      {request.status === 'pending' && (
                        <div className="flex space-x-2">
                          <button
                            onClick={() => handleApprove(request.id)}
                            disabled={processing === request.id}
                            className="bg-green-600 text-white px-3 py-1 text-sm rounded hover:bg-green-700 disabled:opacity-50"
                          >
                            {processing === request.id ? '...' : 'Aprovar'}
                          </button>
                          <button
                            onClick={() => handleReject(request.id)}
                            disabled={processing === request.id}
                            className="bg-red-600 text-white px-3 py-1 text-sm rounded hover:bg-red-700 disabled:opacity-50"
                          >
                            {processing === request.id ? '...' : 'Rejeitar'}
                          </button>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </DashboardLayout>
  )
}
```

#### **4.2 Adicionar Link no Menu de Navegação**
```typescript
// frontend/src/components/layout/dashboard-layout.tsx - Adicionar no menu

// Adicionar no array de navigation (apenas para admins):
{
  name: 'Solicitações',
  href: '/admin/join-requests',
  icon: UserPlusIcon,
  current: pathname === '/admin/join-requests',
  adminOnly: true // Mostrar apenas para admins
}
```

### **FASE 5: DADOS DE EXEMPLO E TESTES** 🧪

#### **5.1 Popular Banco com Dados de Teste**
```sql
-- Executar no Supabase SQL Editor:

-- 1. Criar empresa de exemplo com código
INSERT INTO public.tenants (name, slug, code, settings)
VALUES (
  'Escritório de Investimentos Demo',
  'demo',
  'DEMO2024',
  '{"company_type": "investment_advisory"}'::jsonb
)
ON CONFLICT (slug) DO UPDATE SET
  code = EXCLUDED.code,
  updated_at = NOW();

-- 2. Obter ID do tenant para próximos passos
-- (Usar o ID retornado nos próximos comandos)
```

#### **5.2 Cenários de Teste Obrigatórios**

**✅ TESTE 1: Registro com Código Válido**
1. Acessar `/signup`
2. Preencher: nome, email, senha, company_code: `DEMO2024`, company_name: `Escritório de Investimentos Demo`
3. Submeter formulário
4. **Resultado esperado**: Conta criada, join_request pendente, redirecionamento para login com mensagem

**✅ TESTE 2: Código de Empresa Inválido**
1. Usar company_code: `INVALID123`
2. **Resultado esperado**: Erro "Código da empresa não encontrado"

**✅ TESTE 3: Aprovação por Admin**
1. Login como admin da empresa
2. Acessar `/admin/join-requests`
3. Ver solicitação pendente
4. Clicar "Aprovar"
5. **Resultado esperado**: Membership criado, usuário pode fazer login

**✅ TESTE 4: Rejeição por Admin**
1. Clicar "Rejeitar" em solicitação
2. **Resultado esperado**: Status alterado para rejected

**✅ TESTE 5: Isolamento por Tenant**
1. Login como usuário aprovado
2. **Resultado esperado**: Ver apenas dados da sua empresa

### **FASE 6: SEGURANÇA E VALIDAÇÕES** 🔒

#### **6.1 Validações Obrigatórias**
- ✅ **Company Code único** por tenant
- ✅ **RLS policies** impedem acesso cross-tenant
- ✅ **Validação de roles** - apenas admins aprovam
- ✅ **Prevenção de duplicatas** - uma solicitação por usuário/tenant
- ✅ **Sanitização de inputs** - prevenir XSS/SQL injection
- ✅ **Rate limiting** - prevenir spam de solicitações

#### **6.2 Auditoria e Logs**
- ✅ **Log de aprovações/rejeições** com timestamp e admin responsável
- ✅ **Histórico de solicitações** para compliance
- ✅ **Métricas de conversão** - quantas solicitações são aprovadas

## 🎯 **CRITÉRIOS DE SUCESSO**

### **FUNCIONAL:**
- ✅ Usuário consegue se registrar com company code
- ✅ Admin recebe notificação de nova solicitação
- ✅ Admin consegue aprovar/rejeitar via interface
- ✅ Usuário aprovado acessa apenas dados da sua empresa
- ✅ Sistema impede acesso cross-tenant

### **TÉCNICO:**
- ✅ Zero erros no console
- ✅ APIs respondem em <2s
- ✅ RLS policies funcionam corretamente
- ✅ Banco de dados consistente
- ✅ Código limpo e bem documentado

### **UX:**
- ✅ Interface intuitiva e responsiva
- ✅ Mensagens de erro claras
- ✅ Feedback visual adequado
- ✅ Fluxo sem fricção desnecessária

## 🚀 **RESULTADO FINAL ESPERADO**

Um **sistema completo de registro corporativo B2B** que permite:

1. **Usuários** se registram com código da empresa
2. **Admins** aprovam solicitações via dashboard
3. **Isolamento total** por tenant/empresa
4. **Auditoria completa** de todas as ações
5. **Interface moderna** e intuitiva
6. **Segurança robusta** com RLS e validações
7. **Performance otimizada** para escala

**💡 OBJETIVO**: Transformar o sistema em uma plataforma B2B profissional com controle total de acesso por empresa, mantendo a simplicidade de uso e a segurança de dados.

---

**🎯 COMEÇE PELA FASE 1** - Correção do banco de dados é crítica para tudo funcionar!



