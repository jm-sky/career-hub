'use client';

// Change password form component for authenticated users

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { getErrorMessage } from '@/lib/error-guards';
import { ChangePasswordSchema, type ChangePasswordFormData } from '@/lib/validations';
import { useChangePassword } from '@/hooks/use-auth';
import { useTranslations } from '@/hooks/use-translations';

export function ChangePasswordForm() {
  const t = useTranslations('changePassword');
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  const changePasswordMutation = useChangePassword();

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<ChangePasswordFormData>({
    resolver: zodResolver(ChangePasswordSchema),
    mode: 'onBlur',
  });

  const onSubmit = async (data: ChangePasswordFormData) => {
    setError(null);
    setSuccess(false);

    try {
      await changePasswordMutation.mutateAsync(data);
      setSuccess(true);
      reset();
    } catch (error: unknown) {
      const errorMessage = getErrorMessage(error);
      setError(errorMessage);
    }
  };

  const isFormLoading = changePasswordMutation.isPending || isSubmitting;

  return (
    <Card className="w-full max-w-md">
      <CardHeader>
        <CardTitle>{t('title')}</CardTitle>
        <CardDescription>
          {t('description')}
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          {error && (
            <div className="p-3 text-sm text-destructive bg-red-50 border border-red-200 rounded-md">
              {error}
            </div>
          )}

          {success && (
            <div className="p-3 text-sm text-green-600 bg-green-50 border border-green-200 rounded-md">
              {t('success')}
            </div>
          )}

          <div className="space-y-2">
            <Label htmlFor="currentPassword">{t('currentPassword')}</Label>
            <Input
              id="currentPassword"
              type="password"
              placeholder="••••••••"
              disabled={isFormLoading}
              {...register('currentPassword')}
            />
            {errors.currentPassword && (
              <p className="text-sm text-destructive">{errors.currentPassword.message}</p>
            )}
          </div>

          <div className="space-y-2">
            <Label htmlFor="newPassword">{t('newPassword')}</Label>
            <Input
              id="newPassword"
              type="password"
              placeholder="••••••••"
              disabled={isFormLoading}
              {...register('newPassword')}
            />
            {errors.newPassword && (
              <p className="text-sm text-destructive">{errors.newPassword.message}</p>
            )}
            <p className="text-xs text-muted-foreground">
              {t('passwordRequirements')}
            </p>
          </div>

          <Button type="submit" className="w-full" disabled={isFormLoading}>
            {isFormLoading ? t('submitting') : t('submit')}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
