// modules/career/utils/queryUtils.ts
import { isAuthError, isClientError } from '@/shared/utils/errorGuards'

export const profileQueryKeys = {
  all: ['career', 'profile'] as const,
  me: () => [...profileQueryKeys.all, 'me'] as const,
  public: (slug: string) => [...profileQueryKeys.all, 'public', slug] as const,
} as const

export function createProfileRetryFunction(maxAttempts = 2) {
  return (failureCount: number, error: unknown) => {
    if (isAuthError(error)) return false
    return failureCount < maxAttempts
  }
}

export function createProfileMutationRetryFunction(maxAttempts = 2) {
  return (failureCount: number, error: unknown) => {
    if (isClientError(error)) return false
    return failureCount < maxAttempts
  }
}

export const profileRetryFunction = createProfileRetryFunction()
export const profileMutationRetryFunction = createProfileMutationRetryFunction()
