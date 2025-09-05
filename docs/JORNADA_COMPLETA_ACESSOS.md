# 👑 **JORNADA COMPLETA DE ACESSOS - HIERARQUIA DO SISTEMA**

## **🏗️ ESTRUTURA HIERÁRQUICA DO SISTEMA**

```
🌟 SUPER-ADMIN (Sistema)
├── 👑 OWNER (Dono da Empresa)
│   ├── 👨‍💼 ADMIN (Administrador)
│   │   └── 👤 MEMBER (Membro/Usuário)
│   └── 👤 MEMBER (Membro/Usuário)
└── 🏢 [Outras Empresas...]
```

---

## 🌟 **NÍVEL 1: SUPER-ADMIN (Administrador do Sistema)**

### **👤 QUEM É:**
- **Desenvolvedor/Owner** do sistema completo
- **Responsável técnico** pela plataforma
- **Único** com acesso total ao sistema

### **🎯 JORNADA DE ACESSO:**

#### **🔐 LOGIN:**
```
Email: admin@sistema.com
Senha: [senha master do sistema]
URL: http://localhost:3000/login
```

#### **🎛️ DASHBOARD SUPER-ADMIN:**
```
📊 VISÃO GLOBAL DO SISTEMA:
├── 🏢 Total: 15 empresas ativas
├── 👥 Usuários: 450 membros no sistema
├── 📈 Crescimento: +5 empresas este mês
└── ⚡ Performance: Sistema 99.9% uptime
```

#### **🔧 FUNCIONALIDADES EXCLUSIVAS:**
- ✅ **Gerenciar Empresas** (`/admin/companies`)
  - Criar, editar, desativar empresas
  - Ver estatísticas globais
  - Definir limites por empresa
- ✅ **Monitorar Sistema**
  - Logs de todas as empresas
  - Performance e uptime
  - Backup e manutenção
- ✅ **Configurações Globais**
  - Limites do sistema
  - Integrações (Supabase, OpenAI)
  - Políticas de segurança

### **🎯 EXEMPLO PRÁTICO - SUPER-ADMIN:**
```
João (Super-Admin) acorda e:
1. 📊 Verifica dashboard: 3 novas empresas ontem
2. 🏢 Aprova criação da "Investimentos Alpha" 
3. ⚙️ Configura limite de 200 membros para eles
4. 📈 Analisa métricas: crescimento de 15% no mês
5. 🔧 Agenda backup automático para domingo
```

---

## 👑 **NÍVEL 2: OWNER (Dono da Empresa)**

### **👤 QUEM É:**
- **Fundador/Sócio** da empresa
- **Responsável final** pela empresa
- **Único** que pode nomear outros admins

### **🎯 JORNADA DE ACESSO:**

#### **📝 COMO VIRA OWNER:**
**MÉTODO 1: Primeiro usuário da empresa**
```sql
-- Super-admin executa após empresa ser criada:
INSERT INTO public.memberships (tenant_id, user_id, role)
VALUES ('[TENANT_ID]', '[USER_ID]', 'owner');
```

**MÉTODO 2: Promoção por outro Owner**
- Owner atual promove admin para owner
- Pode haver múltiplos owners por empresa

#### **🔐 LOGIN:**
```
Email: carlos@investimentosalpha.com
Senha: [senha pessoal]
URL: http://localhost:3000/login
```

#### **🎛️ DASHBOARD OWNER:**
```
📊 EMPRESA: Investimentos Alpha
├── 👥 Membros: 25 (limite: 200)
├── ⏳ Pendentes: 3 solicitações
├── 📈 Leads: 150 este mês (+20%)
└── 💰 Qualificados: 45 leads (30% taxa)
```

#### **🔧 FUNCIONALIDADES DO OWNER:**
- ✅ **Tudo que Admin pode fazer** +
- ✅ **Gerenciar Admins**
  - Promover membros para admin
  - Rebaixar admins para membro
  - Definir permissões especiais
- ✅ **Configurações da Empresa**
  - Alterar nome, descrição
  - Definir políticas internas
  - Configurar integrações
- ✅ **Billing e Limites**
  - Ver uso de recursos
  - Solicitar aumento de limites
  - Gerenciar assinatura

### **🎯 EXEMPLO PRÁTICO - OWNER:**
```
Carlos (Owner da Alpha) na segunda-feira:
1. 📊 Revisa performance: 30% de qualificação
2. 👥 Promove Ana (membro) para admin
3. ⏳ Aprova 3 solicitações pendentes
4. 📈 Analisa ROI: R$ 50k em novos clientes
5. 🎯 Define meta: 40% qualificação próximo mês
6. 💼 Agenda reunião com equipe comercial
```

