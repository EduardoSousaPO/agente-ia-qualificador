'use client'

import { ConversationFilters } from '@/types'
import { useState } from 'react'

interface ConversationsFiltersProps {
  filters: ConversationFilters
  onFiltersChange: (filters: ConversationFilters) => void
}

export function ConversationsFilters({ filters, onFiltersChange }: ConversationsFiltersProps) {
  const [localFilters, setLocalFilters] = useState<ConversationFilters>(filters)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onFiltersChange(localFilters)
  }

  const handleReset = () => {
    const resetFilters: ConversationFilters = {}
    setLocalFilters(resetFilters)
    onFiltersChange(resetFilters)
  }

  return (
    <div className="bg-white shadow rounded-lg">
      <div className="px-4 py-5 sm:p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Filtros</h3>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Status Filter */}
            <div>
              <label htmlFor="status" className="block text-sm font-medium text-gray-700">
                Status
              </label>
              <select
                id="status"
                value={localFilters.status || ''}
                onChange={(e) => setLocalFilters({ ...localFilters, status: e.target.value || undefined })}
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">Todos os status</option>
                <option value="active">Ativo</option>
                <option value="completed">Concluído</option>
                <option value="abandoned">Abandonado</option>
              </select>
            </div>

            {/* Date Range */}
            <div>
              <label htmlFor="dateFrom" className="block text-sm font-medium text-gray-700">
                Data Inicial
              </label>
              <input
                type="date"
                id="dateFrom"
                value={localFilters.dateFrom || ''}
                onChange={(e) => setLocalFilters({ ...localFilters, dateFrom: e.target.value || undefined })}
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            <div>
              <label htmlFor="dateTo" className="block text-sm font-medium text-gray-700">
                Data Final
              </label>
              <input
                type="date"
                id="dateTo"
                value={localFilters.dateTo || ''}
                onChange={(e) => setLocalFilters({ ...localFilters, dateTo: e.target.value || undefined })}
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
          </div>

          <div className="flex justify-end space-x-3">
            <button
              type="button"
              onClick={handleReset}
              className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
            >
              Limpar
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-blue-600 border border-transparent rounded-md text-sm font-medium text-white hover:bg-blue-700"
            >
              Aplicar Filtros
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}











