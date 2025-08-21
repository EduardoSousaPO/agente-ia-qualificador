'use client'

import { DashboardStats as StatsType } from '@/types'
import { 
  UsersIcon, 
  UserPlusIcon, 
  CheckCircleIcon, 
  ChartBarIcon,
  ChatBubbleLeftRightIcon,
  CalendarDaysIcon
} from '@heroicons/react/24/outline'

interface DashboardStatsProps {
  stats: StatsType
}

export function DashboardStats({ stats }: DashboardStatsProps) {
  const statCards = [
    {
      name: 'Total de Leads',
      value: stats.total_leads,
      icon: UsersIcon,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100',
      change: '+12%',
      changeType: 'positive' as const,
    },
    {
      name: 'Leads Hoje',
      value: stats.leads_hoje,
      icon: UserPlusIcon,
      color: 'text-green-600',
      bgColor: 'bg-green-100',
      change: '+8%',
      changeType: 'positive' as const,
    },
    {
      name: 'Qualificados',
      value: stats.leads_qualificados,
      icon: CheckCircleIcon,
      color: 'text-emerald-600',
      bgColor: 'bg-emerald-100',
      change: `${stats.taxa_qualificacao.toFixed(1)}%`,
      changeType: 'neutral' as const,
    },
    {
      name: 'Score Médio',
      value: Math.round(stats.score_medio),
      icon: ChartBarIcon,
      color: 'text-purple-600',
      bgColor: 'bg-purple-100',
      change: '+5 pts',
      changeType: 'positive' as const,
    },
    {
      name: 'Conversas Ativas',
      value: stats.conversas_ativas,
      icon: ChatBubbleLeftRightIcon,
      color: 'text-orange-600',
      bgColor: 'bg-orange-100',
      change: '-2',
      changeType: 'negative' as const,
    },
    {
      name: 'Reuniões Agendadas',
      value: stats.reunioes_agendadas,
      icon: CalendarDaysIcon,
      color: 'text-indigo-600',
      bgColor: 'bg-indigo-100',
      change: '+3',
      changeType: 'positive' as const,
    },
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-6">
      {statCards.map((stat) => (
        <div key={stat.name} className="card p-6">
          <div className="flex items-center">
            <div className={`flex-shrink-0 p-3 rounded-lg ${stat.bgColor}`}>
              <stat.icon className={`w-6 h-6 ${stat.color}`} />
            </div>
            <div className="ml-4 flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-500 truncate">
                {stat.name}
              </p>
              <div className="flex items-baseline">
                <p className="text-2xl font-semibold text-gray-900">
                  {typeof stat.value === 'number' ? stat.value.toLocaleString() : stat.value}
                </p>
                <span
                  className={`ml-2 text-sm font-medium ${
                    stat.changeType === 'positive'
                      ? 'text-green-600'
                      : stat.changeType === 'negative'
                      ? 'text-red-600'
                      : 'text-gray-600'
                  }`}
                >
                  {stat.change}
                </span>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}




