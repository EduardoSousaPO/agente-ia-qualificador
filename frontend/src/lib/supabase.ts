import { createClient as createSupabaseClient } from '@supabase/supabase-js'

// Configuração do Supabase
export const supabaseConfig = {
  url: process.env.NEXT_PUBLIC_SUPABASE_URL!,
  anonKey: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
}

// Cliente simples para uso geral
export const createClient = () => 
  createSupabaseClient(supabaseConfig.url, supabaseConfig.anonKey)

// Cliente padrão
export const supabase = createClient()