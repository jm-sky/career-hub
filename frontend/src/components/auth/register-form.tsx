'use client';

// Register form component with validation and loading states

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
import { RegisterSchema, type RegisterFormData } from '@/lib/validations';
import { AUTH_CONFIG } from '@/lib/auth-config';

export function RegisterForm() {
  const router = useRouter();
  const { register: registerUser, isLoading } = useAuth();
  const t = useTranslations('auth.register');
  const [error, setError] = useState<string | null>(null);
  const [isRedirecting, setIsRedirecting] = useState(false);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<RegisterFormData>({
    resolver: zodResolver(RegisterSchema),
    mode: 'onBlur',
  });

  const onSubmit = async (data: RegisterFormData) => {
    setError(null);

    try {
      await registerUser(data);
      setIsRedirecting(true);
      router.push(AUTH_CONFIG.registerRedirect || AUTH_CONFIG.loginRedirect);
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

          <div className="space-y-2">
            <Label htmlFor="name">{t('name')}</Label>
            <Input
              id="name"
              type="text"
              placeholder={t('namePlaceholder')}
              disabled={isFormLoading}
              {...register('name')}
            />
            {errors.name && (
              <p className="text-sm text-red-600">{errors.name.message}</p>
            )}
          </div>

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
            <Label htmlFor="password">{t('password')}</Label>
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
            <p className="text-xs text-gray-500">
              {t('passwordRequirements')}
            </p>
          </div>

          <Button type="submit" className="w-full" disabled={isFormLoading}>
            {isRedirecting ? t('redirecting') : isLoading ? t('creating') : isSubmitting ? t('submitting') : t('submit')}
          </Button>

          <div className="text-center text-sm text-gray-600">
            {t('hasAccount')}{' '}
            <Button
              variant="link"
              className="p-0 h-auto"
              disabled={isFormLoading}
              asChild
            >
              <Link href="/login">{t('signIn')}</Link>
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
}
