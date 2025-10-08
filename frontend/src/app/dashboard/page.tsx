'use client';

// Protected dashboard page - example of using auth

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { ProtectedRoute } from '@/components/auth/protected-route';
import { useAuth } from '@/contexts/auth-context';
import { useMyProfile } from '@/hooks/use-profile';
import { useTranslations } from '@/hooks/use-translations';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

function DashboardContent() {
  const t = useTranslations('dashboard');
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
          <div className="animate-spin size-12 border-4 border-primary border-t-transparent rounded-full mx-auto mb-4"></div>
          <p className="text-muted-foreground">{t('profile.loading')}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-8">
      <div className="max-w-4xl mx-auto space-y-6">
        <div>
          <h1 className="text-3xl font-bold">{t('title')}</h1>
          <p className="text-muted-foreground mt-1">{t('welcome', { name: user?.name || '' })}</p>
        </div>

        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          <Card>
            <CardHeader>
              <CardTitle>{t('profile.title')}</CardTitle>
              <CardDescription>{t('profile.description')}</CardDescription>
            </CardHeader>
            <CardContent>
              <dl className="space-y-2 text-sm">
                <div>
                  <dt className="font-medium text-muted-foreground">{t('profile.headline')}</dt>
                  <dd className="text-foreground">{profile?.headline ?? t('profile.notSet')}</dd>
                </div>
                <div>
                  <dt className="font-medium text-muted-foreground">{t('profile.location')}</dt>
                  <dd className="text-foreground">{profile?.location ?? t('profile.notSet')}</dd>
                </div>
                <div>
                  <dt className="font-medium text-muted-foreground">{t('profile.completeness')}</dt>
                  <dd className="text-foreground">
                    <div className="flex items-center gap-2">
                      <div className="flex-1 bg-muted rounded-full h-2">
                        <div 
                          className="bg-primary h-2 rounded-full" 
                               style={{ width: `${profile?.completenessScore ?? 0}%` }}
                        ></div>
                      </div>
                      <span className="text-xs">{profile?.completenessScore ?? 0}%</span>
                    </div>
                  </dd>
                </div>
                <div>
                  <dt className="font-medium text-muted-foreground">{t('profile.visibility')}</dt>
                  <dd className="text-foreground capitalize">{profile?.visibility?.toLowerCase() ?? 'private'}</dd>
                </div>
              </dl>
              <div className="mt-4 flex gap-2">
                {profile ? (
                  <Button asChild variant="outline" size="sm" className="w-full">
                    <Link href="/profile/edit">
                      {t('profile.editProfile')}
                    </Link>
                  </Button>
                ) : (
                  <Button asChild size="sm" className="w-full">
                    <Link href="/profile/create">
                      {t('profile.createProfile')}
                    </Link>
                  </Button>
                )}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>{t('account.title')}</CardTitle>
              <CardDescription>{t('account.description')}</CardDescription>
            </CardHeader>
            <CardContent>
              <dl className="space-y-2 text-sm">
                <div>
                  <dt className="font-medium text-muted-foreground">{t('account.email')}</dt>
                  <dd className="text-foreground">{user?.email}</dd>
                </div>
                <div>
                  <dt className="font-medium text-muted-foreground">{t('account.tier')}</dt>
                  <dd className="text-foreground capitalize">{user?.tier || 'free'}</dd>
                </div>
                <div>
                  <dt className="font-medium text-muted-foreground">{t('account.status')}</dt>
                  <dd className="text-foreground">
                    {user?.isActive ? (
                      <span className="text-green-600">{t('account.active')}</span>
                    ) : (
                      <span className="text-destructive">{t('account.inactive')}</span>
                    )}
                  </dd>
                </div>
              </dl>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>{t('experience.title')}</CardTitle>
              <CardDescription>{t('experience.description')}</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground mb-4">
                {t('experience.content')}
              </p>
              <Button asChild variant="outline" size="sm" className="w-full">
                <Link href="/dashboard/experiences">
                  {t('experience.manage')}
                </Link>
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>{t('projects.title')}</CardTitle>
              <CardDescription>{t('projects.description')}</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground mb-4">
                {t('projects.content')}
              </p>
              <Button asChild variant="outline" size="sm" className="w-full">
                <Link href="/dashboard/projects">
                  {t('projects.manage')}
                </Link>
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>{t('cvs.title')}</CardTitle>
              <CardDescription>{t('cvs.description')}</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                {t('cvs.comingSoon')}
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>{t('settings.title')}</CardTitle>
              <CardDescription>{t('settings.description')}</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                {t('settings.comingSoon')}
              </p>
            </CardContent>
          </Card>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>{t('quickStart.title')}</CardTitle>
            <CardDescription>{t('quickStart.description')}</CardDescription>
          </CardHeader>
          <CardContent>
            <ol className="list-decimal list-inside space-y-2 text-sm text-foreground">
              <li>{t('quickStart.step1')}</li>
              <li>{t('quickStart.step2')}</li>
              <li>{t('quickStart.step3')}</li>
              <li>{t('quickStart.step4')}</li>
            </ol>
            <div className="mt-4 pt-4 border-t">
              <Button asChild className="w-full">
                <Link href="/profile/create">
                  {t('quickStart.cta')}
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
