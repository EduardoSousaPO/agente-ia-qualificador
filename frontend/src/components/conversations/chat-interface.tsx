'use client'

import { useState, useRef, useEffect } from 'react'
import { Message } from '@/types'
import { formatDateTime, getInitials, getAvatarColor } from '@/lib/utils'
import { 
  PaperAirplaneIcon, 
  UserIcon, 
  ComputerDesktopIcon,
  ExclamationTriangleIcon 
} from '@heroicons/react/24/outline'
import { LoadingSpinner } from '@/components/ui/loading-spinner'

interface ChatInterfaceProps {
  messages: Message[]
  onSendMessage: (content: string) => void
  sending: boolean
  humanTakeover: boolean
  messagesEndRef: React.RefObject<HTMLDivElement>
}

export function ChatInterface({
  messages,
  onSendMessage,
  sending,
  humanTakeover,
  messagesEndRef
}: ChatInterfaceProps) {
  const [newMessage, setNewMessage] = useState('')
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!newMessage.trim() || sending) return
    
    onSendMessage(newMessage.trim())
    setNewMessage('')
    
    // Reset textarea height
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  const adjustTextareaHeight = () => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`
    }
  }

  useEffect(() => {
    adjustTextareaHeight()
  }, [newMessage])

  return (
    <div className="flex flex-col h-full">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.length === 0 ? (
          <div className="text-center py-12">
            <div className="mx-auto h-12 w-12 text-gray-400 mb-4">
              <ComputerDesktopIcon className="w-full h-full" />
            </div>
            <h3 className="text-lg font-medium text-gray-900">Conversa iniciada</h3>
            <p className="mt-2 text-sm text-gray-500">
              As mensagens aparecerão aqui conforme a conversa progride.
            </p>
          </div>
        ) : (
          messages.map((message, index) => (
            <div
              key={message.id}
              className={`flex ${message.is_ai ? 'justify-start' : 'justify-end'}`}
            >
              <div className={`flex max-w-xs lg:max-w-md ${message.is_ai ? 'flex-row' : 'flex-row-reverse'}`}>
                {/* Avatar */}
                <div className={`flex-shrink-0 ${message.is_ai ? 'mr-3' : 'ml-3'}`}>
                  {message.is_ai ? (
                    <div className="h-8 w-8 rounded-full bg-blue-500 flex items-center justify-center">
                      <ComputerDesktopIcon className="h-4 w-4 text-white" />
                    </div>
                  ) : (
                    <div className="h-8 w-8 rounded-full bg-green-500 flex items-center justify-center">
                      <UserIcon className="h-4 w-4 text-white" />
                    </div>
                  )}
                </div>

                {/* Message Bubble */}
                <div className="flex flex-col">
                  <div
                    className={`px-4 py-2 rounded-lg ${
                      message.is_ai
                        ? 'bg-gray-100 text-gray-900'
                        : 'bg-primary-600 text-white'
                    }`}
                  >
                    <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                  </div>
                  
                  {/* Timestamp */}
                  <div className={`mt-1 text-xs text-gray-500 ${message.is_ai ? 'text-left' : 'text-right'}`}>
                    {formatDateTime(message.created_at)}
                  </div>
                </div>
              </div>
            </div>
          ))
        )}

        {/* Typing Indicator */}
        {sending && (
          <div className="flex justify-start">
            <div className="flex max-w-xs lg:max-w-md">
              <div className="flex-shrink-0 mr-3">
                <div className="h-8 w-8 rounded-full bg-blue-500 flex items-center justify-center">
                  <ComputerDesktopIcon className="h-4 w-4 text-white" />
                </div>
              </div>
              <div className="bg-gray-100 rounded-lg px-4 py-2">
                <div className="flex items-center space-x-1">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-gray-500 rounded-full animate-pulse"></div>
                    <div className="w-2 h-2 bg-gray-500 rounded-full animate-pulse" style={{ animationDelay: '0.1s' }}></div>
                    <div className="w-2 h-2 bg-gray-500 rounded-full animate-pulse" style={{ animationDelay: '0.2s' }}></div>
                  </div>
                  <span className="text-xs text-gray-500 ml-2">IA digitando...</span>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Scroll anchor */}
        <div ref={messagesEndRef} />
      </div>

      {/* Message Input */}
      <div className="border-t border-gray-200 bg-white p-4">
        {/* Takeover Warning */}
        {!humanTakeover && (
          <div className="mb-3 flex items-center space-x-2 text-sm text-amber-700 bg-amber-50 rounded-lg p-3">
            <ExclamationTriangleIcon className="h-5 w-5 flex-shrink-0" />
            <span>
              A IA está controlando esta conversa. Suas mensagens serão enviadas, mas a IA pode responder automaticamente.
            </span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="flex items-end space-x-3">
          <div className="flex-1">
            <textarea
              ref={textareaRef}
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={humanTakeover ? "Digite sua mensagem..." : "Digite uma mensagem (IA ativa)..."}
              className="block w-full resize-none rounded-lg border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 text-sm"
              rows={1}
              style={{ minHeight: '40px', maxHeight: '120px' }}
              disabled={sending}
            />
          </div>
          
          <button
            type="submit"
            disabled={!newMessage.trim() || sending}
            className="inline-flex items-center justify-center w-10 h-10 rounded-lg bg-primary-600 text-white hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {sending ? (
              <LoadingSpinner size="sm" />
            ) : (
              <PaperAirplaneIcon className="h-5 w-5" />
            )}
          </button>
        </form>

        {/* Quick Actions */}
        {humanTakeover && (
          <div className="mt-3 flex flex-wrap gap-2">
            <button
              onClick={() => setNewMessage('Olá! Como posso ajudá-lo hoje?')}
              className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-700 hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              Saudação
            </button>
            <button
              onClick={() => setNewMessage('Poderia me contar mais sobre seus objetivos de investimento?')}
              className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-700 hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              Objetivos
            </button>
            <button
              onClick={() => setNewMessage('Qual seria o valor aproximado que você tem disponível para investir?')}
              className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-700 hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              Patrimônio
            </button>
            <button
              onClick={() => setNewMessage('Gostaria de agendar uma conversa com nosso especialista?')}
              className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-700 hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              Agendamento
            </button>
          </div>
        )}
      </div>
    </div>
  )
}




