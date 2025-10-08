'use client';

import { createContext, useContext, ReactNode, useState, useEffect } from 'react';

export type Locale = 'en' | 'pl';

export interface LanguageOption {
  code: Locale;
  name: string;
  flag: string;
}

export const DEFAULT_LOCALE: Locale = 'en';

export const LANGUAGES: LanguageOption[] = [
  { code: 'en', name: 'English', flag: 'EN' },
  { code: 'pl', name: 'Polski', flag: 'PL' },
];

const COOKIE_NAME = 'NEXT_LOCALE';
const COOKIE_MAX_AGE = 31536000; // 1 year

interface LanguageContextType {
  locale: Locale;
  currentLanguage: LanguageOption;
  languages: LanguageOption[];
  changeLanguage: (newLocale: Locale) => void;
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

export function useLanguage() {
  const context = useContext(LanguageContext);
  if (context === undefined) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
}

export function LanguageProvider({ children }: { children: ReactNode }) {
  const [locale, setLocale] = useState<Locale>(DEFAULT_LOCALE);

  // Load locale from cookie on mount
  useEffect(() => {
    const cookieLocale = getCookieLocale();
    setLocale(cookieLocale);
  }, []);

  const getCookieLocale = (): Locale => {
    if (typeof document === 'undefined') return DEFAULT_LOCALE;
    
    const cookie = document.cookie
      .split('; ')
      .find(row => row.startsWith(`${COOKIE_NAME}=`))
      ?.split('=')[1];
    
    return (cookie as Locale) ?? DEFAULT_LOCALE;
  };

  const getCurrentLanguage = (): LanguageOption => {
    return LANGUAGES.find(lang => lang.code === locale) ?? LANGUAGES[0];
  };

  const changeLanguage = (newLocale: Locale) => {
    // Set cookie
    document.cookie = `${COOKIE_NAME}=${newLocale}; path=/; max-age=${COOKIE_MAX_AGE}`;
    
    // Update state immediately (no need for router.refresh)
    setLocale(newLocale);
  };

  return (
    <LanguageContext.Provider
      value={{
        locale,
        currentLanguage: getCurrentLanguage(),
        languages: LANGUAGES,
        changeLanguage,
      }}
    >
      {children}
    </LanguageContext.Provider>
  );
}
