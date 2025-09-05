'use client'

import { 
  ChatBubbleLeftRightIcon,
  CpuChipIcon,
  ClockIcon,
  ChartBarIcon
} from '@heroicons/react/24/outline'

const benefits = [
  {
    icon: ChatBubbleLeftRightIcon,
    title: 'Conversas Naturais',
    description: 'IA conduz qualificação via WhatsApp coletando informações sobre patrimônio, objetivos e urgência.'
  },
  {
    icon: CpuChipIcon,
    title: 'Qualificação Automática',
    description: 'Sistema analisa respostas e qualifica leads baseado em critérios de investimento pré-definidos.'
  },
  {
    icon: ClockIcon,
    title: 'Funciona 24/7',
    description: 'Qualifica leads automaticamente mesmo fora do horário comercial, maximizando oportunidades.'
  },
  {
    icon: ChartBarIcon,
    title: 'Dashboard Completo',
    description: 'Interface para gestão de leads e acompanhamento de conversões em tempo real.'
  }
]

export function WhyUseSection() {
  return (
    <div className="py-16 bg-white">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            Por que usar o Agente Qualificador?
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Automatize todo o processo de qualificação, desde o primeiro contato 
            até a entrega do lead qualificado para seu time.
          </p>
        </div>

        {/* Benefits Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {benefits.map((benefit, index) => (
            <div 
              key={index}
              className="text-center group"
            >
              <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-100 rounded-xl mb-4 group-hover:bg-blue-200 transition-colors">
                <benefit.icon className="w-8 h-8 text-blue-600" />
              </div>
              
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                {benefit.title}
              </h3>
              
              <p className="text-gray-600 text-sm">
                {benefit.description}
              </p>
            </div>
          ))}
        </div>

        {/* Stats */}
        <div className="mt-12 text-center">
          <div className="inline-flex items-center space-x-8 bg-gray-50 rounded-lg px-8 py-4">
            <div>
              <div className="text-2xl font-bold text-blue-600">85%</div>
              <div className="text-sm text-gray-600">Taxa de Resposta</div>
            </div>
            <div className="w-px h-8 bg-gray-300"></div>
            <div>
              <div className="text-2xl font-bold text-blue-600">3x</div>
              <div className="text-sm text-gray-600">Mais Leads Qualificados</div>
            </div>
            <div className="w-px h-8 bg-gray-300"></div>
            <div>
              <div className="text-2xl font-bold text-blue-600">24/7</div>
              <div className="text-sm text-gray-600">Automação</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}











