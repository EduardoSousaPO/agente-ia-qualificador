'use client'

import { useState } from 'react'
import { Session } from '@/types'
import { formatDateTime, formatTimeAgo, getStatusColor, getStatusLabel, getInitials, getAvatarColor } from '@/lib/utils'
import { ChatBubbleLeftRightIcon, UserIcon, ComputerDesktopIcon } from '@heroicons/react/24/outline'
import Link from 'next/link'

interface ConversationsListProps {
  conversations: Session[]
  onConversationUpdate: () => void
  totalCount: number
  currentPage: number
  onPageChange: (page: number) => void
}

export function ConversationsList({ 
  conversations, 
  onConversationUpdate, 
  totalCount, 
  currentPage, 
  onPageChange 
}: ConversationsListProps) {
  const totalPages = Math.ceil(totalCount / 20)

  if (conversations.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="mx-auto h-12 w-12 text-gray-400">
          <ChatBubbleLeftRightIcon className="w-full h-full" />
        </div>
        <h3 className="mt-2 text-sm font-medium text-gray-900">Nenhuma conversa encontrada</h3>
        <p className="mt-1 text-sm text-gray-500">
          As conversas aparecerão aqui quando os leads começarem a interagir.
        </p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Conversations Grid */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {conversations.map((conversation) => (
          <Link
            key={conversation.id}
            href={`/conversations/${conversation.id}`}
            className="group relative bg-white p-6 rounded-lg shadow-sm border border-gray-200 hover:shadow-md hover:border-primary-300 transition-all duration-200"
          >
            {/* Header */}
            <div className="flex items-start justify-between">
              <div className="flex items-center space-x-3">
                <div className={`flex-shrink-0 h-10 w-10 rounded-full ${getAvatarColor(conversation.lead?.name || 'Unknown')} flex items-center justify-center`}>
                  <span className="text-sm font-medium text-white">
                    {getInitials(conversation.lead?.name || 'U')}
                  </span>
                </div>
                <div className="min-w-0 flex-1">
                  <p className="text-sm font-medium text-gray-900 truncate">
                    {conversation.lead?.name || 'Lead sem nome'}
                  </p>
                  <p className="text-sm text-gray-500 truncate">
                    {conversation.lead?.phone || 'Sem telefone'}
                  </p>
                </div>
              </div>
              
              <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(conversation.status)}`}>
                {getStatusLabel(conversation.status)}
              </span>
            </div>

            {/* Content */}
            <div className="mt-4 space-y-3">
              {/* Last Message */}
              {conversation.messages && conversation.messages.length > 0 && (
                <div className="flex items-start space-x-2">
                  <div className="flex-shrink-0 mt-0.5">
                    {conversation.messages[0].is_ai ? (
                      <ComputerDesktopIcon className="h-4 w-4 text-blue-500" />
                    ) : (
                      <UserIcon className="h-4 w-4 text-green-500" />
                    )}
                  </div>
                  <div className="min-w-0 flex-1">
                    <p className="text-sm text-gray-600 line-clamp-2">
                      {conversation.messages[0].content}
                    </p>
                  </div>
                </div>
              )}

              {/* Metadata */}
              <div className="flex items-center justify-between text-xs text-gray-500">
                <div className="flex items-center space-x-4">
                  {conversation.current_step && (
                    <span>Etapa: {conversation.current_step}</span>
                  )}
                  {conversation.human_takeover && (
                    <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-orange-100 text-orange-800">
                      Humano
                    </span>
                  )}
                </div>
                <span>{formatTimeAgo(conversation.updated_at)}</span>
              </div>

              {/* Progress */}
              {conversation.lead?.score !== undefined && (
                <div className="flex items-center space-x-2">
                  <div className="flex-1 bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-primary-600 h-2 rounded-full transition-all duration-300"
                      style={{ width: `${conversation.lead.score}%` }}
                    />
                  </div>
                  <span className="text-xs font-medium text-gray-600">
                    {conversation.lead.score}%
                  </span>
                </div>
              )}
            </div>

            {/* Hover Effect */}
            <div className="absolute inset-0 rounded-lg border-2 border-transparent group-hover:border-primary-200 pointer-events-none transition-colors duration-200" />
          </Link>
        ))}
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex items-center justify-between border-t border-gray-200 bg-white px-4 py-3 sm:px-6 rounded-lg">
          <div className="flex flex-1 justify-between sm:hidden">
            <button
              onClick={() => onPageChange(Math.max(1, currentPage - 1))}
              disabled={currentPage === 1}
              className="relative inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Anterior
            </button>
            <button
              onClick={() => onPageChange(Math.min(totalPages, currentPage + 1))}
              disabled={currentPage === totalPages}
              className="relative ml-3 inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Próximo
            </button>
          </div>
          
          <div className="hidden sm:flex sm:flex-1 sm:items-center sm:justify-between">
            <div>
              <p className="text-sm text-gray-700">
                Mostrando{' '}
                <span className="font-medium">{(currentPage - 1) * 20 + 1}</span>
                {' '}até{' '}
                <span className="font-medium">
                  {Math.min(currentPage * 20, totalCount)}
                </span>
                {' '}de{' '}
                <span className="font-medium">{totalCount}</span>
                {' '}conversas
              </p>
            </div>
            
            <div>
              <nav className="isolate inline-flex -space-x-px rounded-md shadow-sm" aria-label="Pagination">
                <button
                  onClick={() => onPageChange(Math.max(1, currentPage - 1))}
                  disabled={currentPage === 1}
                  className="relative inline-flex items-center rounded-l-md px-2 py-2 text-gray-400 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <span className="sr-only">Anterior</span>
                  <svg className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                    <path fillRule="evenodd" d="M12.79 5.23a.75.75 0 01-.02 1.06L8.832 10l3.938 3.71a.75.75 0 11-1.04 1.08l-4.5-4.25a.75.75 0 010-1.08l4.5-4.25a.75.75 0 011.06.02z" clipRule="evenodd" />
                  </svg>
                </button>
                
                {/* Page numbers */}
                {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                  const pageNum = Math.max(1, Math.min(totalPages - 4, currentPage - 2)) + i
                  if (pageNum > totalPages) return null
                  
                  return (
                    <button
                      key={pageNum}
                      onClick={() => onPageChange(pageNum)}
                      className={`relative inline-flex items-center px-4 py-2 text-sm font-semibold ${
                        pageNum === currentPage
                          ? 'z-10 bg-primary-600 text-white focus:z-20 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-600'
                          : 'text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0'
                      }`}
                    >
                      {pageNum}
                    </button>
                  )
                })}
                
                <button
                  onClick={() => onPageChange(Math.min(totalPages, currentPage + 1))}
                  disabled={currentPage === totalPages}
                  className="relative inline-flex items-center rounded-r-md px-2 py-2 text-gray-400 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <span className="sr-only">Próximo</span>
                  <svg className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                    <path fillRule="evenodd" d="M7.21 14.77a.75.75 0 01.02-1.06L11.168 10 7.23 6.29a.75.75 0 111.04-1.08l4.5 4.25a.75.75 0 010 1.08l-4.5 4.25a.75.75 0 01-1.06-.02z" clipRule="evenodd" />
                  </svg>
                </button>
              </nav>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}




