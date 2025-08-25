'use client'

import { useState, useEffect } from 'react'
import { PlayIcon, PauseIcon, StopIcon, ForwardIcon } from '@heroicons/react/24/outline'

interface Message {
  id: string
  sender: 'user' | 'ai'
  content: string
  timestamp: string
  delay?: number
}

interface ConversationTemplate {
  id: string
  title: string
  leadName: string
  expectedScore: number
  messages: Message[]
}

const conversationTemplates: ConversationTemplate[] = [
  {
    id: 'quick-qualified',
    title: '⚡ Qualificação Rápida (2 min)',
    leadName: 'Roberto Silva',
    expectedScore: 90,
    messages: [
      {
        id: '1',
        sender: 'ai',
        content: 'Olá Roberto! 👋 Vi que você tem interesse em investimentos. Posso fazer algumas perguntas rápidas?',
        timestamp: '14:30',
        delay: 1000
      },
      {
        id: '2',
        sender: 'user',
        content: 'Claro! Pode perguntar.',
        timestamp: '14:30',
        delay: 2000
      },
      {
        id: '3',
        sender: 'ai',
        content: 'Quanto você tem disponível para investir?\nA) Até R$ 50k B) R$ 50-200k C) R$ 200-500k D) +R$ 500k',
        timestamp: '14:31',
        delay: 1500
      },
      {
        id: '4',
        sender: 'user',
        content: 'D - Tenho R$ 600 mil',
        timestamp: '14:31',
        delay: 3000
      },
      {
        id: '5',
        sender: 'ai',
        content: 'Excelente! Qual seu objetivo?\nA) Aposentadoria B) Crescimento C) Reserva D) Especulação',
        timestamp: '14:32',
        delay: 1500
      },
      {
        id: '6',
        sender: 'user',
        content: 'A - Aposentadoria',
        timestamp: '14:32',
        delay: 2000
      },
      {
        id: '7',
        sender: 'ai',
        content: 'Quando pretende começar?\nA) Esta semana B) Este mês C) 3 meses D) Sem pressa',
        timestamp: '14:33',
        delay: 1500
      },
      {
        id: '8',
        sender: 'user',
        content: 'A - Esta semana',
        timestamp: '14:33',
        delay: 2000
      },
      {
        id: '9',
        sender: 'ai',
        content: 'Gostaria de falar com nosso especialista?\nA) Sim, urgente B) Sim, possível C) Talvez D) Não',
        timestamp: '14:34',
        delay: 1500
      },
      {
        id: '10',
        sender: 'user',
        content: 'A - Sim, urgente!',
        timestamp: '14:34',
        delay: 2000
      },
      {
        id: '11',
        sender: 'ai',
        content: '🎯 QUALIFICADO! Score: 90/100\n\nNosso especialista ligará em 1 hora. Horários disponíveis:\n• 16h-17h\n• 17h-18h\n\nQual prefere?',
        timestamp: '14:35',
        delay: 2000
      },
      {
        id: '12',
        sender: 'user',
        content: 'Perfeito! 16h está ótimo.',
        timestamp: '14:35',
        delay: 1500
      }
    ]
  },
  {
    id: 'nurturing-case',
    title: '📚 Caso de Nurturing (3 min)',
    leadName: 'Fernanda Costa',
    expectedScore: 55,
    messages: [
      {
        id: '1',
        sender: 'ai',
        content: 'Oi Fernanda! 👋 Vi que você se inscreveu na nossa newsletter. Posso te ajudar com algumas dúvidas sobre investimentos?',
        timestamp: '10:15',
        delay: 1000
      },
      {
        id: '2',
        sender: 'user',
        content: 'Oi! Sim, estou começando a me interessar por investimentos.',
        timestamp: '10:16',
        delay: 3000
      },
      {
        id: '3',
        sender: 'ai',
        content: 'Que legal! Quanto você tem disponível para começar?\nA) Até R$ 50k B) R$ 50-200k C) R$ 200-500k D) +R$ 500k',
        timestamp: '10:16',
        delay: 1500
      },
      {
        id: '4',
        sender: 'user',
        content: 'A - Tenho uns R$ 30 mil guardados',
        timestamp: '10:17',
        delay: 4000
      },
      {
        id: '5',
        sender: 'ai',
        content: 'Ótimo começo! Qual seu objetivo principal?\nA) Aposentadoria B) Crescimento C) Reserva D) Especulação',
        timestamp: '10:17',
        delay: 1500
      },
      {
        id: '6',
        sender: 'user',
        content: 'B - Quero fazer o dinheiro crescer, mas não sei muito sobre isso',
        timestamp: '10:18',
        delay: 5000
      },
      {
        id: '7',
        sender: 'ai',
        content: 'Entendo! Todos começaram assim. Quando pretende começar?\nA) Esta semana B) Este mês C) 3 meses D) Sem pressa',
        timestamp: '10:18',
        delay: 1500
      },
      {
        id: '8',
        sender: 'user',
        content: 'C - Quero estudar mais antes, uns 3 meses',
        timestamp: '10:19',
        delay: 4000
      },
      {
        id: '9',
        sender: 'ai',
        content: 'Muito sensato! Gostaria de falar com um especialista?\nA) Sim, urgente B) Sim, possível C) Talvez D) Não',
        timestamp: '10:19',
        delay: 1500
      },
      {
        id: '10',
        sender: 'user',
        content: 'C - Talvez... ainda estou aprendendo',
        timestamp: '10:20',
        delay: 4000
      },
      {
        id: '11',
        sender: 'ai',
        content: '📚 Score: 55/100 - Recomendo nossos materiais educativos:\n\n• Guia do Investidor Iniciante\n• Webinar: Primeiros Passos\n• Simulador de Investimentos\n\n🔗 www.exemplo.com/educacao\n\nQuando se sentir pronta, estaremos aqui! 😊',
        timestamp: '10:20',
        delay: 2500
      },
      {
        id: '12',
        sender: 'user',
        content: 'Perfeito! Vou estudar esse material. Obrigada!',
        timestamp: '10:21',
        delay: 3000
      }
    ]
  }
]

