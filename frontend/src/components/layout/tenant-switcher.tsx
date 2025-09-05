'use client'

import { Fragment, useState, useEffect } from 'react'
import { Menu, Transition } from '@headlessui/react'
import { ChevronDownIcon, BuildingOfficeIcon, CheckIcon } from '@heroicons/react/24/outline'
import { useTenant } from '@/hooks/useTenant'
import { useAuth } from '@/components/providers'
import { api } from '@/lib/api'
import { cn } from '@/lib/utils'
import toast from 'react-hot-toast'

interface UserMembership {
  tenant: {
    id: string
    name: string
    slug: string
  }
  role: string
}

export function TenantSwitcher() {
  const { currentTenant, tenantSlug, switchTenant } = useTenant()
  const { user } = useAuth()
  const [userMemberships, setUserMemberships] = useState<UserMembership[]>([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    loadUserMemberships()
  }, [user])

  const loadUserMemberships = async () => {
    if (!user) return

    try {
      setLoading(true)
      const response = await api.userMemberships()
      
      if (response.success) {
        setUserMemberships(response.memberships || [])
      }
    } catch (error) {
      console.error('Erro ao carregar memberships:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleTenantSwitch = async (slug: string) => {
    if (slug === tenantSlug) return

    try {
      switchTenant(slug)
      toast.success('Tenant alterado com sucesso')
    } catch (error) {
      toast.error('Erro ao trocar de tenant')
    }
  }

  if (!currentTenant) {
    return (
      <div className="flex items-center px-3 py-2">
        <BuildingOfficeIcon className="h-5 w-5 text-gray-400 mr-2" />
        <span className="text-sm text-gray-500">Carregando...</span>
      </div>
    )
  }

  return (
    <Menu as="div" className="relative">
      <Menu.Button className="flex items-center w-full px-3 py-2 text-left text-sm font-medium text-gray-700 rounded-lg hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-primary-500">
        <BuildingOfficeIcon className="h-5 w-5 text-gray-400 mr-2 flex-shrink-0" />
        <div className="flex-1 min-w-0">
          <p className="truncate">{currentTenant.name}</p>
          <p className="text-xs text-gray-500 truncate">/{currentTenant.slug}</p>
        </div>
        <ChevronDownIcon className="h-4 w-4 text-gray-400 ml-2 flex-shrink-0" />
      </Menu.Button>

      <Transition
        as={Fragment}
        enter="transition ease-out duration-100"
        enterFrom="transform opacity-0 scale-95"
        enterTo="transform opacity-100 scale-100"
        leave="transition ease-in duration-75"
        leaveFrom="transform opacity-100 scale-100"
        leaveTo="transform opacity-0 scale-95"
      >
        <Menu.Items className="absolute left-0 z-10 mt-2 w-full origin-top-left rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
          <div className="py-1">
            {userMemberships.length > 0 ? (
              <>
                <div className="px-3 py-2 text-xs font-semibold text-gray-500 uppercase tracking-wider border-b border-gray-200">
                  Suas Organizações
                </div>
                {userMemberships.map((membership) => (
                  <Menu.Item key={membership.tenant.id}>
                    {({ active }) => (
                      <button
                        onClick={() => handleTenantSwitch(membership.tenant.slug)}
                        className={cn(
                          'flex items-center w-full px-3 py-2 text-sm text-left',
                          active ? 'bg-gray-100' : '',
                          membership.tenant.slug === tenantSlug ? 'bg-primary-50 text-primary-700' : 'text-gray-700'
                        )}
                      >
                        <div className="flex-1">
                          <p className="font-medium">{membership.tenant.name}</p>
                          <p className="text-xs text-gray-500">
                            /{membership.tenant.slug} • {membership.role}
                          </p>
                        </div>
                        {membership.tenant.slug === tenantSlug && (
                          <CheckIcon className="h-4 w-4 text-primary-600" />
                        )}
                      </button>
                    )}
                  </Menu.Item>
                ))}
              </>
            ) : (
              <div className="px-3 py-2 text-sm text-gray-500">
                {loading ? 'Carregando...' : 'Nenhuma organização encontrada'}
              </div>
            )}
          </div>
        </Menu.Items>
      </Transition>
    </Menu>
  )
}











