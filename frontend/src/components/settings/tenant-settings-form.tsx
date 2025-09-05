'use client'

import { useState, useEffect } from 'react'
import { 
  CogIcon,
  CpuChipIcon as RobotIcon,
  BellIcon,
  ChartBarIcon,
  ChatBubbleLeftRightIcon as WhatsAppIcon,
  CheckCircleIcon,
  ExclamationCircleIcon
} from '@heroicons/react/24/outline'
import { api } from '@/lib/api'
import { TenantSettings } from '@/types'
import toast from 'react-hot-toast'

interface TenantSettingsFormProps {
  tenantId: string
}

export function TenantSettingsForm({ tenantId }: TenantSettingsFormProps) {
  const [settings, setSettings] = useState<TenantSettings | null>(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [activeTab, setActiveTab] = useState('ai')

  useEffect(() => {
    loadSettings()
  }, [])

  const loadSettings = async () => {
    try {
      setLoading(true)
      const response = await api.settings()
      setSettings(response)
    } catch (error) {
      console.error('Erro ao carregar configurações:', error)
      toast.error('Erro ao carregar configurações')
    } finally {
      setLoading(false)
    }
  }

  const handleSave = async (updatedSettings: Partial<TenantSettings>) => {
    try {
      setSaving(true)
      await api.updateSettings(updatedSettings)
      setSettings(prev => prev ? { ...prev, ...updatedSettings } : null)
      toast.success('Configurações salvas com sucesso!')
    } catch (error) {
      console.error('Erro ao salvar configurações:', error)
      toast.error('Erro ao salvar configurações')
    } finally {
      setSaving(false)
    }
  }

  const handleAIConfigChange = (field: string, value: any) => {
    if (!settings) return
    
    const updatedAIConfig = {
      ...settings.ai_config || {},
      [field]: value
    }
    
    handleSave({ ai_config: updatedAIConfig })
  }

  const handleWhatsAppConfigChange = (field: string, value: any) => {
    if (!settings) return
    
    const updatedWhatsAppConfig = {
      ...settings.whatsapp_config || {},
      [field]: value
    }
    
    handleSave({ whatsapp_config: updatedWhatsAppConfig })
  }

  const handleNotificationConfigChange = (field: string, value: any) => {
    if (!settings) return
    
    const updatedNotificationConfig = {
      ...settings.notification_config || {},
      [field]: value
    }
    
    handleSave({ notification_config: updatedNotificationConfig })
  }

  const handleScoringConfigChange = (field: string, value: any) => {
    if (!settings) return
    
    const updatedScoringConfig = {
      ...settings.scoring_config || {},
      [field]: value
    }
    
    handleSave({ scoring_config: updatedScoringConfig })
  }

  const tabs = [
    { id: 'ai', name: 'Inteligência Artificial', icon: RobotIcon },
    { id: 'whatsapp', name: 'WhatsApp', icon: WhatsAppIcon },
    { id: 'notifications', name: 'Notificações', icon: BellIcon },
    { id: 'scoring', name: 'Pontuação', icon: ChartBarIcon },
  ]

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (!settings) {
    return (
      <div className="text-center py-8">
        <ExclamationCircleIcon className="mx-auto h-12 w-12 text-gray-400" />
        <h3 className="mt-2 text-sm font-medium text-gray-900">Erro ao carregar configurações</h3>
        <p className="mt-1 text-sm text-gray-500">Tente recarregar a página</p>
      </div>
    )
  }

  return (
    <div className="bg-white shadow rounded-lg">
      {/* Tabs */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8 px-6" aria-label="Tabs">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`${
                activeTab === tab.id
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm flex items-center gap-2`}
            >
              <tab.icon className="h-4 w-4" />
              {tab.name}
            </button>
          ))}
        </nav>
      </div>

      {/* Content */}
      <div className="p-6">
        {activeTab === 'ai' && (
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-medium text-gray-900 mb-4">Configurações de IA</h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Modelo
                  </label>
                  <select
                    value={settings.ai_config?.model || 'gpt-4o-mini'}
                    onChange={(e) => handleAIConfigChange('model', e.target.value)}
                    disabled={saving}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 disabled:opacity-50"
                  >
                    <option value="gpt-4o-mini">GPT-4o Mini</option>
                    <option value="gpt-4o">GPT-4o</option>
                    <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Temperatura ({settings.ai_config?.temperature || 0.7})
                  </label>
                  <input
                    type="range"
                    min="0"
                    max="1"
                    step="0.1"
                    value={settings.ai_config?.temperature || 0.7}
                    onChange={(e) => handleAIConfigChange('temperature', parseFloat(e.target.value))}
                    disabled={saving}
                    className="w-full"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Max Tokens
                  </label>
                  <input
                    type="number"
                    min="100"
                    max="4000"
                    value={settings.ai_config?.max_tokens || 1000}
                    onChange={(e) => handleAIConfigChange('max_tokens', parseInt(e.target.value))}
                    disabled={saving}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 disabled:opacity-50"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Limite de Qualificação (%)
                  </label>
                  <input
                    type="number"
                    min="0"
                    max="100"
                    value={settings.ai_config?.qualification_threshold || 70}
                    onChange={(e) => handleAIConfigChange('qualification_threshold', parseInt(e.target.value))}
                    disabled={saving}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 disabled:opacity-50"
                  />
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'whatsapp' && (
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-medium text-gray-900 mb-4">Configurações do WhatsApp</h3>
              
              <div className="space-y-4">
                <div className="flex items-center">
                  <input
                    id="reengagement_24h"
                    type="checkbox"
                    checked={settings.whatsapp_config?.reengagement_24h || false}
                    onChange={(e) => handleWhatsAppConfigChange('reengagement_24h', e.target.checked)}
                    disabled={saving}
                    className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded disabled:opacity-50"
                  />
                  <label htmlFor="reengagement_24h" className="ml-2 block text-sm text-gray-900">
                    Reengajamento em 24h
                  </label>
                </div>

                <div className="flex items-center">
                  <input
                    id="reengagement_72h"
                    type="checkbox"
                    checked={settings.whatsapp_config?.reengagement_72h || false}
                    onChange={(e) => handleWhatsAppConfigChange('reengagement_72h', e.target.checked)}
                    disabled={saving}
                    className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded disabled:opacity-50"
                  />
                  <label htmlFor="reengagement_72h" className="ml-2 block text-sm text-gray-900">
                    Reengajamento em 72h
                  </label>
                </div>

                <div className="border-t pt-4">
                  <h4 className="text-sm font-medium text-gray-900 mb-3">Horário Comercial</h4>
                  
                  <div className="flex items-center mb-3">
                    <input
                      id="business_hours_enabled"
                      type="checkbox"
                      checked={settings.whatsapp_config?.business_hours?.enabled || false}
                      onChange={(e) => handleWhatsAppConfigChange('business_hours', {
                        ...settings.whatsapp_config?.business_hours || {},
                        enabled: e.target.checked
                      })}
                      disabled={saving}
                      className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded disabled:opacity-50"
                    />
                    <label htmlFor="business_hours_enabled" className="ml-2 block text-sm text-gray-900">
                      Ativar horário comercial
                    </label>
                  </div>

                  {settings.whatsapp_config?.business_hours?.enabled && (
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Início
                        </label>
                        <input
                          type="time"
                          value={settings.whatsapp_config?.business_hours?.start || '09:00'}
                          onChange={(e) => handleWhatsAppConfigChange('business_hours', {
                            ...settings.whatsapp_config?.business_hours || {},
                            start: e.target.value
                          })}
                          disabled={saving}
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 disabled:opacity-50"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Fim
                        </label>
                        <input
                          type="time"
                          value={settings.whatsapp_config?.business_hours?.end || '18:00'}
                          onChange={(e) => handleWhatsAppConfigChange('business_hours', {
                            ...settings.whatsapp_config?.business_hours || {},
                            end: e.target.value
                          })}
                          disabled={saving}
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 disabled:opacity-50"
                        />
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'notifications' && (
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-medium text-gray-900 mb-4">Configurações de Notificações</h3>
              
              <div className="space-y-4">
                <div className="flex items-center">
                  <input
                    id="qualified_lead_email"
                    type="checkbox"
                    checked={settings.notification_config?.qualified_lead_email || false}
                    onChange={(e) => handleNotificationConfigChange('qualified_lead_email', e.target.checked)}
                    disabled={saving}
                    className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded disabled:opacity-50"
                  />
                  <label htmlFor="qualified_lead_email" className="ml-2 block text-sm text-gray-900">
                    Email para leads qualificados
                  </label>
                </div>

                <div className="flex items-center">
                  <input
                    id="qualified_lead_slack"
                    type="checkbox"
                    checked={settings.notification_config?.qualified_lead_slack || false}
                    onChange={(e) => handleNotificationConfigChange('qualified_lead_slack', e.target.checked)}
                    disabled={saving}
                    className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded disabled:opacity-50"
                  />
                  <label htmlFor="qualified_lead_slack" className="ml-2 block text-sm text-gray-900">
                    Slack para leads qualificados
                  </label>
                </div>

                <div className="flex items-center">
                  <input
                    id="daily_summary"
                    type="checkbox"
                    checked={settings.notification_config?.daily_summary || false}
                    onChange={(e) => handleNotificationConfigChange('daily_summary', e.target.checked)}
                    disabled={saving}
                    className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded disabled:opacity-50"
                  />
                  <label htmlFor="daily_summary" className="ml-2 block text-sm text-gray-900">
                    Resumo diário
                  </label>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'scoring' && (
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-medium text-gray-900 mb-4">Sistema de Pontuação</h3>
              
              <div className="space-y-6">
                <div>
                  <h4 className="text-sm font-medium text-gray-900 mb-3">Pesos por Patrimônio</h4>
                  <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                    {Object.entries(settings.scoring_config?.patrimonio_weights || {}).map(([range, weight]) => (
                      <div key={range}>
                        <label className="block text-xs font-medium text-gray-700 mb-1">
                          {range}
                        </label>
                        <input
                          type="number"
                          min="0"
                          max="100"
                          value={weight}
                          onChange={(e) => handleScoringConfigChange('patrimonio_weights', {
                            ...settings.scoring_config?.patrimonio_weights || {},
                            [range]: parseInt(e.target.value)
                          })}
                          disabled={saving}
                          className="w-full px-2 py-1 text-sm border border-gray-300 rounded focus:ring-2 focus:ring-primary-500 focus:border-primary-500 disabled:opacity-50"
                        />
                      </div>
                    ))}
                  </div>
                </div>

                <div>
                  <h4 className="text-sm font-medium text-gray-900 mb-3">Pesos por Urgência</h4>
                  <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                    {Object.entries(settings.scoring_config?.urgencia_weights || {}).map(([urgencia, weight]) => (
                      <div key={urgencia}>
                        <label className="block text-xs font-medium text-gray-700 mb-1">
                          {urgencia}
                        </label>
                        <input
                          type="number"
                          min="0"
                          max="100"
                          value={weight}
                          onChange={(e) => handleScoringConfigChange('urgencia_weights', {
                            ...settings.scoring_config?.urgencia_weights || {},
                            [urgencia]: parseInt(e.target.value)
                          })}
                          disabled={saving}
                          className="w-full px-2 py-1 text-sm border border-gray-300 rounded focus:ring-2 focus:ring-primary-500 focus:border-primary-500 disabled:opacity-50"
                        />
                      </div>
                    ))}
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Peso do Objetivo
                    </label>
                    <input
                      type="number"
                      min="0"
                      max="100"
                      value={settings.scoring_config?.objetivo_weight || 15}
                      onChange={(e) => handleScoringConfigChange('objetivo_weight', parseInt(e.target.value))}
                      disabled={saving}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 disabled:opacity-50"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Peso do Interesse
                    </label>
                    <input
                      type="number"
                      min="0"
                      max="100"
                      value={settings.scoring_config?.interesse_weight || 15}
                      onChange={(e) => handleScoringConfigChange('interesse_weight', parseInt(e.target.value))}
                      disabled={saving}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 disabled:opacity-50"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Peso do Engajamento
                    </label>
                    <input
                      type="number"
                      min="0"
                      max="100"
                      value={settings.scoring_config?.engajamento_weight || 10}
                      onChange={(e) => handleScoringConfigChange('engajamento_weight', parseInt(e.target.value))}
                      disabled={saving}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 disabled:opacity-50"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Status de salvamento */}
        {saving && (
          <div className="fixed bottom-4 right-4 bg-primary-600 text-white px-4 py-2 rounded-lg shadow-lg flex items-center gap-2">
            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
            Salvando...
          </div>
        )}
      </div>
    </div>
  )
}
