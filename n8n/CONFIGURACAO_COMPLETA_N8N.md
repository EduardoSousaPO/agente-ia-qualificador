# 🔧 **CONFIGURAÇÃO COMPLETA N8N - AGENTE QUALIFICADOR**

## 📋 **WORKFLOWS NECESSÁRIOS**

### **1. 📥 Lead Intake Completo** (`intake_complete_workflow.json`)
**Função**: Receber leads → Criar no Supabase → Enviar primeira mensagem WhatsApp

**Fluxo**:
```
Webhook → Validar Dados → Criar Lead → Criar Sessão → IA Gera Mensagem → Twilio Envia → Salvar no Supabase
```

### **2. 🤖 WhatsApp AI Agent** (`complete_whatsapp_workflow.json`)
**Função**: Receber mensagens WhatsApp → Processar com IA → Responder → Qualificar → Notificar

**Fluxo**:
```
Webhook Twilio → Filtrar → Buscar Lead → IA Processa → Verifica Qualificação → Envia Resposta → Notifica Closer
```

---

## 🔑 **CREDENCIAIS NECESSÁRIAS NO N8N**

### **1. OpenAI API**
- **Nome**: `openai-credentials`
- **Tipo**: OpenAI
- **API Key**: `sk-proj-sua-chave-openai`

### **2. Twilio API**
- **Nome**: `twilio-credentials`
- **Tipo**: HTTP Basic Auth
- **Username**: `Seu Account SID`
- **Password**: `Seu Auth Token`

### **3. Supabase (via Headers)**
- **Integração direta via HTTP Request**
- **Headers necessários**:
  - `apikey`: Sua Supabase Service Role Key
  - `Authorization`: `Bearer {Service Role Key}`

---

## 📱 **CONFIGURAÇÃO TWILIO WEBHOOKS**

### **No Twilio Console:**

1. **Acesse**: Console Twilio → Phone Numbers → WhatsApp Sandbox
2. **Configure Webhook URL**:
   ```
   https://seu-workspace.app.n8n.cloud/webhook/whatsapp-webhook
   ```
3. **Método**: `POST`
4. **Events**: `Incoming Messages`

### **Variáveis de Ambiente N8N:**
```env
TWILIO_ACCOUNT_SID=ACsua-account-sid
TWILIO_AUTH_TOKEN=seu-auth-token
TWILIO_WHATSAPP_NUMBER=+14155238886
```

---

## 🗄️ **CONFIGURAÇÃO SUPABASE**

### **URLs dos Endpoints:**
- **Leads**: `https://wsoxukpeyzmpcngjugie.supabase.co/rest/v1/leads`
- **Sessions**: `https://wsoxukpeyzmpcngjugie.supabase.co/rest/v1/sessions`
- **Messages**: `https://wsoxukpeyzmpcngjugie.supabase.co/rest/v1/messages`

### **Headers Padrão:**
```json
{
  "apikey": "sua-service-role-key",
  "Authorization": "Bearer sua-service-role-key",
  "Content-Type": "application/json"
}
```

---

## 🚀 **PASSO A PASSO - IMPORTAÇÃO**

### **PASSO 1: Importar Workflows**

1. **N8N Console** → **Workflows** → **Import from File**
2. **Importar na ordem**:
   - `intake_complete_workflow.json` (Intake)
   - `complete_whatsapp_workflow.json` (Conversas)

### **PASSO 2: Configurar Credenciais**

#### **OpenAI:**
```
Settings → Credentials → Create New
Type: OpenAI
Name: openai-credentials
API Key: sk-proj-sua-chave-aqui
```

#### **Twilio:**
```
Settings → Credentials → Create New
Type: HTTP Basic Auth
Name: twilio-credentials
Username: Seu_Account_SID
Password: Seu_Auth_Token
```

### **PASSO 3: Configurar Variáveis de Ambiente**

```
Settings → Variables
TWILIO_ACCOUNT_SID = ACsua-account-sid
TWILIO_AUTH_TOKEN = seu-auth-token
TWILIO_WHATSAPP_NUMBER = +14155238886
```

