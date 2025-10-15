'use client';

// Reset password form component

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { useTranslations } from '@/hooks/use-translations';
import { getErrorMessage } from '@/lib/error-guards';
import { ResetPasswordSchema, type ResetPasswordFormData } from '@/lib/validations';
import { useResetPassword } from '@/hooks/use-auth';

interface ResetPasswordFormProps {
  token: string;
}

export function ResetPasswordForm({ token }: ResetPasswordFormProps) {
  const router = useRouter();
  const t = useTranslations('auth.resetPassword');
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  const resetPasswordMutation = useResetPassword();

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<ResetPasswordFormData>({
    resolver: zodResolver(ResetPasswordSchema),
    mode: 'onBlur',
    defaultValues: {
      token,
    },
  });

  const onSubmit = async (data: ResetPasswordFormData) => {
    setError(null);
    setSuccess(false);

    try {
      await resetPasswordMutation.mutateAsync(data);
      setSuccess(true);
      setTimeout(() => router.push('/login'), 2000);
    } catch (error: unknown) {
      const errorMessage = getErrorMessage(error);
      setError(errorMessage);
    }
  };

  const isFormLoading = resetPasswordMutation.isPending || isSubmitting;

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

          <input type="hidden" {...register('token')} />

          <div className="space-y-2">
            <Label htmlFor="newPassword">{t('newPassword')}</Label>
            <Input
              id="newPassword"
              type="password"
              placeholder={t('passwordPlaceholder')}
              disabled={isFormLoading}
              {...register('newPassword')}
            />
            {errors.newPassword && (
              <p className="text-sm text-red-600">{errors.newPassword.message}</p>
            )}
            <p className="text-xs text-gray-500">
              {t('passwordRequirements')}
            </p>
          </div>

          <Button type="submit" className="w-full" disabled={isFormLoading}>
            {isFormLoading ? t('submitting') : t('submit')}
          </Button>

          <div className="text-center text-sm text-gray-600">
            <Button
              variant="link"
              className="p-0 h-auto"
              disabled={isFormLoading}
              asChild
            >
              <Link href="/login">{t('backToSignIn')}</Link>
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
}
