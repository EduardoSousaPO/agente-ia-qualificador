'use client'

import { useState } from 'react'
import { DashboardLayout } from '@/components/layout/dashboard-layout'
import { ChatBubbleLeftRightIcon, UserIcon, ComputerDesktopIcon } from '@heroicons/react/24/outline'
import { ConversationSimulator } from '@/components/exemplos/conversation-simulator'

interface ConversationExample {
  id: string
  title: string
  description: string
  leadProfile: {
    name: string
    origem: string
    expectedScore: number
    qualified: boolean
  }
  messages: {
    id: string
    sender: 'user' | 'ai'
    content: string
    timestamp: string
    analysis?: string
  }[]
  finalResult: {
    score: number
    qualified: boolean
    breakdown: {
      patrimonio: number
      objetivo: number
      urgencia: number
      interesse: number
    }
    reasoning: string
  }
}

const conversationExamples: ConversationExample[] = [
  {
    id: 'exemplo-1',
    title: '🎯 Lead Altamente Qualificado (Score 95)',
    description: 'Investidor experiente com alto patrimônio e urgência',
    leadProfile: {
      name: 'Carlos Eduardo Silva',
      origem: 'YouTube - Canal de Investimentos',
      expectedScore: 95,
      qualified: true
    },
    messages: [
      {
        id: '1',
        sender: 'ai',
        content: 'Olá Carlos! 👋\n\nVi que você tem interesse em investimentos. Para te conectar com o melhor especialista, preciso fazer algumas perguntas rápidas. Tudo bem?\n\nPrimeira pergunta: Quanto você tem disponível para investir hoje?\n\nA) Até R$ 50 mil\nB) R$ 50 mil a R$ 200 mil\nC) R$ 200 mil a R$ 500 mil\nD) Mais de R$ 500 mil',
        timestamp: '10:30',
        analysis: 'IA inicia qualificação com tom consultivo e apresenta opções claras'
      },
      {
        id: '2',
        sender: 'user',
        content: 'D - Tenho cerca de R$ 800 mil disponível para diversificar meus investimentos',
        timestamp: '10:32',
        analysis: 'Resposta indica alto patrimônio (30 pontos) + contexto adicional positivo'
      },
      {
        id: '3',
        sender: 'ai',
        content: 'Excelente! Com esse valor você tem muitas opções interessantes.\n\nSegunda pergunta: Qual seu principal objetivo com esses investimentos?\n\nA) Aposentadoria\nB) Crescimento do patrimônio\nC) Reserva de emergência\nD) Especulação/day trade',
        timestamp: '10:33',
        analysis: 'IA reconhece o valor alto e adapta linguagem, mantém estrutura'
      },
      {
        id: '4',
        sender: 'user',
        content: 'A - Estou focado em construir uma aposentadoria sólida. Tenho 45 anos e quero me aposentar aos 60.',
        timestamp: '10:35',
        analysis: 'Objetivo claro de aposentadoria (25 pontos) + planejamento de longo prazo'
      },
      {
        id: '5',
        sender: 'ai',
        content: 'Perfeita estratégia! 15 anos é um prazo excelente para construir uma aposentadoria robusta.\n\nTerceira pergunta: Quando você pretende começar a investir?\n\nA) Esta semana\nB) Este mês\nC) Nos próximos 3 meses\nD) Não tenho pressa',
        timestamp: '10:36',
        analysis: 'IA valida estratégia do cliente, cria rapport antes da próxima pergunta'
      },
      {
        id: '6',
        sender: 'user',
        content: 'A - Quero começar esta semana mesmo. Já tenho o dinheiro parado na poupança há meses.',
        timestamp: '10:37',
        analysis: 'Máxima urgência (25 pontos) + dor clara (dinheiro parado)'
      },
      {
        id: '7',
        sender: 'ai',
        content: 'Ótima decisão! A poupança realmente não é o melhor lugar para esse valor.\n\nÚltima pergunta: Gostaria de falar com um de nossos especialistas para uma consultoria gratuita?\n\nA) Sim, com urgência\nB) Sim, quando for possível\nC) Talvez, preciso pensar\nD) Não, obrigado',
        timestamp: '10:38',
        analysis: 'IA cria urgência mencionando problema da poupança'
      },
      {
        id: '8',
        sender: 'user',
        content: 'A - Sim, com urgência! Posso falar hoje mesmo se possível.',
        timestamp: '10:39',
        analysis: 'Máximo interesse (20 pontos) + disponibilidade imediata'
      },
      {
        id: '9',
        sender: 'ai',
        content: '🎯 **PERFEITO! Você está qualificado!**\n\nScore: 95/100\n\n✅ **Patrimônio**: R$ 800 mil (30 pts)\n✅ **Objetivo**: Aposentadoria (25 pts)\n✅ **Urgência**: Esta semana (25 pts)\n✅ **Interesse**: Urgente (20 pts)\n\nNosso especialista sênior entrará em contato em até 1 hora para agendar sua consultoria gratuita.\n\n📅 **Horários disponíveis hoje:**\n• 14h às 15h\n• 16h às 17h\n\nQual prefere?',
        timestamp: '10:40',
        analysis: 'IA calcula score final e oferece agendamento imediato para lead premium'
      },
      {
        id: '10',
        sender: 'user',
        content: 'Perfeito! Prefiro às 14h. Muito obrigado!',
        timestamp: '10:41',
        analysis: 'Lead aceita agendamento - conversão completa!'
      }
    ],
    finalResult: {
      score: 95,
      qualified: true,
      breakdown: {
        patrimonio: 30,
        objetivo: 25,
        urgencia: 25,
        interesse: 20
      },
      reasoning: 'Lead premium com alto patrimônio, objetivo claro de aposentadoria, urgência máxima e interesse imediato. Perfil ideal para consultoria especializada.'
    }
  },
  {
    id: 'exemplo-2',
    title: '⚠️ Lead Parcialmente Qualificado (Score 65)',
    description: 'Investidor iniciante com potencial, mas sem urgência',
    leadProfile: {
      name: 'Ana Paula Santos',
      origem: 'Newsletter - Blog de Finanças',
      expectedScore: 65,
      qualified: false
    },
    messages: [
      {
        id: '1',
        sender: 'ai',
        content: 'Olá Ana! 👋\n\nVi que você se inscreveu na nossa newsletter sobre investimentos. Para te ajudar melhor, preciso fazer algumas perguntas rápidas.\n\nPrimeira pergunta: Quanto você tem disponível para investir hoje?\n\nA) Até R$ 50 mil\nB) R$ 50 mil a R$ 200 mil\nC) R$ 200 mil a R$ 500 mil\nD) Mais de R$ 500 mil',
        timestamp: '14:15',
        analysis: 'IA personaliza abordagem baseada na origem (newsletter)'
      },
      {
        id: '2',
        sender: 'user',
        content: 'B - Tenho uns R$ 80 mil que consegui juntar',
        timestamp: '14:18',
        analysis: 'Patrimônio médio (20 pontos) - boa base para começar'
      },
      {
        id: '3',
        sender: 'ai',
        content: 'Parabéns por ter conseguido juntar esse valor! É um ótimo começo.\n\nSegunda pergunta: Qual seu principal objetivo com esses investimentos?\n\nA) Aposentadoria\nB) Crescimento do patrimônio\nC) Reserva de emergência\nD) Especulação/day trade',
        timestamp: '14:19',
        analysis: 'IA parabeniza para criar rapport e motivar'
      },
      {
        id: '4',
        sender: 'user',
        content: 'B - Quero fazer meu dinheiro crescer, mas não sei muito sobre investimentos',
        timestamp: '14:22',
        analysis: 'Objetivo de crescimento (20 pontos) mas revela inexperiência'
      },
      {
        id: '5',
        sender: 'ai',
        content: 'Entendo! Crescimento é um ótimo objetivo e todos começaram sem saber.\n\nTerceira pergunta: Quando você pretende começar a investir?\n\nA) Esta semana\nB) Este mês\nC) Nos próximos 3 meses\nD) Não tenho pressa',
        timestamp: '14:23',
        analysis: 'IA tranquiliza sobre inexperiência e mantém tom encorajador'
      },
      {
        id: '6',
        sender: 'user',
        content: 'C - Nos próximos 3 meses. Quero estudar mais antes',
        timestamp: '14:25',
        analysis: 'Urgência média (15 pontos) - quer se educar primeiro'
      },
      {
        id: '7',
        sender: 'ai',
        content: 'Muito sensato! Estudar antes é sempre uma boa estratégia.\n\nÚltima pergunta: Gostaria de falar com um de nossos especialistas para uma consultoria gratuita?\n\nA) Sim, com urgência\nB) Sim, quando for possível\nC) Talvez, preciso pensar\nD) Não, obrigado',
        timestamp: '14:26',
        analysis: 'IA valida abordagem cautelosa do cliente'
      },
      {
        id: '8',
        sender: 'user',
        content: 'C - Talvez... ainda estou aprendendo sobre investimentos',
        timestamp: '14:28',
        analysis: 'Interesse baixo (10 pontos) - ainda em fase de educação'
      },
      {
        id: '9',
        sender: 'ai',
        content: '📊 **Obrigado pelas respostas!**\n\nScore: 65/100\n\n• **Patrimônio**: R$ 80 mil (20 pts)\n• **Objetivo**: Crescimento (20 pts)\n• **Urgência**: 3 meses (15 pts)\n• **Interesse**: Talvez (10 pts)\n\nVocê tem um bom perfil, mas recomendo que explore nosso conteúdo educativo primeiro:\n\n📚 **Materiais Gratuitos:**\n• Guia do Investidor Iniciante\n• Webinar: Primeiros Passos\n• E-book: Diversificação\n\n🔗 Acesse: www.exemplo.com/educacao\n\nQuando se sentir mais preparada, estaremos aqui! 😊',
        timestamp: '14:29',
        analysis: 'IA oferece nurturing em vez de hard sell - estratégia de longo prazo'
      },
      {
        id: '10',
        sender: 'user',
        content: 'Perfeito! Vou estudar esse material. Obrigada!',
        timestamp: '14:30',
        analysis: 'Lead aceita nurturing - potencial futuro'
      }
    ],
    finalResult: {
      score: 65,
      qualified: false,
      breakdown: {
        patrimonio: 20,
        objetivo: 20,
        urgencia: 15,
        interesse: 10
      },
      reasoning: 'Lead com potencial mas ainda em fase de educação. Patrimônio adequado e objetivo claro, porém baixa urgência e interesse. Ideal para nurturing com conteúdo educativo.'
    }
  },
  {
    id: 'exemplo-3',
    title: '❌ Lead Não Qualificado (Score 35)',
    description: 'Perfil especulativo com baixo patrimônio',
    leadProfile: {
      name: 'João Trader',
      origem: 'Inbound WhatsApp',
      expectedScore: 35,
      qualified: false
    },
    messages: [
      {
        id: '1',
        sender: 'ai',
        content: 'Olá! 👋\n\nVi que você tem interesse em investimentos. Para te conectar com o melhor especialista, preciso fazer algumas perguntas rápidas.\n\nPrimeira pergunta: Quanto você tem disponível para investir hoje?\n\nA) Até R$ 50 mil\nB) R$ 50 mil a R$ 200 mil\nC) R$ 200 mil a R$ 500 mil\nD) Mais de R$ 500 mil',
        timestamp: '16:45',
        analysis: 'Abordagem padrão para lead inbound'
      },
      {
        id: '2',
        sender: 'user',
        content: 'A - Tenho uns R$ 15 mil que quero multiplicar rápido',
        timestamp: '16:47',
        analysis: 'Baixo patrimônio (10 pontos) + mentalidade especulativa'
      },
      {
        id: '3',
        sender: 'ai',
        content: 'Entendo! Todo valor é importante para começar.\n\nSegunda pergunta: Qual seu principal objetivo com esses investimentos?\n\nA) Aposentadoria\nB) Crescimento do patrimônio\nC) Reserva de emergência\nD) Especulação/day trade',
        timestamp: '16:48',
        analysis: 'IA mantém tom positivo mesmo com valor baixo'
      },
      {
        id: '4',
        sender: 'user',
        content: 'D - Quero fazer day trade e ganhar dinheiro rápido',
        timestamp: '16:50',
        analysis: 'Objetivo especulativo (10 pontos) - perfil de risco alto'
      },
      {
        id: '5',
        sender: 'ai',
        content: 'Entendo seu interesse! Day trade pode ser uma estratégia, mas requer muito conhecimento.\n\nTerceira pergunta: Quando você pretende começar?\n\nA) Esta semana\nB) Este mês\nC) Nos próximos 3 meses\nD) Não tenho pressa',
        timestamp: '16:51',
        analysis: 'IA alerta sobre riscos sem desencorajar completamente'
      },
      {
        id: '6',
        sender: 'user',
        content: 'D - Não tenho pressa, quero só algumas dicas rápidas',
        timestamp: '16:53',
        analysis: 'Sem urgência (5 pontos) - busca informação gratuita'
      },
      {
        id: '7',
        sender: 'ai',
        content: 'Compreendo! Informação é sempre valiosa.\n\nÚltima pergunta: Gostaria de falar com um de nossos especialistas?\n\nA) Sim, com urgência\nB) Sim, quando for possível\nC) Talvez, preciso pensar\nD) Não, obrigado',
        timestamp: '16:54',
        analysis: 'IA mantém processo mesmo prevendo baixo interesse'
      },
      {
        id: '8',
        sender: 'user',
        content: 'D - Não precisa, só queria umas dicas mesmo',
        timestamp: '16:55',
        analysis: 'Sem interesse em consultoria (0 pontos) - apenas busca informação'
      },
      {
        id: '9',
        sender: 'ai',
        content: '📊 **Obrigado pelas respostas!**\n\nScore: 25/100\n\nCom base no seu perfil, recomendo que explore nosso conteúdo educativo gratuito primeiro:\n\n📚 **Materiais Recomendados:**\n• Curso: Fundamentos do Day Trade\n• E-book: Gestão de Risco\n• Simulador de Trading Gratuito\n\n🔗 Acesse: www.exemplo.com/materiais-gratuitos\n\n⚠️ **Lembre-se**: Day trade envolve riscos altos. Sempre estude muito antes de começar!\n\nQuando estiver pronto para investir com mais segurança, estaremos aqui! 😊',
        timestamp: '16:56',
        analysis: 'IA oferece educação e alerta sobre riscos - abordagem responsável'
      },
      {
        id: '10',
        sender: 'user',
        content: 'Valeu pelas dicas!',
        timestamp: '16:57',
        analysis: 'Lead agradece mas não demonstra interesse em prosseguir'
      }
    ],
    finalResult: {
      score: 25,
      qualified: false,
      breakdown: {
        patrimonio: 10,
        objetivo: 10,
        urgencia: 5,
        interesse: 0
      },
      reasoning: 'Lead com perfil especulativo, baixo patrimônio, sem urgência e interesse apenas em informações gratuitas. Não adequado para consultoria paga, mas pode ser nutrido com conteúdo educativo.'
    }
  },
  {
    id: 'exemplo-4',
    title: '🎯 Lead Qualificado Experiente (Score 85)',
    description: 'Investidor experiente buscando diversificação',
    leadProfile: {
      name: 'Maria Fernanda Costa',
      origem: 'Indicação de Cliente',
      expectedScore: 85,
      qualified: true
    },
    messages: [
      {
        id: '1',
        sender: 'ai',
        content: 'Olá Maria! 👋\n\nFui informado que você foi indicada por um de nossos clientes. Para personalizar melhor nossa conversa, preciso fazer algumas perguntas.\n\nPrimeira pergunta: Quanto você tem disponível para novos investimentos?\n\nA) Até R$ 50 mil\nB) R$ 50 mil a R$ 200 mil\nC) R$ 200 mil a R$ 500 mil\nD) Mais de R$ 500 mil',
        timestamp: '09:15',
        analysis: 'IA reconhece indicação e personaliza abordagem'
      },
      {
        id: '2',
        sender: 'user',
        content: 'C - Tenho R$ 300 mil que quero diversificar. Já invisto em ações e fundos, mas quero outras opções.',
        timestamp: '09:18',
        analysis: 'Alto patrimônio (25 pontos) + experiência prévia em investimentos'
      },
      {
        id: '3',
        sender: 'ai',
        content: 'Excelente! Diversificação é fundamental. Que bom saber que já tem experiência no mercado.\n\nSegunda pergunta: Qual seu principal objetivo com essa diversificação?\n\nA) Aposentadoria\nB) Crescimento do patrimônio\nC) Reserva de emergência\nD) Especulação/day trade',
        timestamp: '09:19',
        analysis: 'IA reconhece experiência e foca em diversificação'
      },
      {
        id: '4',
        sender: 'user',
        content: 'B - Crescimento do patrimônio. Quero explorar renda fixa premium e talvez alguns fundos imobiliários.',
        timestamp: '09:22',
        analysis: 'Objetivo claro de crescimento (20 pontos) + conhecimento específico'
      },
      {
        id: '5',
        sender: 'ai',
        content: 'Perfeito! Renda fixa premium e FIIs são ótimas opções para diversificação.\n\nTerceira pergunta: Quando pretende fazer essa diversificação?\n\nA) Esta semana\nB) Este mês\nC) Nos próximos 3 meses\nD) Não tenho pressa',
        timestamp: '09:23',
        analysis: 'IA demonstra conhecimento técnico para criar credibilidade'
      },
      {
        id: '6',
        sender: 'user',
        content: 'B - Este mês. Quero aproveitar as oportunidades atuais do mercado.',
        timestamp: '09:25',
        analysis: 'Boa urgência (20 pontos) + visão de mercado'
      },
      {
        id: '7',
        sender: 'ai',
        content: 'Ótimo timing! O mercado realmente está com boas oportunidades.\n\nÚltima pergunta: Gostaria de falar com nosso especialista em carteiras diversificadas?\n\nA) Sim, com urgência\nB) Sim, quando for possível\nC) Talvez, preciso pensar\nD) Não, obrigado',
        timestamp: '09:26',
        analysis: 'IA concorda com análise de mercado e oferece especialista específico'
      },
      {
        id: '8',
        sender: 'user',
        content: 'B - Sim, quando for possível. Prefiro uma conversa mais técnica.',
        timestamp: '09:28',
        analysis: 'Interesse moderado (15 pontos) mas com preferência por abordagem técnica'
      },
      {
        id: '9',
        sender: 'ai',
        content: '🎯 **Excelente! Você está qualificada!**\n\nScore: 80/100\n\n✅ **Patrimônio**: R$ 300 mil (25 pts)\n✅ **Objetivo**: Crescimento/Diversificação (20 pts)\n✅ **Urgência**: Este mês (20 pts)\n✅ **Interesse**: Sim, técnico (15 pts)\n\nVou conectar você com nosso especialista em carteiras diversificadas. Ele tem experiência específica em:\n\n• Renda fixa premium (CRIs, CRAs, Debêntures)\n• Fundos imobiliários\n• Estruturação de carteiras\n\n📞 **Ele entrará em contato em até 4 horas**\n\nPreferência de horário para ligação?',
        timestamp: '09:29',
        analysis: 'IA destaca expertise específica para investidor experiente'
      },
      {
        id: '10',
        sender: 'user',
        content: 'Perfeito! Prefiro entre 14h e 16h. Obrigada!',
        timestamp: '09:30',
        analysis: 'Lead aceita contato e define horário - conversão bem-sucedida'
      }
    ],
    finalResult: {
      score: 80,
      qualified: true,
      breakdown: {
        patrimonio: 25,
        objetivo: 20,
        urgencia: 20,
        interesse: 15
      },
      reasoning: 'Lead qualificado com perfil experiente. Alto patrimônio, objetivo claro de diversificação, urgência adequada e interesse em consultoria técnica. Ideal para especialista sênior.'
    }
  }
]

