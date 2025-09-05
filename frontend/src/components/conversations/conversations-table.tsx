'use client'

import { Session } from '@/types'

interface ConversationsTableProps {
  conversations: Session[]
  pagination: {
    page: number
    limit: number
    total: number
    totalPages: number
  }
  onPageChange: (page: number) => void
  tenantSlug: string
}

export function ConversationsTable({ 
  conversations, 
  pagination, 
  onPageChange,
  tenantSlug 
}: ConversationsTableProps) {
  return (
    <div className="bg-white shadow rounded-lg overflow-hidden">
      <div className="px-4 py-5 sm:p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">
          Conversas ({pagination.total})
        </h3>
        
        {conversations.length === 0 ? (
          <div className="text-center py-8">
            <p className="text-gray-500">Nenhuma conversa encontrada</p>
          </div>
        ) : (
          <div className="space-y-4">
            {conversations.map((conversation) => (
              <div 
                key={conversation.id} 
                className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50"
              >
                <div className="flex justify-between items-start">
                  <div>
                    <h4 className="font-medium text-gray-900">
                      Conversa #{conversation.id.slice(0, 8)}
                    </h4>
                    <p className="text-sm text-gray-600 mt-1">
                      Status: {conversation.status}
                    </p>
                    <p className="text-sm text-gray-500 mt-1">
                      {new Date(conversation.created_at).toLocaleDateString('pt-BR')}
                    </p>
                  </div>
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                    {conversation.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
        
        {/* Pagination */}
        {pagination.totalPages > 1 && (
          <div className="flex justify-between items-center mt-6">
            <div className="text-sm text-gray-700">
              Página {pagination.page} de {pagination.totalPages}
            </div>
            <div className="flex space-x-2">
              <button
                onClick={() => onPageChange(pagination.page - 1)}
                disabled={pagination.page === 1}
                className="px-3 py-1 border border-gray-300 rounded text-sm disabled:opacity-50"
              >
                Anterior
              </button>
              <button
                onClick={() => onPageChange(pagination.page + 1)}
                disabled={pagination.page === pagination.totalPages}
                className="px-3 py-1 border border-gray-300 rounded text-sm disabled:opacity-50"
              >
                Próxima
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}











