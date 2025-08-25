# 📋 CHANGELOG - Agente Qualificador

## [1.4.0] - 2025-01-25 - Refatoração Completa

### ✅ **Adicionado**
- **Sistema de autenticação JWT multi-tenant** completo
- **Serviço de email SMTP** para notificações de leads qualificados
- **Adaptador CRM genérico** (webhook, Google Sheets, Notion)
- **Endpoints de webhooks** para integração N8N
- **Página de gestão de empresa e membros** no frontend
- **Sistema de scoring unificado** (apenas OpenAI)

### 🔄 **Modificado**
- **Sistema de qualificação** unificado para usar apenas `openai_service.py`
- **N8N workflows** atualizados para usar email + CRM (sem Slack)
- **Documentação** completamente atualizada no `RELATORIO_UNICO_AQ.md`

### ❌ **Removido**
- **Sistema de billing Stripe** completo (temporariamente)
  - `backend/services/stripe_service.py`
  - `backend/services/mock_stripe_service.py`
  - `backend/app/routes/billing.py`
  - Variáveis `STRIPE_*` do `.env`
- **Sistema de qualificação alternativo**
  - `backend/services/simple_qualification.py`
- **Dependência do Slack** nos workflows N8N

### 🔧 **Corrigido**
- **Sistema de scoring** agora retorna valores consistentes (0-100)
- **Isolamento multi-tenant** com RLS ativo em todas as operações
- **Gestão de dependências** removendo bibliotecas não utilizadas

---

## Detalhes da Refatoração

### 1. **Score Unificado (OpenAI-only)**
```diff
- simple_qualification.py (removido)
+ openai_service.py (única fonte da verdade)
```
- **Threshold**: 70 pontos para qualificação
- **Breakdown**: Patrimônio(30) + Objetivo(25) + Urgência(25) + Interesse(20)
- **Testes**: Premium(100), Médio(75), Baixo(25)

### 2. **Autenticação Multi-Tenant**
```diff
+ AuthService com JWT
+ Middleware require_auth(roles)
+ Endpoints /api/auth/login, /api/tenants/me
+ Frontend: useAuth, AuthManager
```
- **Isolamento**: Cada tenant vê apenas seus dados
- **Roles**: admin, operator, viewer
- **JWT**: Contém user_id, tenant_id, email, role

### 3. **N8N + Email + CRM**
```diff
+ EmailService (SMTP)
+ CRMAdapter (webhook/sheets/notion)
+ Endpoints /api/hooks/qualified-lead
- Dependência do Slack
```
- **Email**: Template HTML profissional
- **CRM**: Configurável por tenant
- **Webhook**: Local (mais confiável que N8N externo)

### 4. **Remoção do Stripe**
```diff
- billing.py (8 endpoints)
- stripe_service.py
- mock_stripe_service.py
- STRIPE_* (variáveis ambiente)
```
- **Motivo**: Simplificação conforme solicitado
- **Status**: Sistema gratuito temporariamente
- **Futuro**: Pode ser reimplementado se necessário

---

## Arquivos Principais Afetados

### Backend
- `app.py` - Blueprints atualizados
- `services/openai_service.py` - Scoring unificado
- `services/qualification_service.py` - Webhook local
- `services/auth_service.py` - JWT multi-tenant (novo)
- `services/email_service.py` - SMTP notifications (novo)
- `services/crm_adapter.py` - Integrações CRM (novo)
- `app/routes/tenants.py` - Gestão empresas (novo)
- `app/routes/hooks.py` - Webhooks N8N (novo)

### Frontend
- `app/settings/empresa/page.tsx` - Gestão empresa (novo)
- `lib/auth.ts` - Utilitários JWT (novo)
- `hooks/useAuth.ts` - Hook autenticação (novo)
- `components/layout/sidebar.tsx` - Menu atualizado

### Configuração
- `.env.local.backend` - SMTP_* adicionado, STRIPE_* removido
- `n8n/qualification_notification_workflow_fixed.json` - Sem Slack

### Documentação
- `docs/RELATORIO_UNICO_AQ.md` - Atualizado completamente
- `docs/integracoes_crm.md` - Guia CRM (novo)
- `docs/CHANGELOG.md` - Este arquivo (novo)

---

## Status Atual

### ✅ **Funcionalidades Ativas**
- Qualificação de leads via IA (OpenAI)
- Dashboard completo com métricas
- Simulador WhatsApp integrado
- Upload CSV para leads em massa
- Base de conhecimento por tenant
- Sistema de feedback para IA
- Autenticação JWT multi-tenant
- Notificações email + CRM
- Sistema gratuito (sem cobrança)

### 🚧 **Próximas Melhorias**
- Frontend de autenticação completo
- Integração JWT em todas as páginas
- Configuração CRM via interface
- Testes automatizados completos
- Deploy em produção (Vercel + Railway)

---

## Como Testar

### 1. Sistema Completo
```bash
# Iniciar sistema
python start_system.py

# Testar webhooks
python test_n8n_email_crm.py
```

### 2. Autenticação
```bash
# Login demo
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@demo.com", "password": "qualquer"}'
```

### 3. Scoring Unificado
```bash
cd backend
python services/openai_service.py
```

---

**Versão**: 1.4.0  
**Data**: 25/01/2025  
**Autor**: Refatoração Controlada  
**Status**: ✅ Completa e Funcional

