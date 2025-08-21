'use client'

import { useState, useEffect } from 'react'
import { DashboardLayout } from '@/components/layout/dashboard-layout'
import { ConversationsList } from '@/components/conversations/conversations-list'
import { ConversationFilters } from '@/components/conversations/conversation-filters'
import { api } from '@/lib/api'
import { Session, ConversationFilters as ConversationFiltersType } from '@/types'
import { LoadingSpinner } from '@/components/ui/loading-spinner'
import toast from 'react-hot-toast'

export default function ConversationsPage() {
  const [conversations, setConversations] = useState<Session[]>([])
  const [loading, setLoading] = useState(true)
  const [totalCount, setTotalCount] = useState(0)
  const [currentPage, setCurrentPage] = useState(1)
  const [filters, setFilters] = useState<ConversationFiltersType>({})

  useEffect(() => {
    loadConversations()
  }, [filters, currentPage])

  const loadConversations = async () => {
    try {
      setLoading(true)
      const response = await api.conversations({ ...filters, page: currentPage, limit: 20 })
      setConversations(response.data)
      setTotalCount(response.count)
    } catch (error) {
      console.error('Erro ao carregar conversas:', error)
      toast.error('Erro ao carregar conversas')
    } finally {
      setLoading(false)
    }
  }

  const handleFiltersChange = (newFilters: ConversationFiltersType) => {
    setFilters(newFilters)
    setCurrentPage(1)
  }

  const handleConversationUpdate = () => {
    loadConversations()
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Conversas</h1>
            <p className="text-gray-600">
              Acompanhe todas as conversas ativas e histórico de interações
            </p>
          </div>
        </div>

        {/* Filters */}
        <ConversationFilters
          filters={filters}
          onFiltersChange={handleFiltersChange}
          totalCount={totalCount}
        />

        {/* Content */}
        {loading ? (
          <div className="flex items-center justify-center h-64">
            <LoadingSpinner size="lg" />
          </div>
        ) : (
          <ConversationsList
            conversations={conversations}
            onConversationUpdate={handleConversationUpdate}
            totalCount={totalCount}
            currentPage={currentPage}
            onPageChange={setCurrentPage}
          />
        )}
      </div>
    </DashboardLayout>
  )
}




