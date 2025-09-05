'use client'

import Link from 'next/link'
import { ArrowRightIcon } from '@heroicons/react/24/outline'

export function CTASection() {
  return (
    <div className="py-16 bg-gradient-to-r from-blue-600 to-blue-800">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-white">
        <h2 className="text-3xl md:text-4xl font-bold mb-4">
          Pronto para automatizar sua qualificação de leads?
        </h2>
        <p className="text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
          Configure seu sistema em minutos e comece a qualificar leads hoje mesmo
        </p>

        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
          <Link
            href="/signup"
            className="inline-flex items-center px-8 py-4 bg-white hover:bg-gray-100 text-blue-600 font-semibold rounded-lg transition-colors shadow-lg hover:shadow-xl group"
          >
            Criar Conta Gratuita
            <ArrowRightIcon className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
          </Link>
          
          <Link
            href="/login"
            className="inline-flex items-center px-8 py-4 bg-transparent hover:bg-white/10 text-white font-semibold rounded-lg border-2 border-white/30 hover:border-white/50 transition-colors"
          >
            Já tenho conta - Fazer Login
          </Link>
        </div>

        <p className="text-sm text-blue-200 mt-6">
          Sem cartão de crédito necessário • Configure em minutos
        </p>
      </div>
    </div>
  )
}
