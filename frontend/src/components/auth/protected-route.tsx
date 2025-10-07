'use client';

// Protected route component - redirects unauthenticated users to login

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/auth-context';
import { AUTH_CONFIG } from '@/lib/auth-config';

interface ProtectedRouteProps {
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

export function ProtectedRoute({ children, fallback }: ProtectedRouteProps) {
  const router = useRouter();
  const { isAuthenticated, isLoading } = useAuth();
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push(AUTH_CONFIG.unauthorizedRedirect);
    }
  }, [isAuthenticated, isLoading, router]);

  // Prevent hydration mismatch by not rendering until mounted on client
  if (!isMounted) {
    return null;
  }

  // Show loading state
  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  // Show fallback or null while redirecting
  if (!isAuthenticated) {
    return fallback || null;
  }

  // User is authenticated, show protected content
  return <>{children}</>;
}
