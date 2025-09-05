'use client'

import { useTenant } from '@/hooks/useTenant'
import { ConversationsTable } from '@/components/conversations/conversations-table'
import { ConversationsFilters } from '@/components/conversations/conversations-filters'
import { ConversationsStats } from '@/components/conversations/conversations-stats'
import { useState, useEffect } from 'react'
import { api } from '@/lib/api'
import { Session, ConversationFilters } from '@/types'
import { LoadingSpinner } from '@/components/ui/loading-spinner'

export default function TenantConversations() {
  const { currentTenant, loading: tenantLoading } = useTenant()
  const [conversations, setConversations] = useState<Session[]>([])
  const [filters, setFilters] = useState<ConversationFilters>({})
  const [loading, setLoading] = useState(true)
  const [pagination, setPagination] = useState({
    page: 1,
    limit: 20,
    total: 0,
    totalPages: 0
  })

  useEffect(() => {
    if (currentTenant) {
      loadConversations()
    }
  }, [currentTenant, filters])

  const loadConversations = async () => {
    try {
      setLoading(true)
      const response = await api.conversations({
        ...filters,
        page: pagination.page,
        limit: pagination.limit
      })
      
      setConversations(response.data)
      setPagination({
        page: response.page,
        limit: response.limit,
        total: response.total,
        totalPages: response.totalPages
      })
    } catch (error) {
      console.error('Erro ao carregar conversas:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleFilterChange = (newFilters: ConversationFilters) => {
    setFilters(newFilters)
    setPagination(prev => ({ ...prev, page: 1 }))
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
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Conversas</h1>
        <p className="text-gray-600 mt-1">
          Acompanhe as conversas de {currentTenant.name}
        </p>
      </div>

      {/* Stats */}
      <ConversationsStats />

      {/* Filters */}
      <ConversationsFilters 
        filters={filters}
        onFiltersChange={handleFilterChange}
      />

      {/* Table */}
      <ConversationsTable
        conversations={conversations}
        pagination={pagination}
        onPageChange={(page) => setPagination(prev => ({ ...prev, page }))}
        tenantSlug={currentTenant.slug}
      />
    </div>
  )
}











