'use client';

import React from 'react';
import QualifiedLeadsDashboard from '@/components/dashboard/qualified-leads-dashboard';

export default function DashboardPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <QualifiedLeadsDashboard />
      </div>
    </div>
  );
}


