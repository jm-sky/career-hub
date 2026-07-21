import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query'
import { educationApiService } from '@/modules/career/services/educationApiService'
import { educationQueryKeys, profileMutationRetryFunction, profileRetryFunction } from '@/modules/career/utils/queryUtils'
import type { CreateEducationData, Education, IEducationService, UpdateEducationData } from '@/modules/career/types/education.type'

export function useEducationQuery(service?: IEducationService) {
  return useQuery({
    queryKey: educationQueryKeys.all,
    queryFn: () => (service ?? educationApiService).list(),
    staleTime: 60 * 1000,
    retry: profileRetryFunction,
  })
}

export function useCreateEducation(service?: IEducationService) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (data: CreateEducationData) => (service ?? educationApiService).create(data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: educationQueryKeys.all }),
    retry: profileMutationRetryFunction,
  })
}

export function useUpdateEducation(service?: IEducationService) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, data }: { id: string, data: UpdateEducationData }) => (service ?? educationApiService).update(id, data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: educationQueryKeys.all }),
    retry: profileMutationRetryFunction,
  })
}

export function useDeleteEducation(service?: IEducationService) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (id: string) => (service ?? educationApiService).delete(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: educationQueryKeys.all }),
    retry: profileMutationRetryFunction,
  })
}

export function useReorderEducation(service?: IEducationService) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (orderedIds: string[]) => (service ?? educationApiService).reorder(orderedIds),
    onSuccess: (updated: Education[]) => queryClient.setQueryData(educationQueryKeys.all, updated),
    retry: profileMutationRetryFunction,
  })
}

export function useEducation(service?: IEducationService) {
  const educationQuery = useEducationQuery(service)
  const createMutation = useCreateEducation(service)
  const updateMutation = useUpdateEducation(service)
  const deleteMutation = useDeleteEducation(service)
  const reorderMutation = useReorderEducation(service)

  return {
    educationQuery,
    education: educationQuery.data,
    isLoading: educationQuery.isLoading,
    isError: educationQuery.isError,
    error: educationQuery.error,
    createEducation: createMutation.mutateAsync,
    isCreating: createMutation.isPending,
    updateEducation: updateMutation.mutateAsync,
    isUpdating: updateMutation.isPending,
    deleteEducation: deleteMutation.mutateAsync,
    isDeleting: deleteMutation.isPending,
    reorderEducation: reorderMutation.mutateAsync,
    isReordering: reorderMutation.isPending,
  }
}