export default function ExemplosPage() {
  const [selectedExample, setSelectedExample] = useState<ConversationExample | null>(null)
  const [currentMessageIndex, setCurrentMessageIndex] = useState(0)
  const [isPlaying, setIsPlaying] = useState(false)

  const playConversation = (example: ConversationExample) => {
    setSelectedExample(example)
    setCurrentMessageIndex(0)
    setIsPlaying(true)
    
    // Simular conversa em tempo real
    const interval = setInterval(() => {
      setCurrentMessageIndex(prev => {
        if (prev >= example.messages.length - 1) {
          setIsPlaying(false)
          clearInterval(interval)
          return prev
        }
        return prev + 1
      })
    }, 2000) // Nova mensagem a cada 2 segundos
  }

  const resetConversation = () => {
    setCurrentMessageIndex(0)
    setIsPlaying(false)
  }

  return (
    <DashboardLayout>
      <div className="space-y-8">
        {/* Header */}
        <div className="page-header">
          <h1 className="page-title">💬 Exemplos de Conversas</h1>
          <p className="page-description">
            Veja como a IA qualifica diferentes tipos de leads com conversas reais
          </p>
        </div>

        {/* Simulador de Conversas */}
        <ConversationSimulator />

        {/* Lista de Exemplos */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {conversationExamples.map((example) => (
            <div key={example.id} className="card hover:shadow-lg transition-shadow">
              <div className="card-header">
                <h3 className="card-title">{example.title}</h3>
                <p className="card-description">{example.description}</p>
              </div>
              
              <div className="p-6 space-y-4">
                {/* Lead Profile */}
                <div className="bg-gray-50 rounded-lg p-4">
                  <h4 className="font-medium text-gray-900 mb-2">👤 Perfil do Lead</h4>
                  <div className="grid grid-cols-2 gap-2 text-sm">
                    <div><span className="font-medium">Nome:</span> {example.leadProfile.name}</div>
                    <div><span className="font-medium">Origem:</span> {example.leadProfile.origem}</div>
                    <div><span className="font-medium">Score:</span> {example.leadProfile.expectedScore}/100</div>
                    <div>
                      <span className="font-medium">Status:</span>{' '}
                      <span className={`px-2 py-1 rounded-full text-xs ${
                        example.leadProfile.qualified 
                          ? 'bg-green-100 text-green-800' 
                          : 'bg-red-100 text-red-800'
                      }`}>
                        {example.leadProfile.qualified ? 'Qualificado' : 'Não Qualificado'}
                      </span>
                    </div>
                  </div>
                </div>

                {/* Score Breakdown */}
                <div className="bg-blue-50 rounded-lg p-4">
                  <h4 className="font-medium text-blue-900 mb-2">📊 Breakdown do Score</h4>
                  <div className="grid grid-cols-2 gap-2 text-sm text-blue-800">
                    <div>Patrimônio: {example.finalResult.breakdown.patrimonio} pts</div>
                    <div>Objetivo: {example.finalResult.breakdown.objetivo} pts</div>
                    <div>Urgência: {example.finalResult.breakdown.urgencia} pts</div>
                    <div>Interesse: {example.finalResult.breakdown.interesse} pts</div>
                  </div>
                </div>

                {/* Action Button */}
                <button
                  onClick={() => playConversation(example)}
                  className="w-full btn-primary flex items-center justify-center gap-2"
                >
                  <ChatBubbleLeftRightIcon className="h-5 w-5" />
                  Ver Conversa Completa
                </button>
              </div>
            </div>
          ))}
        </div>

        {/* Modal de Conversa */}
        {selectedExample && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-hidden">
              {/* Header do Modal */}
              <div className="p-6 border-b border-gray-200">
                <div className="flex items-center justify-between">
                  <div>
                    <h2 className="text-xl font-bold text-gray-900">
                      {selectedExample.title}
                    </h2>
                    <p className="text-gray-600">{selectedExample.leadProfile.name}</p>
                  </div>
                  <div className="flex items-center gap-4">
                    {/* Controles */}
                    <div className="flex items-center gap-2">
                      <button
                        onClick={resetConversation}
                        className="px-3 py-1 text-sm bg-gray-100 text-gray-700 rounded hover:bg-gray-200"
                      >
                        ↻ Reiniciar
                      </button>
                      <span className="text-sm text-gray-500">
                        {currentMessageIndex + 1}/{selectedExample.messages.length}
                      </span>
                    </div>
                    <button
                      onClick={() => setSelectedExample(null)}
                      className="text-gray-400 hover:text-gray-600"
                    >
                      ✕
                    </button>
                  </div>
                </div>
              </div>

              {/* Conversa */}
              <div className="flex-1 overflow-y-auto p-6 space-y-4 max-h-[60vh]">
                {selectedExample.messages.slice(0, currentMessageIndex + 1).map((message) => (
                  <div
                    key={message.id}
                    className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div className={`max-w-[70%] ${
                      message.sender === 'user' 
                        ? 'bg-blue-500 text-white' 
                        : 'bg-gray-100 text-gray-900'
                    } rounded-lg p-4`}>
                      {/* Avatar e Nome */}
                      <div className="flex items-center gap-2 mb-2">
                        {message.sender === 'user' ? (
                          <UserIcon className="h-4 w-4" />
                        ) : (
                          <ComputerDesktopIcon className="h-4 w-4" />
                        )}
                        <span className="text-xs font-medium">
                          {message.sender === 'user' ? selectedExample.leadProfile.name : 'IA Qualificador'}
                        </span>
                        <span className="text-xs opacity-75">{message.timestamp}</span>
                      </div>
                      
                      {/* Conteúdo */}
                      <div className="whitespace-pre-line text-sm">
                        {message.content}
                      </div>
                      
                      {/* Análise */}
                      {message.analysis && (
                        <div className={`mt-2 p-2 rounded text-xs ${
                          message.sender === 'user'
                            ? 'bg-blue-600 bg-opacity-50'
                            : 'bg-gray-200'
                        }`}>
                          <span className="font-medium">💡 Análise:</span> {message.analysis}
                        </div>
                      )}
                    </div>
                  </div>
                ))}
                
                {/* Indicador de digitação */}
                {isPlaying && currentMessageIndex < selectedExample.messages.length - 1 && (
                  <div className="flex justify-start">
                    <div className="bg-gray-100 rounded-lg p-4 max-w-[70%]">
                      <div className="flex items-center gap-2">
                        <ComputerDesktopIcon className="h-4 w-4" />
                        <span className="text-xs font-medium">IA Qualificador</span>
                      </div>
                      <div className="mt-2 flex items-center gap-1">
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                        <span className="text-xs text-gray-500 ml-2">digitando...</span>
                      </div>
                    </div>
                  </div>
                )}
              </div>

              {/* Resultado Final */}
              {currentMessageIndex >= selectedExample.messages.length - 1 && (
                <div className="p-6 border-t border-gray-200 bg-gray-50">
                  <h3 className="font-bold text-gray-900 mb-4">📊 Resultado Final da Qualificação</h3>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {/* Score */}
                    <div className="space-y-3">
                      <div className={`text-center p-4 rounded-lg ${
                        selectedExample.finalResult.qualified 
                          ? 'bg-green-100 text-green-800' 
                          : 'bg-red-100 text-red-800'
                      }`}>
                        <div className="text-2xl font-bold">
                          {selectedExample.finalResult.score}/100
                        </div>
                        <div className="text-sm">
                          {selectedExample.finalResult.qualified ? '✅ QUALIFICADO' : '❌ NÃO QUALIFICADO'}
                        </div>
                      </div>
                      
                      {/* Breakdown */}
                      <div className="space-y-2">
                        {Object.entries(selectedExample.finalResult.breakdown).map(([key, value]) => (
                          <div key={key} className="flex justify-between items-center">
                            <span className="text-sm capitalize">{key}:</span>
                            <span className="font-medium">{value} pts</span>
                          </div>
                        ))}
                      </div>
                    </div>
                    
                    {/* Reasoning */}
                    <div>
                      <h4 className="font-medium text-gray-900 mb-2">🧠 Análise da IA</h4>
                      <p className="text-sm text-gray-700">
                        {selectedExample.finalResult.reasoning}
                      </p>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </DashboardLayout>
  )
}
