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

  useEffect(() => {
    loadAgentMessages()
  }, [filter])

  const loadAgentMessages = async () => {
    try {
      setLoading(true)
      
      // Buscar mensagens de todas as sessões ativas
      const sessionsResponse = await fetch('/api/chat/sessions')
      const sessionsData = await sessionsResponse.json()
      
      if (sessionsData.data && sessionsData.data.length > 0) {
        // Para cada sessão, buscar mensagens do agente
        const allMessages: AgentMessage[] = []
        
        for (const session of sessionsData.data.slice(0, 5)) { // Limitar para demo
          try {
            const messagesResponse = await fetch(`/api/agent-messages/${session.id}`)
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

      const response = await fetch('/api/agent-feedback', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(feedbackData)
      })

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
      toast.error('Erro ao salvar feedback')
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

      {/* Estatísticas */}
      <div className="bg-gray-50 py-8">
        <div className="max-w-6xl mx-auto px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="text-center">
              <div className="text-2xl font-thin text-gray-900">
                {messages.length}
              </div>
              <div className="text-sm text-gray-600">Total Mensagens</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-thin text-green-600">
                {messages.filter(m => m.feedback_status === 'approved').length}
              </div>
              <div className="text-sm text-gray-600">Aprovadas</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-thin text-red-600">
                {messages.filter(m => m.feedback_status === 'rejected').length}
              </div>
              <div className="text-sm text-gray-600">Rejeitadas</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-thin text-gray-600">
                {messages.filter(m => !m.feedback_status).length}
              </div>
              <div className="text-sm text-gray-600">Pendentes</div>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  )
}
