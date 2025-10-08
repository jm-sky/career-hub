'use client';

import { NextIntlClientProvider } from 'next-intl';
import { ReactNode, useEffect, useState } from 'react';
import { LanguageProvider, useLanguage, DEFAULT_LOCALE } from '@/contexts/language-context';

function IntlProviderInner({ children }: { children: ReactNode }) {
  const { locale } = useLanguage();
  const [messages, setMessages] = useState<any>(null);

  // Load messages when locale changes
  useEffect(() => {
    import(`../../messages/${locale}.json`)
      .then((mod) => setMessages(mod.default))
      .catch(() => {
        // Fallback to English if locale not found
        import(`../../messages/${DEFAULT_LOCALE}.json`).then((mod) => setMessages(mod.default));
      });
  }, [locale]);

  if (!messages) {
    return <>{children}</>;
  }

  return (
    <NextIntlClientProvider 
      key={locale} 
      locale={locale} 
      messages={messages}
    >
      {children}
    </NextIntlClientProvider>
  );
}

export function IntlProvider({ children }: { children: ReactNode }) {
  return (
    <LanguageProvider>
      <IntlProviderInner>{children}</IntlProviderInner>
    </LanguageProvider>
  );
}
