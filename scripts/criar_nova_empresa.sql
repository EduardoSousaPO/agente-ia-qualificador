-- ==========================================
-- SCRIPT: Criar Nova Empresa no Sistema
-- ==========================================
-- 
-- INSTRUÇÕES:
-- 1. Substitua os valores entre [ ] pelos dados reais
-- 2. Execute no Supabase SQL Editor
-- 3. Anote o código gerado para fornecer aos usuários
--

-- ==========================================
-- PASSO 1: Criar a empresa
-- ==========================================

INSERT INTO public.tenants (name, slug, code, settings) VALUES
(
  '[NOME_DA_EMPRESA]',           -- Ex: 'Consultoria XYZ Ltda'
  '[SLUG_DA_EMPRESA]',           -- Ex: 'consultoria-xyz' (sem espaços, minúsculo)
  '[CODIGO_DA_EMPRESA]',         -- Ex: 'XYZ2024' (único, fácil de lembrar)
  '{"company_type": "investment_advisory", "max_members": 50}'::jsonb
);

-- ==========================================
-- PASSO 2: Verificar se foi criado
-- ==========================================

SELECT 
  id,
  name as "Nome da Empresa",
  slug as "Slug",
  code as "Código da Empresa",
  created_at as "Criado em"
FROM public.tenants 
WHERE code = '[CODIGO_DA_EMPRESA]';

-- ==========================================
-- PASSO 3: (OPCIONAL) Criar admin inicial
-- ==========================================
-- 
-- Se você quiser criar um admin diretamente no banco:
-- 
-- 1. Primeiro, o usuário deve se registrar normalmente via /signup
-- 2. Depois, execute os comandos abaixo para torná-lo admin:

-- -- Buscar o usuário pelo email
-- SELECT id, email FROM auth.users WHERE email = '[EMAIL_DO_ADMIN]';

-- -- Criar profile se não existir
-- INSERT INTO public.profiles (user_id) 
-- SELECT id FROM auth.users WHERE email = '[EMAIL_DO_ADMIN]'
-- ON CONFLICT (user_id) DO NOTHING;

-- -- Criar membership como admin
-- INSERT INTO public.memberships (tenant_id, user_id, role)
-- SELECT 
--   t.id as tenant_id,
--   u.id as user_id,
--   'admin' as role
-- FROM public.tenants t, auth.users u
-- WHERE t.code = '[CODIGO_DA_EMPRESA]' 
--   AND u.email = '[EMAIL_DO_ADMIN]'
-- ON CONFLICT (tenant_id, user_id) DO UPDATE SET role = 'admin';

-- ==========================================
-- EXEMPLO PRÁTICO:
-- ==========================================

-- INSERT INTO public.tenants (name, slug, code, settings) VALUES
-- (
--   'Investimentos Alpha Ltda',
--   'investimentos-alpha',
--   'ALPHA2024',
--   '{"company_type": "investment_advisory", "max_members": 100}'::jsonb
-- );

-- ==========================================
-- CÓDIGOS JÁ UTILIZADOS (não usar):
-- ==========================================
-- DEMO2024 - Escritório de Investimentos Demo
-- LDC2024  - LDC Capital Investimentos  
-- ABC2024  - Consultoria Financeira ABC
-- XYZ2024  - Gestora XYZ Wealth

-- ==========================================
-- SUGESTÕES DE CÓDIGOS:
-- ==========================================
-- [SIGLA_EMPRESA][ANO] - Ex: ALPHA2024, BETA2024
-- [NOME][ANO] - Ex: INVEST2024, CAPITAL2024
-- [INICIAIS][ANO] - Ex: ABC2024, XYZ2024
-- 
-- IMPORTANTE: 
-- - Deve ser ÚNICO
-- - Fácil de lembrar
-- - Entre 6-20 caracteres
-- - Apenas letras e números










