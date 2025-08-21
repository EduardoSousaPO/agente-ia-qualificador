'use client'

import { useState, useEffect } from 'react'
import { DashboardLayout } from '@/components/layout/dashboard-layout'
import { SettingsTabs } from '@/components/settings/settings-tabs'
import { GeneralSettings } from '@/components/settings/general-settings'
import { AISettings } from '@/components/settings/ai-settings'
import { IntegrationSettings } from '@/components/settings/integration-settings'
import { UserManagement } from '@/components/settings/user-management'
import { api } from '@/lib/api'
import { TenantSettings } from '@/types'
import { LoadingSpinner } from '@/components/ui/loading-spinner'
import toast from 'react-hot-toast'

export default function SettingsPage() {
  const [activeTab, setActiveTab] = useState('general')
  const [settings, setSettings] = useState<TenantSettings | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadSettings()
  }, [])

  const loadSettings = async () => {
    try {
      setLoading(true)
      const response = await api.getSettings()
      setSettings(response)
    } catch (error) {
      console.error('Erro ao carregar configurações:', error)
      toast.error('Erro ao carregar configurações')
    } finally {
      setLoading(false)
    }
  }

  const handleSettingsUpdate = (updatedSettings: Partial<TenantSettings>) => {
    if (settings) {
      setSettings({ ...settings, ...updatedSettings })
    }
  }

  if (loading) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center h-64">
          <LoadingSpinner size="lg" />
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
            <h1 className="text-2xl font-bold text-gray-900">Configurações</h1>
            <p className="text-gray-600">
              Gerencie as configurações do seu tenant e personalize o comportamento do sistema
            </p>
          </div>
        </div>

        {/* Tabs */}
        <SettingsTabs activeTab={activeTab} onTabChange={setActiveTab} />

        {/* Content */}
        <div className="bg-white shadow-sm rounded-lg">
          {activeTab === 'general' && (
            <GeneralSettings
              settings={settings}
              onSettingsUpdate={handleSettingsUpdate}
            />
          )}
          
          {activeTab === 'ai' && (
            <AISettings
              settings={settings}
              onSettingsUpdate={handleSettingsUpdate}
            />
          )}
          
          {activeTab === 'integrations' && (
            <IntegrationSettings
              settings={settings}
              onSettingsUpdate={handleSettingsUpdate}
            />
          )}
          
          {activeTab === 'users' && (
            <UserManagement />
          )}
        </div>
      </div>
    </DashboardLayout>
  )
}




