import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query'
import { achievementApiService } from '@/modules/career/services/achievementApiService'
import { achievementQueryKeys, profileMutationRetryFunction, profileRetryFunction } from '@/modules/career/utils/queryUtils'
import type { Achievement, CreateAchievementData, IAchievementService, UpdateAchievementData } from '@/modules/career/types/achievement.type'

export function useAchievementsQuery(service?: IAchievementService) {
  return useQuery({
    queryKey: achievementQueryKeys.all,
    queryFn: () => (service ?? achievementApiService).list(),
    staleTime: 60 * 1000,
    retry: profileRetryFunction,
  })
}

export function useCreateAchievement(service?: IAchievementService) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (data: CreateAchievementData) => (service ?? achievementApiService).create(data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: achievementQueryKeys.all }),
    retry: profileMutationRetryFunction,
  })
}

export function useUpdateAchievement(service?: IAchievementService) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, data }: { id: string, data: UpdateAchievementData }) => (service ?? achievementApiService).update(id, data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: achievementQueryKeys.all }),
    retry: profileMutationRetryFunction,
  })
}

export function useDeleteAchievement(service?: IAchievementService) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (id: string) => (service ?? achievementApiService).delete(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: achievementQueryKeys.all }),
    retry: profileMutationRetryFunction,
  })
}

export function useReorderAchievements(service?: IAchievementService) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (orderedIds: string[]) => (service ?? achievementApiService).reorder(orderedIds),
    onSuccess: (updated: Achievement[]) => queryClient.setQueryData(achievementQueryKeys.all, updated),
    retry: profileMutationRetryFunction,
  })
}

export function useAchievements(service?: IAchievementService) {
  const achievementsQuery = useAchievementsQuery(service)
  const createMutation = useCreateAchievement(service)
  const updateMutation = useUpdateAchievement(service)
  const deleteMutation = useDeleteAchievement(service)
  const reorderMutation = useReorderAchievements(service)

  return {
    achievementsQuery,
    achievements: achievementsQuery.data,
    isLoading: achievementsQuery.isLoading,
    isError: achievementsQuery.isError,
    error: achievementsQuery.error,
    createAchievement: createMutation.mutateAsync,
    isCreating: createMutation.isPending,
    updateAchievement: updateMutation.mutateAsync,
    isUpdating: updateMutation.isPending,
    deleteAchievement: deleteMutation.mutateAsync,
    isDeleting: deleteMutation.isPending,
    reorderAchievements: reorderMutation.mutateAsync,
    isReordering: reorderMutation.isPending,
  }
}
