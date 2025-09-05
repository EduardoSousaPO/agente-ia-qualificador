'use client'

import { useState } from 'react'
import { ChartBarIcon, UserIcon, TrophyIcon, ExclamationTriangleIcon } from '@heroicons/react/24/outline'

interface QualificationScenario {
  id: string
  title: string
  description: string
  score: number
  qualified: boolean
  icon: React.ComponentType<any>
  color: string
  example: {
    name: string
    responses: string[]
    reasoning: string
  }
}

const scenarios: QualificationScenario[] = [
  {
    id: 'high-value',
    title: 'Lead Premium',
    description: 'Alto patrimônio + urgência máxima',
    score: 95,
    qualified: true,
    icon: TrophyIcon,
    color: 'green',
    example: {
      name: 'Carlos Eduardo (CEO)',
      responses: [
        'D - Mais de R$ 500 mil',
        'A - Aposentadoria',
        'A - Esta semana',
        'A - Sim, urgente'
      ],
      reasoning: 'Perfil ideal: alto patrimônio, objetivo claro, urgência máxima e interesse imediato. Prioridade máxima para especialista sênior.'
    }
  },
  {
    id: 'experienced',
    title: 'Investidor Experiente',
    description: 'Conhecimento + diversificação',
    score: 80,
    qualified: true,
    icon: UserIcon,
    color: 'blue',
    example: {
      name: 'Maria Fernanda (Empresária)',
      responses: [
        'C - R$ 200-500 mil',
        'B - Crescimento patrimonial',
        'B - Este mês',
        'B - Sim, quando possível'
      ],
      reasoning: 'Investidor experiente buscando diversificação. Bom patrimônio, objetivo claro e interesse genuíno. Ideal para consultoria técnica.'
    }
  },
  {
    id: 'potential',
    title: 'Potencial Futuro',
    description: 'Bom perfil, mas sem urgência',
    score: 65,
    qualified: false,
    icon: ChartBarIcon,
    color: 'yellow',
    example: {
      name: 'Ana Paula (Profissional Liberal)',
      responses: [
        'B - R$ 50-200 mil',
        'B - Crescimento',
        'C - 3 meses',
        'C - Talvez'
      ],
      reasoning: 'Lead com potencial mas ainda em fase de educação. Ideal para nurturing com conteúdo educativo até estar pronto.'
    }
  },
  {
    id: 'speculative',
    title: 'Perfil Especulativo',
    description: 'Baixo patrimônio + day trade',
    score: 25,
    qualified: false,
    icon: ExclamationTriangleIcon,
    color: 'red',
    example: {
      name: 'João Silva (Estudante)',
      responses: [
        'A - Até R$ 50 mil',
        'D - Day trade',
        'D - Sem pressa',
        'D - Não, obrigado'
      ],
      reasoning: 'Perfil especulativo com baixo patrimônio. Não adequado para consultoria paga. Oferecer conteúdo educativo sobre riscos.'
    }
  }
]

