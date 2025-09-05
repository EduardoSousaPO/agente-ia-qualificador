# 🎯 **EXEMPLOS PRÁTICOS - ONBOARDING CORPORATIVO**
## **Cenários Reais de Uso do Sistema**

---

## 📋 **CENÁRIO 1: Nova Empresa "Investimentos Alpha"**

### **🏢 PASSO 1: Admin cria a empresa**
```sql
-- Executar no Supabase SQL Editor:
INSERT INTO public.tenants (name, slug, code, settings) VALUES
(
  'Investimentos Alpha Ltda',
  'investimentos-alpha', 
  'ALPHA2024',
  '{"company_type": "investment_advisory", "max_members": 50}'::jsonb
);
```

### **👤 PASSO 2: Primeiro funcionário se registra**
1. **Acessa**: `http://localhost:3000/signup`
2. **Preenche**:
   - Nome: "João Silva"
   - Email: "joao@alpha.com.br"
   - **Código da empresa**: `ALPHA2024` ✅
   - Nome da empresa: "Investimentos Alpha Ltda" (preenchido automaticamente)
   - Senha: "MinhaSenh@123"
3. **Resultado**: Solicitação criada, aguardando aprovação

### **👑 PASSO 3: Tornar o primeiro usuário admin**
```sql
-- Executar após o usuário se registrar:
INSERT INTO public.memberships (tenant_id, user_id, role)
SELECT 
  t.id as tenant_id,
  u.id as user_id,
  'admin' as role
FROM public.tenants t, auth.users u
WHERE t.code = 'ALPHA2024' 
  AND u.email = 'joao@alpha.com.br'
ON CONFLICT (tenant_id, user_id) DO UPDATE SET role = 'admin';
```

### **🎯 PASSO 4: Agora João pode aprovar outros**
- João faz login
- Acessa `/admin/join-requests`
- Aprova novos funcionários da Alpha

---

## 📋 **CENÁRIO 2: Funcionário quer entrar na empresa existente**

### **👤 Maria quer entrar na "LDC Capital"**

1. **Acessa**: `http://localhost:3000/signup`
2. **Preenche**:
   - Nome: "Maria Santos"
   - Email: "maria@ldc.com.br"
   - **Código da empresa**: `LDC2024` ✅
   - Nome da empresa: "LDC Capital Investimentos" (automático)
   - Senha: "Senha123@"
3. **Clica**: "Criar conta"
4. **Resultado**: 
   - ✅ Conta criada
   - ⏳ Solicitação pendente
   - 📧 Mensagem: "Aguarde aprovação do administrador"

### **👑 Admin da LDC Capital aprova**
1. **Admin faz login** no sistema
2. **Acessa**: Menu → "Solicitações"
3. **Vê a solicitação** de Maria:
   - 👤 Nome: Maria Santos
   - 📧 Email: maria@ldc.com.br
   - 🏢 Empresa: LDC Capital Investimentos (LDC2024)
   - ⏰ Data: Hoje às 14:30
4. **Clica**: Botão verde "Aprovar"
5. **Resultado**: 
   - ✅ Maria vira membro
   - ✅ Pode fazer login
   - ✅ Acesso aos dados da LDC

### **👤 Maria faz login pela primeira vez**
1. **Acessa**: `http://localhost:3000/login`
2. **Credenciais**:
   - Email: "maria@ldc.com.br"
   - Senha: "Senha123@"
3. **Resultado**:
   - ✅ Login bem-sucedido
   - 🎯 Redirecionada para dashboard
   - 📊 Vê apenas dados da LDC Capital
   - 🚫 Não vê dados de outras empresas

---

## 📋 **CENÁRIO 3: Erro comum - Código inválido**

### **❌ Pedro tenta código que não existe**

1. **Acessa**: `http://localhost:3000/signup`
2. **Preenche**:
   - Nome: "Pedro Costa"
   - Email: "pedro@email.com"
   - **Código da empresa**: `INEXISTENTE2024` ❌
3. **Resultado**:
   - ❌ Campo fica vermelho
   - ❌ Mensagem: "Código da empresa não encontrado"
   - ❌ Não consegue prosseguir

### **✅ Solução**:
1. **Pedro verifica** códigos válidos:
   - `DEMO2024` - Escritório de Investimentos Demo
   - `LDC2024` - LDC Capital Investimentos
   - `ABC2024` - Consultoria Financeira ABC
   - `XYZ2024` - Gestora XYZ Wealth
2. **Usa código correto**: `DEMO2024`
3. **Consegue** se registrar normalmente

---

## 📋 **CENÁRIO 4: Admin gerenciando múltiplas solicitações**

