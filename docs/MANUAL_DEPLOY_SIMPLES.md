# MANUAL DE DEPLOY - AGENTE QUALIFICADOR IA

## PRE-REQUISITOS

### Servidor de Producao:
- Windows 10+ ou Linux
- Docker Desktop instalado
- 4GB RAM minimo
- 20GB espaco em disco

### Contas Necessarias:
- Supabase (banco de dados)
- OpenAI (API de IA)
- Twilio (WhatsApp Business API)
- Gmail (SMTP para emails - opcional)

## CONFIGURACAO

### 1. Preparar Ambiente:
1. Instalar Docker Desktop
2. Clonar o repositorio
3. Configurar variaveis de ambiente

### 2. Configurar Variaveis:
1. Copiar `backend/.env.production` para `backend/.env`
2. Editar com suas chaves reais:
   - SUPABASE_URL e chaves
   - OPENAI_API_KEY
   - TWILIO_ACCOUNT_SID e AUTH_TOKEN
   - Outras configuracoes

### 3. Deploy:
```
cd deploy
deploy.bat
```

## MONITORAMENTO

### Health Checks:
- Backend: http://localhost:5000/api/health
- Frontend: http://localhost:3000

### Logs:
```
docker-compose logs -f
```

### Monitoramento:
```
monitor.bat
```

## TROUBLESHOOTING

### Problemas Comuns:

1. **Container nao inicia**:
   - Verificar logs: docker-compose logs [service]
   - Verificar variaveis de ambiente
   - Reiniciar Docker Desktop

2. **Banco nao conecta**:
   - Verificar SUPABASE_URL e chaves
   - Testar conectividade

3. **WhatsApp nao funciona**:
   - Verificar webhook configurado no Twilio
   - Testar endpoint

## SUPORTE

- Email: suporte@agentequalificador.com
- Documentacao: docs/
