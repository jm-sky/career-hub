'use client';

// Login form component with validation and loading states

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { useAuth } from '@/contexts/auth-context';
import { useTranslations } from '@/hooks/use-translations';
import { getErrorMessage } from '@/lib/error-guards';
import { LoginSchema, type LoginFormData } from '@/lib/validations';
import { AUTH_CONFIG } from '@/lib/auth-config';

const REDIRECT_DELAY = 500;

export function LoginForm() {
  const router = useRouter();
  const { login, isLoading } = useAuth();
  const t = useTranslations('auth.login');
  const [error, setError] = useState<string | null>(null);
  const [isRedirecting, setIsRedirecting] = useState(false);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginFormData>({
    defaultValues: {
      email: process.env.NEXT_PUBLIC_DEFAULT_USER_EMAIL ?? '',
      password: process.env.NEXT_PUBLIC_DEFAULT_USER_PASSWORD ?? '',
    },
    resolver: zodResolver(LoginSchema),
    mode: 'onBlur',
  });

  const onSubmit = async (data: LoginFormData) => {
    setError(null);
    setSuccessMessage(null);

    try {
      await login(data);
      setSuccessMessage(t('successMessage'));
      setIsRedirecting(true);
      
      // Small delay to show success message
      setTimeout(() => {
        router.push(AUTH_CONFIG.loginRedirect);
      }, REDIRECT_DELAY);
    } catch (error: unknown) {
      const errorMessage = getErrorMessage(error);
      setError(errorMessage);
      setIsRedirecting(false);
    }
  };

  const isFormLoading = isLoading || isSubmitting || isRedirecting;

  return (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader>
        <CardTitle>{t('title')}</CardTitle>
        <CardDescription>
          {t('subtitle')}
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          {error && (
            <div className="p-3 text-sm text-red-600 bg-red-50 border border-red-200 rounded-md">
              {error}
            </div>
          )}
          
          {successMessage && (
            <div className="p-3 text-sm text-green-600 bg-green-50 border border-green-200 rounded-md">
              {successMessage}
            </div>
          )}

          <div className="space-y-2">
            <Label htmlFor="email">{t('email')}</Label>
            <Input
              id="email"
              type="email"
              placeholder={t('emailPlaceholder')}
              disabled={isFormLoading}
              {...register('email')}
            />
            {errors.email && (
              <p className="text-sm text-red-600">{errors.email.message}</p>
            )}
          </div>

          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <Label htmlFor="password">{t('password')}</Label>
              <Button
                variant="link"
                className="p-0 h-auto text-sm"
                disabled={isFormLoading}
                asChild
              >
                <Link href="/forgot-password">{t('forgotPassword')}</Link>
              </Button>
            </div>
            <Input
              id="password"
              type="password"
              placeholder={t('passwordPlaceholder')}
              disabled={isFormLoading}
              {...register('password')}
            />
            {errors.password && (
              <p className="text-sm text-red-600">{errors.password.message}</p>
            )}
          </div>

          <Button type="submit" className="w-full" disabled={isFormLoading}>
            {isRedirecting ? t('redirecting') : isLoading ? t('authenticating') : isSubmitting ? t('submitting') : t('submit')}
          </Button>

          <div className="text-center text-sm text-gray-600">
            {t('noAccount')}{' '}
            <Button
              variant="link"
              className="p-0 h-auto"
              disabled={isFormLoading}
              asChild
            >
              <Link href="/register">{t('signUp')}</Link>
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
}
