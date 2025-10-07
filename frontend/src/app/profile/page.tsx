'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { ProtectedRoute } from '@/components/auth/protected-route';
import { useAuth } from '@/contexts/auth-context';
import { useMyProfile } from '@/hooks/use-profile';

function ProfilePage() {
  const router = useRouter();
  const { user } = useAuth();
  const { data: profile, isLoading, error } = useMyProfile();

  useEffect(() => {
    if (!isLoading) {
      if (profile) {
        // User has a profile, redirect to edit or view
        router.push('/profile/edit');
      } else if (error) {
        // User doesn't have a profile, redirect to create
        router.push('/profile/create');
      }
    }
  }, [profile, isLoading, error, router]);

  // Show loading state while checking for profile
  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mx-auto"></div>
        <p className="mt-4 text-gray-600">Loading your profile...</p>
      </div>
    </div>
  );
}

export default function ProfilePageWrapper() {
  return (
    <ProtectedRoute>
      <ProfilePage />
    </ProtectedRoute>
  );
}
