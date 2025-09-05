-- Multi-Tenant B2B Foundation Migration
-- Implementa especificação completa: profiles, memberships, invites, RLS

-- ===============================
-- 1. ESTRUTURAS CORE MULTI-TENANT
-- ===============================

-- Profiles (vincula auth.users com sistema)
create table if not exists public.profiles (
  user_id uuid primary key references auth.users(id) on delete cascade,
  default_tenant_id uuid references public.tenants(id),
  created_at timestamptz not null default now()
);

-- Memberships (many-to-many users/tenants)
create table if not exists public.memberships (
  tenant_id uuid not null references public.tenants(id) on delete cascade,
  user_id uuid not null references auth.users(id) on delete cascade,
  role text not null check (role in ('owner','admin','member')),
  created_at timestamptz not null default now(),
  primary key (tenant_id, user_id)
);

-- Invites (sistema de convites Slack-like)
create table if not exists public.invites (
  id uuid primary key default gen_random_uuid(),
  tenant_id uuid not null references public.tenants(id) on delete cascade,
  email text not null,
  role text not null check (role in ('admin','member')),
  status text not null default 'pending' check (status in ('pending','accepted','revoked')),
  created_at timestamptz not null default now(),
  unique (tenant_id, email)
);

-- ===============================
-- 2. FUNÇÃO HELPER is_member
-- ===============================

create or replace function public.is_member(target_tenant uuid)
returns boolean language sql stable as $$
  select exists(
    select 1 from public.memberships m
    where m.tenant_id = target_tenant and m.user_id = auth.uid()
  );
$$;

-- ===============================
-- 3. HABILITAR RLS
-- ===============================

-- Habilitar RLS nas novas tabelas
alter table public.profiles enable row level security;
alter table public.memberships enable row level security;
alter table public.invites enable row level security;

-- Garantir que tenants já tem RLS habilitado
alter table public.tenants enable row level security;

-- ===============================
-- 4. POLICIES RLS ESSENCIAIS
-- ===============================

-- Tenants: usuário vê apenas tenants onde é membro
drop policy if exists "tenant_select" on public.tenants;
create policy "tenant_select" on public.tenants 
  for select using (public.is_member(id));

drop policy if exists "tenant_update" on public.tenants 
  for update using (public.is_member(id)) with check (public.is_member(id));
create policy "tenant_update" on public.tenants 
  for update using (public.is_member(id)) with check (public.is_member(id));

-- Profiles: usuário vê apenas seu próprio profile
drop policy if exists "profiles_self" on public.profiles;
create policy "profiles_self" on public.profiles 
  for select using (user_id = auth.uid());

drop policy if exists "profiles_self_upd" on public.profiles;
create policy "profiles_self_upd" on public.profiles 
  for update using (user_id = auth.uid()) with check (user_id = auth.uid());

drop policy if exists "profiles_self_ins" on public.profiles;
create policy "profiles_self_ins" on public.profiles 
  for insert with check (user_id = auth.uid());

-- Memberships: usuário vê memberships dos tenants onde é membro
drop policy if exists "memb_select" on public.memberships;
create policy "memb_select" on public.memberships 
  for select using (public.is_member(tenant_id));

drop policy if exists "memb_insert" on public.memberships;
create policy "memb_insert" on public.memberships 
  for insert with check (public.is_member(tenant_id));

-- Invites: usuário vê invites dos tenants onde é membro
drop policy if exists "inv_select" on public.invites;
create policy "inv_select" on public.invites 
  for select using (public.is_member(tenant_id));

drop policy if exists "inv_insert" on public.invites;
create policy "inv_insert" on public.invites 
  for insert with check (public.is_member(tenant_id));

drop policy if exists "inv_update" on public.invites;
create policy "inv_update" on public.invites 
  for update using (public.is_member(tenant_id)) with check (public.is_member(tenant_id));

-- ===============================
-- 5. TRIGGER AUTO-MEMBERSHIP
-- ===============================

create or replace function public.auto_membership_from_invite()
returns trigger language plpgsql as $$
declare 
  v_inv public.invites;
begin
  -- Buscar invite pendente para o email do novo usuário
  select * into v_inv
  from public.invites
  where lower(email) = lower(new.email) and status = 'pending'
  order by created_at desc limit 1;

  if found then
    -- Criar profile se não existir
    insert into public.profiles (user_id) 
    values (new.id)
    on conflict (user_id) do nothing;

    -- Criar membership
    insert into public.memberships (tenant_id, user_id, role)
    values (v_inv.tenant_id, new.id, v_inv.role)
    on conflict do nothing;

    -- Marcar invite como aceito
    update public.invites 
    set status = 'accepted' 
    where id = v_inv.id;
  end if;
  
  return new;
end; 
$$;

-- Remover trigger existente se houver
drop trigger if exists on_auth_user_created on auth.users;

-- Criar trigger para auto-membership
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.auto_membership_from_invite();

-- ===============================
-- 6. ATUALIZAR RLS DAS TABELAS EXISTENTES
-- ===============================

-- Atualizar policies das tabelas de domínio para usar is_member()
-- (mantém compatibilidade com tenant_id existente)

-- LEADS
drop policy if exists "leads_select" on public.leads;
create policy "leads_select" on public.leads 
  for select using (public.is_member(tenant_id));

drop policy if exists "leads_insert" on public.leads;
create policy "leads_insert" on public.leads 
  for insert with check (public.is_member(tenant_id));

