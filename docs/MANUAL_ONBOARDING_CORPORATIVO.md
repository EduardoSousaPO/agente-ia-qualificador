# 📋 **MANUAL DE ONBOARDING - SISTEMA CORPORATIVO**
## **Agente Qualificador IA - Registro e Gestão de Empresas**

---

## 🏢 **1. COMO FUNCIONA O SISTEMA CORPORATIVO**

O sistema funciona com **isolamento total por empresa**. Cada empresa tem:
- ✅ **Código único** (ex: `DEMO2024`)
- ✅ **Dados isolados** (leads, conversas, configurações)
- ✅ **Membros próprios** (admins e usuários)
- ✅ **Aprovação obrigatória** para novos membros

---

## 🔑 **2. CÓDIGOS DAS EMPRESAS DISPONÍVEIS**

### **📊 Empresas Cadastradas:**

| Empresa | Código | Status |
|---------|--------|--------|
| **Escritório de Investimentos Demo** | `DEMO2024` | ✅ Ativo |
| **LDC Capital Investimentos** | `LDC2024` | ✅ Ativo |
| **Consultoria Financeira ABC** | `ABC2024` | ✅ Ativo |
| **Gestora XYZ Wealth** | `XYZ2024` | ✅ Ativo |

### **🔧 Como Adicionar Nova Empresa:**

#### **🎯 MÉTODO 1: Via Interface Admin (RECOMENDADO)**
1. **Faça login** como administrador
2. **Acesse**: Menu lateral → **"Gerenciar Empresas"**
3. **Clique**: Botão **"Nova Empresa"**
4. **Preencha o formulário**:
   - Nome da empresa (ex: "Consultoria XYZ Ltda")
   - Código da empresa (ex: "XYZ2024") - será gerado automaticamente
   - Tipo de empresa
   - Máximo de membros
   - Descrição (opcional)
5. **Clique**: **"Criar Empresa"**
6. **Pronto!** A empresa estará disponível para registro

#### **🔧 MÉTODO 2: Via SQL (Avançado)**
```sql
-- Executar no Supabase SQL Editor:
INSERT INTO public.tenants (name, slug, code, settings) VALUES
('Sua Empresa Ltda', 'sua-empresa', 'SUA2024', '{"company_type": "investment_advisory"}'::jsonb);
```

---

## 👥 **3. FLUXO COMPLETO DE REGISTRO**

### **📝 PASSO 1: Registro do Usuário**

1. **Acesse**: `http://localhost:3000/signup`
2. **Preencha os dados**:
   - Nome completo
   - Email
   - **Código da empresa** (ex: `DEMO2024`)
   - **Nome da empresa** (preenchido automaticamente)
   - Senha (mínimo 8 chars, 1 maiúscula, 1 minúscula, 1 número)
   - Confirmar senha
   - ✅ Aceitar termos
3. **Clique**: "Criar conta"

### **✅ O que acontece:**
- ✅ Conta criada no Supabase Auth
- ✅ Solicitação enviada para aprovação
- ✅ Usuário redirecionado para login
- ✅ Mensagem: *"Sua solicitação está pendente de aprovação"*

---

## 👨‍💼 **4. ACESSO DO ADMINISTRADOR**

### **🔐 Como fazer login como Admin:**

1. **Acesse**: `http://localhost:3000/login`
2. **Use as credenciais demo**:
   - **Email**: `eduspires123@gmail.com`
   - **Senha**: `[senha configurada no sistema]`
3. **Clique**: "Entrar"

### **🎯 Funcionalidades do Admin:**
- ✅ **Dashboard completo** com métricas
- ✅ **Gerenciar leads** da empresa
- ✅ **Aprovar/Rejeitar** novos membros
- ✅ **Criar e gerenciar empresas** (super-admin)
- ✅ **Configurar base de conhecimento**
- ✅ **Validar agente de IA**
- ✅ **Acesso total** aos dados da empresa

---

## ✅ **5. COMO APROVAR NOVOS MEMBROS**

### **📋 Passo a Passo para Admins:**

