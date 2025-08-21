import axios, { AxiosInstance, AxiosResponse } from 'axios'
import { createClient } from './supabase'
import { 
  Lead, 
  Session, 
  Message,
  User, 
  TenantSettings, 
  PaginatedResponse, 
  LeadFilters,
  ConversationFilters,
  UploadResult,
  DashboardStats,
  IntegrationStatus,
  ApiResponse
} from '@/types'

class ApiClient {
  private client: AxiosInstance
  private supabase = createClient()

  constructor() {
    this.client = axios.create({
      baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api',
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    // Interceptor para adicionar token de autenticação
    this.client.interceptors.request.use(
      async (config) => {
        const { data: { session } } = await this.supabase.auth.getSession()
        
        if (session?.access_token) {
          config.headers.Authorization = `Bearer ${session.access_token}`
        }
        
        return config
      },
      (error) => {
        return Promise.reject(error)
      }
    )

    // Interceptor para tratamento de erros
    this.client.interceptors.response.use(
      (response) => response,
      async (error) => {
        if (error.response?.status === 401) {
          // Token expirado, tentar refresh
          const { error: refreshError } = await this.supabase.auth.refreshSession()
          
          if (refreshError) {
            // Redirect para login se não conseguir refresh
            window.location.href = '/login'
          }
        }
        
        return Promise.reject(error)
      }
    )
  }

  // Health Check
  async healthCheck(): Promise<any> {
    const response = await this.client.get('/health')
    return response.data
  }

  async detailedHealthCheck(): Promise<any> {
    const response = await this.client.get('/health/detailed')
    return response.data
  }

  // Auth
  async getCurrentUser(): Promise<User> {
    const response = await this.client.get('/auth/me')
    return response.data
  }

  // Leads
  async getLeads(filters: LeadFilters = {}): Promise<PaginatedResponse<Lead>> {
    const params = new URLSearchParams()
    
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        params.append(key, String(value))
      }
    })
    
    const response = await this.client.get(`/leads?${params.toString()}`)
    return response.data
  }

  async getLead(id: string): Promise<Lead> {
    const response = await this.client.get(`/leads/${id}`)
    return response.data
  }

  async createLead(leadData: {
    name: string
    email?: string
    phone: string
    origem?: string
    tags?: string[]
  }): Promise<Lead> {
    const response = await this.client.post('/leads', leadData)
    return response.data
  }

  async updateLead(id: string, updateData: Partial<Lead>): Promise<Lead> {
    const response = await this.client.put(`/leads/${id}`, updateData)
    return response.data
  }

  async uploadLeadsCSV(file: File): Promise<UploadResult> {
    const formData = new FormData()
    formData.append('file', file)
    
    const response = await this.client.post('/leads/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    
    return response.data
  }

  async qualifyLead(id: string, qualificationData: {
    patrimonio_faixa?: string
    objetivo?: string
    urgencia?: string
    interesse_especialista?: boolean
    score_final?: number
    observacoes?: string
  }): Promise<ApiResponse<any>> {
    const response = await this.client.post(`/leads/${id}/qualify`, qualificationData)
    return response.data
  }

  // Chat & Sessions
  async getConversations(filters: ConversationFilters = {}): Promise<PaginatedResponse<Session>> {
    const params = new URLSearchParams()
    
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        params.append(key, String(value))
      }
    })
    
    const response = await this.client.get(`/chat/sessions?${params.toString()}`)
    return response.data
  }

  async getSession(sessionId: string): Promise<Session> {
    const response = await this.client.get(`/chat/sessions/${sessionId}`)
    return response.data
  }

  async getMessages(sessionId: string): Promise<PaginatedResponse<Message>> {
    const response = await this.client.get(`/chat/sessions/${sessionId}/messages`)
    return response.data
  }

  async getChatHistory(sessionId: string): Promise<{
    session: Session
    lead: Lead
    messages: any[]
  }> {
    const response = await this.client.get(`/chat/${sessionId}`)
    return response.data
  }

  async sendMessage(data: {
    session_id: string
    message: string
    is_ai: boolean
  }): Promise<ApiResponse<any>> {
    const response = await this.client.post(`/chat/send-message`, data)
    return response.data
  }

  async toggleHumanTakeover(sessionId: string, humanTakeover: boolean): Promise<ApiResponse<any>> {
    const response = await this.client.post(`/chat/sessions/${sessionId}/takeover`, { 
      human_takeover: humanTakeover 
    })
    return response.data
  }

  async manualQualification(leadId: string): Promise<ApiResponse<any>> {
    const response = await this.client.post(`/leads/${leadId}/manual-qualify`)
    return response.data
  }

  async takeoverSession(sessionId: string): Promise<ApiResponse<any>> {
    const response = await this.client.post(`/chat/${sessionId}/takeover`)
    return response.data
  }

  async resumeAISession(sessionId: string): Promise<ApiResponse<any>> {
    const response = await this.client.post(`/chat/${sessionId}/resume`)
    return response.data
  }

  async closeSession(sessionId: string, reason?: string): Promise<ApiResponse<any>> {
    const response = await this.client.post(`/chat/${sessionId}/close`, { reason })
    return response.data
  }

  // Settings
  async getTenantSettings(): Promise<TenantSettings> {
    const response = await this.client.get('/settings')
    return response.data
  }

  async getSettings(): Promise<TenantSettings> {
    return this.getTenantSettings()
  }

  async updateTenantSettings(settings: Partial<TenantSettings>): Promise<ApiResponse<any>> {
    const response = await this.client.put('/settings', { settings })
    return response.data
  }

  async getAIPrompts(): Promise<{
    prompts: Record<string, string>
    is_customized: boolean
  }> {
    const response = await this.client.get('/settings/ai-prompts')
    return response.data
  }

  async updateAIPrompts(prompts: Record<string, string>): Promise<ApiResponse<any>> {
    const response = await this.client.put('/settings/ai-prompts', { prompts })
    return response.data
  }

  async getTenantUsers(): Promise<{
    users: User[]
    total: number
  }> {
    const response = await this.client.get('/settings/users')
    return response.data
  }

  async getIntegrationsStatus(): Promise<{
    integrations: IntegrationStatus
    all_configured: boolean
  }> {
    const response = await this.client.get('/settings/integrations')
    return response.data
  }

  // Dashboard Stats (mock - implementar no backend se necessário)
  async getDashboardStats(): Promise<DashboardStats> {
    // Por enquanto, vamos simular com dados dos leads
    const leads = await this.getLeads({ limit: 1000 })
    
    const stats: DashboardStats = {
      total_leads: leads.count,
      leads_hoje: 0, // Implementar lógica
      leads_qualificados: leads.data.filter(l => l.status === 'qualificado').length,
      taxa_qualificacao: 0, // Calcular
      score_medio: leads.data.reduce((acc, l) => acc + l.score, 0) / leads.data.length || 0,
      conversas_ativas: leads.data.filter(l => l.status === 'em_conversa').length,
      reunioes_agendadas: 0, // Implementar
      leads_por_origem: {},
      leads_por_status: {},
      score_distribution: [],
      timeline_leads: []
    }

    // Calcular estatísticas
    leads.data.forEach(lead => {
      // Por origem
      stats.leads_por_origem[lead.origem] = (stats.leads_por_origem[lead.origem] || 0) + 1
      
      // Por status
      stats.leads_por_status[lead.status] = (stats.leads_por_status[lead.status] || 0) + 1
    })

    return stats
  }

  // Webhook intake (para testes)
  async intakeLead(leadData: {
    name: string
    phone: string
    email?: string
    tenant_id: string
    origem?: string
    tags?: string[]
  }): Promise<ApiResponse<any>> {
    const response = await this.client.post('/webhooks/intake/lead', leadData)
    return response.data
  }
}

