'use client'

import { Lead } from '@/types'
import { formatTimeAgo, getStatusColor, getStatusLabel } from '@/lib/utils'
import Link from 'next/link'
import { EyeIcon } from '@heroicons/react/24/outline'

interface RecentLeadsProps {
  leads: Lead[]
}

export function RecentLeads({ leads }: RecentLeadsProps) {
  if (leads.length === 0) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-500">Nenhum lead encontrado</p>
      </div>
    )
  }

  return (
    <div className="overflow-hidden">
      <div className="flow-root">
        <ul className="-my-5 divide-y divide-gray-200">
          {leads.map((lead) => (
            <li key={lead.id} className="py-4">
              <div className="flex items-center space-x-4">
                {/* Avatar */}
                <div className="flex-shrink-0">
                  <div className="w-10 h-10 bg-gray-300 rounded-full flex items-center justify-center">
                    <span className="text-gray-700 font-medium text-sm">
                      {lead.name.charAt(0).toUpperCase()}
                    </span>
                  </div>
                </div>

                {/* Info */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-gray-900 truncate">
                        {lead.name}
                      </p>
                      <p className="text-sm text-gray-500 truncate">
                        {lead.phone} • {lead.email || 'Sem email'}
                      </p>
                    </div>
                    <div className="flex items-center space-x-2">
                      <span
                        className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(
                          lead.status
                        )}`}
                      >
                        {getStatusLabel(lead.status)}
                      </span>
                    </div>
                  </div>

                  <div className="flex items-center justify-between mt-2">
                    <div className="flex items-center space-x-4 text-sm text-gray-500">
                      <span>Score: {lead.score}/100</span>
                      <span>Origem: {lead.origem}</span>
                      <span>{formatTimeAgo(lead.created_at)}</span>
                    </div>

                    <Link
                      href={`/leads/${lead.id}`}
                      className="inline-flex items-center px-3 py-1 border border-gray-300 shadow-sm text-xs font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                    >
                      <EyeIcon className="w-4 h-4 mr-1" />
                      Ver
                    </Link>
                  </div>
                </div>
              </div>
            </li>
          ))}
        </ul>
      </div>

      {/* Ver todos */}
      <div className="mt-6 border-t border-gray-200 pt-4">
        <Link
          href="/leads"
          className="w-full flex justify-center items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
        >
          Ver todos os leads
        </Link>
      </div>
    </div>
  )
}