interface ConversationSimulatorProps {
  template?: ConversationTemplate
  onComplete?: (score: number) => void
}

export function ConversationSimulator({ template, onComplete }: ConversationSimulatorProps) {
  const [selectedTemplate, setSelectedTemplate] = useState<ConversationTemplate | null>(template || null)
  const [currentMessages, setCurrentMessages] = useState<Message[]>([])
  const [currentIndex, setCurrentIndex] = useState(0)
  const [isPlaying, setIsPlaying] = useState(false)
  const [isPaused, setIsPaused] = useState(false)
  const [speed, setSpeed] = useState(1)

  useEffect(() => {
    if (!selectedTemplate || !isPlaying || isPaused) return

    if (currentIndex >= selectedTemplate.messages.length) {
      setIsPlaying(false)
      onComplete?.(selectedTemplate.expectedScore)
      return
    }

    const message = selectedTemplate.messages[currentIndex]
    const delay = (message.delay || 2000) / speed

    const timer = setTimeout(() => {
      setCurrentMessages(prev => [...prev, message])
      setCurrentIndex(prev => prev + 1)
    }, delay)

    return () => clearTimeout(timer)
  }, [selectedTemplate, currentIndex, isPlaying, isPaused, speed, onComplete])

  const startSimulation = (template: ConversationTemplate) => {
    setSelectedTemplate(template)
    setCurrentMessages([])
    setCurrentIndex(0)
    setIsPlaying(true)
    setIsPaused(false)
  }

  const pauseSimulation = () => {
    setIsPaused(!isPaused)
  }

  const stopSimulation = () => {
    setIsPlaying(false)
    setIsPaused(false)
    setCurrentMessages([])
    setCurrentIndex(0)
  }

  const skipToEnd = () => {
    if (!selectedTemplate) return
    setCurrentMessages(selectedTemplate.messages)
    setCurrentIndex(selectedTemplate.messages.length)
    setIsPlaying(false)
    onComplete?.(selectedTemplate.expectedScore)
  }

  if (!template && !selectedTemplate) {
    return (
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">🎬 Simulador de Conversas</h3>
          <p className="card-description">
            Veja conversas de qualificação em tempo real
          </p>
        </div>

        <div className="p-6 space-y-4">
          {conversationTemplates.map((template) => (
            <div
              key={template.id}
              className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 cursor-pointer transition-colors"
              onClick={() => startSimulation(template)}
            >
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="font-medium text-gray-900">{template.title}</h4>
                  <p className="text-sm text-gray-600">Lead: {template.leadName}</p>
                </div>
                <div className="text-right">
                  <div className="text-lg font-bold text-blue-600">
                    {template.expectedScore}
                  </div>
                  <div className="text-xs text-gray-500">
                    {template.messages.length} mensagens
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="card">
      <div className="card-header">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="card-title">
              {selectedTemplate?.title || 'Simulador de Conversa'}
            </h3>
            <p className="card-description">
              Lead: {selectedTemplate?.leadName} | Score Esperado: {selectedTemplate?.expectedScore}/100
            </p>
          </div>
          
          {/* Controles */}
          <div className="flex items-center gap-2">
            {/* Speed Control */}
            <select
              value={speed}
              onChange={(e) => setSpeed(Number(e.target.value))}
              className="text-sm border border-gray-300 rounded px-2 py-1"
            >
              <option value={0.5}>0.5x</option>
              <option value={1}>1x</option>
              <option value={2}>2x</option>
              <option value={4}>4x</option>
            </select>

            {/* Play/Pause */}
            <button
              onClick={pauseSimulation}
              disabled={!isPlaying}
              className="p-2 rounded bg-blue-100 text-blue-600 hover:bg-blue-200 disabled:opacity-50"
            >
              {isPaused ? <PlayIcon className="h-4 w-4" /> : <PauseIcon className="h-4 w-4" />}
            </button>

            {/* Stop */}
            <button
              onClick={stopSimulation}
              className="p-2 rounded bg-red-100 text-red-600 hover:bg-red-200"
            >
              <StopIcon className="h-4 w-4" />
            </button>

            {/* Skip to End */}
            <button
              onClick={skipToEnd}
              disabled={!isPlaying}
              className="p-2 rounded bg-gray-100 text-gray-600 hover:bg-gray-200 disabled:opacity-50"
            >
              <ForwardIcon className="h-4 w-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Chat Area */}
      <div className="p-6">
        <div className="bg-gray-50 rounded-lg p-4 h-96 overflow-y-auto space-y-3">
          {currentMessages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div className={`max-w-[80%] rounded-lg p-3 ${
                message.sender === 'user'
                  ? 'bg-blue-500 text-white'
                  : 'bg-white text-gray-900 border border-gray-200'
              }`}>
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-xs font-medium">
                    {message.sender === 'user' ? selectedTemplate?.leadName : 'IA Qualificador'}
                  </span>
                  <span className="text-xs opacity-75">{message.timestamp}</span>
                </div>
                <div className="text-sm whitespace-pre-line">
                  {message.content}
                </div>
              </div>
            </div>
          ))}

          {/* Typing Indicator */}
          {isPlaying && !isPaused && currentIndex < (selectedTemplate?.messages.length || 0) && (
            <div className="flex justify-start">
              <div className="bg-white border border-gray-200 rounded-lg p-3 max-w-[80%]">
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-xs font-medium">IA Qualificador</span>
                </div>
                <div className="flex items-center gap-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                  <span className="text-xs text-gray-500 ml-2">digitando...</span>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Progress Bar */}
        <div className="mt-4">
          <div className="flex justify-between text-sm text-gray-600 mb-1">
            <span>Progresso</span>
            <span>{currentIndex}/{selectedTemplate?.messages.length || 0}</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-blue-600 h-2 rounded-full transition-all duration-300"
              style={{
                width: `${((currentIndex) / (selectedTemplate?.messages.length || 1)) * 100}%`
              }}
            ></div>
          </div>
        </div>

        {/* Final Result */}
        {currentIndex >= (selectedTemplate?.messages.length || 0) && !isPlaying && (
          <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-lg">
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600 mb-2">
                Score Final: {selectedTemplate?.expectedScore}/100
              </div>
              <div className={`px-4 py-2 rounded-full inline-block ${
                (selectedTemplate?.expectedScore || 0) >= 70
                  ? 'bg-green-100 text-green-800'
                  : 'bg-red-100 text-red-800'
              }`}>
                {(selectedTemplate?.expectedScore || 0) >= 70 ? '✅ QUALIFICADO' : '❌ NÃO QUALIFICADO'}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}


