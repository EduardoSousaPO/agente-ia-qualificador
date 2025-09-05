# 🚀 PROMPT COMPLETO PARA CURSOR AI - AGENTE QUALIFICADOR

## 📋 MISSÃO CRÍTICA
Analise COMPLETAMENTE o projeto "Agente Qualificador" e resolva o erro persistente `Cannot read properties of undefined (reading 'call')` que impede o frontend de funcionar. O sistema deve ficar 100% pronto para produção.

## 🎯 CONTEXTO DO PROJETO
- **Tipo**: Micro SaaS para qualificação de leads via WhatsApp
- **Frontend**: Next.js 15.4.7 + React 18.3.1 + TypeScript + Tailwind CSS
- **Backend**: Flask + Python + SQLAlchemy + Supabase
- **Integração**: Twilio WhatsApp + OpenAI GPT-4
- **Autenticação**: Supabase Auth + JWT personalizado

## ❌ PROBLEMA ATUAL
```
Runtime TypeError: Cannot read properties of undefined (reading 'call')
Call Stack: options.factory -> __webpack_require__ -> fn -> requireModule -> initializeModuleChunk -> readChunk -> Object.react_stack_bottom_frame -> beginWork
```

## 🔍 ANÁLISE OBRIGATÓRIA

### 1. AUDITORIA COMPLETA DE ARQUIVOS
```bash
# Examine TODOS os arquivos do projeto:
- frontend/src/**/*.tsx
- frontend/src/**/*.ts  
- frontend/package.json
- frontend/next.config.js
- frontend/tsconfig.json
- backend/**/*.py
- *.md (documentação)
```

### 2. VERIFICAÇÕES CRÍTICAS

#### A) DEPENDÊNCIAS E COMPATIBILIDADE
- [ ] Verificar package.json para conflitos de versões
- [ ] Analisar compatibilidade React 18.3.1 + Next.js 15.4.7
- [ ] Checar se todas as dependências estão instaladas
- [ ] Validar imports dinâmicos vs estáticos

#### B) CONFIGURAÇÕES
- [ ] next.config.js: verificar experimental features
- [ ] tsconfig.json: validar paths e includes
- [ ] Webpack configuration conflicts
- [ ] Module resolution issues

#### C) CÓDIGO FRONTEND
- [ ] src/components/providers.tsx: Supabase initialization
- [ ] src/lib/api.ts: API client setup
- [ ] src/lib/supabase.ts: Client configuration
- [ ] Todos os imports de Supabase (estático vs dinâmico)
- [ ] Server/Client component boundaries

#### D) PADRÕES DE ERRO
- [ ] Procurar por `undefined.call()` patterns
- [ ] Verificar factory functions malformadas
- [ ] Analisar webpack chunks quebrados
- [ ] Identificar circular dependencies

## 🛠️ AÇÕES OBRIGATÓRIAS

### 1. DIAGNÓSTICO PROFUNDO
```typescript
// Procure por estes padrões problemáticos:
- createClient() calls sem verificação
- useEffect sem dependencies corretas
- Imports condicionais malformados
- Factory functions retornando undefined
```

### 2. CORREÇÕES SISTEMÁTICAS

#### A) SUPABASE CLIENT
```typescript
// CORRETO - Import dinâmico seguro:
const { createClient } = await import('@/lib/supabase')
const supabase = createClient()

// INCORRETO - Import estático problemático:
import { createClient } from '@/lib/supabase'
```

#### B) PROVIDERS PATTERN
```typescript
// Verificar se AuthProvider está corretamente implementado
// Garantir que não há calls em undefined objects
```

#### C) WEBPACK CONFIGURATION
```javascript
// next.config.js - Configuração segura
module.exports = {
  experimental: {
    optimizePackageImports: ['@supabase/supabase-js']
  },
  webpack: (config) => {
    config.resolve.fallback = { fs: false, net: false, tls: false }
    return config
  }
}
```

### 3. TESTES OBRIGATÓRIOS
- [ ] npm run build (deve compilar sem erros)
- [ ] npm run dev (deve iniciar sem crashes)
- [ ] Teste de login funcional
- [ ] Verificação de todas as rotas

## 🎯 RESULTADO ESPERADO

### CRITÉRIOS DE SUCESSO:
1. ✅ Frontend inicia sem erros
2. ✅ Login funciona em < 3 segundos
3. ✅ Todas as páginas carregam
4. ✅ Integração Supabase estável
5. ✅ Build de produção sem warnings
6. ✅ TypeScript sem erros
7. ✅ Webpack compilation limpa

### DELIVERABLES:
1. **RELATÓRIO DE DIAGNÓSTICO**: Liste todos os problemas encontrados
2. **CORREÇÕES IMPLEMENTADAS**: Documente cada fix aplicado
3. **TESTES DE VALIDAÇÃO**: Prove que tudo funciona
4. **CONFIGURAÇÃO FINAL**: Deixe pronto para deploy

## 🚨 REGRAS CRÍTICAS

### NÃO FAÇA:
- ❌ Não simplifique ou use fallbacks temporários
- ❌ Não ignore warnings do TypeScript
- ❌ Não deixe console.errors no código
- ❌ Não use soluções "quick fix"

### FAÇA:
- ✅ Analise a causa raiz de cada erro
- ✅ Implemente soluções robustas
- ✅ Teste cada correção individualmente
- ✅ Documente o processo completo
- ✅ Garanta compatibilidade total

## 📊 ESTRUTURA DE RESPOSTA

```markdown
## 🔍 DIAGNÓSTICO COMPLETO
[Lista detalhada de todos os problemas encontrados]

## 🛠️ CORREÇÕES IMPLEMENTADAS
[Cada fix com before/after code]

## ✅ VALIDAÇÃO
[Testes realizados e resultados]

## 🚀 STATUS FINAL
[Confirmação de que está 100% funcional]
```

## 💡 DICAS TÉCNICAS

### FERRAMENTAS DE DEBUG:
```bash
# Limpar caches
rm -rf .next node_modules package-lock.json
npm install

# Verificar dependências
npm ls --depth=0

# Build verbose
npm run build -- --debug

# Análise de bundle
npm run build -- --analyze
```

### PADRÕES COMUNS DE ERRO:
1. **Supabase SSR Issues**: Import dinâmico obrigatório
2. **React 18 Hydration**: Server/client mismatch
3. **Next.js 15 Breaking Changes**: Configurações obsoletas
4. **Webpack Factory Error**: Module resolution problems

---

**🎯 OBJETIVO FINAL**: Deixar o "Agente Qualificador" 100% funcional, estável e pronto para receber leads reais via WhatsApp, com performance otimizada e zero erros.

**⏰ PRIORIDADE MÁXIMA**: Resolver o erro `Cannot read properties of undefined (reading 'call')` que está impedindo o sistema de funcionar.


