import { useLanguage } from '@/contexts/language-context';
import enMessages from '../../messages/en.json';
import plMessages from '../../messages/pl.json';

const messages = {
  en: enMessages,
  pl: plMessages,
};

export function useTranslations(namespace: string) {
  const { locale } = useLanguage();
  
  const t = (key: string, params?: Record<string, string>) => {
    const keys = `${namespace}.${key}`.split('.');
    let value: any = messages[locale];
    
    for (const k of keys) {
      if (value && typeof value === 'object') {
        value = value[k];
      } else {
        return key; // Return key if not found
      }
    }
    
    if (typeof value !== 'string') {
      return key;
    }
    
    // Replace params like {name}
    if (params) {
      return value.replace(/\{(\w+)\}/g, (match, paramKey) => {
        return params[paramKey] || match;
      });
    }
    
    return value;
  };
  
  return t;
}
