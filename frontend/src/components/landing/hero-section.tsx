'use client'

import Link from 'next/link'
import { ArrowRightIcon } from '@heroicons/react/24/outline'

export function HeroSection() {
  return (
    <div className="relative overflow-hidden bg-gradient-to-br from-blue-900 via-blue-800 to-purple-900">
      <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxnIGZpbGw9IiNmZmZmZmYiIGZpbGwtb3BhY2l0eT0iMC4xIj48Y2lyY2xlIGN4PSIzMCIgY3k9IjMwIiByPSIyIi8+PC9nPjwvZz48L3N2Zz4=')] opacity-20"></div>
      
      <div className="relative max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-32 text-center text-white">
        {/* Título Principal */}
        <h1 className="text-4xl md:text-6xl font-bold mb-6">
          <span className="block">Qualifique Leads</span>
          <span className="block text-blue-300">Automaticamente</span>
        </h1>

        {/* Subtítulo */}
        <p className="text-xl md:text-2xl text-blue-100 mb-12 max-w-2xl mx-auto">
          Sistema que automatiza a qualificação de leads via <strong>WhatsApp</strong> usando IA, 
          entregando leads prontos para fechamento.
        </p>

        {/* CTAs */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
          <Link
            href="/signup"
            className="inline-flex items-center px-8 py-4 bg-white hover:bg-gray-100 text-blue-900 font-semibold rounded-lg transition-colors shadow-lg hover:shadow-xl group"
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
      </div>
    </div>
  )
}
