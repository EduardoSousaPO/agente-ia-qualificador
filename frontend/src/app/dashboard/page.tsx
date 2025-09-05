'use client';

import React from 'react';
import { DashboardLayout } from '@/components/layout/dashboard-layout';
import QualifiedLeadsDashboard from '@/components/dashboard/qualified-leads-dashboard';

export default function DashboardPage() {
  return (
    <DashboardLayout>
      <QualifiedLeadsDashboard />
    </DashboardLayout>
  );
}


