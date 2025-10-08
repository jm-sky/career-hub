'use client';

// User Profile page - Edit user account data (name, email, password)

import { useState } from 'react';
import { ProtectedRoute } from '@/components/auth/protected-route';
import { useAuth } from '@/contexts/auth-context';
import { useTranslations } from '@/hooks/use-translations';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { ChangePasswordForm } from '@/components/auth/change-password-form';
import { User, Shield } from 'lucide-react';

function UserProfileContent() {
  const t = useTranslations('userProfile');
  const { user } = useAuth();
  const [isEditingName, setIsEditingName] = useState(false);
  const [name, setName] = useState(user?.name || '');

  const handleSaveName = async () => {
    // TODO: Implement API call to update user name
    console.log('Saving name:', name);
    setIsEditingName(false);
  };

  return (
    <div className="container mx-auto p-8 max-w-4xl space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold mb-2">{t('title')}</h1>
        <p className="text-muted-foreground">
          {t('description')}
        </p>
      </div>

      {/* Personal Information */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <User className="size-5" />
            {t('personalInfo.title')}
          </CardTitle>
          <CardDescription>
            {t('personalInfo.description')}
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Name */}
          <div className="space-y-2">
            <Label htmlFor="name">{t('personalInfo.fullName')}</Label>
            <div className="flex gap-2">
              <Input
                id="name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                disabled={!isEditingName}
              />
              {isEditingName ? (
                <div className="flex gap-2">
                  <Button onClick={handleSaveName}>{t('personalInfo.save')}</Button>
                  <Button 
                    variant="outline" 
                    onClick={() => {
                      setName(user?.name || '');
                      setIsEditingName(false);
                    }}
                  >
                    {t('personalInfo.cancel')}
                  </Button>
                </div>
              ) : (
                <Button variant="outline" onClick={() => setIsEditingName(true)}>
                  {t('personalInfo.edit')}
                </Button>
              )}
            </div>
          </div>

          {/* Email */}
          <div className="space-y-2">
            <Label htmlFor="email">{t('personalInfo.email')}</Label>
            <div className="flex gap-2">
              <Input
                id="email"
                type="email"
                value={user?.email}
                disabled
              />
              <Button variant="outline" disabled>
                {t('common.edit', undefined, true)}
              </Button>
            </div>
            <p className="text-sm text-muted-foreground">
              {t('personalInfo.emailNote')}
            </p>
          </div>

          {/* Account Tier */}
          <div className="space-y-2">
            <Label>{t('personalInfo.accountTier')}</Label>
            <div className="flex items-center gap-2">
              <span className="px-3 py-1 bg-primary/10 text-primary rounded-md font-medium capitalize">
                {user?.tier || 'free'}
              </span>
            </div>
          </div>

          {/* Account Status */}
          <div className="space-y-2">
            <Label>{t('personalInfo.accountStatus')}</Label>
            <div className="flex items-center gap-2">
              {user?.isActive ? (
                <span className="px-3 py-1 bg-green-100 text-green-800 rounded-md font-medium">
                  {t('personalInfo.active')}
                </span>
              ) : (
                <span className="px-3 py-1 bg-red-100 text-red-800 rounded-md font-medium">
                  {t('personalInfo.inactive')}
                </span>
              )}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Security - Change Password */}
      <div className="flex flex-col items-center">
        <ChangePasswordForm />
      </div>

      {/* Two-Factor Authentication */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Shield className="size-5" />
            {t('twoFactor.title')}
          </CardTitle>
          <CardDescription>
            {t('twoFactor.description')}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Button variant="outline" disabled>
            {t('twoFactor.enable')}
          </Button>
          <Alert variant="info" className="mt-4">
            <AlertTitle>{t('common.comingSoon', undefined, true)}</AlertTitle>
            <AlertDescription>
              {t('twoFactor.comingSoon')}
            </AlertDescription>
          </Alert>
        </CardContent>
      </Card>

      {/* Danger Zone */}
      <Card className="border-destructive">
        <CardHeader>
          <CardTitle className="text-destructive">{t('dangerZone.title')}</CardTitle>
          <CardDescription>
            {t('dangerZone.description')}
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <h4 className="font-medium mb-2">{t('dangerZone.deleteAccount')}</h4>
            <p className="text-sm text-muted-foreground mb-4">
              {t('dangerZone.deleteAccountDescription')}
            </p>
            <Button variant="destructive" disabled>
              {t('dangerZone.deleteMyAccount')}
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

export default function UserProfilePage() {
  return (
    <ProtectedRoute>
      <UserProfileContent />
    </ProtectedRoute>
  );
}
