'use client';

// Settings page

import { useTranslations } from '@/hooks/use-translations';
import { ProtectedRoute } from '@/components/auth/protected-route';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { useTheme } from '@/hooks/use-theme';
import { useLanguage } from '@/hooks/use-language';
import type { Locale } from '@/contexts/language-context';
import { Globe, Moon, Bell, Shield } from 'lucide-react';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';

function SettingsContent() {
  const t = useTranslations('settings');
  const { theme, changeTheme } = useTheme();
  const { locale, changeLanguage } = useLanguage();

  return (
    <div className="container mx-auto p-8 max-w-4xl space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold mb-2">{t('title')}</h1>
        <p className="text-muted-foreground">
          {t('description')}
        </p>
      </div>

      {/* Language Settings */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Globe className="size-5" />
            {t('language.title')}
          </CardTitle>
          <CardDescription>
            {t('language.description')}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            <Label htmlFor="language">{t('sections.language')}</Label>
            <Select value={locale} onValueChange={(value) => changeLanguage(value as Locale)}>
              <SelectTrigger id="language">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="en">🇬🇧 {t('language.english')}</SelectItem>
                <SelectItem value="pl">🇵🇱 {t('language.polish')}</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      {/* Theme Settings */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Moon className="size-5" />
            {t('theme.title')}
          </CardTitle>
          <CardDescription>
            {t('theme.description')}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            <Label htmlFor="theme">{t('theme.title')}</Label>
            <Select value={theme} onValueChange={(value) => changeTheme(value as any)}>
              <SelectTrigger id="theme">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="light">{t('theme.light')}</SelectItem>
                <SelectItem value="dark">{t('theme.dark')}</SelectItem>
                <SelectItem value="system">{t('theme.system')}</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      {/* Notifications Settings */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Bell className="size-5" />
            {t('notifications.title')}
          </CardTitle>
          <CardDescription>
            {t('notifications.description')}
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <div>
                <Label>{t('notifications.email')}</Label>
                <p className="text-sm text-muted-foreground">
                  {t('notifications.emailDescription')}
                </p>
              </div>
              <Button variant="outline" size="sm" disabled>
                {t('notifications.configure')}
              </Button>
            </div>
          </div>
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <div>
                <Label>{t('notifications.push')}</Label>
                <p className="text-sm text-muted-foreground">
                  {t('notifications.pushDescription')}
                </p>
              </div>
              <Button variant="outline" size="sm" disabled>
                {t('notifications.configure')}
              </Button>
            </div>
          </div>
          <Alert variant="info">
            <AlertTitle>
              {t('common.comingSoon')}
            </AlertTitle>
            <AlertDescription>
              {t('notifications.comingSoon')}
            </AlertDescription>
          </Alert>
        </CardContent>
      </Card>

      {/* Privacy Settings */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Shield className="size-5" />
            {t('privacy.title')}
          </CardTitle>
          <CardDescription>
            {t('privacy.description')}
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label>{t('privacy.dataSharing')}</Label>
            <p className="text-sm text-muted-foreground">
              {t('privacy.dataSharingDescription')}
            </p>
          </div>
          <div className="space-y-2">
            <Label>{t('privacy.analytics')}</Label>
            <p className="text-sm text-muted-foreground">
              {t('privacy.analyticsDescription')}
            </p>
          </div>
          <Alert variant="info">
            <AlertTitle>
              {t('common.comingSoon')}
            </AlertTitle>
            <AlertDescription>
              {t('privacy.comingSoon')}
            </AlertDescription>
          </Alert>
        </CardContent>
      </Card>
    </div>
  );
}

export default function SettingsPage() {
  return (
    <ProtectedRoute>
      <SettingsContent />
    </ProtectedRoute>
  );
}
