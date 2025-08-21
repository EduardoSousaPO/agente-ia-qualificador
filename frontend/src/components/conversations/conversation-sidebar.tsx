'use client'

import { Session, Lead } from '@/types'
import { 
  formatDateTime, 
  formatPhone, 
  getStatusColor, 
  getStatusLabel,
  getInitials,
  getAvatarColor
} from '@/lib/utils'
import { 
  UserIcon, 
  EnvelopeIcon, 
  PhoneIcon, 
  CalendarDaysIcon,
  ChartBarIcon,
  TagIcon,
  ClockIcon,
  CheckCircleIcon
} from '@heroicons/react/24/outline'

interface ConversationSidebarProps {
  session: Session
  lead: Lead | null
  onDataUpdate: () => void
}

export function ConversationSidebar({
  session,
  lead,
  onDataUpdate
}: ConversationSidebarProps) {
  return (
    <div className="h-full overflow-y-auto bg-gray-50">
      {/* Lead Profile */}
      <div className="p-6 bg-white border-b border-gray-200">
        <div className="text-center">
          <div className={`mx-auto h-16 w-16 rounded-full ${getAvatarColor(lead?.name || 'Unknown')} flex items-center justify-center`}>
            <span className="text-lg font-medium text-white">
              {getInitials(lead?.name || 'U')}
            </span>
          </div>
          <h3 className="mt-3 text-lg font-medium text-gray-900">
            {lead?.name || 'Lead sem nome'}
          </h3>
          <div className="mt-1 flex items-center justify-center">
            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(lead?.status || 'novo')}`}>
              {getStatusLabel(lead?.status || 'novo')}
            </span>
          </div>
        </div>
      </div>

      {/* Contact Information */}
      <div className="p-6 bg-white border-b border-gray-200">
        <h4 className="text-sm font-medium text-gray-900 mb-3">Contato</h4>
        <div className="space-y-3">
          {lead?.phone && (
            <div className="flex items-center space-x-3">
              <PhoneIcon className="h-5 w-5 text-gray-400" />
              <div>
                <p className="text-sm text-gray-900">{formatPhone(lead.phone)}</p>
                <a
                  href={`tel:${lead.phone}`}
                  className="text-xs text-primary-600 hover:text-primary-700"
                >
                  Ligar agora
                </a>
              </div>
            </div>
          )}
          
          {lead?.email && (
            <div className="flex items-center space-x-3">
              <EnvelopeIcon className="h-5 w-5 text-gray-400" />
              <div>
                <p className="text-sm text-gray-900">{lead.email}</p>
                <a
                  href={`mailto:${lead.email}`}
                  className="text-xs text-primary-600 hover:text-primary-700"
                >
                  Enviar email
                </a>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Lead Score */}
      {lead?.score !== undefined && (
        <div className="p-6 bg-white border-b border-gray-200">
          <h4 className="text-sm font-medium text-gray-900 mb-3">Score de Qualificação</h4>
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Progresso</span>
              <span className="text-sm font-medium text-gray-900">{lead.score}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-3">
              <div
                className="bg-primary-600 h-3 rounded-full transition-all duration-300"
                style={{ width: `${lead.score}%` }}
              />
            </div>
            <div className="text-xs text-gray-500">
              {lead.score >= 70 && 'Lead altamente qualificado'}
              {lead.score >= 50 && lead.score < 70 && 'Lead moderadamente qualificado'}
              {lead.score < 50 && 'Lead em qualificação'}
            </div>
          </div>
        </div>
      )}

      {/* Session Details */}
      <div className="p-6 bg-white border-b border-gray-200">
        <h4 className="text-sm font-medium text-gray-900 mb-3">Detalhes da Sessão</h4>
        <div className="space-y-3">
          <div className="flex items-center space-x-3">
            <ChartBarIcon className="h-5 w-5 text-gray-400" />
            <div>
              <p className="text-sm font-medium text-gray-900">Status</p>
              <p className="text-xs text-gray-600">{getStatusLabel(session.status)}</p>
            </div>
          </div>
          
          {session.current_step && (
            <div className="flex items-center space-x-3">
              <ClockIcon className="h-5 w-5 text-gray-400" />
              <div>
                <p className="text-sm font-medium text-gray-900">Etapa Atual</p>
                <p className="text-xs text-gray-600">{session.current_step}</p>
              </div>
            </div>
          )}
          
          <div className="flex items-center space-x-3">
            <CalendarDaysIcon className="h-5 w-5 text-gray-400" />
            <div>
              <p className="text-sm font-medium text-gray-900">Criado em</p>
              <p className="text-xs text-gray-600">{formatDateTime(session.created_at)}</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-3">
            <ClockIcon className="h-5 w-5 text-gray-400" />
            <div>
              <p className="text-sm font-medium text-gray-900">Última atividade</p>
              <p className="text-xs text-gray-600">{formatDateTime(session.updated_at)}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Lead Metadata */}
      {lead && (
        <div className="p-6 bg-white border-b border-gray-200">
          <h4 className="text-sm font-medium text-gray-900 mb-3">Informações do Lead</h4>
          <div className="space-y-3">
            <div className="flex items-center space-x-3">
              <TagIcon className="h-5 w-5 text-gray-400" />
              <div>
                <p className="text-sm font-medium text-gray-900">Origem</p>
                <p className="text-xs text-gray-600 capitalize">
                  {lead.origem.replace('_', ' ')}
                  {lead.inserido_manual && ' (Manual)'}
                </p>
              </div>
            </div>
            
            <div className="flex items-center space-x-3">
              <CalendarDaysIcon className="h-5 w-5 text-gray-400" />
              <div>
                <p className="text-sm font-medium text-gray-900">Cadastrado em</p>
                <p className="text-xs text-gray-600">{formatDateTime(lead.created_at)}</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tags */}
      {lead?.tags && lead.tags.length > 0 && (
        <div className="p-6 bg-white border-b border-gray-200">
          <h4 className="text-sm font-medium text-gray-900 mb-3">Tags</h4>
          <div className="flex flex-wrap gap-2">
            {lead.tags.map((tag, index) => (
              <span
                key={index}
                className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800"
              >
                {tag}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Qualifications */}
      {lead?.qualifications && lead.qualifications.length > 0 && (
        <div className="p-6 bg-white border-b border-gray-200">
          <h4 className="text-sm font-medium text-gray-900 mb-3">Qualificações</h4>
          <div className="space-y-3">
            {lead.qualifications.map((qualification, index) => (
              <div key={qualification.id} className="p-3 bg-green-50 rounded-lg">
                <div className="flex items-start space-x-2">
                  <CheckCircleIcon className="h-5 w-5 text-green-500 mt-0.5" />
                  <div className="flex-1 space-y-1">
                    {qualification.patrimonio_faixa && (
                      <p className="text-xs">
                        <span className="font-medium">Patrimônio:</span> {qualification.patrimonio_faixa}
                      </p>
                    )}
                    {qualification.urgencia && (
                      <p className="text-xs">
                        <span className="font-medium">Urgência:</span> {qualification.urgencia}
                      </p>
                    )}
                    {qualification.objetivo && (
                      <p className="text-xs">
                        <span className="font-medium">Objetivo:</span> {qualification.objetivo}
                      </p>
                    )}
                    {qualification.score_final !== null && (
                      <p className="text-xs">
                        <span className="font-medium">Score:</span> {qualification.score_final}/100
                      </p>
                    )}
                    <p className="text-xs text-gray-500">
                      {formatDateTime(qualification.created_at)}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Meetings */}
      {lead?.meetings && lead.meetings.length > 0 && (
        <div className="p-6 bg-white">
          <h4 className="text-sm font-medium text-gray-900 mb-3">Reuniões</h4>
          <div className="space-y-3">
            {lead.meetings.map((meeting, index) => (
              <div key={meeting.id} className="p-3 bg-blue-50 rounded-lg">
                <div className="flex items-start space-x-2">
                  <CalendarDaysIcon className="h-5 w-5 text-blue-500 mt-0.5" />
                  <div className="flex-1 space-y-1">
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-medium">Reunião</span>
                      <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${getStatusColor(meeting.status)}`}>
                        {getStatusLabel(meeting.status)}
                      </span>
                    </div>
                    
                    {meeting.horario_sugestao_1 && (
                      <p className="text-xs">
                        <span className="font-medium">Opção 1:</span> {formatDateTime(meeting.horario_sugestao_1)}
                      </p>
                    )}
                    {meeting.horario_sugestao_2 && (
                      <p className="text-xs">
                        <span className="font-medium">Opção 2:</span> {formatDateTime(meeting.horario_sugestao_2)}
                      </p>
                    )}
                    
                    {meeting.closer && (
                      <p className="text-xs">
                        <span className="font-medium">Closer:</span> {meeting.closer.name || meeting.closer.email}
                      </p>
                    )}
                    
                    <p className="text-xs text-gray-500">
                      {formatDateTime(meeting.created_at)}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}




