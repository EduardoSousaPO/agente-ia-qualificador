# 🤖 AGENTE QUALIFICADOR IA - CONTEXTO PARA AGENTE IA

## 🎯 VISÃO GERAL
Sistema de micro SaaS que automatiza qualificação de leads para consultoria de investimentos via WhatsApp usando IA conversacional. Conduz entrevistas estruturadas, calcula score 0-100 e entrega apenas leads qualificados (≥70 pontos) para consultores.

## 🏗️ ARQUITETURA TÉCNICA

### Stack Principal
- **Frontend**: Next.js 14 + TypeScript + Tailwind CSS
- **Backend**: Flask 3.0 + Python 3.11+
- **Banco**: Supabase PostgreSQL + RLS
- **IA**: OpenAI GPT-4o-mini/GPT-4o
- **Mensageria**: Twilio WhatsApp API
- **Automação**: N8N Workflows

### Estrutura de Pastas
```
agente_qualificador/
├── frontend/src/ (Next.js app)
├── backend/ (Flask API + services)
├── database/prisma/ (Schema)
├── n8n/ (Workflows)
└── docs/ (Documentação)
```

## 🗄️ MODELO DE DADOS CORE

### Tabelas Principais
- **tenants**: Multi-tenancy, isolamento por empresa
- **users**: Controle de acesso (admin/closer/operator)
- **leads**: Prospects (nome, telefone, origem, status, score)
- **sessions**: Estados de conversa IA
- **messages**: Histórico WhatsApp completo
- **qualificacoes**: Dados estruturados da qualificação
- **meetings**: Agendamentos com consultores

## 🤖 SISTEMA DE IA QUALIFICAÇÃO

### Fluxo de 4 Perguntas Obrigatórias
1. **PATRIMÔNIO** (0-30pts): "Quanto tem disponível para investir?"
2. **OBJETIVO** (0-25pts): "Principal objetivo com investimentos?"
3. **URGÊNCIA** (0-25pts): "Quando pretende começar?"
4. **INTERESSE** (0-20pts): "Quer falar com especialista?"

### Sistema de Scoring
- **70-100pts**: QUALIFICADO → Notifica consultor
- **0-69pts**: NÃO QUALIFICADO → Conteúdo educativo

### Estados da Conversa
```python
STATES = {
    'inicio': 'Saudação',
    'patrimonio': 'Pergunta 1',
    'objetivo': 'Pergunta 2', 
    'urgencia': 'Pergunta 3',
    'interesse': 'Pergunta 4',
    'qualificacao_completa': 'Finalizado'
}
```

## 🔄 FLUXO OPERACIONAL

### Lead → Qualificação → Handoff
1. **Entrada**: Web form/CSV/Manual → Cria lead
2. **IA Inicia**: Primeira mensagem WhatsApp automática
3. **Qualificação**: 4 perguntas estruturadas
4. **Scoring**: Cálculo automático 0-100
5. **Handoff**: Se ≥70pts → Slack/Email para consultor

### Jornada do Lead (Exemplo Qualificado)
```
Lead: "R$ 300 mil" → 25pts
Lead: "Aposentadoria" → 25pts  
Lead: "Esta semana" → 25pts
Lead: "Sim, urgente" → 20pts
TOTAL: 95pts ✅ QUALIFICADO
```

## 📱 FUNCIONALIDADES DASHBOARD

### Páginas Principais
- **Dashboard**: Métricas, gráficos, KPIs
- **Leads**: CRUD, upload CSV, filtros
- **Conversas**: Chat interface, takeover manual
- **Configurações**: IA, Twilio, N8N, scoring

### Métricas Key
- Total leads, taxa qualificação, score médio
- Conversas ativas, origem dos leads
- Timeline últimos 30 dias

## 🔗 INTEGRAÇÕES TÉCNICAS

### APIs Externas
- **OpenAI**: Processamento conversacional (~$0.01-0.03/lead)
- **Twilio**: WhatsApp Business API ($0.005/msg)
- **Supabase**: Real-time + Auth + RLS
- **N8N**: 5 workflows (intake, notification, reengagement)

