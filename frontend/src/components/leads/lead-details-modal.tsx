'use client'

import { Fragment, useState } from 'react'
import { Dialog, Transition } from '@headlessui/react'
import { XMarkIcon, PhoneIcon, EnvelopeIcon, CalendarDaysIcon, ChatBubbleLeftRightIcon } from '@heroicons/react/24/outline'
import { Lead } from '@/types'
import { formatDateTime, formatPhone, getStatusColor, getStatusLabel, getScoreBadgeColor } from '@/lib/utils'
import Link from 'next/link'

interface LeadDetailsModalProps {
  lead: Lead
  open: boolean
  onClose: () => void
  onLeadUpdate: () => void
}

export function LeadDetailsModal({ lead, open, onClose, onLeadUpdate }: LeadDetailsModalProps) {
  return (
    <Transition.Root show={open} as={Fragment}>
      <Dialog as="div" className="relative z-50" onClose={onClose}>
        <Transition.Child
          as={Fragment}
          enter="ease-out duration-300"
          enterFrom="opacity-0"
          enterTo="opacity-100"
          leave="ease-in duration-200"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
        >
          <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" />
        </Transition.Child>

        <div className="fixed inset-0 z-10 overflow-y-auto">
          <div className="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
            <Transition.Child
              as={Fragment}
              enter="ease-out duration-300"
              enterFrom="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
              enterTo="opacity-100 translate-y-0 sm:scale-100"
              leave="ease-in duration-200"
              leaveFrom="opacity-100 translate-y-0 sm:scale-100"
              leaveTo="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
            >
              <Dialog.Panel className="relative transform overflow-hidden rounded-lg bg-white px-4 pb-4 pt-5 text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-2xl sm:p-6">
                <div className="absolute right-0 top-0 hidden pr-4 pt-4 sm:block">
                  <button
                    type="button"
                    className="rounded-md bg-white text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
                    onClick={onClose}
                  >
                    <span className="sr-only">Fechar</span>
                    <XMarkIcon className="h-6 w-6" />
                  </button>
                </div>

                <div className="sm:flex sm:items-start">
                  <div className="mt-3 text-center sm:ml-0 sm:mt-0 sm:text-left w-full">
                    {/* Header */}
                    <div className="flex items-center space-x-4 pb-4 border-b border-gray-200">
                      <div className="flex-shrink-0">
                        <div className="h-16 w-16 rounded-full bg-gray-300 flex items-center justify-center">
                          <span className="text-xl font-medium text-gray-700">
                            {lead.name.charAt(0).toUpperCase()}
                          </span>
                        </div>
                      </div>
                      <div className="flex-1 min-w-0">
                        <Dialog.Title as="h3" className="text-lg font-semibold leading-6 text-gray-900">
                          {lead.name}
                        </Dialog.Title>
                        <div className="flex items-center space-x-3 mt-1">
                          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(lead.status)}`}>
                            {getStatusLabel(lead.status)}
                          </span>
                          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getScoreBadgeColor(lead.score)}`}>
                            Score: {lead.score}/100
                          </span>
                        </div>
                      </div>
                    </div>

                    {/* Contact Info */}
                    <div className="mt-6 space-y-4">
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="flex items-center space-x-3">
                          <PhoneIcon className="h-5 w-5 text-gray-400" />
                          <div>
                            <p className="text-sm font-medium text-gray-900">Telefone</p>
                            <p className="text-sm text-gray-600">{formatPhone(lead.phone)}</p>
                          </div>
                        </div>
                        
                        <div className="flex items-center space-x-3">
                          <EnvelopeIcon className="h-5 w-5 text-gray-400" />
                          <div>
                            <p className="text-sm font-medium text-gray-900">Email</p>
                            <p className="text-sm text-gray-600">{lead.email || 'Não informado'}</p>
                          </div>
                        </div>
                      </div>

                      {/* Lead Info */}
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-4 border-t border-gray-200">
                        <div>
                          <p className="text-sm font-medium text-gray-900">Origem</p>
                          <p className="text-sm text-gray-600 capitalize">
                            {lead.origem.replace('_', ' ')}
                            {lead.inserido_manual && (
                              <span className="ml-2 text-blue-600">(Manual)</span>
                            )}
                          </p>
                        </div>
                        
                        <div>
                          <p className="text-sm font-medium text-gray-900">Criado em</p>
                          <p className="text-sm text-gray-600">{formatDateTime(lead.created_at)}</p>
                        </div>
                      </div>

                      {/* Tags */}
                      {lead.tags.length > 0 && (
                        <div className="pt-4 border-t border-gray-200">
                          <p className="text-sm font-medium text-gray-900 mb-2">Tags</p>
                          <div className="flex flex-wrap gap-2">
                            {lead.tags.map((tag, index) => (
                              <span
                                key={index}
                                className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800"
                              >
                                {tag}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* Sessions */}
                      {lead.sessions && lead.sessions.length > 0 && (
                        <div className="pt-4 border-t border-gray-200">
                          <p className="text-sm font-medium text-gray-900 mb-3">Conversas</p>
                          <div className="space-y-3">
                            {lead.sessions.map((session) => (
                              <div key={session.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                                <div className="flex items-center space-x-3">
                                  <ChatBubbleLeftRightIcon className="h-5 w-5 text-gray-400" />
                                  <div>
                                    <p className="text-sm font-medium text-gray-900">
                                      Sessão {session.status}
                                    </p>
                                    <p className="text-xs text-gray-600">
                                      {formatDateTime(session.created_at)}
                                      {session.current_step && (
                                        <span className="ml-2">• Etapa: {session.current_step}</span>
                                      )}
                                    </p>
                                  </div>
                                </div>
                                <Link
                                  href={`/conversations/${session.id}`}
                                  className="text-primary-600 hover:text-primary-700 text-sm font-medium"
                                >
                                  Ver conversa
                                </Link>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* Qualifications */}
                      {lead.qualifications && lead.qualifications.length > 0 && (
                        <div className="pt-4 border-t border-gray-200">
                          <p className="text-sm font-medium text-gray-900 mb-3">Qualificações</p>
                          <div className="space-y-3">
                            {lead.qualifications.map((qualification) => (
                              <div key={qualification.id} className="p-3 bg-green-50 rounded-lg">
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
                                  {qualification.patrimonio_faixa && (
                                    <div>
                                      <span className="font-medium">Patrimônio:</span>{' '}
                                      {qualification.patrimonio_faixa}
                                    </div>
                                  )}
                                  {qualification.urgencia && (
                                    <div>
                                      <span className="font-medium">Urgência:</span>{' '}
                                      {qualification.urgencia}
                                    </div>
                                  )}
                                  {qualification.objetivo && (
                                    <div className="md:col-span-2">
                                      <span className="font-medium">Objetivo:</span>{' '}
                                      {qualification.objetivo}
                                    </div>
                                  )}
                                  {qualification.score_final !== null && (
                                    <div>
                                      <span className="font-medium">Score Final:</span>{' '}
                                      {qualification.score_final}/100
                                    </div>
                                  )}
                                  {qualification.interesse_especialista !== null && (
                                    <div>
                                      <span className="font-medium">Interesse em especialista:</span>{' '}
                                      {qualification.interesse_especialista ? 'Sim' : 'Não'}
                                    </div>
                                  )}
                                </div>
                                {qualification.observacoes && (
                                  <div className="mt-2 text-sm">
                                    <span className="font-medium">Observações:</span>{' '}
                                    {qualification.observacoes}
                                  </div>
                                )}
                                <div className="mt-2 text-xs text-gray-500">
                                  {formatDateTime(qualification.created_at)}
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* Meetings */}
                      {lead.meetings && lead.meetings.length > 0 && (
                        <div className="pt-4 border-t border-gray-200">
                          <p className="text-sm font-medium text-gray-900 mb-3">Reuniões</p>
                          <div className="space-y-3">
                            {lead.meetings.map((meeting) => (
                              <div key={meeting.id} className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
                                <div className="flex items-center space-x-3">
                                  <CalendarDaysIcon className="h-5 w-5 text-blue-400" />
                                  <div>
                                    <p className="text-sm font-medium text-gray-900">
                                      Reunião {getStatusLabel(meeting.status)}
                                    </p>
                                    <div className="text-xs text-gray-600 space-y-1">
                                      {meeting.horario_sugestao_1 && (
                                        <div>Opção 1: {formatDateTime(meeting.horario_sugestao_1)}</div>
                                      )}
                                      {meeting.horario_sugestao_2 && (
                                        <div>Opção 2: {formatDateTime(meeting.horario_sugestao_2)}</div>
                                      )}
                                      {meeting.closer && (
                                        <div>Closer: {meeting.closer.name || meeting.closer.email}</div>
                                      )}
                                    </div>
                                  </div>
                                </div>
                                <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(meeting.status)}`}>
                                  {getStatusLabel(meeting.status)}
                                </span>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>

                    {/* Actions */}
                    <div className="mt-6 pt-4 border-t border-gray-200 flex justify-end space-x-3">
                      {lead.sessions && lead.sessions.length > 0 && (
                        <Link
                          href={`/conversations/${lead.sessions[0].id}`}
                          className="inline-flex items-center px-4 py-2 border border-primary-300 shadow-sm text-sm font-medium rounded-md text-primary-700 bg-primary-50 hover:bg-primary-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                        >
                          <ChatBubbleLeftRightIcon className="h-4 w-4 mr-2" />
                          Ver Conversa
                        </Link>
                      )}
                      
                      <button
                        type="button"
                        onClick={onClose}
                        className="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                      >
                        Fechar
                      </button>
                    </div>
                  </div>
                </div>
              </Dialog.Panel>
            </Transition.Child>
          </div>
        </div>
      </Dialog>
    </Transition.Root>
  )
}




