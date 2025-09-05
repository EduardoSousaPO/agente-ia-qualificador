'use client'

import { useAuth } from '@/components/providers'
import { useRouter } from 'next/navigation'
import { useEffect, useState } from 'react'

// Landing Page Components - Simplified
import { HeroSection } from '@/components/landing/hero-section'
import { WhyUseSection } from '@/components/landing/why-use-section'
import { HowItWorksSimple } from '@/components/landing/how-it-works'
import { CTASection } from '@/components/landing/cta-section'

export default function HomePage() {
  const { user, loading } = useAuth()
  const router = useRouter()
  const [shouldRedirect, setShouldRedirect] = useState(false)
  const [isHydrated, setIsHydrated] = useState(false)

  useEffect(() => {
    setIsHydrated(true)
    
    // Redirecionar usuários autenticados diretamente para o dashboard
    if (user && !loading) {
      setShouldRedirect(true)
      console.log('Usuário logado, redirecionando para dashboard...')
      router.replace('/dashboard')
    }
  }, [user, loading, router])

  // Show loading during hydration
  if (!isHydrated) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Inicializando sistema...</p>
        </div>
      </div>
    )
  }

  // Show loading only when redirecting authenticated users
  if (shouldRedirect) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Redirecionando para seu dashboard...</p>
        </div>
      </div>
    )
  }

  // Show landing page for non-authenticated users or during initial load
  return (
    <div className="min-h-screen">
      <HeroSection />
      <WhyUseSection />
      <HowItWorksSimple />
      <CTASection />
    </div>
  )
}