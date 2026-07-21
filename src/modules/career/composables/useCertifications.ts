import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query'
import { certificationApiService } from '@/modules/career/services/certificationApiService'
import { certificationQueryKeys, profileMutationRetryFunction, profileRetryFunction } from '@/modules/career/utils/queryUtils'
import type { Certification, CreateCertificationData, ICertificationService, UpdateCertificationData } from '@/modules/career/types/certification.type'

export function useCertificationsQuery(service?: ICertificationService) {
  return useQuery({
    queryKey: certificationQueryKeys.all,
    queryFn: () => (service ?? certificationApiService).list(),
    staleTime: 60 * 1000,
    retry: profileRetryFunction,
  })
}

export function useCreateCertification(service?: ICertificationService) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (data: CreateCertificationData) => (service ?? certificationApiService).create(data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: certificationQueryKeys.all }),
    retry: profileMutationRetryFunction,
  })
}

export function useUpdateCertification(service?: ICertificationService) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, data }: { id: string, data: UpdateCertificationData }) => (service ?? certificationApiService).update(id, data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: certificationQueryKeys.all }),
    retry: profileMutationRetryFunction,
  })
}

export function useDeleteCertification(service?: ICertificationService) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (id: string) => (service ?? certificationApiService).delete(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: certificationQueryKeys.all }),
    retry: profileMutationRetryFunction,
  })
}

export function useReorderCertifications(service?: ICertificationService) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (orderedIds: string[]) => (service ?? certificationApiService).reorder(orderedIds),
    onSuccess: (updated: Certification[]) => queryClient.setQueryData(certificationQueryKeys.all, updated),
    retry: profileMutationRetryFunction,
  })
}

export function useCertifications(service?: ICertificationService) {
  const certificationsQuery = useCertificationsQuery(service)
  const createMutation = useCreateCertification(service)
  const updateMutation = useUpdateCertification(service)
  const deleteMutation = useDeleteCertification(service)
  const reorderMutation = useReorderCertifications(service)

  return {
    certificationsQuery,
    certifications: certificationsQuery.data,
    isLoading: certificationsQuery.isLoading,
    isError: certificationsQuery.isError,
    error: certificationsQuery.error,
    createCertification: createMutation.mutateAsync,
    isCreating: createMutation.isPending,
    updateCertification: updateMutation.mutateAsync,
    isUpdating: updateMutation.isPending,
    deleteCertification: deleteMutation.mutateAsync,
    isDeleting: deleteMutation.isPending,
    reorderCertifications: reorderMutation.mutateAsync,
    isReordering: reorderMutation.isPending,
  }
}
