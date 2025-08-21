// Tipos principais da aplicação

export interface User {
  id: string;
  email: string;
  name?: string;
  role: 'admin' | 'closer' | 'operator';
  tenant: {
    id: string;
    name: string;
    domain?: string;
  };
  created_at: string;
}

export interface Lead {
  id: string;
  tenant_id: string;
  name: string;
  email?: string;
  phone: string;
  origem: string;
  inserido_manual: boolean;
  tags: string[];
  status: 'novo' | 'em_conversa' | 'qualificado' | 'desqualificado';
  score: number;
  created_at: string;
  updated_at: string;
  sessions?: Session[];
  qualifications?: Qualification[];
  meetings?: Meeting[];
}

export interface Session {
  id: string;
  lead_id: string;
  tenant_id: string;
  status: 'ativa' | 'pausada' | 'finalizada';
  current_step?: string;
  context: Record<string, any>;
  human_takeover?: boolean;
  created_at: string;
  updated_at: string;
  messages?: Message[];
  lead?: Lead;
}

export interface Message {
  id: string;
  session_id: string;
  tenant_id: string;
  direction?: 'inbound' | 'outbound';
  content: string;
  message_type?: string;
  twilio_sid?: string;
  is_ai: boolean;
  created_at: string;
}

export interface Qualification {
  id: string;
  lead_id: string;
  patrimonio_faixa?: string;
  objetivo?: string;
  urgencia?: string;
  interesse_especialista?: boolean;
  score_final?: number;
  observacoes?: string;
  created_at: string;
}

export interface Meeting {
  id: string;
  lead_id: string;
  closer_id?: string;
  horario_sugestao_1?: string;
  horario_sugestao_2?: string;
  status: 'pendente' | 'confirmado' | 'realizado';
  created_at: string;
  closer?: {
    name?: string;
    email: string;
  };
}

export interface TenantSettings {
  ai_config: {
    model: string;
    temperature: number;
    max_tokens: number;
    qualification_threshold: number;
    prompts?: Record<string, string>;
  };
  whatsapp_config: {
    welcome_template: string;
    reengagement_24h: boolean;
    reengagement_72h: boolean;
    business_hours: {
      enabled: boolean;
      start: string;
      end: string;
      timezone: string;
    };
  };
  notification_config: {
    qualified_lead_slack: boolean;
    qualified_lead_email: boolean;
    daily_summary: boolean;
  };
  scoring_config: {
    patrimonio_weights: Record<string, number>;
    objetivo_weight: number;
    urgencia_weights: Record<string, number>;
    interesse_weight: number;
    engajamento_weight: number;
  };
}

export interface Tenant {
  id: string;
  name: string;
  domain?: string;
  settings: TenantSettings;
  created_at: string;
}

export interface ApiResponse<T> {
  data?: T;
  error?: string;
  message?: string;
  success?: boolean;
}

export interface PaginatedResponse<T> {
  data: T[];
  count: number;
  page: number;
  limit: number;
  total_pages: number;
}

export interface LeadFilters {
  status?: string;
  origem?: string;
  inserido_manual?: boolean;
  search?: string;
  page?: number;
  limit?: number;
}

export interface DashboardStats {
  total_leads: number;
  leads_hoje: number;
  leads_qualificados: number;
  taxa_qualificacao: number;
  score_medio: number;
  conversas_ativas: number;
  reunioes_agendadas: number;
  leads_por_origem: Record<string, number>;
  leads_por_status: Record<string, number>;
  score_distribution: { range: string; count: number }[];
  timeline_leads: { date: string; count: number }[];
}

export interface ChatMessage {
  id: string;
  direction: 'inbound' | 'outbound';
  content: string;
  timestamp: string;
  status?: 'sent' | 'delivered' | 'read' | 'failed';
}

export interface UploadResult {
  success: boolean;
  created: number;
  errors: number;
  leads_created: Lead[];
  leads_errors: {
    row: number;
    error: string;
    data: Record<string, string>;
  }[];
}

export interface IntegrationStatus {
  openai: {
    configured: boolean;
    model: string;
  };
  twilio: {
    configured: boolean;
    whatsapp_number: string;
  };
  supabase: {
    configured: boolean;
    url: string;
  };
  n8n: {
    configured: boolean;
    webhook_url: string;
  };
}

// Tipos para formulários
export interface LeadFormData {
  name: string;
  email?: string;
  phone: string;
  origem?: string;
  tags?: string[];
}

export interface MessageFormData {
  message: string;
}

export interface SettingsFormData {
  settings: Partial<TenantSettings>;
}

// Tipos para hooks
export interface UseApiOptions {
  onSuccess?: (data: any) => void;
  onError?: (error: string) => void;
}

export interface UseLeadsOptions extends UseApiOptions {
  filters?: LeadFilters;
  enabled?: boolean;
}

// Tipos de eventos
export interface AuditEvent {
  id: string;
  tenant_id: string;
  user_id?: string;
  action: string;
  resource_type: string;
  resource_id?: string;
  details: Record<string, any>;
  created_at: string;
}

// Tipos para filtros de conversas
export interface ConversationFilters {
  status?: string;
  human_takeover?: boolean;
  current_step?: string;
  search?: string;
  created_after?: string;
  created_before?: string;
  page?: number;
  limit?: number;
}
