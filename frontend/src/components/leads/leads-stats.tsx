'use client'

import { useState, useEffect } from 'react'
import { api } from '@/lib/api'
import { 
  UserGroupIcon, 
  PhoneIcon, 
  CheckCircleIcon, 
  TrophyIcon 
} from '@heroicons/react/24/outline'

interface LeadStats {
  total: number
  new: number
  contacted: number
  qualified: number
  converted: number
  conversionRate: number
}

export function LeadsStats() {
  const [stats, setStats] = useState<LeadStats>({
    total: 0,
    new: 0,
    contacted: 0,
    qualified: 0,
    converted: 0,
    conversionRate: 0
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadStats()
  }, [])

  const loadStats = async () => {
    try {
      setLoading(true)
      // Simulando dados - substitua pela chamada real da API
      const mockStats: LeadStats = {
        total: 342,
        new: 45,
        contacted: 123,
        qualified: 89,
        converted: 85,
        conversionRate: 24.9
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
      name: 'Total de Leads',
      value: stats.total,
      icon: UserGroupIcon,
      color: 'text-blue-600',
      bg: 'bg-blue-100'
    },
    {
      name: 'Novos Leads',
      value: stats.new,
      icon: PhoneIcon,
      color: 'text-green-600',
      bg: 'bg-green-100'
    },
    {
      name: 'Qualificados',
      value: stats.qualified,
      icon: CheckCircleIcon,
      color: 'text-yellow-600',
      bg: 'bg-yellow-100'
    },
    {
      name: 'Taxa de Conversão',
      value: `${stats.conversionRate}%`,
      icon: TrophyIcon,
      color: 'text-purple-600',
      bg: 'bg-purple-100'
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











