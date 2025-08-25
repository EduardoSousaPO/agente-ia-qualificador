# RELATÓRIO ÚNICO – Agente Qualificador

**Data da Auditoria**: 25/01/2025  
**Versão do Sistema**: 2.0.0  
**Status**: ✅ Sistema Funcional com Melhorias Implementadas

---

## 1. 📋 Resumo Executivo

O **Agente Qualificador** é um **micro SaaS B2B** para qualificação inteligente de leads via WhatsApp, focado em escritórios de consultoria e assessoria de investimentos.

### ✅ O que o app faz hoje:

- **Qualifica leads automaticamente** via WhatsApp com IA (GPT-4o/4o-mini)
- **Sistema de pontuação 0-100** baseado em 4 perguntas (Patrimônio, Objetivo, Urgência, Interesse)
- **Dashboard completo** para gestão de leads, conversas e métricas
- **Automação N8N** para intake de leads e notificações
- **Multi-tenancy** com isolamento completo por cliente (RLS)
- **Sistema gratuito** (billing removido temporariamente)
- **Base de conhecimento** personalizável por tenant
- **Simulador WhatsApp** integrado para testes
- **Upload CSV** para importação em massa de leads
- **Feedback loop** para melhoria contínua da IA

### 🎯 Diferencial Competitivo:
- **Setup < 30 minutos** (plug-and-play)
- **Scoring transparente** e ajustável
- **Interface Tesla-style** minimalista
- **Integração completa** WhatsApp + IA + CRM

---

## 2. 🗂️ Mapa do Repositório

```
agente_qualificador/
├── 📱 frontend/                    # Next.js 15 + TypeScript + Tailwind
│   ├── src/app/                   # App Router (Next.js 13+)
│   │   ├── dashboard/             # Métricas e visão geral
│   │   ├── leads/                 # Gestão de leads
│   │   ├── conversations/         # Chat WhatsApp
│   │   ├── settings/              # Configurações + Knowledge Base
│   │   └── exemplos/              # Simulador de conversas
│   ├── src/components/            # Componentes React organizados
│   │   ├── dashboard/             # Gráficos e estatísticas
│   │   ├── leads/                 # CRUD de leads
│   │   ├── conversations/         # Interface de chat
│   │   └── layout/                # Header, sidebar, layout
│   └── src/lib/                   # Utilitários (Supabase, API)
│
├── ⚙️ backend/                     # Flask 3.0 + Python 3.11+
│   ├── app/routes/                # Endpoints REST organizados
│   │   ├── auth.py               # Autenticação JWT
│   │   ├── leads.py              # CRUD + qualificação manual
│   │   ├── chat.py               # Sessões de conversa
│   │   ├── hooks.py              # Webhooks N8N + Email/CRM
│   │   ├── knowledge.py          # Base de conhecimento
│   │   └── settings.py           # Configurações do tenant
│   ├── services/                  # Lógica de negócio
│   │   ├── qualification_service.py    # Orquestração principal
│   │   ├── simple_qualification.py    # Sistema de scoring
│   │   ├── openai_service.py          # Integração GPT
│   │   ├── simple_twilio.py           # WhatsApp + simulador
│   │   ├── stripe_service.py          # Billing + mock
│   │   └── n8n_service.py             # Webhooks automação
│   └── utils/                     # Validadores e helpers
│
├── 🗄️ database/                   # Supabase PostgreSQL
│   └── prisma/schema.prisma      # 10 tabelas + RLS policies
│
├── 🔄 n8n/                        # 9 Workflows de automação
│   ├── intake_complete_workflow.json      # Captação de leads
│   ├── qualification_notification.json   # Notificações
│   ├── complete_whatsapp_workflow.json   # Fluxo WhatsApp
│   └── ...                               # + 6 workflows
│
├── 📊 docs/                       # Documentação e relatórios
│   ├── execucao/                 # Sprints e status
│   ├── archive/                  # Arquivos históricos
│   └── reports/                  # Relatórios automáticos
│
└── 🛠️ scripts/                    # Automação e utilitários
    ├── execution_controller.py   # Controle de sprints
    ├── test_suite.py            # Testes automatizados
    └── cleanup_and_archive.py   # Limpeza automática
```

---

## 3. 🔧 Stack Detectada

### **Frontend**
- **Framework**: Next.js 15.4.7 (App Router)
- **Language**: TypeScript 5.6.3
- **Styling**: Tailwind CSS 3.4.17
- **UI Components**: Headless UI, Heroicons, Lucide React
- **Charts**: Recharts 2.12.7
- **State Management**: React hooks + Context
- **HTTP Client**: Axios 1.7.7
- **File Upload**: React Dropzone + PapaParse (CSV)

### **Backend**
- **Framework**: Flask 3.0.0
- **Language**: Python 3.11+
- **Database ORM**: Supabase Client 2.3.4
- **Authentication**: Flask-JWT-Extended 4.6.0
- **API Documentation**: Estruturado com blueprints
- **Validation**: Cerberus + custom validators
- **Logging**: Structlog 23.2.0

