'use client'

import { useState, useEffect } from 'react'
import { DashboardLayout } from '@/components/layout/dashboard-layout'
import { 
  ChartBarIcon,
  UsersIcon,
  TrophyIcon,
  ClockIcon,
  ArrowTrendingUpIcon,
  DocumentChartBarIcon
} from '@heroicons/react/24/outline'
import { api } from '@/lib/api'
import { DashboardStats } from '@/types'
import toast from 'react-hot-toast'

export default function ReportsPage() {
  const [stats, setStats] = useState<DashboardStats | null>(null)
  const [loading, setLoading] = useState(true)
  const [timeRange, setTimeRange] = useState('30d')

  useEffect(() => {
    loadStats()
  }, [timeRange])

  const loadStats = async () => {
    try {
      setLoading(true)
      const response = await api.dashboard()
      setStats(response)
    } catch (error) {
      console.error('Erro ao carregar estatísticas:', error)
      toast.error('Erro ao carregar relatórios')
    } finally {
      setLoading(false)
    }
  }

  const formatPercentage = (value: number) => {
    return `${(value * 100).toFixed(1)}%`
  }

  const StatCard = ({ title, value, icon: Icon, description, trend }: {
    title: string
    value: string | number
    icon: any
    description?: string
    trend?: 'up' | 'down' | 'stable'
  }) => (
    <div className="bg-white shadow rounded-lg p-6">
      <div className="flex items-center">
        <div className="flex-shrink-0">
          <Icon className="h-8 w-8 text-primary-600" />
        </div>
        <div className="ml-5 w-0 flex-1">
          <dl>
            <dt className="text-sm font-medium text-gray-500 truncate">{title}</dt>
            <dd className="flex items-baseline">
              <div className="text-2xl font-semibold text-gray-900">
                {typeof value === 'number' ? value.toLocaleString() : value}
              </div>
              {trend && (
                <div className={`ml-2 flex items-baseline text-sm font-semibold ${
                  trend === 'up' ? 'text-green-600' : 
                  trend === 'down' ? 'text-red-600' : 'text-gray-500'
                }`}>
                  <ArrowTrendingUpIcon className="h-4 w-4 flex-shrink-0 self-center" />
                </div>
              )}
            </dd>
            {description && (
              <dd className="text-sm text-gray-600 mt-1">{description}</dd>
            )}
          </dl>
        </div>
      </div>
    </div>
  )

  if (loading) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
        </div>
      </DashboardLayout>
    )
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Relatórios</h1>
            <p className="text-gray-600">
              Acompanhe o desempenho do seu sistema de qualificação de leads
            </p>
          </div>
          
          <div className="flex items-center space-x-4">
            <select
              value={timeRange}
              onChange={(e) => setTimeRange(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            >
              <option value="7d">Últimos 7 dias</option>
              <option value="30d">Últimos 30 dias</option>
              <option value="90d">Últimos 90 dias</option>
            </select>
          </div>
        </div>

        {/* Stats Grid */}
        {stats && (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <StatCard
                title="Total de Leads"
                value={stats.total_leads}
                icon={UsersIcon}
                description="Leads cadastrados no sistema"
                trend="up"
              />
              
              <StatCard
                title="Leads Hoje"
                value={stats.leads_hoje}
                icon={ClockIcon}
                description="Novos leads hoje"
                trend="stable"
              />
              
              <StatCard
                title="Leads Qualificados"
                value={stats.leads_qualificados}
                icon={TrophyIcon}
                description="Leads que passaram na qualificação"
                trend="up"
              />
              
              <StatCard
                title="Taxa de Qualificação"
                value={formatPercentage(stats.taxa_qualificacao)}
                icon={ChartBarIcon}
                description="Percentual de leads qualificados"
                trend="up"
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <StatCard
                title="Score Médio"
                value={stats.score_medio.toFixed(1)}
                icon={ArrowTrendingUpIcon}
                description="Pontuação média dos leads"
                trend="up"
              />
              
              <StatCard
                title="Conversas Ativas"
                value={stats.conversas_ativas}
                icon={DocumentChartBarIcon}
                description="Conversas em andamento"
                trend="stable"
              />
            </div>

            {/* Charts Placeholder */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Leads por Origem */}
              <div className="bg-white shadow rounded-lg p-6">
                <h3 className="text-lg font-medium text-gray-900 mb-4">Leads por Origem</h3>
                <div className="space-y-3">
                  {Object.entries(stats.leads_por_origem).map(([origem, count]) => (
                    <div key={origem} className="flex items-center justify-between">
                      <span className="text-sm text-gray-600 capitalize">{origem}</span>
                      <span className="text-sm font-medium text-gray-900">{count}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Leads por Status */}
              <div className="bg-white shadow rounded-lg p-6">
                <h3 className="text-lg font-medium text-gray-900 mb-4">Leads por Status</h3>
                <div className="space-y-3">
                  {Object.entries(stats.leads_por_status).map(([status, count]) => (
                    <div key={status} className="flex items-center justify-between">
                      <span className="text-sm text-gray-600 capitalize">{status}</span>
                      <span className="text-sm font-medium text-gray-900">{count}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Timeline Placeholder */}
            <div className="bg-white shadow rounded-lg p-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Timeline de Leads</h3>
              <div className="text-center text-gray-500 py-8">
                <ChartBarIcon className="h-12 w-12 mx-auto mb-4 text-gray-400" />
                <p>Gráfico de timeline será implementado em breve</p>
                <p className="text-sm mt-1">Visualize a evolução dos seus leads ao longo do tempo</p>
              </div>
            </div>
          </>
        )}

        {!stats && !loading && (
          <div className="bg-white shadow rounded-lg p-6">
            <div className="text-center text-gray-500">
              <DocumentChartBarIcon className="h-12 w-12 mx-auto mb-4 text-gray-400" />
              <p>Nenhum dado disponível para relatórios</p>
              <p className="text-sm mt-1">Adicione alguns leads para visualizar os relatórios</p>
            </div>
          </div>
        )}
      </div>
    </DashboardLayout>
  )
}










