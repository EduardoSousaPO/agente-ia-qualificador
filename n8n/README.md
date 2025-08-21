# N8N Workflows - Agente Qualificador

Este diretório contém os workflows do n8n para automação do sistema de qualificação de leads.

## Workflows Disponíveis

### 1. Intake Workflow (`intake_workflow.json`)
**Objetivo**: Processar novos leads e enviar primeira mensagem via WhatsApp

**Trigger**: Webhook HTTP POST em `/intake-lead`

**Fluxo**:
1. Recebe dados do lead via webhook
2. Valida dados obrigatórios (nome, telefone, tenant_id)
3. Cria lead no Flask API
4. Registra evento de auditoria
5. Retorna resposta de sucesso/erro

**Payload esperado**:
```json
{
  "name": "João Silva",
  "phone": "11999999999",
  "email": "joao@email.com",
  "tenant_id": "uuid-tenant",
  "origem": "newsletter",
  "tags": ["vip", "interessado"]
}
```

### 2. Qualification Notification (`qualification_notification_workflow.json`)
**Objetivo**: Notificar quando um lead é qualificado e criar reunião

**Trigger**: Supabase trigger quando lead.status = 'qualificado'

**Fluxo**:
1. Detecta lead qualificado no Supabase
2. Busca detalhes da qualificação
3. Seleciona closer disponível
4. Gera sugestões de horário
5. Cria reunião no sistema
6. Envia notificações (Slack + Email)
7. Registra auditoria

**Notificações**:
- **Slack**: Mensagem rica com detalhes do lead e botões de ação
- **Email**: HTML formatado para o closer responsável

### 3. Reengagement Workflow (`reengagement_workflow.json`)
**Objetivo**: Reativar leads inativos automaticamente

**Trigger**: Cron diário às 9h

**Fluxo**:
1. Busca leads inativos (24h+ sem interação)
2. Determina tipo de reengajamento:
   - **24-72h**: Mensagem gentil de reativação
   - **72h+**: Última tentativa antes de desqualificar
3. Envia mensagem via WhatsApp
4. Se for tentativa final, marca como desqualificado
5. Registra auditoria e gera resumo

## Configuração

### Variáveis de Ambiente Necessárias

```bash
# Flask API
FLASK_API_URL=https://your-flask-api.vercel.app
FLASK_API_TOKEN=your-api-token

# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your-service-role-key

# Frontend
FRONTEND_URL=https://your-frontend.vercel.app

# Notificações
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
SMTP_FROM_EMAIL=noreply@yourdomain.com

# Twilio (usado pelo Flask)
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
```

### Credenciais Necessárias

1. **Flask API Auth** (`flask-api-auth`)
   - Tipo: HTTP Header Auth
   - Header: `Authorization`
   - Value: `Bearer your-api-token`

2. **Supabase API** (`supabase-credentials`)
   - URL: `https://your-project.supabase.co`
   - Service Role Key: `your-service-role-key`

3. **SMTP Credentials** (`smtp-credentials`)
   - Host: seu provedor SMTP
   - Port: 587 (TLS) ou 465 (SSL)
   - Username/Password: suas credenciais

## Instalação

1. **Importar workflows**:
   - Acesse seu n8n
   - Vá em "Workflows" > "Import from File"
   - Selecione cada arquivo `.json`

2. **Configurar credenciais**:
   - Crie as credenciais listadas acima
   - Associe aos nós correspondentes

3. **Configurar variáveis de ambiente**:
   - No n8n, vá em Settings > Environment Variables
   - Adicione todas as variáveis necessárias

4. **Ativar workflows**:
   - Ative cada workflow importado
   - Teste os webhooks e triggers

## Endpoints dos Webhooks

Após importar e ativar:

- **Intake Webhook**: `https://your-n8n.com/webhook/intake-lead`
- **Test URL**: `https://your-n8n.com/webhook-test/intake-lead`

## Monitoramento

### Logs de Auditoria
Todos os workflows registram eventos na tabela `audit_events`:
- `lead_intake_n8n`: Lead processado via intake
- `qualified_lead_notification`: Notificação enviada
- `reengagement_attempt`: Tentativa de reengajamento

### Métricas Importantes
- Taxa de sucesso dos workflows
- Tempo de processamento
- Leads reengajados com sucesso
- Notificações entregues

## Troubleshooting

### Problemas Comuns

1. **Webhook não recebe dados**:
   - Verifique se o workflow está ativo
   - Confirme a URL do webhook
   - Teste com dados simples primeiro

2. **Erro de autenticação Supabase**:
   - Verifique se a service role key está correta
   - Confirme se RLS permite acesso via service role

3. **Notificações não enviadas**:
   - Teste credenciais SMTP
   - Verifique webhook do Slack
   - Confirme variáveis de ambiente

4. **Leads não sendo reengajados**:
   - Verifique query de busca de leads inativos
   - Confirme se o cron está executando
   - Teste manualmente o workflow

### Debug

1. **Executar manualmente**:
   - Use "Execute Workflow" para testar
   - Verifique logs de cada nó

2. **Testar webhooks**:
   - Use Postman ou curl para testar
   - Verifique payload e headers

3. **Monitorar execuções**:
   - Vá em "Executions" para ver histórico
   - Analise erros e tempos de execução

## Extensões Futuras

### Workflows Adicionais Sugeridos

1. **Lead Scoring Update**: Atualizar score baseado em interações
2. **Meeting Reminder**: Lembrar reuniões agendadas
3. **Performance Analytics**: Gerar relatórios automáticos
4. **CRM Sync**: Sincronizar com CRM externo
5. **Backup Automation**: Backup automático de dados

### Melhorias

1. **Retry Logic**: Implementar retry automático em falhas
2. **Rate Limiting**: Controlar frequência de mensagens
3. **A/B Testing**: Testar diferentes mensagens de reengajamento
4. **Personalization**: Mensagens personalizadas por perfil
5. **Multi-channel**: Suporte a email e SMS além do WhatsApp




