import { createBrowserClient, createServerClient } from '@supabase/ssr'
import { NextRequest, NextResponse } from 'next/server'

// Verificar se as variáveis de ambiente estão definidas
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!

if (!supabaseUrl) {
  throw new Error('NEXT_PUBLIC_SUPABASE_URL não está definida. Verifique o arquivo .env.local')
}

if (!supabaseAnonKey) {
  throw new Error('NEXT_PUBLIC_SUPABASE_ANON_KEY não está definida. Verifique o arquivo .env.local')
}

// Cliente para uso no browser (client-side)
export const createClient = () =>
  createBrowserClient(supabaseUrl, supabaseAnonKey)

// Cliente para Server Components
export const createServerComponentClient = () => {
  // Esta função só pode ser usada em Server Components
  const { cookies } = require('next/headers')
  
  return createServerClient(
    supabaseUrl,
    supabaseAnonKey,
    {
      cookies: {
        get(name: string) {
          return cookies().get(name)?.value
        },
      },
    }
  )
}

// Cliente para Route Handlers (API routes)
export const createRouteHandlerClient = (request: NextRequest, response: NextResponse) =>
  createServerClient(
    supabaseUrl,
    supabaseAnonKey,
    {
      cookies: {
        get(name: string) {
          return request.cookies.get(name)?.value
        },
        set(name: string, value: string, options: any) {
          request.cookies.set({ name, value, ...options })
          response.cookies.set({ name, value, ...options })
        },
        remove(name: string, options: any) {
          request.cookies.set({ name, value: '', ...options })
          response.cookies.set({ name, value: '', ...options })
        },
      },
    }
  )

// Cliente para Middleware
export const createMiddlewareClient = (request: NextRequest, response: NextResponse) =>
  createServerClient(
    supabaseUrl,
    supabaseAnonKey,
    {
      cookies: {
        get(name: string) {
          return request.cookies.get(name)?.value
        },
        set(name: string, value: string, options: any) {
          response.cookies.set({ name, value, ...options })
        },
        remove(name: string, options: any) {
          response.cookies.set({ name, value: '', ...options })
        },
      },
    }
  )

// Cliente padrão removido para evitar erro SSR
// export const supabase = createClient()

// Log para debug (apenas em desenvolvimento)
if (process.env.NODE_ENV === 'development') {
  console.log('🔗 Supabase URL:', supabaseUrl)
  console.log('🔑 Supabase Key:', supabaseAnonKey.substring(0, 20) + '...')
}