'use client'

import { useAuth } from '@/components/providers'
import { DashboardLayout } from '@/components/layout/dashboard-layout'
import { DashboardStats } from '@/components/dashboard/dashboard-stats'
import { RecentLeads } from '@/components/dashboard/recent-leads'
import { LeadsChart } from '@/components/dashboard/leads-chart'
import { ActiveConversations } from '@/components/dashboard/active-conversations'
import { useEffect, useState } from 'react'
import { api } from '@/lib/api'
import { DashboardStats as DashboardStatsType, Lead } from '@/types'
import { LoadingSpinner } from '@/components/ui/loading-spinner'

export default function Dashboard() {
  const { user, loading: authLoading } = useAuth()
  const [stats, setStats] = useState<DashboardStatsType | null>(null)
  const [recentLeads, setRecentLeads] = useState<Lead[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (user) {
      loadDashboardData()
    }
  }, [user])

  const loadDashboardData = async () => {
    try {
      setLoading(true)
      
      // Carregar estatísticas
      const [dashboardStats, leadsResponse] = await Promise.all([
        api.dashboard(),
        api.leads({ limit: 10, page: 1 })
      ])
      
      setStats(dashboardStats)
      setRecentLeads(leadsResponse.data)
    } catch (error) {
      console.error('Erro ao carregar dados do dashboard:', error)
    } finally {
      setLoading(false)
    }
  }

  if (authLoading || loading) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center h-96">
          <LoadingSpinner size="lg" />
        </div>
      </DashboardLayout>
    )
  }

  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="max-w-md w-full space-y-8">
          <div className="text-center">
            <h2 className="mt-6 text-3xl font-bold text-gray-900">
              Faça login para continuar
            </h2>
            <p className="mt-2 text-sm text-gray-600">
              Acesse sua conta para gerenciar leads
            </p>
          </div>
          <div className="mt-8">
            <a
              href="/login"
              className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Fazer Login
            </a>
          </div>
        </div>
      </div>
    )
  }

  return (
    <DashboardLayout>
      <div className="space-y-8">
        {/* Header */}
        <div className="page-header">
          <h1 className="page-title">Dashboard</h1>
          <p className="page-description">
            Visão geral dos seus leads e conversas
          </p>
        </div>

        {/* Stats Cards */}
        {stats && <DashboardStats stats={stats} />}

        {/* Charts and Recent Activity */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Gráfico de Leads */}
          <div className="card">
            <div className="card-header">
              <h3 className="card-title">Leads por Dia</h3>
              <p className="card-description">
                Evolução dos leads nos últimos 30 dias
              </p>
            </div>
            {stats && <LeadsChart data={stats.timeline_leads} />}
          </div>

          {/* Conversas Ativas */}
          <div className="card">
            <div className="card-header">
              <h3 className="card-title">Conversas Ativas</h3>
              <p className="card-description">
                Leads atualmente em conversa com IA
              </p>
            </div>
            <ActiveConversations />
          </div>
        </div>

        {/* Recent Leads */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Leads Recentes</h3>
            <p className="card-description">
              Últimos leads adicionados ao sistema
            </p>
          </div>
          <RecentLeads leads={recentLeads} />
        </div>
      </div>
    </DashboardLayout>
  )
}