// Instância singleton do cliente da API
export const apiClient = new ApiClient()

// Hooks para facilitar uso com React Query/SWR
export const api = {
  // Health
  health: () => apiClient.healthCheck(),
  healthDetailed: () => apiClient.detailedHealthCheck(),
  
  // Auth
  me: () => apiClient.getCurrentUser(),
  
  // Leads
  leads: (filters?: LeadFilters) => apiClient.getLeads(filters),
  lead: (id: string) => apiClient.getLead(id),
  createLead: (data: any) => apiClient.createLead(data),
  updateLead: (id: string, data: any) => apiClient.updateLead(id, data),
  uploadCSV: (file: File) => apiClient.uploadLeadsCSV(file),
  qualifyLead: (id: string, data: any) => apiClient.qualifyLead(id, data),
  
  // Conversations & Chat
  conversations: (filters?: ConversationFilters) => apiClient.getConversations(filters),
  getSession: (sessionId: string) => apiClient.getSession(sessionId),
  getMessages: (sessionId: string) => apiClient.getMessages(sessionId),
  chat: (sessionId: string) => apiClient.getChatHistory(sessionId),
  sendMessage: (data: { session_id: string; message: string; is_ai: boolean }) => apiClient.sendMessage(data),
  toggleHumanTakeover: (sessionId: string, humanTakeover: boolean) => apiClient.toggleHumanTakeover(sessionId, humanTakeover),
  manualQualification: (leadId: string) => apiClient.manualQualification(leadId),
  takeover: (sessionId: string) => apiClient.takeoverSession(sessionId),
  resume: (sessionId: string) => apiClient.resumeAISession(sessionId),
  closeSession: (sessionId: string, reason?: string) => apiClient.closeSession(sessionId, reason),
  
  // Settings
  settings: () => apiClient.getTenantSettings(),
  updateSettings: (settings: any) => apiClient.updateTenantSettings(settings),
  prompts: () => apiClient.getAIPrompts(),
  updatePrompts: (prompts: any) => apiClient.updateAIPrompts(prompts),
  users: () => apiClient.getTenantUsers(),
  integrations: () => apiClient.getIntegrationsStatus(),
  
  // Dashboard
  dashboard: () => apiClient.getDashboardStats(),
}
