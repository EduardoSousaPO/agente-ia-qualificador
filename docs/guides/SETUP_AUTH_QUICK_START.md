# 🚀 Setup Rápido - Sistema de Autenticação

## ⚡ **INÍCIO RÁPIDO (5 minutos)**

### **1. Configurar Supabase** (2 min)
```bash
# 1. Acesse https://supabase.com e crie um projeto
# 2. Vá em Settings > API e copie:
#    - Project URL
#    - anon public key

# 3. Configure variáveis de ambiente
cp .env.local.frontend.example frontend/.env.local
# Edite frontend/.env.local com suas credenciais
```

### **2. Executar Migrations** (1 min)
```sql
-- Copie e execute no SQL Editor do Supabase:
-- 📁 database/supabase/migrations/001_multi_tenant_foundation.sql
-- 📁 database/supabase/migrations/002_seed_ldc_capital.sql
```

### **3. Instalar Dependências** (1 min)
```bash
# Frontend
cd frontend
npm install

# Backend (se não instalado)
cd ../backend
pip install -r requirements.txt
```

### **4. Iniciar Sistema** (1 min)
```bash
# Terminal 1: Backend
cd backend
python app.py

# Terminal 2: Frontend  
cd frontend
npm run dev
```

## ✅ **TESTAR FUNCIONAMENTO**

### **Teste 1: Página de Signup**
1. 🌐 Acesse: http://localhost:3000/signup
2. ✅ **Esperado**: Formulário de cadastro carregado
3. 📧 Digite email: `admin@ldc-capital.com`
4. ✅ **Esperado**: Detecção automática do convite LDC Capital

### **Teste 2: Página de Login**
1. 🌐 Acesse: http://localhost:3000/login
2. ✅ **Esperado**: Formulário de login carregado
3. 🔗 Link para signup visível

### **Teste 3: Criar Conta**
1. 📝 Preencha formulário signup completo
2. 🚀 Submeta formulário
3. ✅ **Esperado**: Email de confirmação enviado
4. 📧 Confirme email no Supabase Auth

### **Teste 4: Login Funcional**
1. 🔑 Faça login com conta criada
2. ✅ **Esperado**: Redirecionamento automático
3. 🏢 Se tiver convite: `/app/ldc-capital/dashboard`
4. 📊 Se não tiver: `/dashboard`

---

## 🔧 **TROUBLESHOOTING**

### **❌ Erro: "NEXT_PUBLIC_SUPABASE_URL não está definida"**
```bash
# Solução:
1. Verifique se frontend/.env.local existe
2. Verifique se as variáveis estão corretas
3. Reinicie o frontend (Ctrl+C e npm run dev)
```

### **❌ Erro 500 no backend**
```bash
# Solução:
1. Verifique se backend está rodando na porta 5000
2. Verifique logs do backend para erros específicos
3. Confirme se migrations foram executadas
```

### **❌ Signup não funciona**
```bash
# Solução:
1. Verifique se email confirmation está habilitado no Supabase
2. Vá em Authentication > Settings > Email Templates
3. Confirme se SMTP está configurado
```

### **❌ Convites não são detectados**
```bash
# Solução:
1. Confirme se migration 002_seed_ldc_capital.sql foi executada
2. Verifique se tabela 'invites' existe no Supabase
3. Use email exato: admin@ldc-capital.com
```

---

## 📋 **CHECKLIST DE VALIDAÇÃO**

### **Configuração**
- [ ] ✅ Projeto Supabase criado
- [ ] ✅ Variáveis de ambiente configuradas  
- [ ] ✅ Migrations executadas
- [ ] ✅ Dependências instaladas
- [ ] ✅ Backend rodando (porta 5000)
- [ ] ✅ Frontend rodando (porta 3000)

### **Funcionalidades**
- [ ] ✅ Página /signup carrega
- [ ] ✅ Página /login carrega
- [ ] ✅ Validação de formulários funciona
- [ ] ✅ Detecção de convites funciona
- [ ] ✅ Signup cria conta no Supabase
- [ ] ✅ Login funciona com Supabase Auth
- [ ] ✅ Redirecionamento por tenant funciona

---

## 🎯 **PRÓXIMOS PASSOS**

### **Desenvolvimento**
1. ✅ **Testar fluxo completo** signup → login → dashboard
2. ✅ **Criar convites** via interface admin
3. ✅ **Testar multi-tenant** com diferentes usuários
4. ✅ **Validar RLS policies** no Supabase

### **Produção**
1. 🚀 **Deploy Supabase** em produção
2. 🚀 **Configurar domínio** personalizado
3. 🚀 **Deploy frontend/backend**
4. 🚀 **Configurar email** SMTP real

---

## 📞 **SUPORTE**

### **Logs Úteis**
```bash
# Backend logs
python backend/app.py  # Veja erros no terminal

# Frontend logs  
npm run dev  # Veja erros no terminal
# Browser DevTools > Console

# Supabase logs
# Dashboard > Logs > Auth/Database
```

### **Recursos**
- 📚 **Documentação**: `docs/AUTH-implementation-report.md`
- 🧪 **Testes**: `python tests/test_auth_integration.py`
- 🔧 **Migrations**: `database/supabase/migrations/`

---

**Status**: ✅ **PRONTO PARA USO**  
**Versão**: 2.0 Multi-Tenant Auth  
**Última atualização**: 26/08/2025




