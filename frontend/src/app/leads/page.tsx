'use client'

import { useState, useEffect } from 'react'
import { DashboardLayout } from '@/components/layout/dashboard-layout'
import { LeadsList } from '@/components/leads/leads-list'
import { LeadsFilters } from '@/components/leads/leads-filters'
import { NewLeadModal } from '@/components/leads/new-lead-modal'
import { UploadCSVModal } from '@/components/leads/upload-csv-modal'
import { api } from '@/lib/api'
import { Lead, LeadFilters } from '@/types'
import { PlusIcon, DocumentArrowUpIcon } from '@heroicons/react/24/outline'
import { LoadingSpinner } from '@/components/ui/loading-spinner'
import toast from 'react-hot-toast'

export default function LeadsPage() {
  const [leads, setLeads] = useState<Lead[]>([])
  const [loading, setLoading] = useState(true)
  const [totalCount, setTotalCount] = useState(0)
  const [currentPage, setCurrentPage] = useState(1)
  const [filters, setFilters] = useState<LeadFilters>({})
  const [showNewLeadModal, setShowNewLeadModal] = useState(false)
  const [showUploadModal, setShowUploadModal] = useState(false)

  useEffect(() => {
    loadLeads()
  }, [filters, currentPage])

  const loadLeads = async () => {
    try {
      setLoading(true)
      const response = await api.leads({ ...filters, page: currentPage, limit: 20 })
      setLeads(response.data)
      setTotalCount(response.count)
    } catch (error) {
      console.error('Erro ao carregar leads:', error)
      toast.error('Erro ao carregar leads')
    } finally {
      setLoading(false)
    }
  }

  const handleFiltersChange = (newFilters: LeadFilters) => {
    setFilters(newFilters)
    setCurrentPage(1)
  }

  const handleLeadCreated = () => {
    setShowNewLeadModal(false)
    loadLeads()
    toast.success('Lead criado com sucesso!')
  }

  const handleUploadComplete = () => {
    setShowUploadModal(false)
    loadLeads()
  }

  const handleLeadUpdate = () => {
    loadLeads()
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Leads</h1>
            <p className="text-gray-600">
              Gerencie seus leads e acompanhe o progresso das qualificações
            </p>
          </div>
          
          <div className="flex space-x-3">
            <button
              onClick={() => setShowUploadModal(true)}
              className="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              <DocumentArrowUpIcon className="h-5 w-5 mr-2" />
              Upload CSV
            </button>
            
            <button
              onClick={() => setShowNewLeadModal(true)}
              className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              <PlusIcon className="h-5 w-5 mr-2" />
              Novo Lead
            </button>
          </div>
        </div>

        {/* Filters */}
        <LeadsFilters
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
          <LeadsList
            leads={leads}
            onLeadUpdate={handleLeadUpdate}
            totalCount={totalCount}
            currentPage={currentPage}
            onPageChange={setCurrentPage}
          />
        )}

        {/* Modals */}
        <NewLeadModal
          open={showNewLeadModal}
          onClose={() => setShowNewLeadModal(false)}
          onLeadCreated={handleLeadCreated}
        />

        <UploadCSVModal
          open={showUploadModal}
          onClose={() => setShowUploadModal(false)}
          onUploadComplete={handleUploadComplete}
        />
      </div>
    </DashboardLayout>
  )
}




