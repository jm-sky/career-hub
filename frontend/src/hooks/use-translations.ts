import { useLanguage } from '@/contexts/language-context';
import enMessages from '../../messages/en.json';
import plMessages from '../../messages/pl.json';

const messages = {
  en: enMessages,
  pl: plMessages,
};

export function useTranslations(namespace: string) {
  const { locale } = useLanguage();
  
  const t = (key: string, params?: Record<string, string>, isRoot?: boolean) => {
    // If isRoot is true, use key as-is (e.g., 'common.comingSoon')
    // Otherwise, prepend namespace (e.g., 'settings' + 'title' = 'settings.title')
    const fullPath = isRoot ? key : `${namespace}.${key}`;
    
    const keys = fullPath.split('.');
    let value: any = messages[locale];
    
    for (const k of keys) {
      if (value && typeof value === 'object') {
        value = value[k];
      } else {
        // Return the full path if not found for debugging
        return fullPath;
      }
    }
    
    if (typeof value !== 'string') {
      return fullPath;
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
