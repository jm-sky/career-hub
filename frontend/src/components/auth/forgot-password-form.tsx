'use client';

// Forgot password form component

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import Link from 'next/link';

import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { useTranslations } from '@/hooks/use-translations';
import { getErrorMessage } from '@/lib/error-guards';
import { ForgotPasswordSchema, type ForgotPasswordFormData } from '@/lib/validations';
import { useForgotPassword } from '@/hooks/use-auth';

export function ForgotPasswordForm() {
  const t = useTranslations('auth.forgotPassword');
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  const forgotPasswordMutation = useForgotPassword();

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<ForgotPasswordFormData>({
    resolver: zodResolver(ForgotPasswordSchema),
    mode: 'onBlur',
  });

  const onSubmit = async (data: ForgotPasswordFormData) => {
    setError(null);
    setSuccess(false);

    try {
      await forgotPasswordMutation.mutateAsync(data);
      setSuccess(true);
    } catch (error: unknown) {
      const errorMessage = getErrorMessage(error);
      setError(errorMessage);
    }
  };

  const isFormLoading = forgotPasswordMutation.isPending || isSubmitting;

  if (success) {
    return (
      <Card className="w-full max-w-md mx-auto">
        <CardHeader>
          <CardTitle>{t('successTitle')}</CardTitle>
          <CardDescription>
            {t('successSubtitle')}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="p-4 text-sm text-green-600 bg-green-50 border border-green-200 rounded-md">
              {t('successMessage')}
            </div>
            <Button variant="outline" className="w-full" asChild>
              <Link href="/login">{t('backToSignIn')}</Link>
            </Button>
          </div>
        </CardContent>
      </Card>
    );
  }

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

          <Button type="submit" className="w-full" disabled={isFormLoading}>
            {isFormLoading ? t('submitting') : t('submit')}
          </Button>

          <div className="text-center text-sm text-gray-600">
            {t('rememberPassword')}{' '}
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
