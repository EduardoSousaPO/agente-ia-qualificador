'use client'

import { useState, useEffect } from 'react'
import { DashboardLayout } from '@/components/layout/dashboard-layout'
import { useAuth } from '@/components/providers'
import toast from 'react-hot-toast'
import {
  PlusIcon,
  BuildingOfficeIcon,
  UsersIcon,
  ClockIcon,
  PencilIcon,
  EyeIcon,
  CheckCircleIcon,
  XCircleIcon
} from '@heroicons/react/24/outline'

interface Company {
  id: string
  name: string
  slug: string
  code: string
  created_at: string
  settings: {
    company_type?: string
    max_members?: number
    description?: string
  }
  member_count: number
  pending_requests: number
}

interface NewCompany {
  name: string
  code: string
  slug: string
  company_type: string
  max_members: number
  description: string
}

export default function CompaniesPage() {
  const [companies, setCompanies] = useState<Company[]>([])
  const [loading, setLoading] = useState(true)
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [editingCompany, setEditingCompany] = useState<Company | null>(null)
  const [newCompany, setNewCompany] = useState<NewCompany>({
    name: '',
    code: '',
    slug: '',
    company_type: 'investment_advisory',
    max_members: 50,
    description: ''
  })
  const [submitting, setSubmitting] = useState(false)
  const { user } = useAuth()

  useEffect(() => {
    loadCompanies()
  }, [])

  const loadCompanies = async () => {
    try {
      setLoading(true)
      const response = await fetch('http://localhost:5000/api/companies', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token') || 'demo-token'}`,
          'Content-Type': 'application/json'
        }
      })

      if (response.ok) {
        const result = await response.json()
        setCompanies(result.companies || [])
      } else {
        const errorResult = await response.json()
        toast.error(errorResult.error || 'Erro ao carregar empresas')
      }
    } catch (error) {
      console.error('Erro ao carregar empresas:', error)
      toast.error('Erro ao carregar empresas')
    } finally {
      setLoading(false)
    }
  }

  const generateSlug = (name: string) => {
    return name
      .toLowerCase()
      .replace(/[^a-z0-9\s-]/g, '')
      .replace(/\s+/g, '-')
      .replace(/-+/g, '-')
      .replace(/^-|-$/g, '')
  }

  const handleNameChange = (name: string) => {
    setNewCompany(prev => ({
      ...prev,
      name,
      slug: prev.slug || generateSlug(name)
    }))
  }

  const handleCreateCompany = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!newCompany.name.trim() || !newCompany.code.trim()) {
      toast.error('Nome e código são obrigatórios')
      return
    }

    try {
      setSubmitting(true)
      const response = await fetch('http://localhost:5000/api/companies', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token') || 'demo-token'}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          ...newCompany,
          code: newCompany.code.toUpperCase()
        })
      })

      const result = await response.json()

      if (response.ok) {
        toast.success(result.message || 'Empresa criada com sucesso!')
        setShowCreateModal(false)
        setNewCompany({
          name: '',
          code: '',
          slug: '',
          company_type: 'investment_advisory',
          max_members: 50,
          description: ''
        })
        loadCompanies()
      } else {
        toast.error(result.error || 'Erro ao criar empresa')
      }
    } catch (error) {
      console.error('Erro ao criar empresa:', error)
      toast.error('Erro ao criar empresa')
    } finally {
      setSubmitting(false)
    }
  }

  const getCompanyTypeLabel = (type: string) => {
    const types: Record<string, string> = {
      'investment_advisory': 'Assessoria de Investimentos',
      'financial_consulting': 'Consultoria Financeira',
      'wealth_management': 'Gestão de Patrimônio',
      'insurance': 'Seguros',
      'other': 'Outros'
    }
    return types[type] || type
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
              Gerenciar Empresas
            </h1>
            <p className="mt-1 text-sm text-gray-500">
              Crie e gerencie empresas no sistema
            </p>
          </div>
          <div className="mt-4 flex md:mt-0 md:ml-4">
            <button
              onClick={() => setShowCreateModal(true)}
              className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              <PlusIcon className="h-4 w-4 mr-2" />
              Nova Empresa
            </button>
          </div>
        </div>

        {/* Estatísticas */}
        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <BuildingOfficeIcon className="h-6 w-6 text-blue-400" />
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">Total de Empresas</dt>
                    <dd className="text-lg font-medium text-gray-900">{companies.length}</dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <UsersIcon className="h-6 w-6 text-green-400" />
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">Total de Membros</dt>
                    <dd className="text-lg font-medium text-gray-900">
                      {companies.reduce((sum, c) => sum + c.member_count, 0)}
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
                  <ClockIcon className="h-6 w-6 text-yellow-400" />
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">Solicitações Pendentes</dt>
                    <dd className="text-lg font-medium text-gray-900">
                      {companies.reduce((sum, c) => sum + c.pending_requests, 0)}
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
                  <CheckCircleIcon className="h-6 w-6 text-purple-400" />
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">Empresas Ativas</dt>
                    <dd className="text-lg font-medium text-gray-900">{companies.length}</dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Lista de Empresas */}
        <div className="bg-white shadow overflow-hidden sm:rounded-md">
          <div className="px-4 py-5 sm:px-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900">
              Empresas Cadastradas ({companies.length})
            </h3>
            <p className="mt-1 max-w-2xl text-sm text-gray-500">
              Gerencie todas as empresas do sistema
            </p>
          </div>
          
          {companies.length === 0 ? (
            <div className="text-center py-12">
              <BuildingOfficeIcon className="mx-auto h-12 w-12 text-gray-400" />
              <h3 className="mt-2 text-sm font-medium text-gray-900">Nenhuma empresa cadastrada</h3>
              <p className="mt-1 text-sm text-gray-500">
                Comece criando a primeira empresa do sistema.
              </p>
              <div className="mt-6">
                <button
                  onClick={() => setShowCreateModal(true)}
                  className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
                >
                  <PlusIcon className="h-4 w-4 mr-2" />
                  Nova Empresa
                </button>
              </div>
            </div>
          ) : (
            <ul className="divide-y divide-gray-200">
              {companies.map((company) => (
                <li key={company.id}>
                  <div className="px-4 py-4 sm:px-6">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center">
                        <div className="flex-shrink-0 h-10 w-10">
                          <div className="h-10 w-10 rounded-lg bg-blue-100 flex items-center justify-center">
                            <BuildingOfficeIcon className="h-6 w-6 text-blue-600" />
                          </div>
                        </div>
                        <div className="ml-4">
                          <div className="flex items-center">
                            <p className="text-sm font-medium text-gray-900 truncate">
                              {company.name}
                            </p>
                            <span className="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                              {company.code}
                            </span>
                          </div>
                          <p className="text-sm text-gray-500">/{company.slug}</p>
                          <div className="mt-1 flex items-center text-sm text-gray-500">
                            <span className="truncate">
                              {getCompanyTypeLabel(company.settings?.company_type || 'other')}
                            </span>
                            <span className="mx-2">•</span>
                            <span>Máx. {company.settings?.max_members || 50} membros</span>
                          </div>
                        </div>
                      </div>
                      <div className="flex items-center space-x-4">
                        <div className="text-right text-sm text-gray-500">
                          <div className="font-medium text-gray-900">{company.member_count} membros</div>
                          {company.pending_requests > 0 && (
                            <div className="text-yellow-600">{company.pending_requests} pendentes</div>
                          )}
                        </div>
                        <div className="flex space-x-2">
                          <button
                            onClick={() => setEditingCompany(company)}
                            className="inline-flex items-center p-2 border border-gray-300 rounded-md text-gray-400 hover:text-gray-500 hover:border-gray-400"
                          >
                            <PencilIcon className="h-4 w-4" />
                          </button>
                        </div>
                      </div>
                    </div>
                    {company.settings?.description && (
                      <div className="mt-2 text-sm text-gray-600">
                        {company.settings.description}
                      </div>
                    )}
                    <div className="mt-2 text-xs text-gray-400">
                      Criada em {new Date(company.created_at).toLocaleDateString('pt-BR', {
                        day: '2-digit',
                        month: '2-digit',
                        year: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit'
                      })}
                    </div>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>

      {/* Modal Criar Empresa */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-full max-w-2xl shadow-lg rounded-md bg-white">
            <div className="mt-3">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Nova Empresa</h3>
              <form onSubmit={handleCreateCompany} className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Nome da Empresa *</label>
                    <input
                      type="text"
                      value={newCompany.name}
                      onChange={(e) => handleNameChange(e.target.value)}
                      className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                      placeholder="Ex: Consultoria XYZ Ltda"
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Código da Empresa *</label>
                    <input
                      type="text"
                      value={newCompany.code}
                      onChange={(e) => setNewCompany(prev => ({ ...prev, code: e.target.value.toUpperCase() }))}
                      className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                      placeholder="Ex: XYZ2024"
                      pattern="[A-Z0-9]{4,20}"
                      title="4-20 caracteres, apenas letras e números"
                      required
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700">Slug (URL)</label>
                  <input
                    type="text"
                    value={newCompany.slug}
                    onChange={(e) => setNewCompany(prev => ({ ...prev, slug: e.target.value }))}
                    className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    placeholder="consultoria-xyz (gerado automaticamente)"
                  />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Tipo de Empresa</label>
                    <select
                      value={newCompany.company_type}
                      onChange={(e) => setNewCompany(prev => ({ ...prev, company_type: e.target.value }))}
                      className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    >
                      <option value="investment_advisory">Assessoria de Investimentos</option>
                      <option value="financial_consulting">Consultoria Financeira</option>
                      <option value="wealth_management">Gestão de Patrimônio</option>
                      <option value="insurance">Seguros</option>
                      <option value="other">Outros</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Máximo de Membros</label>
                    <input
                      type="number"
                      value={newCompany.max_members}
                      onChange={(e) => setNewCompany(prev => ({ ...prev, max_members: parseInt(e.target.value) || 50 }))}
                      className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                      min="1"
                      max="1000"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700">Descrição</label>
                  <textarea
                    value={newCompany.description}
                    onChange={(e) => setNewCompany(prev => ({ ...prev, description: e.target.value }))}
                    rows={3}
                    className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    placeholder="Descrição opcional da empresa..."
                  />
                </div>

                <div className="flex justify-end space-x-3 pt-4">
                  <button
                    type="button"
                    onClick={() => setShowCreateModal(false)}
                    className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
                    disabled={submitting}
                  >
                    Cancelar
                  </button>
                  <button
                    type="submit"
                    disabled={submitting}
                    className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50"
                  >
                    {submitting ? 'Criando...' : 'Criar Empresa'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </DashboardLayout>
  )
}










