'use client'

import { useState, useEffect, Suspense } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { signupSchema, SignupFormData } from '@/lib/validations/auth'
import { createClient } from '@/lib/supabase'
import { api } from '@/lib/api'
import toast from 'react-hot-toast'
import Link from 'next/link'
import { 
  EyeIcon, 
  EyeSlashIcon, 
  UserPlusIcon,
  EnvelopeIcon,
  BuildingOfficeIcon,
  KeyIcon 
} from '@heroicons/react/24/outline'

interface InviteInfo {
  id: string
  tenant_name: string
  tenant_slug: string
  role: string
  email: string
}

function SignupPageContent() {
  const [loading, setLoading] = useState(false)
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  const [inviteInfo, setInviteInfo] = useState<InviteInfo | null>(null)
  const [checkingInvite, setCheckingInvite] = useState(false)
  const [validatingCompany, setValidatingCompany] = useState(false)
  const [companyValid, setCompanyValid] = useState<boolean | null>(null)
  
  const router = useRouter()
  const searchParams = useSearchParams()
  const supabase = createClient()
  
  const inviteId = searchParams.get('invite')
  const emailParam = searchParams.get('email')

  const {
    register,
    handleSubmit,
    watch,
    setValue,
    formState: { errors }
  } = useForm<SignupFormData>({
    resolver: zodResolver(signupSchema),
    defaultValues: {
      email: emailParam || '',
      password: '',
      confirmPassword: '',
      name: '',
      companyCode: '',
      companyName: '',
      acceptTerms: false
    }
  })

  const watchedEmail = watch('email')
  const watchedCompanyCode = watch('companyCode')

  // Validar código da empresa quando digitado
  useEffect(() => {
    const validateCompanyCode = async () => {
      if (!watchedCompanyCode || watchedCompanyCode.length < 3) {
        setCompanyValid(null)
        return
      }

      try {
        setValidatingCompany(true)
        const response = await fetch(`http://localhost:5000/api/company-code/${watchedCompanyCode}/validate`)
        const result = await response.json()
        
        if (result.valid) {
          setCompanyValid(true)
          if (result.company_name) {
            setValue('companyName', result.company_name)
          }
        } else {
          setCompanyValid(false)
        }
      } catch (error) {
        console.error('Erro ao validar código da empresa:', error)
        setCompanyValid(false)
      } finally {
        setValidatingCompany(false)
      }
    }

    // Debounce da validação
    const timeoutId = setTimeout(validateCompanyCode, 500)
    return () => clearTimeout(timeoutId)
  }, [watchedCompanyCode, setValue])

  // Verificar convite quando email for digitado
  useEffect(() => {
    const checkInvite = async () => {
      if (!watchedEmail || watchedEmail.length < 5) {
        setInviteInfo(null)
        return
      }

      try {
        setCheckingInvite(true)
        const response = await api.checkInviteByEmail(watchedEmail)
        
        if (response.success && response.invite) {
          setInviteInfo(response.invite)
        } else {
          setInviteInfo(null)
        }
      } catch (error) {
        // Silently fail - no invite found
        setInviteInfo(null)
      } finally {
        setCheckingInvite(false)
      }
    }

    // Debounce da verificação
    const timeoutId = setTimeout(checkInvite, 500)
    return () => clearTimeout(timeoutId)
  }, [watchedEmail])

  // Verificar convite específico via URL
  useEffect(() => {
    if (inviteId && emailParam) {
      checkSpecificInvite()
    }
  }, [inviteId, emailParam])

  const checkSpecificInvite = async () => {
    try {
      setCheckingInvite(true)
      const response = await api.getInviteById(inviteId!)
      
      if (response.success && response.invite.email.toLowerCase() === emailParam!.toLowerCase()) {
        setInviteInfo(response.invite)
        setValue('email', emailParam!)
      } else {
        toast.error('Convite não encontrado ou email não corresponde')
        router.push('/signup')
      }
    } catch (error) {
      toast.error('Erro ao verificar convite')
      router.push('/signup')
    } finally {
      setCheckingInvite(false)
    }
  }

  const onSubmit = async (data: SignupFormData) => {
    setLoading(true)

    try {
      // 1. Criar conta no Supabase Auth
      const { data: authData, error: authError } = await supabase.auth.signUp({
        email: data.email,
        password: data.password,
        options: {
          data: {
            full_name: data.name,
            invite_id: inviteInfo?.id
          }
        }
      })

      if (authError) {
        throw new Error(authError.message)
      }

      if (!authData.user) {
        throw new Error('Erro ao criar usuário')
      }

      // 2. Se tiver convite, aceitar automaticamente (fluxo antigo)
      if (inviteInfo) {
        try {
          await api.acceptInvite(inviteInfo.id)
          toast.success(`Conta criada! Você foi adicionado à ${inviteInfo.tenant_name}`)
          
          if (authData.user && !authData.user.email_confirmed_at) {
            router.push('/login?message=check-email')
          } else {
            router.push(`/app/${inviteInfo.tenant_slug}/dashboard`)
          }
          return
        } catch (inviteError) {
          console.warn('Erro ao aceitar convite automaticamente:', inviteError)
          // Continua mesmo se falhar - o trigger do banco pode resolver
        }
      }

      // 3. Novo fluxo: Criar solicitação de acesso à empresa
      if (data.companyCode && data.companyName) {
        try {
          const joinRequestResponse = await fetch('http://localhost:5000/api/join-requests', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              user_id: authData.user.id,
              company_code: data.companyCode,
              company_name: data.companyName
            })
          })

          const joinRequestResult = await joinRequestResponse.json()

          if (joinRequestResponse.ok) {
            toast.success('Conta criada! Sua solicitação foi enviada para aprovação.')
            router.push('/login?message=pending-approval')
            return
          } else {
            throw new Error(joinRequestResult.error || 'Erro ao enviar solicitação')
          }
        } catch (joinRequestError: any) {
          console.error('Erro ao criar join request:', joinRequestError)
          toast.error(joinRequestError.message || 'Erro ao enviar solicitação de acesso')
          return
        }
      }

      // 4. Fallback: usuário sem convite nem empresa (não deveria acontecer com nova validação)
      if (authData.user && !authData.user.email_confirmed_at) {
        toast.success(
          'Conta criada! Verifique seu email para confirmar o cadastro.',
          { duration: 6000 }
        )
        router.push('/login?message=check-email')
      } else {
        toast.success('Conta criada com sucesso!')
        router.push('/dashboard')
      }

    } catch (error: any) {
      console.error('Erro no signup:', error)
      
      // Tratar erros específicos
      if (error.message?.includes('already registered')) {
        toast.error('Este email já está cadastrado. Tente fazer login.')
        router.push(`/login?email=${encodeURIComponent(data.email)}`)
      } else if (error.message?.includes('Invalid email')) {
        toast.error('Email inválido. Verifique e tente novamente.')
      } else {
        toast.error(error.message || 'Erro ao criar conta')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="max-w-md w-full space-y-8 p-8">
        {/* Header */}
        <div className="text-center">
          <div className="mx-auto h-12 w-12 flex items-center justify-center rounded-full bg-blue-100">
            <UserPlusIcon className="h-6 w-6 text-blue-600" />
          </div>
          <h2 className="mt-6 text-3xl font-bold text-gray-900">
            Criar Conta
          </h2>
          <p className="mt-2 text-sm text-gray-600">
            {inviteInfo 
              ? `Você foi convidado para ${inviteInfo.tenant_name}`
              : 'Faça seu cadastro para acessar o sistema'
            }
          </p>
        </div>

        {/* Invite Info */}
        {inviteInfo && (
          <div className="bg-green-50 border border-green-200 rounded-lg p-4">
            <div className="flex items-center">
              <BuildingOfficeIcon className="h-5 w-5 text-green-600 mr-2" />
              <div>
                <h3 className="text-sm font-medium text-green-800">
                  Convite para {inviteInfo.tenant_name}
                </h3>
                <p className="text-sm text-green-700">
                  Função: {inviteInfo.role === 'admin' ? 'Administrador' : 'Membro'}
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Signup Form */}
        <form className="mt-8 space-y-6" onSubmit={handleSubmit(onSubmit)}>
          <div className="space-y-4">
            {/* Nome */}
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-gray-700">
                Nome completo *
              </label>
              <input
                {...register('name')}
                type="text"
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                placeholder="Digite seu nome completo"
              />
              {errors.name && (
                <p className="mt-1 text-sm text-red-600">{errors.name.message}</p>
              )}
            </div>

            {/* Email */}
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                Email *
              </label>
              <div className="mt-1 relative">
                <input
                  {...register('email')}
                  type="email"
                  className="block w-full px-3 py-2 pr-10 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  placeholder="Digite seu email"
                />
                {checkingInvite && (
                  <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
                  </div>
                )}
              </div>
              {errors.email && (
                <p className="mt-1 text-sm text-red-600">{errors.email.message}</p>
              )}
            </div>

            {/* Campos da Empresa - só aparecem se não tiver convite */}
            {!inviteInfo && (
              <>
                {/* Código da Empresa */}
                <div>
                  <label htmlFor="companyCode" className="block text-sm font-medium text-gray-700">
                    Código da empresa *
                  </label>
                  <div className="mt-1 relative">
                    <input
                      {...register('companyCode')}
                      type="text"
                      className={`block w-full px-3 py-2 pr-10 border rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 ${
                        companyValid === true 
                          ? 'border-green-300 bg-green-50' 
                          : companyValid === false 
                          ? 'border-red-300 bg-red-50' 
                          : 'border-gray-300'
                      }`}
                      placeholder="Ex: DEMO2024"
                    />
                    <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
                      {validatingCompany && (
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
                      )}
                      {!validatingCompany && companyValid === true && (
                        <div className="h-4 w-4 text-green-500">✓</div>
                      )}
                      {!validatingCompany && companyValid === false && (
                        <div className="h-4 w-4 text-red-500">✗</div>
                      )}
                    </div>
                  </div>
                  {errors.companyCode && (
                    <p className="mt-1 text-sm text-red-600">{errors.companyCode.message}</p>
                  )}
                  {companyValid === false && !errors.companyCode && (
                    <p className="mt-1 text-sm text-red-600">Código da empresa não encontrado</p>
                  )}
                  {companyValid === true && (
                    <p className="mt-1 text-sm text-green-600">Empresa encontrada!</p>
                  )}
                </div>

                {/* Nome da Empresa */}
                <div>
                  <label htmlFor="companyName" className="block text-sm font-medium text-gray-700">
                    Nome da empresa *
                  </label>
                  <input
                    {...register('companyName')}
                    type="text"
                    className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    placeholder="Ex: Escritório de Investimentos Demo"
                  />
                  {errors.companyName && (
                    <p className="mt-1 text-sm text-red-600">{errors.companyName.message}</p>
                  )}
                </div>
              </>
            )}

            {/* Senha */}
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                Senha *
              </label>
              <div className="mt-1 relative">
                <input
                  {...register('password')}
                  type={showPassword ? 'text' : 'password'}
                  className="block w-full px-3 py-2 pr-10 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  placeholder="Digite sua senha"
                />
                <button
                  type="button"
                  className="absolute inset-y-0 right-0 pr-3 flex items-center"
                  onClick={() => setShowPassword(!showPassword)}
                >
                  {showPassword ? (
                    <EyeSlashIcon className="h-5 w-5 text-gray-400" />
                  ) : (
                    <EyeIcon className="h-5 w-5 text-gray-400" />
                  )}
                </button>
              </div>
              {errors.password && (
                <p className="mt-1 text-sm text-red-600">{errors.password.message}</p>
              )}
            </div>

            {/* Confirmar Senha */}
            <div>
              <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700">
                Confirmar senha *
              </label>
              <div className="mt-1 relative">
                <input
                  {...register('confirmPassword')}
                  type={showConfirmPassword ? 'text' : 'password'}
                  className="block w-full px-3 py-2 pr-10 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  placeholder="Confirme sua senha"
                />
                <button
                  type="button"
                  className="absolute inset-y-0 right-0 pr-3 flex items-center"
                  onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                >
                  {showConfirmPassword ? (
                    <EyeSlashIcon className="h-5 w-5 text-gray-400" />
                  ) : (
                    <EyeIcon className="h-5 w-5 text-gray-400" />
                  )}
                </button>
              </div>
              {errors.confirmPassword && (
                <p className="mt-1 text-sm text-red-600">{errors.confirmPassword.message}</p>
              )}
            </div>

            {/* Termos */}
            <div className="flex items-start">
              <input
                {...register('acceptTerms')}
                type="checkbox"
                className="mt-1 h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <label htmlFor="acceptTerms" className="ml-2 block text-sm text-gray-700">
                Eu aceito os{' '}
                <Link href="/terms" className="text-blue-600 hover:text-blue-500">
                  termos de uso
                </Link>{' '}
                e{' '}
                <Link href="/privacy" className="text-blue-600 hover:text-blue-500">
                  política de privacidade
                </Link>
              </label>
            </div>
            {errors.acceptTerms && (
              <p className="mt-1 text-sm text-red-600">{errors.acceptTerms.message}</p>
            )}
          </div>

          {/* Submit Button */}
          <div>
            <button
              type="submit"
              disabled={loading}
              className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <div className="flex items-center">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Criando conta...
                </div>
              ) : (
                'Criar conta'
              )}
            </button>
          </div>
        </form>

        {/* Footer */}
        <div className="text-center">
          <p className="text-sm text-gray-600">
            Já tem uma conta?{' '}
            <Link 
              href="/login" 
              className="font-medium text-blue-600 hover:text-blue-500"
            >
              Fazer login
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}

export default function SignupPage() {
  return (
    <Suspense fallback={<div>Carregando...</div>}>
      <SignupPageContent />
    </Suspense>
  )
}
