'use client'

import { useState } from 'react'
import { DashboardLayout } from '@/components/layout/dashboard-layout'
import { UploadCSVModal } from '@/components/leads/upload-csv-modal'
import { DocumentArrowUpIcon, InformationCircleIcon } from '@heroicons/react/24/outline'
import { useRouter } from 'next/navigation'

export default function UploadPage() {
  const [showUploadModal, setShowUploadModal] = useState(false)
  const router = useRouter()

  const handleUploadComplete = () => {
    setShowUploadModal(false)
    // Redirecionar para a página de leads após upload bem-sucedido
    router.push('/leads')
  }

  return (
    <DashboardLayout>
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">Upload de Leads</h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Importe seus leads em lote através de arquivos CSV. 
            O sistema processará automaticamente os dados e criará os leads na sua base.
          </p>
        </div>

        {/* Info Card */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-8">
          <div className="flex">
            <InformationCircleIcon className="h-6 w-6 text-blue-600 mt-0.5" />
            <div className="ml-3">
              <h3 className="text-sm font-medium text-blue-900">
                Informações importantes sobre o upload
              </h3>
              <div className="mt-2 text-sm text-blue-700">
                <ul className="list-disc list-inside space-y-1">
                  <li><strong>Colunas obrigatórias:</strong> name (nome) e phone (telefone)</li>
                  <li><strong>Colunas opcionais:</strong> email, origem, tags</li>
                  <li><strong>Formato:</strong> Arquivo CSV com até 5MB</li>
                  <li><strong>Encoding:</strong> UTF-8 recomendado para caracteres especiais</li>
                  <li><strong>Separador:</strong> Vírgula (,)</li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        {/* Upload Card */}
        <div className="bg-white shadow rounded-lg p-8">
          <div className="text-center">
            <DocumentArrowUpIcon className="mx-auto h-16 w-16 text-gray-400 mb-4" />
            <h2 className="text-xl font-medium text-gray-900 mb-4">
              Pronto para importar seus leads?
            </h2>
            <p className="text-gray-600 mb-8">
              Clique no botão abaixo para iniciar o processo de upload do seu arquivo CSV.
            </p>
            
            <button
              onClick={() => setShowUploadModal(true)}
              className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              <DocumentArrowUpIcon className="h-5 w-5 mr-2" />
              Fazer Upload de CSV
            </button>
          </div>
        </div>

        {/* Recent Uploads - Placeholder */}
        <div className="mt-8">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Uploads Recentes</h3>
          <div className="bg-white shadow rounded-lg p-6">
            <div className="text-center text-gray-500">
              <p>Nenhum upload realizado ainda.</p>
              <p className="text-sm mt-1">Seus uploads recentes aparecerão aqui.</p>
            </div>
          </div>
        </div>
      </div>

      {/* Upload Modal */}
      <UploadCSVModal
        open={showUploadModal}
        onClose={() => setShowUploadModal(false)}
        onUploadComplete={handleUploadComplete}
      />
    </DashboardLayout>
  )
}










