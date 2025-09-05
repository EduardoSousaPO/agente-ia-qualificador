'use client'

export default function SimpleHomePage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Agente Qualificador
        </h1>
        <p className="text-xl text-gray-600">
          Teste simples - sem providers
        </p>
        <div className="mt-8">
          <button 
            onClick={() => alert('Funcionando!')}
            className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Testar Clique
          </button>
        </div>
      </div>
    </div>
  )
}
