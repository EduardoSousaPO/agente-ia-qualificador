'use client'

import { useState, useEffect } from 'react'
import { DashboardLayout } from '@/components/layout/dashboard-layout'
import { LoadingSpinner } from '@/components/ui/loading-spinner'
import { getAuthHeaders } from '@/lib/auth'
import toast from 'react-hot-toast'
import { PlusIcon, UserIcon } from '@heroicons/react/24/outline'

interface Tenant {
  id: string
  name: string
  domain?: string
  settings: any
  created_at: string
  updated_at: string
}

interface Member {
  id: string
  email: string
  role: string
  name: string
  created_at: string
}

export default function EmpresaPage() {
  const [tenant, setTenant] = useState<Tenant | null>(null)
  const [members, setMembers] = useState<Member[]>([])
  const [loading, setLoading] = useState(true)
  const [showAddMember, setShowAddMember] = useState(false)
  const [newMember, setNewMember] = useState({
    email: '',
    role: 'operator',
    name: ''
  })
  const [addingMember, setAddingMember] = useState(false)

  useEffect(() => {
    loadTenantData()
  }, [])

  const loadTenantData = async () => {
    try {
      setLoading(true)
      
      const response = await fetch('http://localhost:5000/api/tenants/me', {
        headers: getAuthHeaders()
      })
      
      const data = await response.json()
      
      if (data.success) {
        setTenant(data.tenant)
        setMembers(data.members || [])
      } else {
        toast.error(data.error || 'Erro ao carregar dados')
      }
    } catch (error) {
      console.error('Erro ao carregar tenant:', error)
      toast.error('Erro de conexão')
    } finally {
      setLoading(false)
    }
  }

  const handleAddMember = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!newMember.email || !newMember.role) {
      toast.error('Preencha todos os campos obrigatórios')
      return
    }

    setAddingMember(true)

    try {
      const response = await fetch(`http://localhost:5000/api/tenants/${tenant?.id}/members`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify(newMember)
      })

      const data = await response.json()

      if (data.success) {
        toast.success('Membro adicionado com sucesso!')
        setNewMember({ email: '', role: 'operator', name: '' })
        setShowAddMember(false)
        loadTenantData() // Recarregar lista
      } else {
        toast.error(data.error || 'Erro ao adicionar membro')
      }
    } catch (error) {
      console.error('Erro ao adicionar membro:', error)
      toast.error('Erro de conexão')
    } finally {
      setAddingMember(false)
    }
  }

  const getRoleName = (role: string) => {
    const roles = {
      'admin': 'Administrador',
      'operator': 'Operador',
      'viewer': 'Visualizador'
    }
    return roles[role as keyof typeof roles] || role
  }

  const getRoleBadgeColor = (role: string) => {
    const colors = {
      'admin': 'bg-red-100 text-red-800',
      'operator': 'bg-blue-100 text-blue-800',
      'viewer': 'bg-gray-100 text-gray-800'
    }
    return colors[role as keyof typeof colors] || 'bg-gray-100 text-gray-800'
  }

  if (loading) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center h-64">
          <LoadingSpinner />
        </div>
      </DashboardLayout>
    )
  }

  return (
    <DashboardLayout>
      <div className="space-y-8">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-thin text-gray-900">Configurações da Empresa</h1>
          <p className="mt-2 text-gray-600">Gerencie sua empresa e membros da equipe</p>
        </div>

        {/* Informações da Empresa */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-xl font-medium text-gray-900 mb-4">Informações da Empresa</h2>
          
          {tenant && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Nome da Empresa
                </label>
                <div className="p-3 bg-gray-50 rounded-md border">
                  {tenant.name}
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Domínio (Opcional)
                </label>
                <div className="p-3 bg-gray-50 rounded-md border">
                  {tenant.domain || 'Não configurado'}
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  ID da Empresa
                </label>
                <div className="p-3 bg-gray-50 rounded-md border font-mono text-sm">
                  {tenant.id}
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Criada em
                </label>
                <div className="p-3 bg-gray-50 rounded-md border">
                  {new Date(tenant.created_at).toLocaleDateString('pt-BR')}
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Membros da Equipe */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h2 className="text-xl font-medium text-gray-900">Membros da Equipe</h2>
              <p className="text-gray-600">Gerencie os membros que têm acesso ao sistema</p>
            </div>
            
            <button
              onClick={() => setShowAddMember(true)}
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              <PlusIcon className="h-4 w-4 mr-2" />
              Adicionar Membro
            </button>
          </div>

          {/* Lista de Membros */}
          <div className="space-y-4">
            {members.map((member) => (
              <div key={member.id} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                <div className="flex items-center space-x-4">
                  <div className="h-10 w-10 rounded-full bg-gray-100 flex items-center justify-center">
                    <UserIcon className="h-5 w-5 text-gray-500" />
                  </div>
                  
                  <div>
                    <h3 className="text-sm font-medium text-gray-900">
                      {member.name || member.email.split('@')[0]}
                    </h3>
                    <p className="text-sm text-gray-500">{member.email}</p>
                  </div>
                </div>
                
                <div className="flex items-center space-x-3">
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getRoleBadgeColor(member.role)}`}>
                    {getRoleName(member.role)}
                  </span>
                  
                  <span className="text-sm text-gray-500">
                    {new Date(member.created_at).toLocaleDateString('pt-BR')}
                  </span>
                </div>
              </div>
            ))}
            
            {members.length === 0 && (
              <div className="text-center py-8 text-gray-500">
                Nenhum membro encontrado
              </div>
            )}
          </div>
        </div>

        {/* Modal Adicionar Membro */}
        {showAddMember && (
          <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
            <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
              <div className="mt-3">
                <h3 className="text-lg font-medium text-gray-900 mb-4">
                  Adicionar Novo Membro
                </h3>
                
                <form onSubmit={handleAddMember} className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Email *
                    </label>
                    <input
                      type="email"
                      required
                      value={newMember.email}
                      onChange={(e) => setNewMember({ ...newMember, email: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                      placeholder="email@exemplo.com"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Nome (Opcional)
                    </label>
                    <input
                      type="text"
                      value={newMember.name}
                      onChange={(e) => setNewMember({ ...newMember, name: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                      placeholder="Nome do usuário"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Papel *
                    </label>
                    <select
                      required
                      value={newMember.role}
                      onChange={(e) => setNewMember({ ...newMember, role: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    >
                      <option value="operator">Operador</option>
                      <option value="admin">Administrador</option>
                      <option value="viewer">Visualizador</option>
                    </select>
                  </div>
                  
                  <div className="flex items-center justify-end space-x-3 pt-4">
                    <button
                      type="button"
                      onClick={() => setShowAddMember(false)}
                      className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                    >
                      Cancelar
                    </button>
                    
                    <button
                      type="submit"
                      disabled={addingMember}
                      className="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
                    >
                      {addingMember ? 'Adicionando...' : 'Adicionar'}
                    </button>
                  </div>
                </form>
              </div>
            </div>
          </div>
        )}
      </div>
    </DashboardLayout>
  )
}