export function QualificationScenarios() {
  const [selectedScenario, setSelectedScenario] = useState<QualificationScenario | null>(null)

  const getColorClasses = (color: string, qualified: boolean) => {
    const baseClasses = {
      green: qualified ? 'bg-green-50 border-green-200 text-green-800' : 'bg-gray-50 border-gray-200 text-gray-600',
      blue: qualified ? 'bg-blue-50 border-blue-200 text-blue-800' : 'bg-gray-50 border-gray-200 text-gray-600',
      yellow: 'bg-yellow-50 border-yellow-200 text-yellow-800',
      red: 'bg-red-50 border-red-200 text-red-800'
    }
    return baseClasses[color as keyof typeof baseClasses] || baseClasses.green
  }

  const getIconColorClasses = (color: string, qualified: boolean) => {
    const iconClasses = {
      green: qualified ? 'text-green-600' : 'text-gray-400',
      blue: qualified ? 'text-blue-600' : 'text-gray-400',
      yellow: 'text-yellow-600',
      red: 'text-red-600'
    }
    return iconClasses[color as keyof typeof iconClasses] || iconClasses.green
  }

  return (
    <div className="card">
      <div className="card-header">
        <h3 className="card-title">🎯 Cenários de Qualificação</h3>
        <p className="card-description">
          Exemplos de diferentes tipos de leads e como a IA os qualifica
        </p>
      </div>

      <div className="p-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {scenarios.map((scenario) => {
            const IconComponent = scenario.icon
            return (
              <div
                key={scenario.id}
                className={`border rounded-lg p-4 cursor-pointer transition-all hover:shadow-md ${
                  getColorClasses(scenario.color, scenario.qualified)
                }`}
                onClick={() => setSelectedScenario(scenario)}
              >
                <div className="flex items-center justify-between mb-3">
                  <IconComponent className={`h-6 w-6 ${getIconColorClasses(scenario.color, scenario.qualified)}`} />
                  <div className={`text-lg font-bold ${
                    scenario.qualified ? 'text-green-600' : 'text-red-600'
                  }`}>
                    {scenario.score}
                  </div>
                </div>
                
                <h4 className="font-medium mb-1">{scenario.title}</h4>
                <p className="text-sm opacity-75 mb-3">{scenario.description}</p>
                
                <div className={`text-xs px-2 py-1 rounded-full inline-block ${
                  scenario.qualified 
                    ? 'bg-green-100 text-green-800' 
                    : 'bg-red-100 text-red-800'
                }`}>
                  {scenario.qualified ? '✅ Qualificado' : '❌ Não Qualificado'}
                </div>
              </div>
            )
          })}
        </div>

        {/* Legenda */}
        <div className="mt-6 p-4 bg-gray-50 rounded-lg">
          <h4 className="font-medium text-gray-900 mb-2">📊 Sistema de Scoring</h4>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
            <div>
              <span className="font-medium">Patrimônio:</span>
              <div className="text-gray-600">0-30 pontos</div>
            </div>
            <div>
              <span className="font-medium">Objetivo:</span>
              <div className="text-gray-600">0-25 pontos</div>
            </div>
            <div>
              <span className="font-medium">Urgência:</span>
              <div className="text-gray-600">0-25 pontos</div>
            </div>
            <div>
              <span className="font-medium">Interesse:</span>
              <div className="text-gray-600">0-20 pontos</div>
            </div>
          </div>
          <div className="mt-2 text-xs text-gray-500">
            <strong>Threshold:</strong> ≥ 70 pontos para qualificação
          </div>
        </div>
      </div>

      {/* Modal de Detalhes */}
      {selectedScenario && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-hidden">
            <div className="p-6 border-b border-gray-200">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <selectedScenario.icon className={`h-8 w-8 ${getIconColorClasses(selectedScenario.color, selectedScenario.qualified)}`} />
                  <div>
                    <h2 className="text-xl font-bold text-gray-900">
                      {selectedScenario.title}
                    </h2>
                    <p className="text-gray-600">{selectedScenario.description}</p>
                  </div>
                </div>
                <button
                  onClick={() => setSelectedScenario(null)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  ✕
                </button>
              </div>
            </div>

            <div className="p-6 space-y-6">
              {/* Score */}
              <div className="text-center">
                <div className={`text-4xl font-bold mb-2 ${
                  selectedScenario.qualified ? 'text-green-600' : 'text-red-600'
                }`}>
                  {selectedScenario.score}/100
                </div>
                <div className={`px-4 py-2 rounded-full inline-block ${
                  selectedScenario.qualified 
                    ? 'bg-green-100 text-green-800' 
                    : 'bg-red-100 text-red-800'
                }`}>
                  {selectedScenario.qualified ? '✅ QUALIFICADO' : '❌ NÃO QUALIFICADO'}
                </div>
              </div>

              {/* Exemplo */}
              <div className="bg-gray-50 rounded-lg p-4">
                <h3 className="font-medium text-gray-900 mb-3">
                  👤 Exemplo: {selectedScenario.example.name}
                </h3>
                
                <div className="space-y-2 mb-4">
                  <div className="text-sm">
                    <span className="font-medium">Patrimônio:</span> {selectedScenario.example.responses[0]}
                  </div>
                  <div className="text-sm">
                    <span className="font-medium">Objetivo:</span> {selectedScenario.example.responses[1]}
                  </div>
                  <div className="text-sm">
                    <span className="font-medium">Urgência:</span> {selectedScenario.example.responses[2]}
                  </div>
                  <div className="text-sm">
                    <span className="font-medium">Interesse:</span> {selectedScenario.example.responses[3]}
                  </div>
                </div>

                <div className="border-t border-gray-200 pt-3">
                  <h4 className="font-medium text-gray-900 mb-2">🧠 Análise da IA:</h4>
                  <p className="text-sm text-gray-700">
                    {selectedScenario.example.reasoning}
                  </p>
                </div>
              </div>

              {/* Ações Recomendadas */}
              <div className="bg-blue-50 rounded-lg p-4">
                <h4 className="font-medium text-blue-900 mb-2">🎯 Ações Recomendadas:</h4>
                <div className="text-sm text-blue-800">
                  {selectedScenario.qualified ? (
                    <ul className="space-y-1">
                      <li>• Contato imediato com especialista</li>
                      <li>• Agendamento prioritário</li>
                      <li>• Preparação de proposta personalizada</li>
                      <li>• Follow-up em até 2 horas</li>
                    </ul>
                  ) : (
                    <ul className="space-y-1">
                      <li>• Nurturing com conteúdo educativo</li>
                      <li>• Reengajamento em 30-60 dias</li>
                      <li>• Oferecimento de materiais gratuitos</li>
                      <li>• Acompanhamento de longo prazo</li>
                    </ul>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}













