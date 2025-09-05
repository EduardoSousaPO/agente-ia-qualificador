'use client'

import { useState, useEffect, useRef } from 'react'
import { useParams } from 'next/navigation'
import { DashboardLayout } from '@/components/layout/dashboard-layout'
import { ChatInterface } from '@/components/conversations/chat-interface'
import { ConversationHeader } from '@/components/conversations/conversation-header'
import { ConversationSidebar } from '@/components/conversations/conversation-sidebar'
import { api } from '@/lib/api'
import { Session, Message, Lead } from '@/types'
import { LoadingSpinner } from '@/components/ui/loading-spinner'
import toast from 'react-hot-toast'

export default function ConversationPage() {
  const params = useParams()
  const sessionId = params.id as string
  
  const [session, setSession] = useState<Session | null>(null)
  const [messages, setMessages] = useState<Message[]>([])
  const [lead, setLead] = useState<Lead | null>(null)
  const [loading, setLoading] = useState(true)
  const [sending, setSending] = useState(false)
  const [humanTakeover, setHumanTakeover] = useState(false)
  
  const messagesEndRef = useRef<HTMLDivElement | null>(null)

  useEffect(() => {
    if (sessionId) {
      loadConversationData()
    }
  }, [sessionId])

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const loadConversationData = async () => {
    try {
      setLoading(true)
      
      // Carregar sessão e mensagens em paralelo
      const [sessionResponse, messagesResponse] = await Promise.all([
        api.getSession(sessionId),
        api.getMessages(sessionId)
      ])
      
      setSession(sessionResponse)
      setMessages(messagesResponse.data)
      
      // Carregar dados do lead se disponível
      if (sessionResponse.lead_id) {
        const leadResponse = await api.getLead(sessionResponse.lead_id)
        setLead(leadResponse)
      }
      
      setHumanTakeover(sessionResponse.human_takeover || false)
    } catch (error) {
      console.error('Erro ao carregar conversa:', error)
      toast.error('Erro ao carregar conversa')
    } finally {
      setLoading(false)
    }
  }

  const handleSendMessage = async (content: string) => {
    if (!session || sending) return

    try {
      setSending(true)
      
      const response = await api.sendMessage({
        session_id: sessionId,
        message: content,
        is_ai: false
      })

      // Adicionar mensagem do usuário
      const userMessage: Message = {
        id: `temp-${Date.now()}`,
        session_id: sessionId,
        content,
        is_ai: false,
        created_at: new Date().toISOString(),
        tenant_id: session.tenant_id
      }
      
      setMessages(prev => [...prev, userMessage])
      
      // Se não estiver em takeover humano, adicionar resposta da IA
      if (!humanTakeover && response.ai_response) {
        const aiMessage: Message = {
          id: `ai-${Date.now()}`,
          session_id: sessionId,
          content: response.ai_response,
          is_ai: true,
          created_at: new Date().toISOString(),
          tenant_id: session.tenant_id
        }
        
        setTimeout(() => {
          setMessages(prev => [...prev, aiMessage])
        }, 1000) // Simular delay da IA
      }
      
      // Recarregar dados se houve mudança de status
      if (response.status_changed) {
        loadConversationData()
      }
      
    } catch (error: any) {
      console.error('Erro ao enviar mensagem:', error)
      toast.error(error.response?.data?.error || 'Erro ao enviar mensagem')
    } finally {
      setSending(false)
    }
  }

  const handleTakeoverToggle = async () => {
    if (!session) return

    try {
      await api.toggleHumanTakeover(sessionId, !humanTakeover)
      setHumanTakeover(!humanTakeover)
      
      toast.success(
        humanTakeover 
          ? 'IA reativada para esta conversa' 
          : 'Conversa assumida por humano'
      )
    } catch (error: any) {
      console.error('Erro ao alterar takeover:', error)
      toast.error(error.response?.data?.error || 'Erro ao alterar controle da conversa')
    }
  }

  const handleManualQualification = async () => {
    if (!session?.lead_id) return

    try {
      await api.manualQualification(session.lead_id)
      toast.success('Lead qualificado manualmente')
      loadConversationData()
    } catch (error: any) {
      console.error('Erro na qualificação manual:', error)
      toast.error(error.response?.data?.error || 'Erro na qualificação manual')
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

  if (!session) {
    return (
      <DashboardLayout>
        <div className="text-center py-12">
          <h3 className="text-lg font-medium text-gray-900">Conversa não encontrada</h3>
          <p className="mt-2 text-sm text-gray-500">
            A conversa solicitada não existe ou você não tem permissão para acessá-la.
          </p>
        </div>
      </DashboardLayout>
    )
  }

  return (
    <DashboardLayout>
      <div className="h-full flex flex-col">
        {/* Header */}
        <ConversationHeader
          session={session}
          lead={lead}
          humanTakeover={humanTakeover}
          onTakeoverToggle={handleTakeoverToggle}
          onManualQualification={handleManualQualification}
        />

        {/* Main Content */}
        <div className="flex-1 flex overflow-hidden">
          {/* Chat Interface */}
          <div className="flex-1 flex flex-col">
            <ChatInterface
              messages={messages}
              onSendMessage={handleSendMessage}
              sending={sending}
              humanTakeover={humanTakeover}
              messagesEndRef={messagesEndRef}
            />
          </div>

          {/* Sidebar */}
          <div className="w-80 border-l border-gray-200">
            <ConversationSidebar
              session={session}
              lead={lead}
              onDataUpdate={loadConversationData}
            />
          </div>
        </div>
      </div>
    </DashboardLayout>
  )
}




