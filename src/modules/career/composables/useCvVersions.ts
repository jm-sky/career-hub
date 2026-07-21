import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query'
import { cvVersionApiService } from '@/modules/career/services/cvVersionApiService'
import { cvVersionQueryKeys, profileMutationRetryFunction, profileRetryFunction } from '@/modules/career/utils/queryUtils'
import type { CreateCvVersionData, ICvVersionService, UpdateCvVersionData } from '@/modules/career/types/cvVersion.type'

export function useCvVersionsQuery(service?: ICvVersionService) {
  return useQuery({
    queryKey: cvVersionQueryKeys.all,
    queryFn: () => (service ?? cvVersionApiService).list(),
    staleTime: 60 * 1000,
    retry: profileRetryFunction,
  })
}

export function useCreateCvVersion(service?: ICvVersionService) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (data: CreateCvVersionData) => (service ?? cvVersionApiService).create(data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: cvVersionQueryKeys.all }),
    retry: profileMutationRetryFunction,
  })
}

export function useUpdateCvVersion(service?: ICvVersionService) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, data }: { id: string, data: UpdateCvVersionData }) => (service ?? cvVersionApiService).update(id, data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: cvVersionQueryKeys.all }),
    retry: profileMutationRetryFunction,
  })
}

export function useDeleteCvVersion(service?: ICvVersionService) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (id: string) => (service ?? cvVersionApiService).delete(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: cvVersionQueryKeys.all }),
    retry: profileMutationRetryFunction,
  })
}

export function useGenerateCvVersion(service?: ICvVersionService) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (id: string) => (service ?? cvVersionApiService).generate(id),
    // Generation sets pdfUrl on the version — refetch so the UI reflects it
    onSuccess: () => queryClient.invalidateQueries({ queryKey: cvVersionQueryKeys.all }),
    retry: profileMutationRetryFunction,
  })
}

export function useDownloadCvVersionPdf(service?: ICvVersionService) {
  return useMutation({
    mutationFn: (id: string) => (service ?? cvVersionApiService).downloadPdf(id),
    retry: profileMutationRetryFunction,
  })
}

export function useCvVersions(service?: ICvVersionService) {
  const cvVersionsQuery = useCvVersionsQuery(service)
  const createMutation = useCreateCvVersion(service)
  const updateMutation = useUpdateCvVersion(service)
  const deleteMutation = useDeleteCvVersion(service)
  const generateMutation = useGenerateCvVersion(service)
  const downloadMutation = useDownloadCvVersionPdf(service)

  return {
    cvVersionsQuery,
    cvVersions: cvVersionsQuery.data,
    isLoading: cvVersionsQuery.isLoading,
    isError: cvVersionsQuery.isError,
    error: cvVersionsQuery.error,
    createCvVersion: createMutation.mutateAsync,
    isCreating: createMutation.isPending,
    updateCvVersion: updateMutation.mutateAsync,
    isUpdating: updateMutation.isPending,
    deleteCvVersion: deleteMutation.mutateAsync,
    isDeleting: deleteMutation.isPending,
    generateCvVersion: generateMutation.mutateAsync,
    isGenerating: generateMutation.isPending,
    downloadCvVersionPdf: downloadMutation.mutateAsync,
    isDownloading: downloadMutation.isPending,
  }
}
