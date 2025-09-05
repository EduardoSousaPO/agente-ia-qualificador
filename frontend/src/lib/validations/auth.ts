import { z } from 'zod'

// Schema para login
export const loginSchema = z.object({
  email: z
    .string()
    .min(1, 'Email é obrigatório')
    .email('Email inválido'),
  password: z
    .string()
    .min(6, 'Senha deve ter pelo menos 6 caracteres')
})

export type LoginFormData = z.infer<typeof loginSchema>

// Schema para registro
export const signupSchema = z.object({
  email: z
    .string()
    .min(1, 'Email é obrigatório')
    .email('Email inválido'),
  password: z
    .string()
    .min(8, 'Senha deve ter pelo menos 8 caracteres')
    .regex(
      /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/,
      'Senha deve conter pelo menos: 1 letra minúscula, 1 maiúscula e 1 número'
    ),
  confirmPassword: z
    .string()
    .min(1, 'Confirmação de senha é obrigatória'),
  name: z
    .string()
    .min(2, 'Nome deve ter pelo menos 2 caracteres')
    .max(50, 'Nome deve ter no máximo 50 caracteres'),
  companyCode: z
    .string()
    .min(3, 'Código da empresa deve ter pelo menos 3 caracteres')
    .max(20, 'Código da empresa deve ter no máximo 20 caracteres')
    .optional(),
  companyName: z
    .string()
    .min(2, 'Nome da empresa deve ter pelo menos 2 caracteres')
    .max(100, 'Nome da empresa deve ter no máximo 100 caracteres')
    .optional(),
  acceptTerms: z
    .boolean()
    .refine(val => val === true, 'Você deve aceitar os termos de uso')
}).refine(data => data.password === data.confirmPassword, {
  message: 'Senhas não conferem',
  path: ['confirmPassword']
}).refine(data => {
  // Se não tem convite, campos da empresa são obrigatórios
  const hasCompanyFields = data.companyCode && data.companyName;
  return hasCompanyFields;
}, {
  message: 'Código e nome da empresa são obrigatórios para registro corporativo',
  path: ['companyCode']
})

export type SignupFormData = z.infer<typeof signupSchema>

// Schema para convite
export const inviteAcceptSchema = z.object({
  inviteId: z.string().uuid('ID do convite inválido'),
  email: z.string().email('Email inválido'),
  password: z
    .string()
    .min(8, 'Senha deve ter pelo menos 8 caracteres')
    .regex(
      /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/,
      'Senha deve conter pelo menos: 1 letra minúscula, 1 maiúscula e 1 número'
    ),
  confirmPassword: z.string(),
  name: z
    .string()
    .min(2, 'Nome deve ter pelo menos 2 caracteres')
    .max(50, 'Nome deve ter no máximo 50 caracteres')
}).refine(data => data.password === data.confirmPassword, {
  message: 'Senhas não conferem',
  path: ['confirmPassword']
})

export type InviteAcceptFormData = z.infer<typeof inviteAcceptSchema>

