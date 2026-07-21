import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query'
import { experienceApiService } from '@/modules/career/services/experienceApiService'
import { experienceQueryKeys, profileMutationRetryFunction, profileRetryFunction } from '@/modules/career/utils/queryUtils'
import type { CreateExperienceData, Experience, IExperienceService, UpdateExperienceData } from '@/modules/career/types/experience.type'

export function useExperiencesQuery(service?: IExperienceService) {
  return useQuery({
    queryKey: experienceQueryKeys.all,
    queryFn: () => (service ?? experienceApiService).list(),
    staleTime: 60 * 1000,
    retry: profileRetryFunction,
  })
}

export function useCreateExperience(service?: IExperienceService) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (data: CreateExperienceData) => (service ?? experienceApiService).create(data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: experienceQueryKeys.all }),
    retry: profileMutationRetryFunction,
  })
}

export function useUpdateExperience(service?: IExperienceService) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, data }: { id: string, data: UpdateExperienceData }) => (service ?? experienceApiService).update(id, data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: experienceQueryKeys.all }),
    retry: profileMutationRetryFunction,
  })
}

export function useDeleteExperience(service?: IExperienceService) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (id: string) => (service ?? experienceApiService).delete(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: experienceQueryKeys.all }),
    retry: profileMutationRetryFunction,
  })
}

export function useReorderExperiences(service?: IExperienceService) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (orderedIds: string[]) => (service ?? experienceApiService).reorder(orderedIds),
    onSuccess: (updated: Experience[]) => queryClient.setQueryData(experienceQueryKeys.all, updated),
    retry: profileMutationRetryFunction,
  })
}

export function useExperiences(service?: IExperienceService) {
  const experiencesQuery = useExperiencesQuery(service)
  const createMutation = useCreateExperience(service)
  const updateMutation = useUpdateExperience(service)
  const deleteMutation = useDeleteExperience(service)
  const reorderMutation = useReorderExperiences(service)

  return {
    experiencesQuery,
    experiences: experiencesQuery.data,
    isLoading: experiencesQuery.isLoading,
    isError: experiencesQuery.isError,
    error: experiencesQuery.error,
    createExperience: createMutation.mutateAsync,
    isCreating: createMutation.isPending,
    updateExperience: updateMutation.mutateAsync,
    isUpdating: updateMutation.isPending,
    deleteExperience: deleteMutation.mutateAsync,
    isDeleting: deleteMutation.isPending,
    reorderExperiences: reorderMutation.mutateAsync,
    isReordering: reorderMutation.isPending,
  }
}
