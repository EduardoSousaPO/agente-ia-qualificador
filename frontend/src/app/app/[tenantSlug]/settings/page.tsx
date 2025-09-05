'use client'

import { useTenant } from '@/hooks/useTenant'
import { useState, useEffect } from 'react'
import { LoadingSpinner } from '@/components/ui/loading-spinner'
import { 
  UserGroupIcon,
  CogIcon,
  EnvelopeIcon,
  PlusIcon,
  TrashIcon,
  CheckCircleIcon,
  ClockIcon,
  XCircleIcon
} from '@heroicons/react/24/outline'
import { api } from '@/lib/api'
import { TenantSettingsForm } from '@/components/settings/tenant-settings-form'
import toast from 'react-hot-toast'

interface Member {
  user_id: string
  email: string
  name: string
  role: string
  created_at: string
}

interface Invite {
  id: string
  email: string
  role: string
  status: 'pending' | 'accepted' | 'revoked'
  created_at: string
}

export default function TenantSettings() {
  const { currentTenant, loading: tenantLoading, refreshTenant } = useTenant()
  const [members, setMembers] = useState<Member[]>([])
  const [invites, setInvites] = useState<Invite[]>([])
  const [loading, setLoading] = useState(true)
  const [showInviteModal, setShowInviteModal] = useState(false)
  const [inviteForm, setInviteForm] = useState({
    email: '',
    role: 'member'
  })

  useEffect(() => {
    if (currentTenant) {
      loadMembersAndInvites()
    }
  }, [currentTenant])

  const loadMembersAndInvites = async () => {
    if (!currentTenant) return
    
    try {
      setLoading(true)
      
      const [membersResponse, invitesResponse] = await Promise.all([
        api.getTenantMembers(currentTenant.id).catch(() => ({ users: [] })),
        api.getTenantInvites(currentTenant.id).catch(() => ({ invites: [] }))
      ])
      
      // Mapear dados da API para o formato esperado
      setMembers(membersResponse.users || [])
      setInvites(invitesResponse.invites || [])
      
    } catch (error) {
      console.error('Erro ao carregar membros e convites:', error)
      toast.error('Erro ao carregar dados dos membros')
    } finally {
      setLoading(false)
    }
  }

  const handleCreateInvite = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!currentTenant) return

    try {
      await api.createInvite(currentTenant.id, inviteForm)
      toast.success('Convite enviado com sucesso!')
      setShowInviteModal(false)
      setInviteForm({ email: '', role: 'member' })
      loadMembersAndInvites()
    } catch (error) {
      toast.error('Erro ao enviar convite')
      console.error('Erro ao criar convite:', error)
    }
  }

  const handleRevokeInvite = async (inviteId: string) => {
    try {
      await api.revokeInvite(inviteId)
      toast.success('Convite revogado com sucesso!')
      loadMembersAndInvites()
    } catch (error) {
      console.error('Erro ao revogar convite:', error)
      toast.error('Erro ao revogar convite')
    }
  }

  const handleRemoveMember = async (userId: string) => {
    if (!currentTenant || !confirm('Tem certeza que deseja remover este membro?')) return

    try {
      await api.removeTenantMember(currentTenant.id, userId)
      toast.success('Membro removido com sucesso!')
      loadMembersAndInvites()
    } catch (error) {
      console.error('Erro ao remover membro:', error)
      toast.error('Erro ao remover membro')
    }
  }

  const getRoleLabel = (role: string) => {
    const labels = {
      owner: 'Proprietário',
      admin: 'Administrador', 
      member: 'Membro'
    }
    return labels[role as keyof typeof labels] || role
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'pending':
        return <ClockIcon className="h-4 w-4 text-yellow-500" />
      case 'accepted':
        return <CheckCircleIcon className="h-4 w-4 text-green-500" />
      case 'revoked':
        return <XCircleIcon className="h-4 w-4 text-red-500" />
      default:
        return null
    }
  }

  if (tenantLoading || loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <LoadingSpinner size="lg" />
      </div>
    )
  }

  if (!currentTenant) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <h2 className="text-xl font-semibold text-gray-900 mb-2">
            Tenant não encontrado
          </h2>
          <p className="text-gray-600">
            Verifique se você tem acesso a este tenant.
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Configurações</h1>
        <p className="text-gray-600 mt-1">
          Gerencie {currentTenant.name} e seus membros
        </p>
      </div>

      {/* Tenant Settings */}
      <TenantSettingsForm tenantId={currentTenant.id} />

      {/* Tenant Info */}
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-lg font-medium text-gray-900 mb-4 flex items-center gap-2">
          <CogIcon className="h-5 w-5" />
          Informações da Organização
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Nome
            </label>
            <input
              type="text"
              value={currentTenant.name}
              disabled
              className="w-full px-3 py-2 border border-gray-300 rounded-lg bg-gray-50"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Slug
            </label>
            <input
              type="text"
              value={currentTenant.slug}
              disabled
              className="w-full px-3 py-2 border border-gray-300 rounded-lg bg-gray-50"
            />
          </div>
        </div>
      </div>

      {/* Members Section */}
      <div className="bg-white shadow rounded-lg p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-lg font-medium text-gray-900 flex items-center gap-2">
            <UserGroupIcon className="h-5 w-5" />
            Membros ({members.length})
          </h2>
          <button
            onClick={() => setShowInviteModal(true)}
            className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 flex items-center gap-2"
          >
            <PlusIcon className="h-4 w-4" />
            Convidar Membro
          </button>
        </div>

        {/* Members Table */}
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Usuário
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Função
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Adicionado em
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Ações
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {members.map((member) => (
                <tr key={member.user_id}>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div>
                      <div className="text-sm font-medium text-gray-900">
                        {member.name}
                      </div>
                      <div className="text-sm text-gray-500">
                        {member.email}
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                      {getRoleLabel(member.role)}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {new Date(member.created_at).toLocaleDateString('pt-BR')}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    {member.role !== 'owner' && (
                      <button
                        onClick={() => handleRemoveMember(member.user_id)}
                        className="text-red-600 hover:text-red-900"
                      >
                        <TrashIcon className="h-4 w-4" />
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Pending Invites */}
      {invites.length > 0 && (
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-lg font-medium text-gray-900 mb-4 flex items-center gap-2">
            <EnvelopeIcon className="h-5 w-5" />
            Convites Pendentes ({invites.length})
          </h2>

          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Email
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Função
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Enviado em
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Ações
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {invites.map((invite) => (
                  <tr key={invite.id}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {invite.email}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                        {getRoleLabel(invite.role)}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center gap-1">
                        {getStatusIcon(invite.status)}
                        <span className="text-sm text-gray-500 capitalize">
                          {invite.status === 'pending' ? 'Pendente' : 
                           invite.status === 'accepted' ? 'Aceito' : 'Revogado'}
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {new Date(invite.created_at).toLocaleDateString('pt-BR')}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      {invite.status === 'pending' && (
                        <button
                          onClick={() => handleRevokeInvite(invite.id)}
                          className="text-red-600 hover:text-red-900"
                        >
                          Revogar
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Invite Modal */}
      {showInviteModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h3 className="text-lg font-medium text-gray-900 mb-4">
              Convidar Novo Membro
            </h3>
            
            <form onSubmit={handleCreateInvite} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Email
                </label>
                <input
                  type="email"
                  required
                  value={inviteForm.email}
                  onChange={(e) => setInviteForm(prev => ({ ...prev, email: e.target.value }))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  placeholder="email@exemplo.com"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Função
                </label>
                <select
                  value={inviteForm.role}
                  onChange={(e) => setInviteForm(prev => ({ ...prev, role: e.target.value }))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                >
                  <option value="member">Membro</option>
                  <option value="admin">Administrador</option>
                </select>
              </div>
              
              <div className="flex justify-end gap-3 pt-4">
                <button
                  type="button"
                  onClick={() => setShowInviteModal(false)}
                  className="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
                >
                  Enviar Convite
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}

