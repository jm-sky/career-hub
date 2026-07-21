import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query'
import { languageApiService } from '@/modules/career/services/languageApiService'
import { languageQueryKeys, profileMutationRetryFunction, profileRetryFunction } from '@/modules/career/utils/queryUtils'
import type { CreateLanguageData, ILanguageService, Language, UpdateLanguageData } from '@/modules/career/types/language.type'

export function useLanguagesQuery(service?: ILanguageService) {
  return useQuery({
    queryKey: languageQueryKeys.all,
    queryFn: () => (service ?? languageApiService).list(),
    staleTime: 60 * 1000,
    retry: profileRetryFunction,
  })
}

export function useCreateLanguage(service?: ILanguageService) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (data: CreateLanguageData) => (service ?? languageApiService).create(data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: languageQueryKeys.all }),
    retry: profileMutationRetryFunction,
  })
}

export function useUpdateLanguage(service?: ILanguageService) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, data }: { id: string, data: UpdateLanguageData }) => (service ?? languageApiService).update(id, data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: languageQueryKeys.all }),
    retry: profileMutationRetryFunction,
  })
}

export function useDeleteLanguage(service?: ILanguageService) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (id: string) => (service ?? languageApiService).delete(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: languageQueryKeys.all }),
    retry: profileMutationRetryFunction,
  })
}

export function useReorderLanguages(service?: ILanguageService) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (orderedIds: string[]) => (service ?? languageApiService).reorder(orderedIds),
    onSuccess: (updated: Language[]) => queryClient.setQueryData(languageQueryKeys.all, updated),
    retry: profileMutationRetryFunction,
  })
}

export function useLanguages(service?: ILanguageService) {
  const languagesQuery = useLanguagesQuery(service)
  const createMutation = useCreateLanguage(service)
  const updateMutation = useUpdateLanguage(service)
  const deleteMutation = useDeleteLanguage(service)
  const reorderMutation = useReorderLanguages(service)

  return {
    languagesQuery,
    languages: languagesQuery.data,
    isLoading: languagesQuery.isLoading,
    isError: languagesQuery.isError,
    error: languagesQuery.error,
    createLanguage: createMutation.mutateAsync,
    isCreating: createMutation.isPending,
    updateLanguage: updateMutation.mutateAsync,
    isUpdating: updateMutation.isPending,
    deleteLanguage: deleteMutation.mutateAsync,
    isDeleting: deleteMutation.isPending,
    reorderLanguages: reorderMutation.mutateAsync,
    isReordering: reorderMutation.isPending,
  }
}
