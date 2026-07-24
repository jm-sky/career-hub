// modules/career/utils/queryUtils.ts
import { isAuthError, isClientError } from '@/shared/utils/errorGuards'

export const profileQueryKeys = {
  all: ['career', 'profile'] as const,
  me: () => [...profileQueryKeys.all, 'me'] as const,
  public: (slug: string) => [...profileQueryKeys.all, 'public', slug] as const,
} as const

export const experienceQueryKeys = {
  all: ['career', 'experiences'] as const,
} as const

export const skillQueryKeys = {
  all: ['career', 'skills'] as const,
} as const

export const technologyQueryKeys = {
  all: ['career', 'technologies'] as const,
  search: (query?: string) => [...technologyQueryKeys.all, 'search', query ?? ''] as const,
} as const

export const projectQueryKeys = {
  all: ['career', 'projects'] as const,
} as const

export const educationQueryKeys = {
  all: ['career', 'education'] as const,
} as const

export const certificationQueryKeys = {
  all: ['career', 'certifications'] as const,
} as const

export const achievementQueryKeys = {
  all: ['career', 'achievements'] as const,
} as const

export const languageQueryKeys = {
  all: ['career', 'languages'] as const,
} as const

export const cvVersionQueryKeys = {
  all: ['career', 'cv-versions'] as const,
} as const

export const careerOverviewQueryKeys = {
  all: ['career', 'overview'] as const,
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
