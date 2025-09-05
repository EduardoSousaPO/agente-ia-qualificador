# 🤖 **Agente Qualificador IA**

> **Sistema de qualificação de leads via WhatsApp com IA humanizada**  
> *MVP refatorado e pronto para produção*

[![Status](https://img.shields.io/badge/Status-MVP%20Ready-success)]()
[![Score](https://img.shields.io/badge/Score-76%25-brightgreen)]()
[![Python](https://img.shields.io/badge/Python-3.11+-blue)]()
[![Next.js](https://img.shields.io/badge/Next.js-14+-black)]()

---

## 🎯 **Visão Geral**

O **Agente Qualificador IA** automatiza a qualificação de leads para consultorias através do WhatsApp, utilizando a **Ana** - uma IA humanizada que conduz conversas naturais e identifica prospects qualificados.

### **🎭 Conheça a Ana**
- **Consultora Sênior** especializada em investimentos
- **Conversação 100% natural** - clientes não percebem que é IA
- **Qualificação invisível** durante a conversa
- **Encaminhamento automático** de leads qualificados (score ≥70)

---

## 🚀 **Início Rápido**

### **1. Instalação:**
```bash
# Backend
cd backend
pip install -r requirements.txt
cp .env.production .env  # Configure suas chaves

# Frontend
cd frontend
npm install
```

### **2. Configuração:**
Edite `.env` com suas chaves:
```env
SUPABASE_URL=sua-url-supabase
OPENAI_API_KEY=sua-chave-openai
TWILIO_ACCOUNT_SID=seu-account-sid
```

### **3. Executar:**
```bash
# Backend
cd backend
python main.py

# Frontend (novo terminal)
cd frontend
npm run dev
```

### **4. Testar:**
```bash
# Testes automatizados
cd tests
python TESTAR_SISTEMA.py

# WhatsApp: +1 415 523 8886 → "join to-southern" → "Oi, tenho interesse"
```

---

## 📁 **Estrutura Organizada**

```
agente_qualificador/
├── 📱 frontend/           # Next.js Dashboard
├── 🔧 backend/            # Flask API + IA
├── 🗄️ database/          # Supabase Schema  
├── 🧪 tests/             # Suite de Testes
├── 📜 scripts/           # Utilitários
├── 🚀 deploy/            # Deploy Configs
├── 📚 docs/              # Documentação Completa
│   ├── guides/           # Guias de uso
│   ├── technical/        # Docs técnicas
│   └── reports/          # Relatórios
└── 📋 README.md          # Este arquivo
```

---

## ✨ **Funcionalidades**

### **🤖 IA Humanizada:**
- Agente **Ana** com personalidade própria
- Conversação natural e empática
- Base de conhecimento contextual
- Qualificação transparente ao cliente

### **📱 WhatsApp Integration:**
- Webhook direto via **Twilio**
- Processamento em tempo real
- Sandbox para testes

### **🗄️ Multi-Tenant:**
- **Row Level Security (RLS)**
- Isolamento completo por empresa
- Configurações personalizáveis

### **📊 Dashboard:**
- Interface **Next.js** moderna
- Gestão de leads e conversas
- Métricas de conversão

---

## 🧪 **Qualidade e Testes**

### **📊 Score MVP: 76%** ✅
- **Backend**: 62% (estrutura sólida)
- **Frontend**: 86% (interface funcional)
- **WhatsApp**: 100% (integração completa)
- **Database**: 100% (todas as tabelas)

### **🧪 Suite de Testes:**
```bash
# Executar todos os testes
python tests/run_all_tests.py

# Teste de produção
python tests/test_production_ready.py
```

---

## 🚀 **Deploy em Produção**

### **🐳 Docker (Recomendado):**
```bash
cd deploy
./deploy.bat     # Windows
./deploy.sh      # Linux
```

### **📊 Monitoramento:**
```bash
./monitor.bat    # Windows
./monitor.sh     # Linux
```

### **⚙️ Configuração:**
- Usar `.env.production` como base
- Configurar domínio e SSL
- Webhook Twilio para seu domínio

---

## 📚 **Documentação**

### **📖 Guias:**
- [Manual de Deploy](docs/MANUAL_DEPLOY_SIMPLES.md)
- [Guia WhatsApp](docs/guides/GUIA_AGENTE_HUMANIZADO_WHATSAPP.md)
- [Configuração Twilio](docs/guides/GUIA_TESTE_TWILIO_SANDBOX_PASSO_A_PASSO.md)

### **🔧 Técnica:**
- [Arquitetura](docs/technical/INTERFACES_POR_NIVEL.md)
- [Prompts IA](docs/technical/prompts_perfeitos_qualificador.md)

### **📊 Relatórios:**
- [Refatoração Completa](RELATORIO_REFATORACAO_COMPLETA.md)
- [Cronograma MVP](CRONOGRAMA_FINAL_MVP.md)

---

## 🎯 **Como Funciona**

### **1. Cliente inicia conversa:**
```
Cliente: "Oi, tenho interesse em investimentos"
```

### **2. Ana responde naturalmente:**
```
Ana: "Oi! Que bom! Sou Ana, consultora da InvestCorp.
     Para te ajudar melhor, me conta: você já investe?"
```

### **3. Qualificação automática:**
- Conversa flui naturalmente
- Sistema calcula score em background
- Score ≥70: Lead qualificado
- Consultor notificado automaticamente

---

## 🔧 **Desenvolvimento**

### **Requisitos:**
- Python 3.11+
- Node.js 18+
- Docker Desktop
- Contas: Supabase, OpenAI, Twilio

### **Contribuindo:**
1. Fork o repositório
2. Crie branch: `git checkout -b feature/nova-funcionalidade`
3. Commit: `git commit -m 'Adiciona nova funcionalidade'`
4. Push: `git push origin feature/nova-funcionalidade`
5. Abra Pull Request

---

## 📞 **Suporte**

### **🐛 Troubleshooting:**
```bash
# Backend não inicia
python -c "import os; print(os.getenv('SUPABASE_URL'))"

# WhatsApp não responde  
curl -X POST http://localhost:5000/api/whatsapp/webhook \
  -d "Body=teste&From=whatsapp:+5511999999999"
```

### **📧 Contato:**
- Email: suporte@agentequalificador.com
- WhatsApp: +55 11 9999-9999
- Issues: [GitHub Issues](https://github.com/seu-usuario/agente-qualificador-ia/issues)

---

## 🏆 **Status do Projeto**

### **✅ Concluído:**
- 🤖 Agente IA humanizado funcionando
- 📱 Integração WhatsApp completa
- 🗄️ Banco multi-tenant configurado
- 🚀 Deploy automatizado
- 📚 Documentação completa

### **🎯 Pronto para:**
- Qualificar leads reais via WhatsApp
- Operação 24/7 automatizada
- Escalabilidade multi-tenant
- Deploy em produção

---

<div align="center">

**🤖 Sistema refatorado e pronto para produção**

**🎊 MVP funcional para qualificar leads reais via WhatsApp**

</div>
