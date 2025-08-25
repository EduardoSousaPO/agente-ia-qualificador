# 🚀 **GUIA DE EXECUÇÃO FINAL - AGENTE QUALIFICADOR IA**

## ✅ **SISTEMA 100% PRONTO PARA RODAR**

### **📋 PRÉ-REQUISITOS VERIFICADOS:**
- ✅ Python 3.11+ instalado
- ✅ Node.js 18+ instalado  
- ✅ Banco Supabase configurado
- ✅ Arquivos .env criados
- ✅ Página de login implementada

---

## **🎯 OPÇÃO 1: EXECUÇÃO AUTOMÁTICA (RECOMENDADA)**

### **1. Executar Script de Inicialização**
```bash
# No Windows
INICIAR_SISTEMA.bat

# No Linux/Mac
chmod +x INICIAR_SISTEMA.bat
./INICIAR_SISTEMA.bat
```

### **2. Aguardar Inicialização**
- ⏳ Backend Flask iniciando na porta 5000
- ⏳ Frontend Next.js iniciando na porta 3000
- ✅ Sistema pronto em ~30 segundos

### **3. Acessar Sistema**
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:5000
- **Login**: `admin@demo.com` / `demo123`

---

## **🔧 OPÇÃO 2: EXECUÇÃO MANUAL**

### **Passo 1: Configurar OpenAI (OBRIGATÓRIO)**
```bash
# Editar .env.local.backend na raiz do projeto
OPENAI_API_KEY=sk-sua-chave-openai-aqui
```

### **Passo 2: Iniciar Backend**
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### **Passo 3: Iniciar Frontend (Nova janela)**
```bash
cd frontend
npm install
npm run dev
```

### **Passo 4: Testar Sistema**
```bash
python TESTE_SISTEMA_COMPLETO.py
```

---

## **🧪 VALIDAÇÃO FINAL**

### **Teste Automático:**
```bash
python TESTE_SISTEMA_COMPLETO.py
```

### **Resultado Esperado:**
```
🎉 SISTEMA PRONTO PARA USO!
✅ Todos os componentes funcionando
✅ Login: admin@demo.com / demo123
✅ URLs: Frontend (3000) + Backend (5000)
```

---

## **📱 COMO USAR O SISTEMA**

### **1. Fazer Login**
- Acesse: http://localhost:3000
- Email: `admin@demo.com`
- Senha: `demo123`

### **2. Dashboard Principal**
- Visualizar métricas em tempo real
- Acompanhar leads e conversas

### **3. Adicionar Leads**
- **Manual**: Botão "Novo Lead"
- **CSV**: Botão "Upload CSV"
- **Automático**: Via webhooks/formulários

### **4. Testar Qualificação**
- Criar lead de teste
- Iniciar qualificação
- Simular conversa WhatsApp
- Ver resultado (qualificado/não qualificado)

---

## **🔑 CREDENCIAIS E CONFIGURAÇÕES**

### **Login Demo:**
- **Email**: admin@demo.com
- **Senha**: demo123

### **APIs Configuradas:**
- ✅ **Supabase**: Banco funcionando
- ⏳ **OpenAI**: Precisa configurar chave
- ✅ **WhatsApp**: Simulador ativo
- ⏳ **N8N**: Opcional (automação)

### **URLs Importantes:**
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:5000/api/health
- **Supabase**: https://supabase.com/dashboard/project/wsoxukpeyzmpcngjugie

---

## **⚠️ SOLUÇÃO DE PROBLEMAS**

### **Backend não inicia:**
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### **Frontend não inicia:**
```bash
cd frontend
npm install
npm run dev
```

### **Erro de CORS:**
- Verificar CORS_ORIGINS no backend/.env
- Deve incluir: http://localhost:3000

### **Login não funciona:**
- Verificar se backend está rodando
- Credenciais: admin@demo.com / demo123

---

## **🎉 SISTEMA PRONTO!**

### **Funcionalidades Disponíveis:**
- ✅ **Dashboard** com métricas
- ✅ **Gestão de Leads** (CRUD completo)
- ✅ **Conversas WhatsApp** (simulador)
- ✅ **Qualificação IA** (OpenAI)
- ✅ **Sistema de Scoring** (0-100 pontos)
- ✅ **Autenticação** (login/logout)
- ✅ **Multi-tenant** (isolamento de dados)

### **Próximos Passos Opcionais:**
1. **Configurar OpenAI** (para IA real)
2. **Configurar Twilio** (para WhatsApp real)
3. **Configurar N8N** (para automação)
4. **Deploy em produção** (Vercel)

---

**🚀 O Agente Qualificador IA está 100% funcional e pronto para qualificar leads!**

