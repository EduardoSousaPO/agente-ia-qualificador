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
  const [showPreview, setShowPreview] = useState(false)
  
  const templates = {
    investimentos: {
      name: "Consultoria de Investimentos",
      content: `**Sobre Nossa Empresa:**

Somos uma consultoria especializada em investimentos de alto patrimônio, focada em aposentadoria e crescimento patrimonial de longo prazo.

**Critérios de Qualificação:**
- Patrimônio mínimo: R$ 500.000 para investir
- Perfil conservador a moderado
- Objetivo: aposentadoria ou crescimento patrimonial
- Prazo de investimento: mínimo 5 anos

**Nossos Produtos:**
- Carteiras diversificadas personalizadas
- Fundos exclusivos de investimento
- Planejamento sucessório
- Consultoria financeira especializada

**Diferenciais:**
- Especialistas certificados CPA-20 e CFP
- Atendimento personalizado e consultivo
- Foco em relacionamento de longo prazo
- Estratégias conservadoras e sustentáveis

**Processo de Atendimento:**
1. Qualificação inicial via WhatsApp
2. Agendamento de consultoria gratuita
3. Análise de perfil e objetivos
4. Proposta personalizada de investimentos
5. Acompanhamento contínuo da carteira`
    },
    imobiliario: {
      name: "Consultoria Imobiliária",
      content: `**Sobre Nossa Empresa:**

Somos uma consultoria imobiliária especializada em investimentos de alto padrão e assessoria patrimonial.

**Critérios de Qualificação:**
- Interesse em investimento imobiliário acima de R$ 1.000.000
- Perfil investidor ou comprador final
- Localização: São Paulo, Rio de Janeiro ou capitais
- Timeline: decisão em até 6 meses

**Nossos Serviços:**
- Assessoria em investimentos imobiliários
- Análise de mercado e rentabilidade
- Acompanhamento jurídico completo
- Gestão de locação e patrimônio

**Diferenciais:**
- 15+ anos de experiência no mercado
- Rede exclusiva de oportunidades
- Análise técnica e financeira detalhada
- Suporte completo pós-venda

**Processo de Atendimento:**
1. Qualificação do perfil e necessidades
2. Apresentação de oportunidades selecionadas
3. Visitas acompanhadas e análise técnica
4. Negociação e fechamento
5. Acompanhamento pós-venda`
    },
    saude: {
      name: "Clínica Médica Premium",
      content: `**Sobre Nossa Clínica:**

Clínica médica premium especializada em medicina preventiva e tratamentos personalizados para executivos e suas famílias.

**Critérios de Qualificação:**
- Executivos C-level ou empresários
- Interesse em medicina preventiva premium
- Disponibilidade para consultas personalizadas
- Plano de saúde ou pagamento particular

**Nossos Serviços:**
- Check-ups executivos completos
- Medicina preventiva e longevidade
- Telemedicina 24/7
- Concierge médico personalizado

**Diferenciais:**
- Médicos especialistas renomados
- Tecnologia de ponta em diagnósticos
- Atendimento sem filas ou esperas
- Planos personalizados por família

**Processo de Atendimento:**
1. Consulta inicial de avaliação
2. Definição do plano personalizado
3. Agendamento de exames e consultas
4. Acompanhamento contínuo da saúde
5. Relatórios periódicos e ajustes`
    }
  }
  
  const loadTemplate = (templateKey: string) => {
    const template = templates[templateKey as keyof typeof templates]
    if (template) {
      setContent(template.content)
      toast.success(`Template "${template.name}" carregado!`)
    }
  }

  useEffect(() => {
    loadKnowledgeBase()
  }, [])

  const loadKnowledgeBase = async () => {
    try {
      setLoading(true)
      // Usar tenant_id fixo para demo
      const tenantId = '60675861-e22a-4990-bab8-65ed07632a63'
      
      // Timeout de 10 segundos
      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), 10000)
      
      const response = await fetch(`http://localhost:5000/api/knowledge-base/${tenantId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        signal: controller.signal
      })
      
      clearTimeout(timeoutId)
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }
      
      const data = await response.json()
      
      if (data.success && data.data) {
        setContent(data.data.content || '')
        toast.success('Base de conhecimento carregada!')
      } else if (data.success && !data.data) {
        // Não existe conhecimento ainda, usar conteúdo vazio
        setContent('')
        toast.success('Nenhum conhecimento configurado ainda. Configure abaixo.')
      }
    } catch (error) {
      console.error('Erro ao carregar base de conhecimento:', error)
      
      if (error instanceof Error) {
        if (error.name === 'AbortError') {
          toast.error('Timeout: Backend não respondeu em 10 segundos')
        } else if (error.message.includes('fetch')) {
          toast.error('Backend offline. Verifique se o servidor está rodando.')
        } else {
          toast.error(`Erro ao carregar: ${error.message}`)
        }
      } else {
        toast.error('Erro desconhecido ao carregar base de conhecimento')
      }
      
      // Em caso de erro, inicializar com conteúdo vazio para permitir configuração
      setContent('')
    } finally {
      setLoading(false)
    }
  }

  const handleSave = async () => {
    try {
      setSaving(true)
      
      if (!content.trim()) {
        toast.error('Por favor, insira algum conteúdo antes de salvar.')
        return
      }
      
      const requestData = {
        tenant_id: '60675861-e22a-4990-bab8-65ed07632a63',
        user_id: '5f9c5ba8-0ad7-43a6-92df-c205cb6b5e23', // ID real do usuário de teste
        content: content.trim()
      }
      
      // Timeout de 15 segundos para salvamento
      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), 15000)
      
      const response = await fetch('http://localhost:5000/api/knowledge-base', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData),
        signal: controller.signal
      })
      
      clearTimeout(timeoutId)
      
      if (!response.ok) {
        const errorText = await response.text()
        throw new Error(`HTTP ${response.status}: ${errorText}`)
      }
      
      const data = await response.json()
      
      if (data.success) {
        toast.success('Base de conhecimento salva com sucesso! 🎉')
      } else {
        throw new Error(data.error || 'Erro desconhecido')
      }
    } catch (error) {
      console.error('Erro ao salvar:', error)
      
      if (error instanceof Error) {
        if (error.name === 'AbortError') {
          toast.error('Timeout: Salvamento demorou mais que 15 segundos')
        } else if (error.message.includes('fetch')) {
          toast.error('Backend offline. Não foi possível salvar.')
        } else {
          toast.error(`Erro ao salvar: ${error.message}`)
        }
      } else {
        toast.error('Erro desconhecido ao salvar')
      }
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

            {/* Templates Pré-definidos */}
            <div className="bg-blue-50 p-6 rounded-lg">
              <h3 className="text-lg font-medium text-gray-900 mb-4">🎯 Templates Pré-definidos</h3>
              <p className="text-sm text-gray-600 mb-4">Use um dos templates abaixo como ponto de partida e personalize para seu negócio:</p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                {Object.entries(templates).map(([key, template]) => (
                  <button
                    key={key}
                    onClick={() => loadTemplate(key)}
                    className="bg-white p-4 rounded border hover:border-blue-300 hover:shadow-sm transition-all duration-200 text-left"
                  >
                    <h4 className="font-medium text-gray-800 mb-2">{template.name}</h4>
                    <p className="text-xs text-gray-500">Clique para carregar este template</p>
                  </button>
                ))}
              </div>
            </div>

            {/* Exemplos de Uso */}
            <div className="bg-gray-50 p-6 rounded-lg">
              <h3 className="text-lg font-medium text-gray-900 mb-4">💡 Dicas para Configuração</h3>
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

            {/* Botões de Ação */}
            <div className="flex justify-between items-center">
              <button
                onClick={() => setShowPreview(!showPreview)}
                className="bg-gray-100 text-gray-800 px-6 py-3 font-light hover:bg-gray-200 transition-colors duration-200 flex items-center gap-2"
              >
                {showPreview ? '📝 Editar' : '👁️ Preview'}
              </button>
              
              <button
                onClick={handleSave}
                disabled={saving || !content.trim()}
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

            {/* Preview */}
            {showPreview && content && (
              <div className="bg-gray-50 border rounded-lg p-6">
                <h3 className="text-lg font-medium text-gray-900 mb-4">📋 Preview do Conhecimento</h3>
                <div className="prose prose-sm max-w-none">
                  {content.split('\n').map((line, index) => {
                    if (line.startsWith('**') && line.endsWith('**')) {
                      return <h4 key={index} className="font-semibold text-gray-800 mt-4 mb-2">{line.replace(/\*\*/g, '')}</h4>
                    } else if (line.startsWith('- ')) {
                      return <li key={index} className="ml-4 text-gray-600">{line.substring(2)}</li>
                    } else if (line.match(/^\d+\./)) {
                      return <div key={index} className="ml-4 text-gray-600">{line}</div>
                    } else if (line.trim()) {
                      return <p key={index} className="text-gray-600 mb-2">{line}</p>
                    }
                    return <br key={index} />
                  })}
                </div>
              </div>
            )}

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
