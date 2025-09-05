'use client'

import { useState } from 'react'
import type { ConversationFilters } from '@/types'
import { MagnifyingGlassIcon, FunnelIcon } from '@heroicons/react/24/outline'
import { debounce } from '@/lib/utils'

interface ConversationFiltersProps {
  filters: ConversationFilters
  onFiltersChange: (filters: ConversationFilters) => void
  totalCount: number
}

export function ConversationFilters({ filters, onFiltersChange, totalCount }: ConversationFiltersProps) {
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

  const handleFilterChange = (key: keyof ConversationFilters, value: any) => {
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
            placeholder="Buscar por nome do lead, telefone ou mensagem..."
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
                Status da Sessão
              </label>
              <select
                value={filters.status || ''}
                onChange={(e) => handleFilterChange('status', e.target.value)}
                className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 text-sm"
              >
                <option value="">Todos os status</option>
                <option value="ativa">Ativa</option>
                <option value="pausada">Pausada</option>
                <option value="finalizada">Finalizada</option>
              </select>
            </div>

            {/* Human Takeover Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Controle
              </label>
              <select
                value={filters.human_takeover === undefined ? '' : filters.human_takeover ? 'true' : 'false'}
                onChange={(e) => handleFilterChange('human_takeover', e.target.value === '' ? undefined : e.target.value === 'true')}
                className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 text-sm"
              >
                <option value="">Todos</option>
                <option value="false">IA</option>
                <option value="true">Humano</option>
              </select>
            </div>

            {/* Current Step Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Etapa Atual
              </label>
              <select
                value={filters.current_step || ''}
                onChange={(e) => handleFilterChange('current_step', e.target.value)}
                className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 text-sm"
              >
                <option value="">Todas as etapas</option>
                <option value="apresentacao">Apresentação</option>
                <option value="descoberta_investimento">Descoberta de Investimento</option>
                <option value="patrimonio">Patrimônio</option>
                <option value="objetivo">Objetivo</option>
                <option value="urgencia">Urgência</option>
                <option value="interesse_especialista">Interesse em Especialista</option>
                <option value="qualificado">Qualificado</option>
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

          {/* Date Range */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Criado Após
              </label>
              <input
                type="date"
                value={filters.created_after || ''}
                onChange={(e) => handleFilterChange('created_after', e.target.value)}
                className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 text-sm"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Criado Antes
              </label>
              <input
                type="date"
                value={filters.created_before || ''}
                onChange={(e) => handleFilterChange('created_before', e.target.value)}
                className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 text-sm"
              />
            </div>
          </div>
        </div>
      )}

      {/* Results Count */}
      <div className="flex items-center justify-between text-sm text-gray-600">
        <span>
          {totalCount} conversa{totalCount !== 1 ? 's' : ''} encontrada{totalCount !== 1 ? 's' : ''}
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




