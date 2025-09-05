'use client'

import { useTenant } from '@/hooks/useTenant'
import { LeadsTable } from '@/components/leads/leads-table'
import { LeadsStats } from '@/components/leads/leads-stats'
import { useState, useEffect } from 'react'
import { api } from '@/lib/api'
import { Lead, LeadFilters } from '@/types'
import { LoadingSpinner } from '@/components/ui/loading-spinner'
import { PlusIcon } from '@heroicons/react/24/outline'

export default function TenantLeads() {
  const { currentTenant, loading: tenantLoading } = useTenant()
  const [leads, setLeads] = useState<Lead[]>([])
  const [loading, setLoading] = useState(true)
  const [pagination, setPagination] = useState({
    page: 1,
    limit: 20,
    total: 0,
    totalPages: 0
  })

  useEffect(() => {
    if (currentTenant) {
      loadLeads()
    }
  }, [currentTenant])

  const loadLeads = async () => {
    try {
      setLoading(true)
      // Simulando dados para não quebrar
      const mockLeads: Lead[] = [
        {
          id: '1',
          tenant_id: currentTenant?.id || '',
          name: 'João Silva',
          email: 'joao@exemplo.com',
          phone: '+5511999999999',
          origem: 'website',
          inserido_manual: false,
          tags: ['interessado'],
          status: 'new',
          score: 75,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString()
        }
      ]
      
      setLeads(mockLeads)
      setPagination({
        page: 1,
        limit: 20,
        total: mockLeads.length,
        totalPages: 1
      })
    } catch (error) {
      console.error('Erro ao carregar leads:', error)
    } finally {
      setLoading(false)
    }
  }

  if (tenantLoading || loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <LoadingSpinner size="lg" />
      </div>
    )
  }

  if (!currentTenant) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <h2 className="text-xl font-semibold text-gray-900 mb-2">
            Tenant não encontrado
          </h2>
          <p className="text-gray-600">
            Verifique se você tem acesso a este tenant.
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Leads</h1>
          <p className="text-gray-600 mt-1">
            Gerencie os leads de {currentTenant.name}
          </p>
        </div>
        <button
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center gap-2"
        >
          <PlusIcon className="h-4 w-4" />
          Novo Lead
        </button>
      </div>

      {/* Stats */}
      <LeadsStats />

      {/* Table */}
      <LeadsTable
        leads={leads}
        pagination={pagination}
        onPageChange={(page) => setPagination(prev => ({ ...prev, page }))}
        tenantSlug={currentTenant.slug}
      />
    </div>
  )
}