drop policy if exists "leads_update" on public.leads;
create policy "leads_update" on public.leads 
  for update using (public.is_member(tenant_id)) with check (public.is_member(tenant_id));

drop policy if exists "leads_delete" on public.leads;
create policy "leads_delete" on public.leads 
  for delete using (public.is_member(tenant_id));

-- SESSIONS (via leads.tenant_id)
drop policy if exists "sessions_select" on public.sessions;
create policy "sessions_select" on public.sessions 
  for select using (
    exists(
      select 1 from public.leads l 
      where l.id = lead_id and public.is_member(l.tenant_id)
    )
  );

drop policy if exists "sessions_insert" on public.sessions;
create policy "sessions_insert" on public.sessions 
  for insert with check (
    exists(
      select 1 from public.leads l 
      where l.id = lead_id and public.is_member(l.tenant_id)
    )
  );

drop policy if exists "sessions_update" on public.sessions;
create policy "sessions_update" on public.sessions 
  for update using (
    exists(
      select 1 from public.leads l 
      where l.id = lead_id and public.is_member(l.tenant_id)
    )
  ) with check (
    exists(
      select 1 from public.leads l 
      where l.id = lead_id and public.is_member(l.tenant_id)
    )
  );

drop policy if exists "sessions_delete" on public.sessions;
create policy "sessions_delete" on public.sessions 
  for delete using (
    exists(
      select 1 from public.leads l 
      where l.id = lead_id and public.is_member(l.tenant_id)
    )
  );

-- MESSAGES (via sessions -> leads.tenant_id)
drop policy if exists "messages_select" on public.messages;
create policy "messages_select" on public.messages 
  for select using (
    exists(
      select 1 from public.sessions s
      join public.leads l on s.lead_id = l.id
      where s.id = session_id and public.is_member(l.tenant_id)
    )
  );

drop policy if exists "messages_insert" on public.messages;
create policy "messages_insert" on public.messages 
  for insert with check (
    exists(
      select 1 from public.sessions s
      join public.leads l on s.lead_id = l.id
      where s.id = session_id and public.is_member(l.tenant_id)
    )
  );

-- QUALIFICACOES
drop policy if exists "qualificacoes_select" on public.qualificacoes;
create policy "qualificacoes_select" on public.qualificacoes 
  for select using (
    exists(
      select 1 from public.leads l 
      where l.id = lead_id and public.is_member(l.tenant_id)
    )
  );

drop policy if exists "qualificacoes_insert" on public.qualificacoes;
create policy "qualificacoes_insert" on public.qualificacoes 
  for insert with check (
    exists(
      select 1 from public.leads l 
      where l.id = lead_id and public.is_member(l.tenant_id)
    )
  );

drop policy if exists "qualificacoes_update" on public.qualificacoes;
create policy "qualificacoes_update" on public.qualificacoes 
  for update using (
    exists(
      select 1 from public.leads l 
      where l.id = lead_id and public.is_member(l.tenant_id)
    )
  ) with check (
    exists(
      select 1 from public.leads l 
      where l.id = lead_id and public.is_member(l.tenant_id)
    )
  );

-- MEETINGS
drop policy if exists "meetings_select" on public.meetings;
create policy "meetings_select" on public.meetings 
  for select using (
    exists(
      select 1 from public.leads l 
      where l.id = lead_id and public.is_member(l.tenant_id)
    )
  );

drop policy if exists "meetings_insert" on public.meetings;
create policy "meetings_insert" on public.meetings 
  for insert with check (
    exists(
      select 1 from public.leads l 
      where l.id = lead_id and public.is_member(l.tenant_id)
    )
  );

drop policy if exists "meetings_update" on public.meetings;
create policy "meetings_update" on public.meetings 
  for update using (
    exists(
      select 1 from public.leads l 
      where l.id = lead_id and public.is_member(l.tenant_id)
    )
  ) with check (
    exists(
      select 1 from public.leads l 
      where l.id = lead_id and public.is_member(l.tenant_id)
    )
  );

-- AUDIT_EVENTS
drop policy if exists "audit_events_select" on public.audit_events;
create policy "audit_events_select" on public.audit_events 
  for select using (public.is_member(tenant_id));

drop policy if exists "audit_events_insert" on public.audit_events;
create policy "audit_events_insert" on public.audit_events 
  for insert with check (public.is_member(tenant_id));

-- ===============================
-- 7. ADICIONAR SLUG PARA TENANTS
-- ===============================

-- Adicionar coluna slug se não existir
alter table public.tenants add column if not exists slug text;

-- Criar índice único para slug
drop index if exists tenants_slug_unique;
create unique index tenants_slug_unique on public.tenants (slug) where slug is not null;

-- ===============================
-- 8. COMENTÁRIOS INFORMATIVOS
-- ===============================

comment on table public.profiles is 'Vincula auth.users com sistema multi-tenant';
comment on table public.memberships is 'Many-to-many: usuários podem pertencer a múltiplos tenants';
comment on table public.invites is 'Sistema de convites estilo Slack';
comment on function public.is_member(uuid) is 'Helper function para RLS: verifica se user é membro do tenant';
comment on function public.auto_membership_from_invite() is 'Trigger: aceita convite automaticamente quando usuário se cadastra';

-- Migration concluída
select 'Multi-tenant foundation migration completed successfully' as status;