---

## 👨‍💼 **NÍVEL 3: ADMIN (Administrador da Empresa)**

### **👤 QUEM É:**
- **Gerente/Coordenador** da empresa
- **Mão direita** do owner
- **Responsável** pelo dia a dia operacional

### **🎯 JORNADA DE ACESSO:**

#### **📝 COMO VIRA ADMIN:**
1. **Owner promove** membro existente, OU
2. **Convite direto** com role admin, OU
3. **Aprovação** de join-request como admin

#### **🔐 LOGIN:**
```
Email: ana@investimentosalpha.com
Senha: [senha pessoal]
URL: http://localhost:3000/login
```

#### **🎛️ DASHBOARD ADMIN:**
```
📊 VISÃO OPERACIONAL:
├── ⏳ 5 solicitações para aprovar
├── 💬 12 conversas ativas hoje
├── 🎯 8 leads qualificados ontem
└── 👥 3 membros da equipe online
```

#### **🔧 FUNCIONALIDADES DO ADMIN:**
- ✅ **Aprovar Solicitações** (`/admin/join-requests`)
  - Ver todas as solicitações
  - Aprovar/rejeitar candidatos
  - Definir role (member/admin)
- ✅ **Gerenciar Leads**
  - Ver todos os leads da empresa
  - Iniciar qualificações manuais
  - Exportar relatórios
- ✅ **Configurar Sistema**
  - Base de conhecimento
  - Prompts da IA
  - Validação do agente
- ✅ **Monitorar Equipe**
  - Ver atividade dos membros
  - Relatórios de performance
  - Métricas de conversão

### **🎯 EXEMPLO PRÁTICO - ADMIN:**
```
Ana (Admin da Alpha) na terça-feira:
1. ⏳ Aprova 2 solicitações de novos vendedores
2. 🎯 Configura nova base de conhecimento
3. 📊 Gera relatório semanal para Carlos (Owner)
4. 💬 Monitora 15 conversas ativas
5. 🔧 Ajusta prompts da IA (melhor qualificação)
6. 👥 Treina novo membro sobre o sistema
```

---

## 👤 **NÍVEL 4: MEMBER (Membro/Usuário)**

### **👤 QUEM É:**
- **Vendedor/Operador** da empresa
- **Usuário final** do sistema
- **Foco** em leads e conversas

### **🎯 JORNADA DE ACESSO:**

#### **📝 COMO VIRA MEMBER:**

**FLUXO COMPLETO:**
1. **Registro**: `/signup` com código da empresa
2. **Aguarda**: Aprovação do admin/owner
3. **Login**: Após aprovação
4. **Trabalha**: Com leads e conversas

#### **🔐 LOGIN:**
```
Email: pedro@investimentosalpha.com
Senha: [senha pessoal]
URL: http://localhost:3000/login
```

#### **🎛️ DASHBOARD MEMBER:**
```
📊 VISÃO OPERACIONAL:
├── 🎯 Meus leads: 25 ativos
├── 💬 Conversas: 8 em andamento
├── ✅ Qualificados: 6 hoje
└── 📈 Meta mensal: 75% (18/24)
```

#### **🔧 FUNCIONALIDADES DO MEMBER:**
- ✅ **Trabalhar com Leads**
  - Ver leads atribuídos
  - Iniciar conversas
  - Acompanhar qualificação
- ✅ **Dashboard Pessoal**
  - Métricas individuais
  - Metas e progresso
  - Histórico de performance
- ✅ **Ferramentas Básicas**
  - Base de conhecimento (leitura)
  - Exemplos de conversas
  - Relatórios básicos

### **🎯 EXEMPLO PRÁTICO - MEMBER:**
```
Pedro (Vendedor da Alpha) na quarta-feira:
1. 📊 Checa dashboard: 6 novos leads
2. 💬 Inicia 3 conversas via WhatsApp
3. 🎯 Acompanha qualificação automática
4. ✅ Confirma 2 leads qualificados
5. 📞 Agenda reunião com lead premium
6. 📈 Atualiza CRM com resultados
```

---

## 🔄 **FLUXOS DE ACESSO DETALHADOS**

### **🚀 FLUXO 1: Primeira Empresa no Sistema**