### **👑 Admin da "Consultoria ABC" tem 5 solicitações**

**Dashboard mostra:**
- 📊 **5 Pendentes** | 12 Aprovadas | 2 Rejeitadas | 19 Total

**Lista de solicitações:**
1. **Ana Silva** - ana@abc.com - Hoje 09:15 ⏳
2. **Carlos Pereira** - carlos@abc.com - Hoje 10:30 ⏳  
3. **Fernanda Lima** - fernanda@abc.com - Hoje 11:45 ⏳
4. **Roberto Santos** - roberto@abc.com - Hoje 13:20 ⏳
5. **Lucia Costa** - lucia@abc.com - Hoje 14:10 ⏳

### **✅ Admin aprova todos de uma vez:**
1. **Clica "Aprovar"** na Ana → ✅ Aprovada
2. **Clica "Aprovar"** no Carlos → ✅ Aprovado
3. **Clica "Aprovar"** na Fernanda → ✅ Aprovada
4. **Clica "Aprovar"** no Roberto → ✅ Aprovado
5. **Clica "Aprovar"** na Lucia → ✅ Aprovada

### **📊 Dashboard atualiza automaticamente:**
- 📊 **0 Pendentes** | 17 Aprovadas | 2 Rejeitadas | 19 Total

### **👥 Todos podem fazer login:**
- Ana, Carlos, Fernanda, Roberto e Lucia
- Recebem acesso completo aos dados da ABC
- Podem usar o sistema normalmente

---

## 📋 **CENÁRIO 5: Rejeição de solicitação**

### **❌ Solicitação suspeita**

**Admin vê solicitação:**
- 👤 Nome: "Hacker Malicioso"
- 📧 Email: "hack@competitor.com"
- 🏢 Empresa: Consultoria Financeira ABC (ABC2024)
- ⏰ Data: Hoje às 02:30 (horário suspeito)

### **🚫 Admin rejeita:**
1. **Clica**: Botão vermelho "Rejeitar"
2. **Confirma**: "Tem certeza que deseja rejeitar?"
3. **Resultado**:
   - ❌ Status: "Rejeitado"
   - ❌ Usuário não pode fazer login
   - ❌ Sem acesso aos dados da empresa

### **🔒 Usuário rejeitado tenta fazer login:**
1. **Acessa**: `/login`
2. **Credenciais**: hack@competitor.com / senha
3. **Resultado**: 
   - ❌ "Credenciais inválidas" 
   - ❌ Sem acesso ao sistema

---

## 📋 **CENÁRIO 6: Filtros na interface admin**

### **👑 Admin com muitas solicitações usa filtros**

**Situação inicial:**
- 📊 **8 Pendentes** | 45 Aprovadas | 12 Rejeitadas | 65 Total

### **🔍 Admin quer ver apenas pendentes:**
1. **Clica**: Filtro "Pendentes"
2. **Resultado**: Lista mostra apenas 8 solicitações pendentes
3. **Aprova**: As que são válidas
4. **Rejeita**: As suspeitas

### **📊 Admin quer revisar rejeitadas:**
1. **Clica**: Filtro "Rejeitadas"  
2. **Resultado**: Lista mostra apenas 12 rejeitadas
3. **Analisa**: Se alguma foi rejeitada por engano
4. **Pode reavaliar**: Se necessário

### **📈 Admin quer ver histórico:**
1. **Clica**: Filtro "Aprovadas"
2. **Resultado**: Lista mostra 45 aprovações
3. **Vê**: Quem foi aprovado e quando
4. **Controla**: Crescimento da equipe

---

## 🎯 **DICAS PRÁTICAS**

### **👑 Para Administradores:**
- ✅ **Verifique diariamente** as solicitações pendentes
- ✅ **Confirme identidade** antes de aprovar
- ✅ **Use filtros** para organizar visualização
- ✅ **Monitore** tentativas suspeitas
- ✅ **Mantenha** comunicação com a equipe

### **👤 Para Novos Usuários:**
- ✅ **Confirme o código** da empresa com seu gestor
- ✅ **Use dados reais** no cadastro
- ✅ **Aguarde pacientemente** a aprovação
- ✅ **Entre em contato** com admin se demorar
- ✅ **Teste o login** após aprovação

### **🏢 Para Empresas:**
- ✅ **Defina admin** responsável pelas aprovações
- ✅ **Comunique o código** da empresa aos funcionários
- ✅ **Estabeleça processo** interno de solicitação
- ✅ **Monitore** quem está solicitando acesso
- ✅ **Mantenha** segurança dos dados

---

**🚀 Com estes exemplos práticos, qualquer empresa pode implementar o onboarding corporativo de forma segura e eficiente!**