1. **Faça login** como administrador
2. **Acesse**: Menu lateral → **"Solicitações"**
3. **Visualize o dashboard**:
   - 📊 **Estatísticas**: Pendentes, Aprovadas, Rejeitadas, Total
   - 🔍 **Filtros**: Todas, Pendentes, Aprovadas, Rejeitadas
4. **Para cada solicitação pendente**:
   - 👤 **Veja os dados**: Nome, email, empresa
   - ⏰ **Data da solicitação**
   - 🎯 **Ações disponíveis**:

### **✅ APROVAR SOLICITAÇÃO:**
- **Clique**: Botão verde **"Aprovar"**
- **Resultado**: 
  - ✅ Usuário vira membro da empresa
  - ✅ Pode fazer login normalmente
  - ✅ Acesso aos dados da empresa
  - ✅ Status: "Aprovado"

### **❌ REJEITAR SOLICITAÇÃO:**
- **Clique**: Botão vermelho **"Rejeitar"**
- **Confirme** a rejeição
- **Resultado**:
  - ❌ Usuário não pode acessar
  - ❌ Status: "Rejeitado"
  - ❌ Pode solicitar novamente (se necessário)

---

## 🏢 **6. GERENCIAMENTO DE EMPRESAS (SUPER-ADMIN)**

### **📋 Como Gerenciar Empresas via Interface:**

1. **Faça login** como super-administrador
2. **Acesse**: Menu lateral → **"Gerenciar Empresas"**
3. **Visualize o dashboard**:
   - 📊 **Estatísticas**: Total de empresas, membros, solicitações
   - 📈 **Métricas**: Empresas ativas, crescimento

### **➕ CRIAR NOVA EMPRESA:**
1. **Clique**: Botão **"Nova Empresa"**
2. **Preencha o formulário**:
   - **Nome**: "Consultoria Alpha Ltda"
   - **Código**: "ALPHA2024" (único, 4-20 caracteres)
   - **Slug**: "consultoria-alpha" (gerado automaticamente)
   - **Tipo**: Assessoria de Investimentos
   - **Máx. Membros**: 100
   - **Descrição**: "Consultoria especializada em..."
3. **Clique**: **"Criar Empresa"**
4. **Resultado**: ✅ Empresa criada e disponível para registro

### **✏️ EDITAR EMPRESA:**
1. **Na lista de empresas**, clique no ícone de **edição** ✏️
2. **Modifique** os dados necessários
3. **Salve** as alterações
4. **Resultado**: ✅ Empresa atualizada

### **📊 VER ESTATÍSTICAS:**
- 👥 **Membros**: Quantidade de usuários na empresa
- ⏳ **Pendentes**: Solicitações aguardando aprovação
- 📅 **Data criação**: Quando a empresa foi cadastrada
- 🏷️ **Tipo**: Categoria da empresa

---

## 👤 **7. ACESSO DOS MEMBROS APROVADOS**

### **🔐 Como fazer login como Membro:**

1. **Aguarde aprovação** do administrador
2. **Acesse**: `http://localhost:3000/login`
3. **Use suas credenciais** cadastradas
4. **Clique**: "Entrar"

### **🎯 Funcionalidades do Membro:**
- ✅ **Dashboard básico** com métricas
- ✅ **Ver leads** da empresa
- ✅ **Acessar conversas** ativas
- ✅ **Usar base de conhecimento**
- ❌ **Não pode aprovar** novos membros
- ❌ **Não pode alterar** configurações críticas

---

## 🔒 **8. NÍVEIS DE PERMISSÃO**

### **👑 ADMIN/OWNER:**
- ✅ **Tudo** que o membro pode fazer
- ✅ **Aprovar/Rejeitar** solicitações
- ✅ **Gerenciar configurações** da empresa
- ✅ **Convidar novos membros** via email
- ✅ **Alterar base de conhecimento**
- ✅ **Configurar agente de IA**

### **👤 MEMBER:**
- ✅ **Dashboard** e métricas
- ✅ **Leads e conversas** da empresa
- ✅ **Base de conhecimento** (visualizar)
- ❌ **Não pode aprovar** outros usuários
- ❌ **Não pode alterar** configurações

