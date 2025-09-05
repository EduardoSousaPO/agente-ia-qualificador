'use client'

import { TenantProvider } from '@/hooks/useTenant'
import { DashboardLayout } from '@/components/layout/dashboard-layout'

export default function TenantLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <TenantProvider>
      <DashboardLayout>
        {children}
      </DashboardLayout>
    </TenantProvider>
  )
}
