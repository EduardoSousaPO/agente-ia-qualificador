# Multi-Tenant Discovery Report

## 📊 ANÁLISE DO ESTADO ATUAL

### ✅ **Estruturas Multi-Tenant EXISTENTES**

#### 1. **Tabelas com Tenant Support**
- ✅ `tenants` - Estrutura básica já implementada
- ✅ `users` - Com `tenant_id` FK
- ✅ `leads` - Com `tenant_id` FK  
- ✅ `audit_events` - Com `tenant_id` FK
- ✅ Todas as tabelas de domínio já têm `tenant_id`

#### 2. **RLS Policies Existentes**
- ✅ Políticas RLS implementadas e ativas
- ✅ Isolamento por `tenant_id` via JWT claims
- ✅ Função `auth.jwt() ->> 'tenant_id'` em uso

#### 3. **Backend Auth & Middleware**
- ✅ `AuthService` com JWT
- ✅ Decorator `@require_auth(roles)` 
- ✅ Context injection via `g.tenant_id`, `g.user_id`
- ✅ Rota `/api/tenants/me` para dados do tenant
- ✅ Gestão de membros em `/api/tenants/<id>/members`

#### 4. **Frontend Auth**
- ✅ Supabase Auth integration
- ✅ `useAuth` hook e context
- ✅ API client com auth headers
- ✅ Tenant display em sidebar

### ❌ **GAPS IDENTIFICADOS (não atende SPEC)**

#### 1. **Estruturas Faltantes da SPEC**
- ❌ **Tabela `profiles`** (vincula auth.users)
- ❌ **Tabela `memberships`** (many-to-many user/tenant)
- ❌ **Tabela `invites`** (sistema de convites Slack-like)
- ❌ **Função `is_member()`** (helper RLS)
- ❌ **Trigger auto-membership** via invite

#### 2. **Rotas Faltantes**
- ❌ **Estrutura `/app/[tenantSlug]/...`** (rotas atuais são flat)
- ❌ **Middleware tenantSlug resolver**
- ❌ **TenantSwitcher component**
- ❌ **Convite workflow** (signup via email)

#### 3. **RLS Policies Inadequadas**
- ❌ Policies atuais usam JWT claims, **SPEC requer `is_member()` function**
- ❌ Falta policies para `profiles`, `memberships`, `invites`
- ❌ Auto-membership trigger ausente

#### 4. **Knowledge Base Multi-Tenant**
- ❌ Knowledge tables sem `tenant_id` (se existirem)
- ❌ UI de knowledge não filtra por tenant

### 🏗️ **ARQUITETURA ATUAL vs SPEC**

#### **Atual (Funcional, mas não conforme SPEC)**
```
tenants -> users (tenant_id) -> RLS via JWT claims
```

#### **SPEC Requerida**
```
tenants -> memberships <- users (auth.users)
         -> profiles <- users (auth.users)  
         -> invites -> auto-membership trigger
```

### 📋 **DECISÃO DE IMPLEMENTAÇÃO**

**VEREDICTO**: O sistema atual tem funcionalidade multi-tenant básica, mas **NÃO atende à especificação exata** do item 3 (SPEC).

**AÇÃO**: Implementar a especificação completa:
1. ✅ Manter tabelas existentes que não conflitam
2. 🔄 Adicionar estruturas faltantes (profiles, memberships, invites)
3. 🔄 Migrar RLS policies para usar `is_member()`
4. 🔄 Implementar rotas `/app/[tenantSlug]/...`
5. 🔄 Adicionar sistema de convites
6. 🔄 Criar TenantSwitcher e workflow completo

### 🎯 **COMPATIBILIDADE**

**Tabelas a MANTER**:
- `tenants` ✅ (compatível com SPEC)
- `users` ✅ (será complementada por `profiles`)
- Todas as tabelas de domínio ✅ (já têm `tenant_id`)

**Tabelas a ADICIONAR**:
- `profiles` (nova)
- `memberships` (nova)  
- `invites` (nova)

**Código a MANTER**:
- Backend routes existentes ✅
- Frontend components existentes ✅
- AuthService base ✅

**Código a MODIFICAR**:
- RLS policies (migrar para `is_member()`)
- Frontend routing (adicionar tenantSlug)
- Middleware (tenantSlug resolver)

### 📈 **IMPACTO DA MIGRAÇÃO**

- **Risco**: Baixo (aditivo, não destrutivo)
- **Downtime**: Zero (migrations com `IF NOT EXISTS`)
- **Compatibilidade**: Mantida (tabelas existentes preservadas)
- **Benefícios**: Conformidade total com SPEC + sistema de convites

---

## 🔄 **PRÓXIMOS PASSOS**

1. ✅ Completar discovery ← **ATUAL**
2. 🔄 Implementar migrations SQL (SPEC completa)
3. 🔄 Atualizar RLS policies
4. 🔄 Implementar rotas tenantSlug
5. 🔄 Criar sistema de convites
6. 🔄 Seed LDC Capital
7. 🔄 Testes de aceite











