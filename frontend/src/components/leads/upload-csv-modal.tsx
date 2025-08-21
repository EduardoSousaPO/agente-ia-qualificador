'use client'

import { Fragment, useState, useCallback } from 'react'
import { Dialog, Transition } from '@headlessui/react'
import { XMarkIcon, DocumentArrowUpIcon, ExclamationTriangleIcon } from '@heroicons/react/24/outline'
import { useDropzone } from 'react-dropzone'
import { api } from '@/lib/api'
import { isValidCSVFile, formatFileSize } from '@/lib/utils'
import { UploadResult } from '@/types'
import toast from 'react-hot-toast'

interface UploadCSVModalProps {
  open: boolean
  onClose: () => void
  onUploadComplete: () => void
}

export function UploadCSVModal({ open, onClose, onUploadComplete }: UploadCSVModalProps) {
  const [file, setFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<UploadResult | null>(null)
  const [showResults, setShowResults] = useState(false)

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const uploadedFile = acceptedFiles[0]
    
    if (!uploadedFile) return
    
    if (!isValidCSVFile(uploadedFile)) {
      toast.error('Por favor, selecione um arquivo CSV válido')
      return
    }
    
    if (uploadedFile.size > 5 * 1024 * 1024) { // 5MB
      toast.error('Arquivo muito grande. Máximo 5MB')
      return
    }
    
    setFile(uploadedFile)
    setResult(null)
    setShowResults(false)
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/csv': ['.csv'],
      'application/vnd.ms-excel': ['.csv'],
      'text/plain': ['.txt']
    },
    multiple: false,
    maxSize: 5 * 1024 * 1024 // 5MB
  })

  const handleUpload = async () => {
    if (!file) return

    try {
      setLoading(true)
      const uploadResult = await api.uploadCSV(file)
      setResult(uploadResult)
      setShowResults(true)
      
      if (uploadResult.created > 0) {
        toast.success(`${uploadResult.created} lead(s) criado(s) com sucesso!`)
      }
      
      if (uploadResult.errors > 0) {
        toast.error(`${uploadResult.errors} erro(s) encontrado(s)`)
      }
    } catch (error: any) {
      console.error('Erro no upload:', error)
      toast.error(error.response?.data?.error || 'Erro no upload do arquivo')
    } finally {
      setLoading(false)
    }
  }

  const handleClose = () => {
    if (result && result.created > 0) {
      onUploadComplete()
    }
    
    setFile(null)
    setResult(null)
    setShowResults(false)
    onClose()
  }

  const downloadSample = () => {
    const csvContent = `name,phone,email,origem,tags
João Silva,11999999999,joao@email.com,newsletter,vip
Maria Santos,11888888888,maria@email.com,youtube,interessada
Pedro Oliveira,11777777777,,manual,`

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
    const link = document.createElement('a')
    const url = URL.createObjectURL(blob)
    link.setAttribute('href', url)
    link.setAttribute('download', 'exemplo-leads.csv')
    link.style.visibility = 'hidden'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  return (
    <Transition.Root show={open} as={Fragment}>
      <Dialog as="div" className="relative z-50" onClose={handleClose}>
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
                    onClick={handleClose}
                  >
                    <span className="sr-only">Fechar</span>
                    <XMarkIcon className="h-6 w-6" />
                  </button>
                </div>

                <div className="sm:flex sm:items-start">
                  <div className="mt-3 text-center sm:ml-0 sm:mt-0 sm:text-left w-full">
                    <Dialog.Title as="h3" className="text-base font-semibold leading-6 text-gray-900">
                      Upload de Leads (CSV)
                    </Dialog.Title>
                    
                    {!showResults ? (
                      <div className="mt-4 space-y-6">
                        <div className="text-sm text-gray-500">
                          <p>Faça upload de um arquivo CSV com seus leads. O arquivo deve conter as colunas:</p>
                          <ul className="mt-2 list-disc list-inside space-y-1">
                            <li><strong>name</strong> - Nome do lead (obrigatório)</li>
                            <li><strong>phone</strong> - Telefone do lead (obrigatório)</li>
                            <li><strong>email</strong> - Email do lead (opcional)</li>
                            <li><strong>origem</strong> - Origem do lead (opcional)</li>
                            <li><strong>tags</strong> - Tags separadas por vírgula (opcional)</li>
                          </ul>
                        </div>

                        {/* Download Sample */}
                        <div className="flex justify-end">
                          <button
                            onClick={downloadSample}
                            className="text-sm text-primary-600 hover:text-primary-700 font-medium"
                          >
                            Baixar arquivo de exemplo
                          </button>
                        </div>

                        {/* File Drop Zone */}
                        <div
                          {...getRootProps()}
                          className={`mt-4 flex justify-center px-6 pt-5 pb-6 border-2 border-dashed rounded-lg cursor-pointer transition-colors ${
                            isDragActive
                              ? 'border-primary-400 bg-primary-50'
                              : file
                              ? 'border-green-400 bg-green-50'
                              : 'border-gray-300 hover:border-gray-400'
                          }`}
                        >
                          <div className="space-y-1 text-center">
                            <DocumentArrowUpIcon className={`mx-auto h-12 w-12 ${
                              file ? 'text-green-600' : 'text-gray-400'
                            }`} />
                            <div className="flex text-sm text-gray-600">
                              <input {...getInputProps()} />
                              {file ? (
                                <div className="text-center">
                                  <p className="font-medium text-green-600">{file.name}</p>
                                  <p className="text-xs text-gray-500">{formatFileSize(file.size)}</p>
                                </div>
                              ) : (
                                <div>
                                  <span className="relative cursor-pointer rounded-md bg-white font-medium text-primary-600 focus-within:outline-none focus-within:ring-2 focus-within:ring-primary-500 focus-within:ring-offset-2 hover:text-primary-500">
                                    Clique para selecionar
                                  </span>
                                  <p className="pl-1">ou arraste e solte</p>
                                  <p className="text-xs text-gray-500">CSV até 5MB</p>
                                </div>
                              )}
                            </div>
                          </div>
                        </div>

                        {/* Actions */}
                        <div className="mt-5 sm:mt-6 sm:grid sm:grid-flow-row-dense sm:grid-cols-2 sm:gap-3">
                          <button
                            type="button"
                            onClick={handleUpload}
                            disabled={!file || loading}
                            className="inline-flex w-full justify-center rounded-md bg-primary-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primary-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-600 disabled:opacity-50 disabled:cursor-not-allowed sm:col-start-2"
                          >
                            {loading ? 'Enviando...' : 'Enviar Arquivo'}
                          </button>
                          <button
                            type="button"
                            onClick={handleClose}
                            disabled={loading}
                            className="mt-3 inline-flex w-full justify-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 sm:col-start-1 sm:mt-0 disabled:opacity-50 disabled:cursor-not-allowed"
                          >
                            Cancelar
                          </button>
                        </div>
                      </div>
                    ) : result && (
                      <div className="mt-4 space-y-4">
                        {/* Summary */}
                        <div className="bg-gray-50 rounded-lg p-4">
                          <h4 className="text-sm font-medium text-gray-900 mb-3">Resultado do Upload</h4>
                          <div className="grid grid-cols-2 gap-4 text-sm">
                            <div className="text-center">
                              <div className="text-2xl font-bold text-green-600">{result.created}</div>
                              <div className="text-gray-600">Leads criados</div>
                            </div>
                            <div className="text-center">
                              <div className="text-2xl font-bold text-red-600">{result.errors}</div>
                              <div className="text-gray-600">Erros</div>
                            </div>
                          </div>
                        </div>

                        {/* Errors */}
                        {result.leads_errors.length > 0 && (
                          <div className="bg-red-50 rounded-lg p-4">
                            <div className="flex">
                              <ExclamationTriangleIcon className="h-5 w-5 text-red-400 mt-0.5" />
                              <div className="ml-3">
                                <h4 className="text-sm font-medium text-red-800">
                                  Erros encontrados ({result.leads_errors.length})
                                </h4>
                                <div className="mt-2 max-h-40 overflow-y-auto">
                                  {result.leads_errors.slice(0, 10).map((error, index) => (
                                    <div key={index} className="text-sm text-red-700 py-1">
                                      <strong>Linha {error.row}:</strong> {error.error}
                                    </div>
                                  ))}
                                  {result.leads_errors.length > 10 && (
                                    <div className="text-sm text-red-600 font-medium mt-2">
                                      ... e mais {result.leads_errors.length - 10} erro(s)
                                    </div>
                                  )}
                                </div>
                              </div>
                            </div>
                          </div>
                        )}

                        {/* Action */}
                        <div className="mt-6">
                          <button
                            type="button"
                            onClick={handleClose}
                            className="w-full inline-flex justify-center rounded-md bg-primary-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primary-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-600"
                          >
                            Concluir
                          </button>
                        </div>
                      </div>
                    )}
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




