'use client'

import { useTenant } from '@/hooks/useTenant'
import { useState, useEffect } from 'react'
import { LoadingSpinner } from '@/components/ui/loading-spinner'
import { 
  BookOpenIcon, 
  PlusIcon, 
  DocumentTextIcon,
  FolderIcon,
  MagnifyingGlassIcon
} from '@heroicons/react/24/outline'

interface KnowledgeItem {
  id: string
  title: string
  content: string
  type: 'document' | 'faq' | 'process'
  category: string
  created_at: string
  updated_at: string
}

export default function TenantKnowledge() {
  const { currentTenant, loading: tenantLoading } = useTenant()
  const [knowledgeItems, setKnowledgeItems] = useState<KnowledgeItem[]>([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('all')

  useEffect(() => {
    if (currentTenant) {
      loadKnowledgeBase()
    }
  }, [currentTenant])

  const loadKnowledgeBase = async () => {
    try {
      setLoading(true)
      
      if (!currentTenant?.id) return
      
      // Usar API real para buscar base de conhecimento
      const response = await fetch(`http://localhost:5000/api/knowledge-base/${currentTenant.id}`)
      
      if (response.ok) {
        const result = await response.json()
        
        if (result.success && result.data) {
          // Converter para formato de KnowledgeItem
          const knowledgeItem: KnowledgeItem = {
            id: '1',
            title: 'Base de Conhecimento da Empresa',
            content: result.data.content || 'Base de conhecimento vazia',
            type: 'document',
            category: 'Empresa',
            created_at: result.data.created_at || new Date().toISOString(),
            updated_at: result.data.updated_at || new Date().toISOString()
          }
          
          setKnowledgeItems([knowledgeItem])
        } else {
          setKnowledgeItems([])
        }
      } else {
        console.error('Erro na API:', response.status)
        setKnowledgeItems([])
      }
    } catch (error) {
      console.error('Erro ao carregar base de conhecimento:', error)
      setKnowledgeItems([])
    } finally {
      setLoading(false)
    }
  }

  const filteredItems = knowledgeItems.filter(item => {
    const matchesSearch = item.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         item.content.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesCategory = selectedCategory === 'all' || item.category === selectedCategory
    return matchesSearch && matchesCategory
  })

  const categories = ['all', ...Array.from(new Set(knowledgeItems.map(item => item.category)))]

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'document':
        return <DocumentTextIcon className="h-5 w-5" />
      case 'faq':
        return <BookOpenIcon className="h-5 w-5" />
      case 'process':
        return <FolderIcon className="h-5 w-5" />
      default:
        return <DocumentTextIcon className="h-5 w-5" />
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
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Base de Conhecimento</h1>
          <p className="text-gray-600 mt-1">
            Gerencie o conhecimento de {currentTenant.name}
          </p>
        </div>
        <button className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 flex items-center gap-2">
          <PlusIcon className="h-4 w-4" />
          Novo Documento
        </button>
      </div>

      {/* Search and Filters */}
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="flex-1 relative">
          <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
          <input
            type="text"
            placeholder="Buscar na base de conhecimento..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
          />
        </div>
        <select
          value={selectedCategory}
          onChange={(e) => setSelectedCategory(e.target.value)}
          className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
        >
          {categories.map(category => (
            <option key={category} value={category}>
              {category === 'all' ? 'Todas as categorias' : category}
            </option>
          ))}
        </select>
      </div>

      {/* Knowledge Items Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredItems.map((item) => (
          <div
            key={item.id}
            className="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow cursor-pointer"
          >
            <div className="flex items-start gap-3 mb-3">
              <div className="text-primary-600">
                {getTypeIcon(item.type)}
              </div>
              <div className="flex-1">
                <h3 className="font-medium text-gray-900 mb-1">{item.title}</h3>
                <span className="inline-block px-2 py-1 text-xs bg-gray-100 text-gray-600 rounded">
                  {item.category}
                </span>
              </div>
            </div>
            
            <p className="text-sm text-gray-600 mb-4 line-clamp-3">
              {item.content}
            </p>
            
            <div className="text-xs text-gray-500">
              Atualizado em {new Date(item.updated_at).toLocaleDateString('pt-BR')}
            </div>
          </div>
        ))}
      </div>

      {/* Empty State */}
      {filteredItems.length === 0 && (
        <div className="text-center py-12">
          <BookOpenIcon className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">
            Nenhum documento encontrado
          </h3>
          <p className="mt-1 text-sm text-gray-500">
            {searchTerm || selectedCategory !== 'all' 
              ? 'Tente ajustar os filtros de busca.'
              : 'Comece criando seu primeiro documento de conhecimento.'
            }
          </p>
        </div>
      )}
    </div>
  )
}





