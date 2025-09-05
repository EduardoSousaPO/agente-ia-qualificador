'use client'

import { createContext, useContext, useEffect, useState } from 'react'
import { User } from '@/types'

interface AuthContextType {
  user: User | null
  loading: boolean
  signOut: () => Promise<void>
  refreshUser: () => Promise<void>
}

const AuthContext = createContext<AuthContextType>({
  user: null,
  loading: true,
  signOut: async () => {},
  refreshUser: async () => {},
})

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth deve ser usado dentro de um AuthProvider')
  }
  return context
}

function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  const refreshUser = async () => {
    try {
      // Verificação simples das variáveis de ambiente
      const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL
      const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY
      
      if (!supabaseUrl || !supabaseKey) {
        console.warn('Supabase não configurado - usando modo demo')
        setUser(null)
        setLoading(false)
        return
      }

      // Importação dinâmica para evitar erro de inicialização
      const { createClient } = await import('@/lib/supabase')
      const supabase = createClient()
      
      // Timeout para evitar travamento
      const sessionPromise = supabase.auth.getSession()
      const timeoutPromise = new Promise((_, reject) => 
        setTimeout(() => reject(new Error('Session timeout')), 3000)
      )
      
      const { data: { session }, error } = await Promise.race([sessionPromise, timeoutPromise]) as any
      
      if (error || !session?.user) {
        setUser(null)
        setLoading(false)
        return
      }
      
      // Criação dos dados do usuário
      const userData: User = {
        id: session.user.id,
        email: session.user.email || '',
        name: session.user.user_metadata?.full_name || session.user.email?.split('@')[0] || 'Usuário',
        role: 'admin',
        tenant: {
          id: '05dc8c52-c0a0-44ae-aa2a-eeaa01090a27',
          name: 'LDC Capital Investimentos',
          slug: 'ldc-capital'
        },
        created_at: session.user.created_at || new Date().toISOString()
      }

      setUser(userData)
    } catch (error) {
      console.warn('Erro na autenticação:', error)
      setUser(null)
    } finally {
      setLoading(false)
    }
  }

  const signOut = async () => {
    try {
      const { createClient } = await import('@/lib/supabase')
      const supabase = createClient()
      await supabase.auth.signOut()
    } catch (error) {
      console.warn('Erro no logout:', error)
    }
    
    setUser(null)
    localStorage.removeItem('demo_token')
    localStorage.removeItem('demo_user')
  }

  useEffect(() => {
    // Inicialização simplificada
    refreshUser()
  }, [])

  return (
    <AuthContext.Provider value={{ user, loading, signOut, refreshUser }}>
      {children}
    </AuthContext.Provider>
  )
}

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <AuthProvider>
      {children}
    </AuthProvider>
  )
}




