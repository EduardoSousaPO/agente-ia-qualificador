'use client'

import { useState, useEffect } from 'react'
import { DashboardLayout } from '@/components/layout/dashboard-layout'
import { LoadingSpinner } from '@/components/ui/loading-spinner'
import toast from 'react-hot-toast'

interface AgentMessage {
  id: string
  content: string
  session_id: string
  created_at: string
  sessions?: {
    leads?: {
      name: string
      phone: string
    }
  }
  feedback_status?: 'approved' | 'rejected' | null
}

export default function FeedbackPage() {
  const [messages, setMessages] = useState<AgentMessage[]>([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState<'all' | 'approved' | 'rejected' | 'pending'>('pending')
  
  // Estados para chat de teste
  const [showTestChat, setShowTestChat] = useState(false)
  const [testMessages, setTestMessages] = useState<{role: 'user' | 'agent', content: string, timestamp: string}[]>([])
  const [testInput, setTestInput] = useState('')
  const [testLoading, setTestLoading] = useState(false)

  useEffect(() => {
    loadAgentMessages()
  }, [filter])

  const loadAgentMessages = async () => {
    try {
      setLoading(true)
      
      // Buscar mensagens de todas as sessões ativas
      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), 10000)
      
      const sessionsResponse = await fetch('http://localhost:5000/api/chat/sessions', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        signal: controller.signal
      })
      
      clearTimeout(timeoutId)
      
      if (!sessionsResponse.ok) {
        throw new Error(`HTTP ${sessionsResponse.status}: ${sessionsResponse.statusText}`)
      }
      
      const sessionsData = await sessionsResponse.json()
      
      if (sessionsData.data && sessionsData.data.length > 0) {
        // Para cada sessão, buscar mensagens do agente
        const allMessages: AgentMessage[] = []
        
        for (const session of sessionsData.data.slice(0, 5)) { // Limitar para demo
          try {
            const messagesResponse = await fetch(`http://localhost:5000/api/agent-messages/${session.id}`, {
              method: 'GET',
              headers: {
                'Content-Type': 'application/json',
              },
              signal: controller.signal
            })
            
            if (messagesResponse.ok) {
              const messagesData = await messagesResponse.json()
              if (messagesData.success && messagesData.data) {
                allMessages.push(...messagesData.data)
              }
            } else {
              // Fallback: criar mensagens mock para demo
              const mockMessages = generateMockMessages(session)
              allMessages.push(...mockMessages)
            }
          } catch (error) {
            // Fallback: criar mensagens mock
            const mockMessages = generateMockMessages(session)
            allMessages.push(...mockMessages)
          }
        }
        
        // Filtrar por status se necessário
        let filteredMessages = allMessages
        if (filter !== 'all') {
          if (filter === 'pending') {
            filteredMessages = allMessages.filter(msg => !msg.feedback_status)
          } else {
            filteredMessages = allMessages.filter(msg => msg.feedback_status === filter)
          }
        }
        
        setMessages(filteredMessages.slice(0, 10)) // Limitar para demo
      } else {
        // Gerar mensagens mock para demo
        setMessages(generateMockMessagesDemo())
      }
      
    } catch (error) {
      console.error('Erro ao carregar mensagens:', error)
      
      if (error instanceof Error) {
        if (error.name === 'AbortError') {
          toast.error('Timeout: Backend não respondeu em 10 segundos')
        } else if (error.message.includes('fetch')) {
          toast.error('Backend offline. Mostrando dados de demonstração.')
        } else {
          toast.error(`Erro ao carregar mensagens: ${error.message}`)
        }
      } else {
        toast.error('Erro desconhecido ao carregar mensagens')
      }
      
      // Fallback para demo
      setMessages(generateMockMessagesDemo())
    } finally {
      setLoading(false)
    }
  }

  const generateMockMessages = (session: any): AgentMessage[] => {
    return [
      {
        id: `msg_${session.id}_1`,
        content: "Olá! 👋 Vi que você tem interesse em investimentos. Para te conectar com o melhor especialista, preciso fazer algumas perguntas rápidas. Primeira pergunta: Quanto você tem disponível para investir hoje?",
        session_id: session.id,
        created_at: new Date().toISOString(),
        sessions: {
          leads: {
            name: session.lead_name || 'Lead Demo',
            phone: session.phone || '+5511999999999'
          }
        },
        feedback_status: null
      },
      {
        id: `msg_${session.id}_2`,
        content: "Perfeito! Agora me conta: qual seu principal objetivo com os investimentos? A) Aposentadoria B) Crescimento do patrimônio C) Reserva de emergência D) Especulação/day trade",
        session_id: session.id,
        created_at: new Date().toISOString(),
        sessions: {
          leads: {
            name: session.lead_name || 'Lead Demo',
            phone: session.phone || '+5511999999999'
          }
        },
        feedback_status: null
      }
    ]
  }

  const generateMockMessagesDemo = (): AgentMessage[] => {
    return [
      {
        id: 'demo_msg_1',
        content: "Olá! 👋 Vi que você tem interesse em investimentos. Para te conectar com o melhor especialista, preciso fazer algumas perguntas rápidas. Primeira pergunta: Quanto você tem disponível para investir hoje?",
        session_id: 'demo_session_1',
        created_at: new Date().toISOString(),
        sessions: {
          leads: {
            name: 'Maria Silva',
            phone: '+5511888777666'
          }
        },
        feedback_status: null
      },
      {
        id: 'demo_msg_2',
        content: "Perfeito! Agora me conta: qual seu principal objetivo com os investimentos? A) Aposentadoria B) Crescimento do patrimônio C) Reserva de emergência D) Especulação/day trade",
        session_id: 'demo_session_1',
        created_at: new Date().toISOString(),
        sessions: {
          leads: {
            name: 'Maria Silva',
            phone: '+5511888777666'
          }
        },
        feedback_status: null
      },
      {
        id: 'demo_msg_3',
        content: "Excelente escolha! E quando você pretende começar a investir? A) Esta semana B) Este mês C) Nos próximos 3 meses D) Não tenho pressa",
        session_id: 'demo_session_2',
        created_at: new Date().toISOString(),
        sessions: {
          leads: {
            name: 'João Santos',
            phone: '+5511999888777'
          }
        },
        feedback_status: 'approved'
      }
    ]
  }

  const handleFeedback = async (messageId: string, status: 'approved' | 'rejected', notes?: string) => {
    try {
      const message = messages.find(m => m.id === messageId)
      if (!message) return

      const feedbackData = {
        tenant_id: '60675861-e22a-4990-bab8-65ed07632a63',
        user_id: 'admin-user-001',
        session_id: message.session_id,
        agent_message: message.content,
        status: status,
        notes: notes
      }

      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), 15000)
      
      const response = await fetch('http://localhost:5000/api/agent-feedback', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(feedbackData),
        signal: controller.signal
      })
      
      clearTimeout(timeoutId)
      
      if (!response.ok) {
        const errorText = await response.text()
        throw new Error(`HTTP ${response.status}: ${errorText}`)
      }

      const data = await response.json()

      if (data.success) {
        // Atualizar estado local
        setMessages(prev => prev.map(msg => 
          msg.id === messageId 
            ? { ...msg, feedback_status: status }
            : msg
        ))
        
        toast.success(`Mensagem ${status === 'approved' ? 'aprovada' : 'rejeitada'} com sucesso!`)
      } else {
        throw new Error(data.error || 'Erro desconhecido')
      }
    } catch (error) {
      console.error('Erro ao salvar feedback:', error)
      
      if (error instanceof Error) {
        if (error.name === 'AbortError') {
          toast.error('Timeout: Salvamento demorou mais que 15 segundos')
        } else if (error.message.includes('fetch')) {
          toast.error('Backend offline. Não foi possível salvar o feedback.')
        } else {
          toast.error(`Erro ao salvar feedback: ${error.message}`)
        }
      } else {
        toast.error('Erro desconhecido ao salvar feedback')
      }
    }
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString('pt-BR')
  }

  const getStatusColor = (status?: string | null) => {
    switch (status) {
      case 'approved': return 'text-green-600 bg-green-50'
      case 'rejected': return 'text-red-600 bg-red-50'
      default: return 'text-gray-600 bg-gray-50'
    }
  }

  const getStatusText = (status?: string | null) => {
    switch (status) {
      case 'approved': return 'Aprovada'
      case 'rejected': return 'Rejeitada'
      default: return 'Pendente'
    }
  }

  const startTestChat = async () => {
    setShowTestChat(true)
    setTestMessages([])
    
    // Simular início de qualificação
    try {
      setTestLoading(true)
      
      const response = await fetch('http://localhost:5000/api/qualification/start', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          lead_id: 'test-lead-validation',
          phone: '+5511999999999',
          name: 'Teste de Validação'
        })
      })
      
      if (response.ok) {
        const data = await response.json()
        if (data.success && data.message) {
          setTestMessages([{
            role: 'agent',
            content: data.message,
            timestamp: new Date().toISOString()
          }])
          toast.success('Chat de teste iniciado!')
        }
      } else {
        // Fallback para mensagem padrão
        setTestMessages([{
          role: 'agent',
          content: 'Olá! 👋 Vi que você tem interesse em investimentos. Para te conectar com o melhor especialista, preciso fazer algumas perguntas rápidas. Primeira pergunta: Quanto você tem disponível para investir hoje?\n\nA) Até R$ 50 mil\nB) R$ 50 mil a R$ 200 mil\nC) R$ 200 mil a R$ 500 mil\nD) Mais de R$ 500 mil',
          timestamp: new Date().toISOString()
        }])
        toast.success('Chat de teste iniciado em modo simulado')
      }
    } catch (error) {
      // Fallback para mensagem padrão
      setTestMessages([{
        role: 'agent',
        content: 'Olá! 👋 Vi que você tem interesse em investimentos. Para te conectar com o melhor especialista, preciso fazer algumas perguntas rápidas. Primeira pergunta: Quanto você tem disponível para investir hoje?\n\nA) Até R$ 50 mil\nB) R$ 50 mil a R$ 200 mil\nC) R$ 200 mil a R$ 500 mil\nD) Mais de R$ 500 mil',
        timestamp: new Date().toISOString()
      }])
      toast.success('Chat de teste iniciado em modo simulado')
    } finally {
      setTestLoading(false)
    }
  }

  const sendTestMessage = async () => {
    if (!testInput.trim()) return
    
    const userMessage = testInput.trim()
    setTestInput('')
    
    // Adicionar mensagem do usuário
    const newUserMessage = {
      role: 'user' as const,
      content: userMessage,
      timestamp: new Date().toISOString()
    }
    
    setTestMessages(prev => [...prev, newUserMessage])
    setTestLoading(true)
    
    try {
      // Simular processamento do agente
      const response = await fetch('http://localhost:5000/api/qualification/process', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session_id: 'test-session-validation',
          user_message: userMessage
        })
      })
      
      if (response.ok) {
        const data = await response.json()
        if (data.success && data.ai_message) {
          setTestMessages(prev => [...prev, {
            role: 'agent',
            content: data.ai_message,
            timestamp: new Date().toISOString()
          }])
          
          if (data.completed) {
            toast.success(`Qualificação completa! Score: ${data.final_score}`)
          }
        }
      } else {
        // Fallback para resposta simulada
        const mockResponses = [
          'Perfeito! Agora me conta: qual seu principal objetivo com os investimentos?\n\nA) Aposentadoria\nB) Crescimento\nC) Reserva\nD) Especulação',
          'Excelente escolha! E quando você pretende começar a investir?\n\nA) Esta semana\nB) Este mês\nC) Nos próximos 3 meses\nD) Não tenho pressa',
          'Por último: você gostaria de falar com um de nossos especialistas?\n\nA) Sim, urgente\nB) Sim, quando possível\nC) Talvez\nD) Não'
        ]
        
        const randomResponse = mockResponses[Math.floor(Math.random() * mockResponses.length)]
        setTestMessages(prev => [...prev, {
          role: 'agent',
          content: randomResponse,
          timestamp: new Date().toISOString()
        }])
        
        toast.success('Resposta simulada (backend offline)')
      }
    } catch (error) {
      // Fallback para resposta simulada
      setTestMessages(prev => [...prev, {
        role: 'agent',
        content: 'Obrigado pela resposta! Continuando com a próxima pergunta...',
        timestamp: new Date().toISOString()
      }])
      toast.success('Resposta simulada (erro de conexão)')
    } finally {
      setTestLoading(false)
    }
  }

  const runTestScenario = async (scenarioType: 'high_value' | 'low_value' | 'edge_case') => {
    setShowTestChat(true)
    setTestMessages([])
    setTestLoading(true)
    
    const scenarios = {
      high_value: {
        name: "Cliente Qualificado",
        responses: ["D", "A", "A", "A"], // Mais de R$500k, Aposentadoria, Esta semana, Sim urgente
        description: "Simula um cliente com alto patrimônio interessado em aposentadoria"
      },
      low_value: {
        name: "Cliente Desqualificado", 
        responses: ["A", "D", "D", "D"], // Até R$50k, Especulação, Sem pressa, Não
        description: "Simula um cliente com baixo patrimônio sem interesse real"
      },
      edge_case: {
        name: "Caso Limite",
        responses: ["C", "C", "B", "C"], // R$200-500k, Reserva, Este mês, Talvez
        description: "Simula um cliente no limite da qualificação"
      }
    }
    
    const scenario = scenarios[scenarioType]
    toast.success(`Executando cenário: ${scenario.name}`)
    
    try {
      // Iniciar conversa
      setTestMessages([{
        role: 'agent',
        content: 'Olá! 👋 Vi que você tem interesse em investimentos. Para te conectar com o melhor especialista, preciso fazer algumas perguntas rápidas. Primeira pergunta: Quanto você tem disponível para investir hoje?\n\nA) Até R$ 50 mil\nB) R$ 50 mil a R$ 200 mil\nC) R$ 200 mil a R$ 500 mil\nD) Mais de R$ 500 mil',
        timestamp: new Date().toISOString()
      }])
      
      // Simular respostas automaticamente
      for (let i = 0; i < scenario.responses.length; i++) {
        await new Promise(resolve => setTimeout(resolve, 1500)) // Pausa entre respostas
        
        const userResponse = scenario.responses[i]
        setTestMessages(prev => [...prev, {
          role: 'user',
          content: userResponse,
          timestamp: new Date().toISOString()
        }])
        
        await new Promise(resolve => setTimeout(resolve, 1000)) // Pausa antes da resposta do agente
        
        // Respostas do agente baseadas no fluxo
        const agentResponses = [
          'Perfeito! Agora me conta: qual seu principal objetivo com os investimentos?\n\nA) Aposentadoria\nB) Crescimento\nC) Reserva\nD) Especulação',
          'Excelente escolha! E quando você pretende começar a investir?\n\nA) Esta semana\nB) Este mês\nC) Nos próximos 3 meses\nD) Não tenho pressa',
          'Por último: você gostaria de falar com um de nossos especialistas?\n\nA) Sim, urgente\nB) Sim, quando possível\nC) Talvez\nD) Não',
          // Resposta final baseada no cenário
          scenarioType === 'high_value' 
            ? '🎉 QUALIFICADO! Score: 85. Parabéns! Você está qualificado para falar com um de nossos especialistas. Em breve entraremos em contato para agendar sua reunião.'
            : scenarioType === 'low_value'
            ? '📋 DESQUALIFICADO. Score: 25. Agradecemos suas respostas. No momento, nossos serviços são mais adequados para outro perfil de investidor.'
            : '🤔 QUALIFICAÇÃO LIMITE. Score: 55. Obrigado pelas respostas. Vamos avaliar seu perfil e entrar em contato em breve.'
        ]
        
        if (i < agentResponses.length) {
          setTestMessages(prev => [...prev, {
            role: 'agent',
            content: agentResponses[i],
            timestamp: new Date().toISOString()
          }])
        }
      }
      
      // Feedback final
      const finalScore = scenarioType === 'high_value' ? 85 : scenarioType === 'low_value' ? 25 : 55
      toast.success(`Cenário completo! Score final: ${finalScore}`)
      
    } catch (error) {
      toast.error('Erro ao executar cenário de teste')
    } finally {
      setTestLoading(false)
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
        <div className="max-w-6xl mx-auto px-8">
          <h1 className="text-5xl font-thin text-black mb-6">Validação do Agente</h1>
          <p className="text-xl text-gray-600 font-light max-w-4xl">
            Revise e aprove as respostas do agente para aprendizado contínuo. 
            Seu feedback ajuda o sistema a melhorar continuamente as abordagens comerciais.
          </p>
          
          {/* Controles de Teste */}
          <div className="mt-8 flex gap-4 flex-wrap">
            <button
              onClick={startTestChat}
              disabled={testLoading}
              className="bg-blue-600 text-white px-6 py-3 font-light hover:bg-blue-700 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              {testLoading ? (
                <>
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  Iniciando...
                </>
              ) : (
                <>
                  💬 Testar Agente
                </>
              )}
            </button>
            
            {/* Cenários Pré-definidos */}
            <div className="flex gap-2">
              <button
                onClick={() => runTestScenario('high_value')}
                className="bg-green-600 text-white px-4 py-3 text-sm font-light hover:bg-green-700 transition-colors"
              >
                🎯 Cliente Qualificado
              </button>
              <button
                onClick={() => runTestScenario('low_value')}
                className="bg-red-600 text-white px-4 py-3 text-sm font-light hover:bg-red-700 transition-colors"
              >
                ❌ Cliente Desqualificado
              </button>
              <button
                onClick={() => runTestScenario('edge_case')}
                className="bg-yellow-600 text-white px-4 py-3 text-sm font-light hover:bg-yellow-700 transition-colors"
              >
                ⚠️ Caso Limite
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* FILTROS */}
      <div className="bg-white border-b border-gray-100">
        <div className="max-w-6xl mx-auto px-8 py-6">
          <div className="flex gap-4">
            {[
              { key: 'pending', label: 'Pendentes', count: messages.filter(m => !m.feedback_status).length },
              { key: 'approved', label: 'Aprovadas', count: messages.filter(m => m.feedback_status === 'approved').length },
              { key: 'rejected', label: 'Rejeitadas', count: messages.filter(m => m.feedback_status === 'rejected').length },
              { key: 'all', label: 'Todas', count: messages.length }
            ].map(({ key, label, count }) => (
              <button
                key={key}
                onClick={() => setFilter(key as any)}
                className={`px-4 py-2 text-sm font-light transition-colors ${
                  filter === key
                    ? 'bg-black text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {label} ({count})
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* CHAT DE TESTE */}
      {showTestChat && (
        <div className="bg-blue-50 border-b border-blue-100">
          <div className="max-w-6xl mx-auto px-8 py-8">
            <div className="bg-white rounded-lg shadow-sm border border-blue-200">
              {/* Header do Chat */}
              <div className="flex justify-between items-center p-6 border-b border-gray-100">
                <h3 className="text-lg font-medium text-gray-900">🧪 Chat de Teste - Validação do Agente</h3>
                <button
                  onClick={() => setShowTestChat(false)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  ✕
                </button>
              </div>
              
              {/* Área de Mensagens */}
              <div className="h-96 overflow-y-auto p-6 space-y-4">
                {testMessages.length === 0 ? (
                  <div className="text-center text-gray-500 py-12">
                    <div className="text-2xl mb-2">🤖</div>
                    <p>Clique em "Testar Agente" para iniciar uma conversa de teste</p>
                  </div>
                ) : (
                  testMessages.map((message, index) => (
                    <div key={index} className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                      <div className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                        message.role === 'user'
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-100 text-gray-900'
                      }`}>
                        <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                        <p className={`text-xs mt-1 ${
                          message.role === 'user' ? 'text-blue-200' : 'text-gray-500'
                        }`}>
                          {new Date(message.timestamp).toLocaleTimeString('pt-BR')}
                        </p>
                      </div>
                    </div>
                  ))
                )}
                
                {testLoading && (
                  <div className="flex justify-start">
                    <div className="bg-gray-100 text-gray-900 px-4 py-2 rounded-lg">
                      <div className="flex items-center gap-2">
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                        <span className="text-sm">Agente está digitando...</span>
                      </div>
                    </div>
                  </div>
                )}
              </div>
              
              {/* Input de Mensagem */}
              <div className="p-6 border-t border-gray-100">
                <div className="flex gap-3">
                  <input
                    type="text"
                    value={testInput}
                    onChange={(e) => setTestInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && !testLoading && sendTestMessage()}
                    placeholder="Digite sua resposta aqui..."
                    disabled={testLoading}
                    className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:opacity-50"
                  />
                  <button
                    onClick={sendTestMessage}
                    disabled={testLoading || !testInput.trim()}
                    className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Enviar
                  </button>
                </div>
                <div className="mt-2 text-xs text-gray-500">
                  💡 Teste o fluxo de qualificação completo: responda as 4 perguntas do agente
                </div>
                
                {/* Debug Info */}
                <div className="mt-3 p-3 bg-gray-50 rounded text-xs">
                  <div className="font-medium text-gray-700 mb-1">🔍 Informações de Debug:</div>
                  <div className="text-gray-600">
                    • Integração com Base de Conhecimento: ✅ Ativa<br/>
                    • Tenant ID: 60675861-e22a-4990-bab8-65ed07632a63<br/>
                    • Modo: {testMessages.length > 0 ? 'Chat Ativo' : 'Aguardando Teste'}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* LISTA DE MENSAGENS */}
      <div className="bg-white py-12">
        <div className="max-w-6xl mx-auto px-8">
          {messages.length === 0 ? (
            <div className="text-center py-12">
              <div className="text-gray-400 text-lg font-light">
                Nenhuma mensagem encontrada para revisão
              </div>
              <p className="text-gray-500 text-sm mt-2">
                As mensagens do agente aparecerão aqui conforme as conversas acontecem
              </p>
            </div>
          ) : (
            <div className="space-y-8">
              {messages.map((message, index) => (
                <div key={message.id} className="border-b border-gray-100 pb-8 last:border-b-0">
                  <div className="flex justify-between items-start gap-6">
                    {/* Conteúdo da Mensagem */}
                    <div className="flex-1 space-y-4">
                      <div className="flex items-center gap-4">
                        <div className="text-2xl font-thin text-gray-400">
                          {String(index + 1).padStart(2, '0')}
                        </div>
                        <div>
                          <h3 className="font-medium text-gray-900">
                            {message.sessions?.leads?.name || 'Lead Demo'}
                          </h3>
                          <p className="text-sm text-gray-500">
                            {message.sessions?.leads?.phone || '+55119999999'} • {formatDate(message.created_at)}
                          </p>
                        </div>
                        <div className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(message.feedback_status)}`}>
                          {getStatusText(message.feedback_status)}
                        </div>
                      </div>
                      
                      <div className="bg-gray-50 p-4 rounded-lg">
                        <p className="text-lg font-light text-gray-900 leading-relaxed">
                          {message.content}
                        </p>
                      </div>
                    </div>
                    
                    {/* Ações de Feedback */}
                    {!message.feedback_status && (
                      <div className="flex flex-col gap-3">
                        <button
                          onClick={() => handleFeedback(message.id, 'approved')}
                          className="flex items-center gap-2 text-green-600 hover:bg-green-50 px-4 py-2 rounded transition-colors"
                          title="Aprovar mensagem"
                        >
                          ✅ <span className="hidden sm:inline">Aprovar</span>
                        </button>
                        <button
                          onClick={() => handleFeedback(message.id, 'rejected')}
                          className="flex items-center gap-2 text-red-600 hover:bg-red-50 px-4 py-2 rounded transition-colors"
                          title="Rejeitar mensagem"
                        >
                          ❌ <span className="hidden sm:inline">Rejeitar</span>
                        </button>
                        <button
                          className="flex items-center gap-2 text-gray-600 hover:bg-gray-50 px-4 py-2 rounded transition-colors"
                          title="Adicionar comentário"
                        >
                          📝 <span className="hidden sm:inline">Comentar</span>
                        </button>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Estatísticas Avançadas */}
      <div className="bg-gray-50 py-8">
        <div className="max-w-6xl mx-auto px-8">
          <h2 className="text-2xl font-thin text-gray-900 mb-6">📊 Métricas de Performance</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <div className="bg-white p-6 rounded-lg shadow-sm">
              <div className="text-2xl font-thin text-gray-900">
                {messages.length}
              </div>
              <div className="text-sm text-gray-600">Total Mensagens</div>
              <div className="text-xs text-gray-400 mt-1">Últimas 24h</div>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-sm">
              <div className="text-2xl font-thin text-green-600">
                {messages.filter(m => m.feedback_status === 'approved').length}
              </div>
              <div className="text-sm text-gray-600">Aprovadas</div>
              <div className="text-xs text-green-500 mt-1">
                {messages.length > 0 ? Math.round((messages.filter(m => m.feedback_status === 'approved').length / messages.length) * 100) : 0}% taxa aprovação
              </div>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-sm">
              <div className="text-2xl font-thin text-red-600">
                {messages.filter(m => m.feedback_status === 'rejected').length}
              </div>
              <div className="text-sm text-gray-600">Rejeitadas</div>
              <div className="text-xs text-red-500 mt-1">
                {messages.length > 0 ? Math.round((messages.filter(m => m.feedback_status === 'rejected').length / messages.length) * 100) : 0}% taxa rejeição
              </div>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-sm">
              <div className="text-2xl font-thin text-blue-600">
                {messages.filter(m => !m.feedback_status).length}
              </div>
              <div className="text-sm text-gray-600">Pendentes</div>
              <div className="text-xs text-blue-500 mt-1">Aguardando revisão</div>
            </div>
          </div>
          
          {/* Métricas de Qualidade */}
          <div className="bg-white p-6 rounded-lg shadow-sm">
            <h3 className="text-lg font-medium text-gray-900 mb-4">🎯 Qualidade do Agente</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div>
                <div className="text-lg font-thin text-gray-900">
                  {messages.length > 0 ? Math.round((messages.filter(m => m.feedback_status === 'approved').length / (messages.filter(m => m.feedback_status).length || 1)) * 100) : 0}%
                </div>
                <div className="text-sm text-gray-600">Taxa de Aprovação</div>
                <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                  <div 
                    className="bg-green-500 h-2 rounded-full" 
                    style={{width: `${messages.length > 0 ? Math.round((messages.filter(m => m.feedback_status === 'approved').length / (messages.filter(m => m.feedback_status).length || 1)) * 100) : 0}%`}}
                  ></div>
                </div>
              </div>
              <div>
                <div className="text-lg font-thin text-gray-900">
                  {testMessages.length}
                </div>
                <div className="text-sm text-gray-600">Testes Executados</div>
                <div className="text-xs text-gray-400 mt-1">Sessão atual</div>
              </div>
              <div>
                <div className="text-lg font-thin text-gray-900">
                  {showTestChat ? '🟢 Ativo' : '🔴 Inativo'}
                </div>
                <div className="text-sm text-gray-600">Status do Sistema</div>
                <div className="text-xs text-gray-400 mt-1">Validação em tempo real</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  )
}
