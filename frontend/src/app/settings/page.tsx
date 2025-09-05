'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/components/providers'

export default function SettingsRedirectPage() {
  const router = useRouter()
  const { user } = useAuth()

  useEffect(() => {
    // Redirecionar para configurações do tenant se o usuário estiver logado
    if (user?.tenant?.slug) {
      router.replace(`/app/${user.tenant.slug}/settings`)
    } else {
      // Fallback para configurações gerais
      router.replace('/dashboard')
    }
  }, [user, router])

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="text-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto"></div>
        <p className="mt-4 text-gray-600">Redirecionando para configurações...</p>
      </div>
    </div>
  )
}