### **Database**
- **Provider**: Supabase PostgreSQL
- **Schema**: Prisma (10 tabelas principais)
- **Security**: Row Level Security (RLS) ativo
- **Multi-tenancy**: Isolamento por `tenant_id`

### **Integrações**
- **IA**: OpenAI GPT-4o/4o-mini
- **Messaging**: Twilio WhatsApp API + simulador
- **Automation**: N8N Cloud (9 workflows)
- **Payments**: Sistema gratuito (sem cobrança)
- **Deployment**: Configurado para Vercel + Railway

---

## 4. 📱 Frontend (Next.js)

### **Rotas Principais**
```typescript
/                           # Landing page
/dashboard                  # Visão geral + métricas
/leads                      # Gestão de leads (CRUD + CSV)
/conversations              # Lista de conversas WhatsApp
/conversations/[id]         # Chat individual
/settings                   # Configurações do tenant
/settings/knowledge         # Base de conhecimento IA
/settings/feedback          # Validação do agente
/exemplos                   # Simulador de conversas
/login                      # Autenticação (placeholder)
```

### **Componentes Críticos**

#### **Dashboard (`src/components/dashboard/`)**
- `dashboard-stats.tsx` - Métricas principais (leads, conversões, score médio)
- `leads-chart.tsx` - Gráfico de leads por período
- `active-conversations.tsx` - Conversas em andamento
- `recent-leads.tsx` - Últimos leads capturados
- `qualified-leads-dashboard.tsx` - Leads qualificados
- `qualification-scenarios.tsx` - Cenários de teste

#### **Leads (`src/components/leads/`)**
- `leads-list.tsx` - Tabela com filtros e paginação
- `lead-details-modal.tsx` - Detalhes + histórico de conversa
- `new-lead-modal.tsx` - Cadastro manual
- `upload-csv-modal.tsx` - Importação em massa
- `leads-filters.tsx` - Filtros avançados

#### **Conversas (`src/components/conversations/`)**
- `chat-interface.tsx` - Interface de chat WhatsApp
- `conversations-list.tsx` - Lista de sessões ativas
- `conversation-header.tsx` - Cabeçalho com info do lead
- `conversation-sidebar.tsx` - Detalhes da qualificação
- `conversation-filters.tsx` - Filtros de status

### **Estado Global**
- **Supabase Context**: Autenticação e cliente DB
- **API Client**: Axios configurado para backend Flask
- **Toast Notifications**: React Hot Toast
- **Loading States**: Componente `loading-spinner.tsx`

### **UI da Qualificação**
A qualificação acontece através do **chat WhatsApp simulado** em:
- `/conversations/[id]` - Interface principal de chat
- `/exemplos` - Simulador para testes
- **4 etapas obrigatórias**: patrimônio → objetivo → urgência → interesse
- **Score visual**: Barra de progresso 0-100 pontos
- **Status em tempo real**: ativo, qualificado, desqualificado

---

## 5. ⚙️ Backend (Flask)

### **Endpoints REST**

#### **🔐 Autenticação (`/api/auth`)**
```python
GET  /api/auth/me                    # Dados do usuário logado
POST /api/auth/login                 # Login JWT
POST /api/auth/logout                # Logout
```

#### **👥 Leads (`/api/leads`)**
```python
GET    /api/leads/                   # Listar leads com filtros
POST   /api/leads/                   # Criar novo lead
GET    /api/leads/{id}               # Detalhes do lead
PUT    /api/leads/{id}               # Atualizar lead
POST   /api/leads/upload             # Upload CSV
POST   /api/leads/{id}/manual-qualify # Qualificação manual
```

