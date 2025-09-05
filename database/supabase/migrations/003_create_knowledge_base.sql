-- Criar tabela knowledge_base
CREATE TABLE IF NOT EXISTS public.knowledge_base (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES public.tenants(id) ON DELETE CASCADE,
  user_id UUID NOT NULL,
  content TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  
  -- Constraint para garantir apenas um conhecimento por tenant
  UNIQUE(tenant_id)
);

-- Habilitar RLS
ALTER TABLE public.knowledge_base ENABLE ROW LEVEL SECURITY;

-- Política RLS: usuários podem acessar apenas conhecimento do seu tenant
CREATE POLICY "Users can access their tenant knowledge base" ON public.knowledge_base
FOR ALL USING (
  tenant_id IN (
    SELECT tenant_id FROM public.users WHERE id = auth.uid()
    UNION
    SELECT tenant_id FROM public.memberships WHERE user_id = auth.uid()
  )
);

-- Índices para performance
CREATE INDEX IF NOT EXISTS idx_knowledge_base_tenant_id ON public.knowledge_base(tenant_id);
CREATE INDEX IF NOT EXISTS idx_knowledge_base_updated_at ON public.knowledge_base(updated_at);

-- Trigger para atualizar updated_at automaticamente
CREATE OR REPLACE FUNCTION update_knowledge_base_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_knowledge_base_updated_at
  BEFORE UPDATE ON public.knowledge_base
  FOR EACH ROW
  EXECUTE FUNCTION update_knowledge_base_updated_at();

-- Inserir conhecimento padrão para o tenant demo
INSERT INTO public.knowledge_base (tenant_id, user_id, content) VALUES (
  '60675861-e22a-4990-bab8-65ed07632a63',
  '5f9c5ba8-0ad7-43a6-92df-c205cb6b5e23',
  '**Sobre Nossa Empresa:**

Somos uma consultoria especializada em investimentos de alto patrimônio, focada em aposentadoria e crescimento patrimonial de longo prazo.

**Critérios de Qualificação:**
- Patrimônio mínimo: R$ 500.000 para investir
- Perfil conservador a moderado
- Objetivo: aposentadoria ou crescimento patrimonial
- Prazo de investimento: mínimo 5 anos

**Nossos Produtos:**
- Carteiras diversificadas personalizadas
- Fundos exclusivos de investimento
- Planejamento sucessório
- Consultoria financeira especializada

**Diferenciais:**
- Especialistas certificados CPA-20 e CFP
- Atendimento personalizado e consultivo
- Foco em relacionamento de longo prazo
- Estratégias conservadoras e sustentáveis

**Processo de Atendimento:**
1. Qualificação inicial via WhatsApp
2. Agendamento de consultoria gratuita
3. Análise de perfil e objetivos
4. Proposta personalizada de investimentos
5. Acompanhamento contínuo da carteira'
) ON CONFLICT (tenant_id) DO NOTHING;
