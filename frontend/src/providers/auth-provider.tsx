'use client';

// Combined Auth and Query provider for app-wide authentication

import { ReactNode } from 'react';
import { QueryProvider } from './query-provider';
import { AuthProvider as AuthContextProvider } from '@/contexts/auth-context';

export function AuthProvider({ children }: { children: ReactNode }) {
  return (
    <QueryProvider>
      <AuthContextProvider>
        {children}
      </AuthContextProvider>
    </QueryProvider>
  );
}
