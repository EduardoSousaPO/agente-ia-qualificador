'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';

interface SystemStats {
  total_leads: number;
  qualified_leads: number;
  qualification_rate: number;
  system_status: 'online' | 'offline';
  last_qualification: string | null;
}

export default function HomePage() {
  const [stats, setStats] = useState<SystemStats | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchStats = async () => {
    try {
      const response = await fetch('/api/health');
      if (response.ok) {
        const healthData = await response.json();
        
        // Buscar estatísticas de leads
        const leadsResponse = await fetch('/api/leads');
        if (leadsResponse.ok) {
          const leadsData = await leadsResponse.json();
          const leads = leadsData.data || [];
          const qualifiedLeads = leads.filter((lead: any) => lead.score >= 70);
          
          setStats({
            total_leads: leads.length,
            qualified_leads: qualifiedLeads.length,
            qualification_rate: leads.length > 0 ? (qualifiedLeads.length / leads.length) * 100 : 0,
            system_status: healthData.status === 'healthy' ? 'online' : 'offline',
            last_qualification: qualifiedLeads.length > 0 ? qualifiedLeads[0].created_at : null
          });
        }
      }
    } catch (error) {
      console.error('Erro ao buscar estatísticas:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStats();
    
    // Atualizar a cada 60 segundos
    const interval = setInterval(fetchStats, 60000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-16">
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            🤖 Agente Qualificador IA
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Sistema inteligente de qualificação de leads via WhatsApp
          </p>
          
          {/* Status do Sistema */}
          <div className="flex justify-center items-center mb-8">
            <div className={`flex items-center px-4 py-2 rounded-full ${
              stats?.system_status === 'online' 
                ? 'bg-green-100 text-green-800' 
                : 'bg-red-100 text-red-800'
            }`}>
              <div className={`w-2 h-2 rounded-full mr-2 ${
                stats?.system_status === 'online' ? 'bg-green-500' : 'bg-red-500'
              }`}></div>
              {loading ? 'Verificando...' : stats?.system_status === 'online' ? 'Sistema Online' : 'Sistema Offline'}
            </div>
          </div>
          
          <div className="flex justify-center space-x-4">
            <Link 
              href="/leads" 
              className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 transition-colors"
            >
              📋 Gerenciar Leads
            </Link>
            <Link 
              href="/conversations" 
              className="bg-green-600 text-white px-8 py-3 rounded-lg hover:bg-green-700 transition-colors"
            >
              💬 Conversas
            </Link>
            <Link 
              href="/dashboard" 
              className="bg-purple-600 text-white px-8 py-3 rounded-lg hover:bg-purple-700 transition-colors"
            >
              🎯 Dashboard
            </Link>
          </div>
        </div>

        {/* Estatísticas em Tempo Real */}
        <div className="bg-white rounded-lg shadow-md p-8 mb-16">
          <h2 className="text-2xl font-bold text-gray-900 mb-6 text-center">📊 Estatísticas em Tempo Real</h2>
          <div className="grid md:grid-cols-4 gap-6">
            <div className="text-center">
              <div className="text-3xl font-bold text-blue-600">
                {loading ? '...' : stats?.total_leads || 0}
              </div>
              <div className="text-gray-600">Total de Leads</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-green-600">
                {loading ? '...' : stats?.qualified_leads || 0}
              </div>
              <div className="text-gray-600">Qualificados</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-purple-600">
                {loading ? '...' : `${stats?.qualification_rate.toFixed(1) || 0}%`}
              </div>
              <div className="text-gray-600">Taxa de Qualificação</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-orange-600">70+</div>
              <div className="text-gray-600">Score para Qualificação</div>
            </div>
          </div>
          
          {stats?.last_qualification && (
            <div className="mt-4 text-center text-sm text-gray-500">
              Última qualificação: {new Date(stats.last_qualification).toLocaleString('pt-BR')}
            </div>
          )}
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-3 gap-8 mb-16">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="text-3xl mb-4">🎯</div>
            <h3 className="text-xl font-semibold mb-2">Qualificação Automática</h3>
            <p className="text-gray-600">
              IA conversa naturalmente com leads e aplica scoring automático baseado em critérios pré-definidos.
            </p>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="text-3xl mb-4">📱</div>
            <h3 className="text-xl font-semibold mb-2">WhatsApp Integrado</h3>
            <p className="text-gray-600">
              Conversas fluidas via WhatsApp Business API com respostas inteligentes e contextualizadas.
            </p>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="text-3xl mb-4">🔔</div>
            <h3 className="text-xl font-semibold mb-2">Notificações Inteligentes</h3>
            <p className="text-gray-600">
              Consultores são notificados automaticamente quando um lead é qualificado com score alto.
            </p>
          </div>
        </div>

        {/* Sistema em Funcionamento */}
        <div className="bg-white rounded-lg shadow-md p-8 text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">🚀 Sistema em Funcionamento</h2>
          <div className="grid md:grid-cols-4 gap-6">
            <div>
              <div className="text-3xl font-bold text-blue-600">24/7</div>
              <div className="text-gray-600">Disponibilidade</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-green-600">&lt;5min</div>
              <div className="text-gray-600">Tempo de Qualificação</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-purple-600">95%</div>
              <div className="text-gray-600">Precisão da IA</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-orange-600">
                {stats?.system_status === 'online' ? '✅' : '❌'}
              </div>
              <div className="text-gray-600">Status do Sistema</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}