#### **PASSO 1: Super-Admin cria empresa**
```
Super-Admin João:
1. 🖱️ Acessa /admin/companies
2. ➕ Clica "Nova Empresa"
3. 📝 Preenche: "Investimentos Alpha" / "ALPHA2024"
4. ✅ Empresa criada no sistema
```

#### **PASSO 2: Dono se registra**
```
Carlos (futuro owner):
1. 📝 Vai em /signup
2. 🔑 Usa código "ALPHA2024"
3. ⏳ Solicitação fica pendente
4. 📧 Super-admin recebe notificação
```

#### **PASSO 3: Super-Admin promove para Owner**
```sql
-- Super-admin executa:
UPDATE public.memberships 
SET role = 'owner' 
WHERE user_id = '[CARLOS_ID]' AND tenant_id = '[ALPHA_ID]';
```

#### **PASSO 4: Owner tem acesso total**
```
Carlos (agora Owner):
1. 🔐 Faz login
2. 👑 Vê interface completa de owner
3. 🎯 Pode aprovar solicitações
4. 👥 Pode promover admins
```

### **🚀 FLUXO 2: Novo Funcionário na Empresa Existente**

#### **PASSO 1: Funcionário se registra**
```
Pedro (vendedor):
1. 📝 Acessa /signup
2. 🔑 Usa código "ALPHA2024"
3. 📧 Email: pedro@investimentosalpha.com
4. ⏳ Aguarda aprovação
```

#### **PASSO 2: Admin aprova**
```
Ana (Admin da Alpha):
1. 🔐 Login no sistema
2. 📋 Acessa /admin/join-requests
3. 👤 Vê solicitação do Pedro
4. ✅ Clica "Aprovar" como "member"
```

#### **PASSO 3: Pedro acessa como membro**
```
Pedro (agora member):
1. 🔐 Faz login
2. 📊 Vê dashboard de membro
3. 🎯 Acessa apenas leads da Alpha
4. 💬 Pode trabalhar com conversas
```

### **🚀 FLUXO 3: Promoção Interna**

#### **CENÁRIO: Pedro vira Admin**
```
Carlos (Owner) decide:
1. 👤 Pedro está performando bem
2. 📈 Quer promovê-lo para admin
3. 🎯 Acessa configurações de membros
4. ⬆️ Promove Pedro: member → admin
```

#### **RESULTADO:**
```
Pedro (agora admin):
1. 🔄 Próximo login: interface admin
2. ✅ Pode aprovar solicitações
3. 🔧 Pode configurar sistema
4. 📊 Vê métricas completas da empresa
```

---

## 🎯 **COMPARAÇÃO DE ACESSOS**

### **📊 MATRIZ DE PERMISSÕES**

| Funcionalidade | 🌟 Super | 👑 Owner | 👨‍💼 Admin | 👤 Member |
|----------------|----------|----------|------------|-----------|
| **Criar Empresas** | ✅ | ❌ | ❌ | ❌ |
| **Configurar Sistema** | ✅ | ❌ | ❌ | ❌ |
| **Promover Owners** | ✅ | ✅ | ❌ | ❌ |
| **Promover Admins** | ✅ | ✅ | ❌ | ❌ |
| **Aprovar Solicitações** | ✅ | ✅ | ✅ | ❌ |
| **Configurar Empresa** | ✅ | ✅ | ✅ | ❌ |
| **Ver Todos os Leads** | ✅ | ✅ | ✅ | ❌ |
| **Trabalhar com Leads** | ✅ | ✅ | ✅ | ✅ |
| **Dashboard Pessoal** | ✅ | ✅ | ✅ | ✅ |

### **🔐 ISOLAMENTO DE DADOS**

```
🏢 EMPRESA A (Alpha):
├── 👑 Carlos (Owner) - Vê tudo da Alpha
├── 👨‍💼 Ana (Admin) - Vê tudo da Alpha  
└── 👤 Pedro (Member) - Vê apenas seus leads da Alpha

🏢 EMPRESA B (Beta):
├── 👑 Maria (Owner) - Vê tudo da Beta
└── 👤 João (Member) - Vê apenas seus leads da Beta

🚫 ISOLAMENTO: Pedro nunca vê dados da Beta
🚫 ISOLAMENTO: João nunca vê dados da Alpha
```

---

## 🎯 **CENÁRIOS PRÁTICOS COMPLETOS**

### **📋 CENÁRIO 1: Dia Típico na "Investimentos Alpha"**