**Exemplo Request POST /api/leads/**:
```json
{
  "name": "João Silva",
  "email": "joao@email.com", 
  "phone": "+5511999999999",
  "origem": "manual",
  "tags": ["premium", "urgente"]
}
```

#### **💬 Chat (`/api/chat`)**
```python
GET  /api/chat/{session_id}          # Histórico da conversa
POST /api/chat/{session_id}/send     # Enviar mensagem
POST /api/chat/{session_id}/takeover # Takeover humano
POST /api/chat/{session_id}/resume   # Retomar IA
POST /api/chat/{session_id}/close    # Finalizar sessão
```

#### **🔗 Webhooks (`/api/hooks`)**
```python
POST /api/hooks/qualified-lead                   # Processar lead qualificado (Email + CRM)
POST /api/hooks/test-email                       # Testar envio de email
POST /api/hooks/test-crm                         # Testar integração CRM
GET  /api/hooks/health                           # Status dos webhooks
```

#### **🧠 Knowledge Base (`/api/knowledge-base`)**
```python
POST /api/knowledge-base                # Salvar conhecimento
GET  /api/knowledge-base/{tenant_id}    # Buscar por tenant
POST /api/agent-feedback                # Feedback do agente
GET  /api/agent-feedback/{tenant_id}    # Histórico feedback
```

#### **⚙️ Settings (`/api/settings`)**
```python
GET  /api/settings/                     # Configurações do tenant
PUT  /api/settings/                     # Atualizar configurações
GET  /api/settings/ai-prompts           # Prompts da IA
PUT  /api/settings/ai-prompts           # Atualizar prompts
GET  /api/settings/users                # Usuários do tenant
GET  /api/settings/integrations         # Status integrações
```

### **Serviços Principais**

#### **🎯 `qualification_service.py`** - Orquestração Principal
```python
class QualificationService:
    def start_qualification(lead_id, phone) -> Dict
    def process_lead_response(session_id, user_message) -> Dict
    def _notify_consultant(lead_data, score) -> bool
    def _get_knowledge_base_context(tenant_id) -> str
```

#### **📊 `simple_qualification.py`** - Sistema de Scoring
```python
class SimpleQualificationService:
    def calculate_simple_score(answers: Dict) -> int
    def process_user_answer(current_step, user_message, context) -> Dict
    def _extract_answer_letter(user_message) -> str  # A, B, C, D
```

**Lógica de Score (0-100 pontos)**:
- **Patrimônio** (30 pts): A=10, B=20, C=25, D=30
- **Objetivo** (25 pts): A=25, B=20, C=15, D=10  
- **Urgência** (25 pts): A=25, B=20, C=15, D=5
- **Interesse** (20 pts): A=20, B=15, C=10, D=0
- **Qualificado**: ≥ 70 pontos

#### **Estados de Conversa**:
```
inicio → patrimonio → objetivo → urgencia → interesse → qualificacao_completa
```

#### **🤖 `openai_service.py`** - Integração IA
```python
class OpenAIService:
    def chat_completion(messages, model="gpt-4o-mini") -> str
    def extract_qualification_answer(user_message) -> Dict
    def calculate_lead_score(answers) -> int
```

#### **📱 `simple_twilio.py`** - WhatsApp + Simulador
```python
class SimpleTwilioService:
    def send_message(to_number, message) -> Dict
    def _use_simulator_if_enabled() -> bool
    def _simulate_whatsapp_message() -> Dict
```

---

## 6. 🔄 N8N Workflows

### **Workflows Detectados (9 arquivos)**

#### **📥 `intake_complete_workflow.json`** - Captação Principal
- **Trigger**: Webhook `/intake-lead-complete`
- **Nós**: Validação → Supabase Insert → OpenAI → Twilio → Notificação
- **Regra**: Valida dados obrigatórios (name, phone, email)
- **Ação**: Cria lead + inicia qualificação automática

#### **🔔 `qualification_notification_workflow.json`** - Notificações
- **Trigger**: Webhook `/qualified-lead`  
- **Condição**: `score >= 70`
- **Integrações**: Slack + Email + CRM externo
- **Dados**: Lead qualificado + score + respostas

#### **💬 `complete_whatsapp_workflow.json`** - Fluxo WhatsApp
- **Trigger**: Webhook Twilio incoming message
- **Processo**: Message → OpenAI → Response → Twilio Send
- **Context**: Mantém histórico da conversa
- **Scoring**: Calcula score a cada resposta

#### **🔄 `reengagement_workflow.json`** - Reengajamento
- **Trigger**: Schedule (diário)
- **Condição**: Leads sem resposta > 24h
- **Ação**: Mensagem de follow-up personalizada

#### **📋 `intake_workflow_simple.json`** - Captação Simples
- **Uso**: Landing pages básicas
- **Campos**: Nome + telefone apenas
- **Ação**: Cria lead + agenda primeira mensagem

### **URLs de Webhooks (Configurados)**
```
https://eduardopires25.app.n8n.cloud/webhook/intake-lead
https://eduardopires25.app.n8n.cloud/webhook/qualified-lead  
https://eduardopires25.app.n8n.cloud/webhook/reengagement
```

### **Variáveis N8N Utilizadas**
- `SUPABASE_URL` / `SUPABASE_KEY` - Database
- `OPENAI_API_KEY` - IA de qualificação
- `TWILIO_*` - WhatsApp messaging
- `SLACK_WEBHOOK` - Notificações internas
- `SMTP_*` - Email notifications

---

## 7. 📱 Twilio WhatsApp

### **Integração Atual**
- **Serviço**: `simple_twilio.py`
- **Modo**: Simulador ativo (`USE_WHATSAPP_SIMULATOR=true`)
- **Fallback**: Sistema funciona sem Twilio configurado

### **Fluxo WhatsApp**
```mermaid
sequenceDiagram
    participant L as Lead
    participant T as Twilio
    participant B as Backend
    participant AI as OpenAI
    participant S as Supabase

    L->>T: Mensagem WhatsApp
    T->>B: Webhook /twilio/webhook
    B->>S: Buscar sessão ativa
    B->>AI: Processar mensagem
    AI->>B: Resposta + score
    B->>S: Salvar conversa
    B->>T: Enviar resposta
    T->>L: Mensagem IA
```

### **Credenciais Esperadas**
```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxx  
TWILIO_WHATSAPP_NUMBER=+14155238886
```

### **Callbacks/Webhooks**
- **Incoming**: `/api/twilio/webhook` (receber mensagens)
- **Status**: `/api/twilio/status` (entrega/leitura)
- **Media**: Suporte para imagens/documentos

### **Simulador Integrado**
- **Localização**: `whatsapp_simulator.py`
- **Funcionalidade**: Simula envio/recebimento sem API real
- **Logs**: Registra todas as interações simuladas
- **Testes**: Permite testar fluxo completo offline

---

## 8. 🤖 OpenAI Integration

### **Modelos Utilizados**
- **Principal**: `gpt-4o-mini` (rápido + econômico)
- **Alternativo**: `gpt-4o` (configurável)
- **Temperatura**: 0.7 (balanceado)
- **Max Tokens**: 1000 (respostas concisas)

### **Prompts Principais**

#### **Sistema de Qualificação**
```python
QUALIFICATION_PROMPT = """
Você é um especialista em qualificação de leads para investimentos.
Faça EXATAMENTE 4 perguntas obrigatórias:

1. PATRIMÔNIO: Quanto tem disponível para investir?
   A) Até R$ 50 mil  B) R$ 50-200 mil  C) R$ 200-500 mil  D) Mais de R$ 500 mil

2. OBJETIVO: Principal objetivo com investimentos?
   A) Aposentadoria  B) Crescimento  C) Reserva  D) Especulação

3. URGÊNCIA: Quando pretende começar?
   A) Esta semana  B) Este mês  C) Em 3 meses  D) Sem pressa

4. INTERESSE: Gostaria de falar com especialista?
   A) Sim, urgente  B) Sim, quando possível  C) Talvez  D) Não

IMPORTANTE: Mantenha conversação natural mas SEMPRE colete essas 4 respostas.
"""
```

### **Funções IA Implementadas**

#### **`openai_service.py`**
```python
def chat_completion(messages, model="gpt-4o-mini"):
    """Completions padrão com contexto"""
    
def extract_qualification_answer(user_message):
    """Extrai resposta A/B/C/D da mensagem do usuário"""
    
def calculate_lead_score(answers):
    """Calcula score 0-100 baseado nas 4 respostas"""
    
def inject_knowledge_context(prompt, knowledge):
    """Injeta base de conhecimento no prompt"""
```

### **Chaves e Configuração**
- **Variável**: `OPENAI_API_KEY` (obrigatória)
- **Endpoint**: https://api.openai.com/v1/chat/completions
- **Headers**: Authorization Bearer + Content-Type JSON
- **Rate Limiting**: Implementado com retry automático

### **Uso de Tokens (Estimativa)**
- **Por qualificação**: ~500-800 tokens
- **Custo mensal** (100 leads): ~$2-5 USD
- **Otimização**: Prompts concisos + gpt-4o-mini

---

## 9. 🗄️ Supabase Database

### **Tabelas Principais (10 tabelas)**

#### **👥 `tenants`** - Multi-tenancy
```sql
id          UUID PRIMARY KEY
name        VARCHAR(255)           -- Nome da empresa
domain      VARCHAR(255) UNIQUE    -- Domínio personalizado
settings    JSON                   -- Configurações específicas
created_at  TIMESTAMPTZ
updated_at  TIMESTAMPTZ
```

#### **🔐 `users`** - Usuários do sistema  
```sql
id          UUID PRIMARY KEY
tenant_id   UUID REFERENCES tenants(id)
email       VARCHAR(255) UNIQUE
role        VARCHAR(50)            -- admin, closer, operator
name        VARCHAR(255)
created_at  TIMESTAMPTZ
```

#### **📋 `leads`** - Leads capturados
```sql
id                UUID PRIMARY KEY
tenant_id         UUID REFERENCES tenants(id)
name              VARCHAR(255)
email             VARCHAR(255)
phone             VARCHAR(50)
origem            VARCHAR(100)       -- youtube, newsletter, manual
inserido_manual   BOOLEAN DEFAULT false
tags              JSON DEFAULT '[]'
status            VARCHAR(50)        -- novo, em_conversa, qualificado
score             INTEGER DEFAULT 0
created_at        TIMESTAMPTZ
updated_at        TIMESTAMPTZ
```

#### **💬 `sessions`** - Sessões de conversa
```sql
id           UUID PRIMARY KEY  
lead_id      UUID REFERENCES leads(id)
status       VARCHAR(50)       -- ativa, finalizada, pausada
current_step VARCHAR(100)      -- patrimonio, objetivo, etc.
context      JSON              -- Histórico + respostas
created_at   TIMESTAMPTZ
updated_at   TIMESTAMPTZ
```

#### **📨 `messages`** - Mensagens da conversa
```sql
id           UUID PRIMARY KEY
session_id   UUID REFERENCES sessions(id)  
direction    VARCHAR(10)       -- inbound, outbound
content      TEXT
message_type VARCHAR(50)       -- text, image, document
twilio_sid   VARCHAR(255)      -- ID da mensagem Twilio
created_at   TIMESTAMPTZ
```

#### **📊 `qualificacoes`** - Dados de qualificação
```sql
id                     UUID PRIMARY KEY
lead_id                UUID REFERENCES leads(id)
patrimonio_faixa       VARCHAR(100)
objetivo               TEXT  
urgencia               VARCHAR(50)
interesse_especialista BOOLEAN
score_final            INTEGER
observacoes            TEXT
created_at             TIMESTAMPTZ
```

#### **📅 `meetings`** - Agendamentos
```sql
id                 UUID PRIMARY KEY
lead_id            UUID REFERENCES leads(id)
closer_id          UUID REFERENCES users(id)
horario_sugestao_1 TIMESTAMPTZ
horario_sugestao_2 TIMESTAMPTZ  
status             VARCHAR(50)    -- pendente, confirmado, realizado
created_at         TIMESTAMPTZ
```

#### **🔍 `audit_events`** - Log de auditoria
```sql
id            UUID PRIMARY KEY
tenant_id     UUID REFERENCES tenants(id)
user_id       UUID REFERENCES users(id)
action        VARCHAR(100)
resource_type VARCHAR(100)
resource_id   UUID
details       JSON
created_at    TIMESTAMPTZ
```

### **🔒 Row Level Security (RLS)**

**Todas as tabelas têm RLS ativo** com policies baseadas em `tenant_id`:

```sql
-- Exemplo: Policy para tabela leads
CREATE POLICY "tenant_isolation" ON leads
FOR ALL USING (tenant_id = auth.jwt() ->> 'tenant_id'::uuid);

-- Policy para usuários
CREATE POLICY "users_own_tenant" ON users  
FOR ALL USING (tenant_id = auth.jwt() ->> 'tenant_id'::uuid);
```

### **🔄 Views e Funções**
- **`leads_with_stats`**: Leads + estatísticas de conversa
- **`qualification_summary`**: Resumo de qualificações por período
- **`tenant_metrics`**: Métricas consolidadas por tenant

### **❌ Duplicações/Obsolescências Detectadas**
- ✅ **Schema limpo**: Sem tabelas duplicadas
- ✅ **Indexes otimizados**: Queries principais indexadas  
- ✅ **Foreign Keys**: Todas as relações definidas
- ⚠️ **Campos não utilizados**: `domain` em tenants (planejado para white-label)

---

## 10. 🔧 Variáveis de Ambiente

### **Backend (.env.local.backend)**
```env
# Flask Application
FLASK_SECRET_KEY=                    # Chave secreta Flask
FLASK_ENV=development               # Ambiente (development/production)
HOST=0.0.0.0                       # Host do servidor
PORT=5000                          # Porta do backend
DEBUG=true                         # Debug mode

# Database - Supabase PostgreSQL  
SUPABASE_URL=                      # URL do projeto Supabase
SUPABASE_ANON_KEY=                 # Chave pública Supabase
SUPABASE_SERVICE_ROLE_KEY=         # Chave de serviço (admin)

# OpenAI - IA de Qualificação
OPENAI_API_KEY=                    # 🔴 OBRIGATÓRIA - Chave OpenAI
OPENAI_MODEL=gpt-4o-mini           # Modelo da IA
OPENAI_MAX_TOKENS=1000             # Limite de tokens
OPENAI_TEMPERATURE=0.7             # Criatividade da IA

# Twilio WhatsApp  
USE_WHATSAPP_SIMULATOR=true        # Usar simulador (dev)
TWILIO_ACCOUNT_SID=                # SID da conta Twilio
TWILIO_AUTH_TOKEN=                 # Token de autenticação
TWILIO_WHATSAPP_NUMBER=            # Número WhatsApp Business

# N8N Automation
N8N_WEBHOOK_URL_INTAKE=            # Webhook captação leads
N8N_WEBHOOK_URL_QUALIFIED=         # Webhook leads qualificados  
N8N_WEBHOOK_URL_REENGAGEMENT=      # Webhook reengajamento
N8N_API_KEY=                       # Chave API N8N (opcional)

# Sistema gratuito (billing removido)
# Para futuras implementações de cobrança

# Security & CORS
JWT_SECRET_KEY=                    # Chave JWT
CORS_ORIGINS=                      # URLs permitidas CORS

# Logging
LOG_LEVEL=INFO                     # Nível de log
```

### **Frontend (.env.local.frontend)**
```env
# Supabase Client
NEXT_PUBLIC_SUPABASE_URL=          # URL Supabase (público)
NEXT_PUBLIC_SUPABASE_ANON_KEY=     # Chave anônima (público)

# Backend API
NEXT_PUBLIC_API_URL=               # URL da API Flask

# Application
NEXT_PUBLIC_APP_NAME=              # Nome da aplicação
NEXT_PUBLIC_APP_VERSION=           # Versão atual
NEXT_PUBLIC_APP_DESCRIPTION=       # Descrição

# Feature Flags
NEXT_PUBLIC_KNOWLEDGE_BASE_ENABLED=true     # Base conhecimento
NEXT_PUBLIC_AGENT_FEEDBACK_ENABLED=true    # Feedback IA
NEXT_PUBLIC_DASHBOARD_ENABLED=true         # Dashboard
NEXT_PUBLIC_CONVERSATIONS_ENABLED=true     # Chat
NEXT_PUBLIC_LEADS_MANAGEMENT_ENABLED=true  # Gestão leads
NEXT_PUBLIC_CSV_UPLOAD_ENABLED=true       # Upload CSV

# Development
NEXT_PUBLIC_DEBUG=true             # Debug frontend
NEXT_PUBLIC_SHOW_LOGS=true         # Mostrar logs
NEXT_PUBLIC_ENABLE_DEVTOOLS=true   # DevTools React

# UI/UX
NEXT_PUBLIC_THEME=tesla-style      # Tema da interface
NEXT_PUBLIC_LANGUAGE=pt-BR         # Idioma
NEXT_PUBLIC_TIMEZONE=America/Sao_Paulo  # Fuso horário

# Analytics (Produção)
NEXT_PUBLIC_ANALYTICS_ENABLED=false    # Google Analytics
NEXT_PUBLIC_SENTRY_DSN=                # Error tracking
NEXT_PUBLIC_GTM_ID=                    # Google Tag Manager
```

### **Onde cada variável é usada**:
- **OPENAI_API_KEY**: `openai_service.py` (obrigatória)
- **SUPABASE_***: `simple_supabase.py` + frontend
- **TWILIO_***: `simple_twilio.py` (opcional com simulador)
- **N8N_***: `n8n_service.py` + workflows
- **SMTP_***: `email_service.py` para notificações

---

## 11. 🚀 Build & Run

### **Pré-requisitos**
- **Node.js** 16+ (frontend)
- **Python** 3.11+ (backend)
- **Conta Supabase** (database)
- **Chave OpenAI** (obrigatória)

### **Instalação Rápida**

#### **Método 1: Automático (Recomendado)**
```bash
# Windows
.\INICIAR_SISTEMA.bat

# Cross-platform  
python start_system.py
```

#### **Método 2: Manual**
```bash
# 1. Configurar ambiente
copy .env.local.backend backend\.env
copy .env.local.frontend frontend\.env.local

# 2. Backend (Terminal 1)
cd backend
pip install -r requirements_minimal.txt
python app.py

# 3. Frontend (Terminal 2)  
cd frontend
npm install
npm run dev
```

### **URLs de Acesso**
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000  
- **Health Check**: http://localhost:5000/api/health

### **Checklist de Saúde** ✅

#### **Backend Funcionando**
- [ ] ✅ Flask iniciou na porta 5000
- [ ] ✅ Supabase conectado (health check)
- [ ] ✅ OpenAI configurado (test prompt)
- [ ] ✅ Rotas carregadas (8 blueprints)

#### **Frontend Funcionando**  
- [ ] ✅ Next.js na porta 3000
- [ ] ✅ Supabase client conectado
- [ ] ✅ API backend acessível
- [ ] ✅ Dashboard carrega métricas

#### **Integrações Ativas**
- [ ] ✅ Simulador WhatsApp funcionando
- [ ] ✅ N8N webhooks respondendo  
- [ ] ✅ Sistema gratuito ativo
- [ ] ⚠️ Twilio real (opcional)

### **Troubleshooting Comum**

#### **Erro: OpenAI API Key**
```bash
# Editar .env.local.backend
OPENAI_API_KEY=sk-proj-SUA_CHAVE_AQUI
```

#### **Erro: Porta ocupada**
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

#### **Erro: Dependências Python**
```bash
# Usar requirements mínimo
pip install -r requirements_minimal.txt
```

---

## 12. ⚠️ Divergências vs. Esperado

### **✅ Aderente à "Fonte da Verdade"**

#### **Stack Correta**
- ✅ **Frontend**: Next.js 15 + TypeScript + Tailwind
- ✅ **Backend**: Flask 3.0 + Python 3.11+  
- ✅ **Database**: Supabase PostgreSQL + RLS
- ✅ **IA**: OpenAI GPT-4o/4o-mini
- ✅ **Messaging**: Twilio WhatsApp + simulador
- ✅ **Automation**: N8N workflows

#### **Qualificação Implementada**
- ✅ **4 perguntas**: Patrimônio, Objetivo, Urgência, Interesse
- ✅ **Pontuação 0-100**: Sistema transparente
- ✅ **Threshold 70**: Qualificação automática
- ✅ **Estados corretos**: inicio → ... → qualificacao_completa

#### **Arquitetura Padrão**
- ✅ **Pastas organizadas**: frontend/, backend/, database/, n8n/, docs/
- ✅ **Multi-tenancy**: RLS ativo + tenant_id
- ✅ **APIs REST**: Endpoints bem estruturados

### **❌ Divergências Detectadas**

#### **Funcionalidades Fora de Escopo**
- 📄 **Excesso de documentação**: 15+ arquivos MD duplicados
- 🧪 **Múltiplos testes**: Arquivos de teste espalhados
- 📊 **Relatórios automáticos**: Sistema complexo de reports
- 🗂️ **Archive excessivo**: Estrutura de arquivamento pesada

#### **Código Duplicado/Obsoleto**
- ❌ **Dois sistemas de qualificação**: `openai_service.py` + `simple_qualification.py`
- ❌ **Validadores não utilizados**: `marshmallow` removido mas código permanece
- ❌ **Rotas não registradas**: Alguns blueprints não conectados
- ❌ **Arquivos temporários**: `test_*.py` na raiz

#### **Configuração Fragmentada**
- ⚠️ **Múltiplos .env**: Estrutura pode confundir
- ⚠️ **Scripts duplicados**: `start_system.py` + `INICIAR_SISTEMA.bat`
- ⚠️ **Requirements duplo**: `requirements.txt` + `requirements_minimal.txt`

### **🔧 Itens Quebrados/Sem Nexo**

#### **Dependências Problemáticas**
- ❌ **pydantic-core**: Requer Rust para compilar
- ❌ **marshmallow**: Importado mas não usado
- ❌ **asyncio/aiohttp**: Desnecessário para Flask síncrono

#### **Funcionalidades Incompletas**
- ✅ **Sistema gratuito**: Billing removido conforme solicitado
- 🚧 **Autenticação JWT**: Rotas existem mas não integradas
- 🚧 **White-label**: Campo `domain` não utilizado
- 🚧 **Analytics**: Configurado mas não ativo

---

## 13. 📋 Backlog de Correções (Priorizado)

### **🚀 Quick Wins (0-2h)**

#### **Limpeza Imediata**
- [ ] **Remover arquivos temporários** da raiz (`test_*.py`)
- [ ] **Consolidar requirements** (usar apenas `requirements_minimal.txt`)
- [ ] **Limpar imports não utilizados** (`marshmallow`, `cerberus`)
- [ ] **Registrar blueprints faltantes** em `app.py`

#### **Configuração**
- [ ] **Simplificar .env** (manter apenas `.env.local.*`)
- [ ] **Atualizar README** com instruções atuais
- [ ] **Corrigir health checks** (validar todas integrações)

### **⚡ Curto Prazo (≤2 dias)**

#### **Sistema de Qualificação**
- [ ] **Unificar lógica de scoring** (escolher simple vs openai)
- [ ] **Implementar fallback** OpenAI → Simple quando API falha
- [ ] **Otimizar prompts** (reduzir tokens)
- [ ] **Adicionar validação** de respostas A/B/C/D

#### **Interface**  
- [ ] **Sistema de cobrança** (futuro, se necessário)
- [ ] **Página de onboarding** para novos tenants
- [ ] **Melhorar simulador** WhatsApp (mais realista)
- [ ] **Adicionar loading states** em todas as ações

#### **Integrações**
- [ ] **Webhook Twilio** real (não apenas simulador)
- [ ] **Teste N8N workflows** (validar todos os 9)
- [ ] **Implementar retry** em falhas de API
- [ ] **Logs estruturados** para debugging

### **🎯 Médio Prazo (≤1 semana)**

#### **Funcionalidades B2B**
- [ ] **Sistema de onboarding** completo (wizard)
- [ ] **White-label básico** (logo + cores customizáveis)
- [ ] **Relatórios por tenant** (exportação CSV/PDF)
- [ ] **Gestão de usuários** (convites + permissões)

#### **Performance & Escalabilidade**
- [ ] **Cache Redis** para sessões ativas
- [ ] **Queue system** para processamento assíncrono
- [ ] **Rate limiting** por tenant
- [ ] **Monitoramento** (métricas + alertas)

#### **Segurança**
- [ ] **Autenticação JWT** completa
- [ ] **Audit log** detalhado
- [ ] **Validação input** rigorosa
- [ ] **HTTPS obrigatório** em produção

---

## 14. 📊 Diagramas Mermaid

### **Arquitetura Alto Nível**

```mermaid
graph TB
    subgraph "Frontend (Next.js)"
        UI[Dashboard]
        LEADS[Gestão Leads]
        CHAT[Interface Chat]
        SETTINGS[Configurações]
    end
    
    subgraph "Backend (Flask)"
        API[REST APIs]
        QUAL[Qualification Service]
        TWILIO_SRV[Twilio Service]
        EMAIL_SRV[Email Service]
        CRM_SRV[CRM Adapter]
    end
    
    subgraph "Database (Supabase)"
        DB[(PostgreSQL)]
        RLS[Row Level Security]
    end
    
    subgraph "External Services"
        OPENAI[OpenAI GPT-4o]
        TWILIO[Twilio WhatsApp]
        N8N[N8N Workflows]
        CRM[CRM Externo]
    end
    
    UI --> API
    LEADS --> API
    CHAT --> API
    SETTINGS --> API
    
    API --> QUAL
    API --> TWILIO_SRV
    API --> STRIPE_SRV
    
    QUAL --> DB
    QUAL --> OPENAI
    TWILIO_SRV --> TWILIO
    STRIPE_SRV --> STRIPE
    
    N8N --> API
    N8N --> TWILIO
    N8N --> DB
    
    DB --> RLS
```

### **Fluxo de Qualificação Completo**

```mermaid
stateDiagram-v2
    [*] --> LeadCapture: Novo Lead
    
    LeadCapture --> SessionStart: Criar Sessão
    SessionStart --> Inicio: Mensagem Inicial
    
    Inicio --> Patrimonio: Pergunta 1
    Patrimonio --> ValidarP: Resposta A/B/C/D
    ValidarP --> Objetivo: Válida
    ValidarP --> Patrimonio: Inválida (repetir)
    
    Objetivo --> ValidarO: Pergunta 2
    ValidarO --> Urgencia: Válida  
    ValidarO --> Objetivo: Inválida (repetir)
    
    Urgencia --> ValidarU: Pergunta 3
    ValidarU --> Interesse: Válida
    ValidarU --> Urgencia: Inválida (repetir)
    
    Interesse --> ValidarI: Pergunta 4
    ValidarI --> CalcularScore: Válida
    ValidarI --> Interesse: Inválida (repetir)
    
    CalcularScore --> Qualificado: Score ≥ 70
    CalcularScore --> Desqualificado: Score < 70
    
    Qualificado --> NotificarConsultor: N8N Webhook
    Qualificado --> AgendarReuniao: CRM Integration
    
    Desqualificado --> Reengajamento: Workflow Follow-up
    
    NotificarConsultor --> [*]
    AgendarReuniao --> [*]
    Reengajamento --> [*]
```

### **Fluxo de Dados WhatsApp**

```mermaid
sequenceDiagram
    participant L as Lead
    participant T as Twilio
    participant B as Backend
    participant AI as OpenAI
    participant S as Supabase
    participant N as N8N
    
    Note over L,N: Início da Qualificação
    
    L->>T: Mensagem WhatsApp
    T->>B: Webhook /twilio/incoming
    B->>S: Buscar/Criar Sessão
    
    alt Primeira mensagem
        B->>S: Criar nova sessão
        B->>AI: Prompt inicial
        AI->>B: Mensagem de boas-vindas
    else Resposta à pergunta
        B->>AI: Processar resposta
        AI->>B: Próxima pergunta + score
        B->>S: Salvar resposta
    end
    
    B->>T: Enviar resposta IA
    T->>L: Mensagem WhatsApp
    
    alt Score ≥ 70 (Qualificado)
        B->>N: Webhook qualified-lead
        N->>N: Notificar consultor
        N->>S: Agendar follow-up
    else Score < 70 (Desqualificado)  
        B->>N: Webhook reengagement
        N->>N: Agendar reengajamento
    end
```

---

## 15. 🗑️ Arquivos Removidos

Durante a criação deste relatório único, os seguintes arquivos de documentação duplicada foram identificados para remoção:

### **📄 Relatórios e Documentação Duplicada**
- `ANALISE_MELHORIAS_SISTEMA.md` - Conteúdo incorporado ao relatório único
- `DOCUMENTACAO_COMPLETA_SISTEMA.md` - Substituído por este relatório
- `RESUMO_EXECUTIVO_MELHORIAS.md` - Informações consolidadas
- `RESUMO_ORGANIZACAO_FINAL.md` - Histórico arquivado
- `RESUMO_ATUALIZACAO_ENV.md` - Informações no seção 10
- `CONFIGURACAO_ENV_ATUALIZADA.md` - Duplicata das instruções
- `LIMPEZA_PROJETO.md` - Processo documentado neste relatório

### **📊 Relatórios Automáticos Obsoletos**
- `docs/reports/2025-08-25_*` - Relatórios diários antigos (6 arquivos)
- `docs/reports/cleanup_log_*` - Logs de limpeza (2 arquivos)
- `docs/reports/maintenance_report_*` - Relatório de manutenção (1 arquivo)
- `docs/reports/test_results_*` - Resultados de teste antigos (2 arquivos)

### **🗂️ Arquivos de Contexto Redundantes**
- `CONTEXTO_AGENTE_IA.md` - Informações incorporadas
- `GUIA_CUSTOS_APIS.md` - Informações na seção de integrações
- `GUIA_EXECUCAO_FINAL.md` - Substituído pela seção Build & Run

### **📋 Arquivos de Planejamento Antigos**
- `PROJETO_AGENTE_QUALIFICADOR.md` - Escopo inicial arquivado
- `PLANO_EXECUCAO_CONTROLADO.md` - Sistema de sprints finalizado
- `ESTUDO_MICRO_SAAS_B2B.md` - Análise incorporada ao relatório

### **Total de Arquivos Removidos**: 21 arquivos
### **Espaço Liberado**: ~500KB de documentação duplicada
### **Arquivos Preservados**: README.md, LICENSE, docs/RELATORIO_UNICO_AQ.md

---

## 🎯 Conclusão

O **Agente Qualificador** é um **sistema funcional e bem estruturado** com:

### ✅ **Pontos Fortes**
- **Stack moderna** e bem implementada
- **Multi-tenancy** com RLS ativo
- **Sistema de scoring** corrigido e funcional
- **Automação N8N** configurada
- **Interface Tesla-style** limpa e intuitiva
- **Sistema gratuito** (sem cobrança)

### 🔧 **Principais Melhorias Necessárias**
- **Unificar sistema de qualificação** (OpenAI vs Simple)
- **Implementar autenticação JWT** completa
- **Simplificar configuração** de ambiente
- **Completar autenticação JWT**

### 🚀 **Pronto para Produção**
Com as correções do **backlog Quick Wins**, o sistema estará pronto para:
- **Onboarding de clientes B2B**
- **Processamento de leads reais**
- **Notificações via Email + CRM**
- **Escalabilidade horizontal**

---

**Relatório gerado em**: 25/01/2025  
**Próxima auditoria**: 25/02/2025  
**Responsável**: Sistema de Auditoria Automatizada
