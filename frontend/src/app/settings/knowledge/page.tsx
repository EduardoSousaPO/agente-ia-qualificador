'use client'

import { useState, useEffect } from 'react'
import { DashboardLayout } from '@/components/layout/dashboard-layout'
import { LoadingSpinner } from '@/components/ui/loading-spinner'
import { api } from '@/lib/api'
import toast from 'react-hot-toast'

export default function KnowledgePage() {
  const [content, setContent] = useState('')
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    loadKnowledgeBase()
  }, [])

  const loadKnowledgeBase = async () => {
    try {
      setLoading(true)
      // Usar tenant_id fixo para demo
      const tenantId = '60675861-e22a-4990-bab8-65ed07632a63'
      
      const response = await fetch(`/api/knowledge-base/${tenantId}`)
      const data = await response.json()
      
      if (data.success && data.data) {
        setContent(data.data.content || '')
      }
    } catch (error) {
      console.error('Erro ao carregar base de conhecimento:', error)
      toast.error('Erro ao carregar base de conhecimento')
    } finally {
      setLoading(false)
    }
  }

  const handleSave = async () => {
    try {
      setSaving(true)
      
      const requestData = {
        tenant_id: '60675861-e22a-4990-bab8-65ed07632a63',
        user_id: 'admin-user-001',
        content: content
      }
      
      const response = await fetch('/api/knowledge-base', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData)
      })
      
      const data = await response.json()
      
      if (data.success) {
        toast.success('Base de conhecimento salva com sucesso!')
      } else {
        throw new Error(data.error || 'Erro desconhecido')
      }
    } catch (error) {
      console.error('Erro ao salvar:', error)
      toast.error('Erro ao salvar base de conhecimento')
    } finally {
      setSaving(false)
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
      {/* HEADER TESLA-STYLE */}
      <div className="bg-white py-16">
        <div className="max-w-4xl mx-auto px-8">
          <h1 className="text-5xl font-thin text-black mb-6">Base de Conhecimento</h1>
          <p className="text-xl text-gray-600 font-light max-w-3xl">
            Personalize o conhecimento do seu agente sobre sua empresa, produtos e critérios específicos de qualificação. 
            O agente utilizará essas informações durante as conversas com os leads.
          </p>
        </div>
      </div>

      {/* FORM MINIMALISTA */}
      <div className="bg-white py-12">
        <div className="max-w-4xl mx-auto px-8">
          <div className="space-y-8">
            {/* Textarea Principal */}
            <div className="space-y-4">
              <label className="block text-sm font-medium text-gray-700">
                Conhecimento da Empresa
              </label>
              <textarea
                value={content}
                onChange={(e) => setContent(e.target.value)}
                className="w-full h-80 border-0 border-b border-gray-200 focus:border-black resize-none text-lg font-light p-4 bg-gray-50 focus:bg-white transition-colors duration-200"
                placeholder="Descreva sua empresa, produtos, diferenciais, critérios específicos de qualificação...

Exemplo:
- Somos uma consultoria especializada em investimentos de alto patrimônio
- Trabalhamos apenas com clientes que possuem mais de R$ 500 mil para investir
- Nosso foco é aposentadoria e crescimento patrimonial de longo prazo
- Oferecemos consultoria personalizada com especialistas certificados
- Nossos produtos principais são: carteiras diversificadas, fundos exclusivos e planejamento sucessório"
              />
              <div className="flex justify-between items-center text-sm text-gray-500">
                <span>{content.length} caracteres</span>
                <span>Dica: Seja específico sobre critérios de qualificação e diferenciais</span>
              </div>
            </div>

            {/* Exemplos de Uso */}
            <div className="bg-gray-50 p-6 rounded-lg">
              <h3 className="text-lg font-medium text-gray-900 mb-4">💡 Exemplos de Informações Úteis</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-gray-600">
                <div>
                  <h4 className="font-medium text-gray-800">Critérios de Qualificação:</h4>
                  <ul className="mt-2 space-y-1 list-disc list-inside">
                    <li>Patrimônio mínimo exigido</li>
                    <li>Perfil de risco aceito</li>
                    <li>Objetivos preferenciais</li>
                    <li>Prazo de investimento</li>
                  </ul>
                </div>
                <div>
                  <h4 className="font-medium text-gray-800">Informações da Empresa:</h4>
                  <ul className="mt-2 space-y-1 list-disc list-inside">
                    <li>Especialidades e produtos</li>
                    <li>Diferenciais competitivos</li>
                    <li>Processo de atendimento</li>
                    <li>Certificações e credenciais</li>
                  </ul>
                </div>
              </div>
            </div>

            {/* Botão de Salvar */}
            <div className="flex justify-end">
              <button
                onClick={handleSave}
                disabled={saving}
                className="bg-black text-white px-8 py-3 font-light hover:bg-gray-800 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
              >
                {saving ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                    Salvando...
                  </>
                ) : (
                  'Salvar Conhecimento'
                )}
              </button>
            </div>

            {/* Status */}
            {content && (
              <div className="text-center py-4">
                <div className="inline-flex items-center gap-2 text-sm text-green-600">
                  <div className="w-2 h-2 bg-green-500 rounded-full" />
                  Agente configurado com conhecimento personalizado
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </DashboardLayout>
  )
}
