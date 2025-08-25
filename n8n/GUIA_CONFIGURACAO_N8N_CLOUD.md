# 🚀 GUIA COMPLETO - CONFIGURAÇÃO N8N CLOUD

## 📋 **PASSO A PASSO PARA CONFIGURAR N8N CLOUD**

### **1. CRIAR CONTA N8N CLOUD**
1. Acesse: https://n8n.cloud/
2. Clique em "Start for free"
3. Crie sua conta
4. Confirme o email

### **2. IMPORTAR WORKFLOW**
1. No dashboard N8N Cloud, clique em "New Workflow"
2. Clique nos 3 pontos (⋮) → "Import from file"
3. Selecione o arquivo: `n8n/workflow_notificacao_consultor_real.json`
4. Clique em "Import"

### **3. CONFIGURAR CREDENCIAIS**

#### **3.1 SLACK (Opcional)**
1. No workflow, clique no nó "Notificar Slack"
2. Clique em "Create New Credential"
3. Siga o processo de OAuth com Slack
4. Selecione o canal onde quer receber notificações
5. Teste a conexão

#### **3.2 EMAIL SMTP**
1. No workflow, clique no nó "Enviar Email"
2. Clique em "Create New Credential"
3. Configure com seus dados SMTP:
   ```
   Host: smtp.gmail.com (para Gmail)
   Port: 587
   Security: STARTTLS
   Username: seu-email@gmail.com
   Password: sua-senha-de-app
   ```

### **4. ATIVAR WEBHOOK**
1. Clique no nó "Webhook - Lead Qualificado"
2. Copie a URL do webhook (será algo como):
   ```
   https://[seu-n8n].app.n8n.cloud/webhook/qualified-lead
   ```
3. **IMPORTANTE**: Ative o workflow (toggle no canto superior direito)

### **5. CONFIGURAR NO BACKEND**
Atualize o arquivo `backend/.env`:
```env
# N8N Configuration
N8N_WEBHOOK_URL_QUALIFIED=https://[seu-n8n].app.n8n.cloud/webhook/qualified-lead
N8N_API_KEY=opcional-se-necessario
```

### **6. TESTAR WORKFLOW**
1. No N8N, clique em "Test Workflow"
2. Use este JSON de teste:
```json
{
  "event": "lead_qualified",
  "lead": {
    "id": "test-123",
    "name": "João Silva",
    "phone": "+5511999999999",
    "email": "joao@teste.com",
    "origem": "teste"
  },
  "qualification": {
    "patrimonio": "C",
    "objetivo": "A", 
    "urgencia": "A",
    "interesse": "A",
    "score": 95
  }
}
```

## 🔧 **CONFIGURAÇÕES AVANÇADAS**

### **PERSONALIZAR NOTIFICAÇÕES**

#### **Slack**
- Edite o texto no nó "Notificar Slack"
- Adicione emojis e formatação
- Configure diferentes canais por score

#### **Email**
- Personalize o HTML no nó "Enviar Email"
- Adicione logo da empresa
- Configure diferentes destinatários

### **ADICIONAR MAIS INTEGRAÇÕES**
- **WhatsApp Business**: Para notificar via WhatsApp
- **CRM**: Integrar com HubSpot, Pipedrive, etc.
- **Google Sheets**: Salvar leads em planilha
- **Zapier**: Conectar com outras ferramentas

## 📊 **MONITORAMENTO**

### **Logs e Execuções**
1. Vá em "Executions" no N8N
2. Monitore sucessos/falhas
3. Debug problemas

### **Alertas**
- Configure alertas para falhas
- Monitor performance
- Acompanhe volume de leads

## 🚨 **TROUBLESHOOTING**

### **Webhook não funciona**
- Verifique se workflow está ATIVO
- Confirme URL no backend
- Teste manualmente no N8N

### **Slack não envia**
- Reautorize credenciais
- Verifique permissões do bot
- Confirme canal existe

### **Email não envia**
- Teste credenciais SMTP
- Verifique spam/firewall
- Use senha de app (Gmail)

## ✅ **CHECKLIST FINAL**
- [ ] Workflow importado
- [ ] Credenciais configuradas
- [ ] Webhook ativo
- [ ] URL atualizada no backend
- [ ] Teste realizado com sucesso
- [ ] Notificações funcionando

---

**🎯 Após configurar, o sistema enviará automaticamente:**
- Notificação Slack para leads qualificados
- Email detalhado para consultores
- Resposta JSON para o backend

**💡 Dica**: Mantenha o workflow sempre ativo para receber notificações em tempo real!