### **PASSO 4: Ativar Workflows**

1. **Intake Workflow** → **Active: ON**
2. **WhatsApp Workflow** → **Active: ON**

### **PASSO 5: Obter URLs dos Webhooks**

#### **Para Intake (Frontend/Formulários):**
```
https://seu-workspace.app.n8n.cloud/webhook/intake-lead-complete
```

#### **Para Twilio (Configurar no Twilio Console):**
```
https://seu-workspace.app.n8n.cloud/webhook/whatsapp-webhook
```

---

## 🧪 **TESTANDO AS INTEGRAÇÕES**

### **Teste 1: Lead Intake**
```bash
curl -X POST https://seu-workspace.app.n8n.cloud/webhook/intake-lead-complete \
-H "Content-Type: application/json" \
-d '{
  "name": "João Teste",
  "phone": "+5511999888777",
  "email": "joao@teste.com",
  "origem": "teste_n8n"
}'
```

**Resultado Esperado**:
- ✅ Lead criado no Supabase
- ✅ Sessão de chat criada
- ✅ Mensagem WhatsApp enviada via Twilio
- ✅ Mensagem salva no histórico

### **Teste 2: Resposta WhatsApp**
**Envie mensagem WhatsApp** para o número do Twilio Sandbox

**Resultado Esperado**:
- ✅ Webhook recebido no N8N
- ✅ IA processa mensagem
- ✅ Resposta enviada via Twilio
- ✅ Conversa salva no Supabase
- ✅ Se qualificado → Notificação Slack

---

## 🔄 **FLUXO COMPLETO INTEGRADO**

```mermaid
graph TD
    A[Lead Form/CSV] --> B[N8N Intake Webhook]
    B --> C[Criar Lead Supabase]
    C --> D[Criar Sessão Chat]
    D --> E[IA Gera Boas-vindas]
    E --> F[Twilio Envia WhatsApp]
    F --> G[Salvar Mensagem]
    
    H[WhatsApp Response] --> I[N8N WhatsApp Webhook]
    I --> J[Buscar Lead Supabase]
    J --> K[IA Processa Resposta]
    K --> L[Twilio Envia Resposta]
    L --> M{Qualificado?}
    M -->|Sim| N[Slack Notification]
    M -->|Não| O[Continuar Conversa]
```

---

## 📊 **MONITORAMENTO**

### **N8N Executions**
- **Intake Workflow**: Monitore execuções bem-sucedidas
- **WhatsApp Workflow**: Verifique processamento de mensagens

### **Logs Importantes**
- **Twilio Delivery Status**: Confirmar envio de mensagens
- **OpenAI Token Usage**: Monitorar uso da API
- **Supabase Operations**: Verificar criação de registros

---

## ⚠️ **TROUBLESHOOTING**

### **Erro: Webhook não recebe dados**
- ✅ Verificar URL do webhook no Twilio
- ✅ Confirmar workflow ativo no N8N
- ✅ Testar com curl manual

### **Erro: OpenAI não responde**
- ✅ Verificar API Key válida
- ✅ Confirmar créditos na conta OpenAI
- ✅ Testar modelo `gpt-4o-mini`

### **Erro: Twilio não envia**
- ✅ Verificar Account SID e Auth Token
- ✅ Confirmar WhatsApp Sandbox ativo
- ✅ Testar número de destino válido

### **Erro: Supabase não salva**
- ✅ Verificar Service Role Key
- ✅ Confirmar RLS policies
- ✅ Testar endpoints manualmente

---

## 🎯 **RESULTADO FINAL**

Com essas configurações, você terá:

✅ **Lead Intake** automático com primeira mensagem  
✅ **Conversas IA** inteligentes e contextuais  
✅ **Qualificação** automática baseada em critérios  
✅ **Notificações** para closers via Slack  
✅ **Persistência** completa no Supabase  
✅ **WhatsApp** real via Twilio  

**🚀 SISTEMA COMPLETO E INTEGRADO!**


