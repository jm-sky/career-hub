'use client';

// Landing page - redirects to dashboard if authenticated, otherwise shows welcome

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useAuth } from '@/contexts/auth-context';
import { useTranslations } from '@/hooks/use-translations';
import { Button } from '@/components/ui/button';
import LogoTextLink from '@/components/layout/LogoTextLink';
import { LanguageSwitcher } from '@/components/layout/LanguageSwitcher';

export default function HomePage() {
  const router = useRouter();
  const { isAuthenticated, isLoading } = useAuth();
  const t = useTranslations('homepage');

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
          <p className="mt-4 text-gray-600">{t('common.loading', undefined, true)}</p>
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
          <LogoTextLink href="/" />
          <div className="flex flex-row items-center gap-2">
            <LanguageSwitcher />
            <Button variant="ghost" asChild>
              <Link href="/login">{t('signIn')}</Link>
            </Button>
            <Button asChild>
              <Link href="/register">{t('createAccount')}</Link>
            </Button>
          </div>
        </div>
      </header>

      <main className="flex-1 flex items-center justify-center px-4">
        <div className="max-w-3xl mx-auto text-center space-y-8">
          <div className="space-y-4">
            <h2 className="text-5xl font-bold tracking-tight">
              {t('title')}
            </h2>
            <p className="text-xl text-gray-600">
              {t('subtitle')}
            </p>
          </div>

          <div className="flex items-center justify-center gap-4">
            <Button size="lg" asChild>
              <Link href="/register">{t('createAccount')}</Link>
            </Button>
            <Button size="lg" variant="outline" asChild>
              <Link href="/login">{t('signIn')}</Link>
            </Button>
          </div>

          <div className="grid md:grid-cols-3 gap-6 mt-16 text-left">
            <div className="space-y-2">
              <h3 className="font-semibold text-lg">{t('features.smartProfiles.title')}</h3>
              <p className="text-sm text-gray-600">
                {t('features.smartProfiles.description')}
              </p>
            </div>
            <div className="space-y-2">
              <h3 className="font-semibold text-lg">{t('features.multipleCvs.title')}</h3>
              <p className="text-sm text-gray-600">
                {t('features.multipleCvs.description')}
              </p>
            </div>
            <div className="space-y-2">
              <h3 className="font-semibold text-lg">{t('features.aiPowered.title')}</h3>
              <p className="text-sm text-gray-600">
                {t('features.aiPowered.description')}
              </p>
            </div>
          </div>
        </div>
      </main>

      <footer className="border-t py-6">
        <div className="container mx-auto px-4 text-center text-sm text-gray-600">
          <p>{t('footer.copyright')}</p>
        </div>
      </footer>
    </div>
  );
}
