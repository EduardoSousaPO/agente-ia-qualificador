/**
 * Utilitários de autenticação
 * Versão simplificada para compatibilidade
 */

export interface AuthHeaders {
  'Content-Type': string
  'Authorization'?: string
  [key: string]: string | undefined
}

/**
 * Obter headers de autenticação para requisições API
 * Por enquanto usa um token demo, mas pode ser expandido para JWT real
 */
export function getAuthHeaders(): Record<string, string> {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json'
  }

  // Verificar se há token no localStorage (sistema demo)
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('auth_token') || localStorage.getItem('demo_token')
    
    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }
  }

  return headers
}

/**
 * Verificar se o usuário está autenticado
 */
export function isAuthenticated(): boolean {
  if (typeof window === 'undefined') return false
  
  const token = localStorage.getItem('auth_token') || localStorage.getItem('demo_token')
  return !!token
}

/**
 * Obter dados do usuário do localStorage
 */
export function getCurrentUser() {
  if (typeof window === 'undefined') return null
  
  const userData = localStorage.getItem('user_data') || localStorage.getItem('demo_user')
  
  if (userData) {
    try {
      return JSON.parse(userData)
    } catch (error) {
      console.error('Erro ao parsear dados do usuário:', error)
      return null
    }
  }
  
  return null
}

/**
 * Fazer logout
 */
export function logout() {
  if (typeof window === 'undefined') return
  
  localStorage.removeItem('auth_token')
  localStorage.removeItem('demo_token')
  localStorage.removeItem('user_data')
  localStorage.removeItem('demo_user')
  
  // Redirecionar para login
  window.location.href = '/login'
}

/**
 * Salvar token de autenticação
 */
export function saveAuthToken(token: string) {
  if (typeof window === 'undefined') return
  
  localStorage.setItem('auth_token', token)
}

/**
 * Salvar dados do usuário
 */
export function saveUserData(userData: any) {
  if (typeof window === 'undefined') return
  
  localStorage.setItem('user_data', JSON.stringify(userData))
}

/**
 * Obter tenant ID do usuário atual
 */
export function getCurrentTenantId(): string | null {
  const user = getCurrentUser()
  return user?.tenant_id || null
}

/**
 * Verificar se o usuário tem uma role específica
 */
export function hasRole(role: string): boolean {
  const user = getCurrentUser()
  return user?.role === role
}

/**
 * Verificar se o usuário é admin
 */
export function isAdmin(): boolean {
  return hasRole('admin')
}
