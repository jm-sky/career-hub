'use client';

// Protected dashboard page - example of using auth

import { ProtectedRoute } from '@/components/auth/protected-route';
import { useAuth } from '@/contexts/auth-context';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

function DashboardContent() {
  const { user } = useAuth();

  return (
    <div className="container mx-auto p-8">
      <div className="max-w-4xl mx-auto space-y-6">
        <div>
          <h1 className="text-3xl font-bold">Dashboard</h1>
          <p className="text-gray-600 mt-1">Welcome back, {user?.name}!</p>
        </div>

        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          <Card>
            <CardHeader>
              <CardTitle>Profile</CardTitle>
              <CardDescription>Your account information</CardDescription>
            </CardHeader>
            <CardContent>
              <dl className="space-y-2 text-sm">
                <div>
                  <dt className="font-medium text-gray-500">Email</dt>
                  <dd className="text-gray-900">{user?.email}</dd>
                </div>
                <div>
                  <dt className="font-medium text-gray-500">Account Tier</dt>
                  <dd className="text-gray-900 capitalize">{user?.tier || 'free'}</dd>
                </div>
                <div>
                  <dt className="font-medium text-gray-500">Status</dt>
                  <dd className="text-gray-900">
                    {user?.isActive ? (
                      <span className="text-green-600">Active</span>
                    ) : (
                      <span className="text-red-600">Inactive</span>
                    )}
                  </dd>
                </div>
              </dl>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>CVs</CardTitle>
              <CardDescription>Manage your CVs</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-600">
                Coming soon: Create and manage multiple versions of your CV tailored for different positions.
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Settings</CardTitle>
              <CardDescription>Account settings</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-600">
                Coming soon: Update your profile, change password, and manage preferences.
              </p>
            </CardContent>
          </Card>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Quick Start Guide</CardTitle>
            <CardDescription>Get started with CareerHub</CardDescription>
          </CardHeader>
          <CardContent>
            <ol className="list-decimal list-inside space-y-2 text-sm text-gray-700">
              <li>Complete your professional profile with experience and skills</li>
              <li>Create your first CV using our templates</li>
              <li>Customize your CV for specific job applications</li>
              <li>Export to PDF and share with employers</li>
            </ol>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

export default function DashboardPage() {
  return (
    <ProtectedRoute>
      <DashboardContent />
    </ProtectedRoute>
  );
}
