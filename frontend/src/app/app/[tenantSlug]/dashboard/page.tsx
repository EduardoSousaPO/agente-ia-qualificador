'use client'

import { useTenant } from '@/hooks/useTenant'
import { DashboardStats } from '@/components/dashboard/dashboard-stats'
import { RecentLeads } from '@/components/dashboard/recent-leads'
import { LeadsChart } from '@/components/dashboard/leads-chart'
import { ActiveConversations } from '@/components/dashboard/active-conversations'
import { QualificationScenarios } from '@/components/dashboard/qualification-scenarios'
import { useEffect, useState } from 'react'
import { api } from '@/lib/api'
import { DashboardStats as DashboardStatsType, Lead } from '@/types'
import { LoadingSpinner } from '@/components/ui/loading-spinner'

export default function TenantDashboard() {
  const { currentTenant, loading: tenantLoading } = useTenant()
  const [stats, setStats] = useState<DashboardStatsType | null>(null)
  const [recentLeads, setRecentLeads] = useState<Lead[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (currentTenant) {
      loadDashboardData()
    }
  }, [currentTenant])

  const loadDashboardData = async () => {
    try {
      setLoading(true)
      
      // Carregar estatísticas do tenant atual
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

  if (tenantLoading || loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <LoadingSpinner size="lg" />
      </div>
    )
  }

  if (!currentTenant) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <h2 className="text-xl font-semibold text-gray-900 mb-2">
            Tenant não encontrado
          </h2>
          <p className="text-gray-600">
            Verifique se você tem acesso a este tenant.
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="border-b border-gray-200 pb-4">
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-1">
          Visão geral de {currentTenant.name}
        </p>
      </div>

      {/* Stats Cards */}
      {stats && <DashboardStats stats={stats} />}

      {/* Charts and Tables */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Charts */}
        <div className="space-y-6">
          {stats && <LeadsChart data={stats.leads_chart || []} />}
          <QualificationScenarios />
        </div>

        {/* Tables */}
        <div className="space-y-6">
          <RecentLeads leads={recentLeads} />
          <ActiveConversations />
        </div>
      </div>
    </div>
  )
}











