-- Seed: LDC Capital Tenant
-- Cria tenant de exemplo conforme especificação

-- ===============================
-- 1. CRIAR TENANT LDC CAPITAL
-- ===============================

-- Inserir LDC Capital se não existir
insert into public.tenants (name, slug, settings)
values (
  'LDC Capital',
  'ldc-capital',
  '{
    "company_type": "investment_advisory",
    "qualification_threshold": 70,
    "ai_model": "gpt-4o-mini",
    "whatsapp_enabled": true,
    "email_notifications": true,
    "timezone": "America/Sao_Paulo"
  }'::jsonb
)
on conflict (slug) do update set
  name = excluded.name,
  settings = excluded.settings,
  updated_at = now();

-- ===============================
-- 2. CRIAR INVITE ADMIN DE TESTE
-- ===============================

-- Obter ID do tenant LDC Capital
do $$
declare
  ldc_tenant_id uuid;
begin
  select id into ldc_tenant_id 
  from public.tenants 
  where slug = 'ldc-capital';
  
  -- Criar invite admin de teste
  insert into public.invites (tenant_id, email, role, status)
  values (
    ldc_tenant_id,
    'admin@ldc-capital.com',
    'admin',
    'pending'
  )
  on conflict (tenant_id, email) do update set
    role = excluded.role,
    status = 'pending',
    created_at = now();
  
  -- Log do resultado
  raise notice 'LDC Capital tenant criado com ID: %', ldc_tenant_id;
  raise notice 'Invite admin criado para: admin@ldc-capital.com';
end $$;

-- ===============================
-- 3. CONHECIMENTO BASE EXEMPLO
-- ===============================

-- Verificar se existe tabela de knowledge e popular
do $$
begin
  -- Verificar se existe alguma tabela knowledge_*
  if exists (
    select 1 from information_schema.tables 
    where table_schema = 'public' 
    and table_name like 'knowledge_%'
  ) then
    raise notice 'Tabelas de knowledge encontradas - implementar seed específico';
  else
    raise notice 'Nenhuma tabela de knowledge encontrada - pular seed de conhecimento';
  end if;
end $$;

-- ===============================
-- 4. CONFIGURAÇÕES ESPECÍFICAS
-- ===============================

-- Atualizar configurações específicas do LDC Capital
update public.tenants 
set settings = settings || '{
  "qualification_questions": [
    {
      "id": "patrimonio",
      "question": "Quanto você tem disponível para investir hoje?",
      "type": "multiple_choice",
      "options": ["Até R$ 100k", "R$ 100k - R$ 500k", "R$ 500k - R$ 1M", "Acima de R$ 1M"],
      "weight": 30
    },
    {
      "id": "objetivo",
      "question": "Qual seu principal objetivo com os investimentos?",
      "type": "multiple_choice", 
      "options": ["Preservar capital", "Crescimento moderado", "Crescimento agressivo", "Renda passiva"],
      "weight": 25
    },
    {
      "id": "urgencia",
      "question": "Quando pretende começar a investir?",
      "type": "multiple_choice",
      "options": ["Imediatamente", "Em até 30 dias", "Em até 3 meses", "Ainda estou estudando"],
      "weight": 25
    },
    {
      "id": "interesse",
      "question": "Gostaria de falar com um de nossos especialistas?",
      "type": "boolean",
      "weight": 20
    }
  ],
  "contact_info": {
    "phone": "+55 11 99999-9999",
    "email": "contato@ldc-capital.com",
    "website": "https://ldc-capital.com",
    "address": "São Paulo, SP"
  },
  "business_hours": {
    "monday": "09:00-18:00",
    "tuesday": "09:00-18:00", 
    "wednesday": "09:00-18:00",
    "thursday": "09:00-18:00",
    "friday": "09:00-18:00",
    "saturday": "closed",
    "sunday": "closed"
  }
}'::jsonb
where slug = 'ldc-capital';

-- ===============================
-- 5. VERIFICAÇÃO FINAL
-- ===============================

-- Mostrar dados criados
select 
  'LDC Capital Seed Summary' as title,
  t.id as tenant_id,
  t.name,
  t.slug,
  (select count(*) from public.invites where tenant_id = t.id) as pending_invites,
  t.created_at
from public.tenants t
where t.slug = 'ldc-capital';

-- Mostrar invites pendentes
select 
  'Pending Invites' as title,
  i.email,
  i.role,
  i.status,
  i.created_at
from public.invites i
join public.tenants t on i.tenant_id = t.id
where t.slug = 'ldc-capital';

select 'LDC Capital seed completed successfully' as status;











