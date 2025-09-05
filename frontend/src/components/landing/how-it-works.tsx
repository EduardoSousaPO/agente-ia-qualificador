'use client'

import { 
  UserPlusIcon,
  ChatBubbleLeftRightIcon,
  CpuChipIcon,
  HandRaisedIcon
} from '@heroicons/react/24/outline'

const steps = [
  {
    icon: UserPlusIcon,
    title: 'Lead Intake',
    description: 'Recebe leads de YouTube, newsletters, landing pages ou adiciona manualmente.'
  },
  {
    icon: ChatBubbleLeftRightIcon,
    title: 'Conversa IA',
    description: 'IA inicia conversa no WhatsApp coletando patrimônio, objetivos e urgência.'
  },
  {
    icon: CpuChipIcon,
    title: 'Qualificação',
    description: 'Sistema analisa respostas e atribui score baseado em critérios.'
  },
  {
    icon: HandRaisedIcon,
    title: 'Handoff',
    description: 'Lead qualificado entregue com resumo e sugestões de agendamento.'
  }
]

export function HowItWorksSimple() {
  return (
    <div className="py-16 bg-gray-50">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            Como funciona?
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Processo automatizado que transforma leads frios em oportunidades qualificadas
          </p>
        </div>

        {/* Steps */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {steps.map((step, index) => (
            <div key={index} className="text-center">
              {/* Step Number */}
              <div className="inline-flex items-center justify-center w-10 h-10 bg-blue-600 text-white rounded-full text-lg font-bold mb-4">
                {index + 1}
              </div>

              {/* Icon */}
              <div className="inline-flex items-center justify-center w-16 h-16 bg-white rounded-xl shadow-sm mb-4">
                <step.icon className="w-8 h-8 text-blue-600" />
              </div>

              {/* Content */}
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                {step.title}
              </h3>
              
              <p className="text-gray-600 text-sm">
                {step.description}
              </p>
            </div>
          ))}
        </div>

        {/* Simple Flow */}
        <div className="mt-12 text-center">
          <div className="inline-flex items-center space-x-4 bg-white rounded-lg px-6 py-3 shadow-sm">
            <span className="text-sm font-medium text-gray-700">Lead</span>
            <div className="text-gray-400">→</div>
            <span className="text-sm font-medium text-gray-700">WhatsApp</span>
            <div className="text-gray-400">→</div>
            <span className="text-sm font-medium text-gray-700">IA</span>
            <div className="text-gray-400">→</div>
            <span className="text-sm font-medium text-blue-600">Qualificado</span>
          </div>
        </div>
      </div>
    </div>
  )
}
