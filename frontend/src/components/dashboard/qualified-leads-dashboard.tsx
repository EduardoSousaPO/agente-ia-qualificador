'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

interface Lead {
  id: string;
  name: string;
  phone: string;
  email?: string;
  origem: string;
  status: string;
  score: number;
  created_at: string;
  qualification_completed_at?: string;
}

interface QualificationStats {
  total_leads: number;
  qualified_leads: number;
  qualification_rate: number;
  avg_score: number;
  today_qualified: number;
}

export default function QualifiedLeadsDashboard() {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [stats, setStats] = useState<QualificationStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    try {
      setLoading(true);
      
      // Buscar leads
      const leadsResponse = await fetch('/api/leads');
      if (!leadsResponse.ok) throw new Error('Erro ao carregar leads');
      const leadsData = await leadsResponse.json();
      
      // Filtrar apenas leads qualificados (score >= 70)
      const qualifiedLeads = leadsData.data?.filter((lead: Lead) => lead.score >= 70) || [];
      setLeads(qualifiedLeads);
      
      // Calcular estatísticas
      const totalLeads = leadsData.data?.length || 0;
      const qualifiedCount = qualifiedLeads.length;
      const qualificationRate = totalLeads > 0 ? (qualifiedCount / totalLeads) * 100 : 0;
      const avgScore = qualifiedLeads.length > 0 
        ? qualifiedLeads.reduce((sum: number, lead: Lead) => sum + lead.score, 0) / qualifiedLeads.length 
        : 0;
      
      // Leads qualificados hoje
      const today = new Date().toISOString().split('T')[0];
      const todayQualified = qualifiedLeads.filter((lead: Lead) => 
        lead.qualification_completed_at?.startsWith(today) || 
        lead.created_at.startsWith(today)
      ).length;
      
      setStats({
        total_leads: totalLeads,
        qualified_leads: qualifiedCount,
        qualification_rate: qualificationRate,
        avg_score: avgScore,
        today_qualified: todayQualified
      });
      
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro desconhecido');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    
    // Atualizar a cada 30 segundos
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, []);

  const getScoreColor = (score: number) => {
    if (score >= 90) return 'text-green-600 bg-green-100';
    if (score >= 80) return 'text-blue-600 bg-blue-100';
    if (score >= 70) return 'text-yellow-600 bg-yellow-100';
    return 'text-gray-600 bg-gray-100';
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString('pt-BR');
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <span className="ml-2">Carregando dashboard...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 bg-red-100 border border-red-400 text-red-700 rounded">
        <h3 className="font-bold">Erro ao carregar dados</h3>
        <p>{error}</p>
        <button 
          onClick={fetchData}
          className="mt-2 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
        >
          Tentar novamente
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">🎯 Leads Qualificados</h1>
        <button 
          onClick={fetchData}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 flex items-center"
        >
          🔄 Atualizar
        </button>
      </div>

      {/* Estatísticas */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">Total de Leads</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-gray-900">{stats.total_leads}</div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">Qualificados</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-green-600">{stats.qualified_leads}</div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">Taxa de Qualificação</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-blue-600">{stats.qualification_rate.toFixed(1)}%</div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">Score Médio</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-purple-600">{stats.avg_score.toFixed(0)}</div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">Hoje</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-orange-600">{stats.today_qualified}</div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Lista de Leads Qualificados */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            🏆 Leads Qualificados (Score ≥ 70)
            <span className="ml-2 text-sm font-normal text-gray-500">
              ({leads.length} leads)
            </span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          {leads.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <div className="text-4xl mb-2">🎯</div>
              <p>Nenhum lead qualificado ainda</p>
              <p className="text-sm">Leads com score ≥ 70 aparecerão aqui</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b">
                    <th className="text-left py-2 px-4">Nome</th>
                    <th className="text-left py-2 px-4">Contato</th>
                    <th className="text-left py-2 px-4">Origem</th>
                    <th className="text-left py-2 px-4">Score</th>
                    <th className="text-left py-2 px-4">Qualificado em</th>
                    <th className="text-left py-2 px-4">Ações</th>
                  </tr>
                </thead>
                <tbody>
                  {leads.map((lead) => (
                    <tr key={lead.id} className="border-b hover:bg-gray-50">
                      <td className="py-3 px-4">
                        <div>
                          <div className="font-medium text-gray-900">{lead.name}</div>
                          <div className="text-sm text-gray-500">ID: {lead.id.slice(0, 8)}...</div>
                        </div>
                      </td>
                      <td className="py-3 px-4">
                        <div>
                          <div className="text-sm">{lead.phone}</div>
                          {lead.email && (
                            <div className="text-sm text-gray-500">{lead.email}</div>
                          )}
                        </div>
                      </td>
                      <td className="py-3 px-4">
                        <span className="px-2 py-1 text-xs rounded-full bg-blue-100 text-blue-800">
                          {lead.origem}
                        </span>
                      </td>
                      <td className="py-3 px-4">
                        <span className={`px-2 py-1 text-sm font-bold rounded-full ${getScoreColor(lead.score)}`}>
                          {lead.score}/100
                        </span>
                      </td>
                      <td className="py-3 px-4 text-sm text-gray-600">
                        {formatDate(lead.qualification_completed_at || lead.created_at)}
                      </td>
                      <td className="py-3 px-4">
                        <div className="flex space-x-2">
                          <button className="text-blue-600 hover:text-blue-800 text-sm">
                            📞 Ligar
                          </button>
                          <button className="text-green-600 hover:text-green-800 text-sm">
                            💬 WhatsApp
                          </button>
                          <button className="text-purple-600 hover:text-purple-800 text-sm">
                            📧 Email
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Rodapé com informações */}
      <div className="text-center text-sm text-gray-500">
        <p>🤖 Dashboard atualizado automaticamente a cada 30 segundos</p>
        <p>🎯 Leads com score ≥ 70 são considerados qualificados</p>
      </div>
    </div>
  );
}




