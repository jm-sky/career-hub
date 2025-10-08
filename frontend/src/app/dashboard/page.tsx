'use client';

// Protected dashboard page - example of using auth

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { ProtectedRoute } from '@/components/auth/protected-route';
import { useAuth } from '@/contexts/auth-context';
import { useMyProfile } from '@/hooks/use-profile';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

function DashboardContent() {
  const router = useRouter();
  const { user } = useAuth();
  const { data: profile, isLoading: profileLoading, error: profileError } = useMyProfile();

  // Redirect to profile creation if user doesn't have a profile
  useEffect(() => {
    if (!profileLoading && !profile && profileError) {
      // If we get a 404 error, it means the user doesn't have a profile yet
      router.push('/profile/create');
    }
  }, [profile, profileLoading, profileError, router]);

  // Show loading state while checking for profile
  if (profileLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading your profile...</p>
        </div>
      </div>
    );
  }

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
              <CardDescription>Your professional profile</CardDescription>
            </CardHeader>
            <CardContent>
              <dl className="space-y-2 text-sm">
                <div>
                  <dt className="font-medium text-gray-500">Headline</dt>
                  <dd className="text-gray-900">{profile?.headline ?? 'Not set'}</dd>
                </div>
                <div>
                  <dt className="font-medium text-gray-500">Location</dt>
                  <dd className="text-gray-900">{profile?.location ?? 'Not set'}</dd>
                </div>
                <div>
                  <dt className="font-medium text-gray-500">Completeness</dt>
                  <dd className="text-gray-900">
                    <div className="flex items-center gap-2">
                      <div className="flex-1 bg-gray-200 rounded-full h-2">
                        <div 
                          className="bg-blue-600 h-2 rounded-full" 
                               style={{ width: `${profile?.completenessScore ?? 0}%` }}
                        ></div>
                      </div>
                      <span className="text-xs">{profile?.completenessScore ?? 0}%</span>
                    </div>
                  </dd>
                </div>
                <div>
                  <dt className="font-medium text-gray-500">Visibility</dt>
                  <dd className="text-gray-900 capitalize">{profile?.visibility?.toLowerCase() ?? 'private'}</dd>
                </div>
              </dl>
              <div className="mt-4 flex gap-2">
                <Button asChild variant="outline" size="sm" className="flex-1">
                  <Link href="/profile/edit">
                    Edit Profile
                  </Link>
                </Button>
                <Button asChild size="sm" className="flex-1">
                  <Link href="/profile/create">
                    Create Profile
                  </Link>
                </Button>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Account</CardTitle>
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
              <CardTitle>Experience</CardTitle>
              <CardDescription>Manage your work experience</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-600 mb-4">
                Add and manage your professional work experience and career history.
              </p>
              <Button asChild variant="outline" size="sm" className="w-full">
                <Link href="/dashboard/experiences">
                  Manage Experience
                </Link>
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Projects</CardTitle>
              <CardDescription>Manage your projects</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-600 mb-4">
                Showcase your notable projects and technical achievements.
              </p>
              <Button asChild variant="outline" size="sm" className="w-full">
                <Link href="/dashboard/projects">
                  Manage Projects
                </Link>
              </Button>
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
            <div className="mt-4 pt-4 border-t">
              <Button asChild className="w-full">
                <Link href="/profile/create">
                  🚀 Create Your Profile
                </Link>
              </Button>
            </div>
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
