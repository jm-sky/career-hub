import { useMutation } from '@tanstack/vue-query'
import { careerAiApiService } from '@/modules/career/services/careerAiApiService'
import { profileMutationRetryFunction } from '@/modules/career/utils/queryUtils'
import type { ICareerAiService, OptimizeDescriptionData, SuggestResponsibilitiesData } from '@/modules/career/types/ai.type'

export function useOptimizeDescription(service?: ICareerAiService) {
  return useMutation({
    mutationFn: (data: OptimizeDescriptionData) => (service ?? careerAiApiService).optimizeDescription(data),
    retry: profileMutationRetryFunction,
  })
}

export function useSuggestResponsibilities(service?: ICareerAiService) {
  return useMutation({
    mutationFn: (data: SuggestResponsibilitiesData) => (service ?? careerAiApiService).suggestResponsibilities(data),
    retry: profileMutationRetryFunction,
  })
}

export function useAnalyzeProfile(service?: ICareerAiService) {
  return useMutation({
    mutationFn: (targetRole: string) => (service ?? careerAiApiService).analyzeProfile(targetRole),
    retry: profileMutationRetryFunction,
  })
}

export function useCareerAi(service?: ICareerAiService) {
  const optimizeMutation = useOptimizeDescription(service)
  const suggestResponsibilitiesMutation = useSuggestResponsibilities(service)
  const analyzeMutation = useAnalyzeProfile(service)

  return {
    optimizeDescription: optimizeMutation.mutateAsync,
    isOptimizing: optimizeMutation.isPending,
    suggestResponsibilities: suggestResponsibilitiesMutation.mutateAsync,
    isSuggestingResponsibilities: suggestResponsibilitiesMutation.isPending,
    analyzeProfile: analyzeMutation.mutateAsync,
    isAnalyzing: analyzeMutation.isPending,
  }
}