---

## 🛡️ **9. SEGURANÇA E ISOLAMENTO**

### **🔐 Garantias do Sistema:**
- ✅ **Isolamento total** por empresa
- ✅ **RLS (Row Level Security)** no banco
- ✅ **Cada empresa** vê apenas seus dados
- ✅ **Validação de permissões** em todas as APIs
- ✅ **Prevenção de acesso cruzado**

### **📊 Dados Isolados por Empresa:**
- 🎯 **Leads** e qualificações
- 💬 **Conversas** e mensagens
- ⚙️ **Configurações** e base de conhecimento
- 👥 **Membros** e permissões
- 📈 **Métricas** e relatórios

---

## 🚨 **10. CENÁRIOS COMUNS**

### **❓ "Esqueci minha senha"**
1. **Acesse**: Página de login
2. **Clique**: "Esqueci minha senha"
3. **Digite seu email** cadastrado
4. **Verifique seu email** para redefinir

### **❓ "Código da empresa inválido"**
- ✅ **Verifique** se digitou corretamente
- ✅ **Confirme** com seu administrador
- ✅ **Códigos disponíveis**: `DEMO2024`, `LDC2024`, `ABC2024`, `XYZ2024`

### **❓ "Solicitação ainda pendente"**
- ⏰ **Aguarde** a aprovação do administrador
- 📧 **Entre em contato** com admin da empresa
- 🔄 **Não crie** nova conta com mesmo email

### **❓ "Não consigo ver solicitações"**
- 👑 **Apenas admins** podem ver e aprovar
- 🔐 **Verifique** se tem permissão de admin
- 📞 **Contate** o owner da empresa

---

## 🔧 **11. CONFIGURAÇÃO TÉCNICA**

### **🗄️ Banco de Dados:**
- **Tabela**: `public.tenants` (empresas)
- **Coluna**: `code` (código da empresa)
- **Tabela**: `public.join_requests` (solicitações)
- **Tabela**: `public.memberships` (membros aprovados)

### **🌐 URLs Importantes:**
- **Signup**: `/signup`
- **Login**: `/login`
- **Dashboard**: `/dashboard`
- **Solicitações Admin**: `/admin/join-requests`
- **Configurações**: `/settings`

### **🔑 APIs Principais:**
- `POST /api/join-requests` - Criar solicitação
- `GET /api/tenants/{id}/join-requests` - Listar (admin)
- `POST /api/join-requests/{id}/approve` - Aprovar
- `POST /api/join-requests/{id}/reject` - Rejeitar
- `GET /api/company-code/{code}/validate` - Validar código

---

## 📞 **12. SUPORTE**

### **🆘 Em caso de problemas:**

1. **Verifique** se o backend está rodando: `http://localhost:5000/api/health`
2. **Confirme** se o frontend está ativo: `http://localhost:3000`
3. **Consulte** os logs do navegador (F12 → Console)
4. **Teste** com códigos de empresa válidos
5. **Certifique-se** que há admin na empresa para aprovar

### **🔧 Comandos de Debug:**
```bash
# Iniciar backend
cd backend && python app.py

# Iniciar frontend  
cd frontend && npm run dev

# Verificar banco
# Acesse: https://supabase.com/dashboard
```

---

## 🎯 **RESUMO RÁPIDO**

### **👤 Para NOVOS USUÁRIOS:**
1. Acesse `/signup`
2. Use código da empresa (ex: `DEMO2024`)
3. Aguarde aprovação do admin
4. Faça login após aprovação

### **👑 Para ADMINISTRADORES:**
1. Acesse `/admin/join-requests`
2. Veja solicitações pendentes
3. Clique "Aprovar" ou "Rejeitar"
4. Usuário aprovado pode fazer login

### **🏢 Para EMPRESAS:**
1. Solicite criação de código único
2. Defina administrador inicial
3. Admin aprova novos membros
4. Dados totalmente isolados

---

**🚀 Sistema pronto para uso! Qualquer dúvida, consulte este manual ou entre em contato com o suporte técnico.**
