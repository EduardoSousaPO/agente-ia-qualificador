'use client'

import { Session, Lead } from '@/types'
import { getStatusColor, getStatusLabel, getInitials, getAvatarColor, formatTimeAgo } from '@/lib/utils'
import { 
  UserIcon, 
  ComputerDesktopIcon, 
  PhoneIcon, 
  CheckCircleIcon,
  ArrowLeftIcon 
} from '@heroicons/react/24/outline'
import Link from 'next/link'

interface ConversationHeaderProps {
  session: Session
  lead: Lead | null
  humanTakeover: boolean
  onTakeoverToggle: () => void
  onManualQualification: () => void
}

export function ConversationHeader({
  session,
  lead,
  humanTakeover,
  onTakeoverToggle,
  onManualQualification
}: ConversationHeaderProps) {
  return (
    <div className="bg-white shadow-sm border-b border-gray-200 px-6 py-4">
      <div className="flex items-center justify-between">
        {/* Left Section */}
        <div className="flex items-center space-x-4">
          {/* Back Button */}
          <Link
            href="/conversations"
            className="inline-flex items-center text-gray-500 hover:text-gray-700"
          >
            <ArrowLeftIcon className="h-5 w-5 mr-1" />
            Voltar
          </Link>

          {/* Lead Info */}
          <div className="flex items-center space-x-3">
            <div className={`flex-shrink-0 h-10 w-10 rounded-full ${getAvatarColor(lead?.name || 'Unknown')} flex items-center justify-center`}>
              <span className="text-sm font-medium text-white">
                {getInitials(lead?.name || 'U')}
              </span>
            </div>
            
            <div>
              <h1 className="text-lg font-semibold text-gray-900">
                {lead?.name || 'Lead sem nome'}
              </h1>
              <div className="flex items-center space-x-3 text-sm text-gray-500">
                <span>{lead?.phone || 'Sem telefone'}</span>
                {lead?.email && (
                  <>
                    <span>•</span>
                    <span>{lead.email}</span>
                  </>
                )}
                <span>•</span>
                <span>Atualizado {formatTimeAgo(session.updated_at)}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Right Section */}
        <div className="flex items-center space-x-4">
          {/* Session Status */}
          <div className="flex items-center space-x-2">
            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(session.status)}`}>
              {getStatusLabel(session.status)}
            </span>
            
            {session.current_step && (
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                {session.current_step}
              </span>
            )}
          </div>

          {/* Lead Score */}
          {lead?.score !== undefined && (
            <div className="flex items-center space-x-2">
              <div className="flex items-center space-x-1">
                <div className="w-16 bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-primary-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${lead.score}%` }}
                  />
                </div>
                <span className="text-sm font-medium text-gray-600">
                  {lead.score}%
                </span>
              </div>
            </div>
          )}

          {/* Control Toggle */}
          <button
            onClick={onTakeoverToggle}
            className={`inline-flex items-center px-3 py-2 rounded-md text-sm font-medium transition-colors ${
              humanTakeover
                ? 'bg-orange-100 text-orange-800 hover:bg-orange-200'
                : 'bg-blue-100 text-blue-800 hover:bg-blue-200'
            }`}
          >
            {humanTakeover ? (
              <>
                <UserIcon className="h-4 w-4 mr-1" />
                Controle Humano
              </>
            ) : (
              <>
                <ComputerDesktopIcon className="h-4 w-4 mr-1" />
                IA Ativa
              </>
            )}
          </button>

          {/* Actions Menu */}
          <div className="flex items-center space-x-2">
            {/* Manual Qualification */}
            {lead?.status !== 'qualificado' && (
              <button
                onClick={onManualQualification}
                className="inline-flex items-center px-3 py-2 border border-green-300 shadow-sm text-sm font-medium rounded-md text-green-700 bg-green-50 hover:bg-green-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
              >
                <CheckCircleIcon className="h-4 w-4 mr-1" />
                Qualificar
              </button>
            )}

            {/* Call Lead */}
            {lead?.phone && (
              <a
                href={`tel:${lead.phone}`}
                className="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
              >
                <PhoneIcon className="h-4 w-4 mr-1" />
                Ligar
              </a>
            )}
          </div>
        </div>
      </div>

      {/* Additional Info Bar */}
      {(session.current_step || lead?.origem) && (
        <div className="mt-3 pt-3 border-t border-gray-100">
          <div className="flex items-center justify-between text-sm text-gray-600">
            <div className="flex items-center space-x-4">
              {session.current_step && (
                <span>
                  <strong>Etapa atual:</strong> {session.current_step}
                </span>
              )}
              {lead?.origem && (
                <span>
                  <strong>Origem:</strong> {lead.origem.replace('_', ' ')}
                  {lead.inserido_manual && ' (Manual)'}
                </span>
              )}
            </div>
            
            {lead?.tags && lead.tags.length > 0 && (
              <div className="flex items-center space-x-1">
                <span className="text-gray-500">Tags:</span>
                {lead.tags.slice(0, 3).map((tag, index) => (
                  <span
                    key={index}
                    className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-800"
                  >
                    {tag}
                  </span>
                ))}
                {lead.tags.length > 3 && (
                  <span className="text-xs text-gray-500">
                    +{lead.tags.length - 3}
                  </span>
                )}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}




