'use client'

import { useState, useEffect } from 'react'
import { DashboardLayout } from '@/components/layout/dashboard-layout'
import { useAuth } from '@/components/providers'
import toast from 'react-hot-toast'
import {
  CheckCircleIcon,
  XCircleIcon,
  ClockIcon,
  UserPlusIcon,
  BuildingOfficeIcon
} from '@heroicons/react/24/outline'

interface JoinRequest {
  id: string
  user_id: string
  user_email: string
  user_name: string
  company_name: string
  company_code: string
  status: 'pending' | 'approved' | 'rejected'
  created_at: string
  approved_at?: string
}

export default function JoinRequestsPage() {
  const [requests, setRequests] = useState<JoinRequest[]>([])
  const [loading, setLoading] = useState(true)
  const [processing, setProcessing] = useState<string | null>(null)
  const [filter, setFilter] = useState<'all' | 'pending' | 'approved' | 'rejected'>('all')
  const { user } = useAuth()

  useEffect(() => {
    loadJoinRequests()
  }, [user])

  const loadJoinRequests = async () => {
    if (!user?.tenant?.id) {
      setLoading(false)
      return
    }

    try {
      setLoading(true)
      const response = await fetch(`http://localhost:5000/api/tenants/${user.tenant.id}/join-requests`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token') || 'demo-token'}`,
          'Content-Type': 'application/json'
        }
      })

      if (response.ok) {
        const result = await response.json()
        setRequests(result.requests || [])
      } else {
        const errorResult = await response.json()
        toast.error(errorResult.error || 'Erro ao carregar solicitações')
      }
    } catch (error) {
      console.error('Erro ao carregar solicitações:', error)
      toast.error('Erro ao carregar solicitações')
    } finally {
      setLoading(false)
    }
  }

  const handleApprove = async (requestId: string, role: string = 'member') => {
    try {
      setProcessing(requestId)
      const response = await fetch(`http://localhost:5000/api/join-requests/${requestId}/approve`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token') || 'demo-token'}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ role })
      })

      if (response.ok) {
        toast.success('Solicitação aprovada com sucesso!')
        loadJoinRequests() // Recarregar lista
      } else {
        const result = await response.json()
        toast.error(result.error || 'Erro ao aprovar solicitação')
      }
    } catch (error) {
      console.error('Erro ao aprovar solicitação:', error)
      toast.error('Erro ao aprovar solicitação')
    } finally {
      setProcessing(null)
    }
  }

  const handleReject = async (requestId: string) => {
    if (!confirm('Tem certeza que deseja rejeitar esta solicitação?')) return

    try {
      setProcessing(requestId)
      const response = await fetch(`http://localhost:5000/api/join-requests/${requestId}/reject`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token') || 'demo-token'}`,
          'Content-Type': 'application/json'
        }
      })

      if (response.ok) {
        toast.success('Solicitação rejeitada')
        loadJoinRequests() // Recarregar lista
      } else {
        const result = await response.json()
        toast.error(result.error || 'Erro ao rejeitar solicitação')
      }
    } catch (error) {
      console.error('Erro ao rejeitar solicitação:', error)
      toast.error('Erro ao rejeitar solicitação')
    } finally {
      setProcessing(null)
    }
  }

  const filteredRequests = requests.filter(request => {
    if (filter === 'all') return true
    return request.status === filter
  })

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'pending':
        return (
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
            <ClockIcon className="w-3 h-3 mr-1" />
            Pendente
          </span>
        )
      case 'approved':
        return (
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
            <CheckCircleIcon className="w-3 h-3 mr-1" />
            Aprovado
          </span>
        )
      case 'rejected':
        return (
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
            <XCircleIcon className="w-3 h-3 mr-1" />
            Rejeitado
          </span>
        )
      default:
        return null
    }
  }

  if (loading) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        </div>
      </DashboardLayout>
    )
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="md:flex md:items-center md:justify-between">
          <div className="flex-1 min-w-0">
            <h1 className="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate">
              Solicitações de Acesso
            </h1>
            <p className="mt-1 text-sm text-gray-500">
              Gerencie solicitações de novos membros para {user?.tenant?.name}
            </p>
          </div>
        </div>

        {/* Estatísticas */}
        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <ClockIcon className="h-6 w-6 text-yellow-400" />
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">Pendentes</dt>
                    <dd className="text-lg font-medium text-gray-900">
                      {requests.filter(r => r.status === 'pending').length}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <CheckCircleIcon className="h-6 w-6 text-green-400" />
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">Aprovadas</dt>
                    <dd className="text-lg font-medium text-gray-900">
                      {requests.filter(r => r.status === 'approved').length}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <XCircleIcon className="h-6 w-6 text-red-400" />
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">Rejeitadas</dt>
                    <dd className="text-lg font-medium text-gray-900">
                      {requests.filter(r => r.status === 'rejected').length}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <UserPlusIcon className="h-6 w-6 text-blue-400" />
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">Total</dt>
                    <dd className="text-lg font-medium text-gray-900">{requests.length}</dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Filtros */}
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <div className="flex flex-wrap gap-2">
              {(['all', 'pending', 'approved', 'rejected'] as const).map((status) => (
                <button
                  key={status}
                  onClick={() => setFilter(status)}
                  className={`px-3 py-2 text-sm font-medium rounded-md ${
                    filter === status
                      ? 'bg-blue-100 text-blue-700'
                      : 'text-gray-500 hover:text-gray-700 hover:bg-gray-100'
                  }`}
                >
                  {status === 'all' ? 'Todas' :
                   status === 'pending' ? 'Pendentes' :
                   status === 'approved' ? 'Aprovadas' : 'Rejeitadas'}
                  <span className="ml-2 bg-gray-200 text-gray-600 px-2 py-0.5 rounded-full text-xs">
                    {status === 'all' ? requests.length : requests.filter(r => r.status === status).length}
                  </span>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Lista de Solicitações */}
        <div className="bg-white shadow overflow-hidden sm:rounded-md">
          <div className="px-4 py-5 sm:px-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900">
              Solicitações ({filteredRequests.length})
            </h3>
            <p className="mt-1 max-w-2xl text-sm text-gray-500">
              {filter === 'pending' ? 'Solicitações aguardando sua aprovação' : 
               filter === 'approved' ? 'Solicitações já aprovadas' :
               filter === 'rejected' ? 'Solicitações rejeitadas' :
               'Todas as solicitações de acesso'}
            </p>
          </div>
          
          {filteredRequests.length === 0 ? (
            <div className="text-center py-12">
              <BuildingOfficeIcon className="mx-auto h-12 w-12 text-gray-400" />
              <h3 className="mt-2 text-sm font-medium text-gray-900">
                {filter === 'pending' ? 'Nenhuma solicitação pendente' : 'Nenhuma solicitação encontrada'}
              </h3>
              <p className="mt-1 text-sm text-gray-500">
                {filter === 'pending' ? 'Quando houver novas solicitações, elas aparecerão aqui.' : 
                 `Não há solicitações com status "${filter}".`}
              </p>
            </div>
          ) : (
            <ul className="divide-y divide-gray-200">
              {filteredRequests.map((request) => (
                <li key={request.id}>
                  <div className="px-4 py-4 sm:px-6">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center">
                        <div className="flex-shrink-0 h-10 w-10">
                          <div className="h-10 w-10 rounded-full bg-gray-300 flex items-center justify-center">
                            <span className="text-sm font-medium text-gray-700">
                              {request.user_name?.charAt(0) || request.user_email?.charAt(0) || '?'}
                            </span>
                          </div>
                        </div>
                        <div className="ml-4">
                          <div className="flex items-center">
                            <p className="text-sm font-medium text-gray-900 truncate">
                              {request.user_name || 'Nome não informado'}
                            </p>
                            <div className="ml-2">
                              {getStatusBadge(request.status)}
                            </div>
                          </div>
                          <p className="text-sm text-gray-500">{request.user_email}</p>
                          <div className="mt-1 flex items-center text-sm text-gray-500">
                            <BuildingOfficeIcon className="flex-shrink-0 mr-1.5 h-4 w-4 text-gray-400" />
                            <span className="truncate">
                              {request.company_name} ({request.company_code})
                            </span>
                          </div>
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        {request.status === 'pending' && (
                          <>
                            <button
                              onClick={() => handleApprove(request.id)}
                              disabled={processing === request.id}
                              className="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50"
                            >
                              {processing === request.id ? (
                                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-1"></div>
                              ) : (
                                <CheckCircleIcon className="h-4 w-4 mr-1" />
                              )}
                              Aprovar
                            </button>
                            <button
                              onClick={() => handleReject(request.id)}
                              disabled={processing === request.id}
                              className="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50"
                            >
                              {processing === request.id ? (
                                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-1"></div>
                              ) : (
                                <XCircleIcon className="h-4 w-4 mr-1" />
                              )}
                              Rejeitar
                            </button>
                          </>
                        )}
                        <div className="text-sm text-gray-500">
                          {new Date(request.created_at).toLocaleDateString('pt-BR', {
                            day: '2-digit',
                            month: '2-digit',
                            year: 'numeric',
                            hour: '2-digit',
                            minute: '2-digit'
                          })}
                        </div>
                      </div>
                    </div>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </DashboardLayout>
  )
}










