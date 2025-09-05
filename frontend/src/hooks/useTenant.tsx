'use client'

import React, { useState, useEffect, createContext, useContext } from 'react'
import { useParams, useRouter } from 'next/navigation'
import { api } from '@/lib/api'
import toast from 'react-hot-toast'

export interface Tenant {
  id: string
  name: string
  slug: string
  domain?: string
  settings: Record<string, any>
  created_at: string
  updated_at: string
}

export interface Membership {
  tenant_id: string
  user_id: string
  role: 'owner' | 'admin' | 'member'
  created_at: string
  tenant: Tenant
}

interface TenantContextType {
  currentTenant: Tenant | null
  tenantSlug: string | null
  memberships: Membership[]
  loading: boolean
  switchTenant: (slug: string) => void
  refreshTenant: () => Promise<void>
}

const TenantContext = createContext<TenantContextType | undefined>(undefined)

interface TenantProviderProps {
  children: React.ReactNode
}

export function TenantProvider({ children }: TenantProviderProps) {
  const [currentTenant, setCurrentTenant] = useState<Tenant | null>(null)
  const [memberships, setMemberships] = useState<Membership[]>([])
  const [loading, setLoading] = useState(true)
  const params = useParams()
  const router = useRouter()

  const tenantSlug = (params?.tenantSlug as string) || null

  const refreshTenant = async () => {
    if (!tenantSlug) {
      setLoading(false)
      return
    }

    try {
      setLoading(true)
      const response = await api.tenant(tenantSlug)
      
      if (response.success) {
        setCurrentTenant(response.tenant)
        setMemberships(response.memberships || [])
      } else {
        toast.error('Tenant não encontrado ou acesso negado')
        router.push('/')
      }
    } catch (error) {
      console.error('Erro ao carregar tenant:', error)
      toast.error('Erro ao carregar dados do tenant')
      router.push('/')
    } finally {
      setLoading(false)
    }
  }

  const switchTenant = (slug: string) => {
    if (slug === tenantSlug) return
    router.push(`/app/${slug}/dashboard`)
  }

  useEffect(() => {
    refreshTenant()
  }, [tenantSlug])

  const value = {
    currentTenant,
    tenantSlug,
    memberships,
    loading,
    switchTenant,
    refreshTenant,
  }

  return (
    <TenantContext.Provider value={value}>
      {children}
    </TenantContext.Provider>
  )
}

export function useTenant() {
  const context = useContext(TenantContext)
  if (context === undefined) {
    throw new Error('useTenant must be used within a TenantProvider')
  }
  return context
}











