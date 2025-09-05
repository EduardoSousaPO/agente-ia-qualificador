'use client'

import { useState, useEffect } from 'react'
import { api } from '@/lib/api'
import { ChatBubbleLeftRightIcon, CheckCircleIcon, XCircleIcon, ClockIcon } from '@heroicons/react/24/outline'

interface ConversationStats {
  total: number
  active: number
  completed: number
  abandoned: number
}

export function ConversationsStats() {
  const [stats, setStats] = useState<ConversationStats>({
    total: 0,
    active: 0,
    completed: 0,
    abandoned: 0
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadStats()
  }, [])

  const loadStats = async () => {
    try {
      setLoading(true)
      // Simulando dados - substitua pela chamada real da API
      const mockStats: ConversationStats = {
        total: 156,
        active: 23,
        completed: 98,
        abandoned: 35
      }
      setStats(mockStats)
    } catch (error) {
      console.error('Erro ao carregar estatísticas:', error)
    } finally {
      setLoading(false)
    }
  }

  const statItems = [
    {
      name: 'Total de Conversas',
      value: stats.total,
      icon: ChatBubbleLeftRightIcon,
      color: 'text-blue-600',
      bg: 'bg-blue-100'
    },
    {
      name: 'Conversas Ativas',
      value: stats.active,
      icon: ClockIcon,
      color: 'text-yellow-600',
      bg: 'bg-yellow-100'
    },
    {
      name: 'Concluídas',
      value: stats.completed,
      icon: CheckCircleIcon,
      color: 'text-green-600',
      bg: 'bg-green-100'
    },
    {
      name: 'Abandonadas',
      value: stats.abandoned,
      icon: XCircleIcon,
      color: 'text-red-600',
      bg: 'bg-red-100'
    }
  ]

  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="bg-white p-6 rounded-lg shadow animate-pulse">
            <div className="h-4 bg-gray-200 rounded mb-2"></div>
            <div className="h-8 bg-gray-200 rounded"></div>
          </div>
        ))}
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      {statItems.map((item) => (
        <div key={item.name} className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center">
            <div className={`p-3 rounded-full ${item.bg}`}>
              <item.icon className={`h-6 w-6 ${item.color}`} />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">{item.name}</p>
              <p className="text-2xl font-semibold text-gray-900">{item.value}</p>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}