#### **🌅 MANHÃ (9:00)**
```
Carlos (Owner):
├── 📊 Revisa dashboard: 5 novos leads ontem
├── ⏳ 2 solicitações de funcionários pendentes
└── 📈 Meta mensal: 80% atingida

Ana (Admin):
├── ✅ Aprova 2 solicitações pendentes
├── 🔧 Atualiza base de conhecimento
└── 📊 Prepara relatório para Carlos

Pedro (Member):
├── 🎯 6 novos leads atribuídos
├── 💬 3 conversas ativas do dia anterior
└── 📞 2 reuniões agendadas
```

#### **🌆 TARDE (14:00)**
```
Carlos (Owner):
├── 👥 Promove Pedro para admin (boa performance)
├── 💼 Reunião com equipe comercial
└── 🎯 Define novas metas trimestrais

Ana (Admin):
├── 🎓 Treina Pedro nas funções de admin
├── 📊 Monitora conversas ativas (15 em andamento)
└── 🔧 Ajusta prompts da IA

Pedro (novo Admin):
├── 🆕 Explora interface admin
├── ⏳ Vê solicitações pendentes pela primeira vez
└── 📚 Estuda configurações do sistema
```

### **📋 CENÁRIO 2: Onboarding de Nova Empresa**

#### **DIA 1: Criação**
```
João (Super-Admin):
├── 🏢 Cria "Consultoria Beta" / "BETA2024"
├── 📧 Envia código para Maria (futura owner)
└── 📊 Monitora métricas globais do sistema
```

#### **DIA 2: Primeiro Acesso**
```
Maria (registra-se):
├── 📝 Signup com código "BETA2024"
├── ⏳ Aguarda aprovação
└── 📧 Recebe email de confirmação

João (Super-Admin):
├── 👑 Promove Maria para owner da Beta
├── ✅ Maria pode fazer login
└── 🎯 Sistema pronto para a Beta
```

#### **DIA 3: Primeira Equipe**
```
Maria (Owner da Beta):
├── 📋 Acessa /admin/join-requests
├── 👥 Convida 5 funcionários
└── ⏳ 3 já se registraram e aguardam

Roberto (funcionário):
├── 📝 Registra-se com "BETA2024"
├── ⏳ Aguarda aprovação da Maria
└── 📧 Recebe confirmação de solicitação
```

#### **DIA 4: Equipe Ativa**
```
Maria (Owner):
├── ✅ Aprova 3 funcionários como members
├── 👨‍💼 Promove Roberto para admin
└── 🎯 Equipe da Beta está operacional

Roberto (Admin da Beta):
├── 🔧 Configura base de conhecimento
├── 🎯 Importa primeiros leads
└── 💬 Testa conversas com IA
```

---

## 🚀 **JORNADAS DE CRESCIMENTO**

### **📈 EVOLUÇÃO DO USUÁRIO:**

```
👤 MEMBER (Início)
├── 📊 Trabalha com leads
├── 💬 Usa conversas
├── 📈 Mostra resultados
└── ⬆️ Performance alta

👨‍💼 ADMIN (Promoção)
├── ✅ Aprova solicitações  
├── 🔧 Configura sistema
├── 📊 Monitora equipe
└── ⬆️ Liderança demonstrada

👑 OWNER (Promoção/Fundação)
├── 🏢 Responsável pela empresa
├── 👥 Gerencia toda equipe
├── 💼 Define estratégias
└── 🎯 Crescimento da empresa

🌟 SUPER-ADMIN (Técnico)
├── 🔧 Mantém sistema
├── 🏢 Gerencia todas empresas
├── 📈 Escala plataforma
└── 🌍 Visão global
```

---

## 🎯 **RESUMO DAS JORNADAS**

### **🌟 SUPER-ADMIN:**
- **Foco**: Sistema completo
- **Acesso**: Todas as empresas
- **Responsabilidade**: Plataforma global

### **👑 OWNER:**
- **Foco**: Sua empresa
- **Acesso**: Total na empresa
- **Responsabilidade**: Crescimento e estratégia

### **👨‍💼 ADMIN:**
- **Foco**: Operação diária
- **Acesso**: Gerencial na empresa
- **Responsabilidade**: Equipe e processos

### **👤 MEMBER:**
- **Foco**: Leads e vendas
- **Acesso**: Operacional limitado
- **Responsabilidade**: Performance individual

---

**🎯 CONCLUSÃO: Cada nível tem sua jornada específica, com responsabilidades e acessos adequados ao seu papel. O sistema garante isolamento total entre empresas e progressão natural de responsabilidades.**
