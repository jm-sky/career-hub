'use client';

// Landing page - redirects to dashboard if authenticated, otherwise shows welcome

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useAuth } from '@/contexts/auth-context';
import { Button } from '@/components/ui/button';
import LogoTextLink from '@/components/layout/LogoTextLink';

export default function HomePage() {
  const router = useRouter();
  const { isAuthenticated, isLoading } = useAuth();

  useEffect(() => {
    if (!isLoading && isAuthenticated) {
      router.push('/dashboard');
    }
  }, [isAuthenticated, isLoading, router]);

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

  if (isAuthenticated) {
    return null; // Will redirect to dashboard
  }

  return (
    <div className="flex min-h-screen flex-col">
      <header className="border-b">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <LogoTextLink />
          <div className="space-x-2">
            <Button variant="ghost" asChild>
              <Link href="/login">Sign In</Link>
            </Button>
            <Button asChild>
              <Link href="/register">Get Started</Link>
            </Button>
          </div>
        </div>
      </header>

      <main className="flex-1 flex items-center justify-center px-4">
        <div className="max-w-3xl mx-auto text-center space-y-8">
          <div className="space-y-4">
            <h2 className="text-5xl font-bold tracking-tight">
              Professional Profile Management
            </h2>
            <p className="text-xl text-gray-600">
              Create tailored CVs, manage your experience, and showcase your professional journey with CareerHub
            </p>
          </div>

          <div className="flex items-center justify-center gap-4">
            <Button size="lg" asChild>
              <Link href="/register">Create Account</Link>
            </Button>
            <Button size="lg" variant="outline" asChild>
              <Link href="/login">Sign In</Link>
            </Button>
          </div>

          <div className="grid md:grid-cols-3 gap-6 mt-16 text-left">
            <div className="space-y-2">
              <h3 className="font-semibold text-lg">Smart Profiles</h3>
              <p className="text-sm text-gray-600">
                Build comprehensive professional profiles with your experience, skills, and projects
              </p>
            </div>
            <div className="space-y-2">
              <h3 className="font-semibold text-lg">Multiple CVs</h3>
              <p className="text-sm text-gray-600">
                Create unlimited CV versions tailored for different positions and industries
              </p>
            </div>
            <div className="space-y-2">
              <h3 className="font-semibold text-lg">AI-Powered</h3>
              <p className="text-sm text-gray-600">
                Get intelligent suggestions to improve your profile and CV content
              </p>
            </div>
          </div>
        </div>
      </main>

      <footer className="border-t py-6">
        <div className="container mx-auto px-4 text-center text-sm text-gray-600">
          <p>&copy; 2025 DEV Made IT. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
