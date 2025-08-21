'use client'

import { useEffect, useState } from 'react'
import { api } from '@/lib/api'
import { Lead } from '@/types'
import { formatTimeAgo } from '@/lib/utils'
import { ChatBubbleLeftRightIcon } from '@heroicons/react/24/outline'
import Link from 'next/link'

export function ActiveConversations() {
  const [activeLeads, setActiveLeads] = useState<Lead[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadActiveConversations()
  }, [])

  const loadActiveConversations = async () => {
    try {
      const response = await api.leads({ status: 'em_conversa', limit: 5 })
      setActiveLeads(response.data)
    } catch (error) {
      console.error('Erro ao carregar conversas ativas:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="animate-pulse space-y-4">
        {[...Array(3)].map((_, i) => (
          <div key={i} className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-gray-200 rounded-full" />
            <div className="flex-1 space-y-1">
              <div className="h-4 bg-gray-200 rounded w-3/4" />
              <div className="h-3 bg-gray-200 rounded w-1/2" />
            </div>
          </div>
        ))}
      </div>
    )
  }

  if (activeLeads.length === 0) {
    return (
      <div className="text-center py-8">
        <ChatBubbleLeftRightIcon className="mx-auto h-12 w-12 text-gray-400" />
        <h3 className="mt-2 text-sm font-medium text-gray-900">
          Nenhuma conversa ativa
        </h3>
        <p className="mt-1 text-sm text-gray-500">
          Quando houver leads conversando com a IA, eles aparecerão aqui.
        </p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {activeLeads.map((lead) => (
        <div key={lead.id} className="flex items-center space-x-3">
          {/* Status indicator */}
          <div className="flex-shrink-0">
            <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
          </div>

          {/* Avatar */}
          <div className="flex-shrink-0">
            <div className="w-8 h-8 bg-gray-300 rounded-full flex items-center justify-center">
              <span className="text-gray-700 font-medium text-xs">
                {lead.name.charAt(0).toUpperCase()}
              </span>
            </div>
          </div>

          {/* Info */}
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-gray-900 truncate">
              {lead.name}
            </p>
            <p className="text-xs text-gray-500">
              Score: {lead.score}/100 • {formatTimeAgo(lead.updated_at)}
            </p>
          </div>

          {/* Action */}
          <div className="flex-shrink-0">
            {lead.sessions && lead.sessions.length > 0 && (
              <Link
                href={`/conversations/${lead.sessions[0].id}`}
                className="text-primary-600 hover:text-primary-700 text-xs font-medium"
              >
                Ver
              </Link>
            )}
          </div>
        </div>
      ))}

      {/* Ver todas */}
      <div className="mt-4 pt-4 border-t border-gray-200">
        <Link
          href="/conversations"
          className="text-sm text-primary-600 hover:text-primary-700 font-medium"
        >
          Ver todas as conversas →
        </Link>
      </div>
    </div>
  )
}




