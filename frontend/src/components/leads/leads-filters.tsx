'use client'

import { useState } from 'react'
import { LeadFilters } from '@/types'
import { MagnifyingGlassIcon, FunnelIcon } from '@heroicons/react/24/outline'
import { debounce } from '@/lib/utils'

interface LeadsFiltersProps {
  filters: LeadFilters
  onFiltersChange: (filters: LeadFilters) => void
  totalCount: number
}

export function LeadsFilters({ filters, onFiltersChange, totalCount }: LeadsFiltersProps) {
  const [searchTerm, setSearchTerm] = useState(filters.search || '')
  const [showAdvanced, setShowAdvanced] = useState(false)

  // Debounced search
  const debouncedSearch = debounce((term: string) => {
    onFiltersChange({ ...filters, search: term || undefined })
  }, 300)

  const handleSearchChange = (value: string) => {
    setSearchTerm(value)
    debouncedSearch(value)
  }

  const handleFilterChange = (key: keyof LeadFilters, value: any) => {
    onFiltersChange({
      ...filters,
      [key]: value || undefined
    })
  }

  const clearFilters = () => {
    setSearchTerm('')
    onFiltersChange({})
  }

  const hasActiveFilters = Object.values(filters).some(value => value !== undefined && value !== '')

  return (
    <div className="bg-white shadow-sm rounded-lg p-6 space-y-4">
      {/* Search Bar */}
      <div className="flex items-center space-x-4">
        <div className="flex-1 relative">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <MagnifyingGlassIcon className="h-5 w-5 text-gray-400" />
          </div>
          <input
            type="text"
            placeholder="Buscar por nome, telefone ou email..."
            value={searchTerm}
            onChange={(e) => handleSearchChange(e.target.value)}
            className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-primary-500 focus:border-primary-500"
          />
        </div>
        
        <button
          onClick={() => setShowAdvanced(!showAdvanced)}
          className={`inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-lg text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 ${
            showAdvanced ? 'ring-2 ring-primary-500 border-primary-500' : ''
          }`}
        >
          <FunnelIcon className="h-5 w-5 mr-2" />
          Filtros
          {hasActiveFilters && (
            <span className="ml-2 inline-flex items-center justify-center px-2 py-1 text-xs font-bold leading-none text-white bg-primary-600 rounded-full">
              {Object.values(filters).filter(v => v !== undefined && v !== '').length}
            </span>
          )}
        </button>
      </div>

      {/* Advanced Filters */}
      {showAdvanced && (
        <div className="border-t pt-4 space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {/* Status Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Status
              </label>
              <select
                value={filters.status || ''}
                onChange={(e) => handleFilterChange('status', e.target.value)}
                className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 text-sm"
              >
                <option value="">Todos os status</option>
                <option value="novo">Novo</option>
                <option value="em_conversa">Em Conversa</option>
                <option value="qualificado">Qualificado</option>
                <option value="desqualificado">Desqualificado</option>
              </select>
            </div>

            {/* Origem Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Origem
              </label>
              <select
                value={filters.origem || ''}
                onChange={(e) => handleFilterChange('origem', e.target.value)}
                className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 text-sm"
              >
                <option value="">Todas as origens</option>
                <option value="youtube">YouTube</option>
                <option value="newsletter">Newsletter</option>
                <option value="manual">Manual</option>
                <option value="inbound_whatsapp">Inbound WhatsApp</option>
                <option value="upload_csv">Upload CSV</option>
                <option value="external">Externa</option>
              </select>
            </div>

            {/* Inserção Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Tipo de Inserção
              </label>
              <select
                value={filters.inserido_manual === undefined ? '' : filters.inserido_manual ? 'true' : 'false'}
                onChange={(e) => handleFilterChange('inserido_manual', e.target.value === '' ? undefined : e.target.value === 'true')}
                className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 text-sm"
              >
                <option value="">Todos os tipos</option>
                <option value="true">Manual</option>
                <option value="false">Automático</option>
              </select>
            </div>

            {/* Clear Filters */}
            <div className="flex items-end">
              <button
                onClick={clearFilters}
                disabled={!hasActiveFilters}
                className="w-full inline-flex items-center justify-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Limpar Filtros
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Results Count */}
      <div className="flex items-center justify-between text-sm text-gray-600">
        <span>
          {totalCount} lead{totalCount !== 1 ? 's' : ''} encontrado{totalCount !== 1 ? 's' : ''}
          {hasActiveFilters && ' (filtrado)'}
        </span>
        
        {hasActiveFilters && (
          <button
            onClick={clearFilters}
            className="text-primary-600 hover:text-primary-700 font-medium"
          >
            Limpar todos os filtros
          </button>
        )}
      </div>
    </div>
  )
}