### Configuração Ambiente
```bash
# Backend
SUPABASE_URL, SUPABASE_ANON_KEY
OPENAI_API_KEY, TWILIO_*, N8N_*

# Frontend  
NEXT_PUBLIC_SUPABASE_URL
NEXT_PUBLIC_SUPABASE_ANON_KEY
```

## 🧪 SISTEMA DE TESTES

### Arquivos de Teste
- `TESTE_SISTEMA_COMPLETO.py`: End-to-end completo
- `teste_n8n_notification.py`: Workflows N8N
- Cenários: Lead qualificado (95pts) vs não qualificado (35pts)

## 💰 ECONOMICS

### Custos Operacionais
- **Por Lead**: $0.05-0.08 (IA + WhatsApp + infraestrutura)
- **Fixo Mensal**: ~$65 (Vercel + Supabase + N8N)
- **ROI**: 4.000-166.667% (valor cliente R$ 2k-50k)

## 🚀 STATUS ATUAL

### Pronto para Produção
- ✅ Sistema 100% funcional e testado
- ✅ Frontend completo com todas as funcionalidades
- ✅ Backend com APIs REST completas
- ✅ IA de qualificação implementada
- ✅ Integrações Supabase + Twilio + N8N
- ✅ Testes automatizados end-to-end
- ✅ Documentação técnica completa

### Arquivos de Deploy
- `INICIAR_SISTEMA.bat`: Start completo
- `start_system.py`: Orquestrador Python
- `GUIA_EXECUCAO_FINAL.md`: Deploy production

### Próximos Passos
1. Deploy Vercel (frontend) + Railway/Vercel (backend)
2. Configurar Twilio WhatsApp real (sair do sandbox)
3. Setup N8N Cloud workflows
4. Monitoramento e métricas produção

## 🛡️ SEGURANÇA
- Row Level Security (RLS) por tenant
- JWT + Supabase Auth
- Audit trail completo
- LGPD compliance ready

## 📂 ARQUIVOS IMPORTANTES

### Backend Key Files
- `backend/app.py`: Servidor Flask principal
- `backend/services/qualification_service.py`: Lógica IA qualificação
- `backend/services/simple_supabase.py`: Client Supabase
- `backend/services/simple_twilio.py`: Client WhatsApp
- `backend/services/n8n_service.py`: Integração workflows

### Frontend Key Files
- `frontend/src/app/page.tsx`: Landing page
- `frontend/src/app/dashboard/page.tsx`: Dashboard principal
- `frontend/src/app/leads/page.tsx`: Gestão de leads
- `frontend/src/app/conversations/page.tsx`: Interface chat
- `frontend/src/components/`: Componentes reutilizáveis

### Configuration Files
- `backend/.env.example`: Template variáveis backend
- `frontend/.env.example`: Template variáveis frontend
- `database/prisma/schema.prisma`: Schema banco de dados
- `n8n/*.json`: Workflows N8N exportados

### Documentation
- `DOCUMENTACAO_COMPLETA_SISTEMA.md`: Doc técnica completa (976 linhas)
- `GUIA_EXECUCAO_FINAL.md`: Guia deploy produção
- `EXEMPLOS_CONVERSAS_README.md`: Exemplos de conversas
- `ANALISE_MELHORIAS_SISTEMA.md`: Análise técnica

## 🎯 CONTEXTO PARA AGENTE IA

**MISSÃO**: Sistema completo de qualificação automatizada via WhatsApp, pronto para produção. Stack moderna (Next.js + Flask + Supabase + OpenAI). Foco em ROI alto para consultoria investimentos.

**ARQUITETURA**: Multi-tenant, IA conversacional estruturada, scoring inteligente. Todos os componentes funcionais e integrados.

**ESTADO**: Código funcional, testes passando, documentação completa. Pronto para deploy e uso em produção.

**PRIORIDADES**: 
1. Manter simplicidade e foco no core (qualificação)
2. Usar dados reais (não sintéticos) 
3. Otimizar custos de APIs
4. Garantir segurança e compliance

---

*Contexto gerado para supervisão por Agente IA | Janeiro 2025 | Status: Production Ready*
